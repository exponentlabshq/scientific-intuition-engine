# Scientific Intuition Engine | Universal Monadic Pattern Framework (UMPF)

### Author: Michael Jagdeo
### Organization: Exponent Labs LLC
### Cite this:
Jagdeo, M. (2025). Scientific Intuition Engine (UMPF). Exponent Labs LLC. https://github.com/exponentlabshq/scientific-intuition-engine

Original Thesis: Jagdeo, M. (2025). The Rosetta Stone of UMPF: A Research Methodology. Exponent Labs LLC. https://github.com/exponentlabshq/the-rosetta-stone

## 📋 **Table of Contents**
1. [Abstract](#abstract)
2. [Purpose](#purpose)
3. [The UMPF Frame](#the-umpf-frame)
4. [The Rosetta Stone: A Four-Layer Monadic Architecture](#-the-rosetta-stone-a-four-layer-monadic-architecture)
5. [Domain-Equivalent Pairs: How UMPF Chooses Cross-Domain Matches](#-domain-equivalent-pairs-how-umpf-chooses-cross-domain-matches)
6. [What the Current Artifacts Show](#what-the-current-artifacts-show)
7. [What main.py Does (run behavior)](#what-mainpy-does-run-behavior)
8. [Repository Contents](#repository-contents)
9. [Get Started](#get-started)
10. [License & Citation](#license--citation)

---

## Abstract

This engine converts canonical scientific sources into two auditable artifacts: (1) a citation‑grade verbatim text substrate and (2) a structured UMPF analysis that maps the source onto monads, graphs, lenses, and a four‑layer abstraction hierarchy. The goal is cross‑domain comparability, faithful provenance, and research acceleration without sacrificing rigor.

---

## Purpose

- Turn narrative into structure without losing truth.  
- Make discoveries comparable across disciplines via a shared language.  
- Create artifacts that are traceable (verbatim text), testable (formal schema), and portable (plain text/Markdown).

---

## The UMPF Frame

- **Monads (computation patterns)**  
  - Maybe: uncertainty/absence  
  - State: evolution/learning  
  - IO: boundary/interaction  
  - Free: orchestration/composition

- **Graphs (relational topology)**  
  Components and interactions; connectivity, modularity, dynamics over time

- **Lenses (focused transformation)**  
  Lawful get/set on subsystem state (Get‑Set, Set‑Get, Set‑Set)

- **Four‑Layer Hierarchy**  
  Atomic → Domain → Control → Orchestration

- **Domain Classification**  
  Physical, Informational, Human/Social, Creative (recurring monad/graph/lens signatures)

---

## 🔬 **The Rosetta Stone: A Four-Layer Monadic Architecture**

### **Layer 0 (Atomic)**: Primitive Operations
- **Monads**: Maybe, Either for handling absence and choice
- **Graphs**: Sparse connectivity, local interactions
- **Lenses**: Basic property access and modification

### **Layer 1 (Domain)**: Stateful Processes  
- **Monads**: State, Reader, Writer for context and evolution
- **Graphs**: Modular structure, functional connectivity
- **Lenses**: Contextual state transformations

### **Layer 2 (Control)**: Boundary Management
- **Monads**: IO, Async, STM for external interaction
- **Graphs**: Hierarchical control, feedback loops  
- **Lenses**: Interface management, protocol handling

### **Layer 3 (Orchestration)**: Emergent Behavior
- **Monads**: Free, Effect systems for compositional behavior
- **Graphs**: System-level organization, emergent properties
- **Lenses**: Strategic transformations, policy implementation

---

## 🏗️ **Domain-Equivalent Pairs: How UMPF Chooses Cross-Domain Matches**

### **Systematic Pattern Transfer Protocol**
UMPF uses a rigorous 6-step protocol to identify and validate cross-domain equivalences:
1. **Domain Decomposition**: Apply monad-graph-lens analysis to both source and target domains
2. **Pattern Matching**: Identify structural correspondences across the four abstraction layers
3. **Mechanism Mapping**: Translate mechanisms via categorical functors/natural transformations
4. **Hypothesis Generation**: Formulate testable predictions about transferred mechanisms
5. **Validation Protocol**: Design experiments to verify transfer effectiveness
6. **Iteration**: Refine mappings based on empirical results

### **Cross-Domain Similarity Metrics**
- **Structural Similarity**: Graph isomorphism and motif preservation across layers
- **Behavioral Similarity**: Monadic pattern correspondence (Maybe/State/IO/Free)
- **Functional Similarity**: Lens operation equivalence (lawful get/set flows)
- **Statistical Validation**: Correlation and effect-size thresholds (e.g., >10% improvement, p<0.05)

### **Why This Works**
- **Abstraction Alignment**: Comparable layers prevent false analogies
- **Monadic Pattern Match**: Ensures like-for-like computation patterns
- **Graph Structure Similarity**: Preserves constraints and feedback topology
- **Lens Compatibility**: Guarantees meaningful intervention/observation symmetry

---

## What the Current Artifacts Show

- A Nobel‑level primary source has been re‑expressed as:  
  - Verbatim text (title, authors, DOI, license preserved)  
  - A structured UMPF analysis with formal sections (e.g., Abstract; Formal Framework with Definitions 1–3; Monadic Domain Analysis; “7.2 Technology Development”).
- Outcome: a pair of artifacts that are traceable to the source, comparable across papers, and useful for cross‑domain reasoning.

---

## What main.py Does (run behavior)

- Auto‑selects the first `*.pdf` in `umpf_pipeline/inputs/` (sorted lexicographically).
- Extracts verbatim text with `pdfminer.six` and writes `outputs/<basename>.txt` (truth anchor).
- Loads the UMPF schema prompt from `umpf_pipeline/prompts/umpf_system_prompt.md` (or `.txt` fallback).
- Sends (txt, prompt) to OpenAI ChatCompletion (low temperature) and writes `outputs/<basename>.md` (structured analysis).
- Leaves peer‑review notes under `umpf_pipeline/peer-review/` for model/human audits.

Invariants: the `.txt` is source‑truth; the `.md` is a structured claim constrained by the schema. Analysis must be read against the verbatim anchor.

### Flow (simple)
```mermaid
flowchart TD
    A[PDF in inputs/] --> B[Extract text (pdfminer.six)]
    B --> C[Save outputs/<name>.txt]
    C --> D[Load UMPF prompt]
    D --> E[ChatCompletion (low temperature)]
    E --> F[Save outputs/<name>.md]
    F --> G[Peer-review notes]
```

---

## Repository Contents

- **readme.md** — Project overview, purpose, and framing (this document)
- **umpf_pipeline/**  
  - inputs/ — primary sources (PDFs)  
  - outputs/ — verbatim `.txt` and structured `.md` analyses  
  - prompts/ — UMPF system prompt schema  
  - peer-review/ — model/human audits (e.g., grok.md, openai.md)  
  - main.py — orchestration script (kept minimal; not the focus)  
  - the-rosetta-stone-thesis.md — reference thesis text
- **LICENSE** — MIT
- **CITATION.cff** — repository citation and original thesis reference

---

## Get Started

1) Place a primary source in `umpf_pipeline/inputs/`  
2) Ensure a UMPF schema prompt exists in `umpf_pipeline/prompts/`  
3) Run the pipeline (see `umpf_pipeline/main.py`)  
4) Review artifacts in `umpf_pipeline/outputs/` (verbatim `.txt` and structured `.md`)

Principle: the verbatim `.txt` is the anchor; the `.md` is the formal claim against that anchor.

---

## License & Citation

- License: MIT (© 2025 Michael Jagdeo, Exponent Labs LLC)  
- Repo: https://github.com/exponentlabshq/scientific-intuition-engine  
- Cite this repository:
  - Jagdeo, M. (2025). Scientific Intuition Engine (UMPF). Exponent Labs LLC. https://github.com/exponentlabshq/scientific-intuition-engine
- Cite the original thesis:
  - Jagdeo, M. (2025). The Rosetta Stone of UMPF: A Research Methodology. Exponent Labs LLC. https://github.com/exponentlabshq/the-rosetta-stone

---

## Why These Folders Matter (the meat of the function)

- **inputs/** — Source of truth (primary artifacts)
  - Holds canonical PDFs. Nothing begins without a verifiable source.
  - Guarantees provenance: title, authors, DOI, license remain inspectable.

- **prompts/** — Formal schema (structure, not style)
  - Defines the analytical shape (sections, definitions, mappings) the model must honor.
  - Constrains interpretation so outputs are comparable across domains.

- **outputs/** — Twin artifacts (truth anchor + formal claim)
  - `<name>.txt`: verbatim substrate (citation‑grade; what the paper actually says).
  - `<name>.md`: structured UMPF analysis (how the paper is formally re‑expressed).
  - Read the `.md` against the `.txt`. If they diverge, the `.txt` wins.

- **peer-review/** — Audit loop (accountability and improvement)
  - Stores model/human critiques (e.g., grok.md, openai.md) tied to a specific run.
  - Turns one‑off generations into traceable research assets with a history of review.

Interaction:
- inputs → (schema in prompts) → outputs (.txt, then .md) → peer‑review → better prompts/analyses next run.
