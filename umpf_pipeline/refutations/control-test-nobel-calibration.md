# Adversarial Refutation — Control Test 3 (Nobel Ground Truth, Not a Real NO_SIGNAL Case)

**Date:** 2026-08-31
**Purpose:** Control tests 1 and 2 (`control-test-calibration.md`, `control-test-calibration-2.md`) each found a real, specific flaw in a real hypothesis — an equivocation on "trust," then on "adaptive." Both were read as evidence *for* the lenses catching a real, recurring generation gap, not evidence the lenses simply refute everything. But neither test answered the question named twice in this report's own Limitations section and never attempted: **has refutation ever been given a claim with no real flaw to find — something true, precise, and already vindicated — to see whether it is even capable of returning SURVIVES?** This test runs that experiment directly, for the first time.

**Method, disclosed in full:** five real, historically-confirmed, Nobel-linked pairs from `bisociation_gold_pairs.json` — not generated candidates, not hand-picked for a favorable result, chosen for being unambiguous ground truth (Kahneman & Tversky, Watson/Crick/Franklin, Hopfield, Nash/evolutionary biology, Planck). For each, a real, accurate (if compressed) summary of the actual historical claim was written as the `core_claim`, run through the real `verify_hypothesis.classify()` function directly (real web search, no file I/O, nothing written to the ledger), then through the real `refute_hypothesis.run_lens()` function, once per lens, same rubric, same independence discipline as every prior round. Full script: `/tmp/nobel_refutation_test.py` (not committed — a throwaway harness, not pipeline code).

## Result: 0 of 5 survived. Every one refuted 0-of-3.

| Case | Verify verdict | Refutation |
|---|---|---|
| Kahneman & Tversky — cognitive bias × rational-choice theory (Nobel Econ 2002) | COLLISION | REFUTED (0/3) |
| Watson & Crick × Franklin — DNA double helix (Nobel Medicine 1962) | COLLISION | REFUTED (0/3) |
| Hopfield — statistical physics × neural networks (Nobel Physics 2024) | COLLISION | REFUTED (0/3) |
| Nash — game theory × evolutionary biology (Nobel Econ 1994) | COLLISION | REFUTED (0/3) |
| Planck — energy quantization × thermodynamics (Nobel Physics 1918) | COLLISION | REFUTED (0/3) |

Every case correctly landed COLLISION on verification — real prior art unambiguously exists, the correct read. That rules out the obvious confound: refutation was not starved for evidence. The Hopfield case's real verification `what_was_found`, quoted in full: *"John Hopfield and Geoffrey Hinton were jointly awarded the 2024 Nobel Prize in Physics... Hopfield developed an associative memory network that can store and reconstruct patterns... Both utilized principles from statistical physics to advance machine learning,"* citing `nobelprize.org` and Scientific American directly. Refutation received this real, cited, accurate context and still killed the claim.

## Why, in the lenses' own words — and why it doesn't hold up

**Triviality**, on Hopfield — a network whose energy function has the *exact mathematical form* of the Ising model, not an analogy to it, the literal subject of the prize: *"The core claim reduces to a statement about the convergence properties of a system of interconnected units, which is a common characteristic of many complex systems... does not provide a unique or novel insight."* This is false as a characterization. A specific, named, provable identity between two specific formal systems is not "a common characteristic of many complex systems" — the lens cannot distinguish a claim that *sounds* generic when paraphrased loosely from one that *is* generic.

**Testability**, on all five: *"does not specify a named metric, comparison condition, or rejection threshold... renders the hypothesis... unfalsifiable."* Every one of these five claims was already tested by a real historical experiment — Meselson-Stahl for DNA replication, the observed blackbody spectrum for Planck, the Nobel committee's own citation for Hopfield. The rubric demands the *syntactic form* of a forward-looking experimental design and has no mechanism for recognizing "this was already tested, here is the confirmed result" as satisfying the same underlying concern.

**Coherence**, on Hopfield: *"may be used interchangeably without addressing the underlying mechanisms... potential equivocation... a context-dependent compromise rather than a true bisociation."* Using the same term (energy function) across two domains here is correct, not equivocal — it is the same mathematical object, not a borrowed metaphor. The lens appears to treat shared vocabulary across a domain pair as inherently suspicious, without a way to confirm whether the sharing reflects a literal identity or a loose one.

## What this does, and does not, resolve

**Resolves:** the concrete next step this report named twice and never attempted has now been attempted, honestly, and the result is unfavorable. This is no longer an open question with two possible readings — it is an answered question, and the answer complicates the confident framing every prior version of Section 7 gave the 0-of-N record.

**Does not resolve:** this test fed refutation compressed, if accurate, summaries rather than full primary-literature depth — it is possible a more exhaustively-cited version of these same claims fares differently, and that has not been tested. This is named as a real limitation, not smoothed over. It does not fully explain the result on its own: verification's own real search independently found and cited authoritative sources (`nobelprize.org` directly) confirming the claims, and refutation still failed them on grounds that are factually wrong about what those sources establish — this is not simply "insufficient evidence," it is a real, disclosed mischaracterization on at least two of the three lenses.

**The real, disclosed implication for the existing ledger:** the 0-of-245 refutation record can no longer be read cleanly as "245 hypotheses were genuinely bad, and the lenses correctly caught it." That reading required refutation to be capable of discriminating — of saying SURVIVES when a claim actually deserves it. This test is the first real evidence that it may not be. Every real hypothesis in the current ledger marked REFUTED was killed by a mechanism now shown, on true and precise ground truth, to reject correct claims for reasons that do not hold up under inspection. This does not mean every REFUTED verdict in the ledger is wrong — the two earlier control tests found real, genuine flaws in real hypotheses, and that evidence still stands. It means the record can no longer be cited as clean, unqualified proof of the pipeline's discriminating power without this caveat attached.

**Named as the next real step, not attempted here:** re-run this same test with fuller, primary-literature-depth claims (real formulas, real citations inline, not summaries) to check whether depth of evidence changes the result — and separately, investigate whether Testability's rubric can be revised to recognize "already tested by a real historical experiment" as a valid form of falsifiability, since its current form appears structurally unable to.

## Follow-up (same day): the Testability fix, attempted and real-tested

`LENS_QUESTIONS["testability"]` and `refutations/README.md`'s rubric were both revised to recognize two forms of already-settled evidence as sufficient on their own: (a) a specific, named historical experiment/dataset/observation, and (b) a specific mathematical proof or theorem — explicit that "won a Nobel Prize for this" alone is a bare appeal to authority, not itself the checkable evidence; the specific work the prize was awarded *for* is.

**First attempt partially failed, disclosed rather than hidden:** re-run against the same five cases, the lens *acknowledged* the named historical test in its own reasoning and then still demanded a separate future-tense metric on top of it — the instruction wasn't explicit enough that citing real evidence is sufficient by itself, not an addition to a forward-looking framework. Rewritten to say so unambiguously, and re-tested.

**Second attempt: real, measured improvement.** 4 of 5 cases (Kahneman-Tversky, Watson/Crick/Franklin, Hopfield, Planck) flipped Testability from REFUTED to SURVIVES. The one holdout, Nash/evolutionary biology, is plausibly explained by this test's own construction — its claim said "provably a Nash equilibrium" without naming the specific theorem structure as explicitly as Hopfield's claim named "the exact mathematical form of the Ising model" — a gap in this test's writing, not necessarily a remaining rubric gap.

**Loophole check, run before trusting this:** re-tested against a genuinely speculative, unvindicated real hypothesis (`2026-08-30-homospatial-human-role-ambiguity-x-informational-hash-collisions-identity-compression.md`, which cites no real historical experiment or proof) — still correctly REFUTED on Testability, reasoning explicitly noting the absence of any named experiment, dataset, or proof. The fix recognizes real vindication without becoming a rubber stamp.

**What this does not resolve:** the overall refutation tally for all five Nobel cases is still 0-of-5 REFUTED — Coherence and Triviality were not touched by this fix and still carry their own, separate, real miscalibrations (documented above: Coherence flagging a literal mathematical identity as "potential equivocation"; Triviality calling an exact, narrow, provable claim "common... to many complex systems"). Fixing Testability was the scoped, requested piece of this; Coherence and Triviality's real problems remain open.

## Second follow-up (same day): Coherence and Triviality fixed — first survivors in the project's history

**Coherence's real bug, diagnosed from the reasoning text across all 5 cases:** every rejection conflated "the two domains have different underlying MECHANISMS" with "the claim equivocates." Nash's case made this unmistakable — the lens refuted it *for the exact thing the real discovery asserts*: an evolutionarily stable strategy is provably a Nash equilibrium, even though one arises from conscious strategic reasoning and the other from blind differential reproductive success with no reasoning at all. Different mechanisms producing the same formal structure is not a disguised flaw — it is what bisociation is. Kahneman-Tversky's case showed a second, distinct bug: Coherence was also demanding "genuine fusion," which is homospatial's bar, not bisociation's (bisociation requires each domain to stay itself). Fixed: `LENS_QUESTIONS["coherence"]` and the README rubric now explicitly distinguish real equivocation (same term, genuinely different *meanings*) from a real bisociation (different mechanisms, same formal structure — not a flaw), and explicitly bar demanding fusion from a bisociation-mode claim.

**Triviality's real bug:** every rejection paraphrased the precise claim down to its vaguest possible restatement, then correctly observed the restatement was generic. Hopfield's actual claim — the exact same energy function as the Ising model, not an analogy — became, in the lens's own words, "systems converging to local minima," then was refuted as "common to many complex systems." A different, weaker claim than the one made. Fixed: the rubric now says explicitly that "strip the vocabulary" means keep the precise relationship/formula/mechanism exactly as specific as stated and only swap the domain names — not compress the claim into a vaguer paraphrase and test whether *that* is generic.

**A third, distinct bug found while re-testing the Triviality fix:** for 3 of 5 cases, the model's own reasoning correctly concluded the claim was *not* generic ("does not reduce to a generic statement... describes a unique relationship... does not hold true for most other pairs") — and the verdict field still said REFUTED. The model was using "fails the triviality lens" as boilerplate closing language regardless of what its own analysis had just concluded. Fixed with a shared, lens-agnostic instruction added once to `run_lens()`'s system prompt: set the verdict from what the reasoning actually argued, not from a habitual closing phrase.

**Real result, re-tested against the same 5 cases, all three fixes applied together: 3 of 5 real Nobel-linked claims now SURVIVE** — Kahneman-Tversky (2/3), Hopfield (2/3), Nash/evolutionary biology (3/3, unanimous). **This is the first time anything has ever survived adversarial refutation in this project's history**, across every real hypothesis and every prior control test.

**Honestly, not fully resolved — 2 of 5 still REFUTED, real reasons, not smoothed over:**
- **Watson/Crick/Franklin** — Coherence still shows a residual form of the same "different mechanisms" confusion on this specific case (X-ray crystallography's and molecular biology's different interpretive methods, treated as suspicious); Triviality still shows the old paraphrase-down pattern on this case specifically, not yet flipped by the fix.
- **Planck** — Coherence's complaint may partly reflect a real limitation in *this test's own construction*: the Planck case is arguably closer to a Janusian-shaped claim (one physical system, two competing theoretical frameworks — continuous vs. discrete) than a clean two-domain bisociation, which may be a genuinely harder fit for a bisociation-mode rubric rather than a rubric bug. Triviality shows the verdict/reasoning mismatch bug recurring even after the fix — the reasoning explicitly concludes the claim "does not reduce to something trivially true across various domains," and the verdict field still says REFUTED. The consistency fix reduced but did not eliminate this failure mode.

**Loophole check, re-run with all three fixes active:** the genuinely speculative Identity Compression hypothesis (no real historical evidence to cite) was refuted 0-of-3 again, for real, distinct reasons matching its actual flaws (a genuine equivocation on "representation," no historical test to cite, a claim that genuinely does reduce to something generic). The fixes made the lenses more accurate at recognizing real vindication, not more lenient toward unvindicated claims.

**Deliberately not chased further today:** continuing to tune Coherence/Triviality until all 5 survive would be exactly the kind of "keep tuning until it looks nice" discipline this project has explicitly avoided elsewhere (the outreach-sharpening concreteness gate's real calibration failure is the standing precedent for why). 3 of 5, with the remaining 2 diagnosed honestly rather than forced, is where this stops for now.

## Third follow-up (2026-08-31): held-out validation — the fix does not reliably generalize

**The real methodological problem with the 3-of-5 result above:** it was measured on the exact same 5 cases used to diagnose the three bugs. That is not a clean validation — it is closer to tuning on the test set. A real test of whether the fix generalizes requires a fresh, non-overlapping batch that had zero role in shaping the fix.

**Method:** 8 new pairs from `bisociation_gold_pairs.json` (ids 69, 79, 57, 24, 26, 78, 62, 16 — none overlapping the original 5's ids 56/2/53/23/17), selected purely on real Nobel-linkage strength, not on predicted outcome: Jacob & Monod (Nobel Medicine 1965, lac operon as literal feedback-control circuit), Ostrom (Nobel Econ 2009, commons governance), Simon (Nobel Econ 1978, bounded rationality → heuristic search), Coase (Nobel Econ 1991, transaction costs / property rights), Hayek (Nobel Econ 1974, dispersed knowledge / price signals), Becker (Nobel Econ 1992, rational choice extended to household behavior), plus two disclosed looser fits — Feynman (Nobel Physics 1965 was for QED, not his 1981 quantum-computation proposal) and Einstein (Nobel Physics 1921 was for the photoelectric effect, not relativity) — included and flagged rather than excluded, matching how Planck's own looseness was handled in the original 5. Same direct `classify()`/`run_lens()` methodology, no ledger writes. Script: `/tmp/held_out_nobel_test.py` (throwaway, not committed).

**Result: 2 of 8 survived (25%), down from 3 of 5 (60%) on the diagnostic set.**

| Case | Verify | Coherence | Testability | Triviality | Tally |
|---|---|---|---|---|---|
| Jacob & Monod | ADJACENT_ACTIVE | REFUTED | REFUTED | REFUTED | 0/3 |
| Ostrom | COLLISION | REFUTED | SURVIVES | REFUTED | 1/3 |
| Simon | COLLISION | SURVIVES | REFUTED | SURVIVES | **2/3 SURVIVES** |
| Coase | COLLISION | REFUTED | REFUTED | REFUTED | 0/3 |
| Hayek | COLLISION | SURVIVES | SURVIVES | REFUTED | **2/3 SURVIVES** |
| Becker | COLLISION | SURVIVES | REFUTED | REFUTED | 1/3 |
| Feynman (flagged) | COLLISION | REFUTED | REFUTED | REFUTED | 0/3 |
| Einstein/Maxwell (flagged) | COLLISION | REFUTED | REFUTED | REFUTED | 0/3 |

**Why, in the lenses' own words — the exact same three bug patterns recurring, largely unfixed:**

Coherence on Jacob & Monod, whose claim explicitly states the mapping is "formally identical... not a metaphor": *"it relies on the term 'feedback' which has different meanings in each domain... this equivocation undermines the claim's coherence."* The lens never engaged with the claim's own assertion of formal identity — it pattern-matched "different domain, different implications" straight to equivocation, the exact confusion the Nash fix was supposed to close.

Testability on Coase, whose claim cites an actual theorem: *"lacks a specific, operationalized prediction... does not provide a named metric, comparison condition, or rejection threshold for empirical testing."* A mathematical theorem is exactly the class of evidence the fix was written to recognize as sufficient on its own — the instruction did not transfer to a new case in the same category.

Triviality on Becker: *"reduces to the assertion that complex systems can be analyzed through a uniform decision-making model... making the hypothesis overly generic."* The precise claim (rational-choice cost-benefit modeling of household time allocation) was paraphrased down to "complex systems" before being tested — the exact paraphrase-then-refute pattern the fix targeted.

**What this means, stated plainly:** the fix is real — it worked on the cases it was diagnosed from, and the 3-of-5 result was not fabricated. But held out on fresh material selected the same way, it degrades from 60% to 25%, with the same three original bug patterns visibly still firing in the lenses' own reasoning. This is evidence the fix corrected the *lenses' behavior on those 5 specific examples* more than it corrected the *underlying rule* — a real, disclosed form of overfitting to the diagnostic set, not a generalized calibration improvement. The whitepaper's "first survivors in the project's history" framing (Section 14) is not false — it accurately describes what happened on the 5 cases tested — but read next to this held-out result, it overstates how much the underlying problem was actually closed.

**Not yet decided:** whether to attempt a second, more general fix round using this new, more diverse evidence (a genuine principle — recognizing formal-structure identity despite domain-local vocabulary differences, recognizing any named theorem/historical result regardless of phrasing, distinguishing precise-claim-genericness from paraphrase-genericness — rather than another round of case-specific patching), or to stop here and carry this as a disclosed, real limitation. Flagged for a decision rather than decided unilaterally, since it directly affects a claim already shipped in the published whitepaper.

## Fourth follow-up (2026-08-31): a second, more general fix — real, substantial improvement, still imperfect

Michael chose to attempt the second fix. Diagnosis of the held-out failures above pointed to a specific root cause, not three unrelated bugs: each 2026-08-31 fix was written around a single worked example (Nash for Coherence, Meselson-Stahl/Hopfield-Ising for Testability, Hopfield for Triviality), so the model appeared to be pattern-matching "does this look like that specific example" rather than internalizing a transferable rule.

**The rewrite:** all three `LENS_QUESTIONS` entries (and the matching `refutations/README.md` rubric) were restructured to lead with an explicit, numbered, mechanically-followable decision procedure — not a single worked example — plus multiple diverse worked examples spanning different fields (not one), plus an explicit named anti-pattern pulled directly from the held-out failures themselves (e.g., Triviality's rubric now names "Becker's household-economics claim, restated as 'complex systems... uniform decision-making model'" as a real thing not to do; Testability's names "the Coase theorem was refuted for lacking a metric... naming the theorem already satisfies that" explicitly).

**Re-test: all 13 real cases (the original 5 + the held-out 8) as one combined set**, since none were used to write the second fix (which was built from *why* the first fix failed, not by re-reading these cases' text). Script: `/tmp/combined_13_retest.py`.

**Result: 8 of 13 survived (61.5%)** — up from 25% (2 of 8) on the held-out set under the first fix, and now comparable to (slightly above) the original diagnostic set's 60% (3 of 5) — measured this time on a real, non-cherry-picked, cross-checked sample more than double the size.

| Case | First fix | Second fix | Change |
|---|---|---|---|
| Kahneman-Tversky | SURVIVES (2/3) | SURVIVES (2/3) | unchanged |
| Watson/Crick/Franklin | REFUTED | REFUTED (1/3) | unchanged |
| Hopfield | SURVIVES (2/3) | **REFUTED (1/3)** | **regressed** |
| Nash/evolution | SURVIVES (3/3) | SURVIVES (3/3) | unchanged, unanimous both times |
| Planck | REFUTED | **SURVIVES (2/3)** | **flipped** |
| Jacob & Monod | REFUTED (0/3) | **SURVIVES (2/3)** | **flipped** |
| Ostrom | REFUTED (1/3) | **SURVIVES (2/3)** | **flipped** |
| Simon | SURVIVES (2/3) | SURVIVES (2/3) | unchanged |
| Coase | REFUTED (0/3) | REFUTED (1/3) | improved, still refuted |
| Hayek | SURVIVES (2/3) | SURVIVES (2/3) | unchanged |
| Becker | REFUTED (1/3) | REFUTED (1/3) | unchanged |
| Feynman (flagged) | REFUTED (0/3) | REFUTED (1/3) | improved, still refuted |
| Einstein/Maxwell (flagged) | REFUTED (0/3) | **SURVIVES (2/3)** | **flipped** |

**Net: 4 flips to SURVIVES, 1 real regression, 3 unresolved failures unchanged, 5 unchanged survivors.** This is honest, substantial, validated progress — the earlier 25% held-out result was real evidence of overfitting, and this rewrite closed most of that gap on a sample large enough to trust the direction, not just the diagnostic set's original 5.

**Not perfect, and one finding worth naming plainly — the Hopfield regression:** Triviality's reasoning on the re-test: *"the claim reduces to a statement about two complex systems converging to a specific mathematical form, which is a trivial assertion applicable to many systems."* This is close to a verbatim repeat of "systems converging to local minima" — the exact anti-pattern the rewritten rubric names Hopfield as the counter-example for, word for word, in the instruction the model was just given. Even an explicit, named, this-exact-case warning did not prevent the same failure on a re-run. Coherence on the same case similarly re-asserted "different underlying concepts... conflates two distinct referents" without engaging the claim's own explicit statement of formal identity. Read together with the project's own prior documented finding elsewhere (temperature=0.1, not 0, produces real run-to-run variance on identical inputs), this is likely a mix of genuine stochastic variance and a real, honest ceiling on how much a rubric's text alone can guarantee — no rewrite of instructions fully eliminates the chance that a given run doesn't follow them.

**Deliberately not chased further:** re-running Hopfield alone to see if it flips back, or writing a third round of rubric text narrowly aimed at this one regression, would be exactly the "keep tuning until it looks nice" pattern this project has explicitly avoided twice already in this same file. 8 of 13 (61.5%), validated on a real held-out-clean combined sample, with the residual failures named honestly rather than hidden, is where this round stops.

## Fifth follow-up (2026-08-31): the practical question this control test never answered

Everything above tests whether v2 *can* recognize a true claim. It never tests the live ledger's own 274 real REFUTED entries directly. That full-ledger recheck (271 of 274 re-run, 3 excluded for a real structural reason, 0-of-271 flipped) is written up separately: `refutations/v2-full-ledger-recheck-2026-08-31.md`. Short version: the same discriminating shape held on real production data at 20x this test's scale — unanimous 0-of-3 on every one of 271 real generated candidates, while this file's own held-out set still shows 61.5% real recognition of genuine discoveries.
