# Adversarial Refutation: Janusian — Toxicology — dose-response curves

**Original**: `hypotheses/2026-08-31-janusian-toxicology.md`
**Method**: 3 independent OpenAI completions, one per lens (`refute_hypothesis.py`, unattended) — same rubric, same independence discipline as prior Claude-subagent rounds, at a fraction of the token cost

## Tally: 0 of 3 survive → **REFUTED**

- **Coherence — REFUTED.** The core claim relies on the term 'toxic effects' to describe outcomes from both higher and lower doses of a toxic substance. In toxicology, higher doses typically correlate with increased toxicity, while lower doses can sometimes produce unexpected effects, as seen in hormesis. However, the term 'toxic effects' does not denote the same formal object in both contexts; higher doses lead to predictable toxic effects, while lower doses can lead to beneficial or unexpected responses. Thus, the claim does not maintain coherence as it conflates two different referents of toxicity without clear delineation. Therefore, this is a case of equivocation.
- **Testability — REFUTED.** The core claim presents a specific, falsifiable prediction regarding dose-response relationships in toxicology, particularly emphasizing the simultaneous effects of both higher and lower doses. The mention of variability in toxicity based on individual susceptibility or environmental conditions provides a clear operationalization of the hypothesis. However, while the claim references established concepts like hormesis, it does not explicitly name a specific experiment, dataset, or theorem that would serve as a definitive metric or rejection threshold. Therefore, the claim lacks the necessary specificity to be fully testable as required by the testability lens.
- **Triviality — REFUTED.** The core claim states that both higher and lower doses of a toxic substance can produce greater toxic effects simultaneously, which is a specific assertion about dose-response relationships in toxicology. When stripped of domain-specific vocabulary, the claim reduces to a statement about the variability of effects based on dose, which is a common characteristic of many complex systems. The phrase being tested for genericness is: "both higher doses and lower doses can lead to greater toxic effects simultaneously." This is a broad assertion that could apply to various complex systems, indicating that the claim is trivial and does not hold up under scrutiny. Therefore, the claim does not survive this lens.

## No steelman offered

All three lenses independently converged on REFUTED for this case. If revisited, it would need a genuinely tighter formulation, not a restatement of the same claim.
