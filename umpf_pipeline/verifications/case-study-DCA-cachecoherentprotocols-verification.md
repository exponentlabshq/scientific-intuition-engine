# Verification: Distributed Consensus Algorithms × Cache Coherence Protocols

**Verifies**: `the-rosetta-stone/case-studies/the-rosetta-stone-case-study-DCA-cachecoherentprotocols.md`
**Verified**: 2026-08-28 · **Source**: rosetta-stone-case-study (pre-dates this session's engine)

---

**Naming flag, before anything else:** `domains.json`'s `already_paired` entry for this file reads `["Dynamic Cache-coherent Architectures (DCA)", "Cache-coherent protocols"]`, but the file's own title and Selected Domains line are **"Distributed Consensus Algorithms (e.g., Raft, PBFT)"** vs. **"Distributed Cache Coherence Protocols (e.g., MESI, Directory-based)"** — a different pairing than the tracking label suggests. Verified against the file's actual content, not the label.

## Verdict: **ADJACENT_ACTIVE**

## Query

`distributed consensus algorithm cache coherence protocol structural similarity computer science`

## What was found

No source directly draws the cross-connection the case study claims (consensus's leader-election/agreement/commit cycle ≅ cache coherence's ownership-acquisition/invalidation cycle). The search surfaced real, substantial material on cache coherence protocols on their own (SCI protocol, German protocol model-checking case studies) but nothing bridging to consensus algorithms specifically.

## Reasoning

Not a generic-umbrella case: "distributed systems consistency protocols" is a specific, well-defined CS subfield housing both topics as siblings (both are, precisely, "maintain agreement on shared mutable state across distributed nodes despite failures/latency") — narrower and more load-bearing than a vague catch-all like "complex adaptive systems." Real, fertile, specific territory; the exact functor hasn't been drawn in what surfaced.

## Feedback signal

Worth reconciling the `domains.json` label against the file's actual content in a future pass — this and the Dirac case study (below) are the two label/content mismatches found in this corpus.
