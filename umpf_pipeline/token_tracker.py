"""
token_tracker.py — real ROTI (return-on-token-investment) measurement.

Before this file existed, nothing in the Eureka Engine logged OpenAI token
usage anywhere. Every "tokens per point" estimate produced during the
2026-08-29 ROTI audit was a defensible estimate, not a measurement (with one
real exception: Claude subagent refutation calls, which report their own
usage). This module is the fix: one shared, tiny helper that every OpenAI
call site in the pipeline calls right after receiving a response, appending
one line to token_usage.jsonl. That file is the actual substrate real ROTI
analysis (and audit_agent.py's proposals) run against going forward.

Not append-only by policy alone -- log_usage() only ever appends; nothing in
this pipeline reads token_usage.jsonl expecting to rewrite it.
"""
import json
import os
from datetime import datetime, timezone

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
USAGE_LOG_PATH = os.path.join(PIPELINE_DIR, "token_usage.jsonl")


def log_usage(phase: str, model: str, usage, hypothesis_slug: str = None, extra: dict = None) -> None:
    """Append one usage record. `usage` is an OpenAI response's `.usage`
    object (has .prompt_tokens, .completion_tokens, .total_tokens) -- pass
    it straight through, we don't reshape it. `phase` is one of
    'generation' | 'verification' | 'refutation' | 'audit' so downstream
    analysis can group by pipeline stage, which is the whole point (the
    2026-08-29 audit's central finding -- refutation costs ~15x what
    verification does per call -- is exactly the kind of thing this field
    makes queryable instead of estimated)."""
    if usage is None:
        return  # some SDK paths (e.g. a retried call) may not carry usage; don't crash the caller over it
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": phase,
        "model": model,
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
    }
    if hypothesis_slug:
        record["hypothesis_slug"] = hypothesis_slug
    if extra:
        record.update(extra)
    with open(USAGE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def load_usage():
    """All logged records, oldest first. Returns [] if the log doesn't exist yet."""
    if not os.path.exists(USAGE_LOG_PATH):
        return []
    records = []
    with open(USAGE_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def summarize_by_phase(records=None):
    """{phase: {"n_calls": int, "total_tokens": int, "avg_tokens": float}} --
    the exact aggregation the ROTI audit did by hand from real subagent
    numbers; now computable from real measured data for every phase."""
    if records is None:
        records = load_usage()
    from collections import defaultdict
    agg = defaultdict(lambda: {"n_calls": 0, "total_tokens": 0})
    for r in records:
        p = r.get("phase", "unknown")
        agg[p]["n_calls"] += 1
        agg[p]["total_tokens"] += r.get("total_tokens") or 0
    out = {}
    for phase, d in agg.items():
        out[phase] = {
            "n_calls": d["n_calls"],
            "total_tokens": d["total_tokens"],
            "avg_tokens": (d["total_tokens"] / d["n_calls"]) if d["n_calls"] else 0,
        }
    return out


if __name__ == "__main__":
    summary = summarize_by_phase()
    if not summary:
        print("No usage logged yet.")
    else:
        print(f"{'Phase':15s} {'n_calls':>8s} {'total_tokens':>14s} {'avg_tokens':>12s}")
        for phase, d in sorted(summary.items()):
            print(f"{phase:15s} {d['n_calls']:>8d} {d['total_tokens']:>14d} {d['avg_tokens']:>12.0f}")
