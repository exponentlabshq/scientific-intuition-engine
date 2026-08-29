# Verification: Ecology × Telecommunications

**Verifies**: `hypotheses/2026-08-21-ecology-mycorrhizal-fungal-networks-x-telecommunications-packet-switching-and-routing.md`
**Verified**: 2026-08-28
**Method**: WebSearch (Claude-orchestrated — see README's "current limits" note)

---

## Verdict: **COLLISION**

## Queries run

1. `mycorrhizal fungal network packet switching routing analogy`
2. `bio-inspired network routing algorithm fungal network mycelium`
3. `mycorrhizal network resilience nutrient distribution research 2024`

## What was found

The exact structural correspondence the hypothesis's §3 functor proposes — fungal
network topology/growth dynamics mapping onto routing/path-selection behavior in
communication networks — is not just adjacent, it's an established named subfield:

- **HyphaNet** (ScienceDirect, *Bio-inspired routing algorithm for MANETs based on
  fungi networks*): routes are built the way fungal mycelium grows — several parallel
  paths establish initially, and over time only the highest-flow paths receive
  reinforcement and persist. This is functionally the same claim as the hypothesis's
  §3 mapping ("network resilience ↔ network robustness"), already formalized into a
  working mobile-ad-hoc-network routing protocol.
- **FUNNet** (ResearchGate, *A Novel Biologically-Inspired Routing Algorithm Based on
  Fungi*) — a second, independently-named algorithm built on the same correspondence.
- **"Filamentous Fungi Growth as Metaphor for Mobile Communication Networks Routing"**
  — a paper whose title is close to a restatement of the hypothesis's own framing.
- **"Information and Communication Theoretical Foundations of the Internet of
  Plants"** (arXiv 2509.08434) — models root emission, fungal transport, and plant
  uptake explicitly as transmitter/channel/receiver in a standard communication-link
  model. This is the §3 functor, already made formal, using actual information theory.

Domain-fact spot check: the mycorrhizal-network description in §1 (nutrient exchange,
resilience, resource distribution) holds up against 2024/2025 mycorrhizal research
(Frontiers in Microbiology 2024, New Phytologist 2024) — no fact-check issue on M₁.
Standard-CS description of packet switching (M₂) is uncontested.

## Reasoning

This is a clean collision, not a borderline call. The hypothesis's own §5 self-critique
rated distance **4/5** ("genuinely unrelated communities who've never talked to each
other") and flagged "known prior art: not verified... direct connections... not
well-documented." Both of those self-assessments are wrong: there are at least two
named algorithms and a formal information-theoretic paper built on precisely this
correspondence. The engine's bisociation *instinct* was sound — it found a real,
load-bearing structural match, not a hallucinated one — but its own novelty
self-rating was miscalibrated on this one, and its prior-art hand-wave, if actually
checked, would have caught the collision.

## Feedback signal

Distance score (self-reported 4) vs. actual collision: **a data point that the
distance-score rubric may be over-rating novelty for domain pairs that already have a
named bio-inspired-computing subfield bridging them.** Bio-inspired/nature-inspired
algorithms (ant colony optimization, swarm/boids, genetic algorithms — several of which
are already in `domains.json`'s pool) are a systematically higher collision-risk
category, since "use biological system X as inspiration for computing system Y" is
already an entire established research tradition, not a genuinely uncharted pairing.
