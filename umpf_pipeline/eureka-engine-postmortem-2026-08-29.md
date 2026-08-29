# The Eureka Engine — Postmortem: The Audit-Response Arc

**Scope:** one continuous chain of work, same day, from the first "what must be addressed before we spend $10K" question through a real, corrected 151-entry ledger. Eight commits, seven real bugs found and fixed (two of them in code written *during* this same arc), two new external integrations, one design principle (latest-entry-wins) settled. Written the way this project writes every postmortem — what actually happened, including the parts that didn't work the first time.

**Date:** 2026-08-29

---

## TL;DR

A readiness audit asked what would be wasted if $10K were spent running this system. The honest answer was: money was never the constraint, but three real gates were — two disclosed bugs, no scheduler, and no adversarial check on the scorer itself. Fixing those, then testing the fix with a real bounded ($1) production run, surfaced two *more* real bugs no smaller test had been large enough to catch. Fixing those surfaced a third. Along the way, the single most consequential external dependency (Tavily) turned out to be down for the better part of an hour, which forced a real search-provider fallback (Monid/Exa) into existence — and a mid-fix efficiency bug in that same fallback was caught not by any check this project wrote, but by the person running it, in real time. Every fix in this arc was proven against real data before being called done; two of them were proven wrong the first time and fixed again.

## Timeline

| Commit | What it did |
|---|---|
| `aae5c20` | $10K readiness audit + a real canary hypothesis test (EMH/Nash — predicted COLLISION, got NO_SIGNAL, a real finding about query generation) |
| `8181688` | PRD v2: fixed Failure 4 (mechanical same-instance/comparison checks), closed the query-gen gap, built the scheduler, built a control test for the scorer (found 2 more real bugs) |
| `091ab1f` | Code freeze point: widened refutation's scope to catch ADJACENT_ACTIVE hypotheses that failed their own honesty check |
| `0368635` | The frozen $0.87 real run: found a silent filename-collision data-loss bug and a flag-erasure interaction bug between two of the same day's own fixes |
| `259e194` | Fixed both |
| `21ee6ae` | Proved both fixes live (twice — once deliberately, once by natural collision); found and fixed a *third* bug (a downstream file-matching ambiguity) as a direct side effect of proving the first |
| `d90644e` | Found the real cause of a string of NO_SIGNAL verdicts: Tavily rate-limiting, silently returning zero evidence classified as if it were real. Added retry/backoff, `PENDING_VERIFICATION`, and a Monid/Exa fallback |
| `1d7358f` | Designed and built `ledger.py` (latest-entry-wins read for the append-only ledger); re-verified all 11 real hypotheses corrupted by the Tavily outage; caught and fixed a circuit-breaker gap mid-task, flagged directly by the human running it, not by any automated check |

## What was found, in the order it was found

### 1. The domain pool's own math made "$10K of compute" the wrong question

At the pipeline's real measured unit economics (~$0.019/hypothesis blended), $10,000 buys roughly 37x the entire 14,365-pair combinatorial space, generated exhaustively once. Exhausting it once costs on the order of $300. The real gates were never dollars.

### 2. Failure 4 (same-instance / comparison-word checks) — fixed mechanically, and a real structural finding underneath

Janusian's same-instance test had been a soft, prompt-only self-check with no code enforcement at all; homospatial's comparison-word scan only ever checked §3, missing violations that landed in §2. Both fixed: janusian got its first mechanical context-split scanner (retry once, then honestly flag); homospatial's scan was extended to both sections.

Proven at scale, not just in principle: across a real 39-hypothesis batch, the comparison-word check retry-fixed cleanly 89% of the time it fired. The context-split check retry-fixed only 20% of the time — 8 of 10 janusian hypotheses that tripped it stayed flagged even after a targeted correction. Read as a real property of the mode meeting real domains (many domains simply don't support a genuine same-instance paradox, and the model defaults to a disguised compromise rather than honestly saying so), not a prompt-engineering gap left to keep chasing.

### 3. The query-generation gap — found by a canary, closed with a mechanical check, measured at real compliance rates

The EMH/Nash canary test predicted the classifier would find Andrew Lo's actual Adaptive Markets Hypothesis. It didn't — because none of the five auto-generated search queries ever searched for "Andrew Lo" by name. A soft prompt instruction requiring a named-entity query got 33% real compliance on the first test. A mechanical, retry-enforced version got 92-100%.

### 4. The scorer had never been adversarially tested — until it was, and it found two more real bugs

`control_test_scorer.py` was built specifically in response to Brian Ahuja's review gap: no control test existed for the scorer, the way one already existed for refutation. It found two real, previously undetected bugs in `extract_self_score()` before any real data ever hit them — a hallucinated multi-digit score silently truncated to its first digit, and a case-varied label silently returning `None`. Both fixed, regression-checked against all 76 real hypothesis files on disk: zero differences.

### 5. Silent, permanent data loss via filename collision

`short_name()` reduces long domain descriptions to a short slug for filenames. Two genuinely different domains — "Architecture — modular/prefab construction" and "Architecture (Creative & Performance Systems)..." — both reduced to "Architecture." The second's real, generated output silently overwrote the first's file before verification ever read it. `domains.json` still marked the destroyed domain "already explored," with no hypothesis, verification, or ledger record it was ever attempted. Confirmed via full-repo domain-pool analysis: **25 short-name collision groups already exist in the real 170-domain pool** — this was never a one-off coincidence, it was a structural, everyday risk.

Fixed: `save_hypothesis()` now checks for an existing file before writing and disambiguates with a numeric suffix, loudly, instead of overwriting. Proven twice live: once by deliberately re-triggering the exact real collision (two fresh, real, unexplored domains), once naturally (an autonomous draw of "Control theory — Kalman filtering" collided with a pre-existing entry, unprompted).

### 6. The collision fix's own disambiguation suffix broke a downstream file-matcher

Proving Finding 5 immediately surfaced Finding 6: `assemble_experience_data.py`'s `find_by_substring()` did a bare substring-containment match. A base slug like `...control-theory` is a literal substring of both its own file and the new `...control-theory-2` file, producing real `AMBIGUOUS` warnings on the live run. The existing "shortest match wins" tie-break happened to resolve every real case correctly — checked directly against the assembled experience data, no actual content mix-up occurred — but relying on a lucky tie-break as a permanent guarantee was exactly the kind of gap this project's discipline exists to close. Fixed properly: try an exact filename match first, before ever falling into the substring search.

### 7. Tavily rate-limiting corrupted real Phase 2 verdicts — the most serious finding of the day

A real production run hit sustained Tavily HTTP 432s (Tavily's own rate/quota-limit code) on 11 of 17 verifications in one batch. Every query in those 11 calls failed; `run_searches()` silently returned zero results; `classify()` was handed "(no search results returned for any query)" as if that were real evidence. The classifier's own reasoning said so plainly — *"the absence of search results indicates... this lack of information means the hypothesis cannot be verified"* — and still output a definitive NO_SIGNAL verdict. This is a real Phase 2 classification corrupted by infrastructure failure, not a secondary score or filename — the actual thing this project's entire discipline exists to protect.

Fixed two ways: retry/backoff on rate-limit-shaped Tavily errors, fail-fast on real ones (mirroring `retry.py`'s existing OpenAI pattern); and if every query still fails after retries, mark `PENDING_VERIFICATION` — an existing, already-handled status in `score_hypotheses.py` and `assemble_experience_data.py` that no code had ever actually written until this fix.

### 8. Monid/Exa, wired in as a real fallback

Installed the Monid CLI, configured a real API key, discovered Exa's `/search` endpoint. Wired into `verify_hypothesis.py` as a fallback that only fires once Tavily's own retries are exhausted — a metered, paid call, deliberately kept a backstop, not the primary path. Proven with a real (not mocked) test: Tavily's HTTP layer was mocked to always fail, and the fallback recovered 5 real results, including the actual Andrew Lo paper the original canary test had missed — closing that specific loop for real.

### 9. The circuit-breaker gap — caught by a human, not a check

Re-verifying the 11 real hypotheses corrupted by Finding 7, Tavily was found to be *still* down — every single query, for 20+ minutes straight, with zero real successes. The existing retry logic kept paying the full ~22-second retry cost on *every subsequent query*, even though the service had already been confirmed dead for the rest of the run. This was pointed out directly, in the middle of the work, not discovered by any test this project had written: *"if the web search didn't work we have to... I shouldn't have to explain this to you."* Fair, and correct. Fixed properly: a real circuit breaker — the first query in a process pays the full retry cost; once it's confirmed Tavily is down, every later query in that same process skips straight to Monid with zero wasted delay. Proven synthetically (first query: 4 attempts; every query after: 1) before being used to actually finish the remaining re-verifications.

### 10. The ledger's append-only design needed a read-side convention it never had

Re-verifying the 11 corrupted entries meant appending new, correct lines for slugs that already had an old, wrong one. Every downstream reader — the scorer, the leaderboard assembler, both refutation-selection functions, the verification-dedup check — had been written assuming every ledger line was independently valid, with no notion of "this line supersedes that one." Designed and built `ledger.py`: a single, shared "latest entry per slug wins" read, adopted by every one of those four readers. The ledger's write side is completely untouched — still strictly append-only — only how it's read changed.

## Real outcome of the 11 re-verifications

All 11 hypotheses previously scored as a uniform, spurious NO_SIGNAL (built on zero real search evidence) now carry real, varied, evidence-based verdicts:

| Verdict | Count |
|---|---|
| ADJACENT_ACTIVE | 7 |
| COLLISION | 2 |
| NO_SIGNAL (real this time) | 2 |

The 6 that needed refutation under the widened rule (2 real NO_SIGNAL, 4 ADJACENT_ACTIVE-and-flagged) were all independently REFUTED 0-of-3 again — the unbroken record extends rather than breaks. `audit_agent.py`'s own observation after rescoring: janusian mode's average points rose from 18.2 to 21.8 — a real, measured effect of the correction, not a cosmetic one.

## Final state

- **151 ledger entries** (deduplicated; 164 raw lines on disk, reflecting real correction history, not data loss).
- Verdicts: 80 ADJACENT_ACTIVE, 41 NO_SIGNAL, 28 COLLISION, 1 FLAGGED, 1 FACT_CHECK_FAIL.
- Refutation record: **0 of 54 survived**, project lifetime, unbroken.
- Real cost today: **$2.38 in OpenAI calls, $0.73 in Monid/Exa calls — $3.11 total**, for eight commits' worth of real fixes, three proving batches, and a full 11-entry correction.

## What's still open, honestly

- **Phase 3 (real researcher outreach) — still zero real drafts.** Flagged by Rocky Nguyen's and Brian Ahuja's reviews as the actual gap that matters most; still true. This is real human labor, not something today's work touched.
- **The Koestler triptych mode — still not built.** Confirmed absent from the codebase; needs primary-source doctrine grounding before a pilot, exactly as the original audit concluded.
- **Verification cost — still the single largest cost line ($1.56 of $2.38 today), unaddressed.** No low-risk fix identified; a dedicated pass with its own before/after quality comparison is the honest next step, not a rushed trim.
- **One control-test-scorer edge case left open by design** (a score label mentioned twice in one section, ambiguous which is real) — forcing a fix would trade one failure mode for a different, not-obviously-better one.
- **The scoring-consequence question from earlier in the day turned out to be mostly self-resolving**, not because it was directly fixed, but because widening refutation's scope gives a flagged-and-ADJACENT_ACTIVE hypothesis a real negative-point consequence once it fails refutation — which, this arc's data shows, it reliably does.

## The pattern worth naming, across all of this

Every one of today's real bugs was found at a scale, or under conditions, that a smaller test hadn't reached: the filename collision needed 40 real domain draws before two of them coincided; the Tavily outage needed a long enough real run to distinguish "occasional blip" from "sustained failure"; the flag-erasure bug needed a hypothesis that tripped *two* checks in the same generation call. None of these were found by imagining edge cases in the abstract — all of them were found by running the real thing, at real scale, and reading what actually happened instead of assuming the fix already worked. That discipline is the actual throughline of this arc, more than any individual bug.

---

*Exponent Labs LLC · scientific-intuition-engine/umpf_pipeline · Generated 2026-08-29 · Sourced directly from `token_usage.jsonl`, `verification-log.jsonl` (151 entries via `ledger.py`), `git log`, and the Monid CLI's own balance report.*
