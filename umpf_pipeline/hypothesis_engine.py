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
from retry import call_with_retry

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
GOLD_PAIRS_PATH = os.path.join(PIPELINE_DIR, "bisociation_gold_pairs.json")
JANUSIAN_GOLD_PATH = os.path.join(PIPELINE_DIR, "janusian_gold_pairs.json")
HOMOSPATIAL_GOLD_PATH = os.path.join(PIPELINE_DIR, "homospatial_gold_pairs.json")
PROMPT_PATHS = {
    "bisociation": os.path.join(PIPELINE_DIR, "prompts", "umpf_hypothesis_prompt.md"),
    "janusian": os.path.join(PIPELINE_DIR, "prompts", "umpf_janusian_prompt.md"),
    "homospatial": os.path.join(PIPELINE_DIR, "prompts", "umpf_homospatial_prompt.md"),
}
HYPOTHESES_DIR = os.path.join(PIPELINE_DIR, "hypotheses")

# Sector tags for distance-biased pair sampling (COA 2). First matching
# keyword wins; unknown domains land in "other" and still pair freely.
_SECTOR_KEYWORDS = {
    "physical": ("physical", "physics", "mechan", "thermal", "electr", "optical",
                 "acoustic", "fluid", "bridge", "voltage", "photon", "telescope",
                 "spring", "magnetic", "climat", "ocean", "geology", "astronomy"),
    "biological": ("bio", "neuro", "immune", "genetic", "ecology", "evolution",
                   "organism", "cell", "dna", "epigenetic", "healthcare", "medical"),
    "informational": ("informational", "computer", "algorithm", "network", "database",
                      "cache", "hash", "cryptograph", "compiler", "queue", "sensor",
                      "distributed consensus", "load balanc", "telecommunication"),
    "human_social": ("human", "social", "organiz", "bureaucrat", "trust", "team",
                     "committee", "economic", "finance", "market", "law", "military",
                     "anthropolog", "urban", "institution"),
    "cognitive": ("cognitive", "psycholog", "attention", "learning", "decision",
                  "indecision", "emotion", "model adaptation"),
    "creative": ("creative", "music", "narrative", "art", "comedy", "gaming",
                 "culinary", "architecture", "album", "motif", "improvis"),
}


def _sector_of(domain: str) -> str:
    d = domain.lower()
    for sector, keywords in _SECTOR_KEYWORDS.items():
        if any(k in d for k in keywords):
            return sector
    return "other"


def _pair_distance_weight(a: str, b: str) -> float:
    """Higher weight = more preferred. Cross-sector pairs beat same-sector."""
    sa, sb = _sector_of(a), _sector_of(b)
    if sa == "other" or sb == "other":
        return 1.5
    if sa == sb:
        return 0.25  # demote same-sector (often restatement, not bisociation)
    return 3.0


def load_gold_pairs(mode: str = "bisociation") -> list:
    path = {
        "janusian": JANUSIAN_GOLD_PATH,
        "homospatial": HOMOSPATIAL_GOLD_PATH,
    }.get(mode, GOLD_PAIRS_PATH)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("pairs", [])


def few_shot_block(mode: str = "bisociation", n: int = 3) -> str:
    """Rotate 2–3 gold exemplars into the system prompt (COA 2 / 2b / 2c)."""
    pairs = load_gold_pairs(mode)
    if not pairs:
        return ""
    day_seed = int(datetime.now(timezone.utc).strftime("%Y%m%d"))
    offset = {"janusian": 17, "homospatial": 31}.get(mode, 0)
    rng = random.Random(day_seed + offset)
    sample = rng.sample(pairs, k=min(n, len(pairs)))
    if mode == "janusian":
        lines = [
            "",
            "## Gold Janusian simultaneous-hold exemplars (style only — do not copy poles)",
            "",
            "These are Rothenberg-style reconstructions. Match their *form* "
            "(two contradictory poles true at once for the same instance), not their content. "
            "Signature: “Both of these apparently incompatible things are true.”",
            "",
        ]
        for p in sample:
            label = p.get("thinker_discovery") or p.get("synthesis") or "?"
            poles = f"{p.get('pole_a', '?')} / {p.get('pole_b', '?')}"
            lines.append(
                f"- ({label} — {poles}) {p.get('first_person_sentence', '').strip()}"
            )
    elif mode == "homospatial":
        lines = [
            "",
            "## Gold Homospatial fusion exemplars (style only — do not copy entities)",
            "",
            "These are Rothenberg-style reconstructions. Match their *form* "
            "(two discrete entities forced into the same space until a new identity emerges), "
            "not their content. Signature: “Put these separate things in the same place and see "
            "what new identity emerges.” One chimera at the end — never “A is like B.”",
            "",
        ]
        for p in sample:
            label = p.get("thinker_discovery") or p.get("emergent_identity") or "?"
            ents = f"{p.get('entity_a', '?')} ⊕ {p.get('entity_b', '?')} → {p.get('emergent_identity', '?')}"
            lines.append(
                f"- ({label} — {ents}) {p.get('first_person_sentence', '').strip()}"
            )
    else:
        lines = [
            "",
            "## Gold generative-relation exemplars (style only — do not copy domains)",
            "",
            "These are Koestlerian reconstructions of historical leaps. Match their "
            "*form* (a relational rule transplanted across domains), not their content:",
            "",
        ]
        for p in sample:
            lines.append(
                f"- ({p.get('insight', '?')}) {p.get('first_person_sentence', '').strip()}"
            )
    lines.append("")
    return "\n".join(lines)


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
    """Pick a domain pair not in data[tracking_key], drawn from the combined
    pool with distance-biased sampling (COA 2): cross-sector pairs are
    preferred; same-sector pairs are demoted so autonomous mode reaches for
    habitually incompatible frames rather than near-restatements."""
    used_keys = {_pair_key(a, b) for a, b in data.get(tracking_key, [])}
    pool = load_combined_pool(data)
    candidates = []
    weights = []
    for a, b in itertools.combinations(pool, 2):
        key = _pair_key(a, b)
        if key in used_keys or key in already_used_this_run:
            continue
        candidates.append((a, b))
        weights.append(_pair_distance_weight(a, b))
    if not candidates:
        raise SystemExit(f"Domain pool exhausted for {tracking_key} -- every combination has been explored. Add more domains to domains.json or rosetta_stone_domains.json.")
    return random.choices(candidates, weights=weights, k=1)[0]


def pick_distant_b(domain_a: str, data: dict, already_used_this_run: set, tracking_key: str = "already_paired") -> str:
    """Thesis-in (COA 3): Domain A is fixed (researcher challenge); sample only
    a distant Domain B from the pool, preferring cross-sector."""
    used_keys = {_pair_key(a, b) for a, b in data.get(tracking_key, [])}
    pool = load_combined_pool(data)
    a_key = domain_a.strip().lower()
    candidates = []
    weights = []
    for b in pool:
        if b.strip().lower() == a_key:
            continue
        key = _pair_key(domain_a, b)
        if key in used_keys or key in already_used_this_run:
            continue
        candidates.append(b)
        weights.append(_pair_distance_weight(domain_a, b))
    if not candidates:
        raise SystemExit("No distant Domain B left to pair against this challenge — expand the domain pool or clear already_paired.")
    return random.choices(candidates, weights=weights, k=1)[0]


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
#
# 2026-08-29 readiness audit (Failure 4, still-open at the time): the "Phonetic
# Turbulence" case passed this exact scan clean -- because the scan only ever
# checked SS3. Its own SS2 (the Superimposition) used "akin to," "reminiscent
# of," and "similar to" verbatim, unchecked. Fixed here by scanning both
# sections the prompt itself already tells the model to keep comparison-free
# (SS2's own line: "Avoid comparison language here too").
_COMPARISON_WORDS = [
    "like", "similar to", "resembling", "resembles", "as if", "akin to",
    "parallels", "much like", "just as", "reminiscent of", "mirrors", "mirroring",
]

# Same-instance-test enforcement for janusian mode. Until this fix, the
# same-instance test (see prompts/umpf_janusian_prompt.md) was a soft
# self-check ONLY -- the model was told to run it on its own draft, with no
# mechanical enforcement, unlike homospatial's comparison-word scan. The
# 2026-08-29 readiness audit's newest batch found 3 of 6 fresh janusian
# hypotheses passed that soft check while still being a disguised compromise
# ("in some contexts... in others," "apply to different types of
# models/datasets/areas") -- caught only by adversarial refutation, a step
# later and a real cost later, not by the check meant to catch it at the
# source. The same day's EMH/Nash canary hypothesis (built to test exactly
# this) reproduced it again: its own SS4(C) read "...depending on the type of
# information and the market participants involved" -- textbook context-split
# language -- and was refuted 0-of-3 on exactly that ground. Same lesson as
# homospatial's fix, applied to the sibling mode: check the actual text,
# don't trust the self-check.
_CONTEXT_SPLIT_PHRASES = [
    "depending on", "in some contexts", "in other contexts", "in certain contexts",
    "in some cases", "in other cases", "in some situations", "in other situations",
    "different contexts", "different types of", "different subpopulations",
    "context-dependent", "context dependent", "in some instances", "in other instances",
]


def _extract_section(markdown_text: str, heading_prefix: str) -> str:
    """Pull the body of one '## N. Heading' section out of the generated
    markdown, up to the next '## ' heading. Used to check specific sections,
    not the whole document (e.g. SS1's plain-terms domain descriptions are
    allowed to use ordinary language freely)."""
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


def _find_context_split_phrases(text: str) -> list:
    found = []
    lowered = text.lower()
    for phrase in _CONTEXT_SPLIT_PHRASES:
        if re.search(rf"\b{re.escape(phrase)}\b", lowered):
            found.append(phrase)
    return found


# Named-entity search-query enforcement, all three modes. All three prompt
# templates were given a soft instruction (2026-08-29) requiring at least one
# Search Query to target a specific named theory/framework/researcher, not
# just the general concept -- directly closing the gap a real canary test
# found (an EMH/Nash hypothesis's 5 auto-generated queries never once
# searched for "Andrew Lo" or "Adaptive Markets Hypothesis" by name, so
# verification never had a chance to find that real, existing collision).
# Measured real compliance on the first fresh batch after that soft
# instruction: 2 of 6 -- the same "a written instruction alone gets partially
# followed" lesson this file has already hit twice (homospatial's comparison
# words, janusian's context-split phrases). Mechanically enforced here for
# the same reason those two were: check the actual output, don't trust the
# self-check.
def _extract_queries(markdown_text: str) -> list:
    m = re.search(r"## Search Queries\s*\n(.*)", markdown_text, re.DOTALL)
    if not m:
        return []
    block = m.group(1).strip()
    raw = re.findall(r"^\d+\.\s*(.+)$", block, re.MULTILINE)
    return [q.strip().strip('"') for q in raw if q.strip()]


def _has_named_entity_query(queries: list) -> bool:
    """Crude, deliberately permissive detector -- two consecutive
    capitalized alphabetic words (a real proper noun: "Andrew Lo," "Adaptive
    Markets"), or the literal "OR" from the prompt's own explicit fallback
    pattern ("[X] named theory OR framework OR researcher"). Known, disclosed
    imprecision: a query that simply restates a capitalized multi-word domain
    name at its start (e.g. "Cognitive Cryptography learning framework") can
    false-positive, since that also reads as two consecutive capitalized
    words -- checked directly against real output. This under-catches rather
    than over-catches (a false positive skips a retry that a stricter
    detector would have triggered), but even imperfect is a real improvement
    over the prior state, which caught nothing mechanically at all -- and
    tightening this further (e.g. excluding words that appear in the
    hypothesis's own domain description) risks exactly the kind of unbounded
    bug-chasing this fix exists to stop, not extend."""
    for q in queries:
        if " OR " in q:
            return True
        words = q.split()
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            if w1.isalpha() and w2.isalpha() and len(w1) > 2 and len(w2) > 2 and w1[:1].isupper() and w2[:1].isupper():
                return True
    return False


def _replace_queries_section(markdown_text: str, new_block: str) -> str:
    return re.sub(r"## Search Queries\s*\n.*\Z", f"## Search Queries\n\n{new_block.strip()}\n", markdown_text, flags=re.DOTALL)


# =============================================================================
# 2026-08-31: strict-schema generation, replacing free-form markdown +
# regex section-extraction. Real, documented cost of the old approach:
# Failure 5 -- the self-report extractor read the wrong section for 2 of 3
# modes and captured the "1" out of "(1-5)" instead of the real value,
# silently, for the script's entire lifetime, because there was never a real
# field to read, only a string pattern to guess at. The mechanical honesty
# checks (comparison-word scans, same-instance test) had the same underlying
# fragility -- _extract_section()'s own regex is one more thing that can
# silently miss a boundary.
#
# Architecture: get STRUCTURED fields from the model (one schema per mode,
# matching that mode's real prompt template exactly), run the mechanical
# checks against those real fields directly, then RENDER the structured data
# into the exact same markdown document shape every existing consumer
# depends on (verify_hypothesis.py's section extraction, refute_hypothesis.py,
# score_hypotheses.py's hypothesis_flagged()/hypothesis_sharpened() text
# scans, prefilter_observe.py, and any human reading a Phase 3 draft). This
# is deliberately NOT a raw JSON dump replacing the document -- the document
# format is a real, load-bearing contract this migration does not break.
#
# The old free-form implementation is kept as run_hypothesis_legacy() below,
# unused but not deleted -- a real rollback path if this migration surfaces
# a problem at production scale, matching this project's own "never delete
# something working" discipline.
# =============================================================================

BISOCIATION_SCHEMA = {
    "type": "object",
    "properties": {
        "m1_description": {"type": "string", "description": "M1 (Domain A): 1-2 sentences, what actually happens in this domain, plain terms a working researcher would recognize as accurate -- not UMPF jargon yet."},
        "m2_description": {"type": "string", "description": "M2 (Domain B): same, for domain B."},
        "monadic_atomic_a": {"type": "string", "description": "Domain A: what uncertainty/absence (Maybe/Either) looks like here."},
        "monadic_atomic_b": {"type": "string", "description": "Domain B: same."},
        "monadic_domain_layer_a": {"type": "string", "description": "Domain A: what evolving state/context (State/Reader/Writer) looks like here."},
        "monadic_domain_layer_b": {"type": "string", "description": "Domain B: same."},
        "monadic_control_a": {"type": "string", "description": "Domain A: what boundary/interaction (IO/STM) looks like here."},
        "monadic_control_b": {"type": "string", "description": "Domain B: same."},
        "monadic_orchestration_a": {"type": "string", "description": "Domain A: what system-wide composition (Free/effects) looks like here."},
        "monadic_orchestration_b": {"type": "string", "description": "Domain B: same."},
        "functor_mapping": {"type": "string", "description": "The proposed mapping f: M(A) -> M(B), stated explicitly -- name what maps to what, at the layer where the correspondence is strongest. Zero comparison words (like, similar to, mirrors, akin to, resembles)."},
        "functor_condition": {"type": "string", "description": "One sentence: what would have to be true in BOTH domains for this functor to actually hold (the falsifiability condition) -- not just an assertion that it's plausible."},
        "generative_relation_sentence": {"type": "string", "description": "First-person reconstruction transplanting a RULE, not a resemblance. Exact shape: 'I noticed that the relational rule governing [X in domain A] also governed [Y in domain B] -- specifically [name the rule].' Zero comparison words."},
        "falsifiable_prediction": {"type": "string", "description": "Exact shape: 'If that relation holds, then [specific, checkable prediction] -- or vice versa.'"},
        "distance_score": {"type": "integer", "description": "1-5: how far apart are these domains in ordinary practice? 1 = same field relabeled, 5 = genuinely unrelated communities."},
        "distance_score_reasoning": {"type": "string", "description": "One sentence justifying the distance_score."},
        "testability": {"type": "string", "description": "What specific data/experiment/literature could confirm or kill this hypothesis. Say so plainly if none is known -- never invent one."},
        "known_prior_art": {"type": "string", "description": "Existing work already making this connection, if any. Say 'not verified' rather than asserting novelty you can't back up."},
        "confidence_worth_time": {"type": "string", "description": "Low / Medium / High, with one sentence of reasoning."},
        "if_doesnt_hold": {"type": "string", "description": "One sentence: the most likely reason this functor turns out superficial rather than structural."},
        "search_queries": {
            "type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 5,
            "description": "3-5 concrete search queries to verify the hypothesis or check prior art. At least one MUST search by a specific named theory/framework/researcher, not just the general concept -- if none is known, use the form '[core concept] named theory OR framework OR researcher'.",
        },
    },
    "required": ["m1_description", "m2_description", "monadic_atomic_a", "monadic_atomic_b",
                 "monadic_domain_layer_a", "monadic_domain_layer_b", "monadic_control_a", "monadic_control_b",
                 "monadic_orchestration_a", "monadic_orchestration_b", "functor_mapping", "functor_condition",
                 "generative_relation_sentence", "falsifiable_prediction", "distance_score",
                 "distance_score_reasoning", "testability", "known_prior_art", "confidence_worth_time",
                 "if_doesnt_hold", "search_queries"],
    "additionalProperties": False,
}

JANUSIAN_SCHEMA = {
    "type": "object",
    "properties": {
        "domain_description": {"type": "string", "description": "1-2 sentences, what actually happens in this domain, plain terms."},
        "proposition": {"type": "string", "description": "One sentence: the load-bearing assumption this field treats as settled. Must pass the Gate -- its exact opposite must sound genuinely absurd, not just contrarian."},
        "inversion": {"type": "string", "description": "The exact opposite, stated directly, no hedging ('on the other hand', 'it could also be')."},
        "compromise_option": {"type": "string", "description": "(A) The hedge version: 'it depends,' 'both apply differently.' This is what genuine Janusian output must NOT be."},
        "synthesis_option": {"type": "string", "description": "(B) A resolution that quietly picks a side or averages the two -- also not genuinely Janusian."},
        "is_genuine_paradox": {"type": "boolean", "description": "Commit to this BEFORE writing paradox_option, honestly: true only if you can state a real, same-instance contradiction per Rothenberg's bar (Einstein motion/rest, Bohr wave/particle -- one instance, both poles true, no context-split). false if, after genuine effort, this domain does not support one -- most domains don't, and that is a legitimate, common answer, not a failure. 2026-08-31: added after real data showed a soft 'say so honestly if you can't find one' instruction in the retry prompt was never once used across 91 real flagged cases -- the model always kept forcing a paradox-shaped answer even when its own if_doesnt_hold field, in every one of those 91 cases, already knew better. This field makes the honest decline a structural choice instead of a buried option, mirroring this project's own established lesson that a soft self-check gets talked past and a mechanical one does not."},
        "paradox_option": {"type": "string", "description": "(C) If is_genuine_paradox is true: a claim true BECAUSE both proposition and inversion are true at once, for the SAME instance -- not different instances in different contexts/subpopulations. Zero context-split language (depending on, in some contexts, different types of, etc). If is_genuine_paradox is false: say so plainly here instead -- e.g. 'No genuine same-instance paradox found; proposition and inversion apply to different [instances/conditions/contexts], which is a real compromise (A), not a paradox (C).' Do not force paradox-shaped language you don't believe."},
        "why_not_compromise_synthesis": {"type": "string", "description": "State explicitly why (A) and (B) fail to actually be Janusian, and confirm (C) holds for the same instance, same time."},
        "simultaneous_hold_sentence": {"type": "string", "description": "Exact shape: 'Both [pole A] and [pole B] are true simultaneously for the same [instance]; the theory must contain both.'"},
        "falsifiable_prediction": {"type": "string", "description": "Exact shape: 'If both [proposition] and [inversion] hold simultaneously, then [specific, checkable prediction] -- which would not be predicted by either truth held alone.'"},
        "tension_score": {"type": "integer", "description": "1-5: how load-bearing is the inverted assumption -- 1 = minor detail, 5 = foundational premise the field would consider heretical to invert."},
        "tension_score_reasoning": {"type": "string", "description": "One sentence justifying tension_score."},
        "testability": {"type": "string", "description": "What specific data/experiment/literature could confirm or kill this hypothesis. Say so plainly if none is known."},
        "known_prior_art": {"type": "string", "description": "Existing work already holding this exact contradiction, if any. Say 'not verified' if unsure."},
        "confidence_worth_time": {"type": "string", "description": "Low / Medium / High, with one sentence of reasoning."},
        "if_doesnt_hold": {"type": "string", "description": "One sentence: the most likely reason this turns out to be a compromise or synthesis wearing paradox's clothing."},
        "search_queries": {
            "type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 5,
            "description": "3-5 concrete search queries to verify the claim or check prior art. At least one MUST search by a specific named theory/framework/researcher -- if none known, use '[the domain] named theory OR framework OR researcher'.",
        },
    },
    "required": ["domain_description", "proposition", "inversion", "compromise_option", "synthesis_option",
                 "is_genuine_paradox", "paradox_option", "why_not_compromise_synthesis", "simultaneous_hold_sentence",
                 "falsifiable_prediction", "tension_score", "tension_score_reasoning", "testability",
                 "known_prior_art", "confidence_worth_time", "if_doesnt_hold", "search_queries"],
    "additionalProperties": False,
}

HOMOSPATIAL_SCHEMA = {
    "type": "object",
    "properties": {
        "entity_a_description": {"type": "string", "description": "Entity A: 1-2 sentences, plain terms, what actually happens here."},
        "entity_b_description": {"type": "string", "description": "Entity B: same, for domain B."},
        "superimposition": {"type": "string", "description": "Both entities occupying the exact same conceptual space at once -- overlaid, not side by side or connected by an arrow. Name specific mechanisms from each domain and describe what happens when forced into the same slot. Zero comparison words -- describe the overlay as a literal event happening to one merged thing, not a resemblance between two things that stay separate."},
        "emergent_entity_name": {"type": "string", "description": "A coined name for the single fused entity -- one thing, not two things related to each other."},
        "emergent_entity_description": {"type": "string", "description": "What the fused entity is, in plain terms, as if it already existed and you were describing it to someone unfamiliar with either source domain. HARD RULE: zero comparison words anywhere (like, similar to, resembling, as if, akin to, parallels, much like, just as, reminiscent of, mirrors) -- describe it in its own vocabulary, the way a chimera's anatomy is described directly, not by comparing it to its sources."},
        "fusion_sentence": {"type": "string", "description": "Exact shape: 'I force [Entity A] and [Entity B] into the same [space/frame/slot] until [named fused identity] emerges.'"},
        "falsifiable_prediction": {"type": "string", "description": "Exact shape: 'If [the emergent entity] is real, then [specific, checkable prediction that could only be tested by examining the fused entity, not either source domain alone].'"},
        "fusion_distance": {"type": "integer", "description": "1-5: how discrete/unrelated were the two source entities before fusion -- 1 = already adjacent, 5 = genuinely unrelated fields."},
        "fusion_distance_reasoning": {"type": "string", "description": "One sentence justifying fusion_distance."},
        "testability": {"type": "string", "description": "What specific data/experiment/prototype/literature could confirm or kill the hypothesis about the emergent entity. Say so plainly if none."},
        "known_prior_art": {"type": "string", "description": "Whether the emergent entity already exists under another name, or this exact fusion has been made. Say 'not verified' if unsure."},
        "confidence_worth_time": {"type": "string", "description": "Low / Medium / High, one sentence."},
        "if_doesnt_hold": {"type": "string", "description": "One sentence: the most likely reason the 'emergent third thing' turns out to just be domain A and domain B described side by side."},
        "search_queries": {
            "type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 5,
            "description": "3-5 concrete search queries to verify the claim or check prior art. At least one MUST search by a specific named entity/framework/researcher -- if none known, use '[the emergent entity] named theory OR framework OR researcher'.",
        },
    },
    "required": ["entity_a_description", "entity_b_description", "superimposition", "emergent_entity_name",
                 "emergent_entity_description", "fusion_sentence", "falsifiable_prediction", "fusion_distance",
                 "fusion_distance_reasoning", "testability", "known_prior_art", "confidence_worth_time",
                 "if_doesnt_hold", "search_queries"],
    "additionalProperties": False,
}

QUERIES_SCHEMA = {
    "type": "object",
    "properties": {
        "search_queries": {
            "type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 5,
            "description": "3-5 corrected search queries. At least one MUST search by a specific named theory/framework/researcher, not just the general concept.",
        },
    },
    "required": ["search_queries"],
    "additionalProperties": False,
}

_MODE_SCHEMA = {"bisociation": BISOCIATION_SCHEMA, "janusian": JANUSIAN_SCHEMA, "homospatial": HOMOSPATIAL_SCHEMA}


def _extract_grounding_and_rules(prompt_text: str) -> tuple:
    """Split a mode's real prompt-file text into (grounding, hard_rules) --
    the theoretical-grounding prose and hard-rules list stay exactly as
    human-authored; the markdown-template '## Output' block in between is
    NOT reused -- a schema replaces it (see build_structured_instructions)."""
    grounding = prompt_text[: prompt_text.index("## Input")].strip()
    hard_rules = prompt_text[prompt_text.index("## Hard rules"):].strip()
    return grounding, hard_rules


def build_structured_instructions(mode: str) -> str:
    """The real theoretical grounding and hard rules, verbatim from the
    prompt file, with the markdown-template mechanics replaced by a
    schema-based output instruction. The schema's own field descriptions
    (above) carry the guidance the old bracketed template placeholders used
    to -- this adapter only tells the model the OUTPUT FORMAT changed, not
    what belongs in each part."""
    grounding, hard_rules = _extract_grounding_and_rules(load_prompt(mode))
    adapter = (
        "## Output\n\n"
        "Return a structured object matching the provided schema -- NOT a markdown document. Every "
        "schema field corresponds to one piece of content from this framework's normal document "
        "structure; each field's own description tells you exactly what belongs in it. Write plain "
        "prose for each field (no markdown headers inside field values), under the same ~600-word "
        "total content budget and the same content discipline described above."
    )
    return f"{grounding}\n\n{adapter}\n\n{hard_rules}"


def _fmt_queries(queries: list) -> str:
    return "\n".join(f'{i}. "{q}"' for i, q in enumerate(queries, 1))


def render_bisociation(d: dict, domain_a: str, domain_b: str, date_str: str) -> str:
    return f"""# Hypothesis: {domain_a} × {domain_b}

**Generated**: {date_str}
**Framework**: UMPF Two-Domain Hypothesis Engine (Exponent Labs LLC)

---

## 1. The Two Frames (M₁, M₂)

**M₁ — {domain_a}**: {d['m1_description']}

**M₂ — {domain_b}**: {d['m2_description']}

## 2. Monadic Signature of Each Domain

| Layer | {domain_a} | {domain_b} |
|---|---|---|
| Atomic (Maybe/Either) | {d['monadic_atomic_a']} | {d['monadic_atomic_b']} |
| Domain (State/Reader/Writer) | {d['monadic_domain_layer_a']} | {d['monadic_domain_layer_b']} |
| Control (IO/STM) | {d['monadic_control_a']} | {d['monadic_control_b']} |
| Orchestration (Free/effects) | {d['monadic_orchestration_a']} | {d['monadic_orchestration_b']} |

## 3. The Candidate Functor

{d['functor_mapping']}

For this functor to hold, {d['functor_condition']}

## 4. The Hypothesis

1. **Generative-relation sentence (required):** {d['generative_relation_sentence']}
2. **Falsifiable prediction:** {d['falsifiable_prediction']}

## 5. Novelty & Testability Self-Critique

- **Distance score (1-5)**: {d['distance_score']} — {d['distance_score_reasoning']}
- **Testability**: {d['testability']}
- **Known prior art**: {d['known_prior_art']}
- **Confidence this is worth a researcher's time**: {d['confidence_worth_time']}

## 6. If This Doesn't Hold

{d['if_doesnt_hold']}

## Search Queries

{_fmt_queries(d['search_queries'])}
"""


def render_janusian(d: dict, domain_a: str, date_str: str) -> str:
    return f"""# Janusian Hypothesis: {domain_a}

**Generated**: {date_str}
**Framework**: UMPF Janusian Hypothesis Engine (Exponent Labs LLC)

---

## 1. The Domain

{d['domain_description']}

## 2. The Proposition

{d['proposition']}

## 3. The Inversion

The exact opposite is true: {d['inversion']}

## 4. The Simultaneous Hold

> "{d['proposition']}"
> "{d['inversion']}"
> "Both are true simultaneously."

- **(A) Compromise**: {d['compromise_option']}
- **(B) Synthesis**: {d['synthesis_option']}
- **(C) Paradox** (model's own honest assessment: {'genuine' if d['is_genuine_paradox'] else 'NOT genuine -- declined honestly, see below'}): {d['paradox_option']}

{d['why_not_compromise_synthesis']}

## 5. The Hypothesis (The Third Thing)

1. **Simultaneous-hold sentence (required):** {d['simultaneous_hold_sentence']}
2. **Falsifiable prediction:** {d['falsifiable_prediction']}

## 6. Novelty & Testability Self-Critique

- **Tension score (1-5)**: {d['tension_score']} — {d['tension_score_reasoning']}
- **Testability**: {d['testability']}
- **Known prior art**: {d['known_prior_art']}
- **Confidence this is worth a researcher's time**: {d['confidence_worth_time']}

## 7. If This Doesn't Hold

{d['if_doesnt_hold']}

## Search Queries

{_fmt_queries(d['search_queries'])}
"""


def render_homospatial(d: dict, domain_a: str, domain_b: str, date_str: str) -> str:
    return f"""# Homospatial Hypothesis: {domain_a} ⊕ {domain_b}

**Generated**: {date_str}
**Framework**: UMPF Homospatial Hypothesis Engine (Exponent Labs LLC)

---

## 1. The Two Source Entities

**Entity A — {domain_a}**: {d['entity_a_description']}

**Entity B — {domain_b}**: {d['entity_b_description']}

## 2. The Superimposition

{d['superimposition']}

## 3. The Emergent Third Thing

The emergent entity is termed **{d['emergent_entity_name']}**. {d['emergent_entity_description']}

## 4. The Hypothesis

1. **Fusion sentence (required):** {d['fusion_sentence']}
2. **Falsifiable prediction:** {d['falsifiable_prediction']}

## 5. Novelty & Testability Self-Critique

- **Fusion distance (1-5)**: {d['fusion_distance']} — {d['fusion_distance_reasoning']}
- **Testability**: {d['testability']}
- **Known prior art**: {d['known_prior_art']}
- **Confidence this is worth a researcher's time**: {d['confidence_worth_time']}

## 6. If This Doesn't Hold

{d['if_doesnt_hold']}

## Search Queries

{_fmt_queries(d['search_queries'])}
"""


_RENDER = {"bisociation": render_bisociation, "janusian": render_janusian, "homospatial": render_homospatial}


def run_hypothesis(domain_a: str, domain_b: str = None, model: str = "gpt-4o-mini", mode: str = "bisociation") -> str:
    """Structured generation + deterministic render-to-markdown. See the
    module-level comment above BISOCIATION_SCHEMA for the full rationale.
    Same signature and return contract as the legacy implementation
    (run_hypothesis_legacy, kept below) -- callers in main() are unchanged."""
    instructions = build_structured_instructions(mode)
    instructions = instructions.rstrip() + few_shot_block(mode, 3)
    schema = _MODE_SCHEMA[mode]
    user_content = f"DOMAIN: {domain_a}" if mode == "janusian" else f"DOMAIN A: {domain_a}\n\nDOMAIN B: {domain_b}"
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": user_content},
    ]
    schema_name = f"{mode}_hypothesis"
    resp = call_with_retry(
        client.chat.completions.create,
        model=model,
        messages=messages,
        temperature=0.4,
        response_format={"type": "json_schema", "json_schema": {"name": schema_name, "schema": schema, "strict": True}},
    )
    log_usage("generation", model, resp.usage, extra={"mode": mode, "retry": False})
    data = json.loads(resp.choices[0].message.content)
    generated_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Same "collect flags, append once at the very end" discipline as the
    # legacy implementation (Failure 9's fix) -- structurally simpler here
    # since there's no regex section-replacement that could clobber an
    # earlier flag; render() runs exactly once, after every check.
    honesty_flags = []

    if mode == "bisociation":
        check_text = " ".join([data["functor_mapping"], data["functor_condition"],
                                data["generative_relation_sentence"], data["falsifiable_prediction"]])
        violations = _find_comparison_words(check_text)
        has_relation_form = bool(re.search(
            r"(i noticed|relational rule|generative relation|the rule governing)",
            data["generative_relation_sentence"], re.IGNORECASE,
        ))
        if violations or not has_relation_form:
            reason = []
            if violations:
                reason.append(f"analogy language ({', '.join(violations)})")
            if not has_relation_form:
                reason.append("missing generative-relation sentence form")
            print(f"  ⚠️  Bisociation functor/hypothesis failed generative-relation check ({'; '.join(reason)}) — retrying once...")
            correction = (
                f"Your functor_mapping/functor_condition/generative_relation_sentence/falsifiable_prediction "
                f"fields failed the generative-relation check: {'; '.join(reason)}.\n"
                f"generative_relation_sentence as written: \"{data['generative_relation_sentence'][:600]}\"\n\n"
                "Return the FULL corrected object again (same schema). generative_relation_sentence must open "
                "with a first-person generative-relation sentence transplanting a *rule* (not a resemblance): "
                "'I noticed that the relational rule governing X also governed Y — specifically [rule].' "
                "Zero comparison words (like, similar to, mirrors, akin to, resembles) anywhere in "
                "functor_mapping, functor_condition, generative_relation_sentence, or falsifiable_prediction."
            )
            messages.append({"role": "assistant", "content": json.dumps(data)})
            messages.append({"role": "user", "content": correction})
            resp2 = call_with_retry(client.chat.completions.create, model=model, messages=messages, temperature=0.4,
                                     response_format={"type": "json_schema", "json_schema": {"name": schema_name, "schema": schema, "strict": True}})
            log_usage("generation", model, resp2.usage, extra={"mode": mode, "retry": True})
            data = json.loads(resp2.choices[0].message.content)
            check_text2 = " ".join([data["functor_mapping"], data["functor_condition"],
                                     data["generative_relation_sentence"], data["falsifiable_prediction"]])
            rem = _find_comparison_words(check_text2)
            rel_ok = bool(re.search(r"(i noticed|relational rule|generative relation|the rule governing)",
                                     data["generative_relation_sentence"], re.IGNORECASE))
            if rem or not rel_ok:
                print("  ⚠️  Retry still failed generative-relation check — flagging in output.")
                honesty_flags.append(
                    "**⚠️ Automated check failed twice:** §3/§4 still lack a clean generative-relation "
                    "transplant (analogy language and/or missing relational-rule sentence) after one "
                    "corrective retry. Treat this as resemblance wearing bisociation's name — not a "
                    "thesis-grade lead until rewritten."
                )
            else:
                print("  ✅ Retry passed — generative-relation form clean.")
        else:
            print("  ✅ §3/§4 passed the generative-relation check on the first attempt.")

    if mode == "homospatial":
        check_text = " ".join([data["superimposition"], data["emergent_entity_description"]])
        violations = _find_comparison_words(check_text)
        full_text = " ".join([data["superimposition"], data["emergent_entity_description"],
                               data["fusion_sentence"], data["falsifiable_prediction"]])
        has_fusion_form = bool(re.search(
            r"(overlay|superimpos|fus(e|ed|ion)|emergent|same (conceptual )?space|"
            r"same (frame|slot|place)|chimera|one (entity|thing|identity)|force[d]? .* into|"
            r"occupy(ing)? the same)", full_text, re.IGNORECASE,
        ))
        if violations or not has_fusion_form:
            reason = []
            if violations:
                reason.append(f"comparison language ({', '.join(violations)})")
            if not has_fusion_form:
                reason.append("missing fusion/overlay signature")
            print(f"  ⚠️  Homospatial superimposition/emergent-entity failed fusion check ({'; '.join(reason)}) — retrying once...")
            correction = (
                f"Your superimposition/emergent_entity_description fields failed the Homospatial fusion "
                f"check: {'; '.join(reason)}.\n"
                f"superimposition as written: \"{data['superimposition'][:500]}\"\n"
                f"emergent_entity_description as written: \"{data['emergent_entity_description'][:500]}\"\n\n"
                "Return the FULL corrected object again (same schema). Rothenberg's bar: actively conceive "
                "two discrete entities occupying the SAME space until a NEW identity articulates — one "
                "chimera, not 'A is like B.' superimposition = literal overlay. emergent_entity_description = "
                "name ONE fused entity in its own vocabulary (zero comparison words). Signature form: "
                "'I force A and B into the same space until Z emerges.'"
            )
            messages.append({"role": "assistant", "content": json.dumps(data)})
            messages.append({"role": "user", "content": correction})
            resp2 = call_with_retry(client.chat.completions.create, model=model, messages=messages, temperature=0.4,
                                     response_format={"type": "json_schema", "json_schema": {"name": schema_name, "schema": schema, "strict": True}})
            log_usage("generation", model, resp2.usage, extra={"mode": mode, "retry": True})
            data = json.loads(resp2.choices[0].message.content)
            check_text2 = " ".join([data["superimposition"], data["emergent_entity_description"]])
            remaining = _find_comparison_words(check_text2)
            full_text2 = " ".join([data["superimposition"], data["emergent_entity_description"],
                                    data["fusion_sentence"], data["falsifiable_prediction"]])
            fusion_ok = bool(re.search(
                r"(overlay|superimpos|fus(e|ed|ion)|emergent|same (conceptual )?space|"
                r"same (frame|slot|place)|chimera|one (entity|thing|identity)|force[d]? .* into|"
                r"occupy(ing)? the same)", full_text2, re.IGNORECASE,
            ))
            if remaining or not fusion_ok:
                print("  ⚠️  Retry still failed Homospatial fusion check — flagging in output.")
                honesty_flags.append(
                    "**⚠️ Automated check failed twice:** §2–§4 still fail Homospatial fusion "
                    "(comparison language and/or missing overlay→emergent-identity signature) after one "
                    "corrective retry. This may be bisociation mislabeled as homospatial — not a "
                    "thesis-grade fusion lead until rewritten."
                )
            else:
                print("  ✅ Retry passed — Homospatial fusion form clean.")
        else:
            print("  ✅ §2–§4 passed the Homospatial fusion check on the first attempt.")

    if mode == "janusian":
        if not data["is_genuine_paradox"]:
            # 2026-08-31: real, honest decline -- the model committed, via the
            # schema's own required boolean (not a soft escape-hatch buried in
            # a paragraph), to NOT having found a genuine same-instance
            # paradox for this domain. Real data (91 real flagged cases,
            # before this field existed) showed the old soft instruction was
            # never once used -- the model always kept forcing a paradox-
            # shaped answer even when its own if_doesnt_hold field already
            # knew better. Do not retry here: retrying would just pressure a
            # manufactured answer out of a model that already told us
            # honestly there isn't one. Do not use "may be a disguised
            # compromise" language either -- that wrongly implies dishonesty
            # when the model did the opposite of that.
            print("  ℹ️  Janusian: model honestly found no genuine same-instance paradox for this domain (is_genuine_paradox=false) — not retrying.")
            honesty_flags.append(
                "**ℹ️ No genuine same-instance paradox found (model's own honest assessment):** "
                "the model explicitly declined to force a paradox-shaped answer for this domain "
                "rather than dress a compromise as paradox_option — a real, legitimate "
                "non-result, not a disguised compromise. See §7 for its own account of why."
            )
        else:
            # 2026-08-31: real bug found and fixed while smoke-testing the
            # is_genuine_paradox field above -- this scan was checking
            # compromise_option (A) and why_not_compromise_synthesis for
            # context-split language, but (A) is SCHEMA-REQUIRED to contain
            # exactly that hedge language ("(A) The hedge version: 'it
            # depends,' 'both apply differently.'" -- it's the deliberate
            # foil paradox_option is contrasted against), and
            # why_not_compromise_synthesis legitimately needs to quote and
            # reject that same language to explain why (A)/(B) fail. Scanning
            # the combined blob meant a genuinely clean paradox_option could
            # still trip the check purely because field (A) was doing its
            # job -- confirmed live: 'Acoustics — resonance' generated a
            # clean, real same-instance paradox in (C) with zero
            # context-split language, and still failed this check because
            # (A) said 'depending on the medium and conditions,' exactly as
            # its own schema description asks it to. Only the claim that
            # actually matters -- paradox_option and simultaneous_hold_sentence
            # -- gets scanned for context-split language now.
            section_to_scan = data["paradox_option"] + " " + data["simultaneous_hold_sentence"]
            violations = _find_context_split_phrases(section_to_scan)
            full_text = (data["compromise_option"] + " " + data["synthesis_option"] + " " +
                         data["paradox_option"] + " " + data["why_not_compromise_synthesis"] + " " +
                         data["simultaneous_hold_sentence"] + " " + data["falsifiable_prediction"])
            has_hold_form = bool(re.search(
                r"(both (are )?true|simultaneously|at (the )?same time|same instance|"
                r"mutually exclusive|two necessary faces|apparent(ly)? opposite|"
                r"incompatible things are true)", full_text, re.IGNORECASE,
            ))
            if violations or not has_hold_form:
                reason = []
                if violations:
                    reason.append(f"context-split language ({', '.join(violations)})")
                if not has_hold_form:
                    reason.append("missing simultaneous-hold signature language")
                print(f"  ⚠️  Janusian simultaneous-hold failed same-instance check ({'; '.join(reason)}) — retrying once...")
                correction = (
                    f"Your paradox_option/why_not_compromise_synthesis/simultaneous_hold_sentence fields failed "
                    f"the Janusian simultaneous-hold check: {'; '.join(reason)}.\n"
                    f"paradox_option as written: \"{data['paradox_option'][:600]}\"\n\n"
                    "Return the FULL corrected object again (same schema). Rothenberg's bar: actively conceive "
                    "two contradictory ideas *simultaneously* for the SAME instance — not '[A] in context 1, "
                    "[B] in context 2.' paradox_option must state both poles true at once (Einstein motion/rest, "
                    "Bohr wave/particle). simultaneous_hold_sentence must be: 'Both [pole A] and [pole B] are "
                    "true simultaneously for the same [instance]; the theory must contain both.' Zero "
                    "context-split language. If, on reflection, you don't actually believe this is a genuine "
                    "same-instance paradox, it's fine to set is_genuine_paradox to false and say so honestly in "
                    "paradox_option instead of forcing one — that is a legitimate, complete answer here."
                )
                messages.append({"role": "assistant", "content": json.dumps(data)})
                messages.append({"role": "user", "content": correction})
                resp2 = call_with_retry(client.chat.completions.create, model=model, messages=messages, temperature=0.4,
                                         response_format={"type": "json_schema", "json_schema": {"name": schema_name, "schema": schema, "strict": True}})
                log_usage("generation", model, resp2.usage, extra={"mode": mode, "retry": True})
                data = json.loads(resp2.choices[0].message.content)
                if not data["is_genuine_paradox"]:
                    # Honest capitulation on retry -- real, legitimate outcome,
                    # not a second failure. Same non-accusatory handling as the
                    # first-attempt decline above.
                    print("  ℹ️  Janusian: model honestly declined on retry (is_genuine_paradox=false) — not a disguised compromise.")
                    honesty_flags.append(
                        "**ℹ️ No genuine same-instance paradox found (model's own honest assessment, after one retry):** "
                        "the model explicitly declined to force a paradox-shaped answer for this domain "
                        "rather than dress a compromise as paradox_option — a real, legitimate non-result, "
                        "not a disguised compromise. See §7 for its own account of why."
                    )
                else:
                    # Same fix as the first-attempt scan above -- only the
                    # claim that actually matters gets checked for
                    # context-split language, not the deliberately-hedgy
                    # foil fields.
                    section_to_scan2 = data["paradox_option"] + " " + data["simultaneous_hold_sentence"]
                    remaining = _find_context_split_phrases(section_to_scan2)
                    full_text2 = (data["compromise_option"] + " " + data["synthesis_option"] + " " +
                                  data["paradox_option"] + " " + data["why_not_compromise_synthesis"] + " " +
                                  data["simultaneous_hold_sentence"] + " " + data["falsifiable_prediction"])
                    hold_ok = bool(re.search(
                        r"(both (are )?true|simultaneously|at (the )?same time|same instance|"
                        r"mutually exclusive|two necessary faces|apparent(ly)? opposite|"
                        r"incompatible things are true)", full_text2, re.IGNORECASE,
                    ))
                    if remaining or not hold_ok:
                        print("  ⚠️  Retry still failed Janusian same-instance check — flagging in output.")
                        honesty_flags.append(
                            "**⚠️ Automated check failed twice:** §4/§5 still fail the Janusian same-instance "
                            "test (context-split and/or missing simultaneous-hold signature) after one corrective "
                            "retry, despite the model committing is_genuine_paradox=true. This may be a "
                            "disguised compromise (A) or synthesis (B) mislabeled as paradox (C) — not a "
                            "thesis-grade Janusian lead until rewritten."
                        )
                    else:
                        print("  ✅ Retry passed — Janusian simultaneous-hold clean.")
            else:
                print("  ✅ §4/§5 passed the Janusian same-instance mechanical check on the first attempt.")

    # Named-entity search-query check -- operates on the real search_queries
    # array directly now, not a regex-extracted markdown block. Targeted
    # retry: ask for JUST a corrected query list (QUERIES_SCHEMA), not the
    # whole object, since nothing else needs to change.
    if not _has_named_entity_query(data["search_queries"]):
        print("  ⚠️  No named-entity search query found — asking for a targeted correction...")
        correction = (
            "Your search_queries list did not include any query targeting a specific named theory, "
            "framework, or researcher — only general-concept queries. Return a corrected search_queries "
            "list (3-5 queries), where at least one query searches by name for a specific existing "
            "theory/framework/researcher plausibly already working this exact ground, or, if you genuinely "
            "can't think of one, a query of the form \"[core concept] named theory OR framework OR "
            "researcher\"."
        )
        messages.append({"role": "assistant", "content": json.dumps({"search_queries": data["search_queries"]})})
        messages.append({"role": "user", "content": correction})
        resp3 = call_with_retry(client.chat.completions.create, model=model, messages=messages, temperature=0.4,
                                 response_format={"type": "json_schema", "json_schema": {"name": "search_queries_only", "schema": QUERIES_SCHEMA, "strict": True}})
        log_usage("generation", model, resp3.usage, extra={"mode": mode, "retry": "queries"})
        new_queries = json.loads(resp3.choices[0].message.content)["search_queries"]
        if _has_named_entity_query(new_queries):
            print("  ✅ Retry passed — a named-entity search query is now present.")
        else:
            print("  ⚠️  Retry still has no named-entity query — flagging in output rather than looping indefinitely.")
            honesty_flags.append(
                "**⚠️ Automated check failed twice:** no Search Query targets a specific "
                "named theory, framework, or researcher, even after one corrective retry. Verification "
                "may miss an existing collision with real prior art that a more specific search would "
                "have found — read this hypothesis's verdict with that in mind."
            )
        data["search_queries"] = new_queries
    else:
        print("  ✅ Search Queries includes at least one named-entity query.")

    markdown = _RENDER[mode](data, domain_a, domain_b, generated_date) if mode != "janusian" else render_janusian(data, domain_a, generated_date)

    # Single append point, after every check has run -- same discipline as
    # the legacy implementation (Failure 9's fix), structurally guaranteed
    # here since render() only runs once, after all checks are done.
    if honesty_flags:
        markdown = markdown.rstrip() + "\n\n---\n\n" + "\n\n".join(honesty_flags) + "\n"

    return markdown


def run_hypothesis_legacy(domain_a: str, domain_b: str = None, model: str = "gpt-4o-mini", mode: str = "bisociation") -> str:
    system_prompt = load_prompt(mode)
    if mode in ("bisociation", "janusian", "homospatial"):
        system_prompt = system_prompt.rstrip() + few_shot_block(mode, 3)
    if mode == "janusian":
        user_content = f"DOMAIN: {domain_a}"
    else:
        user_content = f"DOMAIN A: {domain_a}\n\nDOMAIN B: {domain_b}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    resp = call_with_retry(client.chat.completions.create, model=model, messages=messages, temperature=0.4)
    log_usage("generation", model, resp.usage, extra={"mode": mode, "retry": False})
    generated_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_output = resp.choices[0].message.content

    # 2026-08-29 fix: every check's "still failed after one retry" flag is
    # collected here instead of being appended to raw_output immediately.
    # Real bug found by the $1 frozen-run audit: Search Queries is the LAST
    # section in every template, so a flag appended before the query-gen
    # check ran sat AFTER the Search Queries section in raw_output -- and
    # _replace_queries_section()'s regex matches "## Search Queries" to the
    # literal end of the string, silently deleting any flag that happened to
    # land in that region. Confirmed on 3 real cases in one run (2 janusian,
    # 1 homospatial) -- all landed ADJACENT_ACTIVE and should have been
    # swept into refute_hypothesis.py's widened net, none were, because the
    # flag it looks for was already gone. Fix: append nothing mid-function;
    # collect flag text here and write it ONCE, at the very end, after every
    # check (mode-specific and query-gen alike) has had its turn -- so no
    # later check's section-replacement can ever land on top of an earlier
    # check's flag again.
    honesty_flags = []

    if mode == "bisociation":
        # COA 2: analogy language in §3 functor or §4 hypothesis is failure —
        # generative-relation transplant required, not "X is like Y".
        section3 = _extract_section(raw_output, "3. The Candidate Functor")
        section4 = _extract_section(raw_output, "4. The Hypothesis")
        v3 = _find_comparison_words(section3)
        v4 = _find_comparison_words(section4)
        violations = sorted(set(v3 + v4))
        has_relation_form = bool(re.search(
            r"(i noticed|relational rule|generative relation|the rule governing)",
            section4,
            re.IGNORECASE,
        ))
        if violations or not has_relation_form:
            reason = []
            if violations:
                reason.append(f"analogy language ({', '.join(violations)})")
            if not has_relation_form:
                reason.append("missing generative-relation sentence form")
            print(f"  ⚠️  Bisociation §3/§4 failed generative-relation check ({'; '.join(reason)}) — retrying once...")
            correction = (
                f"Your §3/§4 failed the generative-relation check: {'; '.join(reason)}.\n"
                f"§3 as written: \"{section3.strip()[:800]}\"\n"
                f"§4 as written: \"{section4.strip()[:800]}\"\n\n"
                "Rewrite the ENTIRE response. §4 must open with a first-person generative-relation "
                "sentence transplanting a *rule* (not a resemblance): "
                "'I noticed that the relational rule governing X also governed Y — specifically [rule].' "
                "Then a falsifiable If-then prediction. Zero comparison words (like, similar to, mirrors, "
                "akin to, resembles) in §3 or §4."
            )
            messages.append({"role": "assistant", "content": raw_output})
            messages.append({"role": "user", "content": correction})
            resp2 = call_with_retry(client.chat.completions.create, model=model, messages=messages, temperature=0.4)
            log_usage("generation", model, resp2.usage, extra={"mode": mode, "retry": True})
            raw_output2 = resp2.choices[0].message.content
            s3r = _extract_section(raw_output2, "3. The Candidate Functor")
            s4r = _extract_section(raw_output2, "4. The Hypothesis")
            rem = sorted(set(_find_comparison_words(s3r) + _find_comparison_words(s4r)))
            rel_ok = bool(re.search(
                r"(i noticed|relational rule|generative relation|the rule governing)",
                s4r,
                re.IGNORECASE,
            ))
            if rem or not rel_ok:
                print("  ⚠️  Retry still failed generative-relation check — flagging in output.")
                honesty_flags.append(
                    "**⚠️ Automated check failed twice:** §3/§4 still lack a clean generative-relation "
                    "transplant (analogy language and/or missing relational-rule sentence) after one "
                    "corrective retry. Treat this as resemblance wearing bisociation's name — not a "
                    "thesis-grade lead until rewritten."
                )
            else:
                print("  ✅ Retry passed — generative-relation form clean.")
            raw_output = raw_output2
        else:
            print("  ✅ §3/§4 passed the generative-relation check on the first attempt.")

    if mode == "homospatial":
        section2 = _extract_section(raw_output, "2. The Superimposition")
        section3 = _extract_section(raw_output, "3. The Emergent Third Thing")
        section4 = _extract_section(raw_output, "4. The Hypothesis")
        v2 = _find_comparison_words(section2)
        v3 = _find_comparison_words(section3)
        violations = sorted(set(v2 + v3))
        # COA 2c: require fusion/overlay signature, not only absence of analogy words.
        has_fusion_form = bool(re.search(
            r"(overlay|superimpos|fus(e|ed|ion)|emergent|same (conceptual )?space|"
            r"same (frame|slot|place)|chimera|one (entity|thing|identity)|force[d]? .* into|"
            r"occupy(ing)? the same)",
            section2 + "\n" + section3 + "\n" + section4,
            re.IGNORECASE,
        ))
        if violations or not has_fusion_form:
            reason = []
            if violations:
                reason.append(f"comparison language ({', '.join(violations)})")
            if not has_fusion_form:
                reason.append("missing fusion/overlay signature")
            print(f"  ⚠️  Homospatial §2–§4 failed fusion check ({'; '.join(reason)}) — retrying once...")
            correction = (
                f"Your §2–§4 failed the Homospatial fusion check: {'; '.join(reason)}.\n"
                f"§2: \"{section2.strip()[:500]}\"\n§3: \"{section3.strip()[:500]}\"\n"
                f"§4: \"{section4.strip()[:400]}\"\n\n"
                "Rewrite the ENTIRE response. Rothenberg's bar: actively conceive two discrete entities "
                "occupying the SAME space until a NEW identity articulates — one chimera, not 'A is like B.' "
                "§2 = literal overlay. §3 = name ONE fused entity in its own vocabulary (zero comparison words). "
                "§4 = 'If [fused entity] is real, then [prediction about the fusion].' "
                "Signature form: 'I force A and B into the same space until Z emerges.'"
            )
            messages.append({"role": "assistant", "content": raw_output})
            messages.append({"role": "user", "content": correction})
            resp2 = call_with_retry(client.chat.completions.create, model=model, messages=messages, temperature=0.4)
            log_usage("generation", model, resp2.usage, extra={"mode": mode, "retry": True})
            raw_output2 = resp2.choices[0].message.content
            s2r = _extract_section(raw_output2, "2. The Superimposition")
            s3r = _extract_section(raw_output2, "3. The Emergent Third Thing")
            s4r = _extract_section(raw_output2, "4. The Hypothesis")
            remaining = sorted(set(_find_comparison_words(s2r) + _find_comparison_words(s3r)))
            fusion_ok = bool(re.search(
                r"(overlay|superimpos|fus(e|ed|ion)|emergent|same (conceptual )?space|"
                r"same (frame|slot|place)|chimera|one (entity|thing|identity)|force[d]? .* into|"
                r"occupy(ing)? the same)",
                s2r + "\n" + s3r + "\n" + s4r,
                re.IGNORECASE,
            ))
            if remaining or not fusion_ok:
                print("  ⚠️  Retry still failed Homospatial fusion check — flagging in output.")
                honesty_flags.append(
                    "**⚠️ Automated check failed twice:** §2–§4 still fail Homospatial fusion "
                    "(comparison language and/or missing overlay→emergent-identity signature) after one "
                    "corrective retry. This may be bisociation mislabeled as homospatial — not a "
                    "thesis-grade fusion lead until rewritten."
                )
            else:
                print("  ✅ Retry passed — Homospatial fusion form clean.")
            raw_output = raw_output2
        else:
            print("  ✅ §2–§4 passed the Homospatial fusion check on the first attempt.")

    if mode == "janusian":
        section4 = _extract_section(raw_output, "4. The Simultaneous Hold")
        section5 = _extract_section(raw_output, "5. The Hypothesis")
        violations = _find_context_split_phrases(section4)
        # COA 2b: require simultaneous-hold voice (Rothenberg signature), not only
        # absence of context-split. Gold form: both poles true at once / simultaneously.
        has_hold_form = bool(re.search(
            r"(both (are )?true|simultaneously|at (the )?same time|same instance|"
            r"mutually exclusive|two necessary faces|apparent(ly)? opposite|"
            r"incompatible things are true)",
            section4 + "\n" + section5,
            re.IGNORECASE,
        ))
        if violations or not has_hold_form:
            reason = []
            if violations:
                reason.append(f"context-split language ({', '.join(violations)})")
            if not has_hold_form:
                reason.append("missing simultaneous-hold signature language")
            print(f"  ⚠️  Janusian §4/§5 failed same-instance check ({'; '.join(reason)}) — retrying once...")
            correction = (
                f"Your §4/§5 failed the Janusian simultaneous-hold check: {'; '.join(reason)}.\n"
                f"§4 as written: \"{section4.strip()[:900]}\"\n"
                f"§5 as written: \"{section5.strip()[:500]}\"\n\n"
                "Rewrite the ENTIRE response from scratch. Rothenberg's bar: actively conceive two "
                "contradictory ideas *simultaneously* for the SAME instance — not '[A] in context 1, "
                "[B] in context 2.' §4(C) must state both poles true at once (Einstein motion/rest, "
                "Bohr wave/particle). §5 must be: "
                "'If both [proposition] and [inversion] hold simultaneously for the same instance, "
                "then [checkable prediction] — which neither truth alone predicts.' "
                "Zero context-split language in §4 or §5. If you cannot find a genuine same-instance "
                "paradox, say so in §7 rather than dressing a compromise as (C)."
            )
            messages.append({"role": "assistant", "content": raw_output})
            messages.append({"role": "user", "content": correction})
            resp2 = call_with_retry(client.chat.completions.create, model=model, messages=messages, temperature=0.4)
            log_usage("generation", model, resp2.usage, extra={"mode": mode, "retry": True})
            raw_output2 = resp2.choices[0].message.content
            section4_retry = _extract_section(raw_output2, "4. The Simultaneous Hold")
            section5_retry = _extract_section(raw_output2, "5. The Hypothesis")
            remaining = _find_context_split_phrases(section4_retry)
            hold_ok = bool(re.search(
                r"(both (are )?true|simultaneously|at (the )?same time|same instance|"
                r"mutually exclusive|two necessary faces|apparent(ly)? opposite|"
                r"incompatible things are true)",
                section4_retry + "\n" + section5_retry,
                re.IGNORECASE,
            ))
            if remaining or not hold_ok:
                print("  ⚠️  Retry still failed Janusian same-instance check — flagging in output.")
                honesty_flags.append(
                    "**⚠️ Automated check failed twice:** §4/§5 still fail the Janusian same-instance "
                    "test (context-split and/or missing simultaneous-hold signature) after one corrective "
                    "retry. This may be a disguised compromise (A) or synthesis (B) mislabeled as paradox "
                    "(C) — not a thesis-grade Janusian lead until rewritten."
                )
            else:
                print("  ✅ Retry passed — Janusian simultaneous-hold clean.")
            raw_output = raw_output2
        else:
            print("  ✅ §4/§5 passed the Janusian same-instance mechanical check on the first attempt.")

    # Named-entity search-query check -- runs for all three modes, after any
    # mode-specific correction above, as a lightweight PATCH retry (only the
    # Search Queries block gets regenerated, not the whole response) so it
    # can't undo a mode-specific fix that already succeeded.
    queries = _extract_queries(raw_output)
    if not _has_named_entity_query(queries):
        print("  ⚠️  No named-entity search query found — asking for a targeted correction...")
        correction = (
            "Your Search Queries list did not include any query targeting a specific named theory, "
            "framework, or researcher — only general-concept queries. Reply with ONLY a corrected "
            "Search Queries list (3-5 numbered queries, same format as before), where at least one "
            "query searches by name for a specific existing theory/framework/researcher plausibly "
            "already working this exact ground, or, if you genuinely can't think of one, a query of "
            "the form \"[core concept] named theory OR framework OR researcher\". Output nothing but "
            "the numbered list — no other text."
        )
        messages.append({"role": "assistant", "content": raw_output})
        messages.append({"role": "user", "content": correction})
        resp3 = call_with_retry(client.chat.completions.create, model=model, messages=messages, temperature=0.4)
        log_usage("generation", model, resp3.usage, extra={"mode": mode, "retry": "queries"})
        new_block = resp3.choices[0].message.content
        raw_output = _replace_queries_section(raw_output, new_block)
        if _has_named_entity_query(_extract_queries(raw_output)):
            print("  ✅ Retry passed — a named-entity search query is now present.")
        else:
            print("  ⚠️  Retry still has no named-entity query — flagging in output rather than looping indefinitely.")
            honesty_flags.append(
                "**⚠️ Automated check failed twice:** no Search Query targets a specific "
                "named theory, framework, or researcher, even after one corrective retry. Verification "
                "may miss an existing collision with real prior art that a more specific search would "
                "have found — read this hypothesis's verdict with that in mind."
            )
    else:
        print("  ✅ Search Queries includes at least one named-entity query.")

    # Single append point, after every check has run -- see the note where
    # honesty_flags is initialized for why this must happen exactly once,
    # here, and nowhere earlier.
    if honesty_flags:
        raw_output = raw_output.rstrip() + "\n\n---\n\n" + "\n\n".join(honesty_flags) + "\n"

    return _clean_output(raw_output, generated_date)


def save_hypothesis(domain_a: str, domain_b: str, markdown_output: str, mode: str = "bisociation") -> str:
    os.makedirs(HYPOTHESES_DIR, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if mode == "janusian":
        base_slug = f"{date_str}-janusian-{slugify(domain_a)}"
    elif mode == "homospatial":
        base_slug = f"{date_str}-homospatial-{slugify(domain_a)}-x-{slugify(domain_b)}"
    else:
        base_slug = f"{date_str}-{slugify(domain_a)}-x-{slugify(domain_b)}"

    slug = base_slug
    output_file = os.path.join(HYPOTHESES_DIR, slug + ".md")
    if os.path.exists(output_file):
        # 2026-08-29 fix: this used to write here unconditionally. The $1
        # frozen-run audit found a real case -- "Architecture -- modular/
        # prefab construction" and "Architecture (Creative & Performance
        # Systems) -- Atomic: ..." are two genuinely different domains that
        # both reduce to the short name "Architecture" via short_name(), so
        # they produced the identical slug. The second domain's real,
        # already-generated hypothesis silently overwrote the first's file
        # before verify_hypothesis.py ever read it -- permanent, silent data
        # loss, with domains.json left permanently marking the destroyed
        # domain "already explored" and no ledger record it was ever
        # attempted. Never overwrite silently again: disambiguate with a
        # numeric suffix and say so loudly, so whoever's watching the cycle
        # log sees it happen instead of it vanishing without a trace.
        n = 2
        while os.path.exists(output_file):
            slug = f"{base_slug}-{n}"
            output_file = os.path.join(HYPOTHESES_DIR, slug + ".md")
            n += 1
        print(f"  ⚠️  Filename collision on '{base_slug}.md' — a different hypothesis already exists there. Saved as '{slug}.md' instead of overwriting it.")

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
    parser.add_argument("--challenge", type=str, help="Thesis-in (COA 3): researcher's home domain or thesis question as Domain A; samples a distant Domain B automatically (bisociation only)")
    parser.add_argument("--autonomous", action="store_true", help="Draw fresh domain(s) from the combined pool instead of explicit args")
    parser.add_argument("--count", type=int, default=1, help="Number of hypotheses to generate in autonomous or challenge mode")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="OpenAI model to use")
    args = parser.parse_args()

    if args.challenge:
        if args.mode != "bisociation":
            raise SystemExit("--challenge is thesis-in bisociation only (researcher Domain A × distant B).")
        if args.domain_b or args.autonomous:
            raise SystemExit("--challenge is mutually exclusive with --domain-b and --autonomous.")
        data = load_domains()
        used_this_run = set()
        domain_a = args.challenge.strip()
        for i in range(args.count):
            domain_b = pick_distant_b(domain_a, data, used_this_run, tracking_key="already_paired")
            used_this_run.add(_pair_key(domain_a, domain_b))
            print(f"🎓 [{i+1}/{args.count}] Thesis-in: {domain_a}  ×  {domain_b}")
            markdown_output = run_hypothesis(domain_a, domain_b, model=args.model, mode="bisociation")
            output_file = save_hypothesis(domain_a, domain_b, markdown_output, mode="bisociation")
            print(f"✅ Saved to {output_file}")
            data.setdefault("already_paired", []).append([domain_a, domain_b])
        save_domains(data)
        print(f"📒 domains.json updated — {args.count} thesis-in run(s) recorded.")
        return

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
                raise SystemExit("Provide --domain-a and --domain-b, or use --autonomous/--challenge --count N.")
            print(f"{MODE_ICON[args.mode]} {MODE_VERB[args.mode]}: {args.domain_a}  ×  {args.domain_b}")
            markdown_output = run_hypothesis(args.domain_a, args.domain_b, model=args.model, mode=args.mode)
            output_file = save_hypothesis(args.domain_a, args.domain_b, markdown_output, mode=args.mode)
            print(f"✅ Saved to {output_file}")


if __name__ == "__main__":
    main()
