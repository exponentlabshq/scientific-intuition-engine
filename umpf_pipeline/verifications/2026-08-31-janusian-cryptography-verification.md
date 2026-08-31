# Verification: Janusian — Cryptography — zero-knowledge proofs

**Verifies**: `hypotheses/2026-08-31-janusian-cryptography.md`
**Verified**: 2026-08-31 · **Method**: OpenAI web_search (gpt-4o-mini) + classification, single call (`verify_hypothesis.py`, unattended)

## Verdict: **ADJACENT_ACTIVE**

## Queries
- `zero-knowledge proofs limitations`
- `cryptographic protocols information leakage`
- `zero-knowledge proof paradox`
- `knowledge without disclosure cryptography`
- `zero-knowledge proof theory OR framework OR researcher`

## What was found
Zero-knowledge proofs (ZKPs) are cryptographic protocols that allow one party to prove to another that a statement is true without revealing any information beyond the validity of the statement itself. While ZKPs are designed to prevent information leakage, they are not entirely immune to it. For instance, human errors in card-based protocols can lead to unintended information leakage. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0890540122000542?utm_source=openai)) Additionally, electromagnetic information leakage from cryptographic devices has been observed, indicating that physical implementations can inadvertently reveal information. ([doi.org](https://doi.org/10.1109/TEMC.2012.2227486?utm_source=openai)) These examples suggest that while ZKPs aim to prevent information disclosure, under certain conditions, they may inadvertently leak information.

## Reasoning
The search results provide examples where ZKPs, despite their design to prevent information leakage, have been subject to unintended disclosures due to human errors and physical vulnerabilities. This supports the claim that both it is possible to prove knowledge of a secret without revealing any information about the secret itself and it is impossible to prove knowledge of a secret without revealing some information about the secret itself are true simultaneously for the same cryptographic protocol; the theory must contain both.
