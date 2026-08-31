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

# 2026-08-31: the refutation gradient. Previously 0-of-3 and 1-of-3 both
# collapsed into an undifferentiated REFUTED at a flat -15 -- throwing away
# a real, already-computed ensemble-vote signal (three independent models'
# real votes, not a self-report -- see refute_hypothesis.py's
# append_ledger_refutation() docstring for why this isn't the same risk as
# the self-reported-novelty signal that was excluded from scoring the same
# day). 0-of-3 (unanimous rejection) stays the worst outcome; 1-of-3 (a
# real, genuine near-miss -- one independent lens found something worth
# keeping) is real, if weak, positive-adjacent signal, not equivalent to a
# clean sweep against the claim.
REFUTATION_POINTS = {0: -15, 1: -5, 2: 12, 3: 20}


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


def score_entry(rec, *, include_self_report: bool = False):
    """Returns (points, badges, breakdown_lines, held_out_reason_or_None).

    2026-08-31: default flipped to include_self_report=False for the MAIN
    leaderboard score too, not only the outreach-rank path. Self-report
    Distance/Tension/Fusion is near-zero predictive signal (Failure 5
    aftermath) -- that finding already excluded it from outreach_shortlist(),
    but the public leaderboard's default score kept adding it, a real,
    checkable inconsistency between what this codebase documented and what
    it did (see leaderboard rearchitecture, 2026-08-31). Self-report still
    shows in the breakdown as real, honest context -- just not as points.
    include_self_report=True is kept only for anyone who wants the old
    (documented-inconsistent) number for comparison; nothing in this
    pipeline calls it that way anymore.
    """
    points = 0
    badges = []
    breakdown = []

    mode = rec.get("mode")
    if mode in MODE_BADGE:
        badges.append(MODE_BADGE[mode])
    elif rec.get("source") == "rosetta-stone-case-study":
        badges.append("📜 Pre-existing case study")

    # 2026-08-31: real, historically-confirmed Nobel-linked discoveries, hand-
    # authored for refutation-lens calibration (control-test-nobel-calibration.md),
    # added to the public leaderboard by direct instruction. Distinct badge,
    # additive to the mode badge above (not elif) -- these carry a real mode
    # for comparability, but must never read as engine-generated.
    if rec.get("source") == "nobel-calibration-ground-truth":
        badges.append("🏆 Nobel Ground Truth (calibration benchmark, not engine-generated)")

    verdict = rec.get("verdict", "")
    if verdict == "PENDING_VERIFICATION":
        badges.append("⏳ Pending Verification")
        return 0, badges, ["Phase 2 not yet run — genuinely pending, not a verdict"], verdict
    if verdict not in CANONICAL_VERDICTS:
        return 0, badges, [f"Non-standard verdict '{verdict}' — held out of scoring, see report below"], verdict

    # Phase 1 — self-reported novelty score. Real, honest context, always
    # shown -- but not scored by default (2026-08-31), since it carries
    # near-zero predictive signal (Failure 5 aftermath).
    self_report = rec.get("self_reported_distance", rec.get("self_reported_tension"))
    if self_report is not None:
        if include_self_report:
            p = self_report * 2
            points += p
            breakdown.append(f"Phase 1 self-report ({self_report}/5): {p:+d}")
        else:
            breakdown.append(
                f"Phase 1 self-report ({self_report}/5): not scored — "
                f"near-zero predictive signal, see Failure 5"
            )

    # Phase 2 — the four-way verdict. This is DISCOVERY-CREDIT scoring --
    # whether the pipeline itself surfaced something real. Ground-truth
    # entries (source == nobel-calibration-ground-truth) don't earn this:
    # they were hand-authored from an already-known discovery, not found by
    # the engine, so awarding +30 ADJACENT_ACTIVE here would score a
    # calibration specimen as if it were a candidate find. 2026-08-31, after
    # real, independently-converging external critique (a real leaderboard
    # entry pasted into a separate model, more than once, unprompted) flagged
    # this as a category error: validity (does the claim hold up -- the
    # refutation-survival points below, kept intact) and discovery credit
    # (did the ENGINE find this -- zero for ground truth, by construction)
    # are different questions; the old flat scoring conflated them. The real
    # verdict and badge still show (Phase 2 verification is real, honest
    # data either way), just with no points attached for ground truth.
    not_valid = rec.get("not_valid_bisociation", False)
    is_ground_truth = rec.get("source") == "nobel-calibration-ground-truth"
    if verdict == "ADJACENT_ACTIVE":
        badges.append("🗺️ Frontier Research Group")
        if is_ground_truth:
            breakdown.append("Phase 2 ADJACENT_ACTIVE: +0 (ground truth — no discovery credit, see below)")
        else:
            points += 30
            breakdown.append("Phase 2 ADJACENT_ACTIVE: +30")
    elif verdict == "COLLISION":
        if not_valid:
            points -= 5
            badges.append("🚫 Not a Valid Bisociation")
            breakdown.append("Phase 2 COLLISION (not a valid bisociation): -5")
        elif is_ground_truth:
            badges.append("🏛️ Established Department")
            breakdown.append("Phase 2 COLLISION: +0 (ground truth — no discovery credit, see below)")
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

    # Adversarial refutation, if it ran -- graduated by the real 0/1/2/3-of-3
    # ensemble vote, not collapsed to a binary. See REFUTATION_POINTS above.
    refutation_verdict = rec.get("refutation_verdict")
    if refutation_verdict == "REFUTED":
        survived = rec.get("refutation_survival_count")
        if survived == 1:
            p = REFUTATION_POINTS[1]
            points += p
            badges.append("🌗 Contested (1-of-3)")
            breakdown.append(f"Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): {p:+d}")
        else:
            # survived == 0, or unknown (no count recoverable) -- default to
            # the worst outcome under uncertainty, same discipline as the
            # lenses' own "default to REFUTED" rule.
            p = REFUTATION_POINTS[0]
            points += p
            badges.append("💀 Refuted")
            breakdown.append(f"Adversarial refutation REFUTED, unanimous (0-of-3 survive): {p:+d}")
        if rec.get("refutation_independently_confirmed"):
            breakdown.append("  independently confirmed (3 separate agents, full agreement)")
    elif refutation_verdict == "SURVIVES":
        survived = rec.get("refutation_survival_count", 2)
        p = REFUTATION_POINTS.get(survived, 12)
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


TIER_LABELS = {
    0: "✅ Peer-Endorsed",
    1: "🛡️ Survived Refutation",
    2: "🗺️ Verified, Unrefuted",
    3: "⏳ Pending",
    4: "🌗 Contested",
    5: "💀 Refuted / Rejected",
}


def refutation_gradient_pct(rec):
    """The real 0/1/2/3-of-3 ensemble vote as a percentage, or None if
    refutation never ran or the count isn't recoverable. Not a self-report --
    three independent models' real votes, tallied. 2026-08-31."""
    survived = rec.get("refutation_survival_count")
    if survived is None:
        return None
    return round(100 * survived / 3)


def tier_for(rec) -> tuple:
    """Confidence tier (lower rank = better), independent of raw points.

    2026-08-31, leaderboard rearchitecture: fixes a real, checkable bug in
    the old flat-points ranking. An ADJACENT_ACTIVE entry later swept into
    refutation and REFUTED nets +30 (Phase 2) - 15 (refuted) = +15, which
    outranked a genuine NO_SIGNAL entry that SURVIVES refutation 2-of-3
    (0 base + 12 = 12) under the old single-number sort. Points still work
    as a tie-breaker WITHIN a tier (see render_leaderboard) -- they just no
    longer let a refuted claim rank above a survived one.

    2026-08-31, same day: added a Contested tier (rank 4) for a REFUTED
    verdict with a real 1-of-3 survival count -- previously indistinguishable
    from a unanimous 0-of-3 rejection. A definitive negative signal (a
    factual failure, an invalid pairing, a researcher's real dismissal, or
    the mechanical honesty check) still overrides this and lands in the
    worst tier regardless of how close refutation came -- those are separate,
    unambiguous rejections, not softened by a near-miss vote.

    Only ever called on entries that passed score_entry()'s held_out check
    (i.e. verdict is one of the four canonical outcomes), so no fallback
    tier for non-standard verdicts is needed here -- those never reach this
    function; render_leaderboard's existing held-out path handles them.
    """
    verdict = rec.get("verdict", "")
    refutation_verdict = rec.get("refutation_verdict")
    outreach_status = rec.get("outreach_status")
    not_valid = rec.get("not_valid_bisociation", False)
    slug = rec.get("hypothesis_slug") or rec.get("slug") or key_for(rec)
    flagged = hypothesis_flagged(slug)

    # Definitive negative signals beat everything, including a real
    # refutation near-miss -- separate, unambiguous rejections on their own.
    if (verdict == "FACT_CHECK_FAIL"
            or not_valid
            or outreach_status == "researcher_dismissed"
            or flagged):
        return 5, TIER_LABELS[5]

    if refutation_verdict == "REFUTED":
        if rec.get("refutation_survival_count") == 1:
            return 4, TIER_LABELS[4]  # Contested -- a real, if weak, near-miss
        return 5, TIER_LABELS[5]      # 0-of-3, or count unrecoverable -- worst, under uncertainty

    if outreach_status == "researcher_confirmed_novel":
        return 0, TIER_LABELS[0]

    if refutation_verdict == "SURVIVES":
        return 1, TIER_LABELS[1]

    if verdict in ("ADJACENT_ACTIVE", "COLLISION"):
        return 2, TIER_LABELS[2]

    # NO_SIGNAL with no refutation run yet (or PENDING_VERIFICATION, though
    # that's held out before reaching here in practice).
    return 3, TIER_LABELS[3]


PREFILTER_LOG_PATH = os.path.join(PIPELINE_DIR, "prefilter-log.jsonl")


def load_prefilter_map() -> dict:
    """slug -> latest prefilter-log.jsonl entry. Display only -- the
    pre-filter is deliberately observe-only (prefilter_observe.py's own
    docstring: fails open, gates nothing) -- this never affects points or
    tier, only what real, already-collected signal is shown alongside an
    entry. 2026-08-31, leaderboard rearchitecture (COA 2)."""
    if not os.path.exists(PREFILTER_LOG_PATH):
        return {}
    latest = {}
    with open(PREFILTER_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            slug = rec.get("slug")
            if slug:
                latest[slug] = rec  # file is append-only chronological; later wins
    return latest


def compute_prefilter_correlation(entries, prefilter_map) -> dict:
    """Real, LIVE join of prefilter-log.jsonl against the ledger by slug --
    computed fresh every run, never hardcoded, so it can't go stale as the
    ledger grows. This is the actual Phase B question the PRD and whitepaper
    have flagged as unmeasured; first computed 2026-08-31 (session control
    check), now a standing part of every leaderboard regeneration."""
    by_slug = {e.get("hypothesis_slug"): e for e in entries}

    def outcome_quality(verdict, refv):
        if verdict in ("COLLISION", "ADJACENT_ACTIVE"):
            return "good"
        if verdict == "NO_SIGNAL":
            if refv == "SURVIVES":
                return "good"
            if refv == "REFUTED":
                return "bad"
            return None  # still pending -- excluded from the rate, not counted either way
        return None

    from collections import defaultdict, Counter
    pair_type_tab = defaultdict(Counter)
    rec_tab = defaultdict(Counter)
    for slug, p in prefilter_map.items():
        e = by_slug.get(slug)
        if not e:
            continue
        oq = outcome_quality(e.get("verdict"), e.get("refutation_verdict"))
        if oq is None:
            continue
        pt = p.get("pair_type")
        if pt:
            pair_type_tab[pt][oq] += 1
        rec = p.get("recommendation")
        if rec:
            rec_tab[rec][oq] += 1

    def to_rows(tab):
        rows = []
        for k, counts in tab.items():
            total = sum(counts.values())
            if not total:
                continue
            good = counts.get("good", 0)
            rows.append((k, total, good, round(100 * good / total, 1)))
        rows.sort(key=lambda r: -r[3])
        return rows

    return {"pair_type": to_rows(pair_type_tab), "recommendation": to_rows(rec_tab)}


def compute_mode_performance(entries) -> list:
    """Real, live per-mode stats (avg points under the current, self-report-
    excluded formula; NO_SIGNAL rate). Previously computed only privately
    inside audit_agent.py's proposal-grounding snapshot -- surfaced on the
    public leaderboard for the first time 2026-08-31 (COA 4)."""
    from collections import defaultdict
    by_mode_points = defaultdict(list)
    by_mode_no_signal = defaultdict(int)
    for e in entries:
        mode = e.get("mode") or ("case-study" if e.get("source") == "rosetta-stone-case-study" else "other")
        points, badges, breakdown, held = score_entry(e)
        if held:
            continue
        by_mode_points[mode].append(points)
        if e.get("verdict") == "NO_SIGNAL":
            by_mode_no_signal[mode] += 1
    rows = []
    for mode, pts in by_mode_points.items():
        n = len(pts)
        avg = round(sum(pts) / n, 1) if n else 0
        nsr = round(by_mode_no_signal[mode] / n, 2) if n else 0
        rows.append((mode, n, avg, nsr))
    rows.sort(key=lambda r: -r[2])
    return rows


def outreach_shortlist(entries, limit: int = 10):
    """COA 5 + COA 1 + COA 2d: ADJACENT_ACTIVE preferred, no self-report,
    deprioritize flagged janusian / twice-failed honesty checks, and soft-demote
    leads that have not passed sharpen → re-verify (do not hard-drop)."""
    rows = []
    for rec in entries:
        points, badges, breakdown, held = score_entry(rec)  # self-report already excluded by default
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
    prefilter_map = load_prefilter_map()

    scored = []
    held_out = []
    for rec in entries:
        points, badges, breakdown, held_out_reason = score_entry(rec)
        if held_out_reason:
            row = {
                "key": key_for(rec),
                "domains": rec.get("domains", []),
                "verdict": rec.get("verdict", ""),
                "points": points,
                "badges": badges,
                "breakdown": breakdown,
            }
            held_out.append((row, held_out_reason))
            continue
        tier_rank, tier_label = tier_for(rec)
        slug = rec.get("hypothesis_slug") or rec.get("slug") or key_for(rec)
        pf = prefilter_map.get(slug)
        row = {
            "key": key_for(rec),
            "domains": rec.get("domains", []),
            "verdict": rec.get("verdict", ""),
            "points": points,
            "badges": badges,
            "breakdown": breakdown,
            "tier_rank": tier_rank,
            "tier_label": tier_label,
            "pair_type": pf.get("pair_type") if pf else None,
            "refutation_gradient_pct": refutation_gradient_pct(rec),
        }
        scored.append(row)

    # Tier first (real confidence signal), points as the tie-breaker within
    # a tier only -- see tier_for()'s docstring for the bug this replaces.
    scored.sort(key=lambda r: (r["tier_rank"], -r["points"]))

    lines = []
    lines.append("# Eureka Engine — Leaderboard")
    lines.append("")
    lines.append(f"**Regenerated from**: `verification-log.jsonl` ({len(entries)} entries — "
                  f"{len(scored)} scored, {len(held_out)} held out). "
                  "Do not hand-edit this file — re-run `python3 score_hypotheses.py`.")
    lines.append("")
    lines.append("Ranked by **confidence tier** first, points as a tie-breaker within a tier only "
                  "— see `score_hypotheses.py`'s `tier_for()` docstring for the real bug this replaced "
                  "(a refuted claim could outrank a genuine survivor under flat points). Self-reported "
                  "novelty is shown per entry as context but is not scored (near-zero predictive signal, "
                  "Failure 5). Tiers, high to low confidence: " +
                  " → ".join(TIER_LABELS[i] for i in range(6)) + ".")
    lines.append("")

    # COA 4 — mode performance, real and live, not hardcoded.
    mode_perf = compute_mode_performance(entries)
    if mode_perf:
        lines.append("## Department performance")
        lines.append("")
        lines.append("Per-mode averages, computed fresh from the live ledger every run — not a "
                      "one-time snapshot. A high NO_SIGNAL rate isn't a mode failing; it's that "
                      "mode's real base rate for reaching a novel, unresolved claim.")
        lines.append("")
        lines.append("| Mode | n | Avg points | NO_SIGNAL rate |")
        lines.append("|---|---|---|---|")
        for mode, n, avg, nsr in mode_perf:
            lines.append(f"| {mode} | {n} | {avg:+.1f} | {100*nsr:.0f}% |")
        lines.append("")

    # COA 2 — pre-filter / pair-type correlation, real and live.
    corr = compute_prefilter_correlation(entries, prefilter_map)
    if corr["pair_type"] or corr["recommendation"]:
        lines.append("## Pre-filter signal (Phase 0.5, observe-only)")
        lines.append("")
        lines.append("The composability pre-filter never gates generation — it only logs a signal "
                      "(see `prefilter_observe.py`). This is that signal's real, live correlation with "
                      "downstream outcome, joined by slug against the ledger fresh every run — not a "
                      "one-time control-test result.")
        lines.append("")
        if corr["pair_type"]:
            lines.append("**By pair type:**")
            lines.append("")
            lines.append("| Pair type | n | Good outcome |")
            lines.append("|---|---|---|")
            for k, total, good, rate in corr["pair_type"]:
                lines.append(f"| {k} | {total} | {rate}% |")
            lines.append("")
        if corr["recommendation"]:
            lines.append("**By pre-filter recommendation:**")
            lines.append("")
            lines.append("| Recommendation | n | Good outcome |")
            lines.append("|---|---|---|")
            for k, total, good, rate in corr["recommendation"]:
                lines.append(f"| {k} | {total} | {rate}% |")
            lines.append("")

    lines.append("## Ranking")
    lines.append("")
    lines.append("| Rank | Tier | Pairing | Points | Verdict | Refutation | Pair type | Badges |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for i, row in enumerate(scored, 1):
        domains_str = " × ".join(row["domains"]) if row["domains"] else row["key"]
        badges_str = " ".join(row["badges"]) if row["badges"] else "—"
        pt = row["pair_type"] or "—"
        gpct = row["refutation_gradient_pct"]
        ref_str = f"{gpct}% survived" if gpct is not None else "—"
        lines.append(f"| {i} | {row['tier_label']} | {domains_str} | **{row['points']:+d}** | "
                      f"{row['verdict']} | {ref_str} | {pt} | {badges_str} |")
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
        lines.append(f"### {domains_str} — {row['tier_label']} ({row['points']:+d})")
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
