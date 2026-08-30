# Eureka Engine — Audit Proposals

**Status across the board: unreviewed until a human reads it, and nothing here is wired into the
live pipeline automatically.** Same discipline as `outreach/README.md`'s Phase 3 drafts — `audit_agent.py`
proposes, a person decides.

## Disposition board (2026-08-29)

| File | Status | Note |
|---|---|---|
| `2026-08-29-proposal-001.md` | **REJECTED** | Wrong ledger field (`mode` vs `source`); mission conflict |
| `2026-08-29-proposal-002.md` | — | Never written (README was once counted as a proposal; numbering skipped) |
| `2026-08-29-proposal-003.md` | **REJECTED / SUPERSEDED** | Self-report not predictive of NO_SIGNAL once extraction bugs fixed |
| `2026-08-29-correction-to-proposal-003.md` | **Canonical write-up** | Why 003 dies; real win was fixing `extract_self_score()` |

## What this directory is

Every time `audit_agent.py` runs, it computes real, current performance stats from the ledger and
`token_usage.jsonl`, and asks an OpenAI model to propose exactly one specific, additive improvement,
grounded in those numbers. The proposal — rationale, self-reported risks, and the exact data snapshot
it was grounded in — gets written here as `<date>-proposal-<NNN>.md`. Nothing before this file is
written has touched any other file in the pipeline.

## What "additive only" actually means, mechanically

`audit_agent.py` cannot edit or delete an existing file — that isn't a prompt instruction, it's a
structural property of the script (it only ever opens files in `"w"` mode inside `proposals/` and
`alt_scoring/`, both directories it's free to create new entries in, never elsewhere). If a proposal
includes code, that code is validated with `ast.parse()` before being written — invalid Python is
rejected and logged as such in the proposal, never silently written broken.

## The first real proposal, and what it taught us (2026-08-29)

Proposal 001 was grounded in real numbers (case-study mode's 8.1 avg points vs. homospatial's 24.3)
but its generated code contained a real bug: it filtered on `entry.get('mode') == 'case-study'`, a
label that only exists in `audit_agent.py`'s own in-memory aggregation, not in any real ledger entry
(case-study entries are identified by `source == 'rosetta-stone-case-study'`, not a `mode` field) — so
the script runs without error but silently filters nothing. This is exactly why the review checklist
below isn't decorative: the very first proposal needed a human to catch something real before adoption.

## Promotion — always a manual, deliberate act

Reading a proposal and deciding it's right does not make it live. Promotion means:
- If it's a weighting change: hand-edit `mode_weights.json` yourself, citing the proposal in the commit.
- If it's a new scoring/badge variant: keep it running standalone under `alt_scoring/` as a permanent
  *alternative* leaderboard (never silently replacing `leaderboard.md`), or explicitly wire it into a
  new, clearly-labeled section of the published site if you want it public.
- If it's a filter: verify the code is actually correct against the real ledger before trusting its
  output, the same as any other code you didn't write yourself.

Every proposal file ends with a promotion checklist. Check it honestly, don't just tick it.
