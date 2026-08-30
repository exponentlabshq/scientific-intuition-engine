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


def run_hypothesis(domain_a: str, domain_b: str = None, model: str = "gpt-4o-mini", mode: str = "bisociation") -> str:
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
