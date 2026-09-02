#!/usr/bin/env python3
"""
find_new_evidence.py -- COA 7 (2026-09-02): a second look at hypotheses
active_research_check.py already marked NO_MATCH, using Exa's search API
(category="research paper", a specifically academic-tuned index -- the
account's own docs claim ~350M papers) as a different real discovery
source than OpenAI's general-purpose web_search tool.

Two real, tested findings from prototyping this before writing it as a
script (2026-09-02, real $0.007/search cost, so budget was never the
real constraint -- result QUALITY was):

1. Exa's neural search over category="research paper" genuinely
   surfaces different, real candidates than OpenAI's web_search did for
   the same hypothesis -- confirmed directly on the Architecture x
   Cross-Domain-Pattern-Recognition hypothesis, which OpenAI's
   active_research_check.py had marked NO_MATCH.
2. Those candidates do NOT automatically survive the same rigor the
   rest of this pipeline applies. The very first candidate this script
   ever judged -- a real, genuinely topically-relevant 2025 paper on
   LLM-driven design-by-analogy -- came back NO_MATCH once judged
   against the hypothesis's actual specific claim (a statistically
   significant improvement in BOTH aesthetic AND regulatory compliance,
   not just "AI can help with design"). Exa finding a topically
   plausible paper is not the same as that paper being real leverage
   for THIS hypothesis's THIS claim -- so this script never trusts
   Exa's own relevance ranking as the verdict. It always re-runs the
   same skeptical judgment active_research_check.py already applies
   (same schema, same "same mechanism, not same neighborhood" bar),
   just fed Exa's real retrieved candidates as evidence instead of
   letting the model search for itself. A MATCH_FOUND from this script
   is exactly as hard to earn as one from active_research_check.py.

When a real MATCH_FOUND survives that judgment, this writes to the
exact same ledger field active_research_check.py writes to
(active_research_matches / actively_researched, via
verification-log.jsonl) -- not a separate, parallel data store. That is
the actual point: real evidence found here becomes real leverage
everywhere that field already matters (the +20 scoring bonus, contact
resolution eligibility via find_researcher_contact.py, and the sitewide
contact/match display), not a second, disconnected system. The ledger
entry's own active_research_method field discloses which real source
found it (Exa vs. OpenAI web_search), so provenance is never hidden.

Usage:
    python3 find_new_evidence.py <slug> [<slug> ...]
    python3 find_new_evidence.py --all-no-match [--limit N]
    python3 find_new_evidence.py --all-no-match --dry-run
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from exa_py import Exa
from openai import OpenAI

import token_tracker

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
HYPOTHESES_DIR = os.path.join(PIPELINE_DIR, "hypotheses")
LEDGER_PATH = os.path.join(PIPELINE_DIR, "verification-log.jsonl")

load_dotenv("/Users/michaeljagdeo/Downloads/talentOS-2026/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EXA_API_KEY = os.getenv("EXA_AI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
if not EXA_API_KEY:
    raise SystemExit("EXA_AI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)
exa = Exa(api_key=EXA_API_KEY)

MODEL = "gpt-4o-mini"
EXA_NUM_RESULTS = 6

# Same schema active_research_check.py uses -- this script is a second
# discovery SOURCE, not a second discovery STANDARD.
ACTIVE_RESEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["MATCH_FOUND", "NO_MATCH", "AMBIGUOUS"]},
        "matches": {
            "type": "array",
            "description": "Real, specific matches to the SAME mechanism -- empty if NO_MATCH. Only from the candidate list given.",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The real paper title, copied from the candidate list."},
                    "researcher_or_authors": {"type": "string", "description": "Real name(s) if given in the candidate list or its highlights; 'authors not specified in excerpt' if not -- never invented."},
                    "year": {"type": ["integer", "null"], "description": "Real year if known from the candidate's published_date; null if genuinely unknown."},
                    "url": {"type": "string", "description": "The real URL, copied exactly from the candidate list -- never invented."},
                    "explanation": {"type": "string", "description": "1-2 sentences: why this addresses the SAME specific mechanism, not just a shared topic."},
                },
                "required": ["title", "researcher_or_authors", "year", "url", "explanation"],
                "additionalProperties": False,
            },
        },
        "reasoning": {"type": "string", "description": "2-4 sentences, overall assessment."},
    },
    "required": ["verdict", "matches", "reasoning"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = (
    "You are checking one specific question: given a real, specific hypothesis claim, and a list of REAL "
    "candidate papers already retrieved for you by search (real titles, URLs, and excerpted highlights) -- "
    "you do not need to search further -- does any candidate genuinely address the SAME specific mechanism "
    "as the claim: the same variables, the same proposed relationship, not just a shared broad topic?\n\n"
    "Apply the discipline of a careful, skeptical reviewer, not an enthusiastic one. A paper about the "
    "general neighborhood (e.g. 'AI applied to design' when the claim is about a specific measurable "
    "outcome of a specific system) is NOT a match, even when it looks exciting or clearly relevant to the "
    "field. It has to be close enough that a domain expert would call it the same claim, not just the same "
    "neighborhood. Only cite a candidate from the list given -- never invent a title, author, year, or URL "
    "beyond what is provided; if authors are not stated in the excerpt, write 'authors not specified in "
    "excerpt' rather than guessing a name. If none of the candidates genuinely match, return NO_MATCH with "
    "an empty list, even if some are topically related. Do not stretch a tangential result into a match to "
    "make the answer more interesting than it is -- a correct NO_MATCH is exactly as valuable a result as a "
    "correct MATCH_FOUND."
)


def extract_core_claim(mode, filetext):
    if mode == "janusian":
        m = re.search(r"## 5\. The Hypothesis.*?\n(.*?)\n## 6\.", filetext, re.DOTALL)
    else:
        m = re.search(r"## 4\..*?\n(.*?)\n## 5\.", filetext, re.DOTALL)
    return m.group(1).strip() if m else "(could not extract)"


def search_candidates(domains, claim):
    query = " ".join(domains) + " — real research bearing on: " + claim[:300]
    r = exa.search(query, type="auto", num_results=EXA_NUM_RESULTS, category="research paper", contents={"highlights": True})
    candidates = []
    for x in r.results:
        candidates.append({
            "title": x.title,
            "url": x.url,
            "published_date": getattr(x, "published_date", None),
            "highlights": (getattr(x, "highlights", None) or [])[:2],  # cap per-candidate excerpt length
        })
    return candidates, r.cost_dollars.total


def judge(domains, claim, candidates, slug=None):
    text = (
        f"Domain(s): {', '.join(domains)}\n\n"
        f"The specific claim being checked:\n{claim}\n\n"
        f"Real candidate papers already retrieved:\n{json.dumps(candidates, indent=2)}"
    )
    resp = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=text,
        max_output_tokens=1400,
        text={"format": {"type": "json_schema", "name": "active_research_check", "schema": ACTIVE_RESEARCH_SCHEMA, "strict": True}},
    )
    token_tracker.log_usage("exa_second_look", MODEL, resp.usage, hypothesis_slug=slug)
    return json.loads(resp.output_text), resp.usage


def check_one(slug, e):
    domains = e.get("domains", [])
    fp = os.path.join(HYPOTHESES_DIR, f"{slug}.md")
    filetext = open(fp, encoding="utf-8").read()
    claim = extract_core_claim(e.get("mode", "bisociation"), filetext)
    candidates, exa_cost = search_candidates(domains, claim)
    result, usage = judge(domains, claim, candidates, slug=slug)
    return result, candidates, exa_cost, usage


def append_ledger_entry(slug, result):
    """Same shape and same field names as active_research_check.py's own
    append_ledger_entry -- this IS the active_research_matches field
    everywhere else in the pipeline already reads from, not a parallel
    one. active_research_method discloses the real source (Exa search +
    gpt-4o-mini judgment) so provenance is never hidden downstream."""
    most_recent_year = None
    for m in result.get("matches", []):
        y = m.get("year")
        if y and (most_recent_year is None or y > most_recent_year):
            most_recent_year = y

    entry = {
        "hypothesis_slug": slug,
        "actively_researched": result["verdict"] == "MATCH_FOUND",
        "active_research_note": result["reasoning"],
        "active_research_matches": result.get("matches", []),
        "active_research_most_recent_year": most_recent_year,
        "active_research_checked_date": datetime.now(timezone.utc).date().isoformat(),
        "active_research_method": "find_new_evidence.py (Exa research-paper search + gpt-4o-mini structured judgment)",
    }
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def main():
    parser = argparse.ArgumentParser(description="Second-look discovery pass (Exa) over hypotheses active_research_check.py already marked NO_MATCH")
    parser.add_argument("slugs", nargs="*")
    parser.add_argument("--all-no-match", action="store_true", help="Run against every ledger entry currently NO_MATCH / never actively-researched")
    parser.add_argument("--limit", type=int, default=None, help="Cap how many hypotheses to check this pass")
    parser.add_argument("--dry-run", action="store_true", help="Print results only; do not write to the ledger")
    args = parser.parse_args()

    sys.path.insert(0, PIPELINE_DIR)
    from ledger import load_latest_entries
    by_slug = {e.get("hypothesis_slug"): e for e in load_latest_entries() if e.get("hypothesis_slug")}

    slugs = list(args.slugs)
    if args.all_no_match:
        slugs.extend(
            s for s, e in by_slug.items()
            if not e.get("active_research_matches") and re.match(r"^\d{4}-\d{2}-\d{2}-", s)
        )
    if not slugs:
        raise SystemExit("Pass one or more hypothesis slugs, or use --all-no-match.")
    slugs = list(dict.fromkeys(slugs))  # de-dupe, preserve order
    if args.limit:
        slugs = slugs[: args.limit]

    print(f"Checking {len(slugs)} hypothesis(es) with Exa as a second discovery source...")
    total_exa_cost = 0.0
    match_count = 0
    for i, slug in enumerate(slugs, 1):
        e = by_slug.get(slug)
        fp = os.path.join(HYPOTHESES_DIR, f"{slug}.md")
        if not e or not os.path.exists(fp):
            print(f"[{i}/{len(slugs)}] SKIPPED (not found): {slug}")
            continue
        print(f"[{i}/{len(slugs)}] {slug} ...", flush=True)
        try:
            result, candidates, exa_cost, usage = check_one(slug, e)
            total_exa_cost += exa_cost
            n_matches = len(result.get("matches", []))
            print(f"    {result['verdict']} ({n_matches} match(es) of {len(candidates)} candidates) — Exa ${exa_cost:.4f}, {usage.total_tokens} OpenAI tokens", flush=True)
            for m in result.get("matches", []):
                print(f"      - {m.get('title')} ({m.get('year')}) — {m.get('url')}")
            if result["verdict"] == "MATCH_FOUND":
                match_count += 1
            if not args.dry_run:
                append_ledger_entry(slug, result)
        except Exception as ex:
            print(f"    ERROR: {ex}", flush=True)

    print()
    print(f"Done. {match_count}/{len(slugs)} real new matches found. Total Exa spend this pass: ${total_exa_cost:.4f}")
    if not args.dry_run:
        print("Written to verification-log.jsonl — run assemble_experience_data.py + rebuild the site to surface any new matches.")


if __name__ == "__main__":
    main()
