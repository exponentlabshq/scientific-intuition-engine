# Adversarial Refutation — Control Test 2 (Calibration, not a real NO_SIGNAL case)

**Purpose**: `control-test-calibration.md`'s own honest conclusion named exactly what was still
missing: control test 1 reused a real hypothesis (Human Trust Variance × Cryptography) whose §3
functor turned out to equivocate on a specific polysemous word ("trust"), and its final paragraph
flagged that as "a real limitation of this test itself" — the open question left standing was
whether a hypothesis *without* that specific weakness would survive, or whether refutation simply
kills everything regardless. This is a second, independent test built to answer that, using a
different real hypothesis chosen specifically to avoid control test 1's exact failure shape.

**Subject selection, disclosed rather than cherry-picked toward a result**: rather than hand-construct
a synthetic "clean" hypothesis (a real option, and possibly still a good future step — see below),
this test screened the 27 real, never-refuted, currently ADJACENT_ACTIVE bisociation hypotheses in
the live pool for one specific, principled, pre-registered criterion: does §4 (The Hypothesis) avoid
the "— or vice versa" direction-agnostic hedge that sank control test 1's Testability lens? That
screen surfaced a real, useful, disclosed finding on its own — **5 of the first 6 real hypotheses
checked used that exact hedge** — before landing on the one clean case:
`2026-08-29-immunology-x-military-strategy` (Immunology × Military Strategy, real leaderboard entry,
never previously refuted). Its §3 functor also shares no obviously polysemous noun between domains
(unlike "trust" or "tension" in other real pool entries checked along the way) — a second, independent
reason it looked like the best real candidate to test control test 1's open question against.

**Method**: identical protocol to every real case and to control test 1 — `refute_hypothesis.py`,
three independent OpenAI completions, one per lens, each blind to the other two and to this
hypothesis's real ADJACENT_ACTIVE status. Run twice for real: once via `--dry-run` (verdict only,
confirms nothing gets written to the real ledger — this hypothesis keeps its real, current, unflagged
leaderboard status regardless of this test's outcome, same discipline as control test 1), once more
directly against `run_lens()` to capture full reasoning text for this record.

## Tally: 0 of 3 survive → **REFUTED** (control test result, not counted toward the real ledger record)

- **Coherence — REFUTED.** "The hypothesis equivocates on the term 'adaptive' by using it to
  describe both immune responses and military strategies without demonstrating a genuine structural
  mapping. The claim relies on context-dependent similarities rather than a coherent, same-instance
  paradox or fusion. The mapping is more of a side-by-side comparison than a true bisociation."
- **Testability — REFUTED.** "The hypothesis lacks a clear operationalized test for its core claim...
  it does not specify a named metric, comparison condition, or rejection threshold that would allow
  for a definitive test of this mapping." (Notably: this hypothesis has no "or vice versa" hedge at
  all — it still failed Testability, on a different, real, and independent basis. The hedge is a real,
  disclosed, recurring pattern in the pool, but this result shows it is not the *only* way a hypothesis
  fails this lens.)
- **Triviality — REFUTED.** "The hypothesis reduces to a generic analogy between two complex adaptive
  systems: immune responses and military strategies both adapt to changing conditions based on
  feedback. This is a common feature of many complex systems, not a specific insight unique to these
  domains... falling into the umbrella trap." — the identical failure shape Section 6's own
  umbrella-trap rule was written to catch (first found in a real Neuroscience×Climatology case).

## What this actually tells us, read against control test 1

Two independent real tests, on two structurally different real hypotheses, chosen specifically to
avoid repeating each other's known weakness, converged on the same underlying finding through two
different specific mechanisms: control test 1's functor borrowed a word ("trust") that means something
precise and load-bearing in one domain and something looser in the other; control test 2's functor
borrowed a word ("adaptive") the same way. Both were independently caught by Coherence as equivocation
*and* independently caught by Triviality as an umbrella-trap generality — not just one lens agreeing
with itself, but two different lenses, reasoning independently, both landing on the same real
structural gap in two different real cases.

This is real evidence *against* "the lenses simply refute everything regardless of content" — a
rubric with no real discrimination would not be expected to name the *same specific failure shape*
(a loosely-shared connecting word standing in for real structural correspondence) twice, independently,
across two hypotheses chosen specifically to not share a surface-level weakness. It is evidence *for*
a real, specific, recurring generation-quality gap: this pipeline's three modes are good at finding
domain pairs where *something* connects, and consistently weaker at forcing that connection to cash
out as a precise, non-metaphorical structural mapping rather than a well-chosen shared word.

**What this still does not resolve, disclosed plainly rather than oversold:** two real tests is not
proof no hypothesis in the pool could survive — it is evidence about the *specific failure mode* found
twice, not a census. The still-open step control test 1 named — a hand-constructed hypothesis engineered
specifically to have zero shared connecting vocabulary and a fully cashed-out, mechanistic, one-directional
functor — was deliberately not attempted here: constructing one rigorously, without either accidentally
reproducing real prior art or introducing the tester's own bias toward a "survives" result, is real
research work in its own right, not a same-session extension of this screen. Naming it as the next step
rather than attempting a rushed version of it is the same discipline this project applies everywhere else
— a partial, honest answer over a complete-looking one that cuts a corner to get there.

**A secondary, disclosed finding from the screening pass itself:** the "— or vice versa" hedge in §4
appeared in 5 of the first 6 real bisociation hypotheses checked while looking for a clean control-test-2
candidate. This was not the project's known-and-fixed hedge pattern (that was Failure 1/4's Janusian
same-instance problem, in a structurally different section) — it is the same underlying testability
weakness, in bisociation's §4, never named or fixed before now. Flagged here as a real, disclosed,
unaddressed gap; not fixed as part of this pass, since fixing it changes hypothesis generation itself
and deserves its own dedicated pass with its own before/after measurement, not a fix bundled quietly
into a calibration test.
