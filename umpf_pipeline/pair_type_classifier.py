#!/usr/bin/env python3
"""
pair_type_classifier.py -- Phase 0 of the v2 redesign (eureka-engine-v2-prd.md,
Section 2.1). One cheap classification call, before anything spends a real
generation call, labeling a candidate domain pair along the axis the 2026-08-30
gold-pair testing actually validated:

  narrative-shaped   -- the connection, if real, would be a technique, trait,
                         or mechanism that generalizes across prose-describable
                         contexts (invention transplanted between industries;
                         a psychological trait; a market mechanism).
  formalism-shaped    -- the connection, if real, would be a literal shared
                         equation, derivation, or exact physical law.
  mixed-uncertain      -- doesn't cleanly resolve to either.

This label decides routing (PRD Section 2.2/2.3), not correctness -- it is
itself unvalidated against real pipeline outcomes (PRD Section 5, Phase A/B)
and must not be trusted for anything beyond observe-only logging until that
validation exists.

Usage:
    python3 pair_type_classifier.py "Domain A" "Domain B"
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

PAIR_TYPE_SCHEMA = {
    "type": "object",
    "properties": {
        "pair_type": {
            "type": "string",
            "enum": ["narrative-shaped", "formalism-shaped", "mixed-uncertain"],
        },
        "reasoning": {"type": "string", "description": "One or two sentences — what about this pair points to that label."},
        "confidence": {"type": "integer", "description": "1 (low) to 5 (high)."},
    },
    "required": ["pair_type", "reasoning", "confidence"],
    "additionalProperties": False,
}

INSTRUCTIONS = (
    "Classify a candidate cross-domain pair along ONE axis: if a real structural connection "
    "exists between these two domains, would it most likely be narrative-shaped (a technique, "
    "trait, or mechanism that generalizes across prose-describable contexts -- an invention "
    "transplanted between industries, a psychological trait, a market mechanism) or "
    "formalism-shaped (a literal shared equation, derivation, or exact physical law)? Judge the "
    "domains' own character, not whether a connection is likely to exist at all -- that is a "
    "separate question this classification does not answer. If genuinely unclear, say so "
    "(mixed-uncertain) rather than force a label."
)


def classify_pair_type(domain_a: str, domain_b: str) -> dict:
    resp = call_with_retry(
        client.chat.completions.create,
        model=MODEL,
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": f"DOMAIN A: {domain_a}\nDOMAIN B: {domain_b}"},
        ],
        temperature=0.2,
        response_format={"type": "json_schema", "json_schema": {"name": "pair_type", "schema": PAIR_TYPE_SCHEMA, "strict": True}},
    )
    log_usage("pair_type_classification", MODEL, resp.usage)
    return json.loads(resp.choices[0].message.content)


def main():
    parser = argparse.ArgumentParser(description="Phase 0 — classify a domain pair as narrative-shaped or formalism-shaped")
    parser.add_argument("domain_a")
    parser.add_argument("domain_b")
    args = parser.parse_args()
    result = classify_pair_type(args.domain_a, args.domain_b)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
