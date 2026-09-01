# Adversarial Refutation: Bisociation — Control theory — Kalman filtering × Genomics — GWAS and polygenic risk

**Original**: `hypotheses/2026-09-01-control-theory-x-genomics.md`
**Method**: 3 independent OpenAI completions, one per lens (`refute_hypothesis.py`, unattended) — same rubric, same independence discipline as prior Claude-subagent rounds, at a fraction of the token cost

## Tally: 0 of 3 survive → **REFUTED**

- **Coherence — REFUTED.** The core claim rests on the term 'state estimates,' which in control theory refers to the estimated values of system states based on noisy measurements, while in genomics, 'polygenic risk scores' represent a calculated risk based on the cumulative effect of multiple genetic variants. These terms denote different referents: 'state estimates' are dynamic and related to system control, whereas 'polygenic risk scores' are static and related to genetic predisposition. Thus, the claim does not hold as a genuine bisociation, as it relies on an equivocation of terms that do not represent the same formal object or relationship in both domains.
- **Testability — REFUTED.** The core claim suggests a direct functional relationship between Kalman filtering in control theory and polygenic risk scores in genomics. However, while there are applications of Kalman filtering in genomics, specifically in modeling gene regulatory networks and estimating disease states, there is no operationalized evidence or specific metrics linking Kalman filtering directly to polygenic risk scores or GWAS. This lack of a clear, named metric or rejection threshold for the proposed relationship renders the claim vague and unfalsifiable.
- **Triviality — REFUTED.** The core claim states that Kalman filtering state estimates can be mapped to polygenic risk scores, asserting a specific functional relationship between the two domains. When stripped of domain-specific vocabulary, the claim reduces to a general assertion about two systems that refine predictions over time using noisy data. This is a common characteristic of many complex systems, making the claim trivial. The specific mechanisms of Kalman filtering and polygenic risk scores do not provide a unique or non-obvious connection, as the underlying principle of refining predictions from incomplete data is widely applicable across various fields.

## No steelman offered

All three lenses independently converged on REFUTED for this case. If revisited, it would need a genuinely tighter formulation, not a restatement of the same claim.
