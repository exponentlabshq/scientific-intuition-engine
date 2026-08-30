# Peer Review — Eureka Engine (Scientific Intuition Pipeline)

**Reviewer posture:** University Dean of Interdisciplinary Graduate Studies  
**Institution (frame):** a research university evaluating whether this system is fit to advise Masters and PhD candidates on thesis direction and prior art  
**Date:** 2026-08-29 (updated same day — Homospatial gold parity closed; COA 2d soft-vs-hard gate + kill sample)  
**Materials reviewed:** `eureka-engine-system-prd.md`; `eureka-engine-10x-coas.md`; `bisociation-domain-pairs.md`; `janusian-thinking.md`; `homospatial-thinking.md`; gold JSON corpora (bisociation / Janusian / Homospatial, 80 each); live canary results (`canary_results_janusian.json` recall=1.0 on 6; `canary_results_homospatial.json` recall=1.0 on 3 judged, 3 PENDING_VERIFICATION); fresh Janusian generation batch (n=3, 0 clean); fresh Homospatial generation batch (n=3, 2 clean); outreach packet draft set + COA 2d sharpen ritual; ledger/scoring/refutation architecture as documented.

---

## 1. Executive judgment

This is **not** a toy brainstorming app. It is an attempt to build a **faculty-adjacent triage instrument**: propose a falsifiable interdisciplinary lead, then classify whether the lead is already published, adjacent and fertile, or not a real research direction.

Against that standard, my judgment is:

> **Conditionally promising. Cleared for a bounded pilot with real graduate students. Not yet cleared as a general advisor of thesis time.**

The group has earned the right to a pilot. They have not earned the right to scale volume or to tell a doctoral student, without human faculty oversight, that a lead is “safe” to pursue.

Homospatial is no longer the junior instrument on paper — doctrine, few-shots, mechanical fusion check, and prior-art canaries now match Janusian’s shape. Generation quality still trails the filter (as with Janusian). That is an honesty feature, not a product claim.

---

## 2. What this project gets right (and most AI “ideation” systems do not)

### 2.1 Mission discipline

The restated mission — recover Masters/PhD time by classifying COLLISION / ADJACENT_ACTIVE / not a lead — is the correct unit of value for a university. Time is the scarce resource. Novelty theater is not. I particularly commend the explicit exclusion of commercial deal-ideation as a success metric. That temptation would have corrupted the epistemology within a semester.

### 2.2 Doctrine that can be taught

The three-way split is faculty-grade:

| Mechanism | Signature |
|---|---|
| Bisociation (Koestler) | Transplant a generative relation across domains |
| Janusian (Rothenberg) | Hold contradictory poles simultaneously for the **same** instance |
| Homospatial (Rothenberg) | Force discrete entities into the **same space** until a new identity emerges |

The gold tables (**80 bisociation · 80 Janusian · 80 Homospatial** reconstructions) are not decoration. They are **curriculum**. They operationalize what most “creativity” systems leave as vibe. All three modes now inject rotating few-shots at generation time and enforce mode-specific mechanical honesty checks.

### 2.3 Epistemic hygiene

I note with approval:

- Append-only ledger; latest-entry-wins reads  
- Mechanical honesty checks that fail closed and **flag** rather than silently polish  
- Separation of Phase 2 (prior-art grounding) from refutation (internal coherence)  
- Refusal to auto-send researcher outreach  
- Circuit-breaker behavior when search infrastructure degrades (observed live: Tavily 432 → Monid/Exa fallback; PENDING_VERIFICATION when all search paths fail — correctly excluded from canary recall rather than scored as false negatives)  
- Homospatial fusion-form check: comparison-language ban on §2–§3 **plus** required overlay/chimera signature on §2–§4

This is closer to a methods lab than to a chatbot wrapper.

### 2.4 Prior-art canary results

**Janusian (2026-08-29):** six historically established plants (Einstein equivalence, Bohr complementarity, Planck quanta, Dirac antimatter, Heisenberg uncertainty, Gödel incompleteness) → **6/6 COLLISION. Recall = 1.0.**

**Homospatial (2026-08-29):** six plants from `homospatial-thinking.md` (desktop GUI, DNA double helix, McCulloch–Pitts, Hopfield, Toyota kanban, Gutenberg press). Where search returned evidence: **3/3 COLLISION (desktop, DNA, McCulloch–Pitts). Judged recall = 1.0 against an 80% gate.** Three remaining (Hopfield, Toyota, Gutenberg) stayed `PENDING_VERIFICATION` after Tavily 432 and Monid empty/BLOCKED — infrastructure, not classifier miss. Gate cleared on judged set; full 6/6 still owed when search recovers.

Missing named canon when evidence is present would be disqualifying. Passing judged canaries is necessary, not sufficient — but Homospatial now clears the same minimum competence bar Janusian cleared earlier today.

---

## 3. Where the project is not yet ready for unsupervised graduate advice

### 3.1 Generation quality remains weak for arbitrary domains

| Mode | Fresh autonomous batch (n=3) | Interpretation |
|---|---|---|
| Janusian | **0/3** clean same-instance after retry (all flagged) | Filter works; generator produces compromises dressed as paradoxes |
| Homospatial | **2/3** clean fusion first-pass; **1/3** flagged after retry | Better than Janusian on this sample; still not “press button, receive thesis” |

Therefore neither Janusian nor Homospatial may be presented to students as unsupervised lead factories. Flagged outputs are “did not clear method,” not leads.

I would still require, before broader deployment: either (a) a domain pre-filter for load-bearing assumptions / fusible entity pairs, or (b) a hard policy that flagged outputs never reach student-facing “leads.”

### 3.2 Phase 3 — the actual mission test — has not begun

Packets exist. Sends do not. Until a living researcher says *novel / known / dismiss* on a system-generated ADJACENT_ACTIVE lead, the product remains a sophisticated internal seminar, not a graduate service.

No amount of leaderboard points substitutes for that letter.

**Soft vs hard (COA 2d) — required before Store B sends.** Raw ADJACENT often encodes a soft fusion (near-known neighbors) dressed as a lead. The operators now require: closed-loop rewrite → denser re-verify of the *hard* chimera → packet only the hard claim (`sharpened: true` in the outreach manifest). Kill sample (n=3): one soft-trap collapsed to COLLISION (DiCola on Nash×sampling); two hard claims stayed ADJACENT and earned packets. That is the right epistemic shape for a faculty-adjacent tool — do not send soft claims to living researchers.

### 3.3 Self-report scores remain epistemically hollow

The project’s own audits already found Distance/Tension/Fusion near noise. Outreach ranking that excludes self-report is correct. Do not reintroduce vanity novelty scores into any student-facing interface.

### 3.4 ~~Homospatial still lacks gold parity~~ — CLOSED 2026-08-29

Homospatial now has doctrine table (`homospatial-thinking.md`), runtime gold JSON (80), few-shots, fusion-form mechanical check, prompt §4 fusion sentence, and prior-art canaries. Treat remaining risk as **generator quality + search SLA**, not missing doctrine.

### 3.5 Infrastructure fragility

Live canary runs depended on paid fallback search after primary search rate-limited; Homospatial’s second half of the set could not even complete fallback. Fine for a lab. Not fine as silent dependency for a student-facing service without a stated SLA and budget. `PENDING_VERIFICATION` is the correct fail-closed behavior — do not invent COLLISION from empty results.

---

## 4. Recommendation to the faculty / operators

I recommend a **three-store pilot**, in the spirit of staged institutional change:

| Store | What | Pass condition |
|---|---|---|
| **A — Prior-art triage** | Students submit a home domain or thesis question (`--challenge`); system returns COLLISION / ADJACENT / not a lead with citations | ≥5 students report “this clarified whether X was already published” |
| **B — Frontier leads only** | Only **COA 2d–sharpened** unflagged ADJACENT_ACTIVE + actively researched packets (hard claim only; soft near-known retired); Janusian/Homospatial flagged outputs excluded; `NEEDS_SHARPEN` packets are not send-ready | ≥1 external researcher reply logged on ledger |
| **C — Methods teaching** | Use gold tables + canaries as a seminar module on Koestler/Rothenberg | Course eval: students can discriminate bisociation vs Janusian vs Homospatial vs analogy |

**Do not** install unattended high-volume generation until Store A or B produces external confirmation.

**Do not** market this as “AI discovers new science.” Market it as: **“AI helps you not waste a year rediscovering what is already named.”** That is an honorable, fundable graduate-school service.

---

## 5. Formal scorecard

| Criterion | Score (1–5) | Note |
|---|---|---|
| Clarity of research mission | 5 | Correctly recentered away from deal ideation |
| Theoretical grounding | 5 | Koestler + Rothenberg (Janusian *and* Homospatial) operationalized |
| Prior-art honesty (canaries) | 5 | Janusian 6/6; Homospatial 3/3 judged COLLISION (3 PENDING infra) |
| Lead-generation quality (Janusian) | 2 | Fresh n=3: 0 clean same-instance; filter saves the day |
| Lead-generation quality (Homospatial) | 3 | Fresh n=3: 2/3 clean fusion; filter catches the rest |
| Student-facing readiness | 2 | Phase 3 unsent; challenge path exists but unproven with people |
| Governance / fail-closed ethics | 4 | Flags, no auto-send, ledger discipline, PENDING on search failure |
| Scalability claim | 2 | Domain pool and search cost are real; volume is not the lever |

**Overall:** **3.7 / 5 — pilot-ready, not product-ready.** (Up from 3.6 after Homospatial doctrine parity; Phase 3 still the blocker.)

---

## 6. Closing note from the Dean’s chair

Universities are drowning in tools that help students *produce more text*. Almost none help them *avoid a false research program*.

If Exponent Labs keeps the mission narrow — prior-art triage and thesis-direction honesty — and closes the loop with real researchers, this can become a legitimate interdisciplinary methods facility: a small Faculty of Interdisciplinary Research in software form.

If they chase volume, leaderboard vanity, or commercial deal metaphors, they will have built an expensive analogy machine with a scholarly vocabulary.

The Janusian canaries passed. Homospatial doctrine parity is closed; judged Homospatial canaries pass. Soft-vs-hard sharpen is now the Store B gate. The letters have not been sent. **Send the sharpened letters.**

---

*Respectfully submitted in the posture of a Dean of Interdisciplinary Graduate Studies, for the operators of the Eureka Engine / scientific-intuition-engine, 2026-08-29 (Homospatial + COA 2d addendum same day).*
