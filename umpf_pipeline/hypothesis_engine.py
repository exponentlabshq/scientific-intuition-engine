"""
UMPF Hypothesis Engine — the "Eureka Engine" extension of the
scientific-intuition-engine pipeline. Three generation modes, per Rothenberg's
full taxonomy of creative mechanisms (Ops/skills/bisociate.md,
Ops/skills/janusian.md, Ops/skills/homospatial.md in the vault) — three
structurally distinct instruments, not settings of one:

  --mode bisociation (default): TWO domains collide, each stays itself — a
      candidate functor maps between them. Koestler's bisociation (The Act
      of Creation, 1964).
  --mode janusian: ONE domain, its load-bearing assumption inverted and held
      simultaneously with the assumption itself. Proposes a falsifiable
      "third thing" — a genuine paradox, not a compromise.
  --mode homospatial: TWO domains superimposed in the same conceptual space
      until they fuse into ONE new entity that belongs to neither source —
      Rothenberg's homospatial thinking (1976), later re-derived in
      cognitive science as conceptual blending (Fauconnier & Turner).

Where main.py takes ONE source (a Nobel paper PDF) and writes a full UMPF
extension paper, this script writes a short, falsifiable hypothesis — fast,
cheap to generate many of.

Domain pool: drawn from the UNION of domains.json's domain_pool and
rosetta_stone_domains.json's 23-system pool (extracted from
the-rosetta-stone.json's UniversalMonadPatterns.Categories) — see
load_combined_pool(). This enables cross-pool pairs (a domains.json entry ×
a rosetta-stone system), not just within-pool ones.

Usage:
    # Bisociation, explicit pair:
    python3 hypothesis_engine.py --domain-a "Ecology — mycorrhizal fungal networks" \\
                                  --domain-b "Telecommunications — packet switching and routing"

    # Bisociation, autonomous — draw N fresh, unpaired domains from the combined pool,
    # excluding anything already in already_paired or already run this session:
    python3 hypothesis_engine.py --autonomous --count 3

    # Janusian, explicit single domain:
    python3 hypothesis_engine.py --mode janusian --domain-a "Neuroscience — cortical map reorganization"

    # Janusian, autonomous — draw N fresh, un-janused domains:
    python3 hypothesis_engine.py --mode janusian --autonomous --count 3

    # Homospatial, explicit pair:
    python3 hypothesis_engine.py --mode homospatial --domain-a "..." --domain-b "..."

    # Homospatial, autonomous:
    python3 hypothesis_engine.py --mode homospatial --autonomous --count 3

Every run is saved to hypotheses/<slug>.md and, in autonomous mode, the domain
(or pair) is recorded in domains.json's already_paired (bisociation),
already_janused (janusian), or already_homospatial (homospatial) list so a
future run never re-derives the same hypothesis. The three lists are
independent — a domain can appear in all three without conflict.
"""

import argparse
import itertools
import json
import os
import random
import re
from datetime import datetime, timezone

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

from token_tracker import log_usage

# Load environment variables — find_dotenv() walks up from this file's
# location, so it picks up talentOS-2026/.env (the vault root) automatically.
load_dotenv(find_dotenv(usecwd=False))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set; cannot run analysis.")
client = OpenAI(api_key=OPENAI_API_KEY)

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
DOMAINS_PATH = os.path.join(PIPELINE_DIR, "domains.json")
ROSETTA_DOMAINS_PATH = os.path.join(PIPELINE_DIR, "rosetta_stone_domains.json")
EQUIVALENCY_DOMAINS_PATH = os.path.join(PIPELINE_DIR, "equivalency_training_domains.json")
PROMPT_PATHS = {
    "bisociation": os.path.join(PIPELINE_DIR, "prompts", "umpf_hypothesis_prompt.md"),
    "janusian": os.path.join(PIPELINE_DIR, "prompts", "umpf_janusian_prompt.md"),
    "homospatial": os.path.join(PIPELINE_DIR, "prompts", "umpf_homospatial_prompt.md"),
}
HYPOTHESES_DIR = os.path.join(PIPELINE_DIR, "hypotheses")


def load_prompt(mode: str = "bisociation") -> str:
    with open(PROMPT_PATHS[mode], "r", encoding="utf-8") as f:
        return f.read()


def load_domains() -> dict:
    with open(DOMAINS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_domains(data: dict) -> None:
    with open(DOMAINS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def load_combined_pool(data: dict) -> list:
    """The union of domains.json's own domain_pool, rosetta_stone_domains.json's
    23-system pool, and equivalency_training_domains.json's 88 fine-grained
    sub-domains -- enables cross-pool pairs (e.g. a domains.json entry x an
    equivalency-training sub-domain), not just within-pool ones. Deduplicated
    in case an entry appears in more than one source (none do today, but
    don't silently double-count if that ever changes)."""
    pool = list(data["domain_pool"])
    for extra_path in (ROSETTA_DOMAINS_PATH, EQUIVALENCY_DOMAINS_PATH):
        if os.path.exists(extra_path):
            with open(extra_path, "r", encoding="utf-8") as f:
                extra = json.load(f)
            pool.extend(extra["domain_pool"])
    seen = set()
    deduped = []
    for d in pool:
        key = d.strip().lower()
        if key not in seen:
            seen.add(key)
            deduped.append(d)
    return deduped


def _pair_key(a: str, b: str) -> frozenset:
    """Order-independent identity for a domain pair."""
    return frozenset([a.strip().lower(), b.strip().lower()])


def pick_fresh_pair(data: dict, already_used_this_run: set, tracking_key: str = "already_paired") -> tuple:
    """Pick a random domain pair not in data[tracking_key] and not already
    used in this run, drawn from the combined pool (load_combined_pool).
    tracking_key lets bisociation and homospatial share this function while
    keeping independent exploration-history lists. Raises if exhausted."""
    used_keys = {_pair_key(a, b) for a, b in data.get(tracking_key, [])}
    pool = load_combined_pool(data)
    all_combos = list(itertools.combinations(pool, 2))
    random.shuffle(all_combos)
    for a, b in all_combos:
        key = _pair_key(a, b)
        if key not in used_keys and key not in already_used_this_run:
            return a, b
    raise SystemExit(f"Domain pool exhausted for {tracking_key} -- every combination has been explored. Add more domains to domains.json or rosetta_stone_domains.json.")


def pick_fresh_domain(data: dict, already_used_this_run: set) -> str:
    """Single-domain analog of pick_fresh_pair, for Janusian mode. Pick a
    random domain not in already_janused and not already used in this run,
    drawn from the combined pool."""
    janused = {d.strip().lower() for d in data.get("already_janused", [])}
    pool = load_combined_pool(data)
    random.shuffle(pool)
    for d in pool:
        if d.strip().lower() not in janused and d not in already_used_this_run:
            return d
    raise SystemExit("Domain pool exhausted for Janusian mode — every domain has been explored. Add more domains to domains.json or rosetta_stone_domains.json.")


def short_name(domain: str) -> str:
    """rosetta_stone_domains.json entries are long, rich descriptions
    ('Healthcare (Human & Social Systems) -- Atomic: Test results
    missing...'), not short labels like domains.json's plain entries. Slug
    filenames need a short human-readable name, not the full description --
    split on the first ' (' or ' -- ' and keep what's before it. Falls back
    to the full string (existing behavior) if neither delimiter is present,
    so domains.json's own plain entries are unaffected."""
    for delim in (" (", " — ", " -- "):
        if delim in domain:
            return domain.split(delim, 1)[0].strip()
    return domain


def slugify(text: str) -> str:
    text = short_name(text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text[:60]


def _clean_output(raw: str, generated_date: str) -> str:
    """Strip a stray ```markdown fence the model sometimes wraps the answer
    in, and replace whatever date the model invented with the real one —
    models reliably hallucinate a plausible-looking but wrong date here."""
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:markdown)?\s*\n", "", text)
        text = re.sub(r"\n```\s*$", "", text)
    text = re.sub(
        r"\*\*Generated\*\*:.*",
        f"**Generated**: {generated_date}",
        text,
        count=1,
    )
    return text.strip() + "\n"


# Comparison-language enforcement for homospatial mode. A written instruction
# alone was tried first (prompts/umpf_homospatial_prompt.md's own "hard rule")
# and did NOT reliably hold against gpt-4o-mini's strong prior toward analogy
# language for "combine two things" tasks -- verified directly: both of the
# first two real homospatial generations this session still used "mirrors,"
# "much like," "akin to" directly inside SS3 despite the prompt explicitly
# banning them. This is the same lesson as Janusian's same-instance-test fix,
# one level further: a soft self-check in the prompt gets talked past even
# when made maximally explicit; only checking the actual output mechanically
# and forcing a correction closes the gap.
_COMPARISON_WORDS = [
    "like", "similar to", "resembling", "resembles", "as if", "akin to",
    "parallels", "much like", "just as", "reminiscent of", "mirrors", "mirroring",
]


def _extract_section(markdown_text: str, heading_prefix: str) -> str:
    """Pull the body of one '## N. Heading' section out of the generated
    markdown, up to the next '## ' heading. Used to check SS3 specifically,
    not the whole document (SS1's plain-terms domain descriptions are allowed
    to use ordinary language freely)."""
    pattern = rf"##\s*{re.escape(heading_prefix)}.*?\n(.*?)(?=\n##\s|\Z)"
    m = re.search(pattern, markdown_text, re.DOTALL)
    return m.group(1) if m else ""


def _find_comparison_words(text: str) -> list:
    found = []
    lowered = text.lower()
    for word in _COMPARISON_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", lowered):
            found.append(word)
    return found


def run_hypothesis(domain_a: str, domain_b: str = None, model: str = "gpt-4o-mini", mode: str = "bisociation") -> str:
    system_prompt = load_prompt(mode)
    if mode == "janusian":
        user_content = f"DOMAIN: {domain_a}"
    else:
        user_content = f"DOMAIN A: {domain_a}\n\nDOMAIN B: {domain_b}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    resp = client.chat.completions.create(model=model, messages=messages, temperature=0.4)
    log_usage("generation", model, resp.usage, extra={"mode": mode, "retry": False})
    generated_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_output = resp.choices[0].message.content

    if mode == "homospatial":
        section3 = _extract_section(raw_output, "3. The Emergent Third Thing")
        violations = _find_comparison_words(section3)
        if violations:
            print(f"  ⚠️  §3 used forbidden comparison language ({', '.join(violations)}) — retrying once with a correction...")
            correction = (
                f"Your §3 (\"The Emergent Third Thing\") used forbidden comparison words: {', '.join(violations)}. "
                f"Here is what you wrote: \"{section3.strip()}\"\n\n"
                "Rewrite the ENTIRE response from scratch. Describe the fused entity in §3 in its own "
                "vocabulary, the way you'd describe a chimera's actual anatomy directly, not by comparing "
                "it back to a lion and a goat. Zero comparison words anywhere in §3 — check every sentence "
                "before finalizing."
            )
            messages.append({"role": "assistant", "content": raw_output})
            messages.append({"role": "user", "content": correction})
            resp2 = client.chat.completions.create(model=model, messages=messages, temperature=0.4)
            log_usage("generation", model, resp2.usage, extra={"mode": mode, "retry": True})
            raw_output2 = resp2.choices[0].message.content
            section3_retry = _extract_section(raw_output2, "3. The Emergent Third Thing")
            remaining = _find_comparison_words(section3_retry)
            if remaining:
                # Honest failure, not a silently-accepted one: flag it in the
                # output itself rather than pretending the retry succeeded.
                print(f"  ⚠️  Retry still used comparison language ({', '.join(remaining)}) — flagging in output rather than looping indefinitely.")
                raw_output2 = raw_output2.rstrip() + (
                    f"\n\n---\n\n**⚠️ Automated check failed twice:** §3 still contains comparison "
                    f"language ({', '.join(remaining)}) after one corrective retry. This hypothesis may "
                    f"be bisociation mislabeled as homospatial — read §3 with that in mind, don't take "
                    f"the fusion framing at face value.\n"
                )
            else:
                print("  ✅ Retry passed — §3 is comparison-word-free.")
            raw_output = raw_output2
        else:
            print("  ✅ §3 passed the comparison-word check on the first attempt.")

    return _clean_output(raw_output, generated_date)


def save_hypothesis(domain_a: str, domain_b: str, markdown_output: str, mode: str = "bisociation") -> str:
    os.makedirs(HYPOTHESES_DIR, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if mode == "janusian":
        slug = f"{date_str}-janusian-{slugify(domain_a)}"
    elif mode == "homospatial":
        slug = f"{date_str}-homospatial-{slugify(domain_a)}-x-{slugify(domain_b)}"
    else:
        slug = f"{date_str}-{slugify(domain_a)}-x-{slugify(domain_b)}"
    output_file = os.path.join(HYPOTHESES_DIR, slug + ".md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    return output_file


MODE_ICON = {"bisociation": "🧬", "janusian": "🎭", "homospatial": "🪞"}
MODE_VERB = {"bisociation": "Bisociating", "janusian": "Janusian hold on", "homospatial": "Superimposing"}
MODE_TRACKING_KEY = {"bisociation": "already_paired", "homospatial": "already_homospatial"}


def main():
    parser = argparse.ArgumentParser(description="UMPF Hypothesis Engine (bisociation + Janusian + homospatial modes)")
    parser.add_argument("--mode", type=str, choices=["bisociation", "janusian", "homospatial"], default="bisociation", help="Generation mechanism: bisociation (two domains collide), janusian (one domain, its assumption inverted), or homospatial (two domains superimposed into one fused entity)")
    parser.add_argument("--domain-a", type=str, help="First (or only, in janusian mode) domain (explicit mode)")
    parser.add_argument("--domain-b", type=str, help="Second domain (explicit mode, bisociation/homospatial only — invalid in janusian mode)")
    parser.add_argument("--autonomous", action="store_true", help="Draw fresh domain(s) from the combined pool instead of explicit args")
    parser.add_argument("--count", type=int, default=1, help="Number of hypotheses to generate in autonomous mode")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="OpenAI model to use")
    args = parser.parse_args()

    two_domain_mode = args.mode in ("bisociation", "homospatial")

    if args.mode == "janusian" and args.domain_b:
        raise SystemExit("--domain-b is not valid in --mode janusian — Janusian mode takes exactly one domain (--domain-a).")

    if args.autonomous:
        data = load_domains()
        used_this_run = set()
        for i in range(args.count):
            if args.mode == "janusian":
                domain_a = pick_fresh_domain(data, used_this_run)
                used_this_run.add(domain_a)
                print(f"{MODE_ICON[args.mode]} [{i+1}/{args.count}] {MODE_VERB[args.mode]}: {domain_a}")
                markdown_output = run_hypothesis(domain_a, model=args.model, mode="janusian")
                output_file = save_hypothesis(domain_a, None, markdown_output, mode="janusian")
                print(f"✅ Saved to {output_file}")
                data.setdefault("already_janused", []).append(domain_a)
            else:
                tracking_key = MODE_TRACKING_KEY[args.mode]
                domain_a, domain_b = pick_fresh_pair(data, used_this_run, tracking_key=tracking_key)
                used_this_run.add(_pair_key(domain_a, domain_b))
                print(f"{MODE_ICON[args.mode]} [{i+1}/{args.count}] {MODE_VERB[args.mode]}: {domain_a}  ×  {domain_b}")
                markdown_output = run_hypothesis(domain_a, domain_b, model=args.model, mode=args.mode)
                output_file = save_hypothesis(domain_a, domain_b, markdown_output, mode=args.mode)
                print(f"✅ Saved to {output_file}")
                data.setdefault(tracking_key, []).append([domain_a, domain_b])
        save_domains(data)
        print(f"📒 domains.json updated — {args.count} new {args.mode} run(s) recorded as explored.")
    else:
        if args.mode == "janusian":
            if not args.domain_a:
                raise SystemExit("Provide --domain-a, or use --autonomous --count N (janusian mode takes one domain).")
            print(f"{MODE_ICON[args.mode]} {MODE_VERB[args.mode]}: {args.domain_a}")
            markdown_output = run_hypothesis(args.domain_a, model=args.model, mode="janusian")
            output_file = save_hypothesis(args.domain_a, None, markdown_output, mode="janusian")
            print(f"✅ Saved to {output_file}")
        else:
            if not args.domain_a or not args.domain_b:
                raise SystemExit("Provide --domain-a and --domain-b, or use --autonomous --count N.")
            print(f"{MODE_ICON[args.mode]} {MODE_VERB[args.mode]}: {args.domain_a}  ×  {args.domain_b}")
            markdown_output = run_hypothesis(args.domain_a, args.domain_b, model=args.model, mode=args.mode)
            output_file = save_hypothesis(args.domain_a, args.domain_b, markdown_output, mode=args.mode)
            print(f"✅ Saved to {output_file}")


if __name__ == "__main__":
    main()
