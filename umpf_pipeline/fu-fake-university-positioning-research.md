# FU: Fake University — Positioning Research

**Date:** 2026-09-01
**Status:** Research only. No design system, no build, no new personas, no chatbot in this pass — see Diagnosis.
**Prepared for:** Michael Jagdeo
**Method:** the-algorithm's market-research cadence (competitor map / ICP / creator discovery / buyer language / objection map / trend pulse), run via direct web search, plus a full read-only codebase catalog of what already exists in `scientific-intuition-engine/umpf_pipeline`.

---

## 1. Diagnosis

The proposal: reframe The Eureka Engine as **FU: Fake University** — an anthropomorphized institution (faculty, dean, administration, grad/PhD students, public students) sitting on top of the exact same real pipeline, real data, and real leaderboard. No new facts get invented; what changes is the frame.

This document answers the two questions that needed answering before any design work starts: **what already exists that this frame could honestly stand on** (Section 2), and **who else is already doing something like this** (Section 3). It recommends content directions (Section 4) and names real risks (Section 6) — it does not build anything.

---

## 2. The real asset inventory — FU is a naming exercise, not an invention exercise

This is the most load-bearing finding of the whole pass. A full read of `whitepaper.html`, `eureka-engine-dean-evaluation-letter.md`, `dean-letters.html`, `dashboard.html`, `leaderboard.md`, `faculty-of-interdisciplinary-research.md`, `peer-review/eureka-engine-dean-peer-review-2026-08-29.md`, `score_hypotheses.py`, `audit_agent.py`, and sample files in `hypotheses/`, `verifications/`, `refutations/` found the university metaphor is **already load-bearing in production**, not a metaphor being proposed for the first time.

### 2.1 It's already the project's own stated thesis

The whitepaper's own closing paragraph (Section 17, Conclusion):

> "The project's working thesis — that generating successful bisociations is the beginning of a university — has been tested rather than assumed."

`faculty-of-interdisciplinary-research.md` opens with the same claim as its epigraph:

> "The mere fact that we're getting successful bisociations means we have the beginnings of a university"

That file — real, committed, updated across four real batches — then gives this exact, already-shipped mapping:

| Verdict | Faculty role | Meaning |
|---|---|---|
| COLLISION | **Established Department** | Real prior art exists |
| ADJACENT_ACTIVE | **Frontier Research Group** | Real, unclaimed fertile ground |
| FACT_CHECK_FAIL | **Retracted** | Domain description itself was wrong |
| NO_SIGNAL → survives refutation | **Frontier Research Group** (promoted) | Claim's logic held under attack |
| NO_SIGNAL → fails refutation | **REFUTED** | Failed peer review on its central argument, not its data |

### 2.2 The badges are already academic vocabulary, live on the leaderboard right now

`score_hypotheses.py` emits these badges on every real leaderboard row today: `🏛️ Established Department`, `🗺️ Frontier Research Group`, `🚫 Not a Valid Bisociation`, `⚠️ Retracted`, `⚠️ Failed Honesty Check`, `🌗 Contested (1-of-3)`, `💀 Refuted`, `🛡️ Survived the Gauntlet`, `📧 Outreach Drafted`, `✅ Peer-Endorsed`, `❌ Peer-Refuted`, `🔬 Actively Researched`, `🏆 Nobel Ground Truth (calibration benchmark, not engine-generated)`.

`leaderboard.md` has a section literally titled **"Department performance"** — per-mode averages (e.g. "janusian 216 · +28.7 avg points · 8% NO_SIGNAL rate"), reading exactly like a departmental annual report. This isn't a hypothetical reframing; it's the file's real committed heading.

### 2.3 The Dean already exists — twice

`eureka-engine-dean-evaluation-letter.md` is a five-letter correspondence, dated Aug 31–Sept 1 2026, addressed "Dear Provost Alvarez," signed "Yours, Dean of Faculty" every time — a skeptical, evidence-demanding academic administrator deciding whether to fund a departmental pilot. Live on the site at `dean-letters.html`, linked from the production nav bar.

A second, separate document — `peer-review/eureka-engine-dean-peer-review-2026-08-29.md` — is explicitly framed:

```
Reviewer posture: University Dean of Interdisciplinary Graduate Studies
Institution (frame): a research university evaluating whether this system is fit
to advise Masters and PhD candidates on thesis direction and prior art
```

It already calls the system "a faculty-adjacent triage instrument," calls the 80-example-per-mode gold-standard test set "curriculum," and recommends a real academic-integrity guardrail ("must not tell a doctoral student, without human faculty oversight, that a lead is 'safe' to pursue") that an FU frame could inherit wholesale.

### 2.4 The rest of the pipeline maps cleanly, without forcing it

| Real element | File | Natural FU mapping | Why it's honest |
|---|---|---|---|
| 3 generation modes (Bisociation, Janusian, Homospatial) | `whitepaper.html` §2 | Three Schools / Departments of Method | Real, independently documented mechanisms with real named researchers (Koestler, Rothenberg) |
| 4-phase pipeline (generation → verification → refutation → scoring) | `run_cycle.py` | Coursework → Peer Review → Thesis Defense → Transcript Update | Already the real, named phases; only relabeled |
| Adversarial refutation (3 blind AI reviewers, 2-of-3 to survive) | `whitepaper.html` §6 | Thesis Defense Committee | Whitepaper already calls it "a hostile peer-review panel" verbatim |
| 13 real Nobel-linked discoveries used as calibration | `whitepaper.html` §11 | Honorary Faculty / Ground-Truth Alumni | Already distinctly badged `🏆 Nobel Ground Truth (calibration benchmark, not engine-generated)` — never claimed as the engine's own |
| Audit Agent | `audit_agent.py` | Faculty Senate / Curriculum Committee | Its own docstring: "an agent proposes, a person decides" — structurally identical to an advisory faculty body |
| 6-tier leaderboard | `leaderboard.md`, `whitepaper.html` §10 | Dean's List / class ranking | Tier-first ranking already reads as an honor roll |
| 20 postmortem failures | `whitepaper.html` §15 | Published case studies / failure literature | Whitepaper calls these "the clearest evidence of what actually makes this pipeline trustworthy" |
| $6.75 total real spend, per-call accounting | `whitepaper.html` §8 | Tuition / grant ledger | Real OpenAI billing logs |
| Each hypothesis file (Frames, Functor, Novelty self-critique, "If this doesn't hold") | `hypotheses/*.md` | Thesis proposal | Section 6 of every real hypothesis file is already a self-graded honesty field — what a defense asks a student to pre-empt |
| Each verification file (verdict, queries run, citations found) | `verifications/*.md` | Transcript grade / prior-art check | Real fields, not invented |
| Each refutation file (3 lenses, tally, steelman) | `refutations/*.md` | Thesis defense record | The "steelman" field is already exactly a committee's narrower-defensible-thesis rescue attempt |
| 109-domain pool | `domains.json` | Course catalog | Real field list |
| `outreach/` — drafted (never auto-sent) emails to real named researchers | `outreach/README.md` | Office hours with the field | Real drafted correspondence, human-gated |

### 2.5 What genuinely does not exist yet (confirmed by direct grep of the codebase)

- **No FU-facing chatbot, system prompt, or knowledge base.** Every existing "system prompt" in this repo (`prompts/umpf_system_prompt.md`, and inline prompts in `hypothesis_engine.py`, `verify_hypothesis.py`, `refute_hypothesis.py`, `audit_agent.py`) is a pipeline-internal generation prompt, not a conversational assistant. The one explicit mention of "chatbot" in the whole codebase is a negative: the Dean peer-review file states outright, "this is closer to a methods lab than to a chatbot wrapper." Building "talk to the FU knowledge base" is real, new engineering — no scaffold to reuse inside this project. Elsewhere in the wider talentOS vault, `syndi/build_index.py` + `syndi/ask.py` is a real, working RAG pattern (indexing + retrieval + chat) that could be adapted rather than built from scratch, once that phase is greenlit.
- **No Registrar, Provost-as-active-character, or public/grad-student voice exists yet** — only the Dean. New personas would need to be drafted from the real fields above, not invented from nothing, matching this project's own standing discipline.

---

## 3. Competitor / adjacent-space map — "who's already doing this"

The question Michael flagged as most important. Findings:

- **[Sakana AI's "AI Scientist"](https://github.com/sakanaai/ai-scientist)** — the closest functional cousin found anywhere. A full generate → run experiment → write manuscript pipeline; v2 got a real manuscript through real peer review at a real venue; runs ~$6–15/paper with ~3.5 hours of human involvement ([Nature coverage](https://www.nature.com/articles/d41586-026-00899-w)). Independent evaluation found real weaknesses (shallow literature review, mixed reliability) alongside the real milestone ([arXiv evaluation](https://arxiv.org/html/2502.14297v3)). Positioned throughout as a research *tool* / "Artificial Research Intelligence" — never as an institution, never with a persona.
- **[Stanford/Google "Generative Agents" — Smallville](https://arxiv.org/pdf/2304.03442)** — 25 LLM agents with memories, goals, and roles inhabiting a simulated town that includes, notably, "a college with dorms." This is the field's real prior art for the *mechanic* FU would use (agents with campus roles and relationships) — but it's a research paper and open-source demo, with zero brand or commercial framing.
- **[AI Village / Agent Village](https://theaidigest.org/village/blog/what-we-learned-2025)** — ongoing multi-agent experiments (including a 2026 iteration at Edge Esmeralda), framed entirely around AI-safety findings (does an agent stay aligned with what a human would sanction), not branding or education.
- **Corporate university as an established, trusted marketing pattern** — [Hamburger University](https://en.wikipedia.org/wiki/Hamburger_University) (McDonald's, since the 1960s, 275,000+ real "graduates" of "Hamburgerology," 40% of McDonald's global leadership has attended), Salesforce Trailhead, HubSpot Academy. Real precedent that "university" as a brand metaphor is trusted and durable in a business context — it has just never been paired with an *AI system* honestly labeling itself fake.
- **Real diploma-mill scam sites called "fake universities"** are an active, unrelated news story ([wonderfulhighered.com, Aug 2025](https://wonderfulhighered.com/2025/08/15/another-exciting-ai-application-creating-fake-universities/)) — nearly 40 fraudulent sites found using AI to look legitimate. Naming-collision risk, addressed in Section 6.

**Conclusion: this specific combination — an AI research pipeline, self-aware and openly labeled "fake," publishing its own failures under a university frame — was not found anywhere.** Open ground.

---

## 4. ICP, buyer language, and trend pulse

**ICP.** Not a cold general audience: the natural first audience is people already following the Sakana AI Scientist debate, the 2026 AI-peer-review-integrity story (below), and AI-research-skeptical tech/LinkedIn audiences generally — plus Michael's own existing syndicate network. LinkedIn's own 2026 platform data shows educational content and document/PDF-carousel posts getting **3–5x normal reach** ([dataslayer.ai](https://www.dataslayer.ai/blog/linkedin-algorithm-february-2026-whats-working-now)) — real support for the "lectures/courses" content instinct specifically, not content generally.

**Buyer language / objection map — this is FU's real opening, not just a joke.** 2026 is in the middle of a genuine AI-and-science trust crisis:
- [21% of ICLR 2026 peer-review comments were AI-generated](https://howaiworks.ai/blog/iclr-2026-ai-generated-peer-reviews-controversy), and nearly half of submissions got at least one AI-assisted review — an active integrity scandal in real academic publishing.
- ["AI slop" is measurably flooding academic journals](https://www.forbes.com/sites/johndrake/2026/04/30/ai-slop-is-flooding-academic-journals-a-top-journal-measured-it/) — hallucinated citations, fabricated references, harder-to-read AI-generated manuscripts more likely to be rejected.
- Investors and researchers alike are on record explicitly preferring "unmistakably human," radically transparent communication over polished AI output ([searchfunder.com](https://searchfunder.com/post/investor-perspective-ai-generated-pitch-decks-really-hurt-your-credibility)).
- Public postmortems already work as a real trust genre for real companies — GitLab, Cloudflare, Vercel, PostHog all build credibility by publishing exactly the kind of detail most companies hide ([openstatus.dev](https://www.openstatus.dev/guides/public-postmortem-underrated-marketing)).

Put together: while the real AI-and-science conversation is dominated by a credibility crisis (gamed reviews, hallucinated citations, retraction spikes), this project's own standing discipline — publish every failure, disclose every correction, real per-call cost accounting, three blind adversarial reviewers — is already the opposite of that pattern. **"Fake University" that runs a more honest peer-review process than parts of the real one right now is a sharp joke with real teeth, not just a bit.**

One real cautionary tale, not a blocker: [Perplexity's 2025 ad](https://www.tomshardware.com/tech-industry/artificial-intelligence/college-students-drown-out-ai-praising-commencement-speeches-with-boos-deal-with-it-one-speaker-fires-back-as-students-heckle-positive-pitches-for-ais-role) bragging about a student cheating on quizzes drew real, public backlash. FU has to consistently read as "AI does real intellectual labor and shows its work" — never as "AI helps you shortcut the work."

**Persona precedent that this register works at scale:** [Duolingo's owl](https://www.adweek.com/brand-marketing/duolingo-duo-owl-marketing-strategy/) — 9M+ TikTok followers, built on a specific, consistent personality layered over a real product, not a surface gimmick.

**Trend pulse — converging, not fading.** Real universities are having a loud 2026 debate about "agentic AI" running actual campus operations ([Inside Higher Ed, Jan 2026](https://www.insidehighered.com/opinion/columns/online-trending-now/2026/01/07/rise-agentic-ai-university-2026)); the AI-peer-review crisis above is an ongoing, unresolved 2026 story; "AI slop" fatigue is rising. All three make an honestly-labeled, failure-publishing "fake university" more legible right now than a year ago — the timing is good, not incidental.

---

## 5. Recommended tactics (content directions only — none of this is built)

- **"Case Studies in Failure"** — a real content series drawn directly from the 20 real postmortem failures already written up in `whitepaper.html` §15. This is the single strongest, lowest-effort FU content idea: the material already exists, already disclosed, already dense with the specific texture ("Failure 19's fix silently orphaned 161 real refutation results") that makes public postmortems work as a trust genre elsewhere.
- **A "Course Catalog" page** built from the real 109-domain pool (`domains.json`) — a directory, not new content generation.
- **Promote the existing Dean's Letters and `faculty-of-interdisciplinary-research.md` more prominently** under an FU banner — both already exist and are already written in exactly the right register; they just aren't currently framed as part of a unified "university."
- **A real leaderboard-as-"Dean's List"** framing pass on the existing leaderboard page — cosmetic labeling on top of data that already sorts into tiers.
- **Hold off on lectures/live "courses"** as new generated content until the failure case-study series and course-catalog page (both zero-new-fact reuses of existing material) are tested first — sequence low-invention tactics before higher-invention ones.

---

## 6. Explicitly not done in this pass — and open questions for the next one

Not built, per direct instruction:
- No design system, palette, typography, HTML, or CSS
- No new personas (Registrar, Provost-as-character, grad/public-student voices)
- No system-prompt / knowledge-base chatbot (real new engineering; nearest reusable pattern is `syndi/build_index.py` + `syndi/ask.py` elsewhere in the vault, not inside this project)
- No renaming of any live page, file, or commit; no changes to `eureka-engine-web`

**Named risks:**
1. **Naming collision** with real diploma-mill "fake university" scam sites (Section 3) — mitigated with one clear, self-aware disambiguating line wherever FU is introduced (e.g. "not a real degree-granting institution — an honest brand for a real, disclosed AI research pipeline"), not a reason to avoid the name.
2. **Cheating-adjacent backlash** (Section 4, Perplexity precedent) — mitigated by keeping every piece of FU content anchored to real disclosed work (failures, corrections, cost) rather than "AI does the thinking for you" messaging.
3. **Tone mismatch across audiences** — the same "FU" wordplay that reads as sharp/confident to a tech/LinkedIn audience could read as unserious in a more formal investor context; worth deciding deliberately (not by default) how loud vs. contained this launches.

**Open question for Michael:** how public should this launch — a contained pass on already-existing pages first (Dean's Letters, faculty doc, leaderboard labeling), or a full new "FU" landing identity from day one? Recommend the contained pass first, given how much of the frame is already live and just needs surfacing, not rebuilding.
