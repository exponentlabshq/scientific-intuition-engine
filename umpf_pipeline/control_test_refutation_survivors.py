#!/usr/bin/env python3
"""
COA 5 — Planted-survivor control for adversarial refutation.

Lifetime refutation record is 0-of-N SURVIVE. That is either excellent
discrimination or a rubric that defaults to REFUTED. This script plants three
claims that *should* survive a fair coherence/testability/triviality gauntlet
(well-operationalized, non-umbrella, non-equivocating scientific claims) and
runs the same three-lens protocol used in refute_hypothesis.py.

Usage:
    python3 control_test_refutation_survivors.py
    python3 control_test_refutation_survivors.py --dry-run   # print plants only

Exit 0 if ≥1 SURVIVE; exit 1 if 0-of-3 (rubric may be over-defaulting).
Does not write to the production ledger.
"""
import argparse
import json
import os
import sys
from datetime import date

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refute_hypothesis import LENS_QUESTIONS, REFUTATION_MODEL
from token_tracker import log_usage
from retry import call_with_retry

load_dotenv(find_dotenv(usecwd=False))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set")
client = OpenAI(api_key=OPENAI_API_KEY)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "control_test_refutation_survivors_results.json")

# Planted claims: specific, operationalized, not umbrella. A fair gauntlet
# should SURVIVE at least some of these; if all die, the triviality/coherence
# lenses are likely over-defaulting REFUTED.
PLANTED = [
    {
        "id": "hooke-spring",
        "title": "Hooke's law (control plant)",
        "claim": (
            "For an ideal spring within its elastic limit, restoring force is "
            "proportional to displacement: F = −kx. Falsifiable prediction: if "
            "extension doubles under a doubled load within the elastic range, "
            "the constant k is unchanged to within 5% measurement error; outside "
            "the elastic limit the linearity fails."
        ),
    },
    {
        "id": "mendel-segregation",
        "title": "Mendelian segregation (control plant)",
        "claim": (
            "For a monohybrid cross of true-breeding parents differing in one "
            "Mendelian trait, the F2 phenotypic ratio approximates 3:1. "
            "Falsifiable prediction: in an F2 of ≥200 offspring under controlled "
            "conditions, the dominant:recessive count rejects a 1:1 null at "
            "p<0.01 while remaining consistent with 3:1 under a chi-square test."
        ),
    },
    {
        "id": "carnot-efficiency",
        "title": "Carnot efficiency bound (control plant)",
        "claim": (
            "No heat engine operating between reservoirs at T_h and T_c (kelvin) "
            "can exceed efficiency η = 1 − T_c/T_h. Falsifiable prediction: any "
            "claimed engine with measured η > 1 − T_c/T_h + 0.01 (instrument "
            "error) under those reservoir temperatures is rejected."
        ),
    },
]


def refute_plant(plant: dict) -> dict:
    """Run three independent lenses against a planted claim (no hypothesis file)."""
    results = {}
    for lens, question in LENS_QUESTIONS.items():
        system = (
            "You are one adversarial refutation lens for the Eureka Engine control test. "
            "Default to REFUTED under genuine uncertainty. Reply with exactly two lines:\n"
            "VERDICT: SURVIVES|REFUTED\n"
            "REASON: <one paragraph>\n"
            f"Lens focus: {question}"
        )
        user = (
            f"Control plant (known-good scientific claim, not a cross-domain hypothesis):\n"
            f"Title: {plant['title']}\n"
            f"Claim: {plant['claim']}\n\n"
            "If the claim is coherent, operationally falsifiable, and non-trivial "
            "as stated, VERDICT must be SURVIVES. Do not refute merely because this "
            "is not a bisociation — this is a calibration plant."
        )
        resp = call_with_retry(
            client.chat.completions.create,
            model=REFUTATION_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
        )
        log_usage("refutation_control", REFUTATION_MODEL, resp.usage, extra={"plant": plant["id"], "lens": lens})
        text = resp.choices[0].message.content or ""
        verdict = "REFUTED"
        if "VERDICT:" in text.upper():
            line = [ln for ln in text.splitlines() if "VERDICT" in ln.upper()]
            if line and "SURVIVE" in line[0].upper():
                verdict = "SURVIVES"
        results[lens] = {"verdict": verdict, "raw": text}
        print(f"  {plant['id']}/{lens}: {verdict}")
    survive_count = sum(1 for r in results.values() if r["verdict"] == "SURVIVES")
    overall = "SURVIVES" if survive_count >= 2 else "REFUTED"
    return {
        "id": plant["id"],
        "title": plant["title"],
        "survive_count": survive_count,
        "overall": overall,
        "lenses": {k: v["verdict"] for k, v in results.items()},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        for p in PLANTED:
            print(p["id"], "—", p["title"])
        return
    outcomes = []
    for p in PLANTED:
        print(f"Plant: {p['id']}")
        outcomes.append(refute_plant(p))
    survived = sum(1 for o in outcomes if o["overall"] == "SURVIVES")
    payload = {
        "date": date.today().isoformat(),
        "survived": survived,
        "total": len(outcomes),
        "outcomes": outcomes,
        "pass": survived >= 1,
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    print(f"\nSurvived {survived}/{len(outcomes)} → {OUT_PATH}")
    if survived < 1:
        print("FAIL: 0 planted survivors — refute rubric may over-default REFUTED.")
        sys.exit(1)
    print("PASS: ≥1 planted claim SURVIVES.")
    sys.exit(0)


if __name__ == "__main__":
    main()
