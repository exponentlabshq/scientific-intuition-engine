#!/usr/bin/env python3
"""
prefilter_observe.py -- Phase A of the v2 redesign (eureka-engine-v2-prd.md,
Section 5): runs Phase 0 (pair_type_classifier.py) and, for narrative-shaped
or mixed-uncertain pairs, Phase 0.5 (chain_dialectic.py's composability
pre-filter) against every real hypothesis this pipeline generates -- and logs
the signal to prefilter-log.jsonl. Does NOT touch verification-log.jsonl,
ledger.py, domains.json, or score_hypotheses.py. Does NOT change which
candidate gets generated, verified, refuted, or scored. It changes nothing
about how this cycle runs -- it only records what the pre-filter would have
said, against a real slug, so that once real Phase 2/2.5 verdicts land for
that same slug, prefilter-log.jsonl can be joined against verification-log
by slug to measure whether the pre-filter's signal actually predicts
anything (PRD Section 5, Phase B) -- which has not been measured yet.

This step is deliberately FAIL-OPEN, not fail-closed -- the opposite of this
pipeline's normal discipline (Section 8, "Fail-closed, not fail-quiet"), and
that difference is intentional: this is non-critical observational
commentary, the same class of step as audit_agent.py --observe, and its own
failure must never mark a cycle DEGRADED or block verification, refutation,
scoring, or publish. Every real error is still logged, not swallowed --
just never allowed to propagate into cycle status.

Domain-pair seeding follows the discipline chain_dialectic.py's own
docstring now documents (2026-08-30 finding): the plain domain names already
used throughout the rest of the pipeline (the hypothesis's own title/domains,
identical to what verify_hypothesis.py already extracts) -- nothing
hand-enriched, nothing paragraph-length. Real testing found over-specifying
the seed measurably hurts results; this stays deliberately minimal.

Usage:
    python3 prefilter_observe.py --all-unobserved
    python3 prefilter_observe.py hypotheses/<slug>.md
"""
import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_hypothesis import detect_mode, title_and_domains  # reuse, don't reimplement
from pair_type_classifier import classify_pair_type
from chain_dialectic import run_dialectic

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
HYPOTHESES_DIR = os.path.join(PIPELINE_DIR, "hypotheses")
LOG_PATH = os.path.join(PIPELINE_DIR, "prefilter-log.jsonl")

# Modes with only one real domain (Janusian: one domain held against its own
# opposite) have no genuine cross-domain pair to classify or pre-filter --
# skipped explicitly, logged as skipped, not silently omitted.
SINGLE_DOMAIN_MODES = {"janusian"}


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


def observe_one(filepath: str) -> dict:
    slug = os.path.splitext(os.path.basename(filepath))[0]
    base_record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "slug": slug,
        "source_file": os.path.basename(filepath),
    }
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        mode = detect_mode(text)
        title, domains = title_and_domains(text, mode)
        base_record["mode"] = mode
        base_record["domains"] = domains

        if mode in SINGLE_DOMAIN_MODES or len(domains) < 2:
            base_record["status"] = "skipped_single_domain_mode"
            append_log(base_record)
            return base_record

        domain_a, domain_b = domains[0], domains[1]
        pair_type_result = classify_pair_type(domain_a, domain_b)
        base_record["pair_type"] = pair_type_result["pair_type"]
        base_record["pair_type_confidence"] = pair_type_result["confidence"]
        base_record["pair_type_reasoning"] = pair_type_result["reasoning"]

        if pair_type_result["pair_type"] == "formalism-shaped":
            # Real evidence (2026-08-30, 80-pair gold test): the composability
            # pre-filter is measured to fail more than half the time on this
            # category, including on exact, rigorously true connections
            # (Shannon entropy/thermodynamic entropy, Hopfield/Ising). Running
            # it here would risk logging a misleadingly negative signal against
            # a real candidate -- skipped by design, not by oversight.
            base_record["status"] = "skipped_formalism_shaped_by_design"
            append_log(base_record)
            return base_record

        dialectic_result = run_dialectic(domain_a, domain_b, rounds=10)
        base_record["status"] = "observed"
        base_record["composition_metrics"] = dialectic_result["composition_metrics"]
        base_record["final_invariant"] = dialectic_result["final_invariant"]
        base_record["stopped_early"] = dialectic_result["stopped_early"]
        base_record["stop_reason"] = dialectic_result["stop_reason"]
        base_record["recommendation"] = (
            "would_promote" if dialectic_result["composition_metrics"]["longest_run"] >= 2
            else "would_deprioritize"
        )
        base_record["calibration_status"] = (
            "UNCALIBRATED — this recommendation has NOT been validated against real "
            "pipeline outcomes (PRD Section 5, Phase B). It changes nothing about this "
            "hypothesis's real generation, verification, refutation, or score."
        )
        append_log(base_record)
        return base_record
    except Exception as e:
        base_record["status"] = "error"
        base_record["error"] = f"{type(e).__name__}: {e}"
        append_log(base_record)
        return base_record


def main():
    parser = argparse.ArgumentParser(description="Phase A observe-only pre-filter logging (PRD Section 5) — gates nothing")
    parser.add_argument("files", nargs="*", help="Specific hypothesis .md files")
    parser.add_argument("--all-unobserved", action="store_true", help="Process every hypothesis not yet in prefilter-log.jsonl")
    args = parser.parse_args()

    if args.all_unobserved:
        observed = already_observed_slugs()
        targets = [
            f for f in sorted(glob.glob(os.path.join(HYPOTHESES_DIR, "*.md")))
            if os.path.splitext(os.path.basename(f))[0] not in observed
        ]
    elif args.files:
        targets = args.files
    else:
        raise SystemExit("Pass specific files or --all-unobserved.")

    print(f"prefilter_observe.py — {len(targets)} hypothesis file(s) to observe (fail-open, gates nothing)")
    for filepath in targets:
        try:
            record = observe_one(filepath)
            status = record.get("status")
            extra = ""
            if status == "observed":
                m = record["composition_metrics"]
                extra = f" pair_type={record['pair_type']} longest_run={m['longest_run']} pass_rate={m['pass_rate']:.0%} rec={record['recommendation']}"
            elif status == "error":
                extra = f" error={record.get('error')}"
            print(f"  {os.path.basename(filepath)}: {status}{extra}")
        except Exception as e:
            # Belt-and-suspenders: even a bug in observe_one's own error handling
            # must not stop the batch or propagate up to run_cycle.py.
            print(f"  {os.path.basename(filepath)}: UNCAUGHT ERROR (skipped, not fatal): {type(e).__name__}: {e}")

    print(f"Logged to {LOG_PATH}")


if __name__ == "__main__":
    main()
