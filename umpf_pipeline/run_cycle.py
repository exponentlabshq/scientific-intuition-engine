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

Update (2026-08-29): the final stage now also calls publish_site.py, which
regenerates and deploys the site's data-driven pages -- the interactive
leaderboard experience (a pure data render, always safe to automate) and
landing.html's stat fields (templated, everything else on that page is
untouched hand-written content). whitepaper.html is deliberately excluded
from that automation -- see publish_site.py's own docstring for why. Pass
--skip-publish to opt a cycle out of touching the site at all, or --no-push
to build + commit locally without pushing.

Update (2026-08-29) — fail-closed on publish. A verification audit found
this script logged a failed stage's stderr but otherwise treated it as a
no-op and continued straight through to publish anyway -- a fully failed
generation stage could still end in a "successful" cycle that pushed a
site update reflecting nothing new, with no signal anywhere that anything
had gone wrong. Fixed: any stage returning nonzero now marks the cycle
DEGRADED, and publish is skipped entirely once that's true (scoring still
runs against whatever's really in the ledger -- that's always safe, the
ledger is append-only). The script now exits 1 on a degraded or failed
cycle and 0 on a clean one, so a cron wrapper (or just `echo $?`) has an
honest signal to act on -- this script does not send notifications itself,
it makes sure the exit code and cycle_log.jsonl are trustworthy for
whatever does.

Update (2026-08-29) — dashboard. A new lightweight "observe" stage runs
`audit_agent.py --observe` every cycle (cheap, ~1K tokens on gpt-4o-mini,
not the full proposal-with-code mode) before publish, so
publish_site.py's dashboard.html rebuild picks up a fresh, grounded
observation each time rather than replaying the last one.

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


def failed(result) -> bool:
    """A stage's run_subprocess() result, or a list of them (generation runs
    one subprocess per mode) -- True if any real (non-dry-run) call in it
    returned nonzero."""
    if result is None:
        return False
    results = result if isinstance(result, list) else [result]
    return any(r.get("returncode", 0) != 0 for r in results if not r.get("dry_run"))


def main():
    parser = argparse.ArgumentParser(description="One full autonomous Eureka Engine cycle (generate -> verify -> refute -> score)")
    parser.add_argument("--total", type=int, help="Total hypotheses this cycle, split across modes by mode_weights.json")
    parser.add_argument("--hypotheses-per-mode", type=int, help="Exact count per mode, ignoring mode_weights.json")
    parser.add_argument("--skip-refutation", action="store_true", help="Skip Phase 2.5 (adversarial refutation) this cycle")
    parser.add_argument("--skip-score", action="store_true", help="Skip regenerating leaderboard.md this cycle")
    parser.add_argument("--skip-publish", action="store_true", help="Skip regenerating/deploying the site's data-driven pages this cycle")
    parser.add_argument("--no-push", action="store_true", help="Publish and commit the site locally but don't git push (passed through to publish_site.py)")
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
    degraded_reasons = []

    # --- Phase 1: generation ---
    before = existing_hypothesis_files()
    for mode, count in counts.items():
        if count <= 0:
            continue
        cmd = [PYTHON, "hypothesis_engine.py", "--mode", mode, "--autonomous", "--count", str(count)]
        cycle_record["stages"].setdefault("generation", []).append(
            run_subprocess(cmd, args.dry_run)
        )
    if failed(cycle_record["stages"].get("generation")):
        degraded_reasons.append("generation: at least one mode's subprocess failed")

    after = existing_hypothesis_files()
    new_files = sorted(after - before)
    print(f"\nGenerated {len(new_files)} new hypothesis file(s) this cycle.")
    cycle_record["new_hypothesis_files"] = [os.path.basename(f) for f in new_files]

    # --- Phase 2: verification ---
    if not args.dry_run and new_files:
        cmd = [PYTHON, "verify_hypothesis.py", "--all-unverified"]
        cycle_record["stages"]["verification"] = run_subprocess(cmd, args.dry_run)
        if failed(cycle_record["stages"]["verification"]):
            degraded_reasons.append("verification failed")
    elif args.dry_run:
        print(f"$ {PYTHON} verify_hypothesis.py --all-unverified")

    # --- Phase 2.5: refutation ---
    if not args.skip_refutation:
        if not args.dry_run:
            cmd = [PYTHON, "refute_hypothesis.py", "--all-no-signal"]
            cycle_record["stages"]["refutation"] = run_subprocess(cmd, args.dry_run)
            if failed(cycle_record["stages"]["refutation"]):
                degraded_reasons.append("refutation failed")
        else:
            print(f"$ {PYTHON} refute_hypothesis.py --all-no-signal")
    else:
        print("(skipping refutation this cycle — --skip-refutation)")

    # --- Phase: scoring --- always attempted even if an earlier stage
    # degraded (the ledger is append-only, rescoring whatever's really in
    # it is always safe) -- but a scoring failure itself is also a reason
    # to withhold publish, added below.
    if not args.skip_score:
        if not args.dry_run:
            cmd = [PYTHON, "score_hypotheses.py"]
            cycle_record["stages"]["scoring"] = run_subprocess(cmd, args.dry_run)
            if failed(cycle_record["stages"]["scoring"]):
                degraded_reasons.append("scoring failed")
        else:
            print(f"$ {PYTHON} score_hypotheses.py")

    # --- Observe: cheap, per-cycle audit commentary for the dashboard ---
    # Not gated on prior stages, and its own failure never blocks publish --
    # this is a non-critical commentary feed, not core pipeline integrity.
    # Runs before publish so the dashboard rebuild below picks up the fresh
    # observation, not last cycle's.
    if not args.dry_run:
        cmd = [PYTHON, "audit_agent.py", "--observe"]
        cycle_record["stages"]["observe"] = run_subprocess(cmd, args.dry_run)
    else:
        print(f"$ {PYTHON} audit_agent.py --observe")

    # --- Publish: regenerate + deploy the site's data-driven pages ---
    # Fail-closed: skipped entirely if anything upstream degraded, so a
    # partial or broken cycle never pushes a "successful-looking" site
    # update. Scoring still ran above regardless -- only publish is gated.
    if degraded_reasons:
        print(f"\n⚠️  Cycle degraded ({'; '.join(degraded_reasons)}) — skipping publish.")
    elif not args.skip_publish:
        if not args.dry_run:
            cmd = [PYTHON, "publish_site.py"] + (["--no-push"] if args.no_push else [])
            cycle_record["stages"]["publish"] = run_subprocess(cmd, args.dry_run)
            if failed(cycle_record["stages"]["publish"]):
                degraded_reasons.append("publish failed")
        else:
            print(f"$ {PYTHON} publish_site.py" + (" --no-push" if args.no_push else ""))
    else:
        print("(skipping publish this cycle — --skip-publish)")

    cycle_record["status"] = "degraded" if degraded_reasons else "success"
    cycle_record["degraded_reasons"] = degraded_reasons

    if not args.dry_run:
        with open(CYCLE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(cycle_record) + "\n")
        print(f"\nCycle logged to {CYCLE_LOG_PATH} — status: {cycle_record['status']}")

    if degraded_reasons:
        print(f"=== Cycle DEGRADED: {'; '.join(degraded_reasons)} ===")
        sys.exit(1)
    print("=== Cycle complete ===")


if __name__ == "__main__":
    main()
