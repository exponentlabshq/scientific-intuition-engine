# UMPF Pipeline | Who • What • Where • Why • How

## Who
- Author: Michael Jagdeo  
- Organization: Exponent Labs LLC

## What
A minimal, fidelity‑first pipeline that:
- extracts verbatim text from a canonical PDF, and
- produces a structured UMPF analysis (Markdown) constrained by a formal prompt schema.

## Where
- inputs/ — place your PDF here  
- prompts/ — UMPF schema (e.g., `umpf_system_prompt.md`)  
- outputs/ — generated artifacts (`<name>.txt` verbatim, `<name>.md` structured)  
- peer-review/ — model/human audit notes tied to runs  
- main.py — the orchestrator (kept intentionally small)  
- the-rosetta-stone-thesis.md — reference thesis

## Why
- Preserve truth: verbatim `.txt` is a citation‑grade anchor.  
- Enforce structure: `.md` analysis follows a formal schema (monads, graphs, lenses, layers).  
- Enable comparability: identical structure across papers supports cross‑domain reasoning and meta‑analysis.  
- Make it portable: plain text/Markdown artifacts any model or collaborator can use.

## How (run this)
1) Put a PDF in `inputs/`  
2) Ensure a UMPF schema exists in `prompts/` (e.g., `umpf_system_prompt.md`)  
3) Install deps: `pip install -r requirements.txt`  
4) Run: `python3 main.py`  
5) Review `outputs/<name>.txt` (verbatim) and `outputs/<name>.md` (structured)

### Flow (simple sequence)
```mermaid
sequenceDiagram
    participant I as inputs
    participant E as extractor
    participant O as outputs
    participant P as prompts
    participant L as llm
    participant R as review

    I->>E: PDF
    E->>O: save txt
    O->>P: load prompt
    P->>L: send txt and prompt
    L->>O: save md
    O->>R: notes
```

## Guarantees and Invariants
- `.txt` is the source of truth. If `.md` and `.txt` conflict, the `.txt` wins.  
- The prompt schema constrains analysis to comparable sections (e.g., Abstract; Formal Framework; Monadic mapping).  
- Peer‑review captures critique and iteration without losing provenance.

## Requirements
- Python 3.10+  
- `pip install -r requirements.txt` (pdfminer.six, openai 0.28 style, python‑dotenv, rich)  
- `.env` in repo root or parent (if enabling LLM analysis):  
  `OPENAI_API_KEY=...`

## Troubleshooting
- Empty `.txt`? PDF may be image‑only → add OCR fallback (e.g., Tesseract + pdf2image).  
- Long PDFs? Chunk before analysis → stitch outputs for `.md`.  
- Rendering on GitHub? Keep Mermaid node labels simple (no parentheses).

## The Eureka Engine — hypothesis_engine.py + verification (Phase 1 + Phase 2)

`main.py` above takes one paper and writes one structured UMPF analysis. `hypothesis_engine.py`
is a separate, faster mode: given two domains (or one, for Janusian), it generates a candidate
cross-domain hypothesis via one of three distinct generative mechanisms, run with `--mode
{bisociation,janusian,homospatial}`. Explicit pair/domain or `--autonomous --count N` (draws
fresh unpaired domains from the combined pool — `domains.json` unioned with
`rosetta_stone_domains.json` and `equivalency_training_domains.json`, 170 domains total). Outputs
land in `hypotheses/`.

- **Bisociation** (Koestler) — two domains collide horizontally; each stays itself, a functor maps
  between them.
- **Janusian** (Rothenberg) — one domain's load-bearing assumption is held against its exact
  opposite, simultaneously, within a single instance — a genuine paradox, not a compromise. Prompt:
  `prompts/umpf_janusian_prompt.md`, with a mechanical "same-instance test" catching the compromise-
  wearing-paradox failure mode a soft prompt instruction alone did not.
- **Homospatial** (Rothenberg) — two domains are superimposed until they fuse into one new entity,
  not compared side by side. Prompt: `prompts/umpf_homospatial_prompt.md`, with a code-level scan
  for comparison language ("like," "similar to," "akin to") and one corrective re-prompt, for the
  same reason: a written-only rule got talked past by the model it was supposed to constrain.

**Phase 2 — verification (added 2026-08-28).** Every hypothesis's own self-critique includes "known
prior art: not verified" — a hand-wave, not a check. Phase 2 resolves it: web search against the
hypothesis's claim, classified into one of four outcomes per `prompts/umpf_verification_prompt.md`
— COLLISION (the connection is already established; strong signal the engine reasons soundly,
weak/no signal the hypothesis itself is worth pursuing), ADJACENT_ACTIVE (real fertile ground near
the domains, exact connection still open — the target state), FACT_CHECK_FAIL (the domain
description itself is wrong), or NO_SIGNAL (nothing surfaces either way — genuinely ambiguous, not
a pass, routed to adversarial refutation — see `refutations/README.md`). Results land in
`verifications/` (one file per hypothesis, doesn't touch the original) and `verification-log.jsonl`
(append-only, the ledger `score_hypotheses.py` reads to produce `leaderboard.md`).

**Current limit, stated plainly:** Phase 2 as it exists right now is Claude-orchestrated — a
Claude Code session runs the searches and applies the rubric — not a standalone script. Nothing in
this repo can call a web search API unattended; wiring that up (a paid SERP API in a script, or
scheduling a Claude Code session itself via cron) is unbuilt, not assumed done. This is a real,
recurring constraint, not theoretical: a prior session's own live WebSearch budget (200 calls) was
exhausted mid-batch after only 5 of 15 planned verifications, leaving the other 10 in a
`PENDING_VERIFICATION` state until a later, dedicated session — spending its own budget on nothing
else — cleared the backlog. That workaround (dedicate a session to verification alone) is real but
not durable; it will recur at whatever pool size makes a single session's budget insufficient for
the batch at hand, and the standalone-script fix remains the actual solution, still unbuilt.

## License & Citation
- License: MIT (© 2025 Michael Jagdeo, Exponent Labs LLC)  
- Repo: https://github.com/exponentlabshq/scientific-intuition-engine  
- Cite this pipeline: Jagdeo, M. (2025). Scientific Intuition Engine (UMPF). Exponent Labs LLC.  
- Original Thesis: Jagdeo, M. (2025). The Rosetta Stone of UMPF. Exponent Labs LLC. https://github.com/exponentlabshq/the-rosetta-stone

