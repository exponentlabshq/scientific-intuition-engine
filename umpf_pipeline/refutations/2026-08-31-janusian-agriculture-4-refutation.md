# Adversarial Refutation: Janusian — Agriculture — crop rotation and soil health

**Original**: `hypotheses/2026-08-31-janusian-agriculture-4.md`
**Method**: 3 independent OpenAI completions, one per lens (`refute_hypothesis.py`, unattended) — same rubric, same independence discipline as prior Claude-subagent rounds, at a fraction of the token cost

## Tally: 0 of 3 survive → **REFUTED**

- **Coherence — REFUTED.** The core claim relies on the term 'crop rotation' to bridge two contradictory assertions about its effects on soil health. In domain A, 'crop rotation' refers to a practice that enhances soil health through increased diversity and nutrient cycling. In domain B, it is suggested that crop rotation does not improve soil carbon content, indicating a failure to enhance soil health in that specific context. These are two different referents: one emphasizes benefits while the other highlights limitations. Therefore, the claim does equivocate on the term 'crop rotation' by treating it as a singular concept while it denotes different outcomes in each context.
- **Testability — REFUTED.** The core claim presents a simultaneous-hold sentence that asserts both the improvement and lack of improvement of soil health due to crop rotation can be true. However, the falsifiable prediction lacks a specific operationalization of metrics, comparison conditions, and rejection thresholds. While it mentions varying effects on soil health metrics, it does not specify what those metrics are, how they will be measured, or what constitutes a significant difference. Therefore, the prediction remains vague and does not allow for a clear experimental design to test it, leading to a conclusion of refutation on the testability lens.
- **Triviality — REFUTED.** The core claim states that both 'crop rotation improves soil health' and 'crop rotation does not improve soil health' can be true simultaneously for the same practice. When stripped of domain-specific vocabulary, this reduces to a statement about the coexistence of contradictory effects in any complex system. The phrase being tested for genericness is: 'Both crop rotation improves soil health and crop rotation does not improve soil health are true simultaneously for the same crop rotation practice.' This statement is not unique to agriculture; it could apply to many complex systems where contradictory outcomes can coexist. Therefore, the claim is trivial and does not survive this lens.

## No steelman offered

All three lenses independently converged on REFUTED for this case. If revisited, it would need a genuinely tighter formulation, not a restatement of the same claim.
