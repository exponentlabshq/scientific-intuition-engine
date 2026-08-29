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
import re
import sys
import time
from datetime import date, datetime, timezone

import requests
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

from token_tracker import log_usage

load_dotenv(find_dotenv(usecwd=False))
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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
    section = extract_section(text, r"## 6\.\s*[^\n]*\n")
    key = "Tension score" if mode == "janusian" else "Distance score"
    m = re.search(rf"{key}[^\d]*(\d)", section)
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


def run_searches(queries):
    results = []
    for q in queries:
        try:
            hits = tavily_search(q)
        except requests.RequestException as e:
            print(f"    ! Tavily search failed for {q!r}: {e}")
            continue
        for h in hits:
            results.append(
                {
                    "query": q,
                    "title": h.get("title", ""),
                    "url": h.get("url", ""),
                    "content": (h.get("content") or "")[:800],
                }
            )
        time.sleep(0.25)
    return results


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
    resp = client.chat.completions.create(
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
    search_results = run_searches(queries)
    print(f"    {len(search_results)} search results gathered")

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
