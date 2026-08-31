#!/usr/bin/env python3
"""
sharpen_hypothesis_llm.py — COA 2d, automated (2026-08-30, revised same day).

sharpen_hypothesis.py (the original COA 2d ritual) records a sharpening a
human already did by hand -- it takes --soft-retired/--chimera/--hard-claim
as command-line strings someone has to have already invented, and just
formats them into the hypothesis file. This script automates the half of
that ritual that's real automation, and deliberately does NOT automate the
half that turned out not to be automatable.

What's real and kept: given a soft hypothesis, an LLM reliably drafts a
candidate hard reformulation, and correctly DECLINES rather than forcing
one when no real angle exists (confirmed directly: 2 of 3 real backlog
samples this session declined outright, with no candidate written). The
candidate's real-world novelty is then re-verified with the exact same
OpenAI web_search classify() the rest of this pipeline runs on -- proven,
reliable machinery, not a new rubric -- and a candidate that comes back
COLLISION/NO_SIGNAL/FACT_CHECK_FAIL is killed automatically, the same way
the original manual ritual killed Game Theory x Music (DiCola COLLISION).

What's NOT automated, on purpose, after a real test proved it shouldn't
be: whether a hard claim is *actually* concrete rather than soft-dressed-
as-hard. Two different LLM-judge rubrics were built and calibrated against
the three real hard claims already sent or ready (Aronson, Phillips,
Schooler) plus one genuinely weak generated claim (Trust Variance x ZK-
proofs). Neither rubric reliably separated them:

    rubric        | weak (should=SOFT) | Aronson | Phillips | Schooler
    original      | CONCRETE (wrong)   | SOFT(wrong) | CONCRETE(right) | SOFT(wrong)
    tightened     | SOFT (right)       | SOFT(wrong) | SOFT(wrong)     | SOFT(wrong)

Tightening the rubric to specifically reject "operational-sounding filler"
didn't fix it -- it broke worse, rejecting all three of the real, already-
sent, human-approved emails as soft. That is not a wording problem to be
prompt-engineered away; it is real evidence that "is this concrete" sits
closer to the kind of expert judgment a person applies reading one and
just knowing, than to something a single LLM-judge call reliably
approximates. Kept here, unused, for institutional memory -- so nobody
re-adds an auto-gate on this specific kind of judgment without re-reading
why it was tried and dropped the same day.

So: this script drafts candidates and kills the real duds (via re-verify),
and hands you every surviving candidate unfiltered, clearly marked as a
candidate, not a verdict. The one thing you did that a script couldn't --
reading a claim and knowing it's real -- stays yours.

Usage:
    python3 sharpen_hypothesis_llm.py hypotheses/<slug>.md
    python3 sharpen_hypothesis_llm.py --backlog
    python3 sharpen_hypothesis_llm.py --backlog --limit 3
"""
import argparse
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sharpen_hypothesis import (
    VER_DIR,
    resolve_path,
    slug_from_path,
    soft_claim_preview,
    build_revision_banner,
    inject_revision_banner,
    append_hard_query_block,
)
from verify_hypothesis import client, classify, detect_mode, title_and_domains, load_rubric
from token_tracker import log_usage
from retry import call_with_retry

HERE = os.path.dirname(os.path.abspath(__file__))
EMAILS_DIR = os.path.join(HERE, "outreach", "emails")
MANIFEST_PATH = os.path.join(HERE, "outreach", "packets_manifest.json")

# 2026-08-31: strict schema, replacing {"type": "json_object"}. hard_claim
# and could_not_sharpen_reason are genuinely nullable (a real, honest decline
# is a valid output, not an error) -- expressed as ["string", "null"] per
# strict mode's documented nullable-field pattern, both still required keys
# so the model can never simply omit one. The real retry logic below (decline
# without a reason -> ask again) is unchanged; json.loads() still gives
# Python None for a JSON null either way, so gen.get(...) behaves identically.
HARD_CLAIM_SCHEMA = {
    "type": "object",
    "properties": {
        "soft_retired": {"type": "string", "description": "One line naming the soft framing being retired."},
        "chimera": {"type": "string", "description": "A short named identity for the hard, fused system."},
        "hard_claim": {"type": ["string", "null"], "description": "The single hard question, or null if you genuinely cannot find a hard, falsifiable reformulation for this pairing."},
        "could_not_sharpen_reason": {"type": ["string", "null"], "description": "null if hard_claim is set; otherwise a real, specific one-sentence reason -- never leave both null."},
    },
    "required": ["soft_retired", "chimera", "hard_claim", "could_not_sharpen_reason"],
    "additionalProperties": False,
}


# --- Tried, calibrated against real ground truth, and deliberately NOT
# wired into the pipeline below -- see the module docstring's calibration
# table for why. Left here so the evidence survives, not just the verdict.
def mechanical_concreteness_check(hard_claim: str):
    raise NotImplementedError(
        "Retired 2026-08-30 -- neither this nor the adversarial LLM-judge "
        "version reliably separated real good hard claims from real soft "
        "ones when calibrated against the three actual sent/ready emails. "
        "See this module's own docstring for the real calibration table. "
        "Do not re-wire this into sharpen_one() without re-testing against "
        "Aronson/Phillips/Schooler as ground truth first."
    )


def generate_hard_claim(title: str, mode: str, domains: list, soft_text: str) -> dict:
    """The real, kept half: draft ONE candidate hard reformulation, or
    honestly decline if no real angle exists. Real examples given as
    few-shot grounding are the three that actually got sent/readied."""
    system_prompt = (
        "You are sharpening a soft, hand-wavy cross-domain hypothesis into a hard, "
        "operationally specific, falsifiable research question -- the exact discipline "
        "Exponent Labs' Eureka Engine uses before contacting a real researcher. A soft "
        "claim just says two things are connected or similar. A hard claim names a "
        "genuine mechanism or bidirectional relationship between two real, specific "
        "things, phrased as ONE single question, and it distinguishes itself from the "
        "obvious soft/trivial/already-known alternative somewhere in the question.\n\n"
        "Three real hard claims that were actually sent to real professors:\n"
        '1. "Can a swarm use collective environmental / cavity resonance as a stigmergic '
        "blackboard — configuration changes the resonant field, and the resonant field "
        "changes configuration — such that under chamber-geometry change the swarm "
        'spontaneously finds formations that exploit resonance without being given the '
        'global solution?"\n'
        '2. "Can a programmable magnetic-field manifold function as the reinforcement '
        "contingency itself — response-contingent field exposure producing classic "
        "schedule signatures under yoked controls — rather than as background exposure "
        'or a discriminative cue for food/shock?"\n'
        '3. "For a single unfinished creative work left incomplete — not a break-then-'
        "return incubation task — does longer stuck duration both cut interim word/page "
        "count and raise judged novelty of the eventual finished piece relative to "
        "matched projects finished without a block, or does existing incubation / "
        'mind-wandering work already cover that dual role under another name?"\n\n'
        "Never invent a citation or claim something unverified as fact. If you genuinely "
        "cannot find a hard, falsifiable reformulation for this specific pairing, set "
        "hard_claim to null AND you MUST fill in could_not_sharpen_reason with a real, "
        "specific one-sentence reason (never leave it null too -- that's an incomplete "
        "answer)."
    )
    user_prompt = f"Title: {title}\nMode: {mode}\nDomain(s): {', '.join(domains)}\n\nSoft claim (from the hypothesis's own §3/§4):\n{soft_text[:1200]}"

    last = None
    for attempt in range(2):
        resp = call_with_retry(
            client.chat.completions.create,
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.4,
            response_format={"type": "json_schema", "json_schema": {"name": "hard_claim_candidate", "schema": HARD_CLAIM_SCHEMA, "strict": True}},
        )
        log_usage("sharpen", "gpt-4o", resp.usage)
        gen = json.loads(resp.choices[0].message.content)
        # The one thing worth mechanically enforcing here: if it declined,
        # it has to say why. Not a concreteness judgment -- just "did you
        # follow the one instruction that's actually checkable."
        if gen.get("hard_claim") or gen.get("could_not_sharpen_reason"):
            return gen
        last = gen
        user_prompt += "\n\nYou declined but gave no could_not_sharpen_reason. You must state one specific reason this time."
    return last


def draft_candidate_email_md(slug: str, chimera: str, hard_claim: str) -> str:
    """Matches the CONFIRMED gold template (verified against the real
    Gmail send for Aronson/Resonant Swarm, 2026-08-29). Explicitly labeled
    a CANDIDATE, not a send-ready packet -- the concreteness call is
    yours, not this script's."""
    path = os.path.join(EMAILS_DIR, f"email-{slug}.md")
    content = f"""# Email — {chimera} (UNREVIEWED CANDIDATE)

**Status:** DRAFT — auto-generated candidate, NOT reviewed for concreteness, NOT sent
**Hypothesis:** `{slug}`
**Contact:** _(find and verify a real, current contact — do not send without one)_

This candidate survived real-novelty re-verify (ADJACENT_ACTIVE) but was **not**
run through any automated "is this actually concrete" check — that check was
tried twice on 2026-08-30 and both versions failed to reliably tell a real good
claim from a real soft one, even calibrated against the actual sent emails.
Read the hard claim below yourself before deciding whether it's send-worthy.

---

**From:** Mike Jagdeo \\<private@exponentlabs.ai\\>
**To:** _(fill in)_
**Subject:** {chimera}

---

Prof. _(name)_,

I'm with Exponent Labs' Eureka Engine.

**{hard_claim}**

We have a syndicate of investors.

Michael Jagdeo
Exponent Labs LLC - Eureka Engine
private@exponentlabs.ai

---

## Review checklist

- [ ] Read the hard claim — is it actually concrete, or soft dressed as hard?
- [ ] Real contact found and verified (not an aggregator)
- [ ] Sign-off Michael/Rocky
- [ ] Send
- [ ] Date sent: ________
- [ ] Log ledger `outreach_status` on reply
"""
    os.makedirs(EMAILS_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def sharpen_one(path: str, dry_run: bool = False) -> dict:
    slug = slug_from_path(path)
    text = open(path, encoding="utf-8").read()
    mode = detect_mode(text)
    title, domains = title_and_domains(text, mode)
    preview = soft_claim_preview(text)
    soft_text = preview["section3"] or preview["section4"]

    print(f"  → drafting a candidate for: {title}")
    if preview["already_sharpened"]:
        print("    already has a Revision banner — skipping")
        return {"slug": slug, "status": "ALREADY_SHARPENED"}

    gen = generate_hard_claim(title, mode, domains, soft_text)
    hard_claim = gen.get("hard_claim")
    if not hard_claim:
        reason = gen.get("could_not_sharpen_reason") or "(no reason given even after retry)"
        print(f"    declined: {reason}")
        return {"slug": slug, "status": "DECLINED", "reason": reason}

    print(f"    candidate: {hard_claim}")

    # Real, proven machinery -- not a new rubric -- so this gate stays.
    rubric = load_rubric()
    result = classify(gen["chimera"], mode, domains, hard_claim, [], rubric, slug=f"{slug}-hardclaim")
    verdict = result["verdict"]
    print(f"    hard-claim re-verify: {verdict}")

    if verdict != "ADJACENT_ACTIVE":
        print(f"    killed on re-verify ({verdict}): {result.get('reasoning', '')[:200]}")
        return {"slug": slug, "status": "KILLED_ON_REVERIFY", "verdict": verdict, "hard_claim": hard_claim, "reasoning": result.get("reasoning")}

    if dry_run:
        return {"slug": slug, "status": "CANDIDATE_DRY_RUN", "chimera": gen["chimera"], "hard_claim": hard_claim}

    banner = build_revision_banner(gen["soft_retired"], "automated candidate (COA 2d, sharpen_hypothesis_llm.py) — re-verified ADJACENT_ACTIVE; concreteness NOT automatically checked, needs human read.")
    new_text = inject_revision_banner(text, banner)
    new_text = append_hard_query_block(new_text, gen["soft_retired"], gen["chimera"], hard_claim, slug)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)

    os.makedirs(VER_DIR, exist_ok=True)
    ver_path = os.path.join(VER_DIR, f"{slug}-verification.md")
    with open(ver_path, "w", encoding="utf-8") as f:
        f.write(
            f"# Verification: {slug} (COA 2d — automated candidate re-verify)\n\n"
            f"**Verifies**: `hypotheses/{slug}.md`\n"
            f"**Verified**: {date.today().isoformat()} · **Method**: OpenAI web_search (gpt-4o-mini) on the HARD claim, automated (sharpen_hypothesis_llm.py). Concreteness NOT automatically judged — see hypothesis file's own banner.\n\n"
            f"## Hard claim (candidate — not human-reviewed for concreteness)\n{hard_claim}\n\n## Verdict: **{verdict}**\n\n## What was found\n{result.get('what_was_found', '')}\n\n## Reasoning\n{result.get('reasoning', '')}\n"
        )

    email_path = draft_candidate_email_md(slug, gen["chimera"], hard_claim)
    print(f"    ✅ wrote candidate revision, verification, and draft email: {email_path}")

    return {
        "slug": slug, "status": "CANDIDATE_FOR_REVIEW", "chimera": gen["chimera"],
        "hard_claim": hard_claim, "verification_file": ver_path, "email_file": email_path,
    }


def update_manifest(results: list) -> None:
    if not os.path.exists(MANIFEST_PATH):
        return
    manifest = json.load(open(MANIFEST_PATH))
    by_slug = {p["slug"]: p for p in manifest["packets"]}
    for r in results:
        p = by_slug.get(r["slug"])
        if not p:
            continue
        if r["status"] == "CANDIDATE_FOR_REVIEW":
            p["sharpened"] = "candidate"  # not True -- a human hasn't confirmed concreteness yet
            p["hard_claim_one_liner"] = r.get("hard_claim", "")[:120]
            p["status"] = "CANDIDATE_NEEDS_HUMAN_READ"
        elif r["status"] == "KILLED_ON_REVERIFY":
            p["status"] = f"KILLED_ON_REVERIFY ({r.get('verdict')})"
        elif r["status"] == "DECLINED":
            p["status"] = "DECLINED_NO_HARD_ANGLE"
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description="COA 2d, automated candidate drafting: generate + real re-verify; concreteness stays a human call")
    parser.add_argument("hypothesis", nargs="?", help="Path or slug of a hypothesis .md")
    parser.add_argument("--backlog", action="store_true", help="Run every packet currently NEEDS_SHARPEN in outreach/packets_manifest.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen; write nothing")
    args = parser.parse_args()

    if args.backlog:
        if not os.path.exists(MANIFEST_PATH):
            raise SystemExit(f"No manifest at {MANIFEST_PATH}")
        manifest = json.load(open(MANIFEST_PATH))
        targets = [p["slug"] for p in manifest["packets"] if p.get("sharpened") not in (True, "candidate")]
        if args.limit:
            targets = targets[: args.limit]
    else:
        if not args.hypothesis:
            raise SystemExit("Pass a hypothesis file/slug, or use --backlog")
        targets = [slug_from_path(resolve_path(args.hypothesis))]

    print(f"Drafting candidates for {len(targets)} hypothesis(es){' (dry run)' if args.dry_run else ''}...\n")
    results = []
    for slug in targets:
        try:
            path = resolve_path(slug)
            results.append(sharpen_one(path, dry_run=args.dry_run))
        except (Exception, SystemExit) as e:
            # resolve_path() raises SystemExit (not Exception) on a missing
            # file -- real case, hit immediately on the first --backlog run:
            # some packets_manifest.json entries are pre-existing case
            # studies with no real hypothesis .md file to sharpen from.
            # Report and move on rather than letting one bad slug kill the
            # whole batch.
            print(f"    ! FAILED on {slug}: {e}")
            results.append({"slug": slug, "status": f"ERROR: {e}"})
        print()

    print("=" * 60)
    print(f"Done. {len(results)} processed.")
    for r in results:
        print(f"  {r['status']:24s} {r['slug']}")

    if not args.dry_run:
        update_manifest(results)
        print(f"\nUpdated {MANIFEST_PATH}")

    n_candidates = sum(1 for r in results if r["status"] == "CANDIDATE_FOR_REVIEW")
    if n_candidates:
        print(f"\n{n_candidates} real candidate(s) waiting on your read in outreach/emails/ — none are send-ready until you say so.")


if __name__ == "__main__":
    main()
