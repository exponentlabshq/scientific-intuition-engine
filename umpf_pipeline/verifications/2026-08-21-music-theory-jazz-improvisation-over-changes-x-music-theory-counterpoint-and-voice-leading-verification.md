# Verification: Jazz Improvisation × Counterpoint and Voice Leading

**Verifies**: `hypotheses/2026-08-21-music-theory-jazz-improvisation-over-changes-x-music-theory-counterpoint-and-voice-leading.md`
**Verified**: 2026-08-28
**Method**: WebSearch (Claude-orchestrated — see README's "current limits" note)

---

## Verdict: **COLLISION**

## Queries run

1. `jazz improvisation counterpoint voice leading unified analysis research`
2. `computational music theory jazz improvisation counterpoint rules framework`

## What was found

- **Berklee College of Music runs a named course, "Jazz Counterpoint 1"** — the
  pairing isn't just academically explored, it's institutionalized curriculum.
- **"Motivic and Voice-Leading Coherence in the Improvisations of Saxophonist Chris
  Cheek"** (dissertation, UNT) — this is close to a direct execution of the
  hypothesis's own §4 prediction: analyzing a specific improviser's output for
  voice-leading coherence patterns.
- **"Improvised counterpoint: a study of contrapuntal strategies... in jazz
  improvisation"** (thesis, figshare) and a second thesis on Fred Hersch's contrapuntal
  piano technique, explicitly tracing it to his Bach-chorale counterpoint training —
  the causal/pedagogical link the hypothesis proposes, already documented.
- On the computational side: Ebcioğlu's CHORAL system already implements ~350 rules of
  species counterpoint generatively; GenJam and other systems do the jazz-improvisation
  equivalent. The two traditions haven't been fully computationally unified in one
  system per this search, but the underlying music-theoretic connection (analyzing
  improvisation *through* counterpoint/voice-leading principles) is not open — it's
  taught, thesised, and published.

The self-assessed distance score in the original hypothesis was **3/5** ("different
methodologies and goals... distinct educational paths") — already the most cautious of
the three original hypotheses. The search results suggest even 3 was generous: this
isn't two fields that "rarely engage" so much as one field (jazz pedagogy) that
routinely borrows the other's toolkit by name.

## Reasoning

Same shape as the ecology/telecom case, different domain: real, specific, named prior
art (a Berklee course, a directly-on-point dissertation) rather than a generic
"music theory" umbrella. This clears the bar for COLLISION, not a borderline
ADJACENT_ACTIVE call — the connection isn't merely plausible-and-unexplored, it's
taught.

Domain-fact spot check: both §1 descriptions (jazz improvisation's harmonic/motivic
freedom; counterpoint's rule-governed independent voice interaction) are standard,
uncontested characterizations — no fact-check issue.

## Feedback signal

The lowest self-reported distance score of the three hypotheses (3/5) turned out to be
the most direct collision of the three — the model's own instinct that this pair was
"less distant" was correct, and arguably should have been rated lower still (2, not 3)
given how institutionalized the connection already is. This is a second data point
(alongside the ecology/telecom case) suggesting the distance-score rubric needs
sharper anchors for what counts as a 2 vs. a 3-4, not just for extreme cases.
