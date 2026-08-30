#!/usr/bin/env python3
"""
chain_dialectic.py -- an alternative to chain_composition.py's single-call
generate_chain(), built after that call's real failure: asked for a
progressive chain, it produced a combinatorial grid instead (E1:S1, E1:S2,
E2:S1, E2:S2 -- four parallel snapshots of one idea, not four hops that
build on each other). Nothing in a single call forces hop 2 to grow out of
hop 1 rather than restate it.

Two agents, real back-and-forth, real conversation memory, instead of one
model asked to produce a list. EXPERT_A owns domain A and proposes the next
(x, y) pair each round, required to build on the thread so far, not restate
the opening move. EXPERT_B owns domain B, sees A's move and the full history,
and must respond with (a, b) -- honestly, including saying so when it
genuinely can't find a match rather than forcing one. That "I can't extend
this honestly" option matters: a dialectic that can't say no is just two
agents improv-ing their way to an ending, which is a real, named risk here,
not a solved one.

The conversation's own momentum is not treated as proof of anything. After
the dialectic runs, the resulting hops are checked EXACTLY the same way
chain_composition.py's single-call chains are: composition_depth() and its
blind, independent, one-hop-at-a-time verifier, reused unchanged from that
module. Two agents agreeing with each other is not verification -- a third,
uninvolved party checking each link cold, still is.

2026-08-30 fix (promoted from the throwaway /tmp v2/v3/v4 test variants after
real gold-pair validation -- see eureka-engine-v2-prd.md Section 2.2): the
original invariant_so_far field collapsed to a verbatim restatement of
whatever example seeded the round-1 prompt -- Expert A would state "the
invariant" in language that was really just the seed example relabeled, so a
genuinely different real phenomenon in round 3 or 5 would correctly fail
verification for not matching an invariant that never actually described
anything beyond round 1. Real evidence this was the dominant failure, not
generation quality: on a real historically-true gold pair (Kahneman-Tversky
x Economics, bisociation_gold_pairs.json #56), this fix alone took real
verified hop signal from zero across 11 real runs to real, repeatable
positive signal (up to 60% of hops independently verified True). The schema
now requires the invariant to be stated at the mechanism/parameter level,
not the example level, and forces a real self-check every round
(second_phenomenon_this_invariant_also_covers) -- name a second, different
phenomenon the SAME stated invariant would also predict, or admit you can't
and narrow it. A second, separate, real finding from the same testing pass:
over-specifying the SEED (hand-curated literature detail) measurably hurt
every pair it was tried on, worse than a plain, minimally-structured seed --
seed callers should build domain_a/domain_b from short, structured fields
(a name, a one-line collision description, a one-line insight), never from
hand-researched prose. See prefilter_observe.py for the production caller
that follows this discipline.

Usage:
    python3 chain_dialectic.py "Domain A" "Domain B" --rounds 10
"""
import argparse
import json
import os

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

from retry import call_with_retry
from token_tracker import log_usage
from chain_composition import composition_depth, judge_specificity

load_dotenv(find_dotenv(usecwd=False))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"

A_MOVE_SCHEMA = {
    "type": "object",
    "properties": {
        "x": {"type": "string"},
        "y": {"type": "string"},
        "relation": {"type": "string", "description": "In one sentence: what relation connects x and y this round, and how it extends (not restates) the thread so far."},
        "invariant_so_far": {
            "type": "string",
            "description": (
                "State the invariant as the GENERAL underlying mechanism or parameter -- NOT the literal seed "
                "example you were given. A concrete example (an experiment, a named effect) is ONE INSTANCE of "
                "the invariant, not the invariant itself. State it at the level of abstraction where a SECOND, "
                "DIFFERENT real phenomenon (not the seed example) could also genuinely satisfy it -- but still "
                "name the actual mechanism/parameter precisely (not a vague abstraction like 'behavioral "
                "patterns'). Carry the named mechanism forward verbatim round over round; do not re-narrow it "
                "back to one example."
            ),
        },
        "second_phenomenon_this_invariant_also_covers": {
            "type": "string",
            "description": (
                "Name ONE additional real phenomenon -- different from your seed example and from x/y this "
                "round -- that this SAME stated invariant would also genuinely predict, to prove the invariant "
                "isn't just a restatement of one example. If you honestly cannot name one, say so directly and "
                "narrow the invariant until you can."
            ),
        },
    },
    "required": ["x", "y", "relation", "invariant_so_far", "second_phenomenon_this_invariant_also_covers"],
    "additionalProperties": False,
}

B_MOVE_SCHEMA = {
    "type": "object",
    "properties": {
        "can_extend": {"type": "boolean", "description": "Can you honestly find (a,b) in your domain matching this round's relation and the invariant so far? If not, say false rather than force a weak match."},
        "a": {"type": "string"},
        "b": {"type": "string"},
        "relation": {"type": "string", "description": "In one sentence: how (a,b) instantiates the same relation A just proposed."},
        "honest_note": {"type": "string", "description": "If can_extend is false, say why here instead. If true, note any real strain in the match."},
    },
    "required": ["can_extend", "a", "b", "relation", "honest_note"],
    "additionalProperties": False,
}


def _call(instructions, messages, schema, schema_name, phase):
    resp = call_with_retry(
        client.chat.completions.create,
        model=MODEL,
        messages=[{"role": "system", "content": instructions}] + messages,
        temperature=0.4,
        response_format={"type": "json_schema", "json_schema": {"name": schema_name, "schema": schema, "strict": True}},
    )
    log_usage(phase, MODEL, resp.usage)
    return json.loads(resp.choices[0].message.content)


def run_dialectic(domain_a: str, domain_b: str, rounds: int = 10) -> dict:
    a_instructions = (
        f"You are Expert A, speaking only for DOMAIN A: {domain_a}. You are in a live exchange with "
        f"Expert B, who speaks for DOMAIN B: {domain_b}. Each round you propose ONE new pair (x,y) in your "
        "domain and the relation connecting them. Your job each round is to EXTEND the thread — build on "
        "what has come before, not restate your opening move with different labels. Be honest if "
        "you're straining to find a next move; a shorter real thread beats a padded one. "
        "CRITICAL: any concrete example given to you (an experiment, a named effect) is ONE INSTANCE of the "
        "invariant, not the invariant's definition. State invariant_so_far at the level of the general "
        "mechanism/parameter that example is evidence FOR — precisely named, not vague — so that OTHER, "
        "DIFFERENT real phenomena driven by the same mechanism would also count as valid instances. Prove "
        "this every round via second_phenomenon_this_invariant_also_covers."
    )
    b_instructions = (
        f"You are Expert B, speaking only for DOMAIN B: {domain_b}. Expert A, from DOMAIN A: {domain_a}, "
        "just proposed a new (x,y) pair and relation. Your job is to find the genuinely corresponding (a,b) "
        "in your own domain — one that instantiates the SAME relation, building on your own prior answers "
        "the same way A is building on theirs. If you cannot honestly find one, say so directly (can_extend: "
        "false) rather than force a weak match to keep the exchange going."
    )

    history = []  # shared transcript, both experts see all of it
    hops = []
    a_moves = []
    b_moves = []

    for r in range(1, rounds + 1):
        a_prompt = f"Round {r}. Propose your next (x,y) pair and relation, extending the thread so far."
        a_move = _call(a_instructions, history + [{"role": "user", "content": a_prompt}], A_MOVE_SCHEMA, "expert_a_move", "dialectic_a")
        a_moves.append(a_move)
        history.append({"role": "user", "content": a_prompt})
        history.append({"role": "assistant", "content": (
            f"[Expert A] x={a_move['x']} y={a_move['y']} relation={a_move['relation']} "
            f"invariant_so_far={a_move['invariant_so_far']} "
            f"second_phenomenon={a_move['second_phenomenon_this_invariant_also_covers']}"
        )})

        b_prompt = f"Round {r}. Expert A proposed: x={a_move['x']}, y={a_move['y']}, relation: {a_move['relation']}. Your corresponding (a,b)?"
        b_move = _call(b_instructions, history + [{"role": "user", "content": b_prompt}], B_MOVE_SCHEMA, "expert_b_move", "dialectic_b")
        b_moves.append(b_move)
        history.append({"role": "user", "content": b_prompt})
        history.append({"role": "assistant", "content": f"[Expert B] can_extend={b_move['can_extend']} a={b_move.get('a')} b={b_move.get('b')} relation={b_move.get('relation')} note={b_move['honest_note']}"})

        if not b_move["can_extend"]:
            break

        hops.append({
            "x": a_move["x"], "y": a_move["y"],
            "a": b_move["a"], "b": b_move["b"],
            "relation_instance": f"A: {a_move['relation']} | B: {b_move['relation']}",
        })

    final_invariant = a_moves[-1]["invariant_so_far"] if a_moves else ""
    stopped_early = len(a_moves) < rounds or not b_moves[-1]["can_extend"]

    depth, verified_hops, metrics = composition_depth(hops, final_invariant) if hops else (0, [], {"unbroken_depth_from_start": 0, "longest_run": 0, "pass_rate": 0.0, "n_hops": 0})
    specificity = judge_specificity(final_invariant) if final_invariant else None

    return {
        "domain_a": domain_a,
        "domain_b": domain_b,
        "rounds_completed": len(hops),
        "rounds_requested": rounds,
        "stopped_early": stopped_early,
        "stop_reason": (b_moves[-1]["honest_note"] if b_moves and not b_moves[-1]["can_extend"] else None),
        "final_invariant": final_invariant,
        "hops": verified_hops,
        "composition_depth": depth,  # kept for continuity — see composition_metrics for the fuller picture
        "composition_metrics": metrics,
        "specificity": ({**specificity, "calibration_status": "UNCALIBRATED — directional signal only"} if specificity else None),
        "raw_a_moves": a_moves,
        "raw_b_moves": b_moves,
    }


def main():
    parser = argparse.ArgumentParser(description="Two-agent dialectic chain generation, then blind verification")
    parser.add_argument("domain_a")
    parser.add_argument("domain_b")
    parser.add_argument("--rounds", type=int, default=10)
    args = parser.parse_args()
    result = run_dialectic(args.domain_a, args.domain_b, rounds=args.rounds)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
