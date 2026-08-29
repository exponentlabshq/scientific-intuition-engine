#!/usr/bin/env python3
"""
audit_agent.py — the Eureka Engine's self-observation layer.

Reads the real ledger, real token-usage log, and the current scoring code;
computes real performance stats (the same class of analysis that found the
refutation-ROTI problem run_cycle.py and refute_hypothesis.py exist to fix);
asks an OpenAI model to propose exactly ONE specific, additive improvement,
grounded in that data.

HARD CONSTRAINT — enforced by this script's structure, not just prompted
for: this agent can never edit or delete an existing file in this pipeline.
It only ever WRITES NEW, timestamped files:
  - proposals/<date>-proposal-<n>.md   — the rationale, always written
  - alt_scoring/<name>.py              — a complete, standalone, runnable
                                          alternative (a new leaderboard
                                          variant, a new badge scheme, a new
                                          weighting policy), only if the
                                          model proposed one and it parses
                                          as valid Python

Nothing else in this pipeline imports or executes files under alt_scoring/
automatically — run_cycle.py does not know they exist. A proposal becomes
real only when a human reads it, runs the alternative script themselves, and
explicitly promotes whatever it changes (e.g. hand-editing mode_weights.json,
or wiring a new leaderboard variant into the published site). Same
draft-only discipline this pipeline already applies to Phase 3 researcher
outreach — an agent proposes, a person decides.

Usage:
    python3 audit_agent.py                # one proposal, based on current ledger state
    python3 audit_agent.py --dry-run      # print the proposal, write nothing
    python3 audit_agent.py --model o1     # override the reasoning model
"""
import argparse
import ast
import glob
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timezone

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_hypotheses import load_entries, score_entry
from token_tracker import load_usage, summarize_by_phase
from retry import call_with_retry

load_dotenv(find_dotenv(usecwd=False))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
PROPOSALS_DIR = os.path.join(PIPELINE_DIR, "proposals")
ALT_SCORING_DIR = os.path.join(PIPELINE_DIR, "alt_scoring")
AUDIT_LOG_PATH = os.path.join(PIPELINE_DIR, "audit_log.jsonl")
SCORE_HYPOTHESES_PATH = os.path.join(PIPELINE_DIR, "score_hypotheses.py")
MODE_WEIGHTS_PATH = os.path.join(PIPELINE_DIR, "mode_weights.json")

DEFAULT_MODEL = "gpt-4o"


def compute_real_stats() -> dict:
    """Everything an audit proposal should be grounded in, computed fresh
    from the actual ledger and actual token log — never estimated, never
    carried over from a stale prior run."""
    entries = load_entries()
    by_mode_points = defaultdict(list)
    by_mode_no_signal = defaultdict(int)
    by_verdict = defaultdict(list)
    for e in entries:
        mode = e.get("mode") or ("case-study" if e.get("source") == "rosetta-stone-case-study" else "other")
        points, badges, breakdown, held_out = score_entry(e)
        by_mode_points[mode].append(points)
        if e.get("verdict") == "NO_SIGNAL":
            by_mode_no_signal[mode] += 1
        v = e.get("verdict", "")
        refv = e.get("refutation_verdict")
        key = f"{v} -> {refv}" if refv else v
        by_verdict[key].append(points)

    mode_stats = {}
    for mode, pts in by_mode_points.items():
        n = len(pts)
        mode_stats[mode] = {
            "n": n,
            "avg_points": round(sum(pts) / n, 1) if n else 0,
            "total_points": sum(pts),
            "no_signal_rate": round(by_mode_no_signal[mode] / n, 2) if n else 0,
        }

    verdict_stats = {
        v: {"n": len(pts), "avg_points": round(sum(pts) / len(pts), 1), "total_points": sum(pts)}
        for v, pts in by_verdict.items()
    }

    token_summary = summarize_by_phase()

    return {
        "total_hypotheses": len(entries),
        "mode_stats": mode_stats,
        "verdict_stats": verdict_stats,
        "token_usage_by_phase": token_summary,
        "current_mode_weights": json.load(open(MODE_WEIGHTS_PATH)).get("weights") if os.path.exists(MODE_WEIGHTS_PATH) else None,
    }


def load_scoring_source() -> str:
    with open(SCORE_HYPOTHESES_PATH, "r", encoding="utf-8") as f:
        return f.read()


def existing_proposal_count() -> int:
    """Count only real proposal files, not proposals/README.md -- a prior
    version of this function globbed *.md unconditionally and counted the
    README as a proposal, which silently skipped a number (001, then 003,
    no 002) the first time this ran twice. Match the actual naming
    convention instead of every markdown file in the directory."""
    if not os.path.exists(PROPOSALS_DIR):
        return 0
    return len(glob.glob(os.path.join(PROPOSALS_DIR, "*-proposal-*.md")))


def build_prompt(stats: dict, scoring_source: str) -> tuple:
    system_prompt = (
        "You are the audit agent for a research-hypothesis pipeline (the Eureka Engine). Your "
        "job is to observe real, measured performance data and propose exactly ONE specific, "
        "additive improvement — never a rewrite, never a deletion, never a change to how an "
        "existing outcome is scored for hypotheses already in the ledger.\n\n"
        "You may propose ONE of:\n"
        "  (a) a new mode/domain-selection weighting policy, as a complete standalone Python "
        "script that reads verification-log.jsonl and outputs recommended weights (never edits "
        "mode_weights.json directly)\n"
        "  (b) a new alternative scoring formula or badge scheme, as a complete standalone "
        "Python script — a genuine alternative leaderboard, importable and runnable on its own, "
        "that does not modify or import score_hypotheses.py's write path\n"
        "  (c) a new pre-generation or pre-verification filter heuristic, as a complete "
        "standalone Python script\n\n"
        "Hard rules:\n"
        "- Ground every claim in the real numbers given below. Do not invent statistics. If the "
        "data doesn't support a strong claim, say so and propose something more modest instead.\n"
        "- Never propose deleting, disabling, or silently overriding an existing mechanism — "
        "your job is to add a new, separately runnable option, not replace anything.\n"
        "- If you include code, it must be complete, syntactically valid, standalone Python that "
        "does not require editing any existing file to run.\n\n"
        "Respond with ONLY a JSON object:\n"
        '{"title": "short proposal title", "rationale": "2-4 paragraphs, citing the specific '
        'numbers given below that motivate this", "risk_and_limits": "1-2 sentences on what this '
        'proposal does NOT resolve or could get wrong", "filename": "descriptive_snake_case_name.py '
        'or null if no code is warranted", "code": "the full Python source, or null"}'
    )
    user_prompt = (
        f"Real performance data, computed fresh from verification-log.jsonl and token_usage.jsonl "
        f"just before this call:\n\n{json.dumps(stats, indent=2)}\n\n"
        f"Current canonical scoring logic (score_hypotheses.py), for reference — do not propose "
        f"editing this file:\n\n{scoring_source}\n"
    )
    return system_prompt, user_prompt


def validate_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def safe_filename(name: str) -> str:
    name = re.sub(r"[^\w\-.]", "_", name)
    if not name.endswith(".py"):
        name += ".py"
    return name


def write_proposal(stats: dict, proposal: dict, dry_run: bool) -> tuple:
    today = date.today().isoformat()
    n = existing_proposal_count() + 1
    proposal_path = os.path.join(PROPOSALS_DIR, f"{today}-proposal-{n:03d}.md")

    code = proposal.get("code")
    filename = proposal.get("filename")
    code_path = None
    code_status = "not proposed"

    if code and filename:
        if validate_python(code):
            code_path = os.path.join(ALT_SCORING_DIR, safe_filename(filename))
            # Never overwrite — if a name collision happens, append a numeric suffix.
            base, ext = os.path.splitext(code_path)
            i = 2
            while os.path.exists(code_path):
                code_path = f"{base}_v{i}{ext}"
                i += 1
            code_status = f"written to alt_scoring/{os.path.basename(code_path)}"
        else:
            code_status = "REJECTED — proposed code failed ast.parse() syntax validation, not written"
            code_path = None

    proposal_md = f"""# Audit Proposal {n:03d} — {proposal.get('title', 'Untitled')}

**Date**: {today} · **Generated by**: `audit_agent.py` · **Status**: unreviewed — awaiting human sign-off

## Rationale

{proposal.get('rationale', '(none given)')}

## Risks and limits (self-reported by the agent)

{proposal.get('risk_and_limits', '(none given)')}

## Code

{code_status}{f" — see `alt_scoring/{os.path.basename(code_path)}`" if code_path else ""}

## Data this proposal was grounded in

```json
{json.dumps(stats, indent=2)}
```

## Promotion checklist (manual — nothing below happens automatically)

- [ ] A human read this proposal and the data above
- [ ] If code was written, a human ran it standalone and reviewed the output
- [ ] If adopted, the relevant canonical file (e.g. `mode_weights.json`) was hand-edited to reflect it — this proposal file and any `alt_scoring/` script are never auto-wired into the live pipeline
"""

    if dry_run:
        print(proposal_md)
        if code and filename:
            print(f"\n--- would write code to alt_scoring/{safe_filename(filename)} ---\n")
            print(code)
        return None, code_path

    os.makedirs(PROPOSALS_DIR, exist_ok=True)
    with open(proposal_path, "w", encoding="utf-8") as f:
        f.write(proposal_md)

    if code_path:
        os.makedirs(ALT_SCORING_DIR, exist_ok=True)
        header = (
            f'"""\nEXPERIMENTAL -- proposed by audit_agent.py on {today}.\n'
            f"NOT wired into the canonical leaderboard or any pipeline stage.\n"
            f"Human review required before promotion. See proposals/{os.path.basename(proposal_path)}\n"
            f'for the full rationale this was grounded in.\n\nRun standalone:\n'
            f'    python3 alt_scoring/{os.path.basename(code_path)}\n"""\n\n'
        )
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(header + code)

    return proposal_path, code_path


def run_audit(model: str, dry_run: bool):
    stats = compute_real_stats()
    scoring_source = load_scoring_source()
    system_prompt, user_prompt = build_prompt(stats, scoring_source)

    resp = call_with_retry(
        client.chat.completions.create,
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        response_format={"type": "json_object"},
    )
    from token_tracker import log_usage
    log_usage("audit", model, resp.usage)

    proposal = json.loads(resp.choices[0].message.content)
    proposal_path, code_path = write_proposal(stats, proposal, dry_run)

    if not dry_run:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "title": proposal.get("title"),
                "proposal_file": os.path.basename(proposal_path) if proposal_path else None,
                "code_file": os.path.basename(code_path) if code_path else None,
                "stats_snapshot": stats,
            }) + "\n")
        print(f"Wrote proposal: {proposal_path}")
        if code_path:
            print(f"Wrote alternative: {code_path}")
        else:
            print("No code proposed this run (or it failed validation) — rationale-only proposal.")

    return proposal, proposal_path, code_path


def main():
    parser = argparse.ArgumentParser(description="Eureka Engine self-audit — one grounded, additive proposal per run")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="OpenAI model to use for the audit reasoning")
    parser.add_argument("--dry-run", action="store_true", help="Print the proposal; write nothing to disk")
    args = parser.parse_args()
    run_audit(args.model, args.dry_run)


if __name__ == "__main__":
    main()
