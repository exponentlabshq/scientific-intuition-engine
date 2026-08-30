#!/usr/bin/env python3
"""
chain_composition.py -- a cheap, mechanical pre-filter for domain pairs,
built from a real conversation about what x:y = a:b was actually testing
(one arrow -- whether a single object-pair maps) versus what x:y:z = a:b:c
tests (two composable arrows -- whether the SAME relation-type survives a
second hop, which is the actual mathematical content of "functor").

The theory was never new. prompts/umpf_hypothesis_prompt.md already says
so directly: "a mapping f: M(domain1) -> M(domain2) that preserves
compositional structure -- identity and associativity carry across, not
just vocabulary." What was missing is that nothing ever checked it -- the
real §3 output format asks for exactly ONE mapping instance, "at the
layer where the correspondence is strongest," and nothing forces a second,
independent hop to confirm the same relation-type actually holds twice.
This is the same gap Failure 1 already named once, one level up: a
written theoretical requirement that sounds right and is never mechanically
verified gets talked past.

Notation, made precise rather than borrowed from proportion (colons imply
a ratio, which was never the right branch of math): each hop is a
commuting square --

    x --R--> y          (domain A, one relation-type R)
    |f       |f
    v        v
    a --R'-> b          (domain B, one relation-type R')

-- and a chain of length n is n-1 such squares stacked, each required to
commute: f(R(x,y)) == R'(f(x),f(y)).

Two real calls per hop, not one, on purpose -- this project's own lesson
from Failure 1 and Failure 2 ("self-report is not verification") applies
here exactly: a single call that both proposes a chain AND judges its own
consistency will talk itself into the length it wants. So:

  1. generate_chain() -- one call proposes domain A, domain B, an
     invariant statement, and as many hops as it can honestly construct.
  2. verify_hop_independently() -- a SEPARATE call per hop (from hop 2
     onward), shown ONLY that one hop's x/y/a/b/relation content and the
     invariant statement -- not the chain, not the hop number, not told
     this is part of a longer sequence -- asked whether this hop, judged
     completely on its own, genuinely instantiates the same invariant or
     requires a quietly different rule. Same blind-lens discipline as
     refute_hypothesis.py's three independent reviewers.

composition_depth() originally reported one number: consecutive hops from
hop 1 that survive independent verification, stopping at the first failure.
Real gold-pair testing (2026-08-30, magneto-operant-schedule dialectic vs.
a Kahneman-Tversky/Allais-paradox pair from bisociation_gold_pairs.json)
caught this metric discarding real signal -- a run with 6 of 10 hops
independently verified True scored a flat 0 because hops 1-2 happened to
fail first. composition_depth() now also returns a metrics dict:
longest_run (the longest True streak ANYWHERE in the sequence, not
required to start at hop 1) and pass_rate (fraction of all hops that
verified True, cheapest and most position-insensitive, most vulnerable to
a generator padding near-duplicate easy hops -- read alongside longest_run,
never alone). The original hop-1-anchored count is kept as
unbroken_depth_from_start for continuity, not as the primary signal.
A generator that pads a chain to look longer than it really is still gets
caught the same way an unfalsifiable Janusian hedge gets caught: by a
second, independent check that never sees the first check's reasoning --
these metrics just stop throwing away what that check actually found.

specificity is a single, UNCALIBRATED LLM-judge score, disclosed as such
in every output -- this project already has real, disclosed evidence
(the outreach-sharpening concreteness gate, 2026-08-30) that a single-call
LLM judge for "how specific/generic is this" does NOT reliably discriminate
against real ground truth. Report it, do not trust it, do not wire it into
any automated triage decision until it has been calibrated the same
disciplined way the concreteness gate was tested and rejected.

prior_art_distance is NOT computed here. That is Phase 2's job
(verify_hypothesis.py, real web search) -- duplicating it cheaply before
generation would either be too shallow to mean anything or expensive
enough to defeat the point of a pre-filter. This script's real deliverable
is composition_depth: a mechanical, independently-verified signal for
whether a domain pair is worth spending a real hypothesis-generation call
on, not a replacement for Phase 2 or Phase 2.5.

Usage:
    python3 chain_composition.py "Domain A description" "Domain B description"
    python3 chain_composition.py "Domain A" "Domain B" --max-hops 5
"""
import argparse
import json
import os

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

from retry import call_with_retry
from token_tracker import log_usage

load_dotenv(find_dotenv(usecwd=False))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"

CHAIN_SCHEMA = {
    "type": "object",
    "properties": {
        "relation_a": {"type": "string", "description": "The single relation-type R threading domain A's chain, named once."},
        "relation_b": {"type": "string", "description": "The single relation-type R' threading domain B's chain, named once."},
        "invariant": {"type": "string", "description": "The one relational rule this whole chain claims survives the domain change — the thing being tested, stated once, abstractly enough to check each hop against but not so abstract it's contentless."},
        "hops": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "x": {"type": "string"},
                    "y": {"type": "string"},
                    "a": {"type": "string"},
                    "b": {"type": "string"},
                    "relation_instance": {"type": "string", "description": "In one sentence: how R(x,y) and R'(a,b) instantiate the invariant for this specific hop."},
                },
                "required": ["x", "y", "a", "b", "relation_instance"],
                "additionalProperties": False,
            },
        },
        "honest_stopping_reason": {"type": "string", "description": "Why the chain stops where it does — what would the next hop need, that you couldn't honestly construct?"},
    },
    "required": ["relation_a", "relation_b", "invariant", "hops", "honest_stopping_reason"],
    "additionalProperties": False,
}

VERIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "commutes": {"type": "boolean", "description": "Does this hop's relation genuinely instantiate the stated invariant, judged entirely on its own?"},
        "reasoning": {"type": "string"},
    },
    "required": ["commutes", "reasoning"],
    "additionalProperties": False,
}

SPECIFICITY_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "integer", "description": "1 = this invariant would fit almost any two complex systems (umbrella trap). 5 = this invariant is specific enough that most domain pairs could NOT be honestly described this way."},
        "how_many_other_domains_fit": {"type": "string", "description": "Name 2-3 other real domain pairs this exact invariant statement would also honestly describe, if any come to mind."},
        "reasoning": {"type": "string"},
    },
    "required": ["score", "how_many_other_domains_fit", "reasoning"],
    "additionalProperties": False,
}


def _call(instructions, input_text, schema, schema_name, phase):
    resp = call_with_retry(
        client.responses.create,
        model=MODEL,
        instructions=instructions,
        input=input_text,
        text={"format": {"type": "json_schema", "name": schema_name, "schema": schema, "strict": True}},
        max_output_tokens=1200,
    )
    log_usage(phase, MODEL, resp.usage)
    return json.loads(resp.output_text)


def generate_chain(domain_a: str, domain_b: str, max_hops: int = 5) -> dict:
    instructions = (
        "You are proposing a candidate structure-preserving mapping (functor) between two domains, "
        "for the UMPF framework (Exponent Labs LLC). Name ONE relation-type R that threads a chain of "
        "objects in domain A, and the corresponding relation-type R' in domain B. Then construct as many "
        "hops as you can HONESTLY construct — each hop is a pair (x,y) in domain A and the corresponding "
        "pair (a,b) in domain B, where R(x,y) and R'(a,b) both instantiate the SAME single invariant rule. "
        "Do not pad the chain — stop and say so honestly the moment the next hop would require inventing "
        f"a different rule or reaching. Maximum {max_hops} hops. A short, honest chain of 2 is better than "
        "a padded chain of 5 that quietly changes what it's claiming halfway through."
    )
    input_text = f"DOMAIN A: {domain_a}\nDOMAIN B: {domain_b}"
    return _call(instructions, input_text, CHAIN_SCHEMA, "chain", "chain_generation")


def verify_hop_independently(invariant: str, hop: dict) -> dict:
    instructions = (
        "You are an independent reviewer checking ONE claimed instance of a relational invariant. "
        "You are shown the invariant and exactly one (x,y,a,b) pair — nothing else. You do not know how "
        "many other hops exist, whether this is the first or the last, or what any other reviewer found. "
        "Judge entirely on your own: does this specific pair genuinely instantiate the stated invariant, "
        "or does it require a quietly different, looser, or more generic rule than the one stated? "
        "Default to false under genuine uncertainty — a hop wrongly counted costs the whole chain's "
        "credibility; a hop wrongly rejected costs nothing but one data point."
    )
    input_text = (
        f"Invariant: {invariant}\n\n"
        f"x = {hop['x']}\ny = {hop['y']}\na = {hop['a']}\nb = {hop['b']}\n"
        f"Claimed relation instance: {hop['relation_instance']}"
    )
    return _call(instructions, input_text, VERIFY_SCHEMA, "hop_verification", "chain_verification")


def judge_specificity(invariant: str) -> dict:
    instructions = (
        "You are judging how SPECIFIC a relational invariant is — not whether it's true, only how many "
        "other domain pairs could also honestly be described this way. This score is explicitly "
        "UNCALIBRATED — a single-call LLM judge for this exact kind of question (how concrete/specific is "
        "a claim) failed real calibration testing on 2026-08-30 in this same project, so treat this as a "
        "directional signal only, never as ground truth."
    )
    return _call(instructions, f"Invariant: {invariant}", SPECIFICITY_SCHEMA, "specificity", "chain_specificity")


def composition_depth(hops: list, invariant: str) -> tuple:
    """Verify each hop independently and blindly. Returns (depth, verified_hops, metrics).

    depth (a.k.a. unbroken_depth_from_start) — the ORIGINAL metric: consecutive hops from
    hop 1 that survived, stopping at the first failure. Kept for continuity, but shown
    (2026-08-30, real gold-pair test) to discard real signal on its own — see module
    docstring. Don't read this number alone.

    metrics — a dict with the fuller picture:
      longest_run  — the longest CONSECUTIVE True streak found ANYWHERE in the sequence,
                     not required to start at hop 1. A generator's real signal doesn't
                     always land at the front.
      pass_rate    — fraction of all hops that independently verified True. Cheapest and
                     least position-sensitive; most vulnerable to a generator padding many
                     near-duplicate easy hops, so weigh it alongside longest_run, not alone.
      n_hops       — how many hops were actually generated (context for pass_rate).
    """
    verified = []
    depth = 0
    broken = False
    longest_run = 0
    current_run = 0
    n_true = 0
    for i, hop in enumerate(hops):
        result = verify_hop_independently(invariant, hop)
        verified.append({**hop, "commutes": result["commutes"], "verification_reasoning": result["reasoning"]})
        if result["commutes"]:
            n_true += 1
            current_run += 1
            longest_run = max(longest_run, current_run)
        else:
            current_run = 0
        if not broken:
            if result["commutes"]:
                depth += 1
            else:
                broken = True
    metrics = {
        "unbroken_depth_from_start": depth,
        "longest_run": longest_run,
        "pass_rate": (n_true / len(hops)) if hops else 0.0,
        "n_hops": len(hops),
    }
    return depth, verified, metrics


def evaluate_pair(domain_a: str, domain_b: str, max_hops: int = 5) -> dict:
    chain = generate_chain(domain_a, domain_b, max_hops=max_hops)
    depth, verified_hops, metrics = composition_depth(chain["hops"], chain["invariant"])
    specificity = judge_specificity(chain["invariant"])

    return {
        "domain_a": domain_a,
        "domain_b": domain_b,
        "relation_a": chain["relation_a"],
        "relation_b": chain["relation_b"],
        "invariant": chain["invariant"],
        "claimed_hops": len(chain["hops"]),
        "honest_stopping_reason": chain["honest_stopping_reason"],
        "hops": verified_hops,
        "composition_depth": depth,  # kept for continuity — see composition_metrics for the fuller picture
        "composition_metrics": metrics,
        "specificity": {**specificity, "calibration_status": "UNCALIBRATED — directional signal only, see module docstring"},
        "recommendation": (
            "PROMOTE — real composability signal found (longest_run ≥ 2 verified hops), worth a real hypothesis-generation call"
            if metrics["longest_run"] >= 2 else
            "LOW_PRIORITY — no run of 2+ consecutive independently-verified hops found anywhere in the chain"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Chain-composition pre-filter for a candidate domain pair")
    parser.add_argument("domain_a")
    parser.add_argument("domain_b")
    parser.add_argument("--max-hops", type=int, default=5)
    args = parser.parse_args()

    result = evaluate_pair(args.domain_a, args.domain_b, max_hops=args.max_hops)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
