# The $1 Frozen-System Audit

**What this is:** per Michael's instruction — freeze all code after the PRD v2 MUST-FIX pass, spend ~$1.00 of real OpenAI budget running the frozen system exactly as-is, then audit what actually happened. No code was touched during the run (confirmed: `git status` shows zero `.py` files changed, only data/content). This audit found two real, previously-unknown bugs — one of them in code written *this session*, in direct interaction with a fix from the previous pass. Both are reported here, not fixed — the freeze holds until Michael decides how to proceed.

**Real spend:** $0.8691 (79 generation calls, 39 verification calls, 54 refutation calls). Ledger: 95 → 134 entries.

---

## Finding 1 (new, serious): a silent, permanent data-loss bug — filename collisions on `short_name()`

`hypothesis_engine.py`'s `short_name()` shortens long domain descriptions for filenames by splitting on the first `" ("`, `" — "`, or `" -- "` and keeping only what's before it. Two *different* domains this run —

- `"Architecture — modular/prefab construction"`
- `"Architecture (Creative & Performance Systems) — Atomic: Building permits approved/denied..."`

— both reduce to the short name `"Architecture"`, and therefore the identical slug and filename: `2026-08-29-janusian-architecture.md`. `save_hypothesis()` writes with no collision check, so the second domain's real output **silently overwrote the first's** on disk. Confirmed directly:

- The console log shows two separate `✅ Saved to .../janusian-architecture.md` lines (once at generation #9, once at #10).
- The file on disk today contains only the second domain's content.
- `domains.json`'s `already_janused` list contains **both** domain strings — meaning `"Architecture — modular/prefab construction"` is now permanently marked explored and can never be drawn again, even though its actual generated hypothesis was destroyed before verification ever read it.
- `verification-log.jsonl` contains exactly one `janusian-architecture` entry, not two — the ledger has no record the first domain was ever attempted.

**Real cost of this bug:** one full generation call (and whatever retries it triggered) spent for a hypothesis that was never verified, never scored, and can never be regenerated — permanent, silent loss, with zero error or warning anywhere in the run. This happened on 1 of 40 domain draws this run (2.5%). It did not happen in either of the two smaller test batches earlier this session (6 hypotheses, then again 6) — first surfaced at this larger, more realistic batch size, which is exactly the kind of thing a small proving run can miss and a real-scale run finds.

**Not fixed this pass — freeze holds.** The fix is straightforward (check for an existing file at the target path and append a short disambiguating suffix, or hash the full un-shortened domain string into the slug when a collision would occur) but is a code change, and the whole point of this audit was to report the frozen system's real behavior, not patch it mid-audit.

---

## Finding 2 (new, serious): the query-gen fix can silently erase an earlier check's failure flag

This is a bug in code written *this session*, found only because this run was large enough to produce the specific interaction that triggers it.

**The mechanism:** every hypothesis template's `"## Search Queries"` section is the *last* section in the document. When janusian's context-split check (or homospatial's comparison-word check) fails twice, it appends a `"**⚠️ Automated check failed twice:**..."` warning to the end of `raw_output` — which, since Search Queries is already the last section, lands *after* it. If the universal query-gen check then *also* needs a retry on the same hypothesis, `_replace_queries_section()`'s regex (`## Search Queries\s*\n.*\Z`, with `DOTALL`) matches from `"## Search Queries"` to the literal end of the string — which now includes the previously-appended failure warning — and replaces all of it with just the new query block. **The earlier check's honest failure flag is silently deleted.**

**Confirmed directly, three real cases this run:**

| Hypothesis | Mode-specific check | Query-gen check | Flag present in final file? |
|---|---|---|---|
| `janusian-physical-electrical-noise` | Failed twice (context-split) | Tripped, retry ran | **No — erased** |
| `janusian-human-social-influence` | Failed twice (context-split) | Tripped, retry ran | **No — erased** |
| `homospatial-geology-x-music-sound` | Failed twice (comparison-word) | Tripped, retry ran | **No — erased** |
| `janusian-behavioral-psychology` | Failed twice (context-split) | Passed clean, no retry | Yes — intact (control case) |
| `janusian-artificial-intelligence` | Failed twice (context-split) | Passed clean, no retry | Yes — intact (control case) |

The pattern is exact: the flag survives only when the query-gen check *doesn't* need its own retry. The moment both checks need a correction on the same hypothesis, the second one's patch silently destroys the first's evidence.

**Real consequence:** all three of the erased-flag hypotheses landed on verdict `ADJACENT_ACTIVE` — exactly the verdict the previous pass's MUST-FIX #1 (widened refutation scope) exists to catch when the honesty flag is present. Because the flag was erased before `refute_hypothesis.py` ever ran, **none of these three were swept into refutation.** They are sitting on the public leaderboard right now, scored as clean ADJACENT_ACTIVE findings, despite each one failing its own mechanical honesty check — the exact failure mode Finding 1's sibling fix was built to prevent, defeated by an unrelated bug in the fix built alongside it.

**Not fixed this pass — freeze holds.** The fix is also straightforward (either check for the flag before doing the query-gen replacement and re-append it after, or make the query-gen check run *first*, before any mode-specific check has a chance to append trailing content) — but again, this is a code change, reported not applied.

---

## What the mechanical checks actually did, precisely counted (not estimated)

| Check | Mode | Tripped | Fixed by 1 retry | Still failed (flagged) |
|---|---|---:|---:|---:|
| Named-entity query | Bisociation (n=13) | 12 | 11 | 1 |
| Named-entity query | Janusian (n=12) | 3 | 3 | 0 |
| Named-entity query | Homospatial (n=15) | 5 | 5 | 0 |
| Comparison-word (§2/§3) | Homospatial (n=15) | 9 | 8 | 1 |
| Context-split (§4, same-instance) | Janusian (n=12) | 10 | **2** | **8** |

**The named-entity query check and the comparison-word check both retry-fix cleanly (89–100%).** They're shallow, mechanical corrections — swap out a phrase, add a query — and the model executes them reliably when told exactly what's wrong.

**The context-split check does not fix cleanly on retry (20% — the outlier by a wide margin).** This is the most important structural finding in this audit, more important than either bug above for what it says about the mode itself. Janusian mode's own doctrine (`umpf_janusian_prompt.md`) says a genuine same-instance paradox requires the domain's assumption to be *load-bearing enough* that its exact opposite sounds absurd — not every domain clears that bar. The context-split language ("depending on," "in some contexts") isn't a wording accident the model can patch on request; it's the visible symptom of the model having picked a domain where it *couldn't* find a genuine paradox, and defaulted to a disguised compromise instead of using §7's own honest out ("say so plainly ... rather than presenting a context-split compromise as (C)"). Telling it to rewrite without the banned phrases doesn't give it a paradox it didn't have — it just asks it to hide the symptom, which is exactly why it mostly can't comply. **This run's real numbers say roughly one in three janusian domains this batch actually supported a genuine paradox (2 passed clean + 2 fixed on retry = 4 of 12); two in three did not (8 of 12 still flagged after the best correction available).**

---

## Refutation: the widened net worked exactly as designed, where the flag survived

Of 18 hypotheses refuted this run, 11 were the original NO_SIGNAL population and 7 were new — caught only because of the previous pass's widened `--all-pending` rule (ADJACENT_ACTIVE + honesty flag present). **All 7 were independently REFUTED, 0-of-3, by adversarial review that had no knowledge of the mechanical flag at all.** That's a clean, real confirmation that the flag is a meaningful predictive signal, not noise — every hypothesis the widened net caught this run also failed independent scrutiny on the merits.

The three hypotheses in Finding 2 would have made it 10 of 10, not 7 of 7, had their flags survived to be checked. The rule that catches them is working; the pipe carrying the flag to that rule has a leak.

**Refutation's lifetime record now stands at 0 of 46 survived.** Every hypothesis ever put through adversarial refutation — original NO_SIGNAL cases and the newly-added ADJACENT_ACTIVE-and-flagged cases alike — has failed. This is either strong evidence the refutation lenses are doing real, discriminating work, or a sign the rubric defaults to REFUTED more often than it should. This report doesn't resolve that question (raised, not answered, in the whitepaper's own Limitations section via the control test) — it just notes that today's data extends the same open question rather than closing it.

---

## Final ledger state

134 entries. Verdicts: ADJACENT_ACTIVE 69, NO_SIGNAL 38, COLLISION 25, FLAGGED 1, FACT_CHECK_FAIL 1. Refutation: 0-of-46 survived.

---

## What this audit recommends, in order

1. **Fix Finding 1** (filename collision → silent data loss) before any further autonomous run. This is the more serious of the two — it's not just a scoring-accuracy problem, it's permanent, silent loss of both the generated content and the ability to ever try that domain again.
2. **Fix Finding 2** (flag erasure) — reorder the checks or make the query-gen patch flag-aware, so the two mechanisms this project just built stop fighting each other.
3. **Do not treat janusian's 33% clean-paradox rate as a bug to chase further.** It's very likely a real property of the mode meeting real domains, not a prompt-engineering gap — the retry-fix-rate data says so directly. The honest move is to let refutation keep doing the job it's now correctly wired to do (once Finding 2 is fixed), not to keep trying to force the generation step to a 100% clean-paradox rate it may not be able to reach.
4. Everything from the previous PRD v2 pass held up under this larger, more realistic load — no regression in the fixes themselves, only in an interaction between two of them neither smaller test batch was large enough to surface.

---

*Exponent Labs LLC · scientific-intuition-engine/umpf_pipeline · Generated 2026-08-29 · Sourced directly from `run_cycle_scheduled.sh`'s real log, `token_usage.jsonl`, `verification-log.jsonl` (134 entries), and direct file inspection of the affected hypotheses. Code freeze held throughout — confirmed via `git status`.*
