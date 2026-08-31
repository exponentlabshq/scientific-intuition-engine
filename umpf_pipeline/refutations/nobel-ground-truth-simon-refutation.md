# Adversarial Refutation: Bisociation — Simon — Bounded Rationality × Heuristic Search

**Original**: `hypotheses/nobel-ground-truth-simon.md`
**Method**: 3 independent OpenAI completions, one per lens (`refute_hypothesis.py`, unattended) — same rubric, same independence discipline as prior Claude-subagent rounds, at a fraction of the token cost

## Tally: 2 of 3 survive → **SURVIVES** (promoted out of NO_SIGNAL)

- **Coherence — SURVIVES.** The core claim effectively maps the concept of bounded rationality in psychology to heuristic search in computer science without equivocation. Both domains utilize the same underlying principle of limiting the search space to find satisfactory solutions rather than optimal ones, which is a shared formal structure. The terms 'bounded rationality' and 'heuristic search' refer to the same decision-making process under constraints, thus maintaining coherence in the bisociation.
- **Testability — SURVIVES.** The core claim explicitly references Herbert Simon's concept of bounded rationality and its implications for decision-making, which is a named and checkable theory. Additionally, it connects this theory to the development of heuristic search algorithms in AI, citing Simon's collaboration with Newell and the creation of the 'Logic Theorist.' This provides a clear operationalization of the hypothesis, satisfying the testability criteria.
- **Triviality — REFUTED.** The core claim states that decision-makers do not optimize over the full space of alternatives but instead satisfice by searching a limited space using heuristics. When stripped of domain-specific vocabulary, this reduces to a general statement about complex systems using limited resources to find satisfactory solutions, which is true of many systems beyond human decision-making and AI. The specific mechanisms of bounded rationality and heuristic search are lost in this generalization, making the claim trivial.

## What survived, and why this matters

2 of 3 independent lenses could not kill this claim. Per the promotion rule (2-of-3 survival), this hypothesis moves out of NO_SIGNAL — real signal the claim isn't vacuous, not proof it's correct. Still worth Phase 3 outreach consideration if a real researcher in the adjacent field can be identified.
