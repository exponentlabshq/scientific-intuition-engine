#!/usr/bin/env python3
"""
score_email_sharpness.py -- COA 8c: an INDEPENDENT judgment of how sharp
vs. generic a drafted opening_question actually reads, so the send queue
can prioritize genuinely sharp emails over ones that are real but bland.

Deliberately NOT a self-score from the same call that drafted the
question -- this pipeline already has a hard-won lesson on exactly that
failure mode (hypothesis_engine.py's own postmortem: "a soft, written
self-check gets talked past by the model that's supposed to be checking
itself"). This is a second, separate call, given ONLY the finished
question and the paper it's citing -- blind to the hypothesis's own
reasoning or the fact that a generation step produced it -- graded the
way a skeptical outside reader would judge a cold email's opening line.

Usage:
    python3 outreach/score_email_sharpness.py            # scores every
        drafted email in outreach/emails/*.md not yet scored, writes
        results into outreach/sharpness_scores.json
    python3 outreach/score_email_sharpness.py --force    # re-score all
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
SCORES_PATH = os.path.join(PIPELINE_DIR, "outreach", "sharpness_scores.json")

load_dotenv("/Users/michaeljagdeo/Downloads/talentOS-2026/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"

SHARPNESS_SCHEMA = {
    "type": "object",
    "properties": {
        "sharpness": {
            "type": "string",
            "enum": ["SHARP", "BORDERLINE", "GENERIC"],
            "description": (
                "SHARP: a specific, non-obvious question naming a real mechanism or variable a "
                "domain expert would find genuinely worth answering -- could not have been written "
                "by someone who only knew the paper's title. BORDERLINE: real and on-topic, but "
                "mostly restates the paper's own known mechanism back at its author rather than "
                "posing an independent question. GENERIC: could be generated from the domain name "
                "alone (e.g. 'Can X noise improve Y system performance?' for any noise-related "
                "field) -- reads as a textbook restatement, not a real research question."
            ),
        },
        "restates_domain_name": {
            "type": "boolean",
            "description": "True if the question is substantially just the topic/domain name rearranged into a question, with no specific mechanism, variable, or claim added.",
        },
        "reason": {"type": "string", "description": "1 sentence: the specific evidence for this verdict."},
    },
    "required": ["sharpness", "restates_domain_name", "reason"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = (
    "You are a skeptical outside reader judging ONE cold-email opening question, exactly as a "
    "busy researcher would read it in their inbox -- with no knowledge of how it was written or "
    "why. You are given the question and the paper title it cites. Judge only whether the "
    "question itself is sharp and specific enough to make a real researcher stop and think "
    "'huh, that's a real question,' versus generic enough that it could have been produced from "
    "the field's name alone without reading anything. Be genuinely skeptical -- most AI-drafted "
    "questions default to safe, generic phrasing, and your job is to catch that, not to be "
    "generous."
)


def score_one(question, paper_title):
    text = f"Opening question: {question}\n\nPaper it cites: \"{paper_title}\"\n\nJudge this question's sharpness."
    resp = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=text,
        max_output_tokens=500,
        text={"format": {"type": "json_schema", "name": "sharpness_judgment", "schema": SHARPNESS_SCHEMA, "strict": True}},
    )
    token_tracker.log_usage("outreach_sharpness_score", MODEL, resp.usage)
    return json.loads(resp.output_text)


def load_drafted_emails():
    """Parses (question, paper title, filename, hypothesis_slug) out of
    every drafted .md file directly from disk -- same 'never a separate
    list to drift out of sync' discipline as load_already_drafted() in
    the other two outreach scripts."""
    out = []
    for path in sorted(glob.glob(os.path.join(EMAILS_DIR, "*.md"))):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        # Matches any bolded sentence ending in "?" -- not just this
        # session's "Can X...?" phrasing. Found 2026-09-02: three older
        # drafts (Schooler, El-Gohary, Zhang) predate that convention
        # ("For a single unfinished creative work...?"), and a regex
        # anchored on "Can " silently skipped all three.
        qm = re.search(r"\*\*([A-Z][^*]*?\?)\*\*", text)
        slugm = re.search(r"\*\*Hypothesis:\*\*\s*`([^`]+)`", text)
        titlem = re.search(r'"([^"]+),?"\s+looks like', text)
        if qm and slugm:
            out.append({
                "filename": os.path.basename(path),
                "hypothesis_slug": slugm.group(1),
                "question": qm.group(1),
                "paper_title": titlem.group(1) if titlem else "",
            })
    return out


def load_scores():
    if os.path.exists(SCORES_PATH):
        with open(SCORES_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Re-score every drafted email, not just unscored ones")
    args = parser.parse_args()

    drafted = load_drafted_emails()
    scores = {} if args.force else load_scores()

    todo = [d for d in drafted if d["filename"] not in scores]
    print(f"{len(drafted)} drafted email(s) found. {len(todo)} to score.\n")

    for d in todo:
        judgment = score_one(d["question"], d["paper_title"])
        scores[d["filename"]] = {
            "hypothesis_slug": d["hypothesis_slug"],
            "question": d["question"],
            **judgment,
        }
        print(f"[{judgment['sharpness']:10s}] {d['filename']}")
        print(f"    Q: {d['question']}")
        print(f"    -> {judgment['reason']}\n")

    with open(SCORES_PATH, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)
    print(f"Wrote {len(scores)} score(s) to {SCORES_PATH}")


if __name__ == "__main__":
    main()
