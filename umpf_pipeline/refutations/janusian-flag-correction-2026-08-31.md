# Retroactive Correction — 121 Real Janusian Same-Instance Flags Were False Positives

**Date:** 2026-08-31
**Purpose:** closes the loop on Failure 4's real fix (Section 16, whitepaper) by asking the obvious next question directly: given the scan-scope bug is now fixed, how many of the *historical* 128 flagged Janusian hypotheses were wrongly flagged by it, not genuinely disguised compromises?

## Method — zero-cost, no new LLM calls

The fix changed *what text gets scanned* (paradox_option + the simultaneous-hold sentence only, not the whole combined blob including the deliberately-hedgy compromise option), not the generation process itself. That means the question "would this old hypothesis have passed under the new scan" can be answered directly against text that already exists on disk, by re-running the same regex scan with the corrected scope — no regeneration, no API spend.

All 128 real Janusian hypothesis files still carrying the `Automated check failed twice` flag were parsed (two real historical template eras required two extraction paths — the current numbered-field format, and an older, single-paragraph format predating it), then re-scanned:
- `find_violations()` against paradox_option + simultaneous-hold sentence only (the corrected scope)
- `has_hold_form` against the full six-field text (unchanged scope — this part of the check was never buggy)

## Result: 121 of 128 (94.5%) were false positives

Only 7 files genuinely still fail under the corrected scan — real, remaining context-split language actually present in their own paradox_option or hold sentence:

- `2026-08-29-janusian-cognitive-neuron-activation.md` — "depending on"
- `2026-08-29-janusian-swarm-robotics.md` — "in some instances", "in other instances"
- `2026-08-30-janusian-informational-routing-policy-enforcement.md` — "depending on"
- `2026-08-31-janusian-agriculture-2.md` — "depending on"
- `2026-08-31-janusian-game-theory.md` — "depending on"
- `2026-08-31-janusian-human-trust-variance.md` — "context-dependent"
- `2026-08-31-janusian-social-psychology.md` — "in some situations"

These 7 keep their flag, correctly.

## The correction, and a real bug caught mid-fix

The stale flag text on each of the 121 confirmed false positives was replaced with an honest correction note, since `score_hypotheses.py`'s `hypothesis_flagged()` reads the exact string `"Automated check failed twice"` from the file — the flag *is* the file, per this project's own established discipline, so correcting the file's text is what actually fixes downstream scoring.

The first correction pass introduced a real bug, caught before it was trusted: the correction note quoted the original flag phrase for transparency ("the 'Automated check failed twice' flag...") — which meant the literal trigger substring `hypothesis_flagged()` checks for was still present in the file, so the "fix" did not actually clear the flag. Caught by directly re-checking the real flagged-file count after the first pass (still 128, not 7) rather than trusting the correction script's own success message. Fixed with a second pass rewriting the note to convey the same information without the trigger phrase, verified this time by checking the new text does not contain it before writing, and by re-counting real flagged files afterward (7, matching the genuine remainder exactly).

## Real, honest effect on the live leaderboard

Of the 121 corrected entries, checked directly against their current, real tier assignment:

| Current tier | n |
|---|---|
| 💀 Refuted / Rejected | 89 |
| 🗺️ Verified, Unrefuted | 23 |
| 🛡️ Survived Refutation | 7 |
| 🌗 Contested | 2 |

**32 entries genuinely moved out of the worst tier** as a direct result of this correction. **89 correctly remain in Refuted/Rejected** — their generation-time flag was a real false positive, but they were also, separately, legitimately refuted by real adversarial scrutiny (or carry a different definitive negative signal), and clearing a wrongly-triggered mechanical flag does not retroactively undo a real, independently-run refutation verdict. Those two checks test different things and this correction only touches one of them.

## What this does not do

No verification verdict and no refutation verdict was touched, reversed, or re-run for any of these 121 entries. This correction is scoped entirely to the generation-time honesty-check flag and its downstream scoring effect (the &minus;10 point penalty and the "⚠️ Failed Honesty Check" badge/tier override) — nothing else.
