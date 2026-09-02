#!/usr/bin/env python3
"""
audit_citations.py -- COA 8f: retroactive citation audit for every
drafted email whose bibliographic details were never independently
verified against real fetched content -- the 23 drafts written before
generate_email_draft.py's Exa-based rewrite (COA 8b rewrite, 2026-09-02),
which real-world testing found had a ~31% fabrication rate under the
old OpenAI-web_search-recall approach.

Cheaper than re-drafting: this reuses the same exa.get_contents() fetch
the rewrite validated, but only COMPARES the real fetched facts against
what's already written in each file's Match source line -- no OpenAI
drafting call, no re-generated question, just a citation accuracy
check. Flags discrepancies for human review; never silently rewrites a
file (that stays a deliberate, reviewed edit, same as Rajpal/Kim/Wan).

Usage:
    python3 outreach/audit_citations.py [--files pattern1 pattern2 ...]
"""
import argparse
import glob
import os
import re
import sys

from dotenv import load_dotenv
from exa_py import Exa

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAILS_DIR = os.path.join(PIPELINE_DIR, "outreach", "emails")

load_dotenv("/Users/michaeljagdeo/Downloads/talentOS-2026/.env")
EXA_API_KEY = os.getenv("EXA_AI_API_KEY")
if not EXA_API_KEY:
    raise SystemExit("EXA_AI_API_KEY is not set — add it to the vault-root .env")
exa = Exa(api_key=EXA_API_KEY)

EXA_CITATION_QUERY = "What is the exact title, journal or venue name, publication year, and full author list of this paper?"

# Already independently verified this session -- skip, don't re-spend.
ALREADY_VERIFIED = {
    "email-cryptography-x-physical-photon-emission-vajner.md",
    "email-literature-phelan.md",
    "email-reactive-control-network-enciso.md",
    "email-creative-versioning-sterman.md",
    "email-neurogrid-optimization-papageorgiou.md",
    "email-informational-mobile-system-coordination-x-physica-rajpal.md",
    "email-developmental-psychology-kim.md",
    "email-creative-narrative-arc-development-x-human-committ-wan.md",
    "email-law-x-informational-database-state-sun.md",
    "email-resonant-swarm-aronson.md",
    "email-resonant-swarm-frey.md",
}


def parse_match_source(text):
    m = re.search(r"\*\*Match source:\*\*\s*(.+)", text)
    if not m:
        return None, None
    line = m.group(1)
    url_m = re.search(r"(https?://\S+)", line)
    url = url_m.group(1).rstrip(")") if url_m else None
    return line, url


def parse_target_name(text):
    m = re.search(r"\*\*To:\*\*\s*(.+?)\s*\\<", text)
    return m.group(1).strip() if m else ""


def fetch_real(url):
    try:
        r = exa.get_contents([url], text=False, summary={"query": EXA_CITATION_QUERY})
    except Exception as e:
        return None, 0.0
    cost = r.cost_dollars.total if getattr(r, "cost_dollars", None) else 0.0
    if not r.results:
        return None, cost
    res = r.results[0]
    return {
        "title": getattr(res, "title", None),
        "published_date": getattr(res, "published_date", None),
        "summary": getattr(res, "summary", None),
    }, cost


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--files", nargs="*", help="Specific filenames to audit (default: all unverified)")
    args = parser.parse_args()

    all_files = [os.path.basename(p) for p in glob.glob(os.path.join(EMAILS_DIR, "*.md")) if os.path.basename(p) != "README.md"]
    targets = args.files if args.files else [f for f in all_files if f not in ALREADY_VERIFIED]

    print(f"Auditing {len(targets)} drafted email(s) not yet independently citation-checked...\n")
    total_cost = 0.0
    flagged = []
    for fname in sorted(targets):
        path = os.path.join(EMAILS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        already_sent = bool(re.search(r"\*\*Status:\*\*\s*SENT\b", text))
        if already_sent:
            print(f"[SKIP — SENT] {fname}")
            continue
        match_line, url = parse_match_source(text)
        target_name = parse_target_name(text)
        if not url:
            print(f"[SKIP — no URL found in Match source] {fname}")
            continue
        real, cost = fetch_real(url)
        total_cost += cost
        if real is None:
            print(f"[SKIP — fetch failed/empty] {fname}  ({url})")
            continue
        real_year = (real["published_date"] or "")[:4]
        drafted_year_m = re.search(r"\b(19|20)\d{2}\b", match_line)
        drafted_year = drafted_year_m.group(0) if drafted_year_m else None
        year_mismatch = real_year and drafted_year and real_year != drafted_year
        print(f"[{'⚠ YEAR MISMATCH' if year_mismatch else 'checked'}] {fname}")
        print(f"    Recipient: {target_name}")
        print(f"    Drafted:  {match_line[:160]}")
        print(f"    Real title: {real['title']}")
        print(f"    Real published_date: {real['published_date']}")
        print(f"    Real summary: {(real['summary'] or '')[:300]}")
        if year_mismatch:
            flagged.append(fname)
        print()

    print(f"Done. Exa spend: ${total_cost:.4f}. {len(flagged)} file(s) with a detected year mismatch: {flagged}")
    print("This only flags year mismatches mechanically -- read every 'checked' summary above too; "
          "venue/author accuracy needs a human read against the printed real summary, same as the Screen/Rajpal/Kim/Wan cases.")


if __name__ == "__main__":
    main()
