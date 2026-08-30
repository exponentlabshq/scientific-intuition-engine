#!/usr/bin/env python3
"""
Eureka Engine — Points, Badges, Leaderboard.

Reads verification-log.jsonl (the hypothesis ledger — its role has grown
from "verification log" to the full record of every generated or
pre-existing pairing this engine has touched: self-reported novelty score,
Phase 2 web-verification verdict, adversarial-refutation outcome where
applicable) and computes a points total + badge set per entry, per the
schema documented in this session's plan (Ops/Event Log.md, 2026-08-28).

Points are tied to what an outcome actually reveals about a hypothesis's
real potential, not to "did this phase complete":

  Phase 1 self-report (distance/tension x2, max 10)   -- the engine's own
      novelty confidence, later checked against reality
  Phase 2 ADJACENT_ACTIVE            +30   -- the actual target state
  Phase 2 COLLISION (genuine)         +5   -- valid reasoning, zero novelty
  Phase 2 COLLISION (not a valid       -5   -- worse than genuine collision:
      bisociation -- same-field/              the PAIRING was flawed, not
      whole-part, flagged explicitly)         just unoriginal
  Phase 2 FACT_CHECK_FAIL            -10   -- hallucinated domain facts
  Phase 2 NO_SIGNAL (unresolved)       0   -- pending
  Refutation: 3-of-3 survive         +20
  Refutation: 2-of-3 survive         +12
  Refutation: REFUTED (0 or 1 of 3)  -15   -- worse than FACT_CHECK_FAIL --
                                              the core reasoning failed
                                              under real scrutiny
  Phase 3: researcher confirms novel +50   -- strongest possible signal
  Phase 3: researcher confirms known +15   -- converts to external collision
  Phase 3: researcher dismisses      -20
  Phase 3: no response                 0   -- can't penalize silence
  Phase 4: data reconciled            +5   -- flat, once per cycle

  Actively researched                +20   -- ADDED 2026-08-28, per direct
      (real, dated, recent citation             correction: "the best hypotheses
      OR a named currently-active               are the hypotheses found to be
      researcher -- evidence-based,              actively in research." A COLLISION
      never guessed; see                         verdict alone was undervaluing this
      active_research_note)                      -- a hypothesis that independently
                                                   reproduces a living researcher's own
                                                   named framework (e.g. Andrew Lo's
                                                   Adaptive Market Hypothesis) is real,
                                                   strong validation, not "no novelty."
                                                   Orthogonal to the COLLISION/
                                                   ADJACENT_ACTIVE axis on purpose --
                                                   novelty and activity are different
                                                   questions, both worth scoring.

Entries whose `verdict` isn't one of the four canonical outcomes (e.g. the
physics/empiricism case, a single-domain argument paper the four-way rubric
never applied to) are held out of scoring entirely and reported separately
-- never silently coerced into a bucket they don't belong in.

Usage:
    python3 score_hypotheses.py            # writes leaderboard.md
    python3 score_hypotheses.py --print     # also prints the table to stdout
"""

import argparse
import json
import os

from ledger import key_for, load_latest_entries

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(PIPELINE_DIR, "verification-log.jsonl")
LEADERBOARD_PATH = os.path.join(PIPELINE_DIR, "leaderboard.md")

CANONICAL_VERDICTS = {"COLLISION", "ADJACENT_ACTIVE", "FACT_CHECK_FAIL", "NO_SIGNAL"}

MODE_BADGE = {
    "bisociation": "🧬 Bisociative",
    "janusian": "🎭 Janusian",
    "homospatial": "🪞 Homospatial",
}

REFUTATION_SURVIVAL_POINTS = {3: 20, 2: 12}  # of-3 survive -> points; 0/1 handled as REFUTED


def is_calibration_canary(rec_or_key) -> bool:
    """Prior-art canaries are calibration plants (COA 4/4b/4c), not public
    leaderboard hypotheses. They live under hypotheses/canaries/ and use
    canary-* slugs — exclude from scoring + experience assembly."""
    if isinstance(rec_or_key, dict):
        key = key_for(rec_or_key)
    else:
        key = rec_or_key or ""
    return str(key).startswith("canary-")


def load_entries():
    """2026-08-29: now the "latest entry per slug wins" read from ledger.py,
    not a raw line-by-line load. A slug re-verified after a bug fix (e.g.
    the Tavily rate-limit incident) gets exactly one row here -- its most
    recent, correct one -- instead of scoring both the old, wrong entry and
    the new, corrected one as if they were two different hypotheses.

    Canary calibration plants (canary-*) are excluded from the public
    leaderboard / experience surface — they remain on the raw ledger for
    canary_results_*.json."""
    return [e for e in load_latest_entries(LOG_PATH) if not is_calibration_canary(e)]


def score_entry(rec, *, include_self_report: bool = True):
    """Returns (points, badges, breakdown_lines, held_out_reason_or_None).

    include_self_report=False is the COA 5 outreach-rank path: Phase 2 +
    actively-researched + refute + Phase 3 only. Self-report Distance/Tension/
    Fusion is near-zero predictive signal (Failure 5 aftermath) and must not
    decide which thesis leads get shown to researchers.
    """
    points = 0
    badges = []
    breakdown = []

    mode = rec.get("mode")
    if mode in MODE_BADGE:
        badges.append(MODE_BADGE[mode])
    elif rec.get("source") == "rosetta-stone-case-study":
        badges.append("📜 Pre-existing case study")

    verdict = rec.get("verdict", "")
    if verdict == "PENDING_VERIFICATION":
        badges.append("⏳ Pending Verification")
        return 0, badges, ["Phase 2 not yet run — genuinely pending, not a verdict"], verdict
    if verdict not in CANONICAL_VERDICTS:
        return 0, badges, [f"Non-standard verdict '{verdict}' — held out of scoring, see report below"], verdict

    # Phase 1 — self-reported novelty score (excluded from outreach-rank)
    if include_self_report:
        self_report = rec.get("self_reported_distance", rec.get("self_reported_tension"))
        if self_report is not None:
            p = self_report * 2
            points += p
            breakdown.append(f"Phase 1 self-report ({self_report}/5): {p:+d}")

    # Phase 2 — the four-way verdict
    not_valid = rec.get("not_valid_bisociation", False)
    if verdict == "ADJACENT_ACTIVE":
        points += 30
        badges.append("🗺️ Frontier Research Group")
        breakdown.append("Phase 2 ADJACENT_ACTIVE: +30")
    elif verdict == "COLLISION":
        if not_valid:
            points -= 5
            badges.append("🚫 Not a Valid Bisociation")
            breakdown.append("Phase 2 COLLISION (not a valid bisociation): -5")
        else:
            points += 5
            badges.append("🏛️ Established Department")
            breakdown.append("Phase 2 COLLISION (genuine): +5")
    elif verdict == "FACT_CHECK_FAIL":
        points -= 10
        badges.append("⚠️ Retracted")
        breakdown.append("Phase 2 FACT_CHECK_FAIL: -10")
    elif verdict == "NO_SIGNAL":
        breakdown.append("Phase 2 NO_SIGNAL: +0 (pending)")

    # 2026-08-30 fix (eureka-engine-v2-prd.md Section 2.4): the mechanical
    # same-instance / comparison-word honesty checks write "Automated check
    # failed twice" into a hypothesis file when a disguised compromise
    # survives one corrective retry -- but until now, ONLY
    # outreach_shortlist() ever read that signal (as a soft demotion to a
    # completely separate outreach_points number, never the public score).
    # A flagged hypothesis that lands ADJACENT_ACTIVE is swept into
    # refutation regardless and has always been caught there (REFUTED, -15)
    # -- but that's a different check catching it on the merits, not this
    # scorer reflecting the flag itself. A flagged hypothesis that lands
    # COLLISION instead never enters that sweep at all, and scored the plain
    # +5/-5 with zero trace anywhere that it was independently caught
    # disguising a compromise. Fixed at the scorer, for every verdict path,
    # not only the ones that happen to route through refutation first.
    slug = rec.get("hypothesis_slug") or rec.get("slug") or key_for(rec)
    if hypothesis_flagged(slug):
        points -= 10
        badges.append("⚠️ Failed Honesty Check")
        breakdown.append("Mechanical honesty check failed twice (disguised compromise, uncorrected): -10")

    # Adversarial refutation, if it ran
    refutation_verdict = rec.get("refutation_verdict")
    if refutation_verdict == "REFUTED":
        points -= 15
        badges.append("💀 Refuted")
        breakdown.append("Adversarial refutation REFUTED: -15")
        if rec.get("refutation_independently_confirmed"):
            breakdown.append("  independently confirmed (3 separate agents, full agreement)")
    elif refutation_verdict == "SURVIVES":
        survived = rec.get("refutation_survival_count", 2)
        p = REFUTATION_SURVIVAL_POINTS.get(survived, 12)
        points += p
        badges.append("🛡️ Survived the Gauntlet")
        breakdown.append(f"Adversarial refutation survived ({survived}-of-3): +{p}")

    # Phase 3 — researcher outreach, if recorded
    outreach_status = rec.get("outreach_status")
    if outreach_status == "drafted":
        badges.append("📧 Outreach Drafted")
    elif outreach_status == "researcher_confirmed_novel":
        points += 50
        badges.append("✅ Peer-Endorsed")
        breakdown.append("Phase 3 researcher confirmed novel: +50")
    elif outreach_status == "researcher_confirmed_known":
        points += 15
        breakdown.append("Phase 3 researcher confirmed known: +15")
    elif outreach_status == "researcher_dismissed":
        points -= 20
        badges.append("❌ Peer-Refuted")
        breakdown.append("Phase 3 researcher dismissed: -20")

    # Phase 4 — data reconciliation
    if rec.get("data_reconciled"):
        points += 5
        breakdown.append("Phase 4 data reconciled: +5")

    # Actively researched — orthogonal to the novelty axis on purpose.
    if rec.get("actively_researched"):
        points += 20
        badges.append("🔬 Actively Researched")
        breakdown.append("Actively researched (real, current evidence): +20")

    return points, badges, breakdown, None


def hypothesis_flagged(slug: str) -> bool:
    """Twice-failed mechanical honesty check → deprioritize for outreach."""
    if not slug:
        return False
    path = os.path.join(PIPELINE_DIR, "hypotheses", f"{slug}.md")
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        return "Automated check failed twice" in f.read()


def hypothesis_sharpened(slug: str) -> bool:
    """COA 2d: hyp file carries a closed-loop revision banner."""
    if not slug:
        return False
    path = os.path.join(PIPELINE_DIR, "hypotheses", f"{slug}.md")
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        head = f.read(2500)
    return (
        "**Revision**:" in head
        or "human-sharpened" in head.lower()
        or "closed-loop" in head.lower()
        or "COA 2d" in head
    )


def outreach_shortlist(entries, limit: int = 10):
    """COA 5 + COA 1 + COA 2d: ADJACENT_ACTIVE preferred, no self-report,
    deprioritize flagged janusian / twice-failed honesty checks, and soft-demote
    leads that have not passed sharpen → re-verify (do not hard-drop)."""
    rows = []
    for rec in entries:
        points, badges, breakdown, held = score_entry(rec, include_self_report=False)
        if held:
            continue
        if rec.get("verdict") != "ADJACENT_ACTIVE":
            continue
        slug = rec.get("hypothesis_slug") or rec.get("slug") or key_for(rec)
        flagged = hypothesis_flagged(slug)
        janusian_flagged = rec.get("mode") == "janusian" and flagged
        sharpened = hypothesis_sharpened(slug) or bool(rec.get("hypothesis_revision"))
        # Soft demote: subtract so they sort below clean peers, not hard-drop
        # (a clean ADJACENT_ACTIVE janusian can still be worth a packet).
        adj = points
        if flagged:
            adj -= 25
        if janusian_flagged:
            adj -= 15
        if not sharpened:
            adj -= 20  # COA 2d: prefer send-ready sharpened leads
        rows.append({
            "slug": slug,
            "domains": rec.get("domains", []),
            "mode": rec.get("mode"),
            "outreach_points": adj,
            "raw_outreach_points": points,
            "actively_researched": bool(rec.get("actively_researched")),
            "active_research_note": rec.get("active_research_note"),
            "flagged": flagged,
            "sharpened": sharpened,
            "badges": badges,
            "breakdown": breakdown,
        })
    rows.sort(
        key=lambda r: (r["sharpened"], r["actively_researched"], r["outreach_points"]),
        reverse=True,
    )
    return rows[:limit]


def render_leaderboard(entries):
    scored = []
    held_out = []
    for rec in entries:
        points, badges, breakdown, held_out_reason = score_entry(rec)
        row = {
            "key": key_for(rec),
            "domains": rec.get("domains", []),
            "verdict": rec.get("verdict", ""),
            "points": points,
            "badges": badges,
            "breakdown": breakdown,
        }
        if held_out_reason:
            held_out.append((row, held_out_reason))
        else:
            scored.append(row)

    scored.sort(key=lambda r: r["points"], reverse=True)

    lines = []
    lines.append("# Eureka Engine — Leaderboard")
    lines.append("")
    lines.append(f"**Regenerated from**: `verification-log.jsonl` ({len(entries)} entries — "
                  f"{len(scored)} scored, {len(held_out)} held out). "
                  "Do not hand-edit this file — re-run `python3 score_hypotheses.py`.")
    lines.append("")
    lines.append("Points are tied to what an outcome reveals about real potential, not to phase "
                  "completion — see `score_hypotheses.py`'s own docstring for the full schema.")
    lines.append("")
    lines.append("## Ranking")
    lines.append("")
    lines.append("| Rank | Pairing | Points | Verdict | Badges |")
    lines.append("|---|---|---|---|---|")
    for i, row in enumerate(scored, 1):
        domains_str = " × ".join(row["domains"]) if row["domains"] else row["key"]
        badges_str = " ".join(row["badges"]) if row["badges"] else "—"
        lines.append(f"| {i} | {domains_str} | **{row['points']:+d}** | {row['verdict']} | {badges_str} |")
    lines.append("")

    if held_out:
        pending = [r for r in held_out if r[1] == "PENDING_VERIFICATION"]
        non_standard = [r for r in held_out if r[1] != "PENDING_VERIFICATION"]

        if pending:
            lines.append(f"## Pending verification ({len(pending)})")
            lines.append("")
            lines.append("Generated (Phase 1 complete) but not yet run through Phase 2 web verification — "
                         "genuinely pending, not a verdict, not silently dropped.")
            lines.append("")
            for row, _ in pending:
                domains_str = " × ".join(row["domains"]) if row["domains"] else row["key"]
                lines.append(f"- **{domains_str}**")
            lines.append("")

        if non_standard:
            lines.append("## Held out of scoring (non-standard verdict)")
            lines.append("")
            for row, reason in non_standard:
                domains_str = " × ".join(row["domains"]) if row["domains"] else row["key"]
                lines.append(f"- **{domains_str}** — verdict: \"{reason}\" — not one of the four canonical "
                             f"outcomes the point schema is built for; see its own verification file for what "
                             f"was actually found.")
            lines.append("")

    lines.append("## Score breakdown, per entry")
    lines.append("")
    for row in scored:
        domains_str = " × ".join(row["domains"]) if row["domains"] else row["key"]
        lines.append(f"### {domains_str} — {row['points']:+d}")
        lines.append("")
        for b in row["breakdown"]:
            lines.append(f"- {b}")
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Score every hypothesis in verification-log.jsonl and write leaderboard.md")
    parser.add_argument("--print", action="store_true", dest="do_print", help="Also print the leaderboard to stdout")
    parser.add_argument("--outreach", action="store_true", help="COA 5: write outreach shortlist (no self-report) to outreach/shortlist.json")
    parser.add_argument("--outreach-limit", type=int, default=10, help="Max rows in outreach shortlist")
    args = parser.parse_args()

    entries = load_entries()

    if args.outreach:
        rows = outreach_shortlist(entries, limit=args.outreach_limit)
        out_dir = os.path.join(PIPELINE_DIR, "outreach")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "shortlist.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"generated": datetime_now_iso(), "count": len(rows), "rows": rows}, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✅ Outreach shortlist ({len(rows)}) -> {out_path}")
        for i, r in enumerate(rows, 1):
            domains = " × ".join(r["domains"]) if r["domains"] else r["slug"]
            flag = " [FLAGGED]" if r["flagged"] else ""
            active = " 🔬" if r["actively_researched"] else ""
            sharp = " ✂" if r.get("sharpened") else " [NEEDS_SHARPEN]"
            print(f"  {i}. {domains}  outreach={r['outreach_points']:+d}{active}{flag}{sharp}")
        return

    output = render_leaderboard(entries)

    with open(LEADERBOARD_PATH, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"✅ Scored {len(entries)} entries -> {LEADERBOARD_PATH}")
    if args.do_print:
        print()
        print(output)


def datetime_now_iso():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    main()
