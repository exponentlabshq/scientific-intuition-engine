#!/usr/bin/env python3
"""
sharpen_structural_mapping.py -- forces a formalism-shaped hypothesis
through an explicit Level-3 structural-homomorphism attempt, rather than
leaving it at whatever level generation happened to land on.

Real diagnosis this exists to fix (2026-09-01, ChatGPT read of
2026-09-01-physical-mechanical-vibration-x-physical-circuit-evolution,
verified against the real hypothesis/refutation files before acting on
it): cross-domain bisociation naturally comes in three levels.

  Level 1 -- lexical analogy: "A has X, B has Y, X resembles Y."
             Unfalsifiable by construction -- can't be checked against
             math or literature. ("both evolve over time")
  Level 2 -- relational analogy: the same relation R holds across a
             mapping (X --R--> Y in A implies f(X) --R'--> f(Y) in B).
  Level 3 -- structural homomorphism: an explicit mapping f such that
             f(R_A) = R_B(f) -- the governing equation of one domain
             actually transforms into the other's under f. Checkable
             two ways: mathematically (does the equation transform?) and
             against real literature (active_research_check.py).

Generation has no machinery that knows to reach for Level 3 -- it
defaults to Level 1 and gets correctly killed by refutation's coherence/
testability/triviality lenses every time, at the cost of 3 real API
calls per case. This is exactly the mechanism behind a real, previously
unexplained empirical finding: the 80-pair gold-standard test found
"exact-shared-equation" (formalism-shaped) domain pairs had a 56%
zero-signal rate, the worst of any category (whitepaper Section 14).
Confirmed directly on the case that surfaced this: the ORIGINAL hypothesis's
functor (displacement/velocity/acceleration -> voltage/current/power) is a
Level 1 vocabulary swap that got refuted 0-of-3 for equivocation/vagueness/
genericity. The textbook-correct Level 3 mapping (force->voltage,
velocity->current, mass->inductance, damping->resistance, stiffness->
inverse capacitance -- the real "electro-mechanical impedance analogy")
found a real 1943 paper (R. G. Manley) plus a 2025 modern application when
checked with active_research_check.py -- proving the stronger reformulation
is both constructible and checkable, not a hypothetical improvement.

Only applies to formalism-shaped pairs (pair_type_classifier.py) -- a
Level 3 equation-preservation demand is a category error for narrative-
shaped pairs (comedy, invention history) with no equations to preserve.
Guarded explicitly below; do not remove that guard.

Same honest-decline discipline as sharpen_hypothesis_llm.py: a genuine
"no valid Level 3 mapping exists for this pair" is a real, informative
result, not a failure to force past. Additive only -- never overwrites
the original hypothesis file, injects a revision banner + a new section
the same way sharpen_hypothesis_llm.py does, reusing verify_hypothesis.py's
real classify() for re-verification rather than inventing a new rubric.

Usage:
    python3 sharpen_structural_mapping.py hypotheses/<slug>.md
    python3 sharpen_structural_mapping.py <slug>
    python3 sharpen_structural_mapping.py --backlog [--limit N]
    python3 sharpen_structural_mapping.py <slug> --dry-run
"""
import argparse
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sharpen_hypothesis import resolve_path, slug_from_path, soft_claim_preview, HYP_DIR, VER_DIR
from verify_hypothesis import client, classify, detect_mode, title_and_domains, load_rubric
from pair_type_classifier import classify_pair_type
from token_tracker import log_usage
from retry import call_with_retry
from refute_hypothesis import run_lens, LENS_QUESTIONS, REFUTATIONS_DIR, LENS_VERSION, load_verification_note
from ledger import load_latest_entries, LEDGER_PATH

HERE = os.path.dirname(os.path.abspath(__file__))
PREFILTER_LOG_PATH = os.path.join(HERE, "prefilter-log.jsonl")

MODEL = "gpt-4o"  # reasoning-heavy structural derivation -- same choice sharpen_hypothesis_llm.py made for its own generation call, not the gpt-4o-mini used for search-grounded checks.

STRUCTURAL_MAPPING_SCHEMA = {
    "type": "object",
    "properties": {
        "relation_a": {"type": "string", "description": "The candidate relation R_A in domain A, named precisely -- what operation or law connects which objects."},
        "objects_mapped": {
            "type": "array",
            "description": "The explicit object-by-object correspondence f. Empty if declining.",
            "items": {
                "type": "object",
                "properties": {
                    "domain_a_object": {"type": "string"},
                    "domain_b_object": {"type": "string"},
                },
                "required": ["domain_a_object", "domain_b_object"],
                "additionalProperties": False,
            },
        },
        "invariant": {"type": ["string", "null"], "description": "What is claimed to be preserved under f (an equation, a conservation law, a topological property). Null if declining."},
        "mapping_holds": {"type": "boolean", "description": "true only if you actually attempted to verify f(R_A) = R_B(f) and it holds under real, checkable reasoning -- not merely plausible-sounding."},
        "structural_reasoning": {"type": "string", "description": "The actual attempted derivation/verification -- show the equations or the logical steps, not just an assertion. If mapping_holds is false, explain specifically where it breaks."},
        "falsifiable_prediction": {"type": ["string", "null"], "description": "One falsifiable empirical prediction that follows FROM the structural mapping, not a generic one. Null if declining."},
        "could_not_construct_reason": {"type": ["string", "null"], "description": "Null if a real mapping was constructed and mapping_holds is true; otherwise a specific, real reason no valid Level-3 mapping exists for this pair -- never leave both this and invariant/falsifiable_prediction null with mapping_holds true."},
    },
    "required": ["relation_a", "objects_mapped", "invariant", "mapping_holds", "structural_reasoning", "falsifiable_prediction", "could_not_construct_reason"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = (
    "You are attempting to upgrade a cross-domain hypothesis from a lexical analogy "
    "(\"both domains have things that change over time\") to a genuine structural "
    "homomorphism: an explicit mapping f between named mathematical/physical objects "
    "in domain A and domain B, such that the governing relation/equation in A actually "
    "transforms into the governing relation/equation in B under f. This is a much "
    "higher bar than noticing both domains involve change, feedback, or evolution.\n\n"
    "Work through it explicitly:\n"
    "1. Name the real relation R_A in domain A -- the specific operation or law, not "
    "a vague description.\n"
    "2. Identify the actual mathematical or physical objects participating (variables, "
    "quantities with units or well-defined meaning -- not just topic words).\n"
    "3. Construct the object-by-object mapping f.\n"
    "4. Name the invariant f is claimed to preserve.\n"
    "5. Actually attempt to verify f(R_A) = R_B(f) -- show the equations or the "
    "logical steps. Real domain knowledge may make this true (do not invent a false "
    "mapping to force a result) or reveal it does NOT hold, which is a genuine, "
    "informative answer.\n"
    "6. If and only if the mapping holds, state one falsifiable empirical prediction "
    "that follows specifically from the structural correspondence, not a generic one "
    "that would apply to any two systems that 'evolve.'\n\n"
    "If you cannot construct a mapping that actually preserves structure -- if the "
    "honest answer is that the two domains only share vocabulary, not mathematics -- "
    "set mapping_holds to false and give a real, specific could_not_construct_reason. "
    "A genuine 'no valid Level-3 mapping exists here' is a correct, useful answer, not "
    "a failure to force past with a weaker mapping dressed up as strong."
)


def load_pair_type(slug: str, domains: list) -> dict:
    """Look up this slug's pair-type classification from prefilter-log.jsonl
    (append-only, latest entry for a slug wins) before paying for a fresh
    classify_pair_type() call -- reuses Phase 0's real, already-spent work
    rather than re-running it."""
    if os.path.exists(PREFILTER_LOG_PATH):
        latest = None
        with open(PREFILTER_LOG_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec.get("slug") == slug:
                    latest = rec
        if latest:
            return {
                "pair_type": latest["pair_type"],
                "reasoning": latest.get("pair_type_reasoning", ""),
                "confidence": latest.get("pair_type_confidence"),
                "source": "prefilter-log.jsonl (cached)",
            }
    if len(domains) < 2:
        return {"pair_type": "mixed-uncertain", "reasoning": "(single-domain hypothesis -- pair-type classifier needs two)", "confidence": None, "source": "n/a"}
    result = classify_pair_type(domains[0], domains[1])
    result["source"] = "classify_pair_type() (fresh call)"
    return result


def generate_structural_mapping(title: str, mode: str, domains: list, soft_text: str) -> dict:
    user_prompt = f"Title: {title}\nMode: {mode}\nDomain(s): {', '.join(domains)}\n\nCurrent claim (§3/§4, likely Level 1):\n{soft_text[:1200]}"
    last = None
    for attempt in range(2):
        resp = call_with_retry(
            client.chat.completions.create,
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}],
            temperature=0.4,
            response_format={"type": "json_schema", "json_schema": {"name": "structural_mapping", "schema": STRUCTURAL_MAPPING_SCHEMA, "strict": True}},
        )
        log_usage("sharpen_structural", MODEL, resp.usage)
        gen = json.loads(resp.choices[0].message.content)
        if gen.get("mapping_holds") or gen.get("could_not_construct_reason"):
            return gen
        last = gen
        user_prompt += "\n\nYou set mapping_holds to false but gave no could_not_construct_reason. State one specific reason this time."
    return last


def build_structural_block(slug: str, gen: dict, reverify: dict = None) -> str:
    today = date.today().isoformat()
    objects_table = "\n".join(
        f"| {o['domain_a_object']} | {o['domain_b_object']} |" for o in gen.get("objects_mapped", [])
    ) or "| _(none)_ | _(none)_ |"
    reverify_block = ""
    if reverify is not None:
        reverify_block = (
            f"\n### Re-verification of the structural claim\n\n"
            f"**Verdict**: {reverify['verdict']}\n\n"
            f"{reverify.get('reasoning', '')}\n"
        )
    return f"""

---

## Structural Reformulation (Level 3 -- sharpen_structural_mapping.py)

**Attempted**: {today}
**Relation in domain A**: {gen['relation_a']}

**Object mapping (f)**:

| Domain A | Domain B |
|---|---|
{objects_table}

**Claimed invariant**: {gen['invariant']}

**Structural verification (f(R_A) = R_B(f))**:
{gen['structural_reasoning']}

**Falsifiable prediction (from the structural mapping, not a generic one)**: {gen['falsifiable_prediction']}
{reverify_block}
"""


def sharpen_one(path: str, dry_run: bool = False) -> dict:
    slug = slug_from_path(path)
    text = open(path, encoding="utf-8").read()
    mode = detect_mode(text)
    title, domains = title_and_domains(text, mode)
    preview = soft_claim_preview(text)
    soft_text = preview["section3"] or preview["section4"]

    if "## Structural Reformulation (Level 3" in text:
        print("    already has a Level 3 attempt — skipping")
        return {"slug": slug, "status": "ALREADY_ATTEMPTED"}

    pair_type = load_pair_type(slug, domains)
    print(f"  pair_type: {pair_type['pair_type']} (confidence {pair_type.get('confidence')}, {pair_type['source']})")
    # A confident narrative-shaped classification is a real category error
    # (comedy x organizational theory has no equation to preserve) and hard-
    # blocks. mixed-uncertain does NOT block -- the classifier itself is
    # unsure, so the structural-mapping attempt becomes the tie-breaker: a
    # real construction is itself evidence the pair was formalism-shaped
    # after all, and an honest decline costs nothing but one API call and is
    # consistent with it not being. Real case that forced this: the exact
    # ChatGPT-flagged vibration/circuit hypothesis was cached as
    # mixed-uncertain (confidence 3) despite being a clean formalism pair --
    # the classifier's own real-world accuracy on this specific case was
    # shaky, disclosed rather than trusted blindly.
    if pair_type["pair_type"] == "narrative-shaped":
        print(f"    skipping — Level 3 (equation-preservation) is a category error for a narrative-shaped pair")
        return {"slug": slug, "status": "SKIPPED_NARRATIVE", "pair_type": pair_type["pair_type"]}

    print(f"  → attempting a Level 3 structural mapping for: {title}")
    gen = generate_structural_mapping(title, mode, domains, soft_text)

    if not gen.get("mapping_holds"):
        reason = gen.get("could_not_construct_reason") or "(no reason given even after retry)"
        print(f"    declined: {reason}")
        return {"slug": slug, "status": "DECLINED", "reason": reason}

    print(f"    constructed: {gen['invariant']}")
    print(f"    re-verifying the structural claim...")
    rubric = load_rubric()
    reverify = classify(
        f"{title} (Level 3 structural reformulation)", mode, domains,
        gen["structural_reasoning"] + "\n\nFalsifiable prediction: " + (gen.get("falsifiable_prediction") or ""),
        [], rubric, slug=f"{slug}-structural",
    )
    print(f"    re-verify: {reverify['verdict']}")

    if dry_run:
        return {"slug": slug, "status": "CONSTRUCTED_DRY_RUN", "invariant": gen["invariant"], "reverify_verdict": reverify["verdict"]}

    new_text = text.rstrip() + build_structural_block(slug, gen, reverify)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)

    os.makedirs(VER_DIR, exist_ok=True)
    ver_path = os.path.join(VER_DIR, f"{slug}-structural-verification.md")
    with open(ver_path, "w", encoding="utf-8") as f:
        f.write(
            f"# Structural Reformulation Verification: {slug}\n\n"
            f"**Verifies**: `hypotheses/{slug}.md` (Level 3 structural block)\n"
            f"**Verified**: {date.today().isoformat()} · **Method**: sharpen_structural_mapping.py (gpt-4o structural derivation + verify_hypothesis.classify() re-verify)\n\n"
            f"## Object mapping\n" + "\n".join(f"- {o['domain_a_object']} → {o['domain_b_object']}" for o in gen["objects_mapped"]) + "\n\n"
            f"## Invariant claimed\n{gen['invariant']}\n\n"
            f"## Structural reasoning\n{gen['structural_reasoning']}\n\n"
            f"## Re-verify verdict: **{reverify['verdict']}**\n\n{reverify.get('reasoning', '')}\n"
        )
    print(f"    ✅ wrote structural block + verification: {ver_path}")

    return {
        "slug": slug, "status": "CONSTRUCTED", "invariant": gen["invariant"],
        "reverify_verdict": reverify["verdict"], "verification_file": ver_path,
    }


def extract_structural_claim(text: str) -> dict:
    """Re-parse the appended Level 3 block from the hypothesis file's own
    text, rather than trusting anything held in memory from an earlier run
    -- this function has to work standalone, given just a slug, the same
    way refute_hypothesis.py's own extract_core_claim() does. Returns None
    if no Level 3 block exists (nothing to refute yet)."""
    import re
    m = re.search(
        r"## Structural Reformulation \(Level 3.*?\n\n"
        r"\*\*Attempted\*\*: .*?\n"
        r"\*\*Relation in domain A\*\*: (.*?)\n.*?"
        r"\*\*Claimed invariant\*\*: (.*?)\n\n"
        r"\*\*Structural verification.*?\*\*:\n(.*?)\n\n"
        r"\*\*Falsifiable prediction[^:]*\*\*: (.*?)\n",
        text, re.DOTALL,
    )
    if not m:
        return None
    relation_a, invariant, reasoning, prediction = m.groups()
    core_claim = (
        f"Structural claim (Level 3 reformulation): {invariant.strip()}\n\n"
        f"Reasoning: {reasoning.strip()}\n\n"
        f"Falsifiable prediction: {prediction.strip()}"
    )
    return {"relation_a": relation_a.strip(), "invariant": invariant.strip(), "core_claim": core_claim}


def refute_structural_claim(slug: str, dry_run: bool = False) -> dict:
    """Runs the exact same 3-lens adversarial machinery (run_lens, same
    rubric, same independence discipline) refute_hypothesis.py uses --
    but on the NEW Level 3 structural claim, not the original Level 1 one
    extract_core_claim() would pull from section 3/4. Deliberately does
    NOT call append_ledger_refutation() on the main ledger entry: that
    would overwrite the ORIGINAL hypothesis's refutation_verdict with a
    result testing a different claim, conflating two distinct things
    under one slug. Writes a separate refutation file
    ({slug}-structural-refutation.md) and a minimal, separately-prefixed
    ledger record (structural_refutation_*), same minimal-record-relies-
    on-field-merge pattern active_research_check.py established."""
    path = resolve_path(slug)
    text = open(path, encoding="utf-8").read()
    parsed = extract_structural_claim(text)
    if not parsed:
        raise ValueError(f"No Level 3 structural block found in {slug} — run sharpen_structural_mapping.py on it first")

    mode = detect_mode(text)
    title, domains = title_and_domains(text, mode)
    verification_note = load_verification_note(slug)
    rubric = load_rubric()

    print(f"  → refuting the STRUCTURAL claim for: {title}")
    lens_results = {}
    for lens_name, question in LENS_QUESTIONS.items():
        result = run_lens(lens_name, question, rubric, title + " (Level 3 structural reformulation)", mode, domains, parsed["core_claim"], verification_note, f"{slug}-structural")
        lens_results[lens_name] = result
        print(f"    {lens_name}: {result['verdict']}")

    survives = sum(1 for r in lens_results.values() if r["verdict"] == "SURVIVES")
    verdict = "SURVIVES" if survives >= 2 else "REFUTED"
    print(f"    tally: {survives} of 3 survive -> {verdict}")

    if dry_run:
        return {"slug": slug, "verdict": verdict, "survives": survives}

    os.makedirs(REFUTATIONS_DIR, exist_ok=True)
    ref_path = os.path.join(REFUTATIONS_DIR, f"{slug}-structural-refutation.md")
    lens_lines = "\n".join(f"- **{lens.capitalize()} — {res['verdict']}.** {res['reasoning']}" for lens, res in lens_results.items())
    with open(ref_path, "w", encoding="utf-8") as f:
        f.write(
            f"# Adversarial Refutation of the Level 3 Structural Reformulation: {title}\n\n"
            f"**Original hypothesis**: `hypotheses/{slug}.md`\n"
            f"**Tests**: the Level 3 structural claim appended by sharpen_structural_mapping.py, "
            f"NOT the original Level 1 claim -- see this hypothesis's own separate, original "
            f"`{slug}-refutation.md` for that result.\n"
            f"**Method**: 3 independent OpenAI completions, one per lens (refute_hypothesis.py's own "
            f"run_lens(), same rubric, same independence discipline)\n\n"
            f"## Tally: {survives} of 3 survive → **{verdict}**\n\n{lens_lines}\n"
        )

    # Minimal, separately-prefixed ledger record -- relies on ledger.py's
    # field-by-field merge to combine safely with the slug's existing
    # verdict/refutation_verdict fields, exactly the way
    # active_research_check.py's append_ledger_entry() already does.
    entry = {
        "hypothesis_slug": slug,
        "structural_refutation_verdict": verdict,
        "structural_refutation_survival_count": survives,
        "structural_refutation_file": f"refutations/{os.path.basename(ref_path)}",
        "structural_refutation_checked_date": date.today().isoformat(),
    }
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"    ✅ wrote {ref_path}")
    return {"slug": slug, "verdict": verdict, "survives": survives, "file": ref_path}


def main():
    parser = argparse.ArgumentParser(description="Force a formalism-shaped hypothesis through an explicit Level-3 structural-homomorphism attempt")
    parser.add_argument("hypothesis", nargs="?", help="Path or slug of a hypothesis .md")
    parser.add_argument("--backlog", action="store_true", help="Run every formalism-shaped hypothesis in prefilter-log.jsonl not yet attempted")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen; write nothing")
    parser.add_argument("--refute", action="store_true", help="Instead of constructing a mapping, adversarially refute an ALREADY-constructed Level 3 claim (requires a single slug, not --backlog)")
    args = parser.parse_args()

    if args.refute:
        if not args.hypothesis:
            raise SystemExit("--refute requires a single hypothesis slug that already has a Level 3 block")
        result = refute_structural_claim(slug_from_path(resolve_path(args.hypothesis)), dry_run=args.dry_run)
        print(f"\n{result['verdict']} ({result['survives']} of 3 survive)")
        return

    if args.backlog:
        if not os.path.exists(PREFILTER_LOG_PATH):
            raise SystemExit(f"No prefilter log at {PREFILTER_LOG_PATH}")
        by_slug = {}
        with open(PREFILTER_LOG_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec.get("slug"):
                    by_slug[rec["slug"]] = rec
        targets = [s for s, r in by_slug.items() if r.get("pair_type") == "formalism-shaped"]
        targets = [s for s in targets if os.path.exists(os.path.join(HYP_DIR, f"{s}.md"))]
        if args.limit:
            targets = targets[: args.limit]
    else:
        if not args.hypothesis:
            raise SystemExit("Pass a hypothesis file/slug, or use --backlog")
        targets = [slug_from_path(resolve_path(args.hypothesis))]

    print(f"Attempting Level 3 structural mappings for {len(targets)} hypothesis(es){' (dry run)' if args.dry_run else ''}...\n")
    results = []
    for slug in targets:
        try:
            path = resolve_path(slug)
            results.append(sharpen_one(path, dry_run=args.dry_run))
        except (Exception, SystemExit) as e:
            print(f"    ! FAILED on {slug}: {e}")
            results.append({"slug": slug, "status": f"ERROR: {e}"})
        print()

    print("=" * 60)
    print(f"Done. {len(results)} processed.")
    for r in results:
        print(f"  {r['status']:26s} {r['slug']}")

    n_constructed = sum(1 for r in results if r["status"] in ("CONSTRUCTED", "CONSTRUCTED_DRY_RUN"))
    if n_constructed:
        print(f"\n{n_constructed} real structural mapping(s) constructed and re-verified.")


if __name__ == "__main__":
    main()
