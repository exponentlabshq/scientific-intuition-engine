# Adversarial Refutation: Janusian — Swarm Robotics — Ant Colony Optimization

**Original**: `hypotheses/2026-08-29-janusian-swarm-robotics.md`
**Method**: 3 independent OpenAI completions, one per lens (`refute_hypothesis.py`, unattended) — same rubric, same independence discipline as prior Claude-subagent rounds, at a fraction of the token cost

## Tally: 0 of 3 survive → **REFUTED**

- **Coherence — REFUTED.** The core claim rests on the term 'optimization results,' which is used in both domains. In the context of swarm robotics, it refers to the efficiency and effectiveness of algorithms in solving specific problems, while in ant colony optimization, it denotes the performance of algorithms inspired by ant behavior in finding solutions to optimization problems. However, these terms do not refer to the same formal object; the optimization results in swarm robotics may involve different metrics and criteria than those in ant colony optimization. Thus, the claim does equivocate on the term 'optimization results,' as it implies a direct comparison that does not hold when the specific referents are examined. Therefore, the claim is refuted for coherence.
- **Testability — REFUTED.** The core claim does not specify a named metric, comparison condition, or rejection threshold that would allow for a clear experimental test. While it discusses the performance of decentralized and centralized systems, it lacks operationalization in terms of specific scenarios or measurable outcomes that could definitively validate or invalidate the hypothesis. The phrasing is vague and does not provide a concrete basis for testing, making it difficult to derive a clean 'no' from an experiment.
- **Triviality — REFUTED.** The core claim states that the performance of decentralized and centralized systems in optimization scenarios is dictated by the specific characteristics of the problem, which is a general principle applicable to many complex systems. When stripped of domain-specific vocabulary, the claim reduces to a statement about how different systems can yield varying results based on contextual factors, a notion that is broadly true across numerous fields. The phrase being tested for genericness is: "the specific characteristics of the problem will dictate which system performs better". This is indeed a generic statement applicable to many complex systems, indicating that the claim is trivial. Therefore, it does not survive the triviality lens.

## No steelman offered

All three lenses independently converged on REFUTED for this case. If revisited, it would need a genuinely tighter formulation, not a restatement of the same claim.
