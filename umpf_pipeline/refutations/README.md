# Adversarial Refutation — the instrument for the NO_SIGNAL queue

Phase 2 (web-search verification) resolves three of the four outcomes confidently:
COLLISION, ADJACENT_ACTIVE, and FACT_CHECK_FAIL all have something external to check
against. NO_SIGNAL is different by design — it's what happens when nothing surfaces
either way, and that looks identical whether the underlying hypothesis is genuinely
novel-and-real or vacuous-and-not-even-wrong. Search can't tell those apart. This is
the instrument that can: it doesn't search for prior art, it attacks the claim's own
internal structure.

## Protocol

Three independent lenses per case, each genuinely trying to kill the claim, defaulting
to **refuted** when uncertain (not defaulting to survival — the asymmetry is
deliberate, matching this project's standing adversarial-verify discipline elsewhere):

1. **Coherence lens** — is the claimed structural mapping actually well-formed, or does
   it equivocate on a term across the two domains (using one word for two different
   underlying mechanisms and treating that as a match)?
2. **Testability lens** — is the falsifiable prediction actually operationalized, or is
   it vague enough that no real experiment could ever return a "no"?
3. **Triviality lens** — strip the domain-specific vocabulary. Does the claim reduce to
   something true of almost any two complex systems (the same umbrella-trap failure
   mode Phase 2's own rubric already guards against, applied one level deeper)?

**Promotion rule:** a claim needs 2-of-3 lenses to find it survives (fails to refute)
to move out of NO_SIGNAL. Otherwise: **REFUTED** — a new, distinct outcome from
FACT_CHECK_FAIL. FACT_CHECK_FAIL means the domain facts were wrong. REFUTED means the
domain facts are fine, but the specific cross-domain claim built on them doesn't
survive scrutiny — the equivalent of a paper that failed peer review on its central
argument, not its data.

## Files

One record per case, `[slug]-refutation.md`, with all three lenses' findings, the
tally, and the final verdict. Results feed back into `verification-log.jsonl` (adding
a `refutation_verdict` field to the relevant entries) and `faculty-of-interdisciplinary-research.md`
gets a new "REFUTED" section, distinct from "Retracted."
