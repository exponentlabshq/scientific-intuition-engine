# Verdict stability A/B protocol (COA 5 gate before cron)

**Status:** Protocol defined; A/B not yet run; **cron / launchd NOT installed.**

Parallel Tavily + `search_cache/` are live in `verify_hypothesis.py` (`EUREKA_SEARCH_WORKERS`, `EUREKA_SEARCH_CACHE`). Standing schedule stays off until this gate passes.

## Gate

Frozen set of 20 already-verified hypothesis slugs (pick from ledger; mix COLLISION / ADJACENT_ACTIVE / NO_SIGNAL).

1. **Baseline:** re-verify with `EUREKA_SEARCH_WORKERS=1` and `EUREKA_SEARCH_CACHE=0` (or empty cache dir). Record verdicts.
2. **Treatment:** re-verify same slugs with workers=4 and cache enabled. Record verdicts.
3. **Pass:** ≥95% exact verdict agreement (19/20). Cost and wall-clock are secondary metrics.

If fail: keep serial path as default (`EUREKA_SEARCH_WORKERS=1`); do not install `run_cycle_scheduled.sh` into cron/launchd.

## After pass

Install schedule at low cadence only (e.g. 3 hyps/day). Fail-closed publish unchanged.
