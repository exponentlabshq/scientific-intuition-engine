"""
Control test for verify_hypothesis.py's extract_self_score() -- the scorer's
own equivalent of refutations/control-test-calibration.md, built directly in
response to the 2026-08-29 readiness audit (Brian Ahuja's gap, Section 3
item 7): refutation has an adversarial control test that deliberately tries
to break it; the scorer never had one. Failure 5's scoring bug (two real
bugs, silently corrupting 39/39 scored entries) was found by accident,
investigating an unrelated audit-agent proposal -- not by any designed check.
This script is that designed check, run on purpose against synthetic
adversarial cases, not against real ledger data (which, checked separately,
contains no case-sensitivity or multi-digit-value variance today -- see the
grep audit in this session's readiness-audit follow-up).

Usage:
    python3 control_test_scorer.py
"""

import sys

sys.path.insert(0, ".")
from verify_hypothesis import extract_section, extract_self_score  # noqa: E402

CASES = [
    {
        "name": "Standard case (sanity check)",
        "mode": "bisociation",
        "text": (
            "## 5. Novelty & Testability Self-Critique\n\n"
            "- **Distance score (1-5)**: 4 — these domains are genuinely distant.\n"
        ),
        "expect": 4,
    },
    {
        "name": "Multi-digit value (hallucinated out-of-range score)",
        "mode": "bisociation",
        "text": (
            "## 5. Novelty & Testability Self-Critique\n\n"
            "- **Distance score (1-5)**: 10 — a model that ignores its own stated scale.\n"
        ),
        "expect": 10,
    },
    {
        "name": "Case-varied label (lowercase 'fusion distance')",
        "mode": "homospatial",
        "text": (
            "## 5. Novelty & Testability Self-Critique\n\n"
            "- **fusion distance (1-5)**: 5 — genuinely unrelated fields.\n"
        ),
        "expect": 5,
    },
    {
        "name": "Newline between label and colon",
        "mode": "janusian",
        "text": (
            "## 6. Novelty & Testability Self-Critique\n\n"
            "- **Tension score (1-5)**\n: 4 — a foundational premise.\n"
        ),
        "expect": 4,
    },
    {
        "name": "Word-spelled number (should fail safe -> None, not a wrong digit)",
        "mode": "janusian",
        "text": (
            "## 6. Novelty & Testability Self-Critique\n\n"
            "- **Tension score (1-5)**: four — a foundational premise.\n"
        ),
        "expect": None,
    },
    {
        "name": "Score label mentioned twice in one section (ambiguous, documented not fixed)",
        "mode": "bisociation",
        "text": (
            "## 5. Novelty & Testability Self-Critique\n\n"
            "- Compared to a naive baseline Distance score (1-5): 2, this pairing's "
            "actual Distance score (1-5): 4 is higher because the domains rarely co-occur.\n"
        ),
        "expect": 4,
        "known_open": True,
    },
    {
        "name": "Section missing entirely (should fail safe -> None, not crash)",
        "mode": "bisociation",
        "text": "## 4. The Hypothesis\n\nSomething with no self-critique section at all.\n",
        "expect": None,
    },
]


def run():
    print(f"Control test — extract_self_score() — {len(CASES)} adversarial cases\n")
    passed = 0
    for i, case in enumerate(CASES, 1):
        got = extract_self_score(case["text"], case["mode"])
        ok = got == case["expect"]
        flag = "✅ PASS" if ok else ("⚠️  KNOWN-OPEN" if case.get("known_open") and not ok else "❌ FAIL")
        print(f"{i}. {case['name']}")
        print(f"   mode={case['mode']}  expected={case['expect']}  got={got}  -> {flag}")
        if ok:
            passed += 1
    print(f"\n{passed} of {len(CASES)} cases matched expectation.")
    return passed, len(CASES)


if __name__ == "__main__":
    run()
