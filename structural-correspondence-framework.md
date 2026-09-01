# From Bisociation to Functor: A Structural Test for Cross-Domain Analogy

## Abstract

Ordinary analogy-making compares two domains at the level of resemblance: *A reminds us of B*. This is useful but unfalsifiable — resemblance has no built-in test for when it stops being valid. This paper develops a formal alternative grounded in category theory: an analogy is treated not as a claim about objects, but as a claim about a structure-preserving mapping (a functor) between two categories of relations. The central methodological move is elevating a two-term analogy (`x:y = a:b`) to a three-term one (`x:y:z = a:b:c`), because three terms introduce *composition*, and composition is the first point at which a proposed correspondence can actually be tested rather than merely felt. We define a five-way outcome taxonomy — isomorphism, homomorphism with residual, restriction-repair, enrichment-repair, and common-third-category — and validate it against nine cross-domain pairs spanning mathematics, physics, chemistry, biology, economics, and linguistics.

---

## 1. Motivation

An analogy of the form "A is like B" makes a claim about resemblance between objects. It does not, by itself, make any claim about *why* the resemblance holds, or under what conditions it would break. Two domains can share a superficial resemblance while differing completely in their underlying dynamics — and two domains can appear unrelated at the object level while sharing deep structural behavior. Neither case is distinguishable from ordinary analogical reasoning alone.

Category theory offers a natural upgrade path, because it treats objects as secondary to the *relationships between* them, and treats "sameness of structure" as a formal, checkable property (a functor) rather than an impression.

## 2. From Relation to Composition

### 2.1 The two-term case

A basic analogy `x:y = a:b` can be read as a claim that two morphisms correspond:

$$
f: x \rightarrow y \qquad\qquad f': a \rightarrow b
$$

This asks whether the transformation from `x` to `y` plays the same structural role as the transformation from `a` to `b`. It is a claim about a single relation, and it is weak: almost any two loosely similar processes can be made to satisfy it.

### 2.2 The three-term case — where composition enters

Extending to `x:y:z = a:b:c` introduces a second morphism and, critically, their **composite**:

$$
x \xrightarrow{f} y \xrightarrow{g} z \qquad\qquad a \xrightarrow{f'} b \xrightarrow{g'} c
$$

$$
g\circ f : x \rightarrow z \qquad\qquad g'\circ f' : a \rightarrow c
$$

The test is no longer "do the endpoints resemble each other" but:

$$
\boxed{F(g\circ f) = F(g)\circ F(f)}
$$

This is the defining property of a **functor** `F` between the two categories. It is a substantially stronger and more specific claim than pairwise resemblance, because it requires the *sequence* of transformations, not just the transformations individually, to correspond. Two points establish a relationship; three points establish a structure that can actually fail to compose — and a proposed correspondence that fails this test has told you something concrete about where it breaks.

## 3. A Hierarchy of Correspondence

| Level | Content |
|---|---|
| 0 | Objects (`x, y, z`) |
| 1 | Relations (`x:y`) |
| 2 | Relational chains (`x:y:z`) |
| 3 | Composition (`g∘f`) |
| 4 | Cross-domain mapping (`F: 𝒜 → ℬ`) |
| 5 | Structure preservation (`F(g∘f) = F(g)∘F(f)`) |
| 6 | Multiple mappings (`F, G: 𝒜 → ℬ`) |
| 7 | Transformation between mappings (`η: F ⇒ G`, a natural transformation) |
| 8 | Equivalence of structure (`𝒜 ≃ ℬ`) |

Each level asks a strictly stronger question of the proposed correspondence than the one before it. An analogy that only survives Level 1 has told you very little; one that survives Level 5 has told you something a working scientist could use.

## 4. Strength Scale

Not every valid correspondence is equally strong. Three grades matter in practice:

- **Homomorphism** — `F` preserves structure in one direction; some qualitative behavior survives the mapping, but the two domains need not behave identically in degree or rate.
- **Isomorphism** — an inverse `F⁻¹` exists such that `F⁻¹F = I` and `FF⁻¹ = I`; the structures are equivalent in the relevant sense, not merely similar.
- **Common-third-category** — neither domain maps onto the other directly; both are restrictions or projections of a more general structure that is the actual home of the phenomenon.

## 5. Diagnostic Procedure

When `F(g∘f) ≠ F(g)∘F(f)`, the correct response is not automatic rejection. Three repair strategies and one honest failure mode cover the cases observed in this study:

1. **Restrict** — check whether the correspondence holds on a sub-category (a limit, a regime, a parameter range) even though it fails globally.
2. **Enrich** — check whether one domain was modeled with a missing morphism that exists in the fuller theory; add it back and retest.
3. **Re-target** — check whether both domains are independently restrictions of a common third category; if so, the correspondence is not A→B but A→C and B→C.
4. **Report as failure** — if none of the above closes the diagram, report exactly which level (1, 2, or 3) the correspondence broke at. This is itself diagnostic content, not a null result.

A further finding worth stating explicitly: an exact match at Level 1 — even an intentionally borrowed formula — does not guarantee the composite at Level 3 will match. Object-level or even formula-level identity and process-level (dynamical) correspondence are separate claims that can come apart in either direction. Every candidate correspondence should have its composite checked explicitly, even when the underlying relation looks like a slam dunk.

## 6. Validated Case Studies

### 6.1 Multiplication → Addition (exact isomorphism)

$$
\log:(\mathbb{R}^+,\times)\rightarrow(\mathbb{R},+)
$$

With `f` = multiply by `a`, `g` = multiply by `b`:

$$
F(g\circ f) = \log(ab) = \log a + \log b = F(g) + F(f)
$$

This holds exactly for all `a, b`, with no restriction and no residual. It is the cleanest available benchmark for what a fully closing functor looks like.

### 6.2 Electrical circuits → Hydraulic systems (isomorphism within a regime)

Objects: voltage/current/charge (`V, I, Q`) map to pressure/flow/volume (`P, F, Vol`). Ohm's law (`I = V/R`) and pipe-flow law (`F = P/R_h`) are the same functional form; charge accumulation (`dQ/dt = I`) and volume accumulation (`dVol/dt = F`) are likewise identical in form. The composite `V ↦ ∫V/R dt` and `P ↦ ∫P/R_h dt` match exactly within the linear regime, which is why hydraulic analog computers were historically used to model electrical circuits.

### 6.3 Gravitational and electromagnetic radiation (homomorphism, enrichment-repaired)

Both gravitational mass and electric charge obey inverse-square force laws, and both support orbital motion under classical mechanics — Level 1 and Level 2 hold identically. At Level 3, restricting gravity to Newtonian mechanics fails to compose (no radiation term exists, so no orbital decay is predicted, while accelerating charges are known to radiate). Enriching the gravitational category to General Relativity repairs this: two orbiting masses do lose energy to gravitational radiation, and this is directly measured — the Hulse–Taylor binary pulsar's orbital decay matches the GR quadrupole-radiation prediction closely. The functor closes qualitatively (both sides radiate and decay), but not quantitatively: electromagnetic dipole radiation scales as `(v/c)²` while gravitational quadrupole radiation scales as `(v/c)⁵`, with a further suppression factor. This is a genuine homomorphism with an explicit, informative residual — the rate mismatch is itself part of the finding, not a flaw in the correspondence.

### 6.4 Bohr atom → Classical mechanics (restriction-repair)

The correspondence principle states that Bohr's quantized orbital model converges to classical orbital mechanics as the quantum number `n → ∞`. The functor does not commute globally — quantized and classical orbits diverge sharply for small `n` — but it commutes exactly on the sub-category where `n` is large. This is a case where the correct response to an apparent failure was not rejection but explicit restriction to the regime where the diagram does commute.

### 6.5 Wave–particle duality → Quantum state space (common third category)

Neither the wave description nor the particle description of light and matter maps directly onto the other. Diffraction/interference (wave composite) and localized detection (particle composite) both fail to predict each other's composite behavior when treated as a direct A→B correspondence. Both descriptions instead emerge as different projections of one underlying category — quantum state space (`ψ`, Hilbert space) — with interference and localization each recoverable as different measurement composites of the same object. This is the case where the correct repair is not to fix the mapping between A and B, but to recognize that both are restrictions of a common source category C.

### 6.6 Natural selection → Clonal selection (immunology) (near-isomorphism)

Genetic variation and differential reproductive success in evolutionary biology map closely onto somatic hypermutation and affinity-based clonal expansion in the adaptive immune system. This correspondence is not incidental: clonal selection theory was explicitly built on the Darwinian template. Both are instances of a shared general algorithm — variation-generation followed by differential amplification — and the replicator-equation formalism applies to both, giving the correspondence a mathematically shared foundation rather than a merely narrative one.

### 6.7 Thermodynamic entropy → Shannon information entropy (formula-isomorphic, dynamics diverge)

Boltzmann entropy (`S = k log W`) and Shannon entropy (`H = -Σp log p`) share an exact formula, deliberately borrowed by Shannon. At Level 1 this is as close to identical as two formulas can be. At Level 3, however, the composite behaviors diverge: thermodynamic entropy is governed by the second law and increases in isolated systems over time, while Shannon entropy has no analogous temporal-increase law — under deterministic processing, the data-processing inequality means `H` can only decrease. The formula transfers; the dynamics do not. This case demonstrates that Level 1 exactness provides no guarantee about Level 3 behavior.

### 6.8 Market equilibrium → Logistic population growth (strong homomorphism)

The excess-demand-driven price adjustment model in economics (`dP/dt = k(D − S)`, with discrete cobweb variants) and logistic population growth in ecology (`dN/dt = rN(1 − N/K)`, with a discrete logistic map variant) both belong to the same broader class of first-order autonomous dynamical systems. Discrete versions of both models exhibit the same bifurcation route to chaos as a control parameter is increased — a structural match at the level of dynamical behavior, not merely surface form.

### 6.9 Language change → Population genetics (empirically validated homomorphism)

Utterance variation and selection under iterated learning (formalized in Bayesian iterated-learning models) produce drift and convergence signatures formally analogous to allele-frequency drift and selection in population genetics. This correspondence has been tested computationally, not only asserted narratively, giving it stronger empirical grounding than a purely descriptive analogy would have.

## 7. Summary Table

| Pair | Outcome | Repair mechanism |
|---|---|---|
| Multiplication ↔ Addition | Isomorphism (exact) | None needed |
| Circuits ↔ Hydraulics | Isomorphism (regime-bound) | None needed within linear regime |
| Gravitational ↔ EM radiation | Homomorphism | Enrichment (Newtonian → GR) |
| Bohr atom ↔ Classical mechanics | Restriction-valid | Restrict to large-`n` |
| Wave ↔ Particle | Common third category | Re-target both onto quantum state space |
| Natural selection ↔ Clonal selection | Near-isomorphism | None needed — shared replicator formalism |
| Thermodynamic ↔ Shannon entropy | Formula-isomorphic, dynamics diverge | None available — genuine divergence |
| Market equilibrium ↔ Logistic growth | Strong homomorphism | None needed — shared bifurcation structure |
| Language change ↔ Population genetics | Homomorphism, empirically tested | None needed |

## 8. The General Pipeline

$$
\text{Bisociation} \rightarrow \text{Relation} \rightarrow \text{Triad} \rightarrow \text{Composition} \rightarrow \text{Functor} \rightarrow \text{Natural Transformation} \rightarrow \text{Equivalence}
$$

The methodological contribution of this framework is not the claim that any particular pair of domains corresponds — it is the shift in the underlying question. Ordinary analogy asks *how are these two things alike?* This framework asks a more precise and answerable question:

$$
\boxed{\text{When does a surprising analogy become an actual structural correspondence — and when it doesn't, exactly where does it break?}}
$$

## 9. Methodological Checklist

1. **State the triad explicitly.** Name real `x→y→z` and `a→b→c`. If no genuine third term exists, only a Level-1 analogy is available, and no composition test can yet be run.
2. **Compute both composites concretely** — in units, functional form, or explicit qualitative behavior, not prose alone.
3. **Check `F(g∘f) = F(g)∘F(f)`.**
   - Exact match → candidate isomorphism; test for an inverse `F⁻¹`.
   - Same qualitative behavior, different quantitative law → homomorphism; report the residual explicitly.
   - No match → proceed to diagnosis.
4. **Diagnose a failure before rejecting it:**
   - Check for a missing morphism from an under-described domain (enrich).
   - Check for a sub-category where the diagram does commute (restrict).
   - Check whether both domains are independently restrictions of a common third category (re-target).
5. **Report the outcome type explicitly** — isomorphism, homomorphism-with-residual, restriction-valid, enrichment-valid, common-third-category, or genuine failure with the level at which it broke. Each is a distinct, useful claim in its own right.
