#!/usr/bin/env python3
"""
prioritize_outreach.py -- COA 8a: ranks resolved researcher contacts into a
send queue, so "who gets a drafted email first" is a repeatable, inspectable
formula instead of picked by feel each time (which is how the first three
drafts this session were actually chosen).

Priority score = leaderboard points (score_hypotheses.py's own field --
already encodes verdict + refutation survival + badges, more granular than
re-deriving a coarse tier weight) + a recency bonus off the matched paper's
year (2026 -> +20, decaying 2pts/year, unknown year -> a modest neutral +8
rather than 0 or 10 -- unknown-year Exa matches skew recent in practice, so
neither punishing nor rewarding the unknown is the honest default).

Hard gates BEFORE scoring (same discipline as every other filter in this
pipeline -- exclude first, rank second, never let a good score paper over a
bad candidate):
  1. confidence == HIGH and a real, non-empty email (no MEDIUM/LOW, no
     "resolved, no email" rows)
  2. exclude canary-* and nobel-ground-truth-* hypotheses -- calibration
     fixtures, not real ideas worth funding (same reasoning that kept
     Feynman/Seth Lloyd out of the three hand-drafted examples)
  3. exclude anyone already drafted -- scanned live from outreach/emails/*.md
     rather than a separate tracked list, so it can never drift out of sync
     with what's actually on disk

Usage:
    python3 outreach/prioritize_outreach.py [--top N] [--dry-run]
"""
import argparse
import glob
import json
import os
import re

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTACTS_PATH = os.path.join(PIPELINE_DIR, "outreach", "contacts.jsonl")
EXPERIENCE_PATH = os.path.join(PIPELINE_DIR, "experience_data.json")
EMAILS_DIR = os.path.join(PIPELINE_DIR, "outreach", "emails")
QUEUE_PATH = os.path.join(PIPELINE_DIR, "outreach", "outreach_queue.json")

CURRENT_YEAR = 2026


def load_leaderboard():
    with open(EXPERIENCE_PATH, encoding="utf-8") as f:
        data = json.load(f)
    entries = data if isinstance(data, list) else data.get("entries", data.get("rows", []))
    by_slug = {}
    for e in entries:
        slug = e.get("key")
        if slug:
            by_slug[slug] = e
    return by_slug


def load_already_drafted():
    """Scanned live from the actual files on disk, not a separate tracked
    list -- so this can never silently drift out of sync with what's
    really been drafted, the same lesson load_resolved_matches() already
    encodes for contacts.jsonl itself."""
    slugs = set()
    for path in glob.glob(os.path.join(EMAILS_DIR, "*.md")):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for m in re.finditer(r"\*\*Hypothesis:\*\*\s*`([^`]+)`", text):
            slugs.add(m.group(1))
    return slugs


def load_contacts():
    recs = []
    with open(CONTACTS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    return recs


def is_excluded(slug):
    return slug.startswith("canary-") or slug.startswith("nobel-ground-truth-")


def recency_bonus(year):
    if not year:
        return 8  # neutral default -- see module docstring
    return max(0, 20 - (CURRENT_YEAR - year) * 2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=20, help="How many to print/save (default 20)")
    parser.add_argument("--dry-run", action="store_true", help="Print only; do not write outreach_queue.json")
    args = parser.parse_args()

    by_slug = load_leaderboard()
    already_drafted = load_already_drafted()
    contacts = load_contacts()

    candidates = []
    skipped_low_conf = 0
    skipped_excluded = 0
    skipped_drafted = 0
    skipped_no_leaderboard_entry = 0

    for c in contacts:
        slug = c.get("hypothesis_slug")
        if not (c.get("resolved") and c.get("email") and c.get("confidence") == "HIGH"):
            skipped_low_conf += 1
            continue
        if is_excluded(slug):
            skipped_excluded += 1
            continue
        if slug in already_drafted:
            skipped_drafted += 1
            continue
        e = by_slug.get(slug)
        if not e:
            skipped_no_leaderboard_entry += 1
            continue
        points = e.get("points", 0)
        year = c.get("source_match_year")
        match_count = len(e.get("active_research_matches") or [])
        score = points + recency_bonus(year)
        candidates.append({
            "priority_score": score,
            "points": points,
            "tier_label": e.get("tier_label"),
            "verdict": e.get("verdict"),
            "source_match_year": year,
            "match_count": match_count,
            "hypothesis_slug": slug,
            "target_name": c.get("target_name"),
            "institution": c.get("institution"),
            "email": c.get("email"),
            "source_match_title": c.get("source_match_title"),
            "source_match_authors": c.get("source_match_authors"),
            "source_match_url": c.get("source_match_url"),
        })

    # Real ties are common (many candidates share the same points+recency
    # bucket -- 54 unique scores across 285 candidates on the first real
    # run) -- rather than leave those effectively unordered, break ties by
    # match_count: a hypothesis with 3 independently-found real papers on
    # its territory is stronger converging evidence than one with 1, even
    # at equal points+recency. Real year as the final tiebreaker.
    candidates.sort(key=lambda r: (r["priority_score"], r["match_count"], r["source_match_year"] or 0), reverse=True)

    print(f"Loaded {len(contacts)} contact records.")
    print(f"  Skipped (not HIGH confidence / no email): {skipped_low_conf}")
    print(f"  Skipped (canary/nobel-ground-truth calibration): {skipped_excluded}")
    print(f"  Skipped (already drafted): {skipped_drafted}")
    print(f"  Skipped (no matching leaderboard entry): {skipped_no_leaderboard_entry}")
    print(f"  Eligible, ranked: {len(candidates)}\n")

    top = candidates[: args.top]
    for i, c in enumerate(top, 1):
        print(f"[{i}] score={c['priority_score']} (points={c['points']}, year={c['source_match_year']}) "
              f"{c['tier_label']} | {c['target_name']} <{c['email']}> @ {c['institution'] or '?'}")
        print(f"     hypothesis: {c['hypothesis_slug']}")
        print(f"     paper: \"{c['source_match_title']}\" -- {c['source_match_url']}")

    if not args.dry_run:
        with open(QUEUE_PATH, "w", encoding="utf-8") as f:
            json.dump(candidates, f, indent=2)
        print(f"\nWrote {len(candidates)} ranked candidates to {QUEUE_PATH}")


if __name__ == "__main__":
    main()
