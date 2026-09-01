# Hypothesis: Control theory — Kalman filtering × Genomics — GWAS and polygenic risk

**Generated**: 2026-09-01
**Framework**: UMPF Two-Domain Hypothesis Engine (Exponent Labs LLC)

---

## 1. The Two Frames (M₁, M₂)

**M₁ — Control theory — Kalman filtering**: Control theory, specifically Kalman filtering, is a mathematical approach used to estimate the state of a dynamic system from a series of incomplete and noisy measurements. It provides a recursive solution for predicting future states based on past data and current observations.

**M₂ — Genomics — GWAS and polygenic risk**: In genomics, Genome-Wide Association Studies (GWAS) identify genetic variants associated with traits by analyzing data from many individuals. Polygenic risk scores are calculated to predict an individual's likelihood of developing traits or diseases based on the cumulative effect of numerous genetic variants.

## 2. Monadic Signature of Each Domain

| Layer | Control theory — Kalman filtering | Genomics — GWAS and polygenic risk |
|---|---|---|
| Atomic (Maybe/Either) | In Kalman filtering, uncertainty is represented by the covariance of the estimated state, indicating the confidence in the predictions made from the observations. | In GWAS, uncertainty is reflected in the p-values associated with genetic variants, which indicate the strength of the association between variants and traits, often leading to ambiguous interpretations. |
| Domain (State/Reader/Writer) | Kalman filtering evolves the state estimate over time as new measurements are incorporated, updating the prediction based on the dynamics of the system being observed. | In GWAS, the state evolves by accumulating evidence from multiple studies, where new findings can update the understanding of genetic contributions to traits, akin to refining a model as more data becomes available. |
| Control (IO/STM) | Kalman filtering operates within a control framework that defines boundaries for prediction and correction, managing the interaction between the model and the noisy observations. | In GWAS, the control aspect involves managing the interaction between genetic data and phenotype data, requiring rigorous statistical controls to account for confounding factors and ensure valid associations. |
| Orchestration (Free/effects) | Kalman filtering allows for the composition of multiple state estimates into a unified prediction, integrating various sources of information over time to improve accuracy. | In genomics, polygenic risk scores integrate multiple genetic variants into a single score that summarizes the cumulative risk, orchestrating diverse genetic influences into a coherent prediction of phenotype. |

## 3. The Candidate Functor

f: Kalman filtering state estimates (control theory) → polygenic risk scores (genomics)

For this functor to hold, Both domains must effectively incorporate and update information from noisy or incomplete data to refine their predictions over time.

## 4. The Hypothesis

1. **Generative-relation sentence (required):** I noticed that the relational rule governing state estimation with Kalman filtering also governed the calculation of polygenic risk scores — specifically, the updating of predictions based on new data inputs.
2. **Falsifiable prediction:** If that relation holds, then improvements in polygenic risk score accuracy should be observable when applying Kalman filtering techniques to the genomic data, leading to more precise risk assessments.

## 5. Novelty & Testability Self-Critique

- **Distance score (1-5)**: 4 — These domains are typically treated as distinct fields, with control theory focused on dynamic systems and genomics centered on biological data analysis, indicating a significant conceptual distance.
- **Testability**: Empirical testing could involve applying Kalman filtering methods to existing GWAS datasets to evaluate if the predictive accuracy of polygenic risk scores improves, compared to traditional methods.
- **Known prior art**: Not verified.
- **Confidence this is worth a researcher's time**: Medium, as the connection is plausible but may require extensive validation across both fields.

## 6. If This Doesn't Hold

The most likely reason this functor turns out superficial rather than structural is that the underlying assumptions about data and noise in Kalman filtering do not translate well to the complexities of genetic data.

## Search Queries

1. "Kalman filtering applications in genomics"
2. "polygenic risk assessment using control theory"
3. "dynamic systems theory in GWAS"
4. "state-space models in genetic epidemiology"
5. "Kalman filter in polygenic risk score modeling"

---

**⚠️ Automated check failed twice:** no Search Query targets a specific named theory, framework, or researcher, even after one corrective retry. Verification may miss an existing collision with real prior art that a more specific search would have found — read this hypothesis's verdict with that in mind.
