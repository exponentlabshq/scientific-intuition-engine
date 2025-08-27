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
4. [What the Current Artifacts Show](#what-the-current-artifacts-show)
5. [Repository Contents](#repository-contents)
6. [Get Started](#get-started)
7. [License & Citation](#license--citation)

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

## What the Current Artifacts Show

- A Nobel‑level primary source has been re‑expressed as:  
  - Verbatim text (title, authors, DOI, license preserved)  
  - A structured UMPF analysis with formal sections (e.g., Abstract; Formal Framework with Definitions 1–3; Monadic Domain Analysis; “7.2 Technology Development”).
- Outcome: a pair of artifacts that are traceable to the source, comparable across papers, and useful for cross‑domain reasoning.

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
