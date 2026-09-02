#!/usr/bin/env python3
"""
score_email_coherence.py -- COA 8e: a THIRD independent check, distinct
from score_email_sharpness.py's generic-vs-specific axis. Catches the
Vajner failure mode (human-flagged 2026-09-02): a hypothesis whose real
claim is an ABSTRACT STRUCTURAL ANALOGY between two domains ("both
governed by the same relational rule of controlled uncertainty") gets
drafted as a literal causal question ("Can manipulating X affect Y?")
between two things with no real experimental connection -- sharp-
sounding, but confused to an actual domain expert. Sharpness scoring
never catches this; it grades specificity, not physical/logical
coherence.

Independent judgment again, same discipline as the sharpness score and
this pipeline's other adversarial checks: given ONLY the drafted
question and the hypothesis's own real claim (fusion sentence /
simultaneous-hold / generative-relation -- whichever structure it
uses), judge whether the question, AS PHRASED, implies a literal
causal or mechanistic connection the underlying claim doesn't actually
support -- not whether the underlying idea itself is good.

Validated against two real, human-judged cases before trusting it:
Vajner (human-flagged as incoherent) must fail; Phelan (human-approved
as coherent, single-domain paradox) must pass.

Usage:
    python3 outreach/score_email_coherence.py            # checks every
        drafted email not yet checked, writes into
        outreach/coherence_scores.json
    python3 outreach/score_email_coherence.py --force     # re-check all
"""
import argparse
import glob
import json
import os
import re
import sys

from dotenv import load_dotenv
from openai import OpenAI

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PIPELINE_DIR)
import token_tracker

EMAILS_DIR = os.path.join(PIPELINE_DIR, "outreach", "emails")
EXPERIENCE_PATH = os.path.join(PIPELINE_DIR, "experience_data.json")
SCORES_PATH = os.path.join(PIPELINE_DIR, "outreach", "coherence_scores.json")

load_dotenv("/Users/michaeljagdeo/Downloads/talentOS-2026/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"

COHERENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "coherent": {
            "type": "boolean",
            "description": (
                "False if the question, AS PHRASED, implies a literal causal or mechanistic "
                "connection between two things that the underlying claim only asserts are "
                "governed by the same ABSTRACT relational rule or structural analogy -- e.g. "
                "'Can manipulating zero-knowledge proof parameters affect the uncertainty of "
                "emitted photons?' implies tweaking a cryptographic protocol would touch a real "
                "photon source, when the actual claim is only that both domains share an abstract "
                "principle of controlled uncertainty. True if the question is a claim a domain "
                "expert could sensibly engage with, EVEN IF the underlying idea itself is "
                "speculative, cross-domain, or well-trodden territory -- speculative and confused "
                "are different things; only flag the latter."
            ),
        },
        "concern": {
            "type": "string",
            "description": "1-2 sentences: if not coherent, exactly what literal-vs-abstract gap exists. Empty string if coherent.",
        },
    },
    "required": ["coherent", "concern"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = (
    "You are a skeptical outside reader -- a real domain expert in whatever field the recipient "
    "works in -- judging ONE cold-email question for whether it actually MAKES SENSE, not "
    "whether it's interesting. You are given the drafted question and the real underlying claim "
    "it was supposed to be built from.\n\n"
    "CRITICAL, easy to get wrong: every hypothesis in this set proposes a testable causal or "
    "functional claim -- that is what a falsifiable prediction IS, and phrasing a question as "
    "'Can X function as Y?' or 'Can X drive Y?' is completely normal, correct scientific "
    "phrasing, not a defect. Do NOT flag a question merely for asserting a causal or functional "
    "claim -- that is the job of a hypothesis. A question that proposes literally BUILDING or "
    "IMPLEMENTING a rule/mechanism from one domain inside a different substrate is also normal "
    "and coherent, however far apart the two domains are -- bio-inspired engineering routinely "
    "does exactly this (a genetic algorithm implements 'evolution' as a literal optimization "
    "procedure in software; ant-colony optimization implements 'pheromone trails' as literal "
    "routing weights in a network). Example you must rate COHERENT: 'Can the same rule the "
    "brain uses to prune synapses run as the actual control principle for a power grid?' -- "
    "this proposes literally implementing a biological rule as an engineering control law, which "
    "is a real, sensible, common category of hypothesis, not a confused one.\n\n"
    "The actual, narrower failure to catch: a hypothesis whose real claim is only that two "
    "domains share an ABSTRACT PRINCIPLE or PATTERN (not a rule one could implement, borrow, or "
    "build with) gets drafted as if adjusting a parameter in one domain would produce a DIRECT "
    "PHYSICAL SIDE EFFECT in the other, with no proposed system, apparatus, or implementation "
    "connecting them at all. Example you must rate INCOHERENT: 'Can manipulating zero-knowledge "
    "proof parameters affect the uncertainty of emitted photons?' -- this implies tweaking "
    "numbers in a cryptographic proof would have a literal physical effect on a real photon "
    "source, when the underlying claim only asserts the two domains share an abstract pattern "
    "called 'controlled uncertainty' -- there is no proposed system where adjusting one could "
    "plausibly touch the other.\n\n"
    "The test: is there ANY sensible reading -- literal implementation, engineering borrowing, "
    "or a real proposed mechanism -- under which the question makes sense? If yes, COHERENT, "
    "even if that reading is ambitious or cross-domain. Only mark INCOHERENT when the question "
    "asserts a direct physical/causal link between two things with no proposed system connecting "
    "them at all, not merely because it makes a testable claim."
)


def load_hypothesis_content(slug):
    with open(EXPERIENCE_PATH, encoding="utf-8") as f:
        data = json.load(f)
    entries = data if isinstance(data, list) else data.get("entries", data.get("rows", []))
    for e in entries:
        if e.get("key") == slug:
            return e.get("hypothesis_content", "")
    return ""


def score_one(question, hypothesis_content):
    text = (
        f"Drafted question: {question}\n\n"
        f"The hypothesis this question was supposed to be built from:\n\n{hypothesis_content}\n\n"
        "Judge whether the question, as phrased, implies a literal mechanism the hypothesis's own claim doesn't support."
    )
    resp = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=text,
        max_output_tokens=600,
        text={"format": {"type": "json_schema", "name": "coherence_judgment", "schema": COHERENCE_SCHEMA, "strict": True}},
    )
    token_tracker.log_usage("outreach_coherence_score", MODEL, resp.usage)
    return json.loads(resp.output_text)


def load_drafted_emails():
    out = []
    for path in sorted(glob.glob(os.path.join(EMAILS_DIR, "*.md"))):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        qm = re.search(r"\*\*([A-Z][^*]*?\?)\*\*", text)
        slugm = re.search(r"\*\*Hypothesis:\*\*\s*`([^`]+)`", text)
        if qm and slugm:
            out.append({
                "filename": os.path.basename(path),
                "hypothesis_slug": slugm.group(1),
                "question": qm.group(1),
            })
    return out


def load_scores():
    if os.path.exists(SCORES_PATH):
        with open(SCORES_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Re-check every drafted email, not just unchecked ones")
    args = parser.parse_args()

    drafted = load_drafted_emails()
    scores = {} if args.force else load_scores()

    todo = [d for d in drafted if d["filename"] not in scores]
    print(f"{len(drafted)} drafted email(s) found. {len(todo)} to check.\n")

    for d in todo:
        hyp_content = load_hypothesis_content(d["hypothesis_slug"])
        if not hyp_content:
            print(f"[SKIPPED — no hypothesis content] {d['filename']}")
            continue
        judgment = score_one(d["question"], hyp_content)
        scores[d["filename"]] = {
            "hypothesis_slug": d["hypothesis_slug"],
            "question": d["question"],
            **judgment,
        }
        tag = "COHERENT" if judgment["coherent"] else "⚠️ INCOHERENT"
        print(f"[{tag}] {d['filename']}")
        print(f"    Q: {d['question']}")
        if not judgment["coherent"]:
            print(f"    -> {judgment['concern']}")
        print()

    with open(SCORES_PATH, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)
    print(f"Wrote {len(scores)} score(s) to {SCORES_PATH}")


if __name__ == "__main__":
    main()
