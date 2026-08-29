# Verification: Raft × PBFT Consensus

**Verifies**: `the-rosetta-stone/case-studies/the-rosetta-stone-case-study-raft-PBFTconsensus.md`
**Verified**: 2026-08-28 · **Source**: rosetta-stone-case-study

---

## Verdict: **COLLISION**

## Query

`Raft PBFT consensus algorithm comparison structural similarity distributed systems`

## What was found

Textbook-standard, extensively documented comparison. Named sources: GeeksforGeeks *"Consensus Algorithms in Distributed System"*, a full arXiv survey *"Consensus Algorithms of Distributed Ledger Technology — A Comprehensive Analysis"* (2309.13498), a personal-blog-turned-reference *"Overview of consensus algorithms in distributed systems - Paxos, Zab, Raft, PBFT."* Both algorithms are routinely taught and compared side by side as the canonical crash-fault vs. Byzantine-fault consensus pair.

## Reasoning

No ambiguity here — this is standard distributed-systems curriculum content, not a fresh discovery. Real, legitimate, well-covered territory.

## Note

Related content overlap with `case-study-DCA-cachecoherentprotocols-verification.md` — that file's *actual* content (despite its `domains.json` label) is also "Distributed Consensus Algorithms (e.g., Raft, PBFT)" vs. cache coherence, meaning Raft/PBFT material appears across two case studies in this corpus under different framings.
