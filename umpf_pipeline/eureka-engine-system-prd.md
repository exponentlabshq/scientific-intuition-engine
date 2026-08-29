# The Eureka Engine — System PRD

**What this document is:** a canonical, current-state description of how the Eureka Engine actually works, as of 2026-08-29 — not a plan for future work (see the PRDs and postmortems for that), not an incident report. If you want to know what a fresh operator or a new session needs to understand before touching this system, this is the document.

---

## 1. Mission

Exponent Labs LLC's stated goal for this system, in the words it was given: build *"a self-contained inter-disciplinary R&D department whose goal is to recover lost Masters & PhD time by helping them identify which theses and directions of research AREN'T a waste of their time."*

The concrete, checkable version of that mission: for any two ideas from different fields, or one idea and its own inverted assumption, produce a specific, falsifiable hypothesis about the collision — then classify, as honestly as the system knows how, whether that hypothesis is (a) already known and published, (b) genuinely unexplored and worth a researcher's time, or (c) not actually a real idea once tested against adversarial scrutiny. The leaderboard is the interface; the pipeline behind it is what has to be trustworthy for the leaderboard to mean anything.

## 2. The three generation mechanisms

Three structurally distinct instruments, not three settings of one, each with a real, cited doctrine source (`hypothesis_engine.py`'s own docstring; `Ops/skills/bisociate.md`, `janusian.md`, `homospatial.md` in the vault):

| Mode | Mechanism | Doctrine source |
|---|---|---|
| **Bisociation** | Two domains collide; a candidate functor maps between them, each stays itself | Arthur Koestler, *The Act of Creation* (1964) |
| **Janusian** | One domain's load-bearing assumption is inverted and held simultaneously with the original — a genuine paradox, not a compromise | Dr. Albert Rothenberg, *The Emerging Goddess* (1979) |
| **Homospatial** | Two domains superimposed in the same conceptual space until they fuse into one new entity that belongs to neither | Rothenberg, "Homospatial thinking in creativity" (1976); re-derived in cognitive science as conceptual blending (Fauconnier & Turner) |

Domains are drawn from a combined pool of **170 real entries** across three sourced files (`domains.json`: 59; `rosetta_stone_domains.json`: 23; `equivalency_training_domains.json`: 88), giving bisociation/homospatial a **14,365-pair** addressable space and janusian a 170-entry addressable space. `domains.json` tracks which domains/pairs have already been drawn (`already_paired`, `already_janused`, `already_homospatial`), so autonomous runs never regenerate the same hypothesis.

### Mechanical honesty checks (generation-time)

A recurring, hard-won lesson of this project: a written instruction in a prompt gets *partially* followed by the model, never reliably followed. Every generation-time check that matters is therefore enforced mechanically — the actual output is scanned, and a violation triggers one corrective retry — not just requested in prose:

- **Homospatial's comparison-word scan** (§2 and §3): catches bisociation wearing homospatial's name (comparison language like "A is like B" instead of a genuine fusion). Real retry-fix rate: ~89%.
- **Janusian's context-split scan** (§4): catches a disguised compromise ("[proposition] in context A, [inversion] in context B") wearing a genuine paradox's name. Real retry-fix rate: ~20% — read as a real property of the mode (many domains don't support a genuine same-instance paradox) rather than a prompt gap to keep chasing.
- **The named-entity search-query check** (all three modes): requires at least one Search Query to target a specific named theory/framework/researcher, not just the general concept — closes the exact gap that let a real hypothesis miss its own collision with Andrew Lo's published Adaptive Markets Hypothesis. Real retry-fix rate: ~92-100%.

When a check still fails after one retry, the hypothesis file itself is honestly flagged (`**⚠️ Automated check failed twice:**...`) — never silently accepted as clean. All three checks' flag text is collected and appended **once, at the very end** of generation, after every check (including the query check) has already run — a structural fix for a real bug where an earlier check's flag could be silently erased by a later check's own correction.

## 3. The pipeline, stage by stage

`run_cycle.py` orchestrates one full cycle, unattended, no live session required:

1. **Generate** (`hypothesis_engine.py`) — draws fresh domains, produces N hypotheses split across modes by `mode_weights.json`'s real, ledger-derived weights.
2. **Verify** (`verify_hypothesis.py`) — real web search (Tavily, with a Monid/Exa fallback — see §5) + GPT-4o classification against a four-bucket rubric: `COLLISION` (already published), `ADJACENT_ACTIVE` (the concept is real and active, this specific connection isn't documented), `NO_SIGNAL` (no real-world grounding found either way), `FACT_CHECK_FAIL` (a factual claim in the hypothesis is simply wrong). `PENDING_VERIFICATION` is a fifth, distinct state — not a real verdict — for when the search infrastructure itself failed, so a transient outage never gets misclassified as a real negative finding.
3. **Refute** (`refute_hypothesis.py`) — three independent OpenAI completions (coherence / testability / triviality), each its own isolated call with no shared state, 2-of-3 survival required. Runs on every `NO_SIGNAL` verdict, **and** on any `ADJACENT_ACTIVE` verdict whose hypothesis already failed its own mechanical honesty check (see §2) — because Phase 2's verdict and the honesty check test two different things, and passing one says nothing about the other. `COLLISION` is deliberately excluded — real prior art already exists, so refutation would just spend money re-confirming something already correctly badged.
4. **Score** (`score_hypotheses.py`) — real points per phase (self-report, Phase 2 verdict, refutation outcome), badges, leaderboard.
5. **Observe** (`audit_agent.py --observe`) — a cheap (~1,300 tokens, gpt-4o-mini), lightweight comparison against the last observation, feeding the dashboard's live commentary.
6. **Publish** (`publish_site.py`) — rebuilds and deploys the data-driven pages (leaderboard experience, landing page stats, dashboard) to `eureka-engine-web`. `whitepaper.html` is deliberately excluded — its real numbers live inside flowing prose, not substitutable fields, and updating it is a manual, human-reviewed pass.

## 4. The ledger — append-only write, latest-entry-wins read

`verification-log.jsonl` is the single source of truth: one JSON line per verification event, never edited or deleted, only appended to. A correction is always a *new* line for the same `hypothesis_slug`, never a rewrite of an old one.

Every reader (`score_hypotheses.py`, `assemble_experience_data.py`, `refute_hypothesis.py`'s slug-selection functions, `verify_hypothesis.py`'s already-verified check) goes through `ledger.py`'s `load_latest_entries()` — the one place "which line is authoritative for this slug" gets decided. This is what lets a hypothesis be re-verified after a real bug fix without double-counting it on the leaderboard under both its old, wrong verdict and its new, correct one.

`already_verified_slugs()` additionally treats `PENDING_VERIFICATION` as *not done* — a hypothesis whose evidence-gathering failed gets automatically retried the next time `--all-unverified` runs, rather than needing a human to name the file explicitly forever.

## 5. Search providers — Tavily, primary; Monid/Exa, fallback; a real circuit breaker between them

`verify_hypothesis.py` calls Tavily first, with retry/backoff on rate-limit-shaped errors (HTTP 429, and Tavily's own 432) and fail-fast on real errors (auth, bad request). If Tavily is confirmed down once in a given process, a circuit breaker (`_tavily_degraded`) skips its retries for every subsequent query in that same run and falls straight through to the Monid/Exa fallback — because paying a ~22-second retry cost on every query once the service is already known to be dead is waste, not caution.

Monid (`https://monid.ai`, via the `monid` CLI, `MONID_API_KEY` in `.env`) provides Exa neural/keyword search as a metered, paid fallback ($0.01/call) — deliberately kept a backstop, not the primary path, so it doesn't quietly become the majority of search spend. If every query for a hypothesis fails even with the fallback, the hypothesis is marked `PENDING_VERIFICATION` rather than letting the classifier guess a verdict from zero evidence.

## 6. The audit agent — watches the ledger, proposes, never adopts

`audit_agent.py` has two modes: a cheap `--observe` pass every cycle (writes one grounded, comparative sentence to `audit_observations.jsonl`, never proposes code), and an occasional deep pass that writes exactly one proposal plus optional code to `proposals/`. The hard constraint is structural, not a prompt request: the agent can only ever create new, timestamped files. It can never edit or delete an existing one, and nothing in `run_cycle.py` imports or executes anything it writes automatically. Promotion — actually adopting a proposal — is always a manual, deliberate human act.

Real track record: two proposals made, both grounded in real data, both wrong in their generated code, both caught before doing any damage. Investigating the second one, as a side effect, is what found a real silent scoring bug affecting 39 ledger entries.

## 7. Scheduling

`run_cycle_scheduled.sh` is a thin wrapper around `run_cycle.py` that preserves its exit-code contract (0 clean, 1 degraded/failed) and writes a timestamped log under `scheduler_logs/`. It is proven to work via real invocation. It is **not** registered as a standing cron/launchd job — installing a recurring task that spends real API budget and pushes to a public GitHub repo on a timer is a deliberate, standing decision left for a human to make explicitly; the install snippets live in the script's own comments.

## 8. Real economics (measured, not estimated)

| Phase | Real cost driver |
|---|---|
| Verification | The single largest cost line — feeding ~25 real search results into the classifier per hypothesis |
| Refutation | Runs only on NO_SIGNAL and flagged-ADJACENT_ACTIVE cases; the only phase that can only ever cost points |
| Generation | Cheapest phase by a wide margin (gpt-4o-mini) |
| Audit | Two modes, two very different costs — the deep pass is comparable to a verification call; the observe pass is nearly free |

At current unit economics (~$0.019/hypothesis blended), the entire known 14,365-pair domain space could be exhausted once for roughly $300 — money was never the constraint on this system's growth; the domain pool's finite size is.

## 9. Known, disclosed limitations (not gaps to be surprised by)

- **Phase 3 (real researcher confirmation) has zero real drafts, ever.** The scoring bands exist (+50 confirmed novel, -20 dismissed); the mechanism has never been exercised for real. This is genuine human labor, not something the pipeline can do on its own.
- **The Koestler triptych** (a possible fourth generation mode) is not built. Confirmed absent from the codebase; would need real primary-source doctrine grounding and a small pilot before touching any budget, matching the discipline the existing three modes went through.
- **Verification cost is unaddressed.** It's the largest single line and no low-risk reduction has been identified without risking a silent quality regression.
- **Refutation's lifetime record is 0-of-54 survived.** This is either strong evidence the lenses discriminate real quality, or a sign the rubric defaults to REFUTED more often than it should — the control test raised this question; it has not been resolved either way.
- **One control-test-scorer edge case is left open by design**: a self-report score label mentioned twice in one section is ambiguous about which mention is real. Forcing a fix risks trading one failure mode for a different, unproven one.

## 10. File map

| File | Role |
|---|---|
| `hypothesis_engine.py` | Generation — three modes, mechanical honesty checks, filename-collision-safe saving |
| `verify_hypothesis.py` | Phase 2 — Tavily + Monid fallback + circuit breaker, four-bucket classification |
| `refute_hypothesis.py` | Adversarial refutation — three independent lenses, widened pending-selection logic |
| `score_hypotheses.py` | Scoring + leaderboard, reads via `ledger.py` |
| `ledger.py` | The single shared "latest entry per slug wins" read for the append-only ledger |
| `audit_agent.py` | Self-observation (cheap, every cycle) and self-audit (occasional, additive-only proposals) |
| `run_cycle.py` | Orchestrates one full cycle; fail-closed on any stage failure |
| `run_cycle_scheduled.sh` | Thin, logged wrapper proven for real scheduler invocation (not installed) |
| `publish_site.py` | Rebuilds/deploys the data-driven site pages (never touches `whitepaper.html`) |
| `control_test_scorer.py` | Adversarial control test for the scorer, built in direct response to a named review gap |
| `domains.json`, `rosetta_stone_domains.json`, `equivalency_training_domains.json` | The 170-domain combined pool and its already-explored tracking |

---

*Exponent Labs LLC · scientific-intuition-engine/umpf_pipeline · Generated 2026-08-29 · A living reference — update this document, not just the postmortems, when the system's actual shape changes.*
