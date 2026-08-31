# Hypothesis: Cryptography × Physical Voltage Spikes

**Generated**: 2026-08-31
**Framework**: UMPF Two-Domain Hypothesis Engine (Exponent Labs LLC)

---

## 1. The Two Frames (M₁, M₂)

**M₁ — Cryptography**: Public-key infrastructure (PKI) is a system that uses pairs of keys (public and private) to secure communications and verify identities, allowing users to encrypt data and ensure its integrity through digital signatures.

**M₂ — Physical Voltage Spikes**: Voltage spikes are sudden increases in electrical voltage that can disrupt or damage electrical circuits and devices, often caused by lightning strikes or power surges, and require protective measures to ensure the integrity of electrical systems.

## 2. Monadic Signature of Each Domain

| Layer | Cryptography | Physical Voltage Spikes |
|---|---|---|
| Atomic (Maybe/Either) | Uncertainty in key distribution and trust in certificate authorities | Uncertainty in voltage levels and potential for damage |
| Domain (State/Reader/Writer) | Evolving states of encrypted data and key management | Context of voltage levels affecting circuit states |
| Control (IO/STM) | Interaction through secure channels and protocols | Interaction through circuit protection devices |
| Orchestration (Free/effects) | System-wide composition of encryption algorithms and protocols | System-wide composition of electrical systems and surge protectors |

## 3. The Candidate Functor

The proposed mapping *f: M(Cryptography) → M(Voltage Spikes)* is as follows: the public key maps to the protective measures, the private key maps to the integrity of the electrical system, and the encrypted message maps to the stable operation of the circuit. For this functor to hold, both domains must demonstrate that protective measures (keys or devices) are essential for maintaining integrity against disruptive forces (unauthorized access or voltage spikes).

## 4. The Hypothesis

1. **Generative-relation sentence (required):** I noticed that the relational rule governing the use of public and private keys in cryptography to maintain secure communications also governed the deployment of protective devices in electrical systems to prevent damage from voltage spikes — specifically, the rule of ensuring integrity through protective measures.
2. **Falsifiable prediction:** If that relation holds, then the effectiveness of a voltage protection system will correlate with the strength of its design in maintaining operational integrity, just as the security of communications correlates with the strength of cryptographic keys — or vice versa.

## 5. Novelty & Testability Self-Critique

- **Distance score (1-5)**: 4. While both domains deal with integrity and protection, they are typically treated in isolation with different communities of practice, making them relatively unrelated.
- **Testability**: Existing literature on electrical engineering and cryptography can be examined for parallels in protective measures and their effectiveness, particularly looking for studies that analyze the integrity of systems under stress.
- **Known prior art**: Not verified; while there are discussions on security in electrical systems, a direct connection to cryptographic principles has not been established in the literature.
- **Confidence this is worth a researcher's time**: Medium, as the hypothesis presents a novel perspective but lacks direct existing literature to support it.

## 6. If This Doesn't Hold

The most likely reason this functor turns out to be superficial rather than structural is that the mechanisms of maintaining integrity in voltage systems may not exhibit the same relational dynamics as cryptographic keys, particularly if the nature of failure and protection differs fundamentally.

## Search Queries

1. "public key infrastructure and electrical system protection"
2. "voltage spikes protective measures cryptography analogy"
3. "integrity in cryptography and electrical engineering"
4. "surge protection systems and digital security measures"
5. "electrical integrity theory OR cryptographic security framework"

---

**⚠️ Automated check failed twice:** §3/§4 still lack a clean generative-relation transplant (analogy language and/or missing relational-rule sentence) after one corrective retry. Treat this as resemblance wearing bisociation's name — not a thesis-grade lead until rewritten.
