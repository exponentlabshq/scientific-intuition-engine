#!/usr/bin/env python3
"""
structural_correspondence_observe.py -- Phase 1.5 triage, observe-only.

prefilter_observe.py already explicitly skips formalism-shaped pairs "by
design, not by oversight" (its own comment, 2026-08-30): the composability
pre-filter (chain_dialectic.py) is measured to fail more than half the time
on this category, including on exact, rigorously true connections (Shannon
entropy/thermodynamic entropy, Hopfield/Ising) -- running it there risks
logging a misleadingly negative signal against a real candidate. That left
formalism-shaped pairs with NO real triage signal at all.

2026-08-31 finding (structural-correspondence-framework.md, tested for real
against 47 Janusian entries plus a 31-entry cross-mode sample): a different
methodology -- category-theoretic composite-checking (state the triad,
compute both composites, test F(g.f)=F(g).F(f), diagnose via a five-way
outcome taxonomy) -- finds real signal specifically on formalism-shaped
pairs: 3 of 11 (27.3%) STRONG, against 0 of 20 on narrative-shaped and
mixed-uncertain pairs sampled the same way. That's the exact category the
existing pre-filter explicitly declined to touch.

This script targets exactly that gap: every real slug prefilter-log.jsonl
already marked status="skipped_formalism_shaped_by_design", runs the
structural-correspondence checklist against it, and logs the result to its
OWN separate file, structural-correspondence-log.jsonl.

Does NOT touch verification-log.jsonl, ledger.py, domains.json, or
score_hypotheses.py. Does NOT change which candidate gets generated,
verified, refuted, or scored, and does not write anything back into
prefilter-log.jsonl either -- a third, independent, purely additive log,
joinable by slug against either existing log whenever someone wants to
look, exactly the same shape of safety prefilter_observe.py itself already
established and this project has already run in production.

Deliberately FAIL-OPEN, not fail-closed, matching prefilter_observe.py's
own precedent: this is non-critical observational commentary. Its failure
must never mark a cycle DEGRADED or block generation, verification,
refutation, scoring, or publish. Every real error is still logged, not
swallowed -- just never allowed to propagate into cycle status.

Usage:
    python3 structural_correspondence_observe.py --all-unobserved
    python3 structural_correspondence_observe.py <slug> [<slug> ...]
"""
import argparse
import json
import os
import re
from datetime import datetime, timezone

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
HYPOTHESES_DIR = os.path.join(PIPELINE_DIR, "hypotheses")
PREFILTER_LOG_PATH = os.path.join(PIPELINE_DIR, "prefilter-log.jsonl")
LOG_PATH = os.path.join(PIPELINE_DIR, "structural-correspondence-log.jsonl")
FRAMEWORK_PATH = os.path.join(
    os.path.dirname(PIPELINE_DIR), "structural-correspondence-framework.md"
)

MODEL = "o4-mini"

load_dotenv(find_dotenv(usecwd=False))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)


def load_framework() -> str:
    with open(FRAMEWORK_PATH, "r", encoding="utf-8") as f:
        return f.read()


def formalism_shaped_slugs() -> list:
    """Real slugs prefilter_observe.py already marked formalism-shaped and
    explicitly skipped -- read directly from its own log, not re-derived,
    so this stays a true join against that existing signal rather than a
    second, possibly-drifting classification."""
    if not os.path.exists(PREFILTER_LOG_PATH):
        return []
    slugs, seen = [], set()
    with open(PREFILTER_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("status") == "skipped_formalism_shaped_by_design":
                slug = rec.get("slug")
                if slug and slug not in seen:
                    seen.add(slug)
                    slugs.append(slug)
    return slugs


def already_observed_slugs() -> set:
    if not os.path.exists(LOG_PATH):
        return set()
    slugs = set()
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                slugs.add(json.loads(line).get("slug"))
            except json.JSONDecodeError:
                continue
    return slugs


def append_log(record: dict):
    record["observe_only"] = True
    record["gates_nothing"] = True
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def detect_mode(text: str) -> str:
    first_line = text.splitlines()[0].strip()
    if first_line.startswith("# Homospatial Hypothesis:"):
        return "homospatial"
    if first_line.startswith("# Janusian Hypothesis:"):
        return "janusian"
    return "bisociation"


def extract_content(mode: str, text: str):
    if mode == "bisociation":
        m3 = re.search(r"## 3\..*?\n(.*?)\n## 4\.", text, re.DOTALL)
        m4 = re.search(r"## 4\..*?\n(.*?)\n## 5\.", text, re.DOTALL)
        return (m3.group(1).strip() if m3 else ""), (m4.group(1).strip() if m4 else "")
    # homospatial (the only other mode with two real domains -- Janusian is
    # single-domain and never appears in prefilter-log.jsonl's pair_type
    # records at all, so it can't reach this function via the real join)
    m2 = re.search(r"## 2\..*?\n(.*?)\n## 3\.", text, re.DOTALL)
    m3 = re.search(r"## 3\..*?\n(.*?)\n## 4\.", text, re.DOTALL)
    m4 = re.search(r"## 4\..*?\n(.*?)\n## 5\.", text, re.DOTALL)
    combined = (m2.group(1).strip() if m2 else "") + "\n\n" + (m3.group(1).strip() if m3 else "")
    return combined, (m4.group(1).strip() if m4 else "")


SYSTEM_PROMPT_TEMPLATE = (
    "You are applying the structural-correspondence framework below (a real, "
    "validated methodology for testing cross-domain analogies via category "
    "theory) to one real hypothesis from the Eureka Engine. Judge it fresh "
    "and honestly.\n\n"
    "1. State the real triad(s) this hypothesis's own content supports "
    "(x->y->z in each domain, or as close as the real content allows). If no "
    "genuine triad exists, say so.\n"
    "2. Attempt to compute a concrete composite (units, functional form, or "
    "explicit qualitative behavior -- not just prose). If you cannot, say so.\n"
    "3. Diagnose the outcome using the framework's five-way taxonomy: "
    "isomorphism / homomorphism-with-residual / restriction-repair / "
    "enrichment-repair / common-third-category / genuine failure (name the "
    "level it broke at).\n"
    "4. FIRST LINE must be exactly one of: STRONG (the composite check "
    "produces something genuinely more specific/actionable than the "
    "hypothesis's own stated prediction) / WEAK (adds nothing beyond the "
    "original) / MIXED. Then explain briefly.\n"
    "Be honest -- most entries will likely be WEAK; a genuine STRONG finding "
    "should be rare and specific.\n\n"
    "--- FRAMEWORK ---\n{framework}"
)


def observe_one(slug: str, framework: str) -> dict:
    base_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "slug": slug,
    }
    filepath = os.path.join(HYPOTHESES_DIR, f"{slug}.md")
    try:
        if not os.path.exists(filepath):
            base_record["status"] = "error"
            base_record["error"] = "hypothesis file not found"
            append_log(base_record)
            return base_record

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        mode = detect_mode(text)
        base_record["mode"] = mode

        core_content, prediction = extract_content(mode, text)
        input_text = (
            f"=== MODE ===\n{mode}\n\n"
            f"=== CORE CONTENT ===\n{core_content}\n\n"
            f"=== HYPOTHESIS/PREDICTION ===\n{prediction}\n\n"
            "=== CONTEXT ===\npair_type (pre-existing classification): formalism-shaped"
        )
        resp = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT_TEMPLATE.format(framework=framework),
            input=input_text,
            reasoning={"effort": "high"},
        )
        content = resp.output_text
        first_line = content.strip().split("\n", 1)[0] if content.strip() else ""
        verdict = "STRONG" if "STRONG" in first_line.upper() else (
            "MIXED" if "MIXED" in first_line.upper() else "WEAK"
        )
        base_record["status"] = "observed"
        base_record["verdict"] = verdict
        base_record["reasoning"] = content
        base_record["calibration_status"] = (
            "Tested 2026-08-31 against 47 Janusian entries (2.8% STRONG "
            "unfiltered) and a 31-entry cross-mode sample stratified by "
            "pair_type (formalism-shaped: 3/11, 27.3% STRONG; narrative-"
            "shaped and mixed-uncertain: 0/20). This record's own accuracy "
            "on THIS hypothesis has not been separately re-validated -- "
            "informational, not a verdict override. Changes nothing about "
            "this hypothesis's real generation, verification, refutation, "
            "or score."
        )
        append_log(base_record)
        return base_record
    except Exception as e:
        base_record["status"] = "error"
        base_record["error"] = f"{type(e).__name__}: {e}"
        append_log(base_record)
        return base_record


def main():
    parser = argparse.ArgumentParser(
        description="Phase 1.5 observe-only structural-correspondence triage on formalism-shaped pairs — gates nothing"
    )
    parser.add_argument("slugs", nargs="*", help="Specific hypothesis slugs")
    parser.add_argument(
        "--all-unobserved", action="store_true",
        help="Process every real formalism-shaped slug (per prefilter-log.jsonl) not yet in structural-correspondence-log.jsonl",
    )
    args = parser.parse_args()

    if args.all_unobserved:
        candidates = formalism_shaped_slugs()
        observed = already_observed_slugs()
        targets = [s for s in candidates if s not in observed]
    elif args.slugs:
        targets = args.slugs
    else:
        raise SystemExit("Pass specific slugs, or --all-unobserved.")

    framework = load_framework()
    print(f"structural_correspondence_observe.py — {len(targets)} formalism-shaped slug(s) to observe (fail-open, gates nothing)")
    for slug in targets:
        try:
            record = observe_one(slug, framework)
            status = record.get("status")
            extra = f" verdict={record['verdict']}" if status == "observed" else f" error={record.get('error')}" if status == "error" else ""
            print(f"  {slug}: {status}{extra}")
        except Exception as e:
            # Belt-and-suspenders: even a bug in observe_one's own error handling
            # must not stop the batch or propagate up to any caller.
            print(f"  {slug}: UNCAUGHT ERROR (skipped, not fatal): {type(e).__name__}: {e}")

    print(f"Logged to {LOG_PATH}")


if __name__ == "__main__":
    main()
