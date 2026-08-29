#!/bin/bash
# run_cycle_scheduled.sh — the missing piece named directly by the 2026-08-29
# readiness audit (gating item #2: "Nothing schedules the engine yet. Every
# real cycle to date was started by a human typing the command."). run_cycle.py
# was already written to be pointed at by cron -- its own docstring says so --
# but nothing ever actually pointed anything at it. This script is that thing:
# a thin, defensive wrapper that a real scheduler (cron or launchd) calls,
# which then calls run_cycle.py and preserves its exit-code contract for
# whatever's watching (mail-on-error from cron, a launchd StandardErrorPath,
# a human checking `echo $?` after the fact).
#
# This script does NOT install itself into cron or launchd. Registering a
# recurring job that spends real OpenAI API budget and pushes to a public
# GitHub repo on its own, unattended, on a timer, is a standing/persistent
# configuration change -- deliberately left as a manual step for a human to
# take deliberately, not something a script silently sets up for itself.
# See the crontab/launchd snippets at the bottom of this file to actually
# install it.
#
# Usage (manual test, exactly what a scheduler would run):
#   ./run_cycle_scheduled.sh [--total N] [any other run_cycle.py flag]
#
# What it does beyond `python3 run_cycle.py`:
#   1. Resolves its own real path so it works no matter what directory cron
#      invokes it from (cron's default cwd is $HOME, not this repo).
#   2. Writes stdout+stderr to a timestamped file under scheduler_logs/ AND
#      still prints to stdout, so both a human tailing the log and a cron
#      mail-on-error capture see the same thing.
#   3. Preserves run_cycle.py's real exit code as its own -- 0 on a clean
#      cycle, 1 on DEGRADED or failed, exactly as run_cycle.py already
#      defines it. This script adds logging; it does not change the contract.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

PYTHON3="${EUREKA_PYTHON3:-/Library/Frameworks/Python.framework/Versions/3.12/bin/python3}"
mkdir -p scheduler_logs
TIMESTAMP="$(date -u '+%Y-%m-%dT%H-%M-%SZ')"
LOG_FILE="scheduler_logs/${TIMESTAMP}.log"

echo "=== run_cycle_scheduled.sh starting at ${TIMESTAMP} (UTC) ===" | tee "$LOG_FILE"
"$PYTHON3" run_cycle.py "$@" 2>&1 | tee -a "$LOG_FILE"
EXIT_CODE="${PIPESTATUS[0]}"

echo "=== run_cycle_scheduled.sh finished at $(date -u '+%Y-%m-%dT%H-%M-%SZ') (UTC) -- exit ${EXIT_CODE} ===" | tee -a "$LOG_FILE"
exit "$EXIT_CODE"

# ---------------------------------------------------------------------------
# To actually install this on a schedule (NOT done automatically -- a human
# decision, made deliberately, per the standing-configuration rule above):
#
# crontab (e.g. every 6 hours):
#   0 */6 * * * /Users/michaeljagdeo/Downloads/talentOS-2026/scientific-intuition-engine/umpf_pipeline/run_cycle_scheduled.sh --total 4 >> /tmp/eureka_cron.log 2>&1
#
# launchd (macOS-native, survives reboots better than cron): create
# ~/Library/LaunchAgents/com.exponentlabs.eureka-engine.plist pointing its
# ProgramArguments at this script's absolute path, with a StartInterval (in
# seconds) or a StartCalendarInterval, then:
#   launchctl load ~/Library/LaunchAgents/com.exponentlabs.eureka-engine.plist
# ---------------------------------------------------------------------------
