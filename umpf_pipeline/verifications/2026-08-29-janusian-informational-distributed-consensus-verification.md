# Verification: Janusian — Distributed Consensus

**Verifies**: `hypotheses/2026-08-28-janusian-informational-distributed-consensus.md`
**Verified**: 2026-08-29 · **Method**: WebSearch

## Verdict: **COLLISION**

## Query
`CRDT eventual consistency consensus without single agreed state decentralized systems`

## What was found
**Conflict-free Replicated Data Types (CRDTs)** are a real, named, decades-studied class of distributed
data structure built exactly on the hypothesis's (C) paradox: replicas update independently and
concurrently *without consensus*, temporarily disagree, and mathematically converge to the same state
without ever requiring a round of agreement on a single interim state. Strong eventual consistency
(commutativity, idempotency, causality) is the formal property that lets nodes "operate effectively with
differing interpretations of the state" — the hypothesis's own §5 claim, nearly verbatim.

## Reasoning
This is not an adjacent metaphor — CRDTs are the literal, named, actively-used real-world technology
(peer-to-peer apps, blockchain, collaborative editors) built on the exact structural claim the hypothesis
proposes. Clean collision.
