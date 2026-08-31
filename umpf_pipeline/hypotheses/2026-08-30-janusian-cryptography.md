# Janusian Hypothesis: Cryptography — public-key infrastructure

**Generated**: 2026-08-30
**Framework**: UMPF Janusian Hypothesis Engine (Exponent Labs LLC)

---

## 1. The Domain

Public-key infrastructure (PKI) is a framework that enables secure communication over the internet by using pairs of keys: a public key that can be shared openly and a private key that must remain confidential. This system is essential for securing online transactions and communications by allowing users to encrypt messages and verify identities.

## 2. The Proposition

The load-bearing assumption in this field is that public keys can be safely shared without compromising the security of the private keys.

## 3. The Inversion

The exact opposite is true: public keys cannot be safely shared without compromising the security of the private keys.

## 4. The Simultaneous Hold

> "Public keys can be safely shared without compromising the security of the private keys."  
> "Public keys cannot be safely shared without compromising the security of the private keys."  
> "Both are true simultaneously."

- **(A) Compromise**: Public keys can be shared safely under certain conditions, but not universally.
- **(B) Synthesis**: Public keys are generally safe to share, but there are specific instances where sharing them introduces vulnerabilities.
- **(C) Paradox**: Public keys are both secure to share and insecure to share simultaneously, as their safety depends on the specific circumstances of their use.

(C) is the genuine paradox because it asserts that the act of sharing public keys can be both secure and insecure at the same time, regardless of the context. This directly contradicts the notion that public keys can be classified as either safe or unsafe based solely on the conditions of their sharing.

## 5. The Hypothesis (The Third Thing)

1. **Simultaneous-hold sentence (required)**: "Both public keys can be safely shared and cannot be safely shared simultaneously for the same instance; the theory must contain both."  
2. **Falsifiable prediction**: "If both the sharing of public keys is safe and unsafe holds simultaneously, then we should observe that instances of public key sharing lead to both successful secure communications and security breaches at the same time — which neither truth alone predicts."

## 6. Novelty & Testability Self-Critique

- **Tension score (1-5)**: 4 — the assumption that public keys can be safely shared is a fundamental premise of PKI and would be considered heretical to invert.
- **Testability**: Analyzing real-world data on public key sharing incidents could confirm or disprove this hypothesis. Specifically, examining cases where public key sharing led to both secure transactions and breaches would be relevant.
- **Known prior art**: Not verified; while there are discussions regarding the vulnerabilities of PKI, the specific tension of public keys being both secure and insecure simultaneously has not been explicitly addressed in the literature.
- **Confidence this is worth a researcher's time**: Medium, as exploring this paradox could lead to new insights into the security practices surrounding PKI.

## 7. If This Doesn't Hold

The most likely reason this turns out to be a compromise or synthesis wearing paradox's clothing is that the proposition and inversion may apply to different scenarios of public key usage, suggesting that both statements reflect true aspects of the same phenomenon rather than representing a genuine contradiction.

## Search Queries

1. "public key infrastructure security vulnerabilities"
2. "PKI public key sharing risks"
3. "public key security breach case studies"
4. "cryptography paradox public key sharing"
5. "public key infrastructure named theory OR framework OR researcher"
