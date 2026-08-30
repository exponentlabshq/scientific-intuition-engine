# Eureka Engine — 10X Courses of Action (research mission)

**Living tracker.** Companion to `eureka-engine-system-prd.md` and `eureka-engine-10k-readiness-audit.md`. Same shape as vault `Ops/COA Tracker.md`.

**Date opened:** 2026-08-29 (rewritten — research mission only; deal-graph paths removed)  
**Mission:** recover Masters/PhD time by proposing a falsifiable cross-domain hypothesis, then classifying COLLISION / ADJACENT_ACTIVE / not a real lead.  
**Doctrine:**
- Bisociation — [`bisociation-domain-pairs.md`](../bisociation-domain-pairs.md): transplant a **generative relation**
- Janusian — [`janusian-thinking.md`](../janusian-thinking.md): hold two contradictory poles **simultaneously** for the same instance
- Homospatial — [`homospatial-thinking.md`](../homospatial-thinking.md): force discrete entities into the **same space** until a new identity emerges

**Out of scope:** Sayve, MythosHealth, Katalyst, Zorro, vault `/eureka` deal briefs, Exponent deal Domain A.

**Not a 10X path:** blind `run_cycle --total N`.

---

## Scoreboard

| COA | Status | Next move | Last updated |
|---|---|---|---|
| 1 Phase 3 mission loop | **Clock running — 3 sends 2026-08-29** | Await Aronson / Frey / Phillips replies (~21d → 2026-09-19); optional El-Gohary / Schooler after concrete rewrite | 2026-08-29 |
| 2 Generative-relation (bisociation) | Implemented | Blind A/B 20+20 when ready | 2026-08-29 |
| 2b Janusian simultaneous-hold | Implemented — measured | Fresh n=3: **0/3** clean after retry (all flagged). Filter holds; generator still weak on arbitrary domains | 2026-08-29 |
| 2c Homospatial fusion | Implemented — measured | Fresh n=3: **2/3** clean fusion first-pass (1 flagged). Gold 80 + few-shots + fusion-form check shipped | 2026-08-29 |
| 2d Sharpen → re-verify (pre-packet) | **Ritual live — kill sample 1 COLLISION / 2 ADJACENT** | Soft-trap (Game Theory×Music→DiCola) + 2 hard-still-ADJACENT packets. Keep ritual; kill bar not tripped. Send only sharpened | 2026-08-29 |
| 3 Thesis-in | `--challenge` shipped | Run ≥3 real thesis challenges | 2026-08-29 |
| 4 Prior-art canaries (bisociation) | 10 canaries + runner | Live verify; ≥80% COLLISION | 2026-08-29 |
| 4b Janusian COLLISION canaries | **PASS 6/6 (recall 1.0)** | Monid fallback after Tavily 432; gate cleared for janusian prior-art honesty | 2026-08-29 |
| 4c Homospatial COLLISION canaries | **PASS judged 3/3 (recall 1.0)**; 3 PENDING search | Re-verify Hopfield/Toyota/Gutenberg when Tavily/Monid recover | 2026-08-29 |
| 5 Ranking + verify enablers | Rank + control + parallel/cache; cron off | Stability A/B before cron | 2026-08-29 |

**Shared program kill:** if COA 1 fails *and* COA 3 fails → engine is a teaching/calibration artifact (Rosetta/UMPF), not a PhD-time product.

---

## COA 1 — Phase 3: close the mission loop (Schwerpunkt)

**Bet:** ADJACENT_ACTIVE inventory exists. Product unproven until a researcher says novel / known / dismiss.

**Schwerpunkt:** 5–10 one-pagers from Frontier Research Group → authors from verifications → `outreach/` → human send → ledger `outreach_status`.

| Metric | Target | Current |
|---|---|---|
| Phase 3 outcomes | ≥1 confirmed novel or ≥2 confirmed known in 21 days | **3 sent** (Aronson, Frey, Phillips) 2026-08-29; clock → ~2026-09-19 |

**Kill:** 0 substantive replies on 8 sends in 21 days → freeze volume; internal calibration only.

**Owners:** Rocky (send) · Michael (packet quality)

**Artifacts:** `outreach/packets/` · `outreach/shortlist.json`

---

## COA 2 — Generative-relation generation

**Bet:** Better relation transplants, not more random pairs. Wire the 80-table into runtime.

**Schwerpunkt:** gold JSON · §4 generative-relation form · analogy reject · distance-biased pairs · few-shots · A/B.

| Metric | Target | Current |
|---|---|---|
| “Worth a week” lift | ≥1.5× on blind 20+20 | Code shipped; A/B pending |

**Kill:** No lift → revert picker/few-shot; keep §4 form if it alone helps.

**Artifacts:** `bisociation_gold_pairs.json` · `prompts/umpf_hypothesis_prompt.md` · `hypothesis_engine.py`

---

## COA 2b — Janusian simultaneous-hold (parity with COA 2)

**Bet:** Most janusian ADJACENT_ACTIVE → REFUTED failures are context-split compromises. Wire [`janusian-thinking.md`](../janusian-thinking.md) the way bisociation wired its 80-table.

**Schwerpunkt:** `janusian_gold_pairs.json` · few-shots · §5 simultaneous-hold form · stronger same-instance mechanical check (context-split + hold signature).

| Metric | Target | Current |
|---|---|---|
| Same-instance clean rate | Lift vs ~20% historical retry-fix | Gold + prompt + checks shipped |

**Kill:** No lift in clean same-instance rate after fresh batch → keep deprioritize-flagged for outreach; do not scale janusian volume.

**Artifacts:** `janusian_gold_pairs.json` · `prompts/umpf_janusian_prompt.md` · `hypothesis_engine.py` (janusian few-shot + hold check)

---

## COA 3 — Thesis-in (researcher-conditioned generation)

**Bet:** Mission UX = researcher supplies home domain / thesis question as Domain A; engine samples distant B; returns classified lead.

**Schwerpunkt:** `--challenge` (or fixed `--domain-a` + autonomous B). Research brief output — not Ops deal notes. No `--deal`.

| Metric | Target | Current |
|---|---|---|
| Real thesis runs | ≥3 in 4 weeks; ≥1 “clarified direction” | CLI shipped |

**Kill:** Researchers won’t use it → keep autonomous catalog only.

**Artifacts:** `hypothesis_engine.py --challenge`

---

## COA 4 — Prior-art canaries

**Bet:** Missing COLLISION is a mission failure. Known historical pairs must classify COLLISION.

**Schwerpunkt:** Frozen bisociation gold canaries (Darwin×Malthus, Black–Scholes×diffusion, …) · verify recall ≥80%.

| Metric | Target | Current |
|---|---|---|
| Canary COLLISION rate | ≥80% | 10 bisociation canaries + runner; live run pending API |

**Kill:** Canaries stay NO_SIGNAL while literature is obvious → fix verify before more Phase 3.

**Artifacts:** `prior_art_canaries.json` · `run_prior_art_canaries.py`

---

## COA 4b — Janusian prior-art canaries

**Bet:** Documented Janusian leaps (Einstein equivalence, Bohr complementarity, Planck quanta, Dirac antimatter, Heisenberg, Gödel) must classify COLLISION — same honesty bar as bisociation canaries.

**Schwerpunkt:** 6 frozen janusian canaries from `janusian-thinking.md` · `run_prior_art_canaries.py --mode janusian`.

| Metric | Target | Current |
|---|---|---|
| Janusian canary COLLISION rate | ≥80% | 6 stubs shipped; live verify pending |

**Kill:** Obvious named paradoxes stay NO_SIGNAL → query/classifier gap; fix before advising students with janusian leads.

**Artifacts:** `prior_art_canaries.json` (mode=janusian rows) · `hypotheses/canaries/canary-janusian-*.md`

---

## COA 2c — Homospatial fusion (gold parity)

**Bet:** Most “homospatial” ADJACENT_ACTIVE failures are bisociation wearing fusion’s name (comparison language / no chimera). Wire [`homospatial-thinking.md`](../homospatial-thinking.md) the way Janusian wired its 80-table.

**Schwerpunkt:** `homospatial_gold_pairs.json` · few-shots · §4 fusion sentence · mechanical fusion-form check (overlay/chimera signature + comparison-word ban on §2–§3).

| Metric | Target | Current |
|---|---|---|
| Fusion-form clean rate | Lift vs historical comparison-language failures | Fresh n=3: **2/3** clean first-pass; 1 flagged after retry |

**Kill:** No lift after gold + checks → keep flagged homospatial out of outreach; do not scale volume.

**Artifacts:** `homospatial_gold_pairs.json` · `prompts/umpf_homospatial_prompt.md` · `hypothesis_engine.py` (homospatial few-shot + fusion check)

---

## COA 2d — Sharpen → re-verify (pre-packet ritual)

**Bet:** Raw ADJACENT_ACTIVE often encodes a *soft* fusion. One closed-loop sharpen + denser prior-art search splits soft (near-known) from hard (still adjacent) before wasting a researcher's time.

**Evidence (2026-08-29):**

*Lightning ×2 (adopt ritual):*

| Lead | Soft claim | Hard chimera | After re-verify |
|---|---|---|---|
| Resonant Swarm | robots communicate with sound | \(S \leftrightarrow R\) acoustic blackboard | Soft near Aranson/Frey; hard still ADJACENT |
| Magneto-Operant | magnets affect behavior | field manifold *is* the schedule | Soft near Liboff/Thomas; hard still ADJACENT |

*Kill sample (next 3 sharpens — neither kill tripped):*

| Lead | Soft claim | Hard chimera | After re-verify | Packet |
|---|---|---|---|---|
| Game Theory × Music | negotiation ≈ sampling | Nash-Clearance Market | **COLLISION** — DiCola Nash sample-licensing | No (soft-trap) |
| Architecture ⊕ Pattern Recognition | AI helps compliant design | Permit-Pattern Loop | Soft near ACC/Rhonda; hard still ADJACENT | Yes — NOT SENT |
| Janusian Creative Block | struggle / incubation helps | Same-instance Block Paradox | Soft near incubation; hard still ADJACENT | Yes — NOT SENT |

**Result:** 1/3 hard COLLISION · 2/3 hard still ADJACENT. Ritual earns keep: catches soft-traps without sterilizing every lead.

**Schwerpunkt:** Before every Phase 3 send: (1) rewrite §2–§4 as bidirectional closed loop, (2) Exa/search against the hard claim + named neighbors, (3) packet only the hard claim. Gate: `outreach/README.md` + `packets_manifest.json` `sharpened: true`.

**Kill:** If 3/3 next sharpens collapse to COLLISION on the hard claim → raise the bar for what earns ADJACENT from generation; if 0/3 move → ritual is theater, drop it. *(Kill sample: neither.)*

**Artifacts:** `sharpen_hypothesis.py` · Swarm + Magneto + Architecture + Creative Block packets · Game Theory soft-trap verification · this COA row

---

## COA 4c — Homospatial prior-art canaries

**Bet:** Documented Homospatial leaps (desktop GUI, DNA double helix, McCulloch–Pitts, Hopfield, Toyota kanban, Gutenberg press) must classify COLLISION — same honesty bar as Janusian canaries.

**Schwerpunkt:** 6 frozen homospatial canaries from `homospatial-thinking.md` · `run_prior_art_canaries.py --mode homospatial`.

| Metric | Target | Current |
|---|---|---|
| Homospatial canary COLLISION rate | ≥80% | **PASS** judged recall **1.0** (3/3: desktop, DNA, McCulloch–Pitts). Hopfield / Toyota / Gutenberg remain PENDING_VERIFICATION after Monid empty — infra, not classifier |

**Kill:** Obvious named fusions stay NO_SIGNAL when search returns evidence → query/classifier gap; fix before advising students with homospatial leads.

**Artifacts:** `prior_art_canaries.json` (mode=homospatial rows) · `canary_results_homospatial.json` · `hypotheses/canaries/canary-homospatial-*.md`

---

## COA 5 — Ranking + verify enablers (Nebenpunkt)

**Bet:** Surface leads without self-report noise; parallelize verify only after classification is worth scaling.

**Schwerpunkt:** outreach-rank (no self-report) · planted-survivor refute control · parallel Tavily + search cache · **no cron** until stability A/B ≥95%.

| Metric | Target | Current |
|---|---|---|
| Shortlist + control + throughput | Stable shortlist; ≥1 planted SURVIVE; 5× verify if stable | Rank + control + parallel/cache shipped; cron **not** installed |

**Kill:** Planted goods never survive without collapsing discrimination → hard refute; outreach only clean ADJACENT_ACTIVE.

**Artifacts:** `score_hypotheses.py --outreach` · `control_test_refutation_survivors.py` · `verify_hypothesis.py` (cache/parallel)

---

## Parallelization

| When | COA |
|---|---|
| Now | **1 + 2d** (send only sharpened packets; start 21-day clock) |
| Next | 2 + 5 ranking · 4 canaries |
| Product | 3 thesis-in |
| Last | 5 verify scale / cron (gated) |

---

*Exponent Labs LLC · scientific-intuition-engine/umpf_pipeline · Research-mission rewrite 2026-08-29*
