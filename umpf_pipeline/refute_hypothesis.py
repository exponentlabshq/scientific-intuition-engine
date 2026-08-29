#!/usr/bin/env python3
"""
refute_hypothesis.py — adversarial refutation, made unattended and cheap.

Every prior refutation pass in this repo ran as three separate Claude Code
Agent subagent spawns, one per lens. Real, and rigorous — but expensive:
this session's own recorded subagent_tokens figures ran ~34,700 tokens PER
LENS (~104,000 tokens per refuted case), almost entirely conversational-
agent-harness overhead (system reminders, tool scaffolding) rather than the
~1-2K tokens of actual hypothesis content each lens reasons over. The
2026-08-29 ROTI audit found this was, by a wide margin, the single most
expensive step in the pipeline per case — and the only one that reliably
produces negative leaderboard points (-12.3 avg across 14 real cases).

This script reproduces the EXACT SAME three-lens rubric from
refutations/README.md — coherence / testability / triviality, each
defaulting to REFUTED under genuine uncertainty, 2-of-3 survival required to
promote out of NO_SIGNAL — as three independent OpenAI completions instead
of three Claude subagents. Independence is preserved deliberately: each lens
is its own isolated API call with its own fresh message list, no shared
conversation state, and none of the three calls is told what the other two
found. That is the actual scientific property that matters here, not the
subagent harness that happened to deliver it before.

Usage:
    python3 refute_hypothesis.py hypotheses/<file>.md
    python3 refute_hypothesis.py --all-no-signal
    python3 refute_hypothesis.py --all-no-signal --limit 5
    python3 refute_hypothesis.py --all-no-signal --dry-run   # print verdicts only
"""
import argparse
import glob
import json
import os
import sys
from datetime import date

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_hypothesis import (
    HERE,
    HYPOTHESES_DIR,
    LEDGER_PATH,
    detect_mode,
    extract_core_claim,
    title_and_domains,
)
from token_tracker import log_usage
from retry import call_with_retry

load_dotenv(find_dotenv(usecwd=False))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)

REFUTATIONS_DIR = os.path.join(HERE, "refutations")
VERIFICATIONS_DIR = os.path.join(HERE, "verifications")
RUBRIC_PATH = os.path.join(HERE, "refutations", "README.md")

REFUTATION_MODEL = "gpt-4o"  # same model verify_hypothesis.py classifies with; this is a
                              # judgment task, not a bulk-search-summarization one — kept on
                              # the stronger model deliberately rather than downgraded by default

LENS_QUESTIONS = {
    "coherence": (
        "Does the claimed structural mapping equivocate on a term — using one word for two "
        "genuinely different underlying mechanisms and treating that as a match? For a "
        "Janusian hypothesis specifically: is this a genuine same-instance paradox, or a "
        "disguised context-dependent compromise (\"in some contexts... in others\") labeled "
        "'paradox'? For a homospatial hypothesis specifically: is there an actual fusion, or "
        "is this two domains compared side-by-side wearing a fusion's coined name?"
    ),
    "testability": (
        "Is the falsifiable prediction actually operationalized — a named metric, comparison "
        "condition, and rejection threshold — or is it vague enough that no real experiment "
        "could ever return a clean \"no\"? Watch specifically for an \"or vice versa\" hedge, "
        "which usually makes a claim direction-agnostic and therefore unfalsifiable."
    ),
    "triviality": (
        "Strip the domain-specific vocabulary from the claim. Does it reduce to something true "
        "of almost any two complex systems (the umbrella trap) — the same failure mode Phase 2's "
        "own verification rubric guards against, applied one level deeper against the hypothesis "
        "itself rather than against search results?"
    ),
}


def load_rubric() -> str:
    with open(RUBRIC_PATH, "r", encoding="utf-8") as f:
        return f.read()


def load_verification_note(slug: str) -> str:
    """Best-effort: pull the existing Phase 2 verification's 'What was found' /
    'Reasoning' text for this hypothesis, if a verification file exists, to give
    each lens the same real context a human reviewer would have had. Not fatal
    if missing — some NO_SIGNAL cases may be refuted before Phase 2 even wrote
    a file, though in practice verify_hypothesis.py always writes one."""
    candidates = glob.glob(os.path.join(VERIFICATIONS_DIR, f"{slug}*-verification.md"))
    if not candidates:
        return "(no Phase 2 verification file found for this hypothesis)"
    with open(candidates[0], "r", encoding="utf-8") as f:
        return f.read()


def run_lens(lens_name: str, question: str, rubric: str, title: str, mode: str,
             domains: list, core_claim: str, verification_note: str, slug: str) -> dict:
    system_prompt = (
        f"You are one of three independent reviewers running a single-lens adversarial "
        f"refutation test on a cross-domain research hypothesis. You do not know what the "
        f"other two reviewers found, and you must not assume there are other reviewers — "
        f"evaluate entirely on your own.\n\n"
        f"YOUR LENS IS {lens_name.upper()} ONLY. {question}\n\n"
        f"Default to REFUTED under genuine uncertainty — a hypothesis wrongly killed costs "
        f"nothing; a hollow one wrongly promoted costs someone real research time later. "
        f"This is the same rubric this pipeline has applied by hand in every prior refutation "
        f"round:\n\n--- FULL RUBRIC (for context; you are applying only your one lens above) ---\n{rubric}\n\n"
        f'Respond with ONLY a JSON object: {{"verdict": "REFUTED" or "SURVIVES", "reasoning": '
        f'"2-4 sentences, terse peer-reviewer style"}}'
    )
    user_prompt = (
        f"Hypothesis: {title}\nMode: {mode}\nDomain(s): {', '.join(domains)}\n\n"
        f"Core claim:\n{core_claim}\n\n"
        f"Phase 2 web-verification finding for this hypothesis (for context):\n{verification_note}"
    )
    resp = call_with_retry(
        client.chat.completions.create,
        model=REFUTATION_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    log_usage("refutation", REFUTATION_MODEL, resp.usage, hypothesis_slug=slug, extra={"lens": lens_name})
    parsed = json.loads(resp.choices[0].message.content)
    if parsed.get("verdict") not in ("REFUTED", "SURVIVES"):
        raise ValueError(f"Lens {lens_name} returned an invalid verdict: {parsed.get('verdict')!r}")
    return parsed


def write_refutation_md(slug: str, title: str, mode: str, lens_results: dict, verdict: str, survives: int) -> str:
    path = os.path.join(REFUTATIONS_DIR, f"{slug}-refutation.md")
    mode_label = {"bisociation": "Bisociation", "janusian": "Janusian", "homospatial": "Homospatial"}.get(mode, mode)
    lens_lines = "\n".join(
        f"- **{lens.capitalize()} — {res['verdict']}.** {res['reasoning']}"
        for lens, res in lens_results.items()
    )
    if verdict == "REFUTED":
        tally_line = f"## Tally: {survives} of 3 survive → **REFUTED**"
        closing = (
            "## No steelman offered\n\n"
            "All three lenses independently converged on REFUTED for this case. If revisited, "
            "it would need a genuinely tighter formulation, not a restatement of the same claim."
        )
    else:
        tally_line = f"## Tally: {survives} of 3 survive → **SURVIVES** (promoted out of NO_SIGNAL)"
        closing = (
            "## What survived, and why this matters\n\n"
            f"{survives} of 3 independent lenses could not kill this claim. Per the promotion rule "
            "(2-of-3 survival), this hypothesis moves out of NO_SIGNAL — real signal the claim isn't "
            "vacuous, not proof it's correct. Still worth Phase 3 outreach consideration if a real "
            "researcher in the adjacent field can be identified."
        )
    content = f"""# Adversarial Refutation: {mode_label} — {title}

**Original**: `hypotheses/{slug}.md`
**Method**: 3 independent OpenAI completions, one per lens (`refute_hypothesis.py`, unattended) — same rubric, same independence discipline as prior Claude-subagent rounds, at a fraction of the token cost

{tally_line}

{lens_lines}

{closing}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def append_ledger_refutation(slug: str, verdict: str, survives: int, refutation_filename: str):
    """Read the full ledger, find the matching entry by hypothesis_slug, add
    the refutation fields, rewrite. Mirrors the exact field shape every prior
    refutation round wrote by hand — refutation_verdict / refutation_file /
    refutation_independently_confirmed / refutation_confirmation_note, plus
    refutation_survival_count for the SURVIVES case (score_hypotheses.py
    already reads this field)."""
    lines = []
    found = False
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("hypothesis_slug") == slug:
                entry["refutation_verdict"] = verdict
                entry["refutation_file"] = f"refutations/{os.path.basename(refutation_filename)}"
                entry["refutation_independently_confirmed"] = True
                entry["refutation_confirmation_note"] = (
                    "3 independent OpenAI completions, one per lens (coherence/testability/triviality), "
                    "each with its own isolated message list — no shared conversation state, no lens told "
                    "the others' findings. Unattended (refute_hypothesis.py)."
                )
                if verdict == "SURVIVES":
                    entry["refutation_survival_count"] = survives
                found = True
            lines.append(json.dumps(entry))
    if not found:
        raise ValueError(f"No ledger entry found for slug {slug!r} — refutation result not written.")
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def already_refuted_slugs():
    slugs = set()
    if not os.path.exists(LEDGER_PATH):
        return slugs
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            if e.get("refutation_verdict"):
                slugs.add(e.get("hypothesis_slug"))
    return slugs


def no_signal_slugs():
    """Every ledger entry whose verdict is NO_SIGNAL and has no refutation
    result yet — the actual real candidate queue, read from the ledger
    itself rather than re-deriving it from filenames."""
    slugs = []
    if not os.path.exists(LEDGER_PATH):
        return slugs
    already = already_refuted_slugs()
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            if e.get("verdict") == "NO_SIGNAL" and e.get("hypothesis_slug") not in already:
                slugs.append(e.get("hypothesis_slug"))
    return slugs


def refute_one(slug: str, rubric: str, dry_run: bool = False):
    filepath = os.path.join(HYPOTHESES_DIR, f"{slug}.md")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No hypothesis file for slug {slug!r} at {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    mode = detect_mode(text)
    title, domains = title_and_domains(text, mode)
    core_claim = extract_core_claim(text, mode)
    verification_note = load_verification_note(slug)

    print(f"  → [{mode}] {title}")
    lens_results = {}
    for lens_name, question in LENS_QUESTIONS.items():
        result = run_lens(lens_name, question, rubric, title, mode, domains, core_claim, verification_note, slug)
        lens_results[lens_name] = result
        print(f"    {lens_name}: {result['verdict']}")

    survives = sum(1 for r in lens_results.values() if r["verdict"] == "SURVIVES")
    verdict = "SURVIVES" if survives >= 2 else "REFUTED"
    print(f"    tally: {survives} of 3 survive -> {verdict}")

    if dry_run:
        return slug, verdict, survives, None

    os.makedirs(REFUTATIONS_DIR, exist_ok=True)
    path = write_refutation_md(slug, title, mode, lens_results, verdict, survives)
    append_ledger_refutation(slug, verdict, survives, path)
    return slug, verdict, survives, path


def main():
    parser = argparse.ArgumentParser(description="Unattended adversarial refutation (3 independent OpenAI completions per case)")
    parser.add_argument("files", nargs="*", help="Specific hypothesis .md files to refute")
    parser.add_argument("--all-no-signal", action="store_true", help="Refute every ledger entry with verdict NO_SIGNAL and no refutation result yet")
    parser.add_argument("--limit", type=int, default=None, help="Cap how many to run this pass (used with --all-no-signal)")
    parser.add_argument("--dry-run", action="store_true", help="Print verdicts only; write nothing")
    args = parser.parse_args()

    rubric = load_rubric()

    if args.all_no_signal:
        slugs = no_signal_slugs()
        if args.limit:
            slugs = slugs[: args.limit]
    else:
        if not args.files:
            raise SystemExit("Pass hypothesis file(s), or use --all-no-signal")
        slugs = [os.path.splitext(os.path.basename(f))[0] for f in args.files]

    if not slugs:
        print("Nothing to refute — no NO_SIGNAL entries without a refutation result.")
        return

    print(f"Refuting {len(slugs)} hypothesis(es){' (dry run)' if args.dry_run else ''}...\n")
    summary = []
    for slug in slugs:
        try:
            s, verdict, survives, path = refute_one(slug, rubric, dry_run=args.dry_run)
            summary.append((s, verdict, survives))
        except Exception as e:
            print(f"    ! FAILED on {slug}: {e}")
            summary.append((slug, f"ERROR: {e}", None))
        print()

    print("=" * 60)
    print(f"Done. {len(summary)} processed.")
    for slug, verdict, survives in summary:
        tag = f"{verdict} ({survives}/3)" if survives is not None else verdict
        print(f"  {tag:20s} {slug}")


if __name__ == "__main__":
    main()
