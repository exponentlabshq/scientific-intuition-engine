# Adversarial Refutation: Bisociation — Control theory — Kalman filtering × Physical Magnetic Fluctuation

**Original**: `hypotheses/2026-09-01-control-theory-x-physical-magnetic-fluctuation.md`
**Method**: 3 independent OpenAI completions, one per lens (`refute_hypothesis.py`, unattended) — same rubric, same independence discipline as prior Claude-subagent rounds, at a fraction of the token cost

## Tally: 2 of 3 survive → **SURVIVES** (promoted out of NO_SIGNAL)

- **Coherence — REFUTED.** The core claim rests on the term 'state' and 'uncertainty,' which are used in both domains. In control theory, 'state' refers to the variables that describe the system at a given time, while 'uncertainty' pertains to the estimation errors in those variables. In the context of magnetic fluctuations, 'state' refers to the magnetic field parameters being measured, and 'uncertainty' relates to the variability in those measurements. These terms do not denote the same formal objects or relationships; they are contextually distinct. Therefore, the claim exhibits equivocation on these terms, as the mapping does not hold under scrutiny. Thus, the claim is refuted.
- **Testability — SURVIVES.** The core claim operationalizes the relationship between Kalman filtering and magnetic fluctuations by asserting that both domains exhibit measurable relationships between state evolution and uncertainty reduction. This is a specific, checkable assertion that can be tested through empirical studies or existing literature on the application of Kalman filters in magnetic field estimation. The claim does not hedge with vague language, making it testable. Therefore, it survives the testability lens.
- **Triviality — SURVIVES.** The core claim states a specific relationship between Kalman filtering and magnetic fluctuations, asserting that both domains exhibit a measurable relationship between state evolution and uncertainty reduction. This precise relationship does not reduce to a generic statement applicable to almost any two complex systems, as it involves specific mechanisms and processes unique to the domains in question. The phrase being tested for genericness is: "f: Kalman filtering(state, uncertainty) → magnetic fluctuation(state, uncertainty)". This phrase retains its specificity and does not simplify to a more general claim about complex systems, indicating that the claim is not trivial.

## What survived, and why this matters

2 of 3 independent lenses could not kill this claim. Per the promotion rule (2-of-3 survival), this hypothesis moves out of NO_SIGNAL — real signal the claim isn't vacuous, not proof it's correct. Still worth Phase 3 outreach consideration if a real researcher in the adjacent field can be identified.
