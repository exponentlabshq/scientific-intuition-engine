# Eureka Engine — Alternative Scoring & Selection Modules

Every file here was written by `audit_agent.py`, never by hand, and never runs automatically — nothing
else in this pipeline imports or executes anything in this directory. `run_cycle.py` does not know
this directory exists.

Each file is a complete, standalone script: run it yourself (`python3 alt_scoring/<name>.py`), read
its output, and decide whether it's actually correct and worth adopting. See `../proposals/` for the
rationale each one was written to implement, and `../proposals/README.md` for why "the agent wrote
it" is the start of the review, not the end of it.

**2026-08-29 disposition:** `pre_verification_filter.py` (proposal 001) and
`pre_verification_filter_v2.py` (proposal 003) are **REJECTED** — do not promote into the live
pipeline. See `../proposals/README.md` disposition board.

Nothing here is canonical. `score_hypotheses.py` and `mode_weights.json`, in the pipeline root, remain
the only scoring/weighting logic anything else in this pipeline actually reads.
