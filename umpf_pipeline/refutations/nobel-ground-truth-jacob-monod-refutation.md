# Adversarial Refutation: Bisociation — Jacob & Monod — Gene Regulation × Control Engineering

**Original**: `hypotheses/nobel-ground-truth-jacob_monod.md`
**Method**: 3 independent OpenAI completions, one per lens (`refute_hypothesis.py`, unattended) — same rubric, same independence discipline as prior Claude-subagent rounds, at a fraction of the token cost

## Tally: 2 of 3 survive → **SURVIVES** (promoted out of NO_SIGNAL)

- **Coherence — SURVIVES.** The core claim identifies a specific shared structure: the feedback control mechanism in both the lac operon and control engineering systems. In both domains, the term 'feedback' refers to a formal object that describes a system's response to changes in its environment, despite the underlying processes differing (molecular vs. engineering). This mapping does not equivocate on terms, as both domains utilize the same formal structure of feedback control, thus fulfilling the criteria for bisociation without equivocation.
- **Testability — SURVIVES.** The core claim names a specific, checkable result from the work of Jacob, Monod, and Lwoff regarding the lac operon, which is a well-documented genetic control mechanism. This historical experiment and its findings serve as the operationalized metric, comparison condition, and rejection threshold for the hypothesis. The claim is thus testable and not vague, satisfying the criteria for the testability lens.
- **Triviality — REFUTED.** The core claim describes a specific mechanism of gene regulation in E. coli, detailing the role of a repressor protein and its interaction with DNA. When stripped of domain-specific vocabulary, the claim reduces to a general statement about feedback control systems in complex biological processes, which is true of many systems beyond just genetics and control engineering. The phrase being tested for genericness is: 'a real molecular feedback-control circuit, formally identical to negative feedback in control engineering.' This is a broader statement that applies to various complex systems, thus failing the triviality lens.

## What survived, and why this matters

2 of 3 independent lenses could not kill this claim. Per the promotion rule (2-of-3 survival), this hypothesis moves out of NO_SIGNAL — real signal the claim isn't vacuous, not proof it's correct. Still worth Phase 3 outreach consideration if a real researcher in the adjacent field can be identified.
