# Adversarial Refutation: Janusian — Cognitive AI Preprocessing Pipelines

**Original**: `hypotheses/2026-08-29-janusian-cognitive-ai-preprocessing-pipelines.md`
**Method**: 3 independent agents, one per lens, blind to each other

## Tally: 0 of 3 survive → **REFUTED**

Same failure mode as the earlier common-law and materials-science Janusian cases in the archive: a
disguised context-dependency ("helps here, hurts there") labeled "(C) Paradox" rather than a genuine
same-instance paradox.

- **Coherence — REFUTED.** §4C's own phrasing — "in SOME scenarios... in OTHERS, DEPENDING ON the nature of
  the data" — partitions the outcome space by covariate rather than asserting both truths of one identical
  pipeline at one identical moment. §7 is a direct admission: the hypothesis concedes proposition and
  inversion "apply to different types of models or datasets" and are "not genuinely contradictory but...
  context-dependent truths" — the hypothesis refutes itself in its own text.
- **Testability — REFUTED.** "Performance will vary unpredictably based on dataset/model characteristics"
  has no operationalized null, direction, effect size, or threshold — this is the default expectation for
  nearly any ML intervention, not specific to preprocessing or to the claimed paradox.
- **Triviality — REFUTED.** "Whether preprocessing helps depends on the data and model" is standard
  preprocessing folk wisdom taught in any intro ML course (normalization helps SVMs/KNN, is often
  irrelevant to tree-based models) — not a discovery, and not paradoxical once stated plainly.

## No steelman offered

The same-instance test (added to the Janusian prompt specifically to catch this pattern) should have caught
this before generation completed — worth checking why it didn't flag §4C's own "in some... in others"
language as a compromise.
