# Eureka Engine — Session Handoff (2026-08-29, after 18:06 EDT)

**For:** any Claude / harness continuing Eureka Engine work  
**Window:** ~18:06–22:05 EDT, Saturday 2026-08-29 (Cursor session; transcript [`a4237aea-7007-443d-a491-5284643450ec`](../../.cursor/projects/Users-michaeljagdeo-Downloads-talentOS-2026/agent-transcripts/a4237aea-7007-443d-a491-5284643450ec))  
**Root:** `scientific-intuition-engine/` · pipeline: `umpf_pipeline/`  
**Live site repo:** `scientific-intuition-engine/eureka-engine-web` → GitHub `exponentlabshq/eureka-engine-web` (multiple `publish_site.py` pushes tonight)

---

## 0. Mission correction (read this first)

Early plan wrongly treated Eureka as deal-ideation (Sayve / MythosHealth / Katalyst / Zorro). **Michael corrected at 18:29.**

**Canonical mission:** recover Masters/PhD research time — propose a falsifiable cross-domain hypothesis, then classify **COLLISION / ADJACENT_ACTIVE / not a real lead**. R&D prior-art / thesis-direction machine.

**Out of scope forever for this engine:** vault deal Domain A, Exponent commercial deals as success metrics.

Doctrine sources:
- Bisociation → `bisociation-domain-pairs.md`
- Janusian → `janusian-thinking.md`
- Homospatial → `homospatial-thinking.md`
- Triptych overview → `bisociation-janusian-homospatial.md`

Living trackers:
- `umpf_pipeline/eureka-engine-10x-coas.md` ← **read scoreboard first**
- `umpf_pipeline/eureka-engine-system-prd.md`
- `umpf_pipeline/peer-review/eureka-engine-dean-peer-review-2026-08-29.md`

---

## 1. Chronological arc (what landed)

| Time (EDT) | What happened |
|---|---|
| 18:23–18:35 | Deep dive → 10X COAs planned → **rewritten for research mission only** → implementation started |
| 18:35–18:46 | Janusian gold parity path; Dean peer review requested and written |
| 18:58–19:20 | **Homospatial gold parity** closed; canaries + Dean letter updated; site publish question |
| 19:20–19:32 | Leaderboard/dashboard republished to GitHub; proposals folder reviewed (001/003 rejected; correction canonical) |
| 19:50–20:01 | ChatGPT critique of Resonant Swarm → **lightning ×2** (Swarm + Magneto-Operant sharpen→re-verify) → **COA 2d** adopted |
| 20:01–20:05 | COA 2d tooling + kill sample of 3 + doctrine updates + site republish |
| 20:50–22:01 | Phase 3 email drafts → Aronson short template → origin sentences → concrete rewrites for fluffy leads |
| 22:01 | **3 emails SENT** (Aronson, Frey, Phillips); 21-day clock started |

---

## 2. COA scoreboard (current truth)

See `eureka-engine-10x-coas.md` scoreboard. Snapshot:

| COA | Status now |
|---|---|
| **1 Phase 3** | **Clock running** — 3 sends 2026-08-29 → due ~**2026-09-19** |
| 2 Bisociation generative-relation | Implemented; blind A/B still pending |
| 2b Janusian simultaneous-hold | Gold + checks shipped; fresh n=3 → **0/3** clean (filter holds, generator weak) |
| 2c Homospatial fusion | Gold 80 + checks; fresh n=3 → **2/3** clean |
| **2d Sharpen → re-verify** | **Ritual live** — kill sample **1 COLLISION / 2 ADJACENT** (keep ritual) |
| 3 Thesis-in `--challenge` | CLI shipped; need ≥3 real researcher challenges |
| 4 / 4b / 4c Canaries | Janusian **6/6 recall 1.0**; Homospatial **judged 3/3 recall 1.0**, 3 PENDING search infra |
| 5 Ranking + verify | Rank/control/parallel/cache shipped; **cron off** |

**Parallelization now:** COA **1 + 2d** (send only sharpened packets).

---

## 3. Homospatial gold parity (closed tonight)

Previously Homospatial lagged Janusian. Now shipped:

| Artifact | Path |
|---|---|
| Doctrine | `homospatial-thinking.md` |
| Gold table | `umpf_pipeline/homospatial_gold_pairs.json` (**80** pairs) |
| Prompt | `prompts/umpf_homospatial_prompt.md` (§4 fusion sentence) |
| Runtime | `hypothesis_engine.py` — few-shots + **fusion-form mechanical check** (overlay/chimera required; comparison-language ban on §2–§3) |
| Canaries | `prior_art_canaries.json` (mode=homospatial) · `hypotheses/canaries/canary-homospatial-*.md` · `canary_results_homospatial.json` |
| Calibration | Canaries excluded from public leaderboard via `is_calibration_canary` in `score_hypotheses.py` |

**Judged canary result:** desktop GUI / DNA / McCulloch–Pitts → COLLISION. Hopfield / Toyota / Gutenberg → `PENDING_VERIFICATION` (Tavily 432 / Monid empty — infra, not classifier miss).

---

## 4. COA 2d — Soft vs hard (the big epistemic upgrade)

**Bet:** Raw ADJACENT often encodes a *soft* fusion. Closed-loop sharpen + denser prior-art search splits soft (near-known) from hard (still adjacent) before wasting a researcher’s time.

### Tooling

| File | Role |
|---|---|
| `umpf_pipeline/sharpen_hypothesis.py` | Checklist / `--apply` with soft-retired, chimera, hard-claim; writes revision banner + COA 2d block |
| `outreach/README.md` | **Send-ready gate:** hard ADJACENT + revision + soft-vs-hard verification + hard claim in email only |
| `outreach/packets_manifest.json` | `sharpened` bool · `hard_claim_one_liner` · statuses (`NEEDS_SHARPEN` / `SEND_READY_NOT_SENT` / `SENT_AWAITING_REPLY` / `SOFT_TRAP_NO_PACKET`) |
| `score_hypotheses.py --outreach` | Prefers sharpened; **−20 demote** if not sharpened |

### Lightning ×2 (exemplars — still ADJACENT on hard claim)

1. **Resonant Swarm** — `hypotheses/2026-08-29-homospatial-swarm-robotics-x-physical-acoustic-resonance.md`  
   Soft: robots communicate with sound → near Aranson/Frey PRX 2025.  
   Hard: \(S \leftrightarrow R\) cavity-resonance blackboard + chamber-geometry protocol.

2. **Magneto-Operant** — `hypotheses/2026-08-29-homospatial-behavioral-psychology-x-physical-magnetic-field-control.md`  
   Soft: magnets affect operant behavior → near Liboff–Thomas (Liboff **died 2023**).  
   Hard: programmable field manifold *is* the reinforcement schedule + yoked controls.

### Kill sample (next 3 sharpens — neither kill tripped)

| Lead | Hard verdict | Action |
|---|---|---|
| Game Theory × Music | **COLLISION** — Peter DiCola Nash model of sample licensing | No packet (`SOFT_TRAP_NO_PACKET`) |
| Architecture ⊕ Pattern Recognition | ADJACENT — Permit-Pattern / as-built→library→permit | Packet + emails (NOT SENT) |
| Janusian Creative Block | ADJACENT — Same-instance Block Paradox | Packet + email (NOT SENT; claim sharpened vs incubation) |

Verifications under `verifications/*-verification.md`. Ledger appends in `verification-log.jsonl`.

**Kill rules (still open):** 3/3 hard COLLISION → raise ADJACENT bar at generation; 0/3 movement → drop ritual. Current: **1/3 COLLISION, 2/3 still ADJACENT** → keep.

---

## 5. Phase 3 outreach (human loop — live)

### Email body model (Michael — Aronson template)

```
Dear Prof. X,

I'm with Exponent Labs' Eureka Engine.

**[operational hard claim — variables + contrast with soft neighbor]**

[one origin sentence: mode + soft neighbor retired]

We have a syndicate of investors.

Best regards,
Michael Jagdeo
…
```

**Do not** use a/b/c menus, ADJACENT badges, score points, or soft/hard lectures in the body.

### Emails folder

`umpf_pipeline/outreach/emails/` — index in `emails/README.md`

| File | To | Status |
|---|---|---|
| `email-resonant-swarm-aronson.md` | isa12@psu.edu | **SENT 2026-08-29** |
| `email-resonant-swarm-frey.md` | frey@lmu.de | **SENT 2026-08-29** |
| `email-magneto-operant-phillips.md` | jphillip@vt.edu | **SENT 2026-08-29** |
| `email-permit-pattern-el-gohary.md` | gohary@illinois.edu | NOT SENT (rewritten concrete: as-built BIM→library→next permit) |
| `email-permit-pattern-zhang.md` | zhan3062@purdue.edu | NOT SENT (same claim; alt) |
| `email-creative-block-schooler.md` | schooler@psych.ucsb.edu | NOT SENT (rewritten: stuck unfinished work vs incubation break; word/page count + judged novelty) |

### Clock

- **Started:** 2026-08-29  
- **Due (~21d):** 2026-09-19  
- **Pass condition (COA 1):** ≥1 researcher_confirmed_novel **or** ≥2 researcher_confirmed_known  
- **On reply:** set ledger `outreach_status` to `researcher_confirmed_novel` | `researcher_confirmed_known` | `researcher_dismissed`

Packets for Swarm + Magneto marked SENT in `outreach/packets/`. Manifest `phase3_clock` populated.

---

## 6. Proposals / audit discipline

Under `umpf_pipeline/proposals/`:

- **001** and **003** — **REJECTED** (do not implement as written)
- Correction to 003 is canonical
- Dashboard spotlight should show rejected + correction (published)

Same rule as outreach: audit proposals are drafts until human adopt; never auto-merge into live pipeline.

---

## 7. Site / scoring publishes tonight

Repeated: `python3 score_hypotheses.py` → `python3 publish_site.py` → push `eureka-engine-web`.

Data-driven pages only: `leaderboard.html`, `landing.html`, `dashboard.html`. **`whitepaper.html` never auto-touched.**

Outreach shortlist (post-2d): top slots are sharpened (✂); unsharpened demoted `[NEEDS_SHARPEN]`.

---

## 8. Doctrine / peer-review updates

| Doc | What changed |
|---|---|
| `eureka-engine-system-prd.md` | COA 2d send-ready gate paragraph; Phase 3 still 0→now sends logged separately |
| `eureka-engine-10x-coas.md` | COA 2d evidence tables; Parallelization **Now: 1 + 2d**; Phase 3 clock |
| `peer-review/eureka-engine-dean-peer-review-2026-08-29.md` | Homospatial parity closed; Store B requires **COA 2d–sharpened** packets; soft-vs-hard named in §3.2 |

Dean overall still: **pilot-ready, not product-ready** — letters were the blocker; **letters are now partially sent**.

---

## 9. What the other harness should *not* do

- Do not invent deal-ideation COAs or wire Eureka to Sayve/Zorro success metrics  
- Do not send `NEEDS_SHARPEN` / soft-only packets  
- Do not email Liboff (deceased 2023)  
- Do not treat PENDING canaries as classifier failure  
- Do not auto-send researcher email; human sign-off only  
- Do not “fix” fluffy claims with more abstract jargon — operational variables + soft-neighbor contrast only  
- Do not edit Cursor plan files unless Michael asks  

---

## 10. Recommended next moves (priority order)

1. **Await** Aronson / Frey / Phillips replies; log outcomes on ledger when they land  
2. Optional: send **one** of El-Gohary *or* Zhang, and/or Schooler (concrete rewrites ready)  
3. Re-verify PENDING Homospatial canaries when search SLA recovers  
4. Run ≥3 real `--challenge` thesis-in sessions (COA 3)  
5. Blind A/B for bisociation generative-relation (COA 2) when ready  
6. Stability A/B before any verify cron (COA 5)

---

## 11. Key paths cheat-sheet

```
scientific-intuition-engine/
  bisociation-domain-pairs.md
  janusian-thinking.md
  homospatial-thinking.md
  umpf_pipeline/
    eureka-engine-10x-coas.md          # scoreboard
    eureka-engine-system-prd.md
    sharpen_hypothesis.py             # COA 2d
    score_hypotheses.py               # --outreach demotes unsharpened
    verification-log.jsonl
    peer-review/eureka-engine-dean-peer-review-2026-08-29.md
    outreach/
      README.md                       # send-ready gate
      packets_manifest.json
      emails/README.md                # Phase 3 send status
      emails/email-*.md
      packets/
    hypotheses/…                      # revised Swarm, Magneto, batch-3, …
    verifications/…
    proposals/                        # 001/003 REJECTED
  eureka-engine-web/                  # published site
```

---

## 12. One-line state for cold start

> Eureka is a research prior-art engine; Homospatial is at gold parity; soft-vs-hard sharpen (COA 2d) is mandatory before outreach; Phase 3 clock is running with 3 sharpened emails already out to Aronson, Frey, and Phillips — product proof is now their replies, not more internal generation.

---

*Handoff written 2026-08-29 ~22:05 EDT for cross-harness continuity. Update this file if you move the Phase 3 clock or land researcher replies.*
