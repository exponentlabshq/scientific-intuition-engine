# Eureka Engine v2 — Product Requirements Document

**Status:** proposal — nothing in this document is implemented. Every claim about the current system is sourced from `whitepaper.html` (209-entry ledger, 2026-08-30); every claim about the redesign is sourced from real, disclosed testing done 2026-08-30 in `/tmp` (not yet committed) against `bisociation_gold_pairs.json`.
**Author's framing constraint, stated once so it doesn't need repeating in every section:** every design decision below is judged first against Return on Token Investment, and second — as a hard floor, not a tiebreaker — against whether it could cause a real Master's or PhD researcher to never see a hypothesis worth their time. Where those two conflict, this document says so explicitly rather than picking silently.

---

## Background — what the Eureka Engine is, right now

A four-phase, fully automated hypothesis mill, running unattended end to end on real OpenAI calls. **Phase 1 (generation)** forces two real domains from a combined 170-domain pool through one of three creativity-research-grounded modes — Koestler's *bisociation* (two domains collide, each stays itself, and the model must propose a specific, falsifiable structural mapping — a functor — not a metaphor); Rothenberg's *Janusian thinking* (a domain's foundational assumption held against its exact opposite, both genuinely true at once, not "it depends"); Rothenberg's *homospatial thinking* (two domains fused into one new entity belonging to neither source, mechanically checked for comparison language that would give away a disguised metaphor). **Phase 2 (verification)** checks the resulting claim against real, live web search via a four-way classifier — COLLISION (real prior art already exists), ADJACENT_ACTIVE (fertile, unclaimed ground — the actual target state), NO_SIGNAL, FACT_CHECK_FAIL — governed by an empirically-discovered "umbrella-trap" rule: a bridging connection only counts as real evidence if it's specific enough that it wouldn't return the same hit for most other domain pairs in the pool. **Phase 2.5 (adversarial refutation)** puts every hypothesis that lands NO_SIGNAL, or that failed its own mechanical honesty check, through three independent, blind reviewers — each sees only their one lens (Coherence / Testability / Triviality), never the other two's reasoning, and defaults to REFUTED under genuine uncertainty. The real record: **0 of 79 hypotheses have ever survived**, including two deliberate control tests that pointed the same scrutiny at the pool's own strongest hypothesis and at a second hypothesis chosen specifically to avoid the first control's exact weakness. **Phase 3 (outreach)** drafts, but never sends, a short email to a real, named researcher for anything that clears all of the above — sending is always a deliberate human act.

209 real hypotheses carry a canonical verdict in the ledger today. Total real spend to date: $3.02, across 719 OpenAI calls. Fourteen real production failures have been found and fixed along the way, published in full in `whitepaper.html` rather than smoothed over — filename collisions that silently destroyed a hypothesis with no error anywhere, a search-API outage that let a classifier report a verdict from zero evidence, a ledger-dedup bug that silently dropped two hypotheses behind real, sent outreach off the public leaderboard. The whole thing runs as one command (`run_cycle.py --total N`), fails closed rather than fails quiet, and every dollar figure in its own reporting has been checked, corrected, and disclosed when it was wrong (Section 9's own cost numbers were themselves found to be blending two real model eras, overstating verification and understating refutation, until asked directly whether a 10x cost cut was possible).

## What this PRD proposes to add

Not a rewrite. Everything above stays exactly as it is (Section 1). What's new: a cheap classification step *before* generation that labels a candidate domain pair narrative-shaped or formalism-shaped, and routes it accordingly (Section 2) — narrative-shaped pairs (invention history, economics, psychology) go through a new pre-filter, built and tested today against all 80 pairs in the project's own historical gold-standard reference set, that tries to build a small chain of independently-verified structural correspondences before a real generation call gets spent; formalism-shaped pairs — where that same pre-filter is measured, on the same 80-pair test, to fail more than half the time, including on Shannon entropy/thermodynamic entropy and Hopfield networks/the Ising model, two of the most exact isomorphisms in the whole set — skip the pre-filter entirely and go straight to the verification machinery already proven to catch exact connections via real search. The pre-filter can only ever reorder the generation queue, never delete a candidate (Section 3), and only earns the power to reorder anything once it's shown, against the pipeline's own real outcomes and not just the historical reference set, to actually predict something (Section 5). Separately, writing this PRD surfaced a real, live gap in the existing scorer — the public leaderboard never checks the flag the mechanical honesty checks already write to a hypothesis file — fixed as its own item (Section 2.4), independent of everything else here.

---

## 0. Executive summary

The current pipeline (whitepaper Sections 4–11) treats every candidate domain pair identically: generate, verify against real web search, refute if it lands NO_SIGNAL, draft outreach if it survives. That funnel is proven — 209 real ledger entries, a fail-closed autonomous runner, a 0-of-79 refutation record that has survived two independent control tests designed specifically to break it. None of that is being replaced.

What today's work found is a real, evidenced gap upstream of that funnel: **the funnel has no pair-type awareness, and the one new tool tested today (a composability pre-filter, built to catch equivocation and shallow analogies before spending a generation call) turns out to work well on some kinds of pairs and badly on others — not randomly, but along a clean, measured line.** Run against all 80 pairs in the project's own gold-standard reference set:

| Pair category | n | zero-signal rate |
|---|---|---|
| Engineering / invention history (Tesla, Ford, Gutenberg, Wright brothers...) | 14 | **0%** |
| Economics / social science (Kahneman-Tversky, Black-Scholes, Pareto...) | 16 | 19% |
| Biology / evolution-adjacent | 24 | 38% |
| Pure physics / astronomy / chemistry | 15 | 53% |
| Exact-shared-equation pairs (Shannon entropy↔thermodynamic entropy, Hopfield↔Ising model) | 9 | **56%** |

The tool misses more than half the time on precisely the connections a physics or CS-theory researcher would find most interesting — including two of the most rigorously exact isomorphisms in the whole reference set. It never once misses on a real, narrative-shaped invention-history connection. That is not a reason to discard the tool; it's a reason to **route** it — use it where it's shown to work, and don't let it gate anything where it isn't. That routing principle is the spine of this PRD: different pairs benefit from a range of inquiries, and the pipeline should know which inquiry to run before spending a real generation call.

**This is not a cost-reduction proposal, and the numbers say so plainly.** Computed directly from today's real logged spend: the pre-filter costs $0.0084 per run, against $0.0024 for the entire existing funnel per candidate (generation + verification + refutation-when-triggered). Under the non-negotiable floor in Section 3 — the pre-filter may only reorder the generation queue, never delete a candidate from it — a deprioritized candidate still eventually pays the full existing funnel cost when its turn comes, so that $0.0084 is pure addition, not a substitute. A narrative-shaped candidate's real lifetime cost under this redesign rises to roughly **$0.0111 — about 4.6x today's per-candidate cost** (Section 4.5). The entire ROTI case therefore rests on one unproven bet: that reordering a necessarily-bounded operating budget toward higher-expected-value candidates first yields more real discoveries per total dollar spent than today's unweighted selection already does. That correlation has never been measured (Section 5). If it doesn't hold, this redesign is a straightforward regression — more spend, no better allocation — and this document says that outright rather than leaving it implied by a table three sections in.

---

## 1. What stays exactly as it is — proven, load-bearing, not in scope

Named explicitly so nothing below is misread as touching these:

1. **The three generation mechanisms** (bisociation, Janusian, homospatial) and their mechanical enforcement (Failure 1's same-instance check, Failure 2's comparison-word scan) — real, tested at scale, imperfect in a *characterized* way (Janusian's 20% retry-fix rate is a documented property of the mode, not an open bug).
2. **The four-way verification classifier** and the umbrella-trap rule — the single check that turns "did search find something" from a misleading binary into the actual signal the pipeline needs.
3. **Adversarial refutation, three independent lenses, defaulting to REFUTED under uncertainty** — 0 of 79 real hypotheses have ever survived, including the top-ranked hypothesis in the entire pool when pointed at itself as a control, and a second hypothesis chosen specifically to avoid that control's exact weakness. This is the sentence the whitepaper's own conclusion says is "the most important... to sit with honestly." Nothing in this redesign weakens it, adds a shortcut around it, or trades its rigor for cost.
4. **Draft-only outreach with mandatory human sign-off.** Not adjustable by this document, not adjustable by any future one without a separate, explicit decision.
5. **Fail-closed autonomy** (`run_cycle.py`, the DEGRADED-cycle behavior, retry/backoff, the circuit breaker) and **the ledger's single-source-of-truth discipline** (`ledger.py`'s `load_latest_entries()`, `check_ledger_consumers.py` wired into `publish_site.py` as a hard gate). Every new component this PRD proposes must be a *consumer* of that discipline, never a second raw reader of `verification-log.jsonl` — that exact mistake already happened three times (Failures 11, 13, and the recurrence Failure 13 itself was).
6. **Model tiering that's already validated** — refutation and verification both run on gpt-4o-mini after real, disclosed 7-case/21-lens and 3-case testing. Nothing here revisits that.

---

## 2. What's new: pair-type-aware routing

### 2.1 Phase 0 — Pair-Type Classifier (new)

Before any generation call, one cheap gpt-4o-mini classification pass (~200–400 tokens, a fraction of a cent) labels the candidate domain pair along the axis today's testing actually validated:

- **Narrative-shaped** — the connection, if real, would be a technique, trait, or mechanism that generalizes across prose-describable contexts (an invention transplanted between industries; a psychological trait; a market mechanism). This is where engineering-history and economics/social-science pairs live.
- **Formalism-shaped** — the connection, if real, would be a literal shared equation, derivation, or exact physical law. This is where the exact-shared-equation and much of the pure-physics category live.
- **Mixed / uncertain** — doesn't cleanly resolve to either; treated as narrative-shaped for pre-filter purposes but flagged with lower confidence in every downstream record.

This classifier is new, cheap, and **itself needs the same validation discipline as everything else in this document** — Phase 0 ships in observe-only mode (Section 5) before anything downstream trusts its label.

### 2.2 Phase 0.5 — Composability Pre-Filter, narrative-shaped pairs only

The mechanism validated today: a two-agent dialectic (Expert A/Expert B, real conversation memory, an honest `can_extend: false` escape hatch) generates a candidate chain of corresponding pairs, each hop independently and blindly verified (never by the model that proposed it), scored by two metrics discovered today to matter more than the metric first shipped with:

- **`longest_run`** — the longest consecutive run of independently-verified hops found *anywhere* in the chain, not required to start at hop 1.
- **`pass_rate`** — fraction of all generated hops that independently verified.

*(The original metric, `unbroken_depth_from_start`, is kept for continuity but demoted — it was shown today to discard real signal: one real run on a gold pair had 6 of 10 hops independently verify True yet scored a flat 0 under the old rule, purely because the first two hops happened to fail. `chain_composition.py` and `chain_dialectic.py` already carry this fix.)*

Two more real, evidenced findings from today's work shape how this pre-filter must be built, not just that it exists:

- **Seed minimally, not exhaustively.** Every pair tested today where the seed domain description was hand-enriched with careful literature detail scored *worse* than the same pair seeded only from plain, terse reference-file fields (DNA: 0 → 2; Kahneman-Tversky: 3 → 4; Metropolis/annealing: 1 → 2; backprop/calculus: 0 → 1). Over-specifying the seed anchors the dialectic on restating the seed's own examples rather than genuinely extending them — the same failure shape as the invariant-altitude bug found and fixed earlier the same day. **Implementation requirement: seed strings are built programmatically from short, structured fields (a name, a one-line collision description, a one-line insight) — never from hand-curated prose.**
- **The invariant must be forced to the mechanism, not the example.** The schema field that asks for "the invariant" must also require a second, independently-nameable phenomenon the same invariant would predict — the single fix that took this pipeline from zero real verified hops (across 11 real runs on a speculative hypothesis) to real, repeatable signal on a historically-true one.

**Routing rule:** formalism-shaped pairs skip Phase 0.5 entirely and go straight to Phase 1. Running this pre-filter on them is not merely unhelpful — it's actively risky, since a LOW_PRIORITY read on a real connection like Shannon entropy ↔ thermodynamic entropy would deprioritize exactly the kind of rigorous, high-value connection the whole project exists to surface. Do not spend tokens producing a signal you already know, from real n=80 testing, is worse than a coin flip in that category.

### 2.3 Formalism-shaped pairs — a different inquiry, not no inquiry

"Skip the pre-filter" is not "skip scrutiny." The existing Phase 2 verification classifier — real web search, already proven on exactly this kind of claim (it's how the pipeline already catches genuine COLLISIONs) — is the correctly-suited check for formalism-shaped pairs; it just needs to run earlier in the sequence for this category, without waiting on a pre-filter signal that's known not to apply. A more targeted verification-prompt variant for this category (explicitly searching for "is [claimed shared structure] a documented isomorphism," rather than the generic four-way prompt) is a real, promising idea surfaced by today's testing — **named here as a Phase-2-only future refinement, deliberately not part of this redesign's first build**, since it hasn't been tested and this document's own discipline (Section 6) requires that before anything gates real spend.

---

## 2.4 A real gap in the *existing* pipeline, found while writing this PRD — not from today's testing

Re-reading `score_hypotheses.py` against the whitepaper's own Failure 4 (the mechanical same-instance / comparison-word checks) surfaced a live scoring gap, independent of everything else in this document: `hypothesis_flagged()` — which correctly detects the literal "Automated check failed twice" honesty banner those mechanical checks write — is **only ever consulted inside `outreach_shortlist()`**, a separate function used solely by `score_hypotheses.py --outreach`. `score_entry()`, the function that actually produces the public leaderboard points and badges, never calls it, and `render_leaderboard()` never surfaces it as a badge either.

This is partially self-correcting by accident, not by design: a flagged hypothesis that lands ADJACENT_ACTIVE is swept into refutation regardless (per the whitepaper's own text) and refutation has caught every one of them so far, so the −15 REFUTED penalty ends up applied — but *because a different check happened to catch it on the merits*, not because the public score reflects the mechanical flag itself. A flagged hypothesis that lands **COLLISION** instead never enters that sweep at all — refutation only fires on NO_SIGNAL and flagged-ADJACENT_ACTIVE cases — so it scores the plain +5/−5 COLLISION points with zero trace anywhere on the public leaderboard that it was independently caught disguising a compromise.

**Fix, in scope for v2 regardless of the pair-type routing work:** `score_entry()` gets a direct check against `hypothesis_flagged()` — a real, visible penalty and badge (e.g. a `⚠️ Failed Honesty Check` chip, distinct from `💀 Refuted`) applied at scoring time for *every* verdict path, not only the ones that happen to route through refutation first. This is the same class of fix as Failure 13's own lesson, applied to the scorer instead of the ledger reader: a real check's signal has to be verified as actually reaching every consumer that reports on it, not assumed to propagate because one path happens to catch it downstream.

---

## 3. The floor: never let a pre-filter cost a researcher a real discovery

This is the non-negotiable constraint the executive summary named. Concretely, in code terms:

- Phase 0.5's output is a **priority signal, never a delete.** A LOW_PRIORITY pair still enters the generation queue — it just runs later, or requires one operator confirmation to run sooner, exactly the same shape as the existing audit agent's "propose, never auto-adopt" discipline (Section 10 of the whitepaper). It is never silently dropped from `domains.json`'s explored-pair tracking the way Failure 6's filename collision silently was.
- Every LOW_PRIORITY verdict is logged with its own pre-filter reasoning, visible on the leaderboard as a disclosed, uncalibrated badge — same pattern as `chain_composition.py`'s existing `"calibration_status": "UNCALIBRATED — directional signal only"` field. A human glancing at the queue can always see and override it.
- The domain pool is 1.45% explored (209 of ~14,365 possible pairs, per the whitepaper's own Limitations section). At current cost (~$0.0007/generation call on gpt-4o-mini), *exhausting the entire pool once* costs on the order of $10, not $10,000 — the real constraint this whole system has never been dollars. A pre-filter that saves pennies by skipping a pair a real researcher would have wanted to see is a bad trade even under a pure ROTI reading, because token cost was never the binding constraint to begin with. This is stated explicitly so a future cost-cutting pass doesn't quietly forget it.

---

## 4. Sample-size discipline — stakes-scaled, not uniform

Today's investigation surfaced this directly: LLM output is probabilistic, and a single dialectic run on the same pair can land anywhere from `longest_run: 0` to `longest_run: 8` (real range observed across the 80-pair test). The redesign's sampling policy, scaled to what each stage actually gates:

| Stage | Real stake if wrong | Sample size |
|---|---|---|
| Phase 0 (pair-type classification) | Misroutes to the wrong pre-filter mode | n=1, cheap, corrected downstream by Phase 2 regardless |
| Phase 0.5 (composability pre-filter) | Reorders the generation queue only (Section 3's floor) | n=1 during observe-only rollout; **n=3, median-of-3 `longest_run`, once gating is enabled** (Section 5) — gating on a queue-reordering decision from a single stochastic draw is not acceptable once that draw actually changes when a real researcher would see a hypothesis |
| Phase 1 (generation) | Produces the actual candidate | n=1, unchanged — this was never the unreliable step |
| Phase 2 (verification) | Determines COLLISION/ADJACENT/NO_SIGNAL | n=1 real search call, unchanged — grounded in real external evidence, not model improvisation, so single-sample stochasticity is a smaller real risk here |
| Phase 2.5 (refutation) | Can kill a real candidate for good | **n=3 independent lenses, unchanged** — already the correctly-calibrated stake-appropriate sample size in the current system; this document does not touch it |
| Phase 3 (outreach) | Costs a real researcher's time and goodwill | Human judgment, unchanged |

The general principle, stated once: **sample size should track what a wrong answer actually costs, not be uniform for engineering convenience.** The current pipeline already gets this right at the refutation layer (3 independent lenses because a wrongly-promoted hollow hypothesis costs someone real time later). This redesign extends the same logic one layer upstream, calibrated to what Phase 0.5 actually risks — nothing, until it's allowed to gate; real queue-ordering harm, once it is.

---

## 4.5 The real ROTI model — this redesign costs more per candidate, not less

Computed directly from `token_usage.jsonl`'s real logged calls (OpenAI's published gpt-4o-mini/gpt-4o per-token pricing applied to real prompt/completion counts, not estimated), stated plainly rather than left as a qualitative claim:

| | Cost |
|---|---|
| Existing funnel, per candidate (generation + verification + refutation-when-triggered at its real 37.8% rate) | **$0.0024** |
| Phase 0.5 composability pre-filter, per run (real, measured across 92 real v4 runs today) | **$0.0084** |
| Phase 0 classifier, per candidate (estimated, comparable to today's cheapest real classification calls) | **$0.0003** |
| **Narrative-shaped candidate, total lifetime cost under this redesign** (Phase 0 + Phase 0.5 + the existing funnel it still eventually pays, per Section 3's floor) | **≈ $0.0111 — roughly 4.6x today's cost** |
| Formalism-shaped candidate, total cost (Phase 0 only, existing funnel unchanged) | ≈ $0.0027 — ~12% overhead |

**This is the honest headline: under the "reorder, never delete" floor this document commits to in Section 3, the pre-filter cannot reduce total token spend for any candidate that eventually gets run — it can only add to it.** A deprioritized candidate still pays the full existing funnel cost when its turn comes; nothing is skipped, only delayed. The only mechanism by which this redesign improves real ROTI is **allocation quality inside a bounded operating budget** — the domain pool is 1.45% explored after everything run to date, any real batch is a small slice of ~14,365 possible pairs, and a candidate pushed far enough back in a reordered queue is, in practical terms, unlikely to be reached soon even though it is never formally deleted. If Phase 0.5's signal correlates with real downstream outcomes (COLLISION/NO_SIGNAL/REFUTED vs. ADJACENT_ACTIVE-that-holds) better than unweighted selection already does, the same total spend produces more real, valuable hypotheses per dollar. **That correlation has not been measured** — which is exactly why Section 5's Phase A/B gating exists, and it needs to be read with this cost table in hand: if the correlation turns out weak or absent, this redesign is a straightforward ROTI regression, not a neutral experiment, because every narrative-shaped candidate now costs 4.6x more to reach the same eventual funnel outcome.

The one piece of this document with an already-evidenced, non-speculative ROTI case is Section 7's schema-migration recommendation: Failure 12 is a real, recorded production instance of malformed-JSON retries burning real repeated calls (two of forty hypotheses in one batch failed verification twice before the fix shipped); strict schema enforcement removes that waste rather than adding new spend. Section 2.4's scorer fix costs nothing in tokens at all — a scoring-integrity fix, not a ROTI lever.

---

## 5. Rollout — staged, evidence-gated, matching the audit agent's own discipline

**Phase A — Build + observe-only (target: next ~100 real cycles).** Phase 0 and Phase 0.5 run on every new candidate pair, log their signal (pair-type label, `longest_run`, `pass_rate`, recommendation) to a new ledger-adjacent file, and change *nothing* about generation order, priority, or scoring. This is pure data collection against real downstream outcomes.

**Phase B — Correlation check.** Before Phase 0.5 is trusted to reorder anything, directly measure: does a LOW_PRIORITY signal on a real candidate actually predict a worse real downstream verdict (COLLISION/NO_SIGNAL/REFUTED) at a rate meaningfully better than the pool's base rate? This has never been measured — every test run today validated the pre-filter's *internal* metric against known gold-standard history, not against this pipeline's own real, live verdicts. That is a real, disclosed gap this document does not paper over. If the correlation doesn't hold, Phase 0.5 stays observe-only indefinitely; a pre-filter that predicts nothing real is not shipped as a gate no matter how clean its own internal numbers look — the same discipline that killed the outreach-sharpening concreteness gate (whitepaper, Section 13) after real calibration testing failed it twice.

**Phase C — Gated, with an override.** Only if Phase B shows real, measured correlation: Phase 0.5's signal reorders (never deletes) the generation queue, using n=3 sampling per Section 4, with the badge and override path from Section 3 active from day one, not added later.

---

## 6. What this explicitly does not change or resolve

- **Nothing schedules the engine yet** — the whitepaper's own deliberate, standing decision (Limitations, "Deliberately not attempted") is unaffected by anything here and stays held until refutation calibration's open question (a hand-constructed hypothesis with zero shared vocabulary, engineered to test whether anything can survive refutation) is actually attempted.
- **Refutation calibration itself is not addressed here.** It's a real, still-open question this redesign inherits unchanged, not one this document claims to resolve.
- **Lens-weighting by pair type** (the idea that Triviality might be the higher-value lens for narrative pairs and Coherence for formalism pairs, since today's testing found different failure *shapes* in each) is a real, plausible extension surfaced by today's work — and explicitly **not** part of this build. It has not been tested. Naming it here and declining to include it is the same discipline Section 2.3 applies to the Phase-2-prompt-variant idea: promising is not the same as validated.
- **The domain-pool exhaustion question** is unchanged — still 1.45% explored, still a standing resource, not a gap this redesign claims to close.

---

## 7. Data contracts — what actually gets sent to and received from OpenAI

Pulled directly from the real production code (`hypothesis_engine.py`, `verify_hypothesis.py`, `refute_hypothesis.py`) and the two new modules built and tested today (`chain_composition.py`, `chain_dialectic.py`), not reconstructed from memory. The shape of this data is the single biggest architectural finding of this section: **the three existing production call types each handle structured output differently, and none of them use OpenAI's strict schema enforcement** — which is exactly the gap that made Failure 12 (a truncated, malformed JSON response silently dropping a required field) possible in the first place, and exactly what the two new modules avoid by construction.

### 8.1 Phase 1 — Generation (existing, unstructured)

```python
client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "<mode prompt (bisociation/janusian/homospatial) + 3 few-shot examples>"},
        {"role": "user", "content": "DOMAIN A: <domain_a>\n\nDOMAIN B: <domain_b>"},  # janusian: "DOMAIN: <domain_a>" only
    ],
    temperature=0.4,
)
```

**Response: `resp.choices[0].message.content` — raw markdown, not JSON.** The actual hypothesis file (`## 1. The Two Frames`, `## 3. The Candidate Functor`, `## 5. Novelty & Testability Self-Critique`, etc.) *is* the response, parsed downstream by regex — `_extract_section()`, `_find_comparison_words()`, `extract_self_score()`. This is the data shape Failure 5 exploited without anyone intending it: the self-report regex captured the wrong digit from `"Distance score (1-5): 4"` for two-thirds of all hypotheses, silently, for the script's entire lifetime, because there was never a real field to read — only a string pattern to guess at.

### 8.2 Phase 2 — Verification (existing, prose-instructed JSON, not schema-enforced)

```python
client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    instructions="<rubric + a JSON shape spelled out in English inside the prompt text>",
    input="Hypothesis: <title>\nMode: <mode>\nDomain(s): <domains>\n\nCore claim:\n<core_claim>\n\nSuggested search starting points:\n<queries>",
    max_output_tokens=4000,
)
```

**Response** (`resp.output_text`, fence-stripped, then `json.loads()` inside a 3-attempt retry loop):
```json
{
  "verdict": "COLLISION | ADJACENT_ACTIVE | FACT_CHECK_FAIL | NO_SIGNAL",
  "what_was_found": "3-4 sentences, real titles/URLs only",
  "reasoning": "..."
}
```
This is the exact shape that failed in production (Failure 12): a longer, search-augmented response hit an implicit output-token ceiling and the string cut off mid-word — `"...specifically named \"Crea` — before `reasoning` was ever written. The fix shipped (an explicit `max_output_tokens`, a shorter `what_was_found` instruction, three attempts instead of two) mitigates the risk; it does not structurally prevent it, because nothing in the request *enforces* the shape — the model is just following English instructions that describe one.

### 8.3 Phase 2.5 — Refutation (existing, loose `json_object` mode — one call per lens, three total)

```python
client.chat.completions.create(
    model=REFUTATION_MODEL,  # gpt-4o-mini since 2026-08-30, gpt-4o before
    messages=[
        {"role": "system", "content": "<lens-specific instructions (Coherence/Testability/Triviality) + full rubric + JSON shape spelled out>"},
        {"role": "user", "content": "Hypothesis: <title>\nMode: <mode>\nDomain(s): <domains>\n\nCore claim:\n<core_claim>\n\nPhase 2 web-verification finding (for context):\n<verification_note>"},
    ],
    temperature=0.1,
    response_format={"type": "json_object"},
)
```

**Response:**
```json
{"verdict": "REFUTED | SURVIVES", "reasoning": "2-4 sentences, terse peer-reviewer style"}
```
`response_format={"type": "json_object"}` guarantees syntactically valid JSON — it does not guarantee these specific two keys exist, or that `verdict` is one of exactly two values. That's still enforced only by the prompt's own English instructions, the same class of risk Phase 2 has, just not yet observed to fail the same way in the record to date.

### 8.4 New, tested today — composability pre-filter generation (`chain_composition.py`), strict schema

```python
client.responses.create(
    model="gpt-4o-mini",
    instructions="<requires a named relation-type per domain, one invariant, honest hops>",
    input="DOMAIN A: <domain_a>\nDOMAIN B: <domain_b>",
    text={"format": {"type": "json_schema", "name": "chain", "schema": CHAIN_SCHEMA, "strict": True}},
    max_output_tokens=1200,
)
```

`CHAIN_SCHEMA` (real, current):
```json
{
  "type": "object",
  "properties": {
    "relation_a": {"type": "string"},
    "relation_b": {"type": "string"},
    "invariant": {"type": "string"},
    "hops": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "x": {"type": "string"}, "y": {"type": "string"},
          "a": {"type": "string"}, "b": {"type": "string"},
          "relation_instance": {"type": "string"}
        },
        "required": ["x", "y", "a", "b", "relation_instance"],
        "additionalProperties": false
      }
    },
    "honest_stopping_reason": {"type": "string"}
  },
  "required": ["relation_a", "relation_b", "invariant", "hops", "honest_stopping_reason"],
  "additionalProperties": false
}
```
`strict: true` means the API itself enforces this shape at generation time — no fence-stripping, no malformed-JSON retry loop, no truncation risk of the kind that produced Failure 12. Zero schema-shape failures were observed across roughly 2,500 real calls made testing this and the dialectic variant today.

### 8.5 New, tested today — two-agent dialectic moves (`chain_dialectic.py`, v4), strict schema

```python
client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": a_instructions}] + history + [
        {"role": "user", "content": "Round <r>. Propose your next (x,y) pair and relation, extending the thread so far."}
    ],
    temperature=0.4,
    response_format={"type": "json_schema", "json_schema": {"name": "expert_a_move_v4", "schema": A_MOVE_SCHEMA_V4, "strict": True}},
)
```

`A_MOVE_SCHEMA_V4` — the version fixed today, after the "invariant collapses to a verbatim restatement of the seed example" bug was found:
```json
{
  "type": "object",
  "properties": {
    "x": {"type": "string"}, "y": {"type": "string"},
    "relation": {"type": "string"},
    "invariant_so_far": {"type": "string"},
    "second_phenomenon_this_invariant_also_covers": {"type": "string"}
  },
  "required": ["x", "y", "relation", "invariant_so_far", "second_phenomenon_this_invariant_also_covers"],
  "additionalProperties": false
}
```
`B_MOVE_SCHEMA` (Expert B's reply — same call shape, different schema, including the honest early-stop escape hatch):
```json
{
  "type": "object",
  "properties": {
    "can_extend": {"type": "boolean"},
    "a": {"type": "string"}, "b": {"type": "string"},
    "relation": {"type": "string"},
    "honest_note": {"type": "string"}
  },
  "required": ["can_extend", "a", "b", "relation", "honest_note"],
  "additionalProperties": false
}
```
`second_phenomenon_this_invariant_also_covers` is the one field responsible for turning zero real verified hops (11 real runs on a speculative hypothesis, every schema variant before this one) into real, repeatable signal on a historically-true pair — forcing the model to name a *second*, different real phenomenon its own stated invariant would also predict is what keeps the invariant from collapsing back down to "the one example I was just given."

### 8.6 New, proposed but not yet built — Phase 0 pair-type classifier

Designed here, strict-schema from the start, consistent with 8.4/8.5 rather than 8.1–8.3:

```python
client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "<classify whether a real connection between these two domains, if one exists, would be narrative-shaped (a technique/trait/mechanism that generalizes across prose-describable contexts) or formalism-shaped (a literal shared equation, derivation, or exact physical law)>"},
        {"role": "user", "content": "DOMAIN A: <domain_a>\nDOMAIN B: <domain_b>"},
    ],
    temperature=0.2,
    response_format={"type": "json_schema", "json_schema": {"name": "pair_type", "schema": PAIR_TYPE_SCHEMA, "strict": True}},
)
```

`PAIR_TYPE_SCHEMA` (proposed):
```json
{
  "type": "object",
  "properties": {
    "pair_type": {"type": "string", "enum": ["narrative-shaped", "formalism-shaped", "mixed-uncertain"]},
    "reasoning": {"type": "string"},
    "confidence": {"type": "integer", "description": "1 (low) to 5 (high)"}
  },
  "required": ["pair_type", "reasoning", "confidence"],
  "additionalProperties": false
}
```

### 8.7 The concrete recommendation this section produces

Migrate Phase 1, Phase 2, and Phase 2.5 (8.1–8.3) to strict `json_schema` responses, matching 8.4–8.6. For Phase 1 specifically, this replaces regex section-extraction with real structured fields — directly closing the exact class of bug Failure 5 was (a script silently reading the wrong thing because there was never a real field, only a string pattern to guess at) rather than patching that one instance. For Phase 2, this structurally prevents Failure 12's truncation failure rather than mitigating it with a bigger token ceiling and more retries. This is a real, disclosed, non-trivial engineering cost — three production call sites and their prompts need real rework, not a config flag — and is named here as a concrete follow-on item, not folded into Section 2's pair-type routing work, since it's an orthogonal fix that would improve the pipeline even if the pair-type routing work were never built at all.

---

## 8. One-paragraph summary for anyone who reads only this section

The current pipeline is proven and stays as-is. What's new is an evidence-gated routing layer — not a cheap one, at $0.0084 per pre-filter run against $0.0024 for the entire existing funnel per candidate — that sends narrative-shaped domain pairs (where the pre-filter works — 0% failure across 14 real invention-history gold pairs) through it, and sends formalism-shaped pairs (where the same tool fails more than half the time, including on exact, rigorously documented equations like Shannon entropy) straight past it to the verification machinery already suited to catching them. It launches observe-only, is promoted to actually reordering the generation queue only once it's shown, on real pipeline outcomes and not just gold-standard history, to predict something real — and even once gated, it can only ever reorder a candidate, never delete one, both because the one thing this whole system exists to avoid is a real researcher never getting to see a hypothesis worth their time, and because that reorder-not-delete floor is the entire reason this redesign's real cost is higher, not lower, than today's — a bet on better allocation of a larger total spend, not a savings proposal, and not yet a proven bet.
