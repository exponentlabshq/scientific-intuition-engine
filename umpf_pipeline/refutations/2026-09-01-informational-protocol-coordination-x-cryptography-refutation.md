# Adversarial Refutation: Bisociation — Informational Protocol Coordination × Cryptography — public-key infrastructure

**Original**: `hypotheses/2026-09-01-informational-protocol-coordination-x-cryptography.md`
**Method**: 3 independent OpenAI completions, one per lens (`refute_hypothesis.py`, unattended) — same rubric, same independence discipline as prior Claude-subagent rounds, at a fraction of the token cost

## Tally: 1 of 3 survive → **REFUTED**

- **Coherence — REFUTED.** The core claim rests on the term 'Protocol Coordination,' which is used in both domains. In the context of Informational Protocol Coordination, it refers to the systematic management of communication states in distributed systems, while in Cryptography, particularly in PKI, it pertains to the management of digital certificates and identity verification. These are not the same formal objects; the former focuses on communication processes, while the latter emphasizes security and identity management. Therefore, the claim does equivocate on the term 'Protocol Coordination,' as it conflates two distinct referents without establishing a clear formal mapping between them.
- **Testability — SURVIVES.** The core claim presents a specific relationship between protocol coordination and public-key infrastructure (PKI) through the function f: Protocol Coordination(State) -> PKI(Certificate Management). This claim is operationalized by referencing established protocols like the Two-Phase Commit Protocol and key management techniques, which are specific, checkable frameworks that demonstrate systematic approaches to managing communication states and identity verification. Therefore, the claim is not vague and does provide a clear basis for testing its validity.
- **Triviality — REFUTED.** The core claim states that both domains must demonstrate a systematic approach to managing states of communication and identity verification. When stripped of domain-specific vocabulary, the claim reduces to a general assertion about complex systems managing states and ensuring integrity and authenticity in exchanges. This is a common characteristic of many complex systems, making the claim trivial. The exact phrase being tested for genericness is: 'Both domains must demonstrate a systematic approach to managing states of communication and identity verification, ensuring that the integrity and authenticity of messages are maintained across exchanges.' This phrase is indeed broader and more generic than the specific mechanisms of the original claim, indicating that it is not a novel insight.

## No steelman offered

All three lenses independently converged on REFUTED for this case. If revisited, it would need a genuinely tighter formulation, not a restatement of the same claim.
