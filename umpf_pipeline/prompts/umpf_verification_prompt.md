# Rubric: UMPF Hypothesis Verification (Phase 2 of the Eureka Engine)

Phase 1 (`hypothesis_engine.py`, and its future Janusian sibling) generates a candidate
hypothesis and asks itself "known prior art: not verified" — a hand-wave, not a check.
Phase 2 resolves that hand-wave against real search results. This document is the
classification rubric a verifier (human or model) applies to the search results
gathered for one hypothesis.

## Why this is four buckets, not pass/fail

The naive framing — "if the hypothesis connects to active research, the engine is
working" — collapses two signals that point in *opposite* directions:

- Finding the **exact** connection already published proves the engine's bisociation
  reasoning is structurally sound (it found something real, not hallucinated) — but it
  also means the specific hypothesis has **zero marginal research value**. It's not
  "worth investigating." It's already investigated.
- Finding **real, active research near the domains but not this exact connection** is
  the actual target state: the territory is real and fertile, and the connection is
  still open.

Collapsing these into one "found something" bit would reward the engine for
rediscovering consensus over producing discovery. Four buckets, not two:

## The four outcomes

**COLLISION** — the search surfaces work that already makes substantially the same
structural connection the hypothesis's §3 functor claims, not just a shared vocabulary
or a shared parent discipline. Named algorithms, named frameworks, or dissertations
built directly on the claimed correspondence all count. Verdict: not novel — kill or
demote as "worth investigating," but log as a *positive* signal for the engine's
reasoning validity.

**ADJACENT_ACTIVE** — real, current, *specifically relevant* research activity exists
near one or both domains, or a real bridging subfield exists, but the exact functor in
§3 has not been drawn. Verdict: promote. This is the state a genuinely useful
hypothesis should be in.

**Hard rule — the umbrella trap.** A bridging field is only "specifically relevant" if
it would *not* return the same hit for most other domain pairs. "Both are complex
adaptive systems" or "both are studied by systems theory" is true of nearly any two
nonlinear, self-organizing domains — treating that as ADJACENT_ACTIVE evidence makes
the bucket meaningless, since it would confirm almost every pair the engine could ever
propose. If the only bridging material found is this generic, the correct bucket is
NO_SIGNAL, not ADJACENT_ACTIVE, however research-sounding the material reads.

**FACT_CHECK_FAIL** — search results contradict or materially complicate what §1 (the
plain-terms description of M₁ or M₂) asserts about how the domain actually works.
This is a hallucination check on the raw facts, independent of whether the bisociation
itself is novel. Verdict: kill or regenerate; flag the specific domain entry in
`domains.json` for a rewrite — the problem is the domain description, not the pairing.

**NO_SIGNAL** — nothing specifically relevant surfaces on either the connection or the
domains individually. Explicitly ambiguous: this looks identical whether the hypothesis
is genuinely novel-and-real or vacuous-and-not-even-wrong — search cannot tell those
apart. Do not treat NO_SIGNAL as a pass. It is data for a different instrument
(adversarial refutation, not search) that this phase does not build.

## What to write for each hypothesis verified

- The verdict (one of the four).
- Which search queries were run and what, concretely, they surfaced — cite real titles/
  URLs, never a vague "some sources suggest."
- One paragraph connecting the finding to the verdict — not just asserting the bucket.
- If COLLISION: name what the engine reinvented.
- If ADJACENT_ACTIVE: name the specific (non-generic) bridging material found.
- If FACT_CHECK_FAIL: name exactly which claim in §1 is contradicted, and by what.
- If NO_SIGNAL: say so plainly rather than stretching a thin result into ADJACENT_ACTIVE.

## Feedback fields (for the aggregate log, not the per-hypothesis file)

Each verification run appends one line to `verification-log.jsonl` with: hypothesis
slug, mode (bisociation/janusian), verdict, the domains involved, the self-reported
distance score from §5 of the original hypothesis, and a `notes` field for anything
domain-specific worth surfacing later (e.g. "domain description for X may need a
rewrite"). This is the data Phase 3 (refining Phase 1) reads — not the prose files.
