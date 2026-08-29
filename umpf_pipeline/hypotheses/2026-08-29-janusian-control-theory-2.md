# Janusian Hypothesis: Control theory — Kalman filtering

**Generated**: 2026-08-29
**Framework**: UMPF Janusian Hypothesis Engine (Exponent Labs LLC)

---

## 1. The Domain

Kalman filtering is a mathematical technique used in control theory and signal processing to estimate the state of a dynamic system from a series of noisy measurements. It operates under the assumption that both the process and the measurement noise are Gaussian and that the system can be modeled linearly.

## 2. The Proposition

The load-bearing assumption in Kalman filtering is that the system dynamics can be accurately modeled using linear equations and Gaussian noise, which allows for optimal state estimation.

## 3. The Inversion

The exact opposite is true: the system dynamics cannot be accurately modeled using linear equations and Gaussian noise, making optimal state estimation impossible.

## 4. The Simultaneous Hold

> "The system dynamics can be accurately modeled using linear equations and Gaussian noise, allowing for optimal state estimation."  
> "The system dynamics cannot be accurately modeled using linear equations and Gaussian noise, making optimal state estimation impossible."  
> "Both are true simultaneously."

- **(A) Compromise**: The accuracy of state estimation depends on the specific model used; linear models may work in some situations while non-linear models are needed in others.
- **(B) Synthesis**: A model that incorporates both linear and non-linear elements can provide a more comprehensive estimation framework, effectively blending the two approaches.
- **(C) Paradox**: The system can be simultaneously accurately estimated and inaccurately estimated using the same linear model under the same conditions due to the presence of inherent uncertainties and noise characteristics that affect the estimation process.

(C) is the paradox because it asserts that the same model can yield both accurate and inaccurate estimates at the same time, depending on the specific noise realizations and the underlying dynamics of the system. (A) fails because it suggests a context-dependent solution rather than a simultaneous truth, while (B) resolves the contradiction by selecting a side rather than holding both realities.

## 5. The Hypothesis (The Third Thing)

**If both the system dynamics can be accurately modeled using linear equations and Gaussian noise, and cannot be accurately modeled using those same equations and noise, then the estimation results will exhibit both high fidelity and significant error simultaneously due to the unpredictable nature of noise and system dynamics — which would not be predicted by either truth held alone.**

## 6. Novelty & Testability Self-Critique

- **Tension score (1-5)**: 4 — the assumption that linear models suffice in all cases is a foundational premise in control theory, and challenging it could be considered heretical.
- **Testability**: Empirical studies comparing the performance of Kalman filters in linear systems with known noise characteristics versus those with unpredictable noise could confirm or refute this hypothesis.
- **Known prior art**: Research into the behavior of Kalman filters under non-ideal conditions, such as the effects of non-Gaussian noise, may touch on aspects of this tension, but a direct contradiction of the foundational assumption is not verified.
- **Confidence this is worth a researcher's time**: Medium — while the paradox presents an interesting tension, the practical implications may be limited by the existing frameworks already in use.

## 7. If This Doesn't Hold

The most likely reason this turns out to be a compromise or synthesis wearing paradox's clothing is that the proposition and inversion might apply to different contexts or types of systems, suggesting that they are not truly contradictory but rather reflect varying conditions of applicability.

## Search Queries

1. "Kalman filtering non-linear systems"
2. "Extended Kalman Filter vs Linear Kalman Filter"
3. "Gaussian noise assumptions in control theory"
4. "Kalman filter paradox in estimation theory"
5. "Control theory named researcher OR framework"

---

**⚠️ Automated check failed twice:** §4 still contains context-split language (depending on, in some situations, context-dependent) after one corrective retry. This hypothesis may be a disguised compromise (A) or synthesis (B) mislabeled as a genuine paradox (C) — read §4 with that in mind before trusting the paradox framing.
