#!/usr/bin/env python3
"""
verify_hypothesis.py — Phase 2 of the Eureka Engine, made unattended.

Every prior verification pass in this repo was Claude-orchestrated: a live
Claude Code session ran WebSearch by hand and applied the rubric in
prompts/umpf_verification_prompt.md itself. That's the exact constraint
umpf_pipeline/readme.md's "Current limit" section and the whitepaper's
Limitations section both name — no unattended path existed. This script is
that path.

2026-08-29, cut over from a third-party search dependency to OpenAI's own
Responses API `web_search` tool. Earlier the same day this file grew a real
Tavily-outage story: sustained HTTP 432s corrupted 11 real verdicts in one
batch, fixed with retry/backoff, a `PENDING_VERIFICATION` status, a circuit
breaker, and a paid Monid/Exa fallback -- a lot of real, working machinery
built specifically to keep one third-party search vendor's unreliability
from reaching the ledger. All of it is gone now, not just patched around:
`client.responses.create(model="gpt-4o-mini", tools=[{"type": "web_search"}])`
does real, live web search AND classification in a single OpenAI call, so
there is no longer a second vendor whose outage is a distinct failure mode
from OpenAI's own. Proven directly before the cutover: a real test query
("Andrew Lo Adaptive Markets Hypothesis") that Tavily's own generated
queries had completely missed came back correctly, cited from the real
MIT-hosted PDF, on the first try -- and a second real test found the actual
named researcher (Marco Dorigo, ant colony optimization) gpt-4o-mini
specifically. One vendor now for the entire pipeline; if OpenAI itself is
down, every stage is down together, which was already the accepted failure
mode elsewhere in this pipeline, not a new risk this introduces.

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
import re
import sys
from datetime import date, datetime, timezone

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

from ledger import load_latest_entries
from token_tracker import log_usage
from retry import call_with_retry

load_dotenv(find_dotenv(usecwd=False))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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


def load_rubric() -> str:
    with open(RUBRIC_PATH, "r", encoding="utf-8") as f:
        return f.read()


def classify(title, mode, domains, core_claim, queries, rubric, slug=None):
    """Single-call verification: OpenAI's Responses API `web_search` tool
    does real, live web search AND classification together. Replaces the
    prior two-step architecture (a separate Tavily/Monid search-gathering
    pass, then this function classifying pre-gathered snippets) -- see this
    file's module docstring for why. `queries` (the hypothesis's own
    generated Search Queries, including its named-entity requirement) are
    passed as a starting point, not a hard limit -- the model can search
    adaptively beyond them, which a fixed pre-generated list never could."""
    suggested = "\n".join(f"- {q}" for q in queries) if queries else "(none suggested — search based on the hypothesis itself)"
    system_prompt = (
        "You are applying the UMPF Phase 2 verification rubric below to one "
        "hypothesis. Use the web_search tool to find real evidence before "
        "classifying — search adaptively; the suggested queries below are a "
        "starting point, not a limit. Follow the rubric exactly, including "
        "the umbrella-trap rule under ADJACENT_ACTIVE — a generic 'both are "
        "complex systems' bridge is NO_SIGNAL, not ADJACENT_ACTIVE. Cite "
        "real titles/URLs from what you actually find; never invent a "
        "source. Keep what_was_found to 3-4 sentences -- concise, not a "
        "transcript of everything found. Respond with ONLY a JSON object, "
        "no prose outside it, no markdown fences:\n\n"
        '{"verdict": "COLLISION|ADJACENT_ACTIVE|FACT_CHECK_FAIL|NO_SIGNAL", '
        '"what_was_found": "...", "reasoning": "..."}\n\n'
        f"--- RUBRIC ---\n{rubric}"
    )
    user_prompt = (
        f"Hypothesis: {title}\nMode: {mode}\nDomain(s): {', '.join(domains)}\n\n"
        f"Core claim:\n{core_claim}\n\nSuggested search starting points:\n{suggested}"
    )

    # Real failure mode found the first time this ran at real scale
    # (2026-08-29, re-confirmed 2026-08-30 at n=40): a tool-augmented call
    # sometimes returns JSON missing a required key -- and the raw text
    # confirmed it directly (2026-08-30): the string cuts off mid-word
    # ("...specifically named \"Crea) -- an output-length truncation
    # signature, not the model choosing to omit a field. A single retry
    # wasn't always enough: 2 of 4 real cases in one batch failed twice in a
    # row before this fix. Two real mitigations, not just a bigger retry
    # budget: an explicit generous max_output_tokens (removes the likely
    # ceiling being hit) and an instruction to keep what_was_found to 3-4
    # sentences (removes the pressure that was filling the budget before
    # "reasoning" ever got written). Retries bumped 1 -> 2 as a backstop,
    # not the primary fix.
    last_error = None
    for attempt in range(3):
        resp = call_with_retry(
            client.responses.create,
            model="gpt-4o-mini",
            tools=[{"type": "web_search"}],
            instructions=system_prompt,
            input=user_prompt,
            max_output_tokens=4000,
        )
        log_usage("verification", "gpt-4o-mini", resp.usage, hypothesis_slug=slug)
        text = resp.output_text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*\n", "", text)
            text = re.sub(r"\n```\s*$", "", text)
        try:
            parsed = json.loads(text)
            if parsed.get("verdict") not in VALID_VERDICTS:
                raise ValueError(f"Model returned an invalid verdict: {parsed.get('verdict')!r}")
            missing = [k for k in ("what_was_found", "reasoning") if k not in parsed]
            if missing:
                raise ValueError(f"Model JSON missing required key(s): {missing}")
            return parsed
        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            if attempt < 2:
                print(f"    ! Malformed classifier JSON ({e}) — retrying ({attempt + 1}/2): {text[:150]!r}")
    raise last_error


def write_verification_md(slug, title, mode, verdict, queries, result):
    path = os.path.join(VERIFICATIONS_DIR, f"{slug}-verification.md")
    mode_label = {"bisociation": "Bisociation", "janusian": "Janusian", "homospatial": "Homospatial"}[mode]
    content = f"""# Verification: {mode_label} — {title}

**Verifies**: `hypotheses/{slug}.md`
**Verified**: {date.today().isoformat()} · **Method**: OpenAI web_search (gpt-4o-mini) + classification, single call (`verify_hypothesis.py`, unattended)

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
        "verification_method": "openai-web-search+gpt-4o-mini (unattended, verify_hypothesis.py)",
    }
    if mode == "janusian":
        entry["self_reported_tension"] = self_score
    else:
        entry["self_reported_distance"] = self_score
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def already_verified_slugs():
    """2026-08-29: reads ledger.py's "latest entry per slug" view (a slug
    re-verified after a bug fix is judged by its newest entry, not stuck
    forever on a superseded one), and no longer counts PENDING_VERIFICATION
    as "done." Closes a real gap: PENDING_VERIFICATION was added specifically
    for when every search query fails even after retries -- if that verdict
    counted as "verified," --all-unverified would never naturally retry it,
    and it would need a human to name the file explicitly forever, the same
    as the original 2026-08-29 Failure 3 precedent. Now a hypothesis whose
    latest attempt landed PENDING_VERIFICATION is picked back up
    automatically the next time --all-unverified runs."""
    return {
        e.get("hypothesis_slug")
        for e in load_latest_entries()
        if e.get("hypothesis_slug") and e.get("verdict") != "PENDING_VERIFICATION"
    }


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
    print(f"    suggested queries: {queries}")
    # 2026-08-29: no more separate search-gathering step or PENDING_VERIFICATION
    # branch here -- classify() does real web search and classification in one
    # OpenAI call now (see module docstring). If OpenAI itself is unreachable
    # even after call_with_retry's retries, this raises and main()'s per-file
    # try/except reports it as a failure with no ledger entry written -- which
    # already means --all-unverified retries it automatically next time,
    # without needing a distinct PENDING_VERIFICATION status for a provider
    # that's now the same one every other stage in this pipeline depends on.
    result = classify(title, mode, domains, core_claim, queries, rubric, slug=slug)
    verdict = result["verdict"]
    print(f"    verdict: {verdict}")

    if dry_run:
        return slug, verdict, None

    md_path = write_verification_md(slug, title, mode, verdict, queries, result)
    append_ledger_entry(slug, mode, verdict, domains, self_score, result, queries)
    return slug, verdict, md_path


def main():
    parser = argparse.ArgumentParser(description="Unattended Phase 2 verification (OpenAI web_search + gpt-4o-mini)")
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
