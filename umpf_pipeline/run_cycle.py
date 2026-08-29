#!/usr/bin/env python3
"""
run_cycle.py — one full autonomous Eureka Engine cycle: generate -> verify
-> refute -> score. No Claude Code session required for any of it; every
step runs on OpenAI tokens (hypothesis_engine.py, verify_hypothesis.py,
refute_hypothesis.py) or a search API (Tavily, via verify_hypothesis.py).

This is the piece that makes "runs on its own" literal rather than
aspirational: point cron at this script and the ledger keeps growing without
a live session watching it. Every phase's real subprocess output is
captured into cycle_log.jsonl so a human can audit what an unattended run
actually did after the fact, even though nobody was watching live.

Deliberately scoped to the RESEARCH pipeline only -- it does not rebuild or
redeploy the public website (landing/whitepaper/leaderboard-experience).
That stays a separate, human-reviewed publishing step. An unattended cron
job silently redeploying a public site is a materially different risk than
one appending to a private ledger, and this script does not make that call
for you.

Usage:
    python3 run_cycle.py --total 6                 # 6 hypotheses this cycle, split by mode_weights.json
    python3 run_cycle.py --hypotheses-per-mode 2    # exactly 2 per mode (6 total), ignoring weights
    python3 run_cycle.py --total 6 --skip-refutation
    python3 run_cycle.py --total 6 --dry-run        # print the plan, run nothing
"""
import argparse
import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
MODE_WEIGHTS_PATH = os.path.join(PIPELINE_DIR, "mode_weights.json")
CYCLE_LOG_PATH = os.path.join(PIPELINE_DIR, "cycle_log.jsonl")
HYPOTHESES_DIR = os.path.join(PIPELINE_DIR, "hypotheses")
PYTHON = sys.executable

MODES = ["bisociation", "janusian", "homospatial"]


def load_mode_weights():
    with open(MODE_WEIGHTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["weights"]


def split_total(total: int, weights: dict) -> dict:
    """Largest-remainder apportionment -- counts sum to exactly `total`,
    proportional to weights, no mode silently dropped to zero unless total
    is smaller than len(MODES)."""
    raw = {m: total * weights.get(m, 0) for m in MODES}
    floors = {m: int(raw[m]) for m in MODES}
    remainder = total - sum(floors.values())
    remainders_sorted = sorted(MODES, key=lambda m: raw[m] - floors[m], reverse=True)
    for m in remainders_sorted[:remainder]:
        floors[m] += 1
    return floors


def existing_hypothesis_files() -> set:
    return set(glob.glob(os.path.join(HYPOTHESES_DIR, "*.md")))


def run_subprocess(cmd: list, dry_run: bool) -> dict:
    """Runs one pipeline stage as a subprocess (same pattern as running it by
    hand), captures stdout/stderr/exit code. Subprocess, not import, on
    purpose -- it decouples this orchestrator from needing to track internal
    changes to the called scripts, and it's exactly how a human operator
    would run each stage manually, so `run_cycle.py`'s behavior never
    diverges from the documented manual workflow."""
    print(f"$ {' '.join(cmd)}")
    if dry_run:
        return {"cmd": cmd, "dry_run": True}
    result = subprocess.run(cmd, cwd=PIPELINE_DIR, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    return {
        "cmd": cmd,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-2000:] if result.stderr else "",
    }


def main():
    parser = argparse.ArgumentParser(description="One full autonomous Eureka Engine cycle (generate -> verify -> refute -> score)")
    parser.add_argument("--total", type=int, help="Total hypotheses this cycle, split across modes by mode_weights.json")
    parser.add_argument("--hypotheses-per-mode", type=int, help="Exact count per mode, ignoring mode_weights.json")
    parser.add_argument("--skip-refutation", action="store_true", help="Skip Phase 2.5 (adversarial refutation) this cycle")
    parser.add_argument("--skip-score", action="store_true", help="Skip regenerating leaderboard.md this cycle")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan and the commands that would run; execute nothing")
    args = parser.parse_args()

    if not args.total and not args.hypotheses_per_mode:
        raise SystemExit("Pass --total N (split by mode_weights.json) or --hypotheses-per-mode N (exact per mode).")

    if args.hypotheses_per_mode:
        counts = {m: args.hypotheses_per_mode for m in MODES}
    else:
        weights = load_mode_weights()
        counts = split_total(args.total, weights)

    total_planned = sum(counts.values())
    print(f"=== Eureka Engine cycle — {datetime.now(timezone.utc).isoformat()} ===")
    print(f"Plan: {counts} ({total_planned} total)")
    if args.dry_run:
        print("(dry run — printing commands, executing nothing)\n")

    cycle_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "plan": counts,
        "dry_run": args.dry_run,
        "stages": {},
    }

    # --- Phase 1: generation ---
    before = existing_hypothesis_files()
    for mode, count in counts.items():
        if count <= 0:
            continue
        cmd = [PYTHON, "hypothesis_engine.py", "--mode", mode, "--autonomous", "--count", str(count)]
        cycle_record["stages"].setdefault("generation", []).append(
            run_subprocess(cmd, args.dry_run)
        )
    after = existing_hypothesis_files()
    new_files = sorted(after - before)
    print(f"\nGenerated {len(new_files)} new hypothesis file(s) this cycle.")
    cycle_record["new_hypothesis_files"] = [os.path.basename(f) for f in new_files]

    # --- Phase 2: verification ---
    if not args.dry_run and new_files:
        cmd = [PYTHON, "verify_hypothesis.py", "--all-unverified"]
        cycle_record["stages"]["verification"] = run_subprocess(cmd, args.dry_run)
    elif args.dry_run:
        print(f"$ {PYTHON} verify_hypothesis.py --all-unverified")

    # --- Phase 2.5: refutation ---
    if not args.skip_refutation:
        if not args.dry_run:
            cmd = [PYTHON, "refute_hypothesis.py", "--all-no-signal"]
            cycle_record["stages"]["refutation"] = run_subprocess(cmd, args.dry_run)
        else:
            print(f"$ {PYTHON} refute_hypothesis.py --all-no-signal")
    else:
        print("(skipping refutation this cycle — --skip-refutation)")

    # --- Phase: scoring ---
    if not args.skip_score:
        if not args.dry_run:
            cmd = [PYTHON, "score_hypotheses.py"]
            cycle_record["stages"]["scoring"] = run_subprocess(cmd, args.dry_run)
        else:
            print(f"$ {PYTHON} score_hypotheses.py")

    if not args.dry_run:
        with open(CYCLE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(cycle_record) + "\n")
        print(f"\nCycle logged to {CYCLE_LOG_PATH}")

    print("=== Cycle complete ===")


if __name__ == "__main__":
    main()
