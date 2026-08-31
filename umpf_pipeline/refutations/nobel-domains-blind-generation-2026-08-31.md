# Blind Generation Test — 7 Real Nobel-Linked Domain Pairs Run Through the Actual Engine

**Date:** 2026-08-31
**Purpose:** distinct from the 13 hand-authored ground-truth entries already on the leaderboard (`control-test-nobel-calibration.md`, `v2-full-ledger-recheck-2026-08-31.md`) — those tested whether refutation could *recognize* an already-known-correct answer. This tests something different: pointed at the same real domain pairs, blind to the real historical insight, can `hypothesis_engine.py`'s own generation independently land anywhere near it? These 7 are genuine, unmodified engine output — no special badge, no hand-authored content, scored on identical terms to any other hypothesis.

## The 7 pairs

7 real, not-yet-covered Nobel-linked pairs from `bisociation_gold_pairs.json`, run through the real pipeline end to end: `hypothesis_engine.py --domain-a/--domain-b` (exact domain strings from the gold file, no hint of the real answer) → `prefilter_observe.py` → `verify_hypothesis.py` → `refute_hypothesis.py` where triggered. Fibonacci-staged batches (1, 1, 2, 3), per direct instruction.

| Gold # | Domains | Real historical insight |
|---|---|---|
| 44 | Marconi — radio × Telegraphy | Wireless telegraphy (1909 Nobel Physics) |
| 45 | Fleming — bacteriology × Contamination | Penicillin (1945 Nobel Medicine) |
| 64 | Prigogine — thermodynamics × Complex systems | Dissipative structures (1977 Nobel Chemistry) |
| 8 | Black–Scholes — financial pricing × Physics — diffusion equations | Options pricing (1997 Nobel Economics) |
| 29 | Black–Scholes — finance × Wiener processes | Stochastic option pricing (1997 Nobel Economics, same prize as #8) |
| 30 | Nash — equilibrium × Malthus — scarcity | Equilibrium under selection pressure (1994 Nobel Economics, same prize as the ground-truth Nash entry, different pairing) |
| 68 | Watson & Crick — DNA × Information theory | Genetic information paradigm (1962 Nobel Medicine, same prize as the ground-truth Watson-Crick entry, different pairing) |

**A real, disclosed limitation of this test, stated up front:** the generating LLM's training data plausibly already contains real facts about Marconi, Fleming, Prigogine, and the rest. A generated hypothesis landing close to the real insight isn't clean proof of independent bisociative reasoning — it could partly reflect memorized fact recall rather than the engine's own structural mapping. Not something this test can fully control for; disclosed rather than glossed over.

## Real timing, batch by batch

| Batch | Size | Total | Avg/pair |
|---|---|---|---|
| 1 | 1 | 73.9s | 73.9s |
| 2 | 1 | 69.9s | 69.9s |
| 3 | 2 | 39.2s | 19.6s |
| 4 | 3 | 70.5s | 23.5s |

**7 pairs, 253.5s total, 0 errors.** The apparent speedup from batch 1-2 to batch 3-4 is real but **not** a general engine speedup — it's fully explained by `pair_type`, confirmed directly against `prefilter-log.jsonl`: Prigogine and both Black–Scholes pairings classified `formalism-shaped` and hit `prefilter_observe.py`'s existing skip-by-design path (`status: skipped_formalism_shaped_by_design`) — 1.7-1.8s instead of the full two-agent dialectic. Marconi, Fleming, Nash/Malthus, and Watson-Crick/Info-theory classified narrative-shaped or mixed-uncertain and ran the real dialectic (6.7-52.2s). This is the pre-filter working exactly as designed, not a declarative-schema-driven speedup — that claim would have overstated what the data shows.

**What the declarative-schema migration's real effect looks like here:** every `generate` call (10.0-13.3s), every `verify` call (3.4-5.4s), and every `refute` call (4.7-6.0s) across all 7 completed with zero retries and zero malformed-JSON handling — consistent with the strict-schema migration's expected benefit (that failure class is now structurally impossible), though this run has no identical pre-migration baseline to diff against directly, so it's confirmatory, not a measured before/after delta.

## Real results — where blind generation landed vs. the real answer

| Domains | Verdict | Refutation | Honesty flag | Tier |
|---|---|---|---|---|
| Prigogine × Complex systems | ADJACENT_ACTIVE | not triggered | no | 🗺️ Verified, Unrefuted (+30) |
| Watson & Crick × Information theory | ADJACENT_ACTIVE | not triggered | no | 🗺️ Verified, Unrefuted (+30) |
| Black–Scholes × Wiener processes | COLLISION | not triggered | **yes** | 💀 Refuted/Rejected (-5) |
| Marconi × Telegraphy | ADJACENT_ACTIVE | REFUTED | yes | 💀 Refuted/Rejected (+5) |
| Fleming × Contamination | ADJACENT_ACTIVE | REFUTED | yes | 💀 Refuted/Rejected (+5) |
| Black–Scholes × Physics-diffusion | ADJACENT_ACTIVE | REFUTED | yes | 💀 Refuted/Rejected (+5) |
| Nash × Malthus | ADJACENT_ACTIVE | REFUTED | yes | 💀 Refuted/Rejected (+5) |

**2 of 7 landed clean — real signal, unflagged, unrefuted.** Reading the actual generated content against the real insight:

- **Prigogine** — generated: *"the relational rule governing energy exchanges in thermodynamic systems also governed... how local interactions can lead to global emergent behavior... model emergent behaviors using entropy and energy distribution patterns."* Real insight: *"Order need not fight entropy; energy flowing through a system can create structure."* Recognizably the same territory — not the sharp original formulation, but a real, substantive match. The closest of the 7.
- **Watson & Crick × Information theory** — generated: *"the encoding of genetic information in DNA also governed the encoding of information in communication systems... a structured sequence that conveys meaning."* Real insight: *"A molecule that specifies how another molecule is built is behaving like an information-bearing code."* Also genuinely close.
- **Black–Scholes × Wiener** — generated: *"stochastic dynamics of asset prices... governed the paths of Wiener processes... continuous stochastic evolution under uncertainty."* Real insight: *"the mathematics of Brownian motion can price financial claims."* Nearly a restatement of the real foundation — correctly landed COLLISION (real, established prior art), the honest verdict for rediscovering something this well-documented.
- **Black–Scholes × Physics-diffusion** — generated: *"price evolution... governed particle concentration evolution in diffusion equations... probabilistic spread over time."* Real insight: *"An option price evolves like a diffusing quantity."* Also a real, substantive match — and still got REFUTED, a genuine complication worth naming rather than smoothing over: a generation that lands close to the real historical insight is not automatically safe from refutation catching something else (here, the mechanical honesty check flagged it before refutation ran).
- **Nash × Malthus** — generated: *"strategic decision-making in Nash equilibria... governed resource allocation in Malthusian scarcity... optimizing individual choices under constraints."* Real insight: *"equilibrium can emerge from strategy operating under scarcity."* Same general shape, more abstracted/generic than the real, sharper sentence.
- **Marconi** and **Fleming** are the two real misses: Marconi's generated claim ("signal management techniques" transferring between radio and telegraphy) never reaches the actual insight (wireless removing the need for a wire at all); Fleming's ("uncertainty in identifying strains/sources") never reaches the actual insight (the contaminant's antibacterial *effect*). Both correctly refuted.

## What this does and doesn't show

**Real, honest signal:** blind, unprompted generation on domain pairs known to house a real discovery landed in the right conceptual neighborhood 4 of 7 times (Prigogine, Watson-Crick, both Black-Scholes framings), with 2 of those clean enough to survive to `ADJACENT_ACTIVE` unflagged and one correctly self-identifying as existing science (COLLISION). That's a real, current data point on generation quality — not proof the engine "gets" bisociation the way a human scientist does, but evidence it's not merely producing noise on pairs where a real answer exists.

**What it doesn't show:** whether this generalizes to domain pairs with *no* known real answer waiting (the actual, harder, more relevant question for future discovery) — these 7 were deliberately chosen because the answer exists, which is the opposite of the pipeline's normal autonomous mode. And per the disclosed limitation above, closeness to a famous historical fact may partly reflect the model already knowing that fact, not independent structural reasoning.

**Where this sits relative to the 13 ground-truth entries:** those top the entire leaderboard (ranks #1-8) because real, vindicated science that survives refutation has nowhere else to rank — none of the engine's own generated candidates has ever survived. These 7 sit exactly where their own real verdicts and refutation outcomes put them, mixed in with every other real hypothesis, which is the honest baseline the ground-truth entries are there to be compared against: this is what "0 score" currently looks like for the engine's own attempt at Nobel-caliber territory, and the two clean landings (Prigogine, Watson-Crick) are the most concrete evidence so far of what "climbing toward highest score" could look like.
