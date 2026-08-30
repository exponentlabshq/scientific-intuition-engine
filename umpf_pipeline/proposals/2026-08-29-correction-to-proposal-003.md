# Correction to Proposal 003 — the underlying signal was corrupted, and once fixed, doesn't exist

**Date**: 2026-08-29 · **Written by**: manual review (not audit_agent.py) · **Status**: **canonical disposition for proposal 003** — no filter shipped

Michael asked to fix proposal 003's pre-verification filter logic directly. Investigating it surfaced a
real bug upstream of the filter, in `verify_hypothesis.py` itself — fixing that changed the answer to
whether a filter should exist at all.

## What was actually broken

`extract_self_score()` had two real bugs, not one:

1. **Wrong section number.** It hardcoded `## 6.` as the self-critique section for every mode. That's
   only correct for Janusian (which has an extra section, "The Simultaneous Hold," before it).
   Bisociation and homospatial both put the self-critique at `## 5.` — so the function was reading the
   wrong section entirely for those two modes.
2. **Wrong digit captured, silently.** The regex `{key}[^\d]*(\d)` grabs the *first* digit after the
   label. The real text reads `**Distance score (1-5)**: 4 — ...` — the first digit after the label is
   the "1" inside "(1-5)", not the real value "4" after the colon. This bug didn't produce an error or a
   missing value — it produced a plausible-looking wrong one. Every single score this script has ever
   captured for every mode came out as `1`, regardless of what the hypothesis actually self-reported.

Together: 39 of 39 ledger entries verified by `verify_hypothesis.py` had a wrong score. 28 came out `None`
(bisociation/homospatial, wrong section — nothing there to match at all) and 11 came out silently `1`
instead of their real value (janusian, right section, wrong digit). Both bugs are fixed now (matching on
the section's heading text instead of a hardcoded number; requiring the colon before capturing so `(1-5)`
gets skipped). Verified against one real file per mode before trusting it, then backfilled all 39 affected
entries from their real hypothesis files and re-ran `score_hypotheses.py`.

## Why this kills proposal 003's premise, not just its code

Proposal 003's filter needed the self-report score to actually distinguish likely-`NO_SIGNAL` hypotheses
from the rest. With the real, corrected data:

| Score | n | NO_SIGNAL rate |
|---|---|---|
| 3 | 2 | 0% |
| **4** | **57** | **35%** |
| 5 | 7 | 0% |

57 of 66 scored entries cluster at exactly 4 — the model overwhelmingly self-reports the same value
regardless of mode or outcome. That bucket's 35% NO_SIGNAL rate is statistically indistinguishable from
the pool's overall rate; the 3 and 5 buckets are too small (n=2, n=7) to mean anything. There is no real
variance here to filter on. The apparent signal in proposal 003's own analysis (bisociation's 39%
NO_SIGNAL rate, which is real and still true) was never actually connected to the self-report score in a
way that would let a *pre*-verification filter act on it — and now that the score data is correct instead
of corrupted, there's nothing to build that filter out of.

## What this actually resolves

- **No filter shipped.** Writing one now, on this signal, would be re-packaging the same non-signal in
  correct-looking code — worse than proposal 003's broken version, because it would look trustworthy.
- **A real, separate win instead:** 39 ledger entries had systematically wrong Phase 1 self-report points
  (`score_hypotheses.py` awards `self_report × 2`) — every one of them undercounted, several by up to 8
  points. All 39 are now correct, and the leaderboard has been rescored and republished.
- **The real, still-open question:** bisociation's 39% NO_SIGNAL rate is real and unexplained by self-report
  score. If it's worth acting on, the actual next step is finding what *does* predict it — which isn't
  yet known, and shouldn't be guessed at without evidence, the same discipline this project has held to
  everywhere else.

## Promotion checklist

- [x] Bug found, root-caused against real files, fixed in `verify_hypothesis.py`
- [x] Fix verified against one real file per mode before trusting it at scale
- [x] All 39 affected ledger entries backfilled from real hypothesis files, not estimated
- [x] Leaderboard rescored and republished
- [x] Original premise re-tested against corrected data before deciding whether to build the filter
- [x] No filter built, because the data no longer supports one — reported here rather than shipped anyway
