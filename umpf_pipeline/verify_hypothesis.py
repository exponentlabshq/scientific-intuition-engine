#!/usr/bin/env python3
"""
verify_hypothesis.py — Phase 2 of the Eureka Engine, made unattended.

Every prior verification pass in this repo was Claude-orchestrated: a live
Claude Code session ran WebSearch by hand and applied the rubric in
prompts/umpf_verification_prompt.md itself. That's the exact constraint
umpf_pipeline/readme.md's "Current limit" section and the whitepaper's
Limitations section both name — no unattended path existed. This script is
that path: real Tavily web search + GPT-4o classification against the same
four-bucket rubric, writing the same verifications/*.md and
verification-log.jsonl shapes a human-run session already produces.

Verification filenames are derived directly from the hypothesis slug
(<slug>-verification.md) so assemble_experience_data.py's substring matcher
finds them with zero VERIFICATION_FILENAME_OVERRIDES entries needed — the
mismatch that required overrides for the 2026-08-29 batch doesn't recur here.

Usage:
    python3 verify_hypothesis.py hypotheses/<file>.md [hypotheses/<file2>.md ...]
    python3 verify_hypothesis.py --all-unverified
    python3 verify_hypothesis.py --all-unverified --limit 20
    python3 verify_hypothesis.py --all-unverified --dry-run   # print verdicts, write nothing
"""
import argparse
import glob
import json
import os
import random
import re
import subprocess
import sys
import time
from datetime import date, datetime, timezone

import requests
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

from token_tracker import log_usage
from retry import call_with_retry

load_dotenv(find_dotenv(usecwd=False))
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONID_API_KEY = os.getenv("MONID_API_KEY")  # optional -- see _monid_exa_search()
if not TAVILY_API_KEY:
    raise SystemExit("TAVILY_API_KEY is not set — add it to the vault-root .env")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)

HERE = os.path.dirname(os.path.abspath(__file__))
HYPOTHESES_DIR = os.path.join(HERE, "hypotheses")
VERIFICATIONS_DIR = os.path.join(HERE, "verifications")
LEDGER_PATH = os.path.join(HERE, "verification-log.jsonl")
RUBRIC_PATH = os.path.join(HERE, "prompts", "umpf_verification_prompt.md")

VALID_VERDICTS = {"COLLISION", "ADJACENT_ACTIVE", "FACT_CHECK_FAIL", "NO_SIGNAL"}

MODE_TITLE_PREFIX = [
    (re.compile(r"^#\s*Janusian Hypothesis:"), "janusian"),
    (re.compile(r"^#\s*Homospatial Hypothesis:"), "homospatial"),
    (re.compile(r"^#\s*Hypothesis:"), "bisociation"),
]


def detect_mode(text: str) -> str:
    first_line = text.splitlines()[0].strip()
    for pattern, mode in MODE_TITLE_PREFIX:
        if pattern.match(first_line):
            return mode
    return "bisociation"


def title_and_domains(text: str, mode: str):
    first_line = text.splitlines()[0].strip()
    title = first_line.split(":", 1)[1].strip() if ":" in first_line else first_line
    if mode == "janusian":
        return title, [title]
    for sep in ["×", "⊕", " x "]:
        if sep in title:
            return title, [p.strip() for p in title.split(sep)]
    return title, [title]


def extract_section(text: str, header_pattern: str) -> str:
    m = re.search(header_pattern, text)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"\n## ", text[start:])
    end = start + nxt.start() if nxt else len(text)
    return text[start:end].strip()


def extract_core_claim(text: str, mode: str) -> str:
    if mode == "janusian":
        section = extract_section(text, r"## 5\.\s*The Hypothesis[^\n]*\n")
    else:
        section = extract_section(text, r"## 3\.\s*[^\n]*\n")
    return section or "(could not extract core claim — see full hypothesis file)"


def extract_self_score(text: str, mode: str):
    """The self-critique section is numbered differently per mode --
    bisociation and homospatial put it at '## 5.', janusian at '## 6.'
    (one extra section, 'The Simultaneous Hold', comes before it). A prior
    version of this function hardcoded '## 6.' for all three modes, which
    silently returned None for every bisociation and homospatial entry
    (confirmed against the real ledger: 28 of 45 entries verified by this
    script were missing their score entirely). Fixed to match on the
    section's actual heading text, 'Novelty & Testability Self-Critique',
    which is identical across all three modes regardless of its number --
    more robust than hardcoding a number per mode, and won't break again if
    a future prompt template reorders sections.

    The score's own label also differs by mode, not just janusian vs. the
    rest: bisociation says 'Distance score', janusian says 'Tension score',
    homospatial says 'Fusion distance' -- three distinct labels, not two."""
    section = extract_section(text, r"## \d+\.\s*Novelty & Testability Self-Critique[^\n]*\n")
    key = {
        "janusian": "Tension score",
        "homospatial": "Fusion distance",
    }.get(mode, "Distance score")
    # A second, more damaging bug lived here too: [^\d]*(\d) captures the
    # FIRST digit after the label, which for the real text
    # "Tension score (1-5): 4" is the "1" inside the range parenthetical,
    # not the actual "4" after the colon. This wasn't returning None (so
    # it never showed up as a missing-score gap) -- it was silently
    # writing a wrong-but-plausible-looking score (always 1, since every
    # label is followed by "(1-5)") into the ledger for every entry this
    # script has ever verified, undercounting real Phase 1 points in
    # score_hypotheses.py by up to 8 per affected entry. Fixed to require
    # the colon before capturing, so it skips past "(1-5)" and lands on
    # the real value.
    #
    # 2026-08-29 -- control_test_scorer.py (built in direct response to the
    # readiness audit's "no control test exists for the scorer" gap) found
    # two more real, latent bugs in this same line, neither yet observed in
    # the real 89-entry ledger (checked directly: no case drift, no
    # multi-digit values there today) but both real failure modes waiting to
    # happen at scale: (a) `(\d)` captures only the FIRST digit of the real
    # value, so a hallucinated out-of-range score like "10" would silently
    # become "1" -- the exact same shape of bug as the one this function was
    # already fixed for once; (b) the match was case-sensitive, so a model
    # writing "fusion distance" instead of "Fusion distance" would silently
    # return None -- a missing-score gap, not a wrong one, but the same
    # underlying fragility. Fixed both: `(\d+)` captures the full number,
    # and `re.IGNORECASE` makes the label match regardless of case. Regression
    # check run directly against all 76 real hypothesis files on disk after
    # this fix: 0 differences between the old and new extraction -- the fix
    # is additive-safe, not just theoretically safer.
    m = re.search(rf"{key}[^:]*:\s*(\d+)", section, re.IGNORECASE)
    return int(m.group(1)) if m else None


def extract_search_queries(text: str):
    m = re.search(r"## Search Queries\s*\n(.*)", text, re.DOTALL)
    if not m:
        return []
    block = m.group(1).strip()
    raw = re.findall(r"^\d+\.\s*(.+)$", block, re.MULTILINE)
    return [q.strip().strip('"') for q in raw if q.strip()]


def fallback_queries(domains):
    if len(domains) == 1:
        return [f"{domains[0]} paradox contradiction research"]
    return [f"{domains[0]} {domains[1]} connection research"]


def tavily_search(query: str, max_results: int = 5):
    resp = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": False,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])


# Rate-limit-shaped Tavily failures, added 2026-08-29 after a real production
# run hit sustained HTTP 432s (Tavily's own rate/quota-limit status code) on
# 11 of 17 verifications in one batch -- every query in each of those 11
# calls failed, `run_searches` silently returned an empty list, and
# `classify()` was handed "(no search results returned for any query)" as if
# that were a real, evidence-based negative finding. The classifier itself
# said so plainly in its own reasoning ("The absence of search results...
# this lack of information means the hypothesis cannot be verified") and
# STILL output a definitive NO_SIGNAL verdict -- a genuinely wrong signal
# reaching the ledger, worse than either bug the same day's frozen-run audit
# found, because it corrupts the actual Phase 2 classification, not a
# secondary score or filename. 429 is the standard rate-limit code; 432 is
# Tavily's own, confirmed directly against the real error text this run.
TAVILY_RETRYABLE_STATUSES = {429, 432}


def _tavily_search_with_retry(query: str, max_results: int = 5, max_retries: int = 3, base_delay: float = 3.0):
    """Retry a Tavily call with exponential backoff + jitter on rate-limit-
    shaped HTTP errors and on connection/timeout failures. A non-retryable
    HTTP error (auth, bad request) re-raises immediately -- same
    fail-fast-on-real-errors discipline as retry.py's OpenAI wrapper."""
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            return tavily_search(query, max_results=max_results)
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status not in TAVILY_RETRYABLE_STATUSES:
                raise
            last_exc = e
        except requests.exceptions.RequestException as e:
            last_exc = e
        if attempt == max_retries:
            break
        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
        print(f"    ! Tavily rate-limited/transient error on {query!r} (attempt {attempt + 1}/{max_retries + 1}) — retrying in {delay:.1f}s")
        time.sleep(delay)
    raise last_exc


def _monid_exa_search(query: str, max_results: int = 5, timeout: int = 45):
    """Fallback search provider, added 2026-08-29 specifically to overcome
    Tavily's rate-limit incidents (see TAVILY_RETRYABLE_STATUSES's own
    comment) -- Monid's Exa neural/keyword search (https://monid.ai),
    called via the `monid` CLI (npm i -g @monid-ai/cli) rather than a raw
    HTTP call, since Monid's own docs don't publish a plain REST contract
    and the CLI's `-j/--json` output is a clean, parseable contract that
    was directly verified working (confirmed live: a query for "Andrew Lo
    Adaptive Markets Hypothesis" returned his actual 2004 paper directly --
    the exact real-world collision the EMH canary test's Tavily-only search
    missed entirely).

    This is a paid, metered fallback ($0.01/call at time of writing) -- only
    called when Tavily's own retries are exhausted, never as the primary
    path, so it doesn't quietly become the majority of search spend. Returns
    [] (not an exception) on any failure, so a fallback that itself fails
    behaves exactly like "no results," letting the existing
    all-queries-failed -> PENDING_VERIFICATION logic still apply rather than
    crashing the whole verification pass."""
    if not MONID_API_KEY:
        return []
    body = json.dumps({"query": query, "numResults": max_results, "contents": {"text": {"maxCharacters": 800}}})
    try:
        proc = subprocess.run(
            ["monid", "run", "-p", "exa", "-e", "/search", "-i", body, "-j"],
            capture_output=True, text=True, timeout=timeout,
        )
        if proc.returncode != 0:
            print(f"    ! Monid/Exa fallback failed for {query!r}: {proc.stderr.strip()[:200]}")
            return []
        data = json.loads(proc.stdout)
        if data.get("status") != "COMPLETED":
            print(f"    ! Monid/Exa fallback did not complete for {query!r}: status={data.get('status')!r}")
            return []
        return data.get("output", {}).get("results", []) or []
    except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"    ! Monid/Exa fallback errored for {query!r}: {e}")
        return []


def run_searches(queries):
    """Returns (results, failed_query_count). The count matters: zero
    results because every query genuinely errored out (rate-limited or
    transient, even after retries and the Monid fallback) is a fundamentally
    different situation from zero results because every query succeeded and
    legitimately found nothing -- verify_one() treats them differently, see
    its own comment."""
    results = []
    failed_queries = 0
    for q in queries:
        try:
            hits = _tavily_search_with_retry(q)
        except requests.RequestException as e:
            print(f"    ! Tavily search failed for {q!r} after retries — trying Monid/Exa fallback: {e}")
            hits = _monid_exa_search(q)
            if not hits:
                failed_queries += 1
                continue
            print(f"    ✅ Monid/Exa fallback recovered {len(hits)} result(s) for {q!r}")
        for h in hits:
            results.append(
                {
                    "query": q,
                    "title": h.get("title", ""),
                    "url": h.get("url", ""),
                    "content": (h.get("content") or h.get("text") or "")[:800],
                }
            )
        time.sleep(0.25)
    return results, failed_queries


def classify(title, mode, domains, core_claim, search_results, rubric, slug=None):
    results_block = "\n\n".join(
        f"[{i + 1}] {r['title']}\nURL: {r['url']}\nQuery: {r['query']}\nSnippet: {r['content']}"
        for i, r in enumerate(search_results)
    ) or "(no search results returned for any query)"

    system_prompt = (
        "You are applying the UMPF Phase 2 verification rubric below to one "
        "hypothesis, given real web search results already gathered for it. "
        "Follow the rubric exactly, including the umbrella-trap rule under "
        "ADJACENT_ACTIVE — a generic 'both are complex systems' bridge is "
        "NO_SIGNAL, not ADJACENT_ACTIVE. Cite real titles/URLs from the "
        "results given; never invent a source. Respond with ONLY a JSON "
        "object, no prose outside it:\n\n"
        '{"verdict": "COLLISION|ADJACENT_ACTIVE|FACT_CHECK_FAIL|NO_SIGNAL", '
        '"what_was_found": "...", "reasoning": "..."}\n\n'
        f"--- RUBRIC ---\n{rubric}"
    )
    user_prompt = (
        f"Hypothesis: {title}\nMode: {mode}\nDomain(s): {', '.join(domains)}\n\n"
        f"Core claim:\n{core_claim}\n\nSearch results:\n{results_block}"
    )
    resp = call_with_retry(
        client.chat.completions.create,
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    log_usage("verification", "gpt-4o", resp.usage, hypothesis_slug=slug)
    parsed = json.loads(resp.choices[0].message.content)
    if parsed.get("verdict") not in VALID_VERDICTS:
        raise ValueError(f"Model returned an invalid verdict: {parsed.get('verdict')!r}")
    return parsed


def write_verification_md(slug, title, mode, verdict, queries, result):
    path = os.path.join(VERIFICATIONS_DIR, f"{slug}-verification.md")
    mode_label = {"bisociation": "Bisociation", "janusian": "Janusian", "homospatial": "Homospatial"}[mode]
    content = f"""# Verification: {mode_label} — {title}

**Verifies**: `hypotheses/{slug}.md`
**Verified**: {date.today().isoformat()} · **Method**: Tavily search + GPT-4o classification (`verify_hypothesis.py`, unattended)

## Verdict: **{verdict}**

## Queries
{chr(10).join(f'- `{q}`' for q in queries)}

## What was found
{result['what_was_found']}

## Reasoning
{result['reasoning']}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def append_ledger_entry(slug, mode, verdict, domains, self_score, result, queries):
    entry = {
        "hypothesis_slug": slug,
        "mode": mode,
        "verdict": verdict,
        "domains": domains,
        "verified_date": date.today().isoformat(),
        "notes": result["reasoning"],
        "verification_method": "tavily+gpt-4o (unattended, verify_hypothesis.py)",
    }
    if mode == "janusian":
        entry["self_reported_tension"] = self_score
    else:
        entry["self_reported_distance"] = self_score
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def already_verified_slugs():
    slugs = set()
    if not os.path.exists(LEDGER_PATH):
        return slugs
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            s = e.get("hypothesis_slug")
            if s:
                slugs.add(s)
    return slugs


def verify_one(filepath, rubric, dry_run=False):
    slug = os.path.splitext(os.path.basename(filepath))[0]
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    mode = detect_mode(text)
    title, domains = title_and_domains(text, mode)
    core_claim = extract_core_claim(text, mode)
    self_score = extract_self_score(text, mode)
    queries = extract_search_queries(text) or fallback_queries(domains)

    print(f"  → [{mode}] {title}")
    print(f"    queries: {queries}")
    search_results, failed_queries = run_searches(queries)
    print(f"    {len(search_results)} search results gathered" + (f" ({failed_queries} of {len(queries)} queries failed after retries)" if failed_queries else ""))

    if not search_results and failed_queries == len(queries):
        # Every single query failed outright (rate-limited or transient),
        # not "searched successfully and found nothing." Don't let classify()
        # guess a verdict from zero real evidence -- that's how a real
        # infrastructure hiccup turned into a false NO_SIGNAL reaching the
        # ledger (see run_searches()'s own comment for the incident this
        # fixes). PENDING_VERIFICATION already exists as a real, handled
        # status in score_hypotheses.py (held out of scoring) and
        # assemble_experience_data.py (skips the verification-file lookup)
        # -- this is the first code path that actually writes it, closing a
        # gap where it was previously only ever set by hand.
        #
        # Known, disclosed scope limit: already_verified_slugs() below still
        # treats a PENDING_VERIFICATION entry as "done," so --all-unverified
        # will not automatically retry it on its own -- same as the original
        # 2026-08-29 Failure 3 precedent, where PENDING_VERIFICATION entries
        # were resolved by an explicit, deliberate re-run naming the specific
        # files. Building automatic re-queueing would mean rewriting past
        # ledger lines rather than only ever appending to it, which is a
        # real, separate design question -- not one to settle inside this fix.
        print(f"    ⚠️  All {len(queries)} queries failed even after retries — marking PENDING_VERIFICATION rather than guessing a verdict from no evidence.")
        verdict = "PENDING_VERIFICATION"
        result = {
            "what_was_found": "No search results — every query failed (rate-limited or a transient network error), even after retries.",
            "reasoning": (
                f"All {len(queries)} search queries for this hypothesis failed before any results were "
                "gathered, even after retrying with backoff. This is not a real negative finding -- "
                "verification could not run at all. Re-run `verify_hypothesis.py` explicitly against this "
                "file once the search API is healthy."
            ),
        }
    else:
        result = classify(title, mode, domains, core_claim, search_results, rubric, slug=slug)
        verdict = result["verdict"]
    print(f"    verdict: {verdict}")

    if dry_run:
        return slug, verdict, None

    md_path = write_verification_md(slug, title, mode, verdict, queries, result)
    append_ledger_entry(slug, mode, verdict, domains, self_score, result, queries)
    return slug, verdict, md_path


def main():
    parser = argparse.ArgumentParser(description="Unattended Phase 2 verification (Tavily + GPT-4o)")
    parser.add_argument("files", nargs="*", help="Specific hypothesis .md files to verify")
    parser.add_argument("--all-unverified", action="store_true", help="Verify every hypothesis not yet in the ledger")
    parser.add_argument("--limit", type=int, default=None, help="Cap how many to run this pass (used with --all-unverified)")
    parser.add_argument("--dry-run", action="store_true", help="Print verdicts only; write nothing")
    args = parser.parse_args()

    with open(RUBRIC_PATH, "r", encoding="utf-8") as f:
        rubric = f.read()

    if args.all_unverified:
        verified = already_verified_slugs()
        candidates = sorted(glob.glob(os.path.join(HYPOTHESES_DIR, "*.md")))
        targets = [f for f in candidates if os.path.splitext(os.path.basename(f))[0] not in verified]
        if args.limit:
            targets = targets[: args.limit]
    else:
        if not args.files:
            raise SystemExit("Pass hypothesis file(s), or use --all-unverified")
        targets = args.files

    if not targets:
        print("Nothing to verify — every hypothesis already has a ledger entry.")
        return

    print(f"Verifying {len(targets)} hypothesis file(s){' (dry run)' if args.dry_run else ''}...\n")
    summary = []
    for fp in targets:
        try:
            slug, verdict, md_path = verify_one(fp, rubric, dry_run=args.dry_run)
            summary.append((slug, verdict))
        except Exception as e:
            print(f"    ! FAILED on {fp}: {e}")
            summary.append((os.path.basename(fp), f"ERROR: {e}"))
        print()

    print("=" * 60)
    print(f"Done. {len(summary)} processed.")
    for slug, verdict in summary:
        print(f"  {verdict:12s} {slug}")


if __name__ == "__main__":
    main()
