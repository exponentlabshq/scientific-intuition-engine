# Adversarial Refutation — Control Test (Calibration, not a real NO_SIGNAL case)

**Purpose**: the whitepaper's own Limitations section has said, across every revision, that refutation's
0-of-7 survival rate "could mean the domain pool's more speculative pairings are genuinely weak, or that
the refutation lenses are calibrated too strictly, or both — not yet distinguishable... and no control
test (deliberately refuting an already-strong hypothesis to check the lenses don't just refute everything)
has been run." This is that control test.

**Subject**: `hypotheses/2026-08-28-human-trust-variance-x-cryptography.md` — the rank-1 leaderboard entry
(+58 points), chosen specifically because it is the *strongest* case in the current pool: it already
cleared Phase 2 web verification as **ADJACENT_ACTIVE**, with real, citable, positive signal (Zero-Trust
security architecture, decentralized-identity systems letting users "prove credentials while keeping
personal information offchain"). If any hypothesis in the pool should survive adversarial refutation,
this was the strongest candidate.

**Method**: identical protocol to every real NO_SIGNAL refutation — 3 independent agents, one per lens,
each blind to the other two and to this hypothesis's real ADJACENT_ACTIVE status (each was given only the
hypothesis text and the verification note, not told this was a control test or that it had already scored
well).

## Tally: 0 of 3 survive → **REFUTED** (control test result, not counted toward the real 0-of-7 record)

- **Coherence — REFUTED.** The functor equivocates on "trust" twice over: M1's own framing ("a fluctuating
  construct," "variance" is in the hypothesis's own name) contradicts the binary Maybe/Either slot §3
  forces it into, and more fundamentally, ZKPs are a mechanism engineered specifically to *eliminate* the
  need for interpersonal trust — mapping trust's accretion-through-interaction dynamic onto proof-of-a-
  static-secret inverts the mechanism rather than matching it. The reviewer also caught a factual slip in
  §2's Domain row: "the state of knowledge changes as new proofs are generated" misdescribes ZKP mechanics
  — the underlying witness doesn't evolve, only protocol-session state does.
- **Testability — REFUTED.** §4's prediction ("improvements in trust can lead to more efficient and secure
  information exchange protocols — **or vice versa**") is direction-agnostic, so any observed correlation
  in either direction would count as a hit — the classic unfalsifiable double-hedge. §5's own testability
  claim names a data source (case studies) but no metric, comparison condition, or rejection threshold.
- **Triviality — REFUTED.** Strip the vocabulary and §3's functor condition — "evolution... as a function
  of past interactions, where increased trust or knowledge leads to more complex and reliable systems" —
  fits reputation systems, credit scores, immune memory, or ML model confidence equally well. None of
  ZKPs' actual defining properties (completeness, soundness, the zero-knowledge property itself) appear
  anywhere in the hypothesis.

## What this actually tells us

All three lenses converged on the same root finding, independently: the real-world connection Phase 2
verification found (Zero-Trust architecture, decentralized identity) is a **homonym**, not the structural
match §3 claims. "Trust" in the security-doctrine sense that has real, active research behind it is not
"trust" in this hypothesis's own psychological-variance sense — the same nuance Phase 2's own verification
note flagged and did not smooth over. Reading the two results together rather than in isolation: the
hypothesis's ADJACENT_ACTIVE verdict was correct about the *domain pairing* (there is real, fertile
territory near trust-and-cryptography) but the refutation lenses are correct that *this specific functor*
never actually reaches that territory — it borrows the word "trust" without borrowing the structure.

That is a meaningfully different reading than either "the lenses are too strict" or "the domain pool is
weak" alone. It suggests the current 0-of-7 (now effectively 0-of-8 including this control) reflects a
real, specific failure mode — hypotheses that name a genuinely fertile pairing but whose §3 functor doesn't
actually cash out the connection — rather than either blanket miscalibration or blanket domain weakness.
The honest open question this control test does *not* resolve: whether a hypothesis with a tighter,
non-equivocal functor would survive. That requires either a future case that has one, or a second control
test built from scratch specifically to have zero equivocation — this control reused an existing real
hypothesis rather than hand-constructing an artificially clean one, which is a real limitation of this
test itself, disclosed rather than smoothed over.
