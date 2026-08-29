#!/usr/bin/env python3
"""
One-off data assembly for the interactive Leaderboard Experience artifact.
Reads verification-log.jsonl, matches each entry to its real hypothesis /
verification / refutation markdown files (by filename substring matching,
printed for manual verification -- never trusted blindly), computes points
+ badges via score_hypotheses.py's own scoring function (imported directly,
not reimplemented), and writes one consolidated JSON blob:
experience_data.json. That file gets embedded verbatim into the published
HTML artifact -- this script's job is ONLY to assemble real content, not to
summarize or invent it.
"""

import json
import os
import re

from score_hypotheses import load_entries, score_entry, key_for

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
HYPOTHESES_DIR = os.path.join(PIPELINE_DIR, "hypotheses")
VERIFICATIONS_DIR = os.path.join(PIPELINE_DIR, "verifications")
REFUTATIONS_DIR = os.path.join(PIPELINE_DIR, "refutations")
CASE_STUDIES_DIR = os.path.join(os.path.dirname(os.path.dirname(PIPELINE_DIR)), "the-rosetta-stone", "case-studies")

VERIFICATION_FILENAME_OVERRIDES = {
    # Real mismatches between the hypothesis_slug key and the (inconsistently
    # short-named) verification filename actually written -- confirmed by
    # hand against verifications/ directory listing, not guessed.
    "2026-08-28-anthropology-gift-economies-and-reciprocity-x-military-strategy": "2026-08-28-anthropology-military-strategy-verification.md",
    "2026-08-28-swarm-robotics-flocking-boids-behavior-x-culinary-arts": "2026-08-28-swarm-robotics-culinary-arts-verification.md",
    "2026-08-28-homospatial-comedy-x-sports": "2026-08-28-homospatial-comedy-sports-verification.md",
    "2026-08-28-homospatial-chemistry-x-gaming-narrative": "2026-08-28-homospatial-chemistry-gaming-narrative-verification.md",
    "2026-08-28-human-trust-variance-x-cryptography": "2026-08-28-human-trust-variance-cryptography-verification.md",
    "2026-08-28-physical-bridge-cable-tension-x-organizational-theory": "2026-08-28-bridge-cable-tension-organizational-hierarchy-verification.md",
    "2026-08-28-creative-musical-motif-deviation-x-evolutionary-biology": "2026-08-28-musical-motif-deviation-punctuated-equilibrium-verification.md",
    "2026-08-28-informational-hash-collisions-x-human-social-network-dynamics": "2026-08-28-hash-collisions-social-network-dynamics-verification.md",
    "2026-08-28-human-financial-trading-algorithms-x-ecology": "2026-08-28-financial-trading-algorithms-ecology-verification.md",
    # Second verification pass (2026-08-29) clearing the PENDING_VERIFICATION queue -- the
    # hypothesis files kept their original 08-28 generation date, but their verification files
    # are correctly dated 08-29 (when they were actually verified), breaking the substring match.
    "2026-08-28-janusian-informational-distributed-consensus": "2026-08-29-janusian-informational-distributed-consensus-verification.md",
    "2026-08-28-janusian-human-cognitive-bias": "2026-08-29-janusian-human-cognitive-bias-verification.md",
    "2026-08-28-janusian-physical-quantum-measurement": "2026-08-29-janusian-physical-quantum-measurement-verification.md",
    "2026-08-28-janusian-creative-creative-block": "2026-08-29-janusian-creative-creative-block-verification.md",
    "2026-08-28-janusian-informational-load-balancing": "2026-08-29-janusian-informational-load-balancing-verification.md",
    "2026-08-28-homospatial-physical-mechanical-spring-systems-x-human-emotional-fluctuation": "2026-08-29-homospatial-mechanical-spring-x-emotional-fluctuation-verification.md",
    "2026-08-28-homospatial-creative-narrative-arc-development-x-informational-distributed-consensus": "2026-08-29-homospatial-narrative-arc-x-distributed-consensus-verification.md",
    "2026-08-28-homospatial-physical-chemical-reaction-networks-x-human-committee-formation": "2026-08-29-homospatial-chemical-reaction-x-committee-formation-verification.md",
    "2026-08-28-homospatial-astronomy-x-creative-album-production-orchestration": "2026-08-29-homospatial-astronomy-x-album-production-verification.md",
    "2026-08-28-homospatial-informational-cache-miss-handling-x-human-individual-indecision": "2026-08-29-homospatial-cache-miss-x-individual-indecision-verification.md",
}

CASE_STUDY_FILENAME_OVERRIDES = {
    "DCA-cachecoherentprotocols": "the-rosetta-stone-case-study-DCA-cachecoherentprotocols.md",
    "compileroptimization-neuralnetworktraining": "the-rosetta-stone-case-study-compileroptimization-neuralnetworktraining.md",
    "geneticalgorithms-simulatedannealing": "the-rosetta-stone-case-study-geneticalgorithms-simulatedannealing.md",
    "graphalgorithms-gametreesearch": "the-rosetta-stone-case-study-graphalgorithms-gametreesearch.md",
    "graphtraversal-statespacesearch": "the-rosetta-stone-case-study-graphtraversal-statespacesearch.md",
    "humanimmunesystem-distributedledgertechnology": "the-rosetta-stone-case-study-humanimmunesystem-distributedledgertechnology.md",
    "neuralnets-coralreef": "the-rosetta-stone-case-study-neuralnets-coralreef.md",
    "nobelprize2022-quantuminformation": "the-rosetta-stone-case-study-nobelprize2022-quantuminformation.md",
    "physics-empiricismproblem": "the-rosetta-stone-case-study-physics-empiricismproblem.md",
    "raft-PBFTconsensus": "the-rosetta-stone-case-study-raft-PBFTconsensus.md",
    "samplevariation-proteinprediction-eigenron": "the-rosetta-stone-case-study-samplevariation-proteinprediction-eigenron.md",
    "trig-fourier": "the-rosetta-stone-case-study-trig-fourier.md",
    "dirac-largenumbers": "the-rosetta-stone-dirac-largenumbers.md",
}


def read_if_exists(path):
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def find_by_substring(directory, key, suffix_hint=""):
    """Find the single file in `directory` whose name contains all the
    distinctive tokens of `key`. Returns (filename, content) or (None, None).
    Prints ambiguous/failed matches for manual inspection.

    2026-08-29 fix: try an EXACT filename first, before ever falling into
    the substring search below. Found by running hypothesis_engine.py's new
    filename-collision fix for real: a disambiguated slug like
    "...janusian-control-theory-2" is, as a bare substring, contained in
    BOTH "...janusian-control-theory.md" and "...janusian-control-theory-2.md"
    -- so the base entry's own (unsuffixed) key matched two files here. The
    "sorted by length" tie-break happened to resolve it correctly every time
    this ran for real (a suffixed filename is always longer than its own
    base, and a suffixed key is never a substring of the shorter base
    filename) -- verified directly against experience_data.json's assembled
    content, no real mix-up occurred -- but relying on that as a permanent
    guarantee is exactly the kind of "worked by luck, not by design" gap
    this project's own discipline exists to close. Exact match removes the
    ambiguity outright rather than trusting the tie-break to keep landing
    right."""
    if not os.path.isdir(directory):
        return None, None
    candidates = os.listdir(directory)
    key_norm = key.lower().replace("_", "-")
    lower_to_real = {c.lower(): c for c in candidates}
    for exact_candidate in (f"{key_norm}.md", f"{key_norm}-verification.md", f"{key_norm}-refutation.md"):
        if exact_candidate in lower_to_real:
            fn = lower_to_real[exact_candidate]
            return fn, read_if_exists(os.path.join(directory, fn))

    exact_hits = [c for c in candidates if key_norm in c.lower()]
    if len(exact_hits) == 1:
        fn = exact_hits[0]
        return fn, read_if_exists(os.path.join(directory, fn))
    if len(exact_hits) > 1:
        print(f"  AMBIGUOUS in {directory}: key={key!r} matched {exact_hits}")
        fn = sorted(exact_hits, key=len)[0]
        return fn, read_if_exists(os.path.join(directory, fn))
    print(f"  NO MATCH in {directory} for key={key!r}")
    return None, None


def main():
    entries = load_entries()
    assembled = []

    for rec in entries:
        key = key_for(rec)
        points, badges, breakdown, held_out_reason = score_entry(rec)

        is_case_study = rec.get("source") == "rosetta-stone-case-study" or "case_study" in rec

        hypothesis_content = None
        hypothesis_filename = None
        if is_case_study:
            override = CASE_STUDY_FILENAME_OVERRIDES.get(key)
            if override:
                hypothesis_filename = override
                hypothesis_content = read_if_exists(os.path.join(CASE_STUDIES_DIR, override))
            else:
                print(f"  NO CASE-STUDY FILE MAPPING for key={key!r}")
        else:
            hypothesis_filename, hypothesis_content = find_by_substring(HYPOTHESES_DIR, key)

        ver_override = VERIFICATION_FILENAME_OVERRIDES.get(key)
        if ver_override:
            verification_filename = ver_override
            verification_content = read_if_exists(os.path.join(VERIFICATIONS_DIR, ver_override))
        elif rec.get("verdict") == "PENDING_VERIFICATION":
            verification_filename, verification_content = None, None
        else:
            verification_filename, verification_content = find_by_substring(VERIFICATIONS_DIR, key)

        refutation_content = None
        refutation_filename = rec.get("refutation_file")
        if refutation_filename:
            refutation_content = read_if_exists(os.path.join(PIPELINE_DIR, refutation_filename))

        assembled.append({
            "key": key,
            "mode": rec.get("mode"),
            "source": rec.get("source"),
            "domains": rec.get("domains", []),
            "verdict": rec.get("verdict"),
            "points": points,
            "badges": badges,
            "breakdown": breakdown,
            "held_out_reason": held_out_reason,
            "notes": rec.get("notes"),
            "self_reported_distance": rec.get("self_reported_distance"),
            "self_reported_tension": rec.get("self_reported_tension"),
            "hypothesis_filename": hypothesis_filename,
            "hypothesis_content": hypothesis_content,
            "verification_filename": verification_filename,
            "verification_content": verification_content,
            "refutation_filename": refutation_filename,
            "refutation_content": refutation_content,
            "refutation_independently_confirmed": rec.get("refutation_independently_confirmed", False),
        })

    missing_hyp = sum(1 for a in assembled if a["hypothesis_content"] is None)
    missing_ver = sum(1 for a in assembled if a["verification_content"] is None)
    print(f"\nAssembled {len(assembled)} entries. Missing hypothesis content: {missing_hyp}. Missing verification content: {missing_ver}.")

    out_path = os.path.join(PIPELINE_DIR, "experience_data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(assembled, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
