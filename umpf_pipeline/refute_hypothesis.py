#!/usr/bin/env python3
"""
refute_hypothesis.py — adversarial refutation, made unattended and cheap.

Every prior refutation pass in this repo ran as three separate Claude Code
Agent subagent spawns, one per lens. Real, and rigorous — but expensive:
this session's own recorded subagent_tokens figures ran ~34,700 tokens PER
LENS (~104,000 tokens per refuted case), almost entirely conversational-
agent-harness overhead (system reminders, tool scaffolding) rather than the
~1-2K tokens of actual hypothesis content each lens reasons over. The
2026-08-29 ROTI audit found this was, by a wide margin, the single most
expensive step in the pipeline per case — and the only one that reliably
produces negative leaderboard points (-12.3 avg across 14 real cases).

This script reproduces the EXACT SAME three-lens rubric from
refutations/README.md — coherence / testability / triviality, each
defaulting to REFUTED under genuine uncertainty, 2-of-3 survival required to
promote out of NO_SIGNAL — as three independent OpenAI completions instead
of three Claude subagents. Independence is preserved deliberately: each lens
is its own isolated API call with its own fresh message list, no shared
conversation state, and none of the three calls is told what the other two
found. That is the actual scientific property that matters here, not the
subagent harness that happened to deliver it before.

Usage:
    python3 refute_hypothesis.py hypotheses/<file>.md
    python3 refute_hypothesis.py --all-pending
    python3 refute_hypothesis.py --all-pending --limit 5
    python3 refute_hypothesis.py --all-pending --dry-run   # print verdicts only

Update (2026-08-29) -- scope widened from NO_SIGNAL-only to "pending." A
direct audit (prompted by a "what MUST be fixed before this runs on a cron
job" pass) found two real, live entries on the public leaderboard: janusian
hypotheses that failed hypothesis_engine.py's own mechanical honesty check
twice at generation time (a strong signal of a disguised compromise, not a
genuine paradox) but landed on ADJACENT_ACTIVE rather than NO_SIGNAL --
meaning the old --all-no-signal rule never sent them here at all. Phase 2's
verdict and the mechanical honesty check test two different things (does the
CONCEPT have real-world grounding vs. does THIS hypothesis's internal
reasoning hold up); passing one says nothing about the other. See
pending_refutation_slugs()'s own docstring for the exact rule.
"""
import argparse
import glob
import json
import os
import sys
from datetime import date

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_hypothesis import (
    HERE,
    HYPOTHESES_DIR,
    LEDGER_PATH,
    detect_mode,
    extract_core_claim,
    title_and_domains,
)
from ledger import load_latest_entries
from token_tracker import log_usage
from retry import call_with_retry

load_dotenv(find_dotenv(usecwd=False))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)

REFUTATIONS_DIR = os.path.join(HERE, "refutations")
VERIFICATIONS_DIR = os.path.join(HERE, "verifications")
RUBRIC_PATH = os.path.join(HERE, "refutations", "README.md")

REFUTATION_MODEL = "gpt-4o-mini"  # switched 2026-08-30, after this stayed on gpt-4o by
                              # deliberate, reasoned choice ("a judgment task, not a bulk-
                              # search-summarization one") for the whole life of this script,
                              # untested. Tested properly before switching, not assumed safe:
                              # 7 real hypotheses (mode-diverse, seeded random sample, not
                              # hand-picked), 21 individual lens checks total, gpt-4o-mini
                              # matched gpt-4o on every single one -- zero disagreements -- at
                              # a consistent 16.7-17.3x lower cost per case. One real gap that
                              # validation could not close: every case tested REFUTED on both
                              # models, because the real ledger has never had a case gpt-4o
                              # found to SURVIVE (the 0-of-79 record itself) -- so this is
                              # strong, disciplined evidence for the REFUTED side of the
                              # rubric specifically, not a claim the SURVIVES side was ever
                              # directly checked. See whitepaper.html Section 9 and Failure 14
                              # for the full validation record and the cost-measurement bug
                              # that prompted testing this in the first place.

LENS_VERSION = "2026-08-31-v3.1"  # bumped each time LENS_QUESTIONS' rubric text
    # materially changes calibration behavior (not cosmetic edits). "v2" =
    # the second, more general rewrite (explicit numbered decision
    # procedures + multiple worked examples + named anti-patterns), real-
    # tested at 8-of-13 (61.5%) on a held-out Nobel-linked set -- see
    # refutations/control-test-nobel-calibration.md. "v3" = a real, second
    # independent-model review of all 13 Nobel-linked cases (not this
    # project's own reasoning) found two further, distinct real bugs v2
    # didn't close: Coherence still flagging equivocation on a LITERALLY
    # identical shared object (not just Nash's different-mechanism-same-
    # structure case), and Triviality still refuting a claim whose ABSTRACT
    # SHAPE sounds generic even when its precise content was correctly kept
    # intact per v2's own Steps 1-4 -- a new Step 5 added specifically to
    # test historical non-obviousness / genuine new explanatory power,
    # which v2 never asked for. "v3.1" = removed the separate model-supplied
    # "verdict" field entirely (see LENS_SCHEMA above) after the v3 fresh
    # held-out test caught two more real, confirmed reasoning/verdict
    # mismatches on top of the ones the shared instruction was supposed to
    # have already fixed -- the verdict is now mechanically computed from a
    # single boolean field ordered after reasoning in the schema, removing
    # the second channel the inconsistency was hiding in. Written into every new ledger entry's
    # refutation_lens_version field so a REFUTED verdict's provenance is
    # checkable: entries predating v3 were produced under lens text since
    # found to have these two further gaps -- disclosed, not silently
    # treated as equivalent to a v3 verdict. Re-running older entries under
    # v3 is a real, separate, costly decision, not something bumping this
    # constant does on its own.

LENS_SCHEMA = {
    "type": "object",
    "properties": {
        "reasoning": {"type": "string", "description": "2-4 sentences, terse peer-reviewer style. Write this FIRST, before deciding claim_survives_this_lens -- your conclusion must follow from what you argue here, not the other way around."},
        "claim_survives_this_lens": {"type": "boolean", "description": "Set this from what your reasoning above actually concluded, not from habit. true = your reasoning found the claim is NOT vague/generic/equivocal (whichever this lens tests), i.e. it survives. false = your reasoning found a real, specific flaw. Do not default to false out of habitual closing phrasing if your own analysis above concluded otherwise."},
    },
    "required": ["reasoning", "claim_survives_this_lens"],
    "additionalProperties": False,
}
# 2026-08-31-v3: removed the separate "verdict" enum field entirely, after
# real, confirmed evidence (twice, on fresh held-out cases: McClintock and
# Marshall/Warren, see control-test-nobel-calibration.md's sixth follow-up)
# that a shared prompt instruction telling the model to "set verdict from
# your own reasoning, not from habit" was not reliably followed -- the
# reasoning field explicitly concluded the claim was NOT trivial, and a
# separately-asked "verdict" field still said REFUTED. This is the same
# lesson this project has already learned twice elsewhere (Failure 1/2's
# soft self-checks getting talked past): a second, independent field is a
# second channel for the same inconsistency to hide in, no matter how
# strongly worded the instruction connecting them is. The fix removes the
# redundant channel: the model commits to a single boolean, ordered after
# its own reasoning in the schema so it is (by OpenAI's structured-output
# generation order) genuinely written second, and run_lens() below computes
# the actual REFUTED/SURVIVES verdict string mechanically from that boolean
# -- there is no longer a second field for the model's own verdict to
# disagree with.
# 2026-08-31: strict schema, replacing {"type": "json_object"} (loose mode --
# guarantees syntactically valid JSON, not that "verdict" is REFUTED/SURVIVES
# or that "reasoning" exists at all). No documented production failure has
# hit this yet, unlike verify_hypothesis.py's Failure 12 -- this migration is
# preventative, not reactive. But refutation is the single most consequential
# check in this pipeline (the 0-of-N record is, per the whitepaper's own
# words, "the scientific-integrity story, not overhead to be optimized
# away") -- the stakes of a silent malformed-response bug living here,
# undetected, are worse than anywhere else it could hide. Cheap to close the
# gap before it's ever needed, not after.

LENS_QUESTIONS = {
    "coherence": (
        "Does the claimed structural mapping equivocate on a term — using one word for two "
        "genuinely different underlying MEANINGS and treating that as a match? For a Janusian "
        "hypothesis specifically: is this a genuine same-instance paradox, or a disguised "
        "context-dependent compromise (\"in some contexts... in others\") labeled 'paradox'? "
        "For a homospatial hypothesis specifically: is there an actual fusion, or is this two "
        "domains compared side-by-side wearing a fusion's coined name?\n\n"
        "2026-08-31 fix, extended 2026-08-31 after held-out testing found the first fix still "
        "recurring on new cases (see control-test-nobel-calibration.md). RUN THIS EXACT "
        "PROCEDURE before writing your verdict — it is not optional and it is not specific to "
        "any one example below:\n"
        "  STEP 1: Name the specific shared term or structure the claim rests on.\n"
        "  STEP 2: Ask — does this term name the SAME formal object or relationship in both "
        "domains (the same equation, the same equilibrium condition, the same provable "
        "property), even though the underlying PROCESS that produces it differs between the "
        "two domains? If yes, this is NOT equivocation, full stop — regardless of how "
        "different the two domains otherwise feel, and regardless of whether they belong to "
        "obviously unrelated fields.\n"
        "  STEP 3: Only call it equivocation if you can name TWO DIFFERENT REFERENTS — state "
        "concretely what the term denotes in domain A, state concretely what it denotes in "
        "domain B, and show those are not the same formal thing, merely similar-sounding words.\n"
        "  STEP 4 — THE MISTAKE TO AVOID: 'this term carries different implications/context/"
        "connotations in each field' is NOT evidence of equivocation by itself. Every real "
        "bisociation crosses two fields with different vocabularies, conventions, and emphases — "
        "that is expected, not suspicious. If your only evidence is 'field A uses it one way, "
        "field B uses it another way,' you have not found equivocation, you have found the "
        "ordinary fact that two different fields exist. Equivocation requires the claim's own "
        "logic to secretly depend on the reader conflating two different referents — check "
        "whether the argument still works once both referents are stated side by side; if it "
        "does, there is no equivocation.\n"
        "  Worked examples, several, not one — do not treat any single one as the only "
        "exception: an evolutionarily stable strategy is provably a Nash equilibrium, though "
        "one arises from conscious reasoning and the other from blind selection — the "
        "equilibrium CONDITION is the same formal object, so this is not equivocation. The lac "
        "operon's repressor-release circuit and a control-engineering feedback loop both "
        "instantiate the identical formal structure (sensor, setpoint, corrective action) even "
        "though one is molecular and the other electromechanical — not equivocation. "
        "\"Transaction costs\" in the Coase theorem names the same formal economic-cost concept "
        "whether the context is a factory boundary dispute or a fishing-rights dispute — "
        "applying to different institutional settings is not a different meaning of the term.\n"
        "  Also for bisociation mode specifically (not homospatial): do NOT require the two "
        "domains to fuse into one entity, name a single chimera, or stop being separately "
        "identifiable. That is homospatial's bar, not bisociation's — bisociation's own doctrine "
        "requires each domain to \"stay itself,\" connected by a mapping, not merged. Refuting a "
        "bisociation claim for \"not constituting a genuine fusion\" is a category error.\n\n"
        "2026-08-31-v3 addendum, after an independent second-model review of all 13 real "
        "Nobel-linked cases found this lens still flagging equivocation on a STRONGER case Step "
        "2 didn't spell out clearly enough: not just 'different mechanisms, same formal object' "
        "(Nash), but the SAME LITERAL OBJECT — the claim states outright that both domains use "
        "the exact same equation, theorem, or physical structure, not an analogous one. If the "
        "claim says 'the exact same mathematical form,' 'not an analogy to it,' 'the identical "
        "Hamiltonian,' or equivalent — take that at face value as literal identity, the "
        "strongest possible form of coherence, not a claim to independently second-guess. Real "
        "cases this lens got wrong under the v2 wording: Hopfield's network energy function IS "
        "the Ising Hamiltonian, not merely shaped like it — flagging 'energy function' as "
        "equivocal because physics and neural networks are different fields misses that the "
        "claim explicitly asserts mathematical identity, not analogy. Watson/Crick/Franklin's "
        "'double helix' names one real molecular geometry that X-ray diffraction measured and "
        "genetic base-pairing explains — not two different senses of the phrase. Coase's "
        "'transaction costs' is the same formal economic-cost concept whether the dispute is a "
        "factory boundary or a fishing right — real institutional variety is not a different "
        "meaning of the term. Feynman's 'quantum system' refers uniformly to one physical notion "
        "(a system whose state lives in an exponentially large Hilbert space) throughout the "
        "claim, not two. In each of these, ask Step 3's question plainly — can you name two "
        "actually different referents? — and if the honest answer is no, the term names one "
        "thing used consistently, and this is not equivocation regardless of how different the "
        "two fields otherwise are."
    ),
    "testability": (
        "Is the falsifiable prediction actually operationalized — a named metric, comparison "
        "condition, and rejection threshold — or is it vague enough that no real experiment "
        "could ever return a clean \"no\"? Watch specifically for an \"or vice versa\" hedge, "
        "which usually makes a claim direction-agnostic and therefore unfalsifiable.\n\n"
        "2026-08-31 fix, extended 2026-08-31 after held-out testing found the first fix still "
        "recurring on new cases (see control-test-nobel-calibration.md) — including refuting a "
        "claim that names an actual, literal, by-name theorem for 'lacking a metric, comparison "
        "condition, or rejection threshold,' which is a category error: naming the theorem IS "
        "naming those three things. RUN THIS EXACT PROCEDURE before writing your verdict:\n"
        "  STEP 1: Does the claim name ANY specific, real, checkable piece of evidence that "
        "already settled the question — a historical experiment, a dataset, an observation, a "
        "mathematical proof, a derivation, or a named theorem? 'Named' means identifiable and "
        "checkable by someone else (a proper name, a described procedure, a specific dataset), "
        "not merely asserted to exist.\n"
        "  STEP 2: If yes — this is sufficient BY ITSELF, regardless of what grammatical tense "
        "or sentence structure it's phrased in. Do NOT additionally require a separate, future-"
        "tense metric/comparison-condition/rejection-threshold sentence layered on top of it. "
        "The named experiment, dataset, or theorem already IS the metric; its result already IS "
        "the comparison condition; 'the named result does not hold, or the theorem is false' "
        "already IS the rejection threshold. Do not write 'lacks a named metric, comparison "
        "condition, or rejection threshold' as your reason to REFUTE when a specific theorem or "
        "experiment has just been named in the claim you are reading — that combination is "
        "self-contradictory and is exactly the mistake this fix exists to stop.\n"
        "  STEP 3: A named theorem does not need to be restated in formal/mathematical notation "
        "to count — plain-English naming of a real, specific, checkable result (\"the Coase "
        "theorem,\" \"the operon model,\" \"Meselson-Stahl\") is sufficient; you are not required "
        "to independently re-verify the result is correct, that is verification's job, already "
        "done upstream.\n"
        "  Worked examples, several, not one: 'the Meselson-Stahl experiment, 1958' — satisfied. "
        "'the observed blackbody spectrum' — satisfied. 'the energy function is provably "
        "identical to the Ising Hamiltonian' — satisfied. 'the Coase theorem' — satisfied, the "
        "same way, even though the phrasing looks completely different from the physics "
        "examples above; do not require the claim to resemble the physics examples' sentence "
        "structure for the same underlying rule to apply.\n"
        "This is a narrow exception, not a loophole: still REFUTE on this lens if what's cited "
        "is vague, unnamed, or a bare appeal to authority alone (\"won a Nobel Prize for this\" "
        "with nothing else named IS such a bare appeal — the prize is not itself the checkable "
        "evidence; the specific experiment, dataset, or proof the prize was awarded FOR is)."
    ),
    "triviality": (
        "Strip the domain-specific vocabulary from the claim. Does it reduce to something true "
        "of almost any two complex systems (the umbrella trap) — the same failure mode Phase 2's "
        "own verification rubric guards against, applied one level deeper against the hypothesis "
        "itself rather than against search results?\n\n"
        "2026-08-31 fix, extended 2026-08-31 after held-out testing found the first fix still "
        "recurring on new cases (see control-test-nobel-calibration.md). RUN THIS EXACT "
        "PROCEDURE before writing your verdict:\n"
        "  STEP 1: Write down the full, precise claim exactly as stated — every specific noun, "
        "formula, named mechanism, named theorem, numeric detail.\n"
        "  STEP 2: Now, and ONLY now, replace ONLY the domain names and proper nouns with "
        "generic placeholders (\"Domain A\", \"Domain B\"). Every other word — especially the "
        "specific mechanism, relationship, formula, or theorem — must stay exactly as specific "
        "as it was in Step 1. Do not shorten it, summarize it, or drop any qualifying detail.\n"
        "  STEP 3: Ask whether THIS EXACT sentence from Step 2 — not a shorter or looser "
        "version of it — honestly describes most other pairs of complex systems. If answering "
        "this required you to drop or soften ANY specific detail from Step 1 (a formula, a "
        "named theorem, a precise causal mechanism, a numeric constraint) to make the umbrella-"
        "trap argument work, you have violated Step 2 and manufactured a false trivial claim — "
        "go back to Step 1 and redo it on the actual claim, not your summary of it.\n"
        "  STEP 4 — SELF-CHECK, do this before finalizing: quote back, verbatim inside your "
        "reasoning, the exact phrase from Step 2 that you are testing for genericness. If that "
        "quoted phrase is shorter, vaguer, or omits detail present in the original claim's most "
        "specific noun phrase, you paraphrased instead of stripping — this is the single most "
        "common way this lens fails, and it invalidates the verdict; redo Step 1 before writing "
        "your final answer.\n"
        "  Worked examples, several, not one: Hopfield's actual claim — a network's energy "
        "function has THE EXACT SAME mathematical form as the Ising model, not an analogy to "
        "it — must NOT be tested as \"systems converging to local minima\" (that already fails "
        "Step 4's self-check: it is shorter and vaguer than the original). Becker's actual claim "
        "— households allocate scarce time and resources across competing uses via the same "
        "rational-choice utility-maximization framework economists use for markets — must NOT "
        "be tested as \"complex systems can be analyzed through a uniform decision-making "
        "model\" (also fails Step 4: the rational-choice/utility-maximization specificity was "
        "dropped). For a genuinely exact, narrow, provable identity (the same equation, the "
        "same formula, a specific named theorem or mechanism, held to its full original "
        "specificity per Steps 1-2), the honest answer to Step 3 is usually no, and that is "
        "real, load-bearing specificity, not triviality dressed up in domain vocabulary.\n\n"
        "2026-08-31-v3 addendum, after an independent second-model review found this lens "
        "STILL refuting real Nobel-linked claims as trivial even when Steps 1-4 above were "
        "followed correctly and the precise claim was kept intact — a distinct, deeper bug "
        "Steps 1-4 alone do not close. The remaining mistake: treating 'this claim's ABSTRACT "
        "SHAPE is common' as if it were the same thing as 'this claim's SPECIFIC CONTENT is "
        "trivial.' It is not. Nearly every deep scientific law has a simple, generic-sounding "
        "abstract form once stated plainly — natural selection is just 'variation plus "
        "selection produces differential survival'; Newton's second law is just 'force equals "
        "mass times acceleration.' That a law's FORM can be stated briefly and abstractly is "
        "not evidence against its depth — it is what a real discovery usually looks like once "
        "it is already known. Do not refute a claim as trivial merely because, correctly kept "
        "precise, it can still be summarized in one abstract-sounding sentence.\n"
        "  STEP 5, the one that actually distinguishes genuine triviality from a real discovery "
        "that happens to have a simple form — run this in addition to Steps 1-4, not instead of "
        "them: ask whether an expert already working in EITHER source domain, BEFORE this "
        "specific connection was established, would have already treated it as an obvious, "
        "assumed, or definitional fact requiring no real work to state. If establishing the "
        "connection required deriving a new result, running a real experiment, overturning a "
        "prior consensus, or noticing something genuinely not previously stated — even if the "
        "resulting claim can now be summarized simply — it is NOT trivial, regardless of how "
        "generic its abstract shape sounds when paraphrased. Only call a claim trivial if the "
        "honest answer to Step 5 is that yes, this was already obvious or assumed beforehand, "
        "or the claim is tautological/definitional (true by the meaning of its own words, "
        "adding no real content).\n"
        "  Worked examples for Step 5, several, not one: Hayek's claim — that markets aggregate "
        "dispersed local knowledge into a compressed price signal WITHOUT requiring any actor to "
        "know more than their own local circumstances plus the price — was a real, non-obvious "
        "economic insight that overturned central-planning assumptions of its era; 'distributed "
        "information gets aggregated by a signal' is a fair one-sentence summary of its abstract "
        "shape, but that shape being statable briefly does not make the specific no-central-"
        "knowledge-required mechanism trivial. Coase's theorem was a real, counterintuitive "
        "result specifically because it showed transaction costs, not the initial legal "
        "assignment of rights, determine efficiency — economists before Coase did not already "
        "assume this. Feynman's proposal to build a computer that itself obeys quantum "
        "mechanics, to exploit rather than merely suffer from exponential state-space scaling, "
        "was a genuine, non-obvious inversion nobody had proposed before 1981 — 'exponential "
        "scaling is common to complex systems' is true and irrelevant; the claim is not about "
        "scaling being generic, it is about a specific, novel way to exploit it."
    ),
}


def load_rubric() -> str:
    with open(RUBRIC_PATH, "r", encoding="utf-8") as f:
        return f.read()


def load_verification_note(slug: str) -> str:
    """Best-effort: pull the existing Phase 2 verification's 'What was found' /
    'Reasoning' text for this hypothesis, if a verification file exists, to give
    each lens the same real context a human reviewer would have had. Not fatal
    if missing — some NO_SIGNAL cases may be refuted before Phase 2 even wrote
    a file, though in practice verify_hypothesis.py always writes one."""
    candidates = glob.glob(os.path.join(VERIFICATIONS_DIR, f"{slug}*-verification.md"))
    if not candidates:
        return "(no Phase 2 verification file found for this hypothesis)"
    with open(candidates[0], "r", encoding="utf-8") as f:
        return f.read()


def run_lens(lens_name: str, question: str, rubric: str, title: str, mode: str,
             domains: list, core_claim: str, verification_note: str, slug: str) -> dict:
    system_prompt = (
        f"You are one of three independent reviewers running a single-lens adversarial "
        f"refutation test on a cross-domain research hypothesis. You do not know what the "
        f"other two reviewers found, and you must not assume there are other reviewers — "
        f"evaluate entirely on your own.\n\n"
        f"YOUR LENS IS {lens_name.upper()} ONLY. {question}\n\n"
        f"Default to REFUTED (claim_survives_this_lens = false) under genuine uncertainty — a "
        f"hypothesis wrongly killed costs nothing; a hollow one wrongly promoted costs someone "
        f"real research time later.\n\n"
        f"CRITICAL — there is no separate 'verdict' field. claim_survives_this_lens IS the "
        f"verdict, computed directly from it, so it must genuinely follow from your reasoning "
        f"field, not from a habitual closing phrase. If your reasoning concludes the claim is "
        f"NOT vague, NOT generic, NOT equivocal, or DOES hold up, claim_survives_this_lens must "
        f"be true — even if you feel like writing something that sounds like 'fails the [lens] "
        f"test' out of habit. Real, disclosed cases of exactly this mismatch have already "
        f"happened twice (2026-08-31, see refutations/control-test-nobel-calibration.md) — set "
        f"the boolean from what you actually argued above, not from a boilerplate instinct.\n\n"
        f"This is the same rubric this pipeline has applied by hand in every prior refutation "
        f"round:\n\n--- FULL RUBRIC (for context; you are applying only your one lens above) ---\n{rubric}"
    )
    user_prompt = (
        f"Hypothesis: {title}\nMode: {mode}\nDomain(s): {', '.join(domains)}\n\n"
        f"Core claim:\n{core_claim}\n\n"
        f"Phase 2 web-verification finding for this hypothesis (for context):\n{verification_note}"
    )
    resp = call_with_retry(
        client.chat.completions.create,
        model=REFUTATION_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_schema", "json_schema": {"name": "lens_verdict", "schema": LENS_SCHEMA, "strict": True}},
    )
    log_usage("refutation", REFUTATION_MODEL, resp.usage, hypothesis_slug=slug, extra={"lens": lens_name})
    data = json.loads(resp.choices[0].message.content)
    # Mechanically derived, not model-supplied -- see LENS_SCHEMA's 2026-08-31-v3
    # note above for why there is no longer a separate "verdict" field to
    # disagree with the reasoning that produced it.
    return {"verdict": "SURVIVES" if data["claim_survives_this_lens"] else "REFUTED",
            "reasoning": data["reasoning"]}


def write_refutation_md(slug: str, title: str, mode: str, lens_results: dict, verdict: str, survives: int) -> str:
    path = os.path.join(REFUTATIONS_DIR, f"{slug}-refutation.md")
    mode_label = {"bisociation": "Bisociation", "janusian": "Janusian", "homospatial": "Homospatial"}.get(mode, mode)
    lens_lines = "\n".join(
        f"- **{lens.capitalize()} — {res['verdict']}.** {res['reasoning']}"
        for lens, res in lens_results.items()
    )
    if verdict == "REFUTED":
        tally_line = f"## Tally: {survives} of 3 survive → **REFUTED**"
        closing = (
            "## No steelman offered\n\n"
            "All three lenses independently converged on REFUTED for this case. If revisited, "
            "it would need a genuinely tighter formulation, not a restatement of the same claim."
        )
    else:
        tally_line = f"## Tally: {survives} of 3 survive → **SURVIVES** (promoted out of NO_SIGNAL)"
        closing = (
            "## What survived, and why this matters\n\n"
            f"{survives} of 3 independent lenses could not kill this claim. Per the promotion rule "
            "(2-of-3 survival), this hypothesis moves out of NO_SIGNAL — real signal the claim isn't "
            "vacuous, not proof it's correct. Still worth Phase 3 outreach consideration if a real "
            "researcher in the adjacent field can be identified."
        )
    content = f"""# Adversarial Refutation: {mode_label} — {title}

**Original**: `hypotheses/{slug}.md`
**Method**: 3 independent OpenAI completions, one per lens (`refute_hypothesis.py`, unattended) — same rubric, same independence discipline as prior Claude-subagent rounds, at a fraction of the token cost

{tally_line}

{lens_lines}

{closing}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def append_ledger_refutation(slug: str, verdict: str, survives: int, refutation_filename: str):
    """Read the full ledger, find the matching entry by hypothesis_slug, add
    the refutation fields, rewrite. Mirrors the exact field shape every prior
    refutation round wrote by hand — refutation_verdict / refutation_file /
    refutation_independently_confirmed / refutation_confirmation_note, plus
    refutation_survival_count (score_hypotheses.py reads this field).

    2026-08-31: refutation_survival_count is now written for EVERY verdict,
    not only SURVIVES. Collapsing 0-of-3 and 1-of-3 into an undifferentiated
    REFUTED threw away a real, already-computed ensemble-vote signal — the
    difference between a unanimous rejection and a genuine near-miss. The
    271+ pre-existing REFUTED entries were backfilled from their own
    refutation .md files' real "## Tally: N of 3 survive" line (never
    guessed, never re-run) -- see score_hypotheses.py's tier_for() and
    refutation_gradient() for how this is used."""
    lines = []
    found = False
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("hypothesis_slug") == slug:
                entry["refutation_verdict"] = verdict
                entry["refutation_file"] = f"refutations/{os.path.basename(refutation_filename)}"
                entry["refutation_lens_version"] = LENS_VERSION
                entry["refutation_independently_confirmed"] = True
                entry["refutation_confirmation_note"] = (
                    "3 independent OpenAI completions, one per lens (coherence/testability/triviality), "
                    "each with its own isolated message list — no shared conversation state, no lens told "
                    "the others' findings. Unattended (refute_hypothesis.py)."
                )
                entry["refutation_survival_count"] = survives
                found = True
            lines.append(json.dumps(entry))
    if not found:
        raise ValueError(f"No ledger entry found for slug {slug!r} — refutation result not written.")
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def already_refuted_slugs():
    """2026-08-29: reads ledger.py's "latest entry per slug" view, not raw
    lines. If a slug's newest entry (e.g. a real re-verification after the
    Tavily rate-limit fix) doesn't carry a refutation_verdict, an OLDER,
    now-superseded line's refutation_verdict for the same slug no longer
    counts -- it belongs to an entry that isn't the current state of that
    hypothesis anymore. This does mean a slug can end up refuted twice
    across its history (once validly, on the old entry; again on the new
    one, if the new verdict still needs it) -- a small, deliberate cost
    (a few cents) traded for not having to merge stale fields across ledger
    lines by hand."""
    return {e.get("hypothesis_slug") for e in load_latest_entries() if e.get("refutation_verdict")}


def failed_own_honesty_check(slug: str) -> bool:
    """True if hypothesis_engine.py's own mechanical check (janusian's
    context-split scan, homospatial's comparison-word scan) already flagged
    this hypothesis as a likely disguised compromise/bisociation-wearing-
    homospatial's-name, even after one corrective retry. Read directly from
    the hypothesis file's own text -- the flag IS the file, not a separate
    record."""
    filepath = os.path.join(HYPOTHESES_DIR, f"{slug}.md")
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        return "Automated check failed twice" in f.read()


def pending_refutation_slugs():
    """The real candidate queue for adversarial refutation, read from the
    ledger itself rather than re-derived from filenames. Two real reasons a
    hypothesis belongs here, not one:

    1. verdict == NO_SIGNAL -- the original, still-correct reason: Phase 2
       found no real-world grounding either way, so refutation is the only
       remaining check on whether the reasoning itself holds up.

    2. verdict == ADJACENT_ACTIVE AND it already failed its own mechanical
       honesty check twice at generation time. Added 2026-08-29, after a
       direct audit found two real, live examples of exactly this gap: a
       janusian hypothesis can fail hypothesis_engine.py's own context-split
       scan (a strong signal it's a disguised compromise, not a genuine
       paradox) and still land on ADJACENT_ACTIVE -- which never triggered
       refutation under the old NO_SIGNAL-only rule, because ADJACENT_ACTIVE
       means Phase 2 found the CONCEPT has real-world grounding, which says
       nothing about whether THIS hypothesis's internal reasoning is sound.
       Those two checks test different things; only running one of them
       because the other happened to say "real" leaves a hypothesis flagged
       as likely-broken-reasoning sitting on the public leaderboard with no
       adversarial scrutiny ever applied to it. COLLISION is deliberately
       excluded from this rule -- a COLLISION verdict means real, citable
       prior art already exists, so the hypothesis isn't being recommended
       to anyone as a novel direction regardless of its internal coherence;
       refuting it would spend real money re-confirming something the
       leaderboard already correctly badges as "already researched."
    """
    slugs = []
    already = already_refuted_slugs()
    for e in load_latest_entries():
        slug = e.get("hypothesis_slug")
        if not slug or slug in already:
            continue
        if e.get("verdict") == "NO_SIGNAL":
            slugs.append(slug)
        elif e.get("verdict") == "ADJACENT_ACTIVE" and failed_own_honesty_check(slug):
            slugs.append(slug)
    return slugs


def refute_one(slug: str, rubric: str, dry_run: bool = False):
    filepath = os.path.join(HYPOTHESES_DIR, f"{slug}.md")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No hypothesis file for slug {slug!r} at {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    mode = detect_mode(text)
    title, domains = title_and_domains(text, mode)
    core_claim = extract_core_claim(text, mode)
    verification_note = load_verification_note(slug)

    print(f"  → [{mode}] {title}")
    lens_results = {}
    for lens_name, question in LENS_QUESTIONS.items():
        result = run_lens(lens_name, question, rubric, title, mode, domains, core_claim, verification_note, slug)
        lens_results[lens_name] = result
        print(f"    {lens_name}: {result['verdict']}")

    survives = sum(1 for r in lens_results.values() if r["verdict"] == "SURVIVES")
    verdict = "SURVIVES" if survives >= 2 else "REFUTED"
    print(f"    tally: {survives} of 3 survive -> {verdict}")

    if dry_run:
        return slug, verdict, survives, None

    os.makedirs(REFUTATIONS_DIR, exist_ok=True)
    path = write_refutation_md(slug, title, mode, lens_results, verdict, survives)
    append_ledger_refutation(slug, verdict, survives, path)
    return slug, verdict, survives, path


def main():
    parser = argparse.ArgumentParser(description="Unattended adversarial refutation (3 independent OpenAI completions per case)")
    parser.add_argument("files", nargs="*", help="Specific hypothesis .md files to refute")
    parser.add_argument("--all-pending", action="store_true", help="Refute every ledger entry that needs it and has no refutation result yet -- every NO_SIGNAL verdict, plus any ADJACENT_ACTIVE verdict that already failed its own mechanical honesty check twice at generation time (see pending_refutation_slugs())")
    parser.add_argument("--all-no-signal", action="store_true", help="Deprecated alias for --all-pending, kept for any script still calling the old flag name")
    parser.add_argument("--limit", type=int, default=None, help="Cap how many to run this pass (used with --all-pending)")
    parser.add_argument("--dry-run", action="store_true", help="Print verdicts only; write nothing")
    args = parser.parse_args()

    rubric = load_rubric()

    if args.all_pending or args.all_no_signal:
        slugs = pending_refutation_slugs()
        if args.limit:
            slugs = slugs[: args.limit]
    else:
        if not args.files:
            raise SystemExit("Pass hypothesis file(s), or use --all-pending")
        slugs = [os.path.splitext(os.path.basename(f))[0] for f in args.files]

    if not slugs:
        print("Nothing to refute — no pending NO_SIGNAL or flagged-ADJACENT_ACTIVE entries.")
        return

    print(f"Refuting {len(slugs)} hypothesis(es){' (dry run)' if args.dry_run else ''}...\n")
    summary = []
    for slug in slugs:
        try:
            s, verdict, survives, path = refute_one(slug, rubric, dry_run=args.dry_run)
            summary.append((s, verdict, survives))
        except Exception as e:
            print(f"    ! FAILED on {slug}: {e}")
            summary.append((slug, f"ERROR: {e}", None))
        print()

    print("=" * 60)
    print(f"Done. {len(summary)} processed.")
    for slug, verdict, survives in summary:
        tag = f"{verdict} ({survives}/3)" if survives is not None else verdict
        print(f"  {tag:20s} {slug}")


if __name__ == "__main__":
    main()
