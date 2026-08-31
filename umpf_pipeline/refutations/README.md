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
   it equivocate on a term across the two domains (using one word for two genuinely
   different MEANINGS and treating that as a match)? Do not confuse this with two
   domains having different underlying mechanisms that produce the same formal
   structure — that is not equivocation, it is what bisociation is (different
   mechanisms, same structure is the discovery, not a disguised flaw). And for
   bisociation mode specifically, do not require the two domains to fuse into one
   entity — that is homospatial's bar, not bisociation's, which requires each domain
   to stay itself. (2026-08-31, after control test 3 found this lens refuting a real
   evolutionarily-stable-strategy/Nash-equilibrium claim for having different
   mechanisms in each domain — conscious reasoning vs. blind selection — when that is
   precisely the real result: the same equilibrium condition emerges from either. See
   `refutations/control-test-nobel-calibration.md`.)
2. **Testability lens** — is the falsifiable prediction actually operationalized, or is
   it vague enough that no real experiment could ever return a "no"? A claim can satisfy
   this in the past tense, not only the future tense: if it names a specific, real,
   checkable historical experiment, dataset, or observation that already tested it, that
   counts as operationalized — the named result is the metric, "the named result does not
   hold" is the rejection threshold. A vague appeal to consensus or authority ("this is
   well established") does not count; the cited historical test must be specific and
   checkable, or this lens still refutes on the merits. (2026-08-31, after control test 3
   found this lens rejecting real, historically-confirmed claims — Meselson-Stahl, the
   observed blackbody spectrum, a Nobel committee's own citation — for lacking a
   future-tense experimental design that had, in each case, already run and already
   returned its result decades ago. See `refutations/control-test-nobel-calibration.md`.)
3. **Triviality lens** — strip the domain-specific vocabulary. Does the claim reduce to
   something true of almost any two complex systems (the same umbrella-trap failure
   mode Phase 2's own rubric already guards against, applied one level deeper)?
   "Strip the vocabulary" means keep the precise relationship, formula, or mechanism
   exactly as specific as stated and only swap the domain names — it does not mean
   compress the claim into a vaguer paraphrase and then test whether that paraphrase
   is generic. (2026-08-31, after control test 3 found this lens restating Hopfield's
   exact claim — the same energy function as the Ising model, not an analogy — as
   "systems converging to local minima," then correctly calling that weaker restatement
   generic. The claim actually made was never tested. See
   `refutations/control-test-nobel-calibration.md`.)

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
