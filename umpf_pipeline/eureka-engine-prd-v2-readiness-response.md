# Eureka Engine PRD v2 — Readiness Response

**Source:** `eureka-engine-10k-readiness-audit.md` (2026-08-29). This PRD converts that audit's nine gating items and $10K allocation table into concrete courses of action, synthesized (not followed as a single recommended path) into one bounded implementation pass — then Part 2 reports what actually happened when they were built and run for real.

**Date:** 2026-08-29

---

# Part 1 — PRD

## 1. Context

The readiness audit concluded that money was never the Eureka Engine's real constraint — unit economics are cheap enough ($0.019/hypothesis blended) that $10,000 buys roughly 37x the entire known domain space. The real gates were three disclosed-but-unaddressed problems: two open bugs (Failure 4's same-instance and comparison-word checks still missing real violations), no scheduler, and no adversarial control test for the scorer itself (the gap that let Failure 5's scoring bug run silently for the system's entire life until an unrelated audit-agent investigation stumbled onto it). A fourth finding came from the audit's own canary test: the search-query generation step never searches for named researchers or frameworks, which is exactly why the EMH/Nash canary missed its real, findable collision with Andrew Lo's Adaptive Markets Hypothesis.

This PRD addresses those four directly. Phase 3 (real researcher outreach) and the Koestler triptych mode are **explicitly and deliberately not implemented this pass** — see Section 5.

## 2. Objectives

After this PRD executes, all four should be true:

1. A disguised compromise in janusian mode, and a comparison-language violation in homospatial's §2, are both **caught mechanically** (not just by a soft prompt instruction), the same way homospatial's §3 check already worked.
2. Hypothesis generation makes a real, checkable attempt to search for a named prior researcher/framework, not just the general concept — closing the specific gap the EMH canary found.
3. `run_cycle.py` can be invoked by an actual scheduler (cron/launchd) with its exit-code contract intact, proven by a real invocation through the wrapper, not just inspection of the code.
4. The scorer (`extract_self_score`) has been adversarially tested on purpose, the way refutation already has a control test — any bug the test finds gets fixed and regression-checked against the real ledger before being called done.

## 3. Courses of Action

| # | COA | Audit finding addressed | Approach | Status |
|---|---|---|---|---|
| 1 | Mechanical same-instance check (janusian) + extend homospatial's scan to §2 | Failure 4 (open) | Add `_find_context_split_phrases()` scanning §4 for janusian (retry-once, then flag honestly if still failing); extend `_find_comparison_words()` to scan §2 as well as §3 for homospatial | **Implemented** |
| 2 | Close the query-generation gap | The EMH canary's real finding (Section 6 of the audit) | Add an instruction to all three prompt templates: at least one Search Query must target a named theory/framework/researcher, with an explicit fallback pattern ("[X] named theory OR framework OR researcher") when the model can't think of one | **Implemented (soft instruction only — see Part 2 for real compliance rate)** |
| 3 | Build + prove a scheduler | Gating item #2 (no scheduler exists) | `run_cycle_scheduled.sh` — thin wrapper preserving `run_cycle.py`'s exit-code contract, timestamped logging, cron/launchd install snippets included but **not installed** | **Implemented and proven by a real invocation; not registered as a standing cron/launchd job — that's a separate decision** |
| 4 | Control test for the scorer | Gating item #7 (Brian Ahuja's blocker — no adversarial check for a "Failure 5 sibling") | `control_test_scorer.py` — 7 synthetic adversarial cases against `extract_self_score` | **Implemented; found 2 more real bugs, both fixed and regression-checked** |
| 5 | Phase 3 outreach | Gating item #4 | — | **Deliberately deferred — see Section 5** |
| 6 | Koestler triptych mode | Section 5 of the audit | — | **Deliberately deferred — matches the audit's own conclusion** |
| 7 | Verification cost reduction | Gating item #3 | — | **Deliberately deferred — no low-risk fix identified this pass** |

## 4. Success criteria

- COA 1: a fresh batch containing both janusian and homospatial hypotheses shows the new checks actually firing on real model output (not just passing on hand-written synthetic input).
- COA 2: at least one hypothesis in a fresh batch contains a real named-entity search query it would not have generated before this change.
- COA 3: `run_cycle_scheduled.sh` runs a real cycle end-to-end, exits with `run_cycle.py`'s real exit code, and produces a readable timestamped log.
- COA 4: `control_test_scorer.py` is run before and after any fix it motivates; the ledger's real 89 (now more) entries are regression-checked to confirm no existing score changed.

## 5. Explicitly out of scope this pass, with reasons

- **Phase 3 real researcher outreach** — this is genuine human labor (identifying and actually contacting a real person), not something to mechanize under time pressure. Building a tool that pretends to find "the researcher" without a real, reliable mechanism for doing so would produce something that looks like progress without being it — exactly the kind of meta-work this project's own Operator Hang-Up Protocol warns against. Left as the $4,000 human-labor line item the audit already named.
- **Koestler triptych mode** — the audit's own Section 5 concluded this needs real primary-source doctrine grounding before a pilot, not a rebuild-under-pressure. Nothing here changes that conclusion.
- **Verification cost reduction** — the audit flagged this as the single largest cost line (69% of spend) but named no specific low-risk fix (e.g., trimming from 25 search results to fewer risks silently degrading verification quality with no fresh data to check against). Left for a dedicated pass with its own before/after quality comparison, not bundled in here.

---

# Part 2 — Post-Mortem

**What was actually run:** `./run_cycle_scheduled.sh --hypotheses-per-mode 2` — a real, fresh 6-hypothesis cycle (2 bisociation, 2 janusian, 2 homospatial — deliberately weighted to test both fixed modes directly, not the default mode-weighted split) through the fully updated pipeline, followed by a synthetic adversarial run of `control_test_scorer.py` before and after the scorer fix. Total real cost: **$0.1127** (10 generation calls — 6 initial + 4 retries — plus 6 verification calls, 3 refutation calls, 1 audit observation).

## COA 1 — Mechanical checks: real, honest, mixed results

**Homospatial's §2 extension worked cleanly, both times it fired.** Both of the two homospatial hypotheses this run tripped a real §2 comparison-word violation the old code would have missed entirely (`Cryptography ⊕ Cognitive Development`: "similar to, parallels"; `Linguistics — Creole Genesis ⊕ Economics`: "similar to, akin to") — confirming the exact gap the audit diagnosed (the Phonetic Turbulence case's §2 violation going unscanned) is now caught. Both retries passed clean on the first correction.

**Janusian's new mechanical check caught real violations — but the retry did not fix the underlying tendency, in either case it fired.** Both janusian hypotheses this run (`Human Learning Uncertainty`, `Climatology — feedback loops in ice-albedo effect`) tripped the new context-split scan on first generation, were retried once with a correction, and **still contained context-split language after the retry** ("depending on, in other situations"; "in some instances"). This is disclosed honestly in the output itself, exactly as designed — not silently accepted. It's also the same lesson this project has now learned three times in a row (homospatial's original comparison-word fix, the pre-existing note admitting a soft prompt instruction "did NOT reliably hold... verified directly," and now this): a strong generative tendency toward hedge language does not reliably yield to one corrective retry. The check now makes the problem **visible** — a real improvement over the prior soft-only self-check, which caught nothing mechanically at all — but it does not yet make the problem **go away**. Neither flagged hypothesis happened to reach refutation this run (both were ADJACENT_ACTIVE/COLLISION, not NO_SIGNAL), so their disguised-compromise risk currently sits disclosed in the hypothesis file's own text with no scoring consequence — see the new finding below.

## COA 2 — Query-generation gap: partial compliance, a real number instead of a guess

Of the 6 fresh hypotheses, **2 of 6 clearly complied** with the new named-entity-query instruction: `Human Learning Uncertainty` generated the real query "John Dewey uncertainty in education" (a genuine named researcher, unprompted), and `Gaming Narrative × Cognitive Attention Map Evolution` generated "attention mapping theory OR framework" (the literal fallback pattern the instruction specifies). The other 4 did not produce anything clearly named-entity-shaped. **33% real compliance on a soft instruction is itself the finding**, not a disappointing result to smooth over — it's the same pattern COA 1 just re-confirmed: a prompt-only instruction gets partially followed. The honest next step, not taken this pass, is the same fix already applied twice elsewhere in this codebase: check the actual Search Queries output mechanically (e.g., for the literal "OR" fallback pattern or a capitalized proper noun the domain name doesn't already contain) and retry once if none is found.

## COA 3 — Scheduler: proven, not installed

`run_cycle_scheduled.sh` ran the real cycle above end-to-end, wrote `scheduler_logs/2026-08-29T19-35-27Z.log`, and exited 0 — `run_cycle.py`'s own real exit code, preserved correctly through the wrapper. This closes the literal mechanism gap (gating item #2): something now exists that a real cron/launchd entry can point at. **It has deliberately not been registered as a standing, unsupervised job** — installing a recurring task that spends real API budget and pushes to a public GitHub repo on a timer is a persistent-configuration decision, not a code change, and is left for Michael to make explicitly (the crontab/launchd snippets are in the script's own comments, ready to use).

## COA 4 — Scorer control test: found 2 more real bugs, fixed both, left 1 open honestly

Run before the fix: **4 of 7** synthetic adversarial cases passed. Two real, previously-undetected bugs confirmed:
- A hallucinated out-of-range score like "10" was silently truncated to "1" by the old single-digit regex — the same *shape* of bug as Failure 5, not yet triggered in real data (checked directly: no multi-digit values exist in the 76 real hypothesis files on disk today) but a real landmine.
- A case-varied label ("fusion distance" vs. "Fusion distance") silently returned `None` instead of the real score.

Both fixed (`(\d+)` instead of `(\d)`, `re.IGNORECASE` added) and **regression-checked directly against all 76 real hypothesis files: 0 differences between old and new extraction** — the fix is additive-safe. Run after the fix: **6 of 7** cases pass. The 7th (a score label mentioned twice in one section, ambiguous which is "the real one") is left open on purpose — forcing last-match-wins instead of first-match-wins would trade one failure mode for a different, not-obviously-better one, and this project's own discipline is to disclose an open edge case rather than force an unproven fix under time pressure.

## New finding this test surfaced, not anticipated by the PRD: the honesty flag has no scoring consequence

`score_hypotheses.py` does not currently check for the "Automated check failed twice" flag either mechanical check can now write into a hypothesis file. Both janusian hypotheses that failed their retry this run scored **+38** — identical to a hypothesis that passed the check cleanly. The mechanical check now tells a human reader "this may be a disguised compromise," but tells the scorer nothing. This is a real, freshly-discovered gap, not fixed this pass (found too late in an already-large implementation to make a scoring-logic change responsibly under time pressure) — named here explicitly as the next concrete follow-up, in the same spirit as Failure 4 being left disclosed-but-open rather than papered over.

## Ledger state after this pass

95 entries (89 → 95: 6 new this cycle). Verdict distribution: ADJACENT_ACTIVE 41, NO_SIGNAL 27, COLLISION 25, FLAGGED 1, FACT_CHECK_FAIL 1. Refutation record: **still 0-of-27 survived** — every NO_SIGNAL case to date, including this run's one new refutation, has been REFUTED; the disclosed record extends cleanly rather than breaking.

## Final verdict

Three of the four objectives were fully met (mechanical checks now exist and fire on real output; the scheduler is built and proven; the scorer has a real control test that found and fixed two more bugs). The fourth (the query-generation gap) is honestly only a third closed — a real, measured number rather than an assumed fix. And the test run itself surfaced a genuinely new gap the PRD didn't anticipate: the mechanical checks now *see* a disguised compromise but the scorer doesn't yet *care*. That's the correct shape for this kind of pass — real fixes, real proof, and an honest list of what's still open, not a claim that everything named in the audit is now resolved.

---

*Exponent Labs LLC · scientific-intuition-engine/umpf_pipeline · Generated 2026-08-29 · PRD synthesized from `eureka-engine-10k-readiness-audit.md`; Post-Mortem sourced from a real run of `run_cycle_scheduled.sh`, `control_test_scorer.py`, and direct inspection of `token_usage.jsonl` / `verification-log.jsonl` (95 entries).*
