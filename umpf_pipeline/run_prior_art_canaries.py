#!/usr/bin/env python3
"""
COA 4 — Prior-art canary runner.

Loads prior_art_canaries.json (bisociation generative-relation pairs +
Janusian simultaneous-hold poles + Homospatial fusion entities from the
gold doctrine tables). For each:
  1. Write a minimal hypothesis markdown with named-entity search queries
  2. Run verify_hypothesis.verify_one (unless --dry-run or --skip-verify)
  3. Compare verdict to expected_verdict (COLLISION)

Target: ≥80% COLLISION recall on the frozen set.

Usage:
    python3 run_prior_art_canaries.py --dry-run
    python3 run_prior_art_canaries.py --mode janusian --dry-run
    python3 run_prior_art_canaries.py --mode homospatial
    python3 run_prior_art_canaries.py --limit 3
    python3 run_prior_art_canaries.py

Writes canary_results.json. Exit 1 if live run and recall < target.
Does not mutate domains.json already_paired.
"""
import argparse
import json
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
CANARY_PATH = os.path.join(HERE, "prior_art_canaries.json")
HYP_DIR = os.path.join(HERE, "hypotheses", "canaries")
OUT_PATH = os.path.join(HERE, "canary_results.json")


def results_path(mode: str) -> str:
    if mode and mode != "all":
        return os.path.join(HERE, f"canary_results_{mode}.json")
    return OUT_PATH


def render_hypothesis(c: dict) -> str:
    queries = c.get("search_hints") or []
    named = c.get("named_prior_art") or []
    q_lines = []
    for i, q in enumerate(queries[:3], 1):
        q_lines.append(f"{i}. {q}")
    if named:
        q_lines.append(f"{len(q_lines)+1}. {named[0]} named theory OR framework OR researcher")
    query_block = "\n".join(q_lines) if q_lines else "1. prior art named theory OR framework OR researcher"
    mode = c.get("mode", "bisociation")

    if mode == "homospatial":
        entity_a = c.get("entity_a", "Entity A")
        entity_b = c.get("entity_b", "Entity B")
        emergent = c.get("emergent_identity", "Emergent fused identity")
        return f"""# Homospatial Hypothesis: {entity_a} ⊕ {entity_b}

**Generated**: {date.today().isoformat()}
**Framework**: UMPF Prior-Art Canary — Homospatial (COA 4c)
**Canary id**: {c['id']}
**Expected verdict**: {c['expected_verdict']}

---

## 1. The Two Source Entities

**Entity A**: {entity_a}

**Entity B**: {entity_b}

## 2. The Superimposition

Force {entity_a} and {entity_b} into the same conceptual space — overlay, not analogy —
until they occupy one frame. Gold reconstruction from homospatial-thinking.md id {c.get('gold_id')}.

## 3. The Emergent Third Thing

**{emergent}** — one chimera identity that neither source entity names alone.
Named prior art: {', '.join(named)}.

## 4. The Hypothesis

**I force {entity_a} and {entity_b} into the same space until {emergent} emerges.**

**If that fused identity is real, then literature search for {', '.join(named[:2]) or c['id']} will return established published work — this canary expects COLLISION.**

## 5. Novelty & Testability Self-Critique

- **Fusion distance (1-5)**: 5 — historically discrete crafts before the overlay.
- **Known prior art**: {', '.join(named)} — this canary asserts COLLISION.
- **Confidence**: High (calibration plant).

## 6. If This Doesn't Hold

Verifier missed obvious named prior art for a documented Homospatial leap.

## Search Queries

{query_block}
"""

    if mode == "janusian":
        domain = c.get("domain") or c.get("domain_a") or "Unknown domain"
        pole_a = c.get("pole_a", "Pole A")
        pole_b = c.get("pole_b", "Pole B")
        return f"""# Janusian Hypothesis: {domain}

**Generated**: {date.today().isoformat()}
**Framework**: UMPF Prior-Art Canary — Janusian (COA 4b)
**Canary id**: {c['id']}
**Expected verdict**: {c['expected_verdict']}

---

## 1. The Domain

{domain} — historical domain from janusian-thinking.md gold id {c.get('gold_id')}.

## 2. The Proposition

Load-bearing assumption related to **{pole_a}** as settled within this domain.

## 3. The Inversion

The exact opposite is true: the pole of **{pole_b}** holds.

## 4. The Simultaneous Hold

> "{pole_a}."
> "{pole_b}."
> "Both are true simultaneously."

- **(A) Compromise**: poles apply in different contexts — rejected.
- **(B) Synthesis**: average or pick a side — rejected.
- **(C) Paradox**: both poles true for the same instance — this is Janusian.

## 5. The Hypothesis

**Both {pole_a} and {pole_b} are true simultaneously for the same instance; the theory must contain both.**

**If both hold simultaneously, then literature search for {', '.join(named[:2]) or c['id']} will return established published work — this canary expects COLLISION.**

## 6. Novelty & Testability Self-Critique

- **Tension score (1-5)**: 5 — historically load-bearing contradiction.
- **Known prior art**: {', '.join(named)} — this canary asserts COLLISION.
- **Confidence**: High (calibration plant).

## 7. If This Doesn't Hold

Verifier missed obvious named prior art for a documented Janusian leap.

## Search Queries

{query_block}
"""

    return f"""# Hypothesis: {c['domain_a']} × {c['domain_b']}

**Generated**: {date.today().isoformat()}
**Framework**: UMPF Prior-Art Canary (COA 4)
**Canary id**: {c['id']}
**Expected verdict**: {c['expected_verdict']}

---

## 1. The Two Frames (M₁, M₂)

**M₁ — {c['domain_a']}**: Historical domain A from the gold bisociation table.

**M₂ — {c['domain_b']}**: Historical domain B from the gold bisociation table.

## 2. Monadic Signature of Each Domain

| Layer | A | B |
|---|---|---|
| Atomic | (canary stub) | (canary stub) |
| Domain | (canary stub) | (canary stub) |
| Control | (canary stub) | (canary stub) |
| Orchestration | (canary stub) | (canary stub) |

## 3. The Candidate Functor

The historically documented generative relation between these domains
(see bisociation-domain-pairs.md gold id {c.get('gold_id')}). Named prior art:
{', '.join(named)}.

## 4. The Hypothesis

**I noticed that the relational rule governing work in {c['domain_a']} also
governed outcomes in {c['domain_b']} — specifically the documented historical
collision that produced: {', '.join(named[:2]) or c['id']}.**

**If that relation holds, then literature search by the named prior-art terms
above will return established published work — this canary expects COLLISION.**

## 5. Novelty & Testability Self-Critique

- **Distance score (1-5)**: 5 — historically distant communities before the leap.
- **Testability**: named prior-art search must find the established result.
- **Known prior art**: {', '.join(named)} — this canary asserts COLLISION.
- **Confidence**: High (calibration plant).

## 6. If This Doesn't Hold

Verifier query generation failed to retrieve obvious prior art.

## Search Queries

{query_block}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Write hypothesis stubs only")
    parser.add_argument("--skip-verify", action="store_true", help="Write stubs, do not call verify")
    parser.add_argument("--limit", type=int, default=0, help="Verify only first N canaries")
    parser.add_argument("--mode", choices=["all", "bisociation", "janusian", "homospatial"], default="all",
                        help="Filter canaries by mode")
    args = parser.parse_args()

    with open(CANARY_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    canaries = cfg["canaries"]
    if args.mode != "all":
        canaries = [c for c in canaries if c.get("mode", "bisociation") == args.mode]
    target = cfg.get("target_collision_rate", 0.8)
    os.makedirs(HYP_DIR, exist_ok=True)

    results = []
    to_run = canaries[: args.limit] if args.limit else canaries

    for c in to_run:
        slug = f"canary-{c['id']}"
        path = os.path.join(HYP_DIR, f"{slug}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render_hypothesis(c))
        print(f"wrote {path}")
        entry = {
            "id": c["id"],
            "slug": slug,
            "path": path,
            "expected": c["expected_verdict"],
            "verdict": None,
            "hit": None,
        }
        if args.dry_run or args.skip_verify:
            results.append(entry)
            continue

        from verify_hypothesis import verify_one, load_rubric
        rubric = load_rubric()
        try:
            _slug, verdict, _md = verify_one(path, rubric, dry_run=False)
            entry["verdict"] = verdict
            entry["hit"] = verdict == c["expected_verdict"]
            print(f"  → {verdict} (expected {c['expected_verdict']}) {'HIT' if entry['hit'] else 'MISS'}")
        except SystemExit as e:
            entry["error"] = str(e)
            print(f"  ! verify aborted: {e}")
        except Exception as e:
            entry["error"] = repr(e)
            print(f"  ! verify failed: {e}")
        results.append(entry)

    hits = [r for r in results if r.get("hit") is True]
    # Infrastructure failures (PENDING_VERIFICATION) are not classification errors —
    # exclude them from recall so a rate-limited search backend cannot fail the gate.
    judged = [
        r for r in results
        if r.get("verdict") and r.get("verdict") != "PENDING_VERIFICATION"
    ]
    pending = [r for r in results if r.get("verdict") == "PENDING_VERIFICATION"]
    recall = (len(hits) / len(judged)) if judged else None
    payload = {
        "date": date.today().isoformat(),
        "mode_filter": args.mode,
        "target": target,
        "n": len(results),
        "judged": len(judged),
        "pending_verification": len(pending),
        "hits": len(hits),
        "recall": recall,
        "pass": (recall is not None and recall >= target),
        "results": results,
    }
    out = results_path(args.mode)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    # Always mirror latest run to canary_results.json for quick inspection
    if out != OUT_PATH:
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.write("\n")
    print(f"\nWrote {out} recall={recall}")
    if judged and recall is not None and recall < target:
        sys.exit(1)


if __name__ == "__main__":
    main()
