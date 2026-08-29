#!/usr/bin/env python3
import base64
import json
import os

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def compute_live_stats():
    """Read straight from the real ledger (one directory up) so this script
    stays standalone-runnable -- no separate 'live stats' file for
    publish_site.py to remember to generate first. Counts verdicts directly
    rather than importing score_hypotheses.py, since only raw counts are
    needed here, not points/badges."""
    ledger_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "verification-log.jsonl")
    verdicts = {"COLLISION": 0, "ADJACENT_ACTIVE": 0, "NO_SIGNAL": 0}
    total = 0
    refuted = 0
    survived = 0
    pending = 0
    with open(ledger_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            total += 1
            v = e.get("verdict", "")
            if v == "PENDING_VERIFICATION":
                pending += 1
                continue
            if v in verdicts:
                verdicts[v] += 1
            if e.get("refutation_verdict") == "REFUTED":
                refuted += 1
            elif e.get("refutation_verdict") == "SURVIVES":
                survived += 1

    if pending > 0:
        pending_clause = f"{pending} still pending"
    else:
        pending_clause = "nothing left pending"

    if survived == 0:
        survival_clause = "every one of them, a real 0% survival rate reported as-is"
    else:
        survival_clause = f"{survived} of them survived independent scrutiny, the rest did not"

    return {
        "total": total,
        "collision": verdicts["COLLISION"],
        "adjacent": verdicts["ADJACENT_ACTIVE"],
        "refuted": refuted,
        "pending_clause": pending_clause,
        "survival_clause": survival_clause,
    }


live_stats = compute_live_stats()

hero_img = b64("assets/hero-collision.jpg")
mech_bisociation_img = b64("assets/mech-bisociation.jpg")
mech_janusian_img = b64("assets/mech-janusian.jpg")
mech_homospatial_img = b64("assets/mech-homospatial.jpg")
pipeline_img = b64("assets/pipeline.jpg")
mech_verify_img = b64("assets/mech-verify.jpg")
mech_refute_img = b64("assets/mech-refute.jpg")
mech_score_img = b64("assets/mech-score.jpg")

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="robots" content="noindex, nofollow" />
<title>The Eureka Engine</title>
<style>
:root {
  --ink: #14110f;
  --paper: #1c1815;
  --surface: #241f1a;
  --surface-hover: #2c261f;
  --border: #3a3229;
  --text: #ede6d8;
  --text-muted: #a89a86;
  --text-faint: #6f6455;
  --gold: #c89b3c;
  --gold-bright: #e0b954;
  --v-adjacent: #5fa88f;
  --v-refuted: #b56b6b;
  --serif: ui-serif, Georgia, 'Iowan Old Style', 'Times New Roman', serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Inter', ui-sans-serif, 'Segoe UI', sans-serif;
  --mono: ui-monospace, 'SF Mono', Menlo, monospace;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }

/* SITE NAV — shared across landing.html, whitepaper.html, leaderboard.html */
.site-nav {
  position: sticky; top: 0; z-index: 200;
  background: rgba(20,17,15,0.94); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
}
.site-nav-inner {
  max-width: 1080px; margin: 0 auto; padding: 14px 24px;
  display: flex; align-items: center; justify-content: space-between; gap: 20px;
}
.site-nav-brand {
  font-family: var(--serif); font-size: 1rem; color: var(--gold);
  text-decoration: none; font-weight: 600; white-space: nowrap;
}
.site-nav-links { display: flex; gap: 24px; }
.site-nav-links a {
  font-family: var(--mono); font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--text-muted); text-decoration: none; transition: color 0.15s; white-space: nowrap;
}
.site-nav-links a:hover { color: var(--gold); }
.site-nav-links a.is-active { color: var(--gold); border-bottom: 1px solid var(--gold); padding-bottom: 2px; }
@media (max-width: 560px) {
  .site-nav-inner { padding: 12px 16px; }
  .site-nav-links { gap: 14px; }
  .site-nav-brand { font-size: 0.88rem; }
  .site-nav-links a { font-size: 0.68rem; }
}

body {
  background: var(--ink); color: var(--text); font-family: var(--sans);
  font-size: 17px; line-height: 1.65; margin: 0; -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 880px; margin: 0 auto; padding: 0 24px; }

/* HERO */
.hero {
  position: relative;
  min-height: 92vh;
  display: flex;
  align-items: center;
  padding: 110px 24px 60px;
  background-image:
    linear-gradient(180deg, rgba(20,17,15,0.55) 0%, rgba(20,17,15,0.84) 65%, var(--ink) 100%),
    url('data:image/jpeg;base64,__HERO_IMG__');
  background-size: cover;
  background-position: center 42%;
}
.hero-grid {
  display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 56px; align-items: center;
  max-width: 1080px; margin: 0 auto; width: 100%;
}
.hero-text { text-align: left; }
.hero .kicker {
  font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.16em;
  color: var(--gold-bright); font-size: 0.78rem; margin-bottom: 22px;
}
.hero h1 {
  font-family: var(--serif); font-weight: 600; font-size: clamp(2.1rem, 5vw, 3.3rem);
  line-height: 1.15; margin: 0 0 22px; text-wrap: balance;
}
.hero h1 em { color: var(--gold-bright); font-style: normal; }
.hero p.dek {
  font-size: 1.12rem; color: var(--text-muted); margin: 0 0 30px; text-wrap: balance;
}
.hero .scroll-cue {
  font-family: var(--mono); font-size: 0.78rem; color: var(--text-faint);
  text-transform: uppercase; letter-spacing: 0.1em; animation: bob 2.2s ease-in-out infinite;
}
@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(6px); } }
@media (prefers-reduced-motion: reduce) { .hero .scroll-cue { animation: none; } }

.hero-video { display: flex; flex-direction: column; align-items: center; }
.hero-video video {
  width: 100%; max-width: 320px; aspect-ratio: 9 / 16; display: block;
  border-radius: 18px; border: 1px solid rgba(200,155,60,0.35);
  box-shadow: 0 24px 70px rgba(0,0,0,0.55); background: var(--ink);
}
.hero-video .hv-caption {
  text-align: center; font-family: var(--mono); font-size: 0.72rem; color: var(--text-faint);
  margin-top: 14px; text-transform: uppercase; letter-spacing: 0.08em;
}
/* STORY VIDEO — the 90s narrated documentary piece, right under the hero */
.story-video-frame {
  margin-top: 32px; border-radius: 16px; overflow: hidden;
  border: 1px solid var(--border); background: var(--surface);
  box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}
.story-video-frame video { width: 100%; aspect-ratio: 16 / 9; display: block; background: var(--ink); }
.story-video-caption {
  text-align: center; font-family: var(--mono); font-size: 0.76rem; color: var(--text-faint);
  margin-top: 14px; text-transform: uppercase; letter-spacing: 0.08em;
}

@media (max-width: 860px) {
  .hero { padding: 76px 20px 50px; min-height: auto; }
  .hero-grid { grid-template-columns: 1fr; gap: 40px; text-align: center; }
  .hero-text { text-align: center; }
  .hero-video video { max-width: 260px; }
}

section.block { padding: 84px 0; border-top: 1px solid var(--border); }
section.block:first-of-type { border-top: none; }
.eyebrow {
  font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--gold); font-size: 0.76rem; margin-bottom: 14px;
}
h2 {
  font-family: var(--serif); font-size: clamp(1.7rem, 4vw, 2.3rem); font-weight: 600;
  margin: 0 0 22px; text-wrap: balance; line-height: 1.2;
}
.lede { font-size: 1.12rem; color: var(--text); max-width: 700px; margin: 0 0 20px; }
p.body-text { color: var(--text-muted); max-width: 680px; }
strong.accent { color: var(--gold-bright); font-weight: 600; }

/* SYSTEM MAP — quick pipeline overview using all 6 diagrams, right after the hero */
.map-step-label {
  font-family: var(--mono); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--gold); text-align: center; margin: 8px 0 18px; display: block;
}
.map-fork {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;
  border: 1px dashed var(--border); border-radius: 14px; padding: 20px;
}
.map-tile { text-align: center; }
.map-tile img {
  width: 100%; aspect-ratio: 1 / 1; border-radius: 10px; border: 1px solid var(--border);
  background: var(--ink); display: block; margin-bottom: 10px;
}
.map-tile .mt-name { font-family: var(--serif); font-size: 0.98rem; color: var(--text); display: block; margin-bottom: 4px; }
.map-tile .mt-cap { font-size: 0.82rem; color: var(--text-muted); }
.map-tile .mt-tag {
  font-family: var(--mono); font-size: 0.64rem; text-transform: uppercase; letter-spacing: 0.06em;
  display: block; margin-top: 6px; color: var(--text-faint);
}
.map-tile.taken img { border-color: var(--gold); box-shadow: 0 0 0 1px var(--gold); }
.map-tile.taken .mt-tag { color: var(--gold-bright); }
.map-tile.not-taken img { opacity: 0.55; }
.map-arrow { text-align: center; font-family: var(--serif); font-size: 1.7rem; color: var(--gold); margin: 20px 0; }
.map-sequence { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
@media (max-width: 720px) { .map-fork, .map-sequence { grid-template-columns: 1fr; } }

/* CONCEPT TEACHING BLOCKS — every major concept gets the same three-beat
   treatment: a concrete hook, the exact mechanism (with its diagram), then
   where the pattern recurs. Renamed for teaching, not labeled as a theory. */
.concept { margin-top: 44px; padding-top: 38px; border-top: 1px solid var(--border); }
.concept:first-of-type { margin-top: 38px; }
.concept-head { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
.concept-head .c-icon { font-size: 1.5rem; line-height: 1; }
.concept-head h3 { font-family: var(--serif); font-size: 1.32rem; margin: 0; color: var(--text); text-wrap: balance; }
.concept-parts { display: grid; grid-template-columns: 1fr 1.15fr 1fr; gap: 26px; align-items: start; }
.c-part .p-label {
  font-family: var(--mono); font-size: 0.68rem; text-transform: uppercase;
  letter-spacing: 0.08em; color: var(--gold); display: block; margin-bottom: 10px;
}
.c-part h4 { font-family: var(--serif); font-size: 1rem; margin: 0 0 8px; color: var(--text); line-height: 1.32; }
.c-part p { font-size: 0.91rem; color: var(--text-muted); margin: 0; }
.c-part.mechanism img {
  width: 100%; aspect-ratio: 1 / 1; display: block; border-radius: 10px;
  border: 1px solid var(--border); margin-bottom: 14px; background: var(--ink);
}
@media (max-width: 860px) { .concept-parts { grid-template-columns: 1fr; gap: 22px; } }

/* CALLOUT / STORY */
.story {
  background: var(--surface); border: 1px solid var(--gold); border-radius: 14px;
  padding: 32px 30px; margin-top: 30px;
}
.story .eyebrow { color: var(--v-adjacent); }
.story p { color: var(--text); font-size: 1.02rem; margin: 0 0 20px; }
.story p:last-child { margin-bottom: 0; }
.story .beat-label {
  font-family: var(--mono); font-size: 0.7rem; text-transform: uppercase;
  letter-spacing: 0.08em; color: var(--gold); display: block; margin-bottom: 8px;
}
.story .beat { margin-bottom: 22px; }
.story .beat:last-child { margin-bottom: 0; }
.map-bridge {
  text-align: center; font-family: var(--mono); font-size: 0.78rem; color: var(--text-faint);
  text-transform: uppercase; letter-spacing: 0.08em; margin: 40px 0 24px;
}

/* PIPELINE FIGURE */
.pipeline-figure {
  margin-top: 36px; border: 1px solid var(--border); border-radius: 12px;
  overflow: hidden; background: var(--ink);
}
.pipeline-figure img { width: 100%; display: block; }
.pipeline-legend { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 30px; }
.pl-item .pl-n { font-family: var(--mono); font-size: 0.72rem; color: var(--gold); letter-spacing: 0.05em; }
.pl-item h4 { font-family: var(--serif); font-size: 1.02rem; margin: 6px 0 6px; color: var(--text); }
.pl-item p { font-size: 0.88rem; color: var(--text-muted); margin: 0; }
@media (max-width: 720px) { .pipeline-legend { grid-template-columns: 1fr 1fr; } }

/* SCOREBOARD PREVIEW */
.stat-row { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 30px; }
.stat-pill {
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  padding: 16px 20px; flex: 1; min-width: 130px; text-align: center;
}
.stat-pill .n { font-family: var(--mono); font-variant-numeric: tabular-nums; font-size: 1.7rem; font-weight: 700; color: var(--gold-bright); display: block; }
.stat-pill .l { font-size: 0.78rem; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px; display: block; }

/* CTA BUTTON — standalone link, used by the leaderboard/whitepaper teasers */
.cta-btn {
  display: inline-flex; align-items: center; gap: 8px; margin-top: 32px;
  font-family: var(--mono); font-size: 0.84rem; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--ink); background: var(--gold); padding: 14px 26px; border-radius: 8px;
  text-decoration: none; transition: background 0.15s, transform 0.15s;
}
.cta-btn:hover { background: var(--gold-bright); transform: translateY(-1px); }
.cta-btn.secondary {
  background: transparent; color: var(--gold-bright); border: 1px solid var(--gold);
}
.cta-btn.secondary:hover { background: rgba(200,155,60,0.12); }

/* HERO CTAS — direct jump to Whitepaper / Leaderboard, no scrolling required */
.hero-ctas { display: flex; gap: 14px; margin: 0 0 30px; flex-wrap: wrap; }
.hero-ctas .cta-btn { margin-top: 0; }
@media (max-width: 860px) { .hero-ctas { justify-content: center; } }

/* LEADERBOARD TEASER — real top-ranked rows pulled from the live ledger */
.lb-rows { margin-top: 32px; border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
.lb-row {
  display: flex; align-items: flex-start; gap: 20px; padding: 24px;
  background: var(--surface); border-bottom: 1px solid var(--border);
}
.lb-row:last-child { border-bottom: none; }
.lb-rank { font-family: var(--serif); font-size: 1.5rem; color: var(--gold); flex-shrink: 0; width: 38px; }
.lb-body { flex: 1; min-width: 0; }
.lb-pairing { font-family: var(--serif); font-size: 1.05rem; color: var(--text); display: block; margin-bottom: 8px; line-height: 1.35; }
.lb-claim { font-size: 0.88rem; color: var(--text-muted); margin: 0 0 14px; }
.lb-why-label {
  font-family: var(--mono); font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--gold); display: block; margin-bottom: 5px;
}
.lb-why { font-size: 0.88rem; color: var(--text); margin: 0 0 14px; }
.lb-badges { display: flex; gap: 8px; flex-wrap: wrap; }
.lb-badge {
  font-family: var(--mono); font-size: 0.64rem; text-transform: uppercase; letter-spacing: 0.05em;
  padding: 3px 9px; border-radius: 5px; border: 1px solid var(--border); color: var(--text-faint);
}
.lb-badge.verdict-adjacent { color: var(--v-adjacent); border-color: var(--v-adjacent); }
.lb-points {
  font-family: var(--mono); font-variant-numeric: tabular-nums; font-size: 1.3rem; font-weight: 700;
  color: var(--gold-bright); flex-shrink: 0;
}
@media (max-width: 640px) {
  .lb-row { flex-wrap: wrap; }
  .lb-points { margin-left: auto; }
}

/* WHITEPAPER TEASER */
.wp-toc {
  margin-top: 32px; background: var(--surface); border: 1px solid var(--border);
  border-radius: 14px; padding: 30px 32px;
}
.wp-toc-label {
  font-family: var(--mono); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--gold); display: block; margin-bottom: 18px;
}
.wp-toc-list { margin: 0; padding-left: 22px; columns: 2; column-gap: 36px; }
.wp-toc-list li { font-size: 0.94rem; color: var(--text-muted); margin-bottom: 13px; break-inside: avoid; }
@media (max-width: 640px) { .wp-toc-list { columns: 1; } }

footer.colophon {
  padding: 40px 0 70px; color: var(--text-faint); font-size: 0.82rem; font-family: var(--mono);
  border-top: 1px solid var(--border); margin-top: 20px;
}
footer.colophon a { color: var(--text-muted); }
</style>
</head>
<body>

  <nav class="site-nav">
    <div class="site-nav-inner">
      <a class="site-nav-brand" href="landing.html">The Eureka Engine</a>
      <div class="site-nav-links">
        <a href="landing.html" class="is-active">Home</a>
        <a href="dashboard.html">Dashboard</a>
        <a href="whitepaper.html">Whitepaper</a>
        <a href="leaderboard.html">Leaderboard</a>
      </div>
    </div>
  </nav>

  <div class="hero">
    <div class="hero-grid">
      <div class="hero-text">
        <div class="kicker">Exponent Labs LLC</div>
        <h1>Our AI rediscovered a real MIT professor's theory &mdash; <em>before anyone told it the answer</em>.</h1>
        <p class="dek">This isn't a party trick. It's real research infrastructure &mdash; built to generate genuine scientific hypotheses and prove, out in the open, whether its reasoning actually holds up.</p>
        <div class="hero-ctas">
          <a class="cta-btn" href="whitepaper.html">Read the Whitepaper &rarr;</a>
          <a class="cta-btn secondary" href="leaderboard.html">See the Leaderboard &rarr;</a>
        </div>
        <div class="scroll-cue">&darr; keep scrolling</div>
      </div>
      <div class="hero-video">
        <video controls playsinline preload="metadata" poster="eureka-explainer-poster.jpg">
          <source src="eureka-explainer.mp4" type="video/mp4">
        </video>
        <p class="hv-caption">15 seconds &middot; sound on</p>
      </div>
    </div>
  </div>

  <div class="wrap">

    <section class="block" id="story-video">
      <div class="eyebrow">The Eureka Engine, In Action</div>
      <h2>The full story, told in 90 seconds</h2>
      <p class="lede">The same discovery from the headline above &mdash; how one autonomous run collided with a real MIT professor's theory, and what that actually means &mdash; narrated in full.</p>
      <div class="story-video-frame">
        <video controls playsinline preload="metadata" poster="eureka-story-poster.jpg">
          <source src="eureka-story.mp4" type="video/mp4">
        </video>
      </div>
      <p class="story-video-caption">90 seconds &middot; sound on</p>
    </section>

    <section class="block" id="system-map">
      <div class="eyebrow">The Eureka Engine In Action</div>
      <h2>It rediscovered Andrew Lo's Adaptive Market Hypothesis &mdash; on its own.</h2>

      <div class="story">
        <div class="beat">
          <span class="beat-label">The Setup</span>
          <p>One autonomous run pointed the engine's Janusian mode at a single domain: finance. Its job was to take the field's most sacred assumption &mdash; that markets are efficient, meaning prices already reflect all available information &mdash; and hold its exact opposite as equally true.</p>
        </div>
        <div class="beat">
          <span class="beat-label">The Ask</span>
          <p>Not a compromise (&ldquo;sometimes efficient, sometimes not&rdquo;). Not a synthesis (&ldquo;mostly efficient with a few exploitable cracks&rdquo;). A genuine paradox: both true, of the same market, at the same time.</p>
        </div>
        <div class="beat">
          <span class="beat-label">What It Did</span>
          <p>It proposed one: that market prices could be <strong class="accent">both efficient and inefficient simultaneously</strong>, producing unpredictable behavior no single truth could explain alone. It scored its own claim a 5 out of 5 for how heretical the idea was &mdash; and logged, honestly, that it had no evidence anyone had made this exact claim before.</p>
        </div>
        <div class="beat">
          <span class="beat-label">The Result</span>
          <p>When the system checked its own idea against live research, it found MIT economist <strong class="accent">Andrew Lo</strong>'s real, decades-old Adaptive Market Hypothesis &mdash; stating almost word-for-word the same paradox. Nobody told it. It found the collision on its own.</p>
        </div>
      </div>

      <p class="map-bridge">Here's the exact machine that found it</p>

      <span class="map-step-label">Step 1 &middot; Generate &mdash; it had three doors</span>
      <div class="map-fork">
        <div class="map-tile not-taken">
          <img src="data:image/jpeg;base64,__MECH_BISOCIATION_IMG__" alt="Bisociation diagram: two planes meeting at a glowing point" />
          <span class="mt-name">🧬 Bisociation</span>
          <span class="mt-cap">Collides two <em>different</em> fields into one point. Not this run &mdash; finance wasn't paired with anything else.</span>
          <span class="mt-tag">Not this run</span>
        </div>
        <div class="map-tile taken">
          <img src="data:image/jpeg;base64,__MECH_JANUSIAN_IMG__" alt="Janusian diagram: two faces looking opposite directions" />
          <span class="mt-name">🎭 Janusian</span>
          <span class="mt-cap">The one it walked. It took finance's own assumption &mdash; markets are efficient &mdash; and held the exact opposite equally true.</span>
          <span class="mt-tag">The move it took</span>
        </div>
        <div class="map-tile not-taken">
          <img src="data:image/jpeg;base64,__MECH_HOMOSPATIAL_IMG__" alt="Homospatial diagram: a hexagon and circle overlapping" />
          <span class="mt-name">🪞 Homospatial</span>
          <span class="mt-cap">Overlays two things into one new thing. Not this run &mdash; there was only one field to fold in on itself.</span>
          <span class="mt-tag">Not this run</span>
        </div>
      </div>

      <div class="map-arrow">&darr;</div>

      <div class="map-sequence">
        <div class="map-tile">
          <img src="data:image/jpeg;base64,__MECH_VERIFY_IMG__" alt="Web verification diagram: an eye radiating to four outcomes" />
          <span class="mt-name">🔍 Verify</span>
          <span class="mt-cap">Searched live research for the paradox &mdash; and found Andrew Lo's real Adaptive Market Hypothesis, stating almost the same thing.</span>
        </div>
        <div class="map-tile not-taken">
          <img src="data:image/jpeg;base64,__MECH_REFUTE_IMG__" alt="Adversarial refutation diagram: three sentinels testing a gem" />
          <span class="mt-name">⚖️ Refute</span>
          <span class="mt-cap">Skipped. The match was clean enough on its own &mdash; a direct hit against real, published research doesn't need a trial.</span>
          <span class="mt-tag">Skipped this run</span>
        </div>
        <div class="map-tile">
          <img src="data:image/jpeg;base64,__MECH_SCORE_IMG__" alt="Scoring diagram: a balance scale feeding a ranked staircase" />
          <span class="mt-name">🏆 Rank</span>
          <span class="mt-cap">Logged as a collision with a real, currently-active researcher &mdash; the strongest single match found that entire session.</span>
        </div>
      </div>
    </section>

    <section class="block" id="what">
      <div class="eyebrow">The Idea</div>
      <h2>Some of history's biggest discoveries came from connecting two things that had nothing to do with each other.</h2>
      <p class="lede">Newton connected an apple falling with the Moon orbiting the Earth &mdash; two things nobody thought belonged in the same sentence. That connection became gravity. Einstein took seriously that something could be <em>both moving and standing still at once</em>, depending on how you look at it. That became relativity.</p>
      <p class="body-text">Most of the time, smashing two unrelated ideas together produces nothing. But every once in a while it produces a real breakthrough &mdash; and scientists who study creativity have found that great discoveries tend to come from a small number of specific mental moves, not random luck. <strong class="accent">The Eureka Engine automates those moves on purpose</strong>, generates real candidate discoveries, and then checks every single one against actual science before it's allowed to claim credit.</p>
    </section>

    <section class="block" id="featured-hypotheses">
      <div class="eyebrow">Featured Hypotheses</div>
      <h2>Five real discoveries, ranked &mdash; this is what makes the engine real.</h2>
      <p class="lede">Anyone can claim an AI generates ideas. These are the top five, exactly as scored, with what they actually found and why each one is worth taking seriously.</p>

      <div class="lb-rows">
        <div class="lb-row">
          <span class="lb-rank">#1</span>
          <div class="lb-body">
            <span class="lb-pairing">Human Trust Variance &times; Cryptography &mdash; Zero-Knowledge Proofs</span>
            <p class="lb-claim">Trust dynamics between people and the evolution of zero-knowledge proofs might follow the same underlying pattern &mdash; improvements in one predicting improvements in the other.</p>
            <span class="lb-why-label">Why it matters</span>
            <p class="lb-why">Real research already treats &ldquo;trust&rdquo; as a technical property of cryptographic systems &mdash; but nobody's connected that math to how trust actually works between two people. If the pattern holds, it's a genuinely new bridge between psychology and cryptography.</p>
            <div class="lb-badges">
              <span class="lb-badge verdict-adjacent">Adjacent Active</span>
              <span class="lb-badge">🧬 Bisociative</span>
              <span class="lb-badge">🔬 Actively Researched</span>
            </div>
          </div>
          <span class="lb-points">+58</span>
        </div>
        <div class="lb-row">
          <span class="lb-rank">#2</span>
          <div class="lb-body">
            <span class="lb-pairing">Bridge Cable Tension &times; Bureaucratic Organizational Theory</span>
            <p class="lb-claim">An increase in tension imbalance in physical bridge cables might correlate with decreased effectiveness in bureaucratic structures &mdash; the same failure pattern, two different materials.</p>
            <span class="lb-why-label">Why it matters</span>
            <p class="lb-why">Organizational theorists already borrow engineering metaphors loosely. This hypothesis proposes something stricter &mdash; that the actual physics of how tension distributes across a bridge could predict where a bureaucracy is about to fail, not just describe it poetically.</p>
            <div class="lb-badges">
              <span class="lb-badge verdict-adjacent">Adjacent Active</span>
              <span class="lb-badge">🧬 Bisociative</span>
              <span class="lb-badge">🔬 Actively Researched</span>
            </div>
          </div>
          <span class="lb-points">+58</span>
        </div>
        <div class="lb-row">
          <span class="lb-rank">#3</span>
          <div class="lb-body">
            <span class="lb-pairing">Hash Collisions &times; Human Social Network Dynamics</span>
            <p class="lb-claim">A rise in informational hash collisions might correlate with a rise in new social connections forming &mdash; the same coincidence-driven pattern showing up in two unrelated systems.</p>
            <span class="lb-why-label">Why it matters</span>
            <p class="lb-why">Two real bodies of research already exist separately &mdash; one on coincidence in computing, one on coincidence in how people meet. Nobody has drawn the line connecting them. This hypothesis draws it.</p>
            <div class="lb-badges">
              <span class="lb-badge verdict-adjacent">Adjacent Active</span>
              <span class="lb-badge">🧬 Bisociative</span>
              <span class="lb-badge">🔬 Actively Researched</span>
            </div>
          </div>
          <span class="lb-points">+58</span>
        </div>
        <div class="lb-row">
          <span class="lb-rank">#4</span>
          <div class="lb-body">
            <span class="lb-pairing">Creative Block &mdash; Barrier and Facilitator, Simultaneously</span>
            <p class="lb-claim">Creative block might be both a barrier and a facilitator of creativity at the same time &mdash; genuinely engaging with a block, not avoiding it, could produce more innovative work than never hitting one.</p>
            <span class="lb-why-label">Why it matters</span>
            <p class="lb-why">Real psychology research already shows stepping <em>away</em> from a block precedes breakthroughs &mdash; but that's avoidance, not engagement. This hypothesis claims something more specific: engaging with the block directly, not distracting yourself from it, is what unlocks the work. That distinction is still untested.</p>
            <div class="lb-badges">
              <span class="lb-badge verdict-adjacent">Adjacent Active</span>
              <span class="lb-badge">🎭 Janusian</span>
              <span class="lb-badge">🔬 Actively Researched</span>
            </div>
          </div>
          <span class="lb-points">+58</span>
        </div>
        <div class="lb-row">
          <span class="lb-rank">#5</span>
          <div class="lb-body">
            <span class="lb-pairing">Mechanical Spring Systems &times; Human Emotional Fluctuation</span>
            <p class="lb-claim">Emotional responses might follow a mathematical model just like Hooke's Law &mdash; emotional intensity correlating directly with the degree of stimuli, the way a spring's force correlates with how far it's stretched.</p>
            <span class="lb-why-label">Why it matters</span>
            <p class="lb-why">Real, active research already builds mathematical models of emotion &mdash; but none of it uses spring mechanics specifically. If a literal Hooke's-Law-style model held up, it would mean predicting someone's emotional reaction with the same precision engineers use to predict how far a spring stretches.</p>
            <div class="lb-badges">
              <span class="lb-badge verdict-adjacent">Adjacent Active</span>
              <span class="lb-badge">🪞 Homospatial</span>
              <span class="lb-badge">🔬 Actively Researched</span>
            </div>
          </div>
          <span class="lb-points">+58</span>
        </div>
      </div>

      <a class="cta-btn" href="leaderboard.html">See all 40 hypotheses &rarr;</a>
    </section>

    <section class="block" id="pipeline">
      <div class="eyebrow">The Whole Loop</div>
      <h2>How one guess turns into a ranked, public leaderboard entry</h2>
      <p class="lede">Every hypothesis on that leaderboard passed through the same four-stage line before it earned a rank &mdash; nothing skips a stage, and nothing is added to the leaderboard by hand.</p>
      <div class="pipeline-figure">
        <img src="data:image/jpeg;base64,__PIPELINE_IMG__" alt="Diagram: four connected stages along a single glowing gold thread &mdash; two colliding triangular planes, an eye examining a glowing point, three sentinel figures testing a fourth glowing shape, and an ascending bar chart topped with a star" />
      </div>
      <div class="pipeline-legend">
        <div class="pl-item">
          <span class="pl-n">01 &middot; Generate</span>
          <h4>Explore</h4>
          <p>Bisociation, Janusian, or homospatial thinking collides two random fields and produces a candidate hypothesis.</p>
        </div>
        <div class="pl-item">
          <span class="pl-n">02 &middot; Verify</span>
          <h4>Web Search</h4>
          <p>Real, live research is checked. Does this already exist? Is it being actively studied? Does it fall apart on contact with the facts?</p>
        </div>
        <div class="pl-item">
          <span class="pl-n">03 &middot; Refute</span>
          <h4>Adversarial Test</h4>
          <p>Anything too ambiguous to call goes to three independent AI skeptics whose only job is to try to kill it.</p>
        </div>
        <div class="pl-item">
          <span class="pl-n">04 &middot; Rank</span>
          <h4>Score &amp; Publish</h4>
          <p>What survives is scored on novelty, resilience, and real-world research activity &mdash; then it earns its place on the public leaderboard.</p>
        </div>
      </div>
    </section>

    <section class="block" id="mechanisms">
      <div class="eyebrow">How It Generates Ideas</div>
      <h2>Three different ways to find a hidden connection</h2>
      <p class="lede">These aren't three flavors of the same trick &mdash; they're three genuinely different moves, each one linked to a real breakthrough in the history of science. For each: a real example first, then exactly how the move works, then where you'll start noticing it again.</p>

      <div class="concept">
        <div class="concept-head"><span class="c-icon">🧬</span><h3>Bisociation &mdash; Smash Two Ideas Together</h3></div>
        <div class="concept-parts">
          <div class="c-part">
            <span class="p-label">Notice This</span>
            <h4>An apple fell. The Moon didn't.</h4>
            <p>In 1666, Newton watched an apple fall and asked why the same pull might reach all the way to the Moon. Nobody had ever put &ldquo;falling&rdquo; and &ldquo;orbiting&rdquo; in the same sentence before. That one connection became gravity.</p>
          </div>
          <div class="c-part mechanism">
            <img src="data:image/jpeg;base64,__MECH_BISOCIATION_IMG__" alt="Diagram: two textured planes M1 and M2 meeting at a single glowing point of intersection" />
            <span class="p-label">How It Works</span>
            <h4>Find the one point where two frames touch.</h4>
            <p>Take two fields that have never been in the same conversation &mdash; drawn here as two separate planes, M<sub>1</sub> and M<sub>2</sub>. Psychologist Arthur Koestler called this <strong class="accent">bisociation</strong>: holding both frames in mind at once, then finding the single real, checkable point where they secretly line up. This diagram redraws Koestler's own 1964 sketch of the idea.</p>
          </div>
          <div class="c-part">
            <span class="p-label">Where It Shows Up Again</span>
            <h4>170 fields, one collision at a time.</h4>
            <p>Our engine runs this exact move on purpose, over and over, across 170 real academic fields &mdash; comedy and thermodynamics, neuroscience and supply chains &mdash; hunting for the next accidental apple.</p>
          </div>
        </div>
      </div>

      <div class="concept">
        <div class="concept-head"><span class="c-icon">🎭</span><h3>Janusian Thinking &mdash; Believe Two Opposites at Once</h3></div>
        <div class="concept-parts">
          <div class="c-part">
            <span class="p-label">Notice This</span>
            <h4>Moving, or standing still? Both.</h4>
            <p>Einstein imagined standing next to a beam of light and realized whether something is &ldquo;moving&rdquo; depends entirely on where you're standing. Something and its exact opposite were both true at once &mdash; just from different frames. That thought became relativity.</p>
          </div>
          <div class="c-part mechanism">
            <img src="data:image/jpeg;base64,__MECH_JANUSIAN_IMG__" alt="Diagram: two profile faces looking in opposite directions, sharing one glowing point between them" />
            <span class="p-label">How It Works</span>
            <h4>Hold the claim and its opposite, both fully true.</h4>
            <p>Named for Janus, the two-faced Roman god who looks both directions at once. Take a claim everyone treats as settled, take its exact opposite just as seriously &mdash; and refuse to average them into a boring compromise. Believing both, at the same time, is the move.</p>
          </div>
          <div class="c-part">
            <span class="p-label">Where It Shows Up Again</span>
            <h4>A mechanical check, not an honor system.</h4>
            <p>Every Janusian hypothesis has to pass a real check before it counts: is this a genuine paradox &mdash; both things true of the very same case &mdash; or just two different examples dressed up to look like one? Only the real ones survive.</p>
          </div>
        </div>
      </div>

      <div class="concept">
        <div class="concept-head"><span class="c-icon">🪞</span><h3>Homospatial Thinking &mdash; Blend Two Things Into One</h3></div>
        <div class="concept-parts">
          <div class="c-part">
            <span class="p-label">Notice This</span>
            <h4>A dolphin isn't a fast fish.</h4>
            <p>It's what happens when &ldquo;live in water&rdquo; and &ldquo;breathe air&rdquo; get laid completely on top of each other until one new animal falls out. Not a mix of two things side by side &mdash; a fusion into something genuinely new.</p>
          </div>
          <div class="c-part mechanism">
            <img src="data:image/jpeg;base64,__MECH_HOMOSPATIAL_IMG__" alt="Diagram: a hexagon and a circle fully overlapping, with a new glowing shape formed only where both coincide" />
            <span class="p-label">How It Works</span>
            <h4>Overlay two things until something survives the overlap.</h4>
            <p>Take two unrelated things and imagine them occupying the exact same space at the exact same time &mdash; not compared, but superimposed. Psychologist Albert Rothenberg documented this as one of the rarest moves behind real scientific creativity.</p>
          </div>
          <div class="c-part">
            <span class="p-label">Where It Shows Up Again</span>
            <h4>The easiest move to fake &mdash; so we check for faking.</h4>
            <p>It's easy to accidentally just compare two things with the word &ldquo;like.&rdquo; Our system scans its own output for comparison language and forces a rewrite whenever it slips in.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="block" id="verify">
      <div class="eyebrow">How It Checks Its Own Work</div>
      <h2>Anyone can make up a connection that <em>sounds</em> smart.</h2>
      <p class="lede">The hard part is telling a real discovery apart from something that just sounds clever. So every guess goes through two real rounds of fact-checking before it counts for anything.</p>

      <div class="concept">
        <div class="concept-head"><span class="c-icon">🔍</span><h3>Web Verification &mdash; Go Find Out</h3></div>
        <div class="concept-parts">
          <div class="c-part">
            <span class="p-label">Notice This</span>
            <h4>A claim costs nothing to say.</h4>
            <p>Anyone can say two ideas are secretly connected &mdash; the sentence is free. The only way to know if it's real is to go check, the same way a rumor either survives a phone call or it doesn't.</p>
          </div>
          <div class="c-part mechanism">
            <img src="data:image/jpeg;base64,__MECH_VERIFY_IMG__" alt="Diagram: an eye at the center with four threads radiating to four outcomes &mdash; a matched connection, a fertile unconnected gap, a broken claim, and an unresolved question mark" />
            <span class="p-label">How It Works</span>
            <h4>Four possible outcomes. No fifth option.</h4>
            <p>Every hypothesis is checked against real, live research and sorted into exactly one outcome: it's already been discovered <em>(a collision)</em>, it's genuinely unclaimed territory <em>(the target)</em>, it contradicts an actual fact <em>(a fail)</em>, or the search can't tell yet <em>(unresolved)</em>.</p>
          </div>
          <div class="c-part">
            <span class="p-label">Where It Shows Up Again</span>
            <h4>Getting &ldquo;scooped&rdquo; isn't a loss.</h4>
            <p>If our system keeps independently rediscovering real, published ideas with zero hints, that's evidence the reasoning behind it is sound &mdash; even on the guesses that turn out not to be new. See the Andrew Lo example at the top of this page.</p>
          </div>
        </div>
      </div>

      <div class="concept">
        <div class="concept-head"><span class="c-icon">⚖️</span><h3>Adversarial Refutation &mdash; Try to Kill It</h3></div>
        <div class="concept-parts">
          <div class="c-part">
            <span class="p-label">Notice This</span>
            <h4>Agreement isn't proof.</h4>
            <p>A claim that only survives one person's approval hasn't really been tested &mdash; it's just been agreed with. Real confidence comes from a claim surviving people who are actually trying to kill it.</p>
          </div>
          <div class="c-part mechanism">
            <img src="data:image/jpeg;base64,__MECH_REFUTE_IMG__" alt="Diagram: three hooded sentinel figures surrounding a small glowing gem, testing it from three directions" />
            <span class="p-label">How It Works</span>
            <h4>Three strangers, three angles, one verdict.</h4>
            <p>Anything the web search can't resolve goes to three separate AI instances &mdash; genuinely independent, blind to each other's reasoning &mdash; attacking it from three different angles: does it even make sense, could it be tested, and does it say something nontrivial. Two of three must survive for the claim to advance.</p>
          </div>
          <div class="c-part">
            <span class="p-label">Where It Shows Up Again</span>
            <h4>Guilty until proven innocent.</h4>
            <p>Under real uncertainty, the system defaults to killing the claim &mdash; the burden of proof sits on the hypothesis, not on the skeptics. That's what makes a &ldquo;survived&rdquo; verdict worth something.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="block" id="scoreboard">
      <div class="eyebrow">The Scoreboard</div>
      <h2>Every hypothesis gets scored, ranked, and made public &mdash; including the ones that got disproven.</h2>
      <p class="lede">Points come from three things weighed together, not from finishing a phase.</p>

      <div class="concept">
        <div class="concept-head"><span class="c-icon">🏆</span><h3>Scoring &amp; The Leaderboard &mdash; Make It Comparable</h3></div>
        <div class="concept-parts">
          <div class="c-part">
            <span class="p-label">Notice This</span>
            <h4>An opinion isn't a track record.</h4>
            <p>A guess that never gets ranked, dated, or checked against the ones before it is just an opinion floating in a chat log. Turning it into a number you can compare is what makes a track record possible.</p>
          </div>
          <div class="c-part mechanism">
            <img src="data:image/jpeg;base64,__MECH_SCORE_IMG__" alt="Diagram: a balance scale weighing three tokens on the left, feeding into an ascending staircase of bars topped with a star on the right" />
            <span class="p-label">How It Works</span>
            <h4>Three inputs, weighed, not just added.</h4>
            <p>Points come from how surprising the original idea was, whether it survived real scrutiny, and whether it matches research that's genuinely happening right now. A wild guess that gets refuted scores worse than a modest one that holds up.</p>
          </div>
          <div class="c-part">
            <span class="p-label">Where It Shows Up Again</span>
            <h4>Nothing gets quietly deleted.</h4>
            <p>Every hypothesis &mdash; including the ones proven wrong &mdash; stays on the public leaderboard, permanently, with its full reasoning attached.</p>
          </div>
        </div>
      </div>

      <div class="stat-row">
        <div class="stat-pill"><span class="n">__STAT_TOTAL__</span><span class="l">Hypotheses Tested</span></div>
        <div class="stat-pill"><span class="n">170</span><span class="l">Domains In The Pool</span></div>
        <div class="stat-pill"><span class="n">3</span><span class="l">Generation Methods</span></div>
        <div class="stat-pill"><span class="n">__STAT_REFUTED__</span><span class="l">Proven Wrong (And Kept, Not Hidden)</span></div>
      </div>
    </section>

    <section class="block" id="whitepaper-teaser">
      <div class="eyebrow">The Full Report</div>
      <h2>The technical writeup &mdash; what it got right, what it got wrong, and why.</h2>
      <p class="lede">Across all __STAT_TOTAL__ hypotheses in the pool &mdash; __STAT_PENDING_CLAUSE__: __STAT_COLLISION__ collided with real prior work, __STAT_ADJACENT__ found genuinely open territory, and __STAT_REFUTED__ were tested by independent skeptics and failed, __STAT_SURVIVAL_CLAUSE__, not smoothed over. We even tried to break that record on purpose &mdash; the strongest hypothesis in the pool, refuted too.</p>

      <div class="wp-toc">
        <span class="wp-toc-label">What's inside</span>
        <ol class="wp-toc-list">
          <li>What This Is, in One Story &mdash; the Darwin story, told from scratch</li>
          <li>Two Psychologists, Three Ways to Break Your Thinking Open &mdash; Koestler &amp; Rothenberg, explained plainly</li>
          <li>Why This Matters &mdash; What a Bad Hypothesis Costs (real research)</li>
          <li>How the Machine Does It &mdash; Three Mechanisms</li>
          <li>The Four-Phase Pipeline</li>
          <li>The Verification Layer</li>
          <li>Adversarial Refutation</li>
          <li>Points, Badges &amp; the Leaderboard</li>
          <li>Results</li>
          <li>Postmortem &mdash; the real bugs, not polished away</li>
          <li>Limitations</li>
          <li>Conclusion</li>
        </ol>
      </div>

      <a class="cta-btn" href="whitepaper.html">Read the full whitepaper &rarr;</a>
    </section>

  </div>

  <footer class="colophon">
    <div class="wrap">Exponent Labs LLC &middot; The Eureka Engine &middot; 2026-08-28 &middot; <a href="whitepaper.html">Report</a> &middot; <a href="leaderboard.html">Leaderboard</a></div>
  </footer>

</body>
</html>
'''

html = html.replace("__HERO_IMG__", hero_img)
html = html.replace("__MECH_BISOCIATION_IMG__", mech_bisociation_img)
html = html.replace("__MECH_JANUSIAN_IMG__", mech_janusian_img)
html = html.replace("__MECH_HOMOSPATIAL_IMG__", mech_homospatial_img)
html = html.replace("__PIPELINE_IMG__", pipeline_img)
html = html.replace("__MECH_VERIFY_IMG__", mech_verify_img)
html = html.replace("__MECH_REFUTE_IMG__", mech_refute_img)
html = html.replace("__MECH_SCORE_IMG__", mech_score_img)
html = html.replace("__STAT_TOTAL__", str(live_stats["total"]))
html = html.replace("__STAT_REFUTED__", str(live_stats["refuted"]))
html = html.replace("__STAT_COLLISION__", str(live_stats["collision"]))
html = html.replace("__STAT_ADJACENT__", str(live_stats["adjacent"]))
html = html.replace("__STAT_PENDING_CLAUSE__", live_stats["pending_clause"])
html = html.replace("__STAT_SURVIVAL_CLAUSE__", live_stats["survival_clause"])

with open("landing.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote landing.html ({len(html)/1024:.1f} KB)")
