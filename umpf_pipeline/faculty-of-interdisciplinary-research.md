# The Faculty of Interdisciplinary Research

**Built**: 2026-08-28 · **Source**: `verification-log.jsonl` — every verdict below traces to a specific, cited verification file in `verifications/`, no rounding or silent drops.

**Update 2026-08-29 (batch 4) — the batch 3 PENDING_VERIFICATION queue is fully cleared, 0 pending.** A
dedicated follow-up session, spending its own web-search budget on nothing else, resolved all 10
hypotheses batch 3 left pending. Results: **5 COLLISION** — distributed consensus (CRDTs are the real,
named technology built on exactly this claim), human cognitive bias (Gigerenzer's "Homo Heuristicus" /
ecological rationality program states the paradox as a standing academic controversy), quantum
measurement (Many-Worlds + decoherence states it as established physics), information load balancing (a
published hybrid-federated-learning result showing the exact quantified outperformance claimed), and
chemical-reaction-networks × committee-formation (kinetic opinion-dynamics research already models
collective decision-making with reaction-kinetics-style equations). **4 ADJACENT_ACTIVE** — creative
block (real incubation-effect research is adjacent but describes avoidance, not the direct engagement
the hypothesis claims), mechanical springs × emotion (affective computing is real and active but no
source uses a literal Hooke's-Law mapping), narrative-arc × distributed-consensus (collaborative-
storytelling research is real and active but doesn't use formal consensus-theory concepts), and
cache-miss-handling × indecision (ACT-R models memory retrieval but not specifically the cache-miss
framing). **1 NO_SIGNAL** — astronomy × album production, nothing found either way. That case went
through the same three-independent-agent adversarial refutation protocol as every prior case and came
back **REFUTED, 0-of-3 survival** — extending the ledger's refutation record to **0-of-7 overall**, still
unbroken. Full ledger now: **40 of 40 hypotheses carry a canonical verdict, zero pending** — 22
COLLISION, 10 ADJACENT_ACTIVE, 7 REFUTED, 1 held out (non-standard). See `leaderboard.md` for the full
current ranking and `verifications/2026-08-29-*.md` /
`refutations/homospatial-astronomy-albumproduction-refutation.md` for the individual records.

**Update 2026-08-28 (batch 3) — 40 entries total, not 25.** A third domain pool was mined from real,
existing source material: `the-rosetta-stone/finetuning-LLM/equivalency-training-pairs.json` (a real
44-example LLM fine-tuning corpus) yielded 88 individual sub-domains — combined pool now **170 domains,
~14,365 possible pairs**. A 15-hypothesis batch (5 per mode, weighted toward the new pool) was generated;
all 5 homospatial outputs passed the comparison-word check (4 needed one corrective retry, confirming the
enforcement mechanism holds at scale). **Verification hit a hard, honest constraint: the session's
WebSearch budget was exhausted (200/200) after 5 of 15 queries.** Rather than fake the remaining 10 or
silently drop them, they're recorded with an explicit `PENDING_VERIFICATION` status — generated,
Phase-1-complete, genuinely awaiting Phase 2, not a verdict and not hidden. Of the 5 actually verified: 2
COLLISION (musical-motif×punctuated-equilibrium, a direct published hit specific to pop music;
financial-trading×predator-prey, the cleanest collision of the batch — a whole named "market ecology"
research tradition with predator-prey models in their titles), 3 ADJACENT_ACTIVE (including one flagged
nuance: the trust/ZKP pairing found real material, but mostly under "Zero Trust" architecture, a
different sense of "trust" than the hypothesis's own psychological framing — stated plainly, not
smoothed into a clean win). See `leaderboard.md`'s own "Pending verification" section for the full list.

**Update 2026-08-28 (batch 2) — 25 entries total, not 19.** A third generation mechanism (homospatial
thinking — Rothenberg 1976, fusion rather than collision or paradox) and a domain-pool expansion (23
systems from `the-rosetta-stone.json` unioned with `domains.json`'s original 59) were added — see
`hypothesis_engine.py`'s docstring and `rosetta_stone_domains.json`. A 6-hypothesis test batch (2 per
mode, 2 deliberately cross-pool) was generated and verified: 4 COLLISION (including a striking one —
the Finance/Janusian hypothesis independently reproduced Andrew Lo's named Adaptive Market Hypothesis
almost word-for-word), 2 NO_SIGNAL. Both NO_SIGNAL cases went through adversarial refutation (3
independent agents each, same protocol as batch 1) and came back **REFUTED, 0-of-3 survival each** — no
promotions to Frontier Research Group this round. **A real points/badges/leaderboard scorer now exists**
(`score_hypotheses.py` → `leaderboard.md`, regenerated after every batch) — see that file for the full
ranking rather than restating it here. Full updated tally across all 24 scored entries (1 non-standard entry still held out, 25 total): **15
COLLISION, 3 ADJACENT_ACTIVE, 6 REFUTED (every NO_SIGNAL case that has ever occurred in this ledger has
now been adversarially refuted — 4 from batch 1, 2 from batch 2 — zero unresolved NO_SIGNAL entries
remain), 0 FACT_CHECK_FAIL.** Verified directly against `verification-log.jsonl`, not estimated. Phase 3 (researcher outreach) infrastructure was built
(`outreach/README.md`) but produced **zero drafts this round** — no hypothesis in batch 2 reached
ADJACENT_ACTIVE or survived refutation, so per the standing rule (drafts only for real candidates, never
manufactured), there was nothing to draft for. Stated plainly, not hidden.

---

## Why this document exists

*"The mere fact that we're getting successful bisociations means we have the beginnings of a university."*

The Eureka Engine's Phase 2 verifier classifies every generated (or pre-existing) hypothesis into one of four outcomes: COLLISION, ADJACENT_ACTIVE, FACT_CHECK_FAIL, NO_SIGNAL. Those four outcomes, unchanged, double as four faculty roles — this document is that reading, applied to every pairing verified so far:

| Verdict | Faculty role | What it means here |
|---|---|---|
| COLLISION | **Established Department** | Real prior art exists — proof the pairing is legitimate, institutionally-recognized territory, not proof of a fresh discovery |
| ADJACENT_ACTIVE | **Frontier Research Group** | Real, specific, fertile ground — genuinely unclaimed. Where new discovery work should actually point |
| FACT_CHECK_FAIL | **Retracted** | The domain description itself was wrong — needs a fix before the pairing means anything |
| NO_SIGNAL → survives adversarial refutation | **Frontier Research Group** (promoted) | Search found nothing, but the claim's own logical structure held up under 3 independent attempts to kill it |
| NO_SIGNAL → fails adversarial refutation | **REFUTED** | The domain facts are fine, but the specific cross-domain claim doesn't survive scrutiny — failed peer review on its central argument, not its data |

**Reconciliation:** 19 verified entries total. 18 classified under the four-way rubric; 1 (physics/empiricism) is a non-standard single-domain paper the rubric doesn't map onto cleanly, held out and reported on its own terms below. **Update 2026-08-28:** all 4 original NO_SIGNAL cases have since been run through adversarial refutation (3 lenses each — coherence, testability, triviality; promotion requires 2-of-3 survival) — see `refutations/`. All 4 came back 0-of-3 survival. **Second update, same day:** each of the 4 refutations was then independently re-run by 3 separate agents (one per lens, each blind to the original reasoning and to each other) — 12 agents total, **12-of-12 confirmed REFUTED**, full agreement with the original single-reasoner pass, and every single lens surfaced at least one finding the original pass missed (the immune/DLT paper's own admission its analysis is "textual, conceptual, and illustrative"; the variance/protein paper's own table self-rating its central equivalence "Weak" on 3 of 4 axes; independent re-discovery, not re-assertion, of the missing Section 6 in the coral-reef paper). The "Needs Second Opinion" section below is now empty by resolution, not by omission; see the REFUTED section.

---

## Established Departments (COLLISION — 11)

Real, cited prior art exists for each. Split into two shelves: genuine collisions (a real structural correspondence someone else already formalized) and a second, smaller shelf of pairings that turned out not to be genuine bisociations at all — caught during verification, not before.

### Genuine collisions (8)

| Pairing | Mode | What already exists |
|---|---|---|
| Ecology (mycorrhizal networks) × Telecommunications (packet routing) | bisociation | Named algorithms HyphaNet, FUNNet; a formal information-theoretic "Internet of Plants" model (arXiv 2509.08434) |
| Jazz improvisation × Counterpoint/voice leading | bisociation | Berklee's "Jazz Counterpoint 1" course; a UNT dissertation doing near-exactly the study the hypothesis proposed |
| Law (stare decisis) × its own inversion | janusian | Legal scholarship already frames precedent's dual stabilizing/injustice-perpetuating role as simultaneous |
| Linguistics (sound change) × its own inversion | janusian | The century-old, named Neogrammarian-hypothesis-vs-lexical-diffusion debate |
| Materials science (crystal defects) × its own inversion | janusian | Callister's materials-engineering textbook chapter, "Dislocations & Strengthening Mechanisms" |
| Genetic algorithms × Simulated annealing | case study | A named unified mathematical framework already exists (arXiv 2410.10369) |
| Graph algorithms × Minimax game tree search | case study | AND/OR graph model already unifies both (arXiv 2103.16692) |
| Raft × PBFT consensus | case study | Textbook-standard distributed-systems curriculum comparison |

### Not genuine bisociations — same field or whole-part, not incompatible frames (3)

Caught by verification, worth naming as its own category rather than folding silently into the collision count:

| Pairing | Why it doesn't qualify |
|---|---|
| Graph traversal × State space search | Standard AI curriculum treats BFS/DFS/A* as literally *the technique* for state-space search, not an independently-arising parallel |
| Trigonometric analysis × Fourier transform | Fourier analysis is constitutively built on trigonometric functions — whole-part, not two incompatible frames |
| Quantum entanglement/Bell inequalities × Quantum information science | This session's own bisociation prompt already names this exact pairing as the canonical non-example ("same field wearing two names") |

---

## Frontier Research Groups (ADJACENT_ACTIVE — 3)

Real, specific, fertile ground — the state a genuinely useful hypothesis should be in.

| Pairing | Mode | The specific open territory |
|---|---|---|
| Distributed Consensus Algorithms × Cache Coherence Protocols | case study | "Distributed systems consistency protocols" is real, narrow, active territory; no source draws this exact cross-connection yet |
| Compiler optimization × Neural network training | case study | Real active field (ML-for-compilers) exists, but as a tool relationship — the structural-isomorphism claim itself is still open |
| Dirac's Large Numbers Hypothesis × Belnap four-valued logic | case study | The logical substrate (four-valued reasoning for contradictory evidence) is established; the explainable-AI-output extension is not |

---

## Needs Second Opinion (NO_SIGNAL, unresolved — 0)

Empty. All 4 original entries have been run through adversarial refutation — see below.

---

## REFUTED (adversarial refutation, 0-of-3 survival — 4)

Distinct from Retracted: in every case here, the underlying domain facts were fine — what failed was the specific cross-domain claim built on them, under three independent attempts to kill it (coherence / testability / triviality lenses, full reasoning in `refutations/`).

| Pairing | Mode | What actually broke it |
|---|---|---|
| Neuroscience (cortical reorganization) × Climatology (thermohaline circulation) | bisociation | Equivocates "changes over time" with "adapts" — cortical reorganization is teleonomic, thermohaline shift is purely thermodynamic. No operational metric proposed. Confirms the original umbrella-trap finding independently. |
| Human immune system × Distributed ledger technology | case study | The Control-layer mapping (cytokine signaling ↔ consensus protocols) conflates continuous chemical diffusion with discrete algorithmic voting. "Local rules → emergent behavior" is close to definitionally true of any decentralized system. |
| Neural networks × Coral reef ecosystems | case study | **Confirmed, not inferred:** the paper's own abstract promises a "Section 6: hypothesis and experiment" — the file has no Section 6, and cuts off mid-Section-4 at line 134. No falsifiable claim was ever written. |
| Sample variance/statistical estimation × Protein structure prediction | case study | The VAE-information-density conclusion is asserted by shared vocabulary ("uncertainty," "dimensionality"), not derived from the sample-variance formula — the relevant framework would be rate-distortion theory, not finite-population variance correction. |

**Every refutation file also names a steelman** — the narrower, better-scoped version of the claim (if one exists) that might actually survive, rather than closing the door outright. Three of the four have one; the coral-reef case does not (nothing to rescue when the falsifiable content was never written).

---

## Retracted (FACT_CHECK_FAIL — 0)

None yet. Worth stating plainly rather than omitting the section — zero isn't the same as "not checked."

---

## Held out — not a standard case (1)

**Physics × The Empiricism Problem (Philosophy of Science)** — a single-domain argument paper (the CMB "Axis of Evil" anomaly as a case study in inconsistent empirical standards), not a two-domain pairing the four-way rubric maps onto. Its own factual premise was checked instead: the paper frames the anomaly as "unexplained... an epistemological crisis," but real published work (masking-technique systematic-error studies, a 2016 WMAP/Planck anisotropy study finding no evidence for the effect) contests that framing. Flagged for Michael in `verifications/case-study-physics-empiricismproblem-verification.md` — not resolved here.

---

## Two housekeeping items surfaced during verification, not fixed here

`domains.json`'s tracking labels for two case studies don't match what the files actually contain — flagged in their own verification files, not silently corrected:
- `DCA-cachecoherentprotocols.md` is tracked as "Dynamic Cache-coherent Architectures × Cache-coherent protocols" but is actually "Distributed Consensus Algorithms × Cache Coherence Protocols."
- `the-rosetta-stone-dirac-largenumbers.md` is tracked as "Dirac's LNH × Cosmological constants" but is actually "Dirac's LNH × Belnap four-valued logic."

## What this is table stakes for, not the whole thing

This map proves the engine (both generation modes, and the pre-existing hand-authored corpus) reliably lands on real, checkable territory — 11 of 18 classified pairings collided with genuine prior art, 3 more sit in real open territory, and the ambiguous cases were resolved by genuine adversarial scrutiny rather than left as an asterisk or stretched into false positives. That's a real result, with a real committee process behind it now, not just a search pass. It is still not, by itself, a university:

- **Resolved (2026-08-28):** the adversarial refutation instrument's first round used one reasoner (me) playing all three lenses — a real limit, since a genuine committee has independent reviewers, not one mind switching hats. Re-run with 12 genuinely independent agents (3 per case, each blind to the original reasoning and to each other): 12-of-12 confirmed REFUTED. The remaining honest caveat: this is still one round of independent review, not an ongoing standing committee — a REFUTED verdict here means "didn't survive rigorous scrutiny twice, independently," not "can never be revisited."
- **No cross-department synthesis** — nothing here connects an Established Department's method to a Frontier Research Group's open question.
- **No admissions process** — `domain_pool` (59 entries) is hand-seeded, not discovered or expanded systematically.
- **This corpus is a curated slice, not the whole graph** — `case-studies/the-rosetta-stone-case-study-neuralnets-coralreef.md` itself notes "the-rosetta-stone.json has 100+ other domain equivalencies" not written up as full case studies and not covered by this pass.
- **Refuted doesn't mean forgotten** — every refutation file names the steelman where one exists (3 of 4 do); those narrower reformulations are real candidate future hypotheses, not dead ends.

Named as real next steps, not implied as already covered.
