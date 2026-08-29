# The Eureka Engine — $10K Spend Readiness Audit

**Question posed:** if Exponent Labs were going to spend $10,000 running the Eureka Engine, what has to be addressed first so that money isn't wasted?

**Method:** the real cost, bug, and limitation data already on record in `whitepaper.html` and this repo's own logs, cross-checked live against `token_usage.jsonl` and `verification-log.jsonl` as of this writing (89 ledger entries); a real calibration test run through the live pipeline for this report specifically (Section 6); and four review passes through the actual Person notes of Rocky Nguyen, Oma Cox, Ayden Springer, and Brian Ahuja — their documented Episteme/Techne/Voice, not invented positions.

**Date:** 2026-08-29

---

## 1. TL;DR

Money was never the real constraint. At the pipeline's current measured unit economics, $10,000 buys roughly a **million** more hypotheses than the entire known domain space contains pairs to generate. The question "what do we do with $10K of compute" is close to a category error — there isn't $10K of useful compute to spend against this architecture as it stands today.

The real gates are three, in this order:

1. **Two disclosed bugs are still open** (Section 13's "Failure 4" — the same-instance and comparison-word checks that are supposed to catch disguised-compromise hypotheses miss roughly a third to a half of real cases in the newest batch), and there is no independent integrity check for a *third*, undiscovered bug of the same shape as the scoring bug already found once by accident (Failure 5).
2. **Nothing runs this system without a human typing a command**, so "spend $10K running the system" currently has no literal mechanism — there is no scheduler.
3. **The stated mission has never been tested against reality.** Phase 3 — a real researcher confirming a hypothesis is genuinely novel — has zero real drafts sent, ever. Every dollar spent so far has purchased internal self-consistency, not external validation that a single Master's or PhD student's time has actually been saved.

Fix those three, and $10K becomes trivially affordable to spend well — mostly on people's time, not tokens.

---

## 2. The real unit economics

### 2.1 Cost by phase (live, as of this report — 89 ledger entries, includes the canary hypothesis run in Section 6)

| Phase | Calls tracked | Avg tokens/call | Total cost |
|---|---:|---:|---:|
| Verification (gpt-4o) | 31 | 5,450 | $0.4693 |
| Refutation (gpt-4o, 3 lenses/case) | 39 | 1,301 | $0.1527 |
| Generation (gpt-4o-mini) | 33 | 2,321 | $0.0226 |
| Audit — deep proposal (gpt-4o) | 2 | 4,268 | $0.0282 |
| Audit — observation (gpt-4o-mini) | 4 | 1,294 | $0.0009 |
| **Total** | **109** | — | **$0.6736** |

Computed directly from `token_usage.jsonl` using confirmed OpenAI list pricing (gpt-4o: $2.50/$10.00 per million input/output tokens; gpt-4o-mini: $0.15/$0.60 per million) — these rates were back-derived against the whitepaper's own published per-phase totals and match to within rounding, so this table is internally consistent with the whitepaper's Section 9.

**Honest caveat, stated plainly rather than smoothed over:** only 31–33 of the 89 ledger entries have a tracked generation/verification call. Token tracking was added to this pipeline partway through its life — earlier entries, and the entire original Claude-subagent-based refutation architecture (measured separately at ~34,700 tokens/lens, a different system, not in this log), predate it. **This table measures the current OpenAI-based pipeline's marginal, ongoing operating cost — it is not the sunk R&D cost of building the system**, which included many hours of Claude Code-assisted engineering (this session included) that is not instrumented anywhere in `token_usage.jsonl`. That distinction matters directly for a "$10K" question: it means the $10K is far more usefully framed as a *development/labor* budget than a *compute* budget, a point Section 7 returns to.

### 2.2 The domain pool — the actual scarce resource

| Source | Domains |
|---|---:|
| `domains.json` | 59 |
| `rosetta_stone_domains.json` | 23 |
| `equivalency_training_domains.json` | 88 |
| **Combined, deduplicated** | **170** |

- Bisociation and homospatial modes draw *pairs*: C(170, 2) = **14,365** possible pairs.
- Janusian mode draws a *single* domain and inverts it: addressable space is **170**, not 14,365.
- 89 hypotheses have been explored across all three mechanisms combined (one of them, the Section 6 canary, deliberately outside the pool — see below) — roughly **0.6%** of the 14,365-pair space.
- The engine's own bookkeeping (`domains.json`'s `already_paired` / `already_janused` / `already_homospatial` lists) exists specifically to stop the system from re-spending money re-confirming a pair it has already scored — a structural admission, built into the code itself, that the domain space, not the wallet, is the binding constraint.

### 2.3 The punchline

Blended real cost per hypothesis (generation + verification, plus refutation's expected contribution at the current ~29% NO_SIGNAL rate) works out to **≈$0.019/hypothesis**. At that rate:

- **$10,000 ÷ $0.019 ≈ 526,000 hypotheses** — about **37x** the entire 14,365-pair combinatorial space, generated exhaustively, once each.
- **Exhausting the entire known domain space once, generating and verifying every possible bisociation/homospatial pair and every janusian domain, costs on the order of $270–$300** — call it "under a few hundred dollars," with a wide margin for the small tracked-sample caveat above. Even a 10x margin of error on that estimate lands at $2,700–$3,000: still well under $10,000.

There is no version of "run more cycles" that meaningfully spends $10,000 against this architecture today. The system would either start re-exploring pairs it has already scored (wasted, and the code already guards against it) or run out of domains to draw from long before the money ran out.

---

## 3. Nine gating items, ranked

| # | Item | Status | Why it gates the spend | Flagged hardest by |
|---|---|---|---|---|
| 1 | Same-instance / comparison-word checks still miss real violations | **Open** (Failure 4) | In the newest batch, 3 of 6 new Janusian hypotheses and 1 of 6 homospatial hypotheses passed their own mechanical check while being the exact disguised-compromise pattern that check exists to catch. Scaling volume before this is fixed just scales the miss rate. | Ayden, Oma |
| 2 | No scheduler exists | **Open** | `run_cycle.py` is fail-closed and proven safe to run unattended, but nothing calls it. "Spend $10K running the system" has no literal mechanism yet — every cycle to date started with a human typing a command. | Ayden |
| 3 | Verification is 70% of the real spend, unaddressed | **Open**, flagged not fixed | $0.4693 of $0.6736 — "almost entirely the cost of feeding 25 real search results into the classifier for every hypothesis. No change has been made there yet" (whitepaper, verbatim). This is the one line that actually scales with volume. | Brian |
| 4 | Phase 3 (real researcher confirmation) has zero real drafts | **Open**, structural | The stated mission — recovering lost Masters/PhD research time — has never been tested against an actual researcher. Every dollar spent to date buys internal self-consistency, not external validation. | Rocky, Brian |
| 5 | Self-report score carries "almost no real signal" | **Open finding**, disclosed | Failure 5's aftermath: most hypotheses self-report the same value regardless of mode or eventual outcome; outcome rate is statistically indistinguishable from the pool average. Any future filter or scaling logic built on this field would encode noise as signal. | Brian |
| 6 | Domain pool has a real, quantifiable scale ceiling | **Known, quantified** (Section 2) | ~14,365 pairs total, 0.6% explored — plenty of room today, but "spend $10K on compute" runs into this wall long before the money runs out. | Oma |
| 7 | No integrity check exists for a "Failure 5 sibling" | **Open** | The scoring bug that silently corrupted 39/39 scored entries was found by accident, investigating an unrelated audit-agent proposal — not by any designed check. No control-test analog exists for the scorer itself, the way one now exists for refutation (Section 14). | Brian |
| 8 | Koestler's triptych as a 4th generation mode | **Ungrounded, new scope** | Confirmed via full repo search: zero references anywhere in this codebase today. Would need the same doctrine-sourcing and small-pilot discipline the existing three modes went through before touching any budget. | — (assessed in Section 5) |
| 9 | No ground-truth/calibration test had ever been run | **Resolved this session** | Addressed directly — see Section 6. | — |

---

## 4. Four persona reviews

### 4.1 Rocky Nguyen — the distribution-gap lens

Rocky's frame is the Three Ds — Design, Development, Distribution — with distribution treated as the piece almost everyone skips. His fixed instinct on anything new is "where is the distribution gap?", and his own track record backs a specific pattern: he commits real capital after seeing a working prototype, not before — he put $25,000 into MythosHealth once there was something real to look at, not on the strength of the pitch alone. That "show, then tell" discipline is the same lens he'd bring here.

Run through that lens, the readiness picture is uncomfortable in a specific way: the Eureka Engine has a working prototype — 89 real, verified, scored hypotheses, a public leaderboard, a dashboard, a whitepaper — but the actual distribution motion, the thing that turns a scored hypothesis into value someone besides the system itself can use, doesn't exist yet. Phase 3 is the distribution gap here, not a footnote to it: a "novel" hypothesis that never reaches a real researcher is exactly the failure mode his entire framework is built to catch. Rocky would not ask "can we afford to generate more hypotheses" — the ROTI table already answers that (yes, trivially). He'd ask: who is the first real person outside this pipeline who reads one of the 37 ADJACENT_ACTIVE or 24 COLLISION entries and does something with it, and what does that handoff actually look like? Distribution, in his 4Ds sense, is clip production and delivery once an interview happens — the analogous step here (packaging a verified hypothesis and getting it in front of an actual researcher) has a working mechanism designed (the +50/−20 Phase 3 scoring bands exist) and zero real executions.

His likely bottom line: the $10K should buy the first real distribution motion before it buys a single additional generation cycle. Spend on outreach, not on volume the pool can't even sustain.

| Rocky's top 3 blockers | |
|---|---|
| 1 | Phase 3 has never run for real — the entire "recover lost PhD time" mission is unproven |
| 2 | No distribution mechanism exists for a scored hypothesis to reach an actual researcher |
| 3 | More generation volume solves a problem (compute cost) that was never the real constraint |

### 4.2 Oma Cox — the staged-pilot doctrine

Oma's evaluation frame for any proposed change is the Vincentian Canon, restated in his own working language as the difference between *development* (a thing safely expanding to be more itself) and *alteration* (a thing quietly becoming something else). Applied to spend decisions specifically, he has a documented, near-verbatim doctrine from his own Workforce Lifecycle framework: *"you don't propose a $500K enterprise rollout, you propose a bounded study that proves the math... the pilot earns the right to scale."* His three-phase model for any new system is explicit — it starts by listening (collecting, correlating, watching outcomes with no assumptions baked in), then lets weights emerge from real data rather than assumption, and only in a third phase does the system earn the right to recommend anything, "only after it proves it can see what humans missed." His quality floor is equally explicit: "on-time, on-budget, *and good* — not two of three."

Measured against that doctrine, the Eureka Engine is genuinely partway there and genuinely not all the way there. The telemetry Oma would demand — real per-call cost data, not projected — already exists (`token_tracker.py`, Section 2 above). What doesn't exist yet is the third phase: nothing has "earned the right to recommend" anything, because Phase 3 has never closed the loop with a real outcome. Worse, by his own quality floor, two known defects (Failure 4, still open; the absence of any integrity check for a Failure-5-shaped bug) are exactly the kind of silent alteration his framework exists to catch — a system that is silently wrong some fraction of the time is not "good," regardless of whether it is on-time and on-budget. His anti-waste principle cuts the other way, though: *"wasting anything other than not learning, then it's a real waste"* — which means he would not tell Michael to sit on the $10K. He would tell him to spend a small, bounded fraction of it first, structured exactly like his own three-store pilot design (a lowest-performing case, a highest-performing case, and a mean case) — here, that reads as: fix Failure 4 and prove it against a fresh batch; run Phase 3 for real against a handful of real ADJACENT_ACTIVE candidates; and only then propose what the remaining $10K actually buys, priced from what that bounded pilot's real numbers say rather than from the current projection.

| Oma's top 3 blockers | |
|---|---|
| 1 | The system hasn't "earned the right to scale" — no phase-3 real-world outcome exists yet to price ROI against |
| 2 | Two known defects (Failure 4, no Failure-5-sibling check) violate the "good" third of his quality floor |
| 3 | $10K should be proposed as a bounded, criteria-selected pilot, not a lump-sum rollout |

### 4.3 Ayden Springer — the ship/prove/repeat lens

Ayden's documented position is short and consistent everywhere it appears: engineer-first, proof-of-work over credentials, "Ship. Prove. Repeat." His own Person note is notably thin on anything beyond engineering delivery — there is no recorded position from him on financial or investment judgment, and this section states that plainly rather than inventing one: what follows is inference from his documented engineering pattern, not a position he's actually taken.

Applying that pattern here, his read would almost certainly be the most literal of the four: this project already runs on his own standard — "It was proven, not just built" is the exact phrase used elsewhere in this project's own postmortem, for `verify_hypothesis.py`'s unattended fix. He'd apply that same bar to what's still outstanding. Failure 4 is not fixed, so by his standard it isn't done — a mechanical check that lets a third to a half of real violations through in the newest batch has been shipped, but not proven. There is no scheduler, so the system cannot actually "ship" the thing being asked about — running unattended for real, at volume, on a real cadence. And the audit agent's two proposals were both real, both wrong in their generated code, both caught before doing damage — which is the correct outcome of "ship, prove, repeat" working as designed, but it also means the loop isn't closed yet: propose → build → prove → adopt currently stops at "prove," by hard design, with no path to "adopt" other than a human manually rewriting a canonical file. His likely bottom line: fix Failure 4, prove it against a fresh batch the same way the fail-closed cycle logic was proven with a deliberately broken file; build the scheduler and prove it holds unattended for a real stretch of time; only then talk about scale.

| Ayden's top 3 blockers (inferred from pattern, not a documented position) | |
|---|---|
| 1 | Failure 4 is shipped but not proven — a real defect still passes review some of the time |
| 2 | No scheduler means the system literally cannot run unattended yet, whatever the budget |
| 3 | The audit agent's propose→prove loop has no adopt step — repeat never actually closes |

### 4.4 Brian Ahuja — the adversarial map/territory lens

Brian's stated epistemic anchor is Korzybski's "the map is not the territory" — every model, every self-report, every dashboard number is a representation, and his instinct is to look first at the gap between the model and what's actually true. He runs this adversarially by explicit design, including toward his own AI tools: no praise, no validation, explicit confidence levels, accuracy as the only success metric. He has a real, documented track record of applying exactly this discipline to this project specifically — he red-teamed the talentOS whitepaper itself across four review rounds, and the response to that review explicitly concedes multiple overclaims rather than defending them, on his own stated principle that "the right response to a good critique is to concede what's wrong before defending what isn't." Professionally, his investing thesis is upstream structural arbitrage — he backs value created at the source (raw chemistry, raw sourcing) rather than the consumer-facing layer built on top of it.

Both halves of that lens land hard on this specific audit. First, the map/territory gap: Failure 5's aftermath finding — that the self-report score "carries almost no real signal at all" — is precisely the kind of gap his epistemology exists to catch, and it was caught, but by accident, investigating something else. He would ask the obvious next adversarial question: what plays the same role, right now, for the *scorer itself*, that the control test in Section 14 plays for refutation? Refutation has a designed adversarial check (the strongest hypothesis in the pool, refuted on purpose, to see if the check is honest). The scoring pipeline has no equivalent — no one has yet tried, on purpose, to break the fixed `extract_self_score` the way the control test tried to break refutation. Second, the upstream-arbitrage read: in this pipeline's own supply chain, hypothesis generation is the cheap, commoditized layer ($0.0226 of $0.67, and falling further as domains exhaust) — the actual scarce, valuable input, the thing that gives every downstream claim its truth-value, is Phase 3's real researcher confirmation, which has never run. Spending $10K on more generation is, in his own framing, investing in the consumer-facing layer of a stack whose upstream input is still completely unvalidated. He would not treat this as a reason to stop — his review of the whitepaper concluded the system should be "auditable, not trusted on faith," a bar this repo already meets structurally (append-only ledger, timestamped, every claim traceable) — but he would insist the $10K buy an adversarial check for the scorer and real upstream validation (Phase 3) before it buys anything else.

| Brian's top 3 blockers | |
|---|---|
| 1 | No control-test analog exists for the scorer, the way one now exists for refutation |
| 2 | The self-report score's near-zero signal is a map/territory gap already found once by accident — what else is there? |
| 3 | Spend is aimed at the cheap, commoditized layer (generation) while the scarce upstream input (real researcher confirmation) stays untouched |

---

## 5. The Koestler triptych extension, assessed

The idea on the table: extend the three existing generation modes (bisociation, janusian, homospatial) with a fourth grounded in Arthur Koestler's triptych — the Jester/Sage/Artist framing of the comic (Ha!), the scientific (Aha!), and the artistic (Ah!) as three faces of the same underlying bisociative act.

**Confirmed by full-repo search this session: this reference does not exist anywhere in the codebase today.** "Koestler" appears in twelve files, but every occurrence is in the context of his 1964 bisociation concept (already the doctrine source for the bisociation mode) — never the triptych itself. This would be genuinely new scope, not an extension of something already scoped.

Two things gate it before any budget touches it, matching the exact discipline the existing three modes were built under:

1. **Real doctrine-sourcing from the primary text.** This report deliberately does not attempt to reconstruct the precise "first-page" triptych framing from memory — that would repeat exactly the failure mode this project's own postmortem exists to prevent (a plausible-sounding but unverified claim). The correct next step is reading the actual opening chapters of *The Act of Creation* (or a reliable secondary scholarly source) and writing a real `Ops/skills/koestler-triptych.md` doctrine file in the same format as `bisociate.md`, `janusian.md`, and `homospatial.md` — with a real citation, not an inferred one.
2. **A small pilot, not a rollout.** Every existing mode went through exactly this pattern: a small first batch (this project's very first bisociation/janusian/homospatial runs), a real defect found (Failures 1 and 2), a real fix, a real re-proof against a fresh batch. A fourth mode gets the same treatment — 5–10 hypotheses, run through the existing four-way verification classifier, before it's trusted with any share of a $10K budget.

Until both of those are done, a Koestler-triptych mode is an idea worth pursuing, not yet a line item.

---

## 6. The canary test, run for real

**Prediction stated before running it:** Andrew Lo's actual published Adaptive Markets Hypothesis (2004 paper; *Adaptive Markets: Financial Evolution at the Speed of Thought*, 2017) already substantially covers "evolutionary, game-theoretic equilibria that shift as market conditions change" — so a well-calibrated classifier should return **COLLISION or ADJACENT_ACTIVE**, not NO_SIGNAL, for a hypothesis this close to Lo's own framing.

**What was actually run**, live, against the production pipeline, for this report:

```
python3 hypothesis_engine.py --mode janusian --domain-a "Efficient Market Hypothesis"
python3 verify_hypothesis.py hypotheses/2026-08-29-janusian-efficient-market-hypothesis.md
python3 refute_hypothesis.py hypotheses/2026-08-29-janusian-efficient-market-hypothesis.md
python3 score_hypotheses.py
```

**The engine's own generated hypothesis** held: *"If both financial markets are efficient and inefficient simultaneously, then certain market anomalies will persist while others will disappear — which would not be predicted by either truth held alone."* — a real, independently-arrived-at instance of the same Janusian move the ChatGPT-assisted analysis reached (efficient AND inefficient, held simultaneously, not resolved by context).

**The actual result: NO_SIGNAL, not COLLISION — the prediction was wrong, and the reason why is the useful finding.** Verification's own five auto-generated search queries never once searched for "Andrew Lo" or "Adaptive Markets Hypothesis" by name — they searched general terms ("market anomalies and the efficient market hypothesis," "behavioral finance and market efficiency," etc.). The verifier's own written reasoning: *"none of the sources specifically explore the idea of markets being both efficient and inefficient simultaneously in a way that directly supports or refutes the hypothesis."* This is not a classifier-calibration failure so much as a **query-generation gap**: the search process never had a chance to find Lo's work because nothing in the pipeline searches for the specific researcher or named framework a hypothesis might already collide with — it searches the concept, generically. That's a real, concrete, fixable finding this canary surfaced for free.

**Since the verdict was NO_SIGNAL, refutation ran next — and it's a near-perfect live confirmation of Failure 4.** All three independent lenses returned REFUTED:

- **Coherence — REFUTED:** *"this is not a true paradox but rather a dual-context scenario mislabeled as paradoxical"* — the exact "compromise wearing paradox's clothing" pattern Failure 1/4 describes, this time catching it in real time on a case built specifically to probe that boundary.
- **Testability — REFUTED:** no operationalized threshold for "simultaneous efficiency and inefficiency" — unfalsifiable as stated.
- **Triviality — REFUTED:** reduces to "complex systems can be simultaneously stable and unstable," true of most complex systems, not a novel claim about markets specifically.

Final score: **+10** (self-reported Tension 5/5) **− 15** (refutation) **= −5 net**, ranked 63rd of 89. That self-report/outcome mismatch — maximum self-confidence, total refutation — is itself a live, unplanned re-confirmation of Section 3, item 5: the self-report score predicted nothing here.

**Real cost of this entire test: ≈$0.028** (generation 2,525 tokens/gpt-4o-mini; verification 6,103 tokens/gpt-4o; refutation 3,569 tokens/gpt-4o across three lenses) — confirming the unit-economics story in Section 2 at the individual-hypothesis level, not just in aggregate.

**On the ChatGPT-supplied analysis directly, engaged honestly rather than deferred to:** the Janusian framing — markets as simultaneously efficient and inefficient, refusing the false binary — is a genuinely correct instance of the mode's doctrine, and Koestler's own bisociation concept (colliding two "habitually incompatible frames of reference") is a reasonable lens for what Nash's equilibrium-discovery-under-repeated-play adds to it. But the specific synthesis is very likely **not novel** relative to Lo's own published work — Adaptive Markets Hypothesis already frames market efficiency as an evolving, ecological equilibrium rather than a fixed state, using language close to "efficiency is repeatedly rediscovered, not permanently achieved." This engine's own verifier missed that collision this time because of a query-generation gap, not because the collision doesn't exist. Stated plainly, not smoothed over: this is a good example of Janusian thinking as a *method*, and a weak candidate for a *novel, fundable hypothesis* as currently framed — exactly the distinction Section 3 of the whitepaper exists to draw.

This new entry is left in the local ledger (`verification-log.jsonl`, `leaderboard.md`) but has **not** been published to the live site — `publish_site.py` was deliberately not run as part of this report. Publishing it is a separate, outward-facing decision.

---

## 7. If the gates clear — a recommended $10K allocation

Given Section 2's finding — raw compute is nearly free, and the domain pool caps out around $300 to exhaust once — almost none of $10,000 should go to token spend. A rough allocation, weighted toward the gating items in Section 3:

| Allocation | Amount | What it buys |
|---|---:|---|
| Fix Failure 4 + prove it | $1,500 | Engineering time rebuilding the same-instance and comparison-word checks (likely: scan every section, not just §3, per the diagnosed cause), then a fresh batch proving it holds |
| Build + prove a scheduler | $1,500 | A real cron/launchd wrapper around `run_cycle.py`, proven running unattended for a real stretch (days, not one run) before being trusted with volume |
| A control-test analog for the scorer | $1,000 | Brian's gap, closed: an adversarial, on-purpose attempt to break the fixed `extract_self_score`, mirroring the refutation control test in Section 14 |
| Real Phase 3 outreach — labor, not compute | $4,000 | Actually contacting real researchers behind a handful of the 37 ADJACENT_ACTIVE / 24 COLLISION entries — Rocky's and Brian's shared gap, and the only line item that tests the stated mission against reality |
| Koestler-triptych doctrine + pilot | $500 | Real primary-source grounding + a 5–10 hypothesis pilot, same discipline as the existing three modes |
| Raw pipeline compute (generation/verification/refutation/audit at scale) | $1,500 | At ~$0.02/hypothesis blended, this alone funds roughly 75,000 hypotheses — more than 5x the entire known domain space, several times over |

That leaves real margin unallocated, on purpose — Oma's doctrine says the bounded pilot (rows 1–3 and 5 above) should run first and *set the price* of what rows 4 and 6 look like at full scale, rather than committing the whole $10K up front against numbers no real pilot has produced yet.

---

## 8. Final verdict

The Eureka Engine is not under-resourced; it is under-tested against the world it claims to serve. Its unit economics are already excellent — cheap enough that the domain pool, not the wallet, is the real ceiling on raw generation — and its self-audit discipline is real (two proposals made, both wrong, both caught before doing damage, exactly as the hard-coded additive-only constraint was designed to guarantee). What it has never done is close the loop on its own stated purpose: no hypothesis has yet reached a real researcher, no scheduler runs it without a human, and two known defects (plus, per this report's own canary, the possibility of others the mechanical checks still miss) remain open. Rocky's distribution-gap lens, Oma's staged-pilot doctrine, Ayden's ship-prove-repeat bar, and Brian's adversarial map/territory instinct converge, from four genuinely different starting points, on the same conclusion: spend the $10K on closing those three gaps first — the compute will still be nearly free when it's actually time to scale.

---

*Exponent Labs LLC · scientific-intuition-engine/umpf_pipeline · Generated 2026-08-29 · Sourced from `whitepaper.html`, `token_usage.jsonl`, `verification-log.jsonl` (89 entries), and the four Person notes in the talentOS vault.*
