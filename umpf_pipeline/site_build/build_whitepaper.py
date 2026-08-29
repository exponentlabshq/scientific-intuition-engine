#!/usr/bin/env python3
import base64

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

pipeline_img = b64("assets/pipeline-diagram.jpg")
classifier_img = b64("assets/classifier-diagram.jpg")
verdict_img = b64("assets/verdict-chart.jpg")

LEADERBOARD_URL = "https://claude.ai/code/artifact/1db8f5cd-85ce-496c-8f93-16002a06b8bf"

html = r'''<title>The Eureka Engine</title>

<style>
:root {
  --ink: #14110f;
  --paper: #1c1815;
  --surface: #241f1a;
  --border: #3a3229;
  --text: #ede6d8;
  --text-muted: #a89a86;
  --text-faint: #6f6455;
  --gold: #c89b3c;
  --v-adjacent: #5fa88f;
  --v-collision: #6f93bd;
  --v-refuted: #b56b6b;
  --v-pending: #8a8577;
  --serif: ui-serif, Georgia, 'Iowan Old Style', 'Times New Roman', serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Inter', ui-sans-serif, 'Segoe UI', sans-serif;
  --mono: ui-monospace, 'SF Mono', Menlo, monospace;
}
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    --ink: #faf7f0; --paper: #ffffff; --surface: #f6f2ea; --border: #ddd2bd;
    --text: #241f1a; --text-muted: #6b5f4d; --text-faint: #948a76; --gold: #8a6f2e;
  }
}
:root[data-theme="light"] {
  --ink: #faf7f0; --paper: #ffffff; --surface: #f6f2ea; --border: #ddd2bd;
  --text: #241f1a; --text-muted: #6b5f4d; --text-faint: #948a76; --gold: #8a6f2e;
}
* { box-sizing: border-box; }
body {
  background: var(--ink); color: var(--text); font-family: var(--sans);
  font-size: 16.5px; line-height: 1.7; margin: 0; padding: 0 22px 100px;
  -webkit-font-smoothing: antialiased;
}
.page { max-width: 760px; margin: 0 auto; }

.masthead { padding: 64px 0 40px; border-bottom: 2px solid var(--gold); }
.masthead .kicker {
  font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--gold); font-size: 0.78rem; margin-bottom: 14px;
}
.masthead h1 {
  font-family: var(--serif); font-size: clamp(2.1rem, 5vw, 3.1rem); font-weight: 600;
  margin: 0 0 14px; text-wrap: balance; letter-spacing: -0.01em;
}
.masthead .dek { color: var(--text-muted); font-size: 1.12rem; max-width: 600px; margin: 0 0 20px; }
.masthead .byline { color: var(--text-faint); font-size: 0.88rem; font-family: var(--mono); }

.abstract {
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  padding: 26px 28px; margin: 36px 0; font-size: 0.98rem; color: var(--text);
}
.abstract .label {
  font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--gold); font-size: 0.72rem; margin-bottom: 10px; display: block;
}

nav.toc {
  margin: 36px 0; padding: 22px 26px; border: 1px solid var(--border); border-radius: 10px;
}
nav.toc .label {
  font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--gold); font-size: 0.72rem; margin-bottom: 12px; display: block;
}
nav.toc ol { margin: 0; padding-left: 0; list-style: none; columns: 2; column-gap: 28px; }
nav.toc li { margin: 5px 0; font-size: 0.92rem; break-inside: avoid; }
nav.toc a { color: var(--text); text-decoration: none; border-bottom: 1px solid transparent; }
nav.toc a:hover { border-bottom-color: var(--gold); color: var(--gold); }

article section { margin: 56px 0; }
article h2 {
  font-family: var(--serif); font-size: 1.65rem; font-weight: 600; margin: 0 0 18px;
  padding-bottom: 10px; border-bottom: 1px solid var(--border); text-wrap: balance;
}
article h2 .num { color: var(--gold); font-family: var(--mono); font-size: 1rem; margin-right: 10px; }
article h3 { font-family: var(--serif); font-size: 1.2rem; font-weight: 600; margin: 28px 0 10px; color: var(--text); }
article p { margin: 14px 0; }
article ul, article ol.plain { margin: 14px 0; padding-left: 24px; }
article li { margin: 6px 0; }
article strong { color: var(--gold); font-weight: 600; }
article code { font-family: var(--mono); font-size: 0.85em; background: var(--surface); padding: 1px 6px; border-radius: 4px; }
article blockquote {
  margin: 20px 0; padding: 4px 22px; border-left: 3px solid var(--gold);
  color: var(--text-muted); font-style: italic; font-size: 1.02rem;
}
article a { color: var(--gold); }

figure { margin: 28px 0; text-align: center; }
figure img { max-width: 100%; border-radius: 10px; border: 1px solid var(--border); }
figure figcaption { color: var(--text-faint); font-size: 0.84rem; margin-top: 10px; font-family: var(--mono); }

.table-wrap { overflow-x: auto; margin: 20px 0; border: 1px solid var(--border); border-radius: 8px; }
table { border-collapse: collapse; width: 100%; font-size: 0.9rem; }
th, td { padding: 9px 13px; text-align: left; border-bottom: 1px solid var(--border); vertical-align: top; }
th { background: var(--surface); font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.04em; font-size: 0.74rem; color: var(--gold); }
td.num, th.num { font-family: var(--mono); font-variant-numeric: tabular-nums; text-align: right; }
tr:last-child td { border-bottom: none; }

.chip { display: inline-block; padding: 1px 9px; border-radius: 100px; font-size: 0.72rem; font-weight: 600; font-family: var(--mono); }
.chip.adj { color: var(--v-adjacent); background: rgba(95,168,143,0.14); }
.chip.col { color: var(--v-collision); background: rgba(111,147,189,0.14); }
.chip.ref { color: var(--v-refuted); background: rgba(181,107,107,0.14); }
.chip.pen { color: var(--v-pending); background: rgba(138,133,119,0.14); }

.callout {
  background: var(--surface); border-left: 3px solid var(--gold); border-radius: 0 8px 8px 0;
  padding: 16px 20px; margin: 20px 0; font-size: 0.94rem;
}
.callout.warn { border-left-color: var(--v-refuted); }
.callout .callout-label {
  font-family: var(--mono); text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.08em;
  color: var(--gold); display: block; margin-bottom: 8px;
}
.callout.warn .callout-label { color: var(--v-refuted); }

.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin: 24px 0; }
.stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 18px 20px; }
.stat-card .stat-num { font-family: var(--serif); font-size: 1.9rem; font-weight: 600; color: var(--gold); line-height: 1.1; }
.stat-card .stat-label { color: var(--text-muted); font-size: 0.86rem; margin-top: 6px; }
.stat-card .stat-src { color: var(--text-faint); font-size: 0.72rem; font-family: var(--mono); margin-top: 8px; }

.story-open {
  font-family: var(--serif); font-size: 1.12rem; line-height: 1.75; color: var(--text);
}
.story-open::first-letter {
  font-family: var(--serif); font-size: 3.4rem; font-weight: 600; color: var(--gold);
  float: left; line-height: 0.85; margin: 6px 8px 0 0;
}

.cta-link {
  display: block; margin: 24px 0; padding: 20px 24px; background: var(--surface);
  border: 1px solid var(--gold); border-radius: 10px; text-decoration: none; color: var(--text);
}
.cta-link:hover { background: var(--border); }
.cta-link .cta-title { font-family: var(--serif); font-size: 1.15rem; font-weight: 600; color: var(--gold); }
.cta-link .cta-sub { color: var(--text-muted); font-size: 0.88rem; margin-top: 4px; }

footer.colophon {
  margin-top: 64px; padding-top: 22px; border-top: 1px solid var(--border);
  color: var(--text-faint); font-size: 0.82rem; font-family: var(--mono);
}
</style>

<div class="page">
  <header class="masthead">
    <span class="kicker">Exponent Labs LLC &middot; Technical Report</span>
    <h1>The Eureka Engine</h1>
    <p class="dek">A machine that manufactures scientific hunches on purpose, thousands at a time &mdash; and then honestly checks each one before anyone wastes a year finding out by hand whether it was worth having.</p>
    <p class="byline">Exponent Labs LLC &middot; 2026-08-29 &middot; scientific-intuition-engine/umpf_pipeline</p>
  </header>

  <div class="abstract">
    <span class="label">Abstract</span>
    <p>Most scientific breakthroughs do not come from staring harder at one field &mdash; they come from smashing two unrelated fields together (Darwin reading an economics pamphlet; Einstein imagining a falling man). This report describes the Eureka Engine, a system that automates three specific, well-documented ways of forcing that collision &mdash; Arthur Koestler's <em>bisociation</em> and psychiatrist Albert Rothenberg's <em>Janusian</em> and <em>homospatial</em> thinking &mdash; and then, critically, checks honestly whether each resulting hypothesis is actually worth a researcher's time, the same way a fact-checker or a skeptical colleague would, before anyone spends real months finding out. Across 58 hypotheses drawn from a 170-domain pool (~14,365 possible pairings), the engine's four-way verification classifier found 23 COLLISION (the connection already exists in the literature &mdash; evidence the engine reasons soundly, even though the specific hypothesis has no novelty left), 19 ADJACENT_ACTIVE (real, fertile, unclaimed territory &mdash; the actual target state), 1 FACT_CHECK_FAIL, and 14 that reached NO_SIGNAL and were then independently refuted by three separate AI reviewers working blind to each other (0 of 14 survived). We also ran, for the first time, a control test &mdash; taking the single strongest hypothesis in the entire pool through the same refutation gauntlet specifically to check whether the lenses were calibrated to refute everything regardless of quality. It was refuted too, a genuinely uncomfortable finding reported here in full. Verification is no longer session-bound: a standalone script now runs it unattended against a real search API. We report the real engineering failures found along the way, including one this batch's Janusian mode hit three times in a row, and we ground the whole exercise in a genuinely uncomfortable fact about human research: PhD students spend an average of 7.3 years per degree, 40&ndash;60% never finish, and a widely cited 2015 economic analysis put the annual cost of irreproducible biomedical research in the United States alone at roughly $28.2 billion. This report exists to explain, from nothing, why that gap is worth automating &mdash; and to show the actual, disclosed record of an attempt to do it.</p>
  </div>

  <nav class="toc">
    <span class="label">Table of Contents</span>
    <ol>
      <li><a href="#story">1. What This Is, in One Story</a></li>
      <li><a href="#psychologists">2. Two Psychologists, Three Ways to Break Your Thinking Open</a></li>
      <li><a href="#cost">3. Why This Matters &mdash; What a Bad Hypothesis Costs</a></li>
      <li><a href="#methodology">4. How the Machine Does It &mdash; Three Mechanisms</a></li>
      <li><a href="#pipeline">5. The Four-Phase Pipeline</a></li>
      <li><a href="#verification">6. The Verification Layer</a></li>
      <li><a href="#refutation">7. Adversarial Refutation</a></li>
      <li><a href="#scoring">8. Points, Badges, and the Leaderboard</a></li>
      <li><a href="#results">9. Results</a></li>
      <li><a href="#postmortem">10. Postmortem</a></li>
      <li><a href="#limitations">11. Limitations</a></li>
      <li><a href="#conclusion">12. Conclusion</a></li>
    </ol>
  </nav>

  <article>

  <section id="story">
    <h2><span class="num">1</span>What This Is, in One Story</h2>
    <p class="story-open">In October 1838, Charles Darwin picked up a book that had nothing to do with finches, barnacles, or beetles. It was <em>An Essay on the Principle of Population</em>, an economics pamphlet by Thomas Malthus about the brutal arithmetic of famine &mdash; the observation that human populations grow faster than food supplies ever can, guaranteeing that most of every generation dies before it gets the chance to reproduce. Darwin was reading it, by his own account, &ldquo;for amusement.&rdquo; He wasn&rsquo;t looking for anything.</p>
    <p>He had, by then, spent two years turning over a puzzle from a five-year voyage around the world: why do closely related species on nearby islands differ in small, specific ways &mdash; a slightly different beak here, a slightly different shell there? He had the observations. He didn&rsquo;t have the mechanism. Then, reading Malthus&rsquo;s chapter on the mathematics of overcrowded cities, something clicked. If human populations are held in check by a permanent, brutal excess of births over food, then every wild population must be too. Every generation of every species is born into a competition it mostly loses. And the individuals that happen to carry some small edge &mdash; survive that competition more often than their siblings, on average, over and over, for millions of generations. No one has to design anything. You get evolution by natural selection.</p>
    <p>Darwin named the collision himself, later, in his autobiography: reading Malthus is where the idea &ldquo;at once occurred to me.&rdquo; The single most consequential idea in the history of biology was not produced by staring harder at finches. It was produced by forcing two fields that had nothing to do with each other &mdash; population economics and natural history &mdash; into the same sentence.</p>
    <p>This is not a freak occurrence. Johannes Kepler spent years trying to explain planetary orbits using the geometry of musical harmony. Claude Shannon founded information theory by noticing that the on/off logic of telephone relay switches was, structurally, the same thing as the true/false logic of Boolean algebra &mdash; a discipline built decades earlier to formalize philosophical logic, with no telephones in mind at all. The pattern recurs often enough across the history of science that it is worth asking a genuinely strange question: <strong>what if the collision itself &mdash; not talent, not luck, not years of immersion in one field &mdash; is the actual mechanism, and it can be done on purpose?</strong></p>
    <p>A <strong>hypothesis</strong>, in the sense this report uses the word, is nothing more exotic than a specific, falsifiable guess about how two things are secretly connected &mdash; precise enough that it could turn out to be wrong. Darwin&rsquo;s guess was falsifiable: if population pressure didn&rsquo;t actually produce differential survival, the theory would collapse. Most guesses like this, tried by most people, go nowhere &mdash; a plausible-sounding connection that turns out, on inspection, to already be well known, or to not actually hold up, or to be too vague to ever be wrong. Finding that out is the slow, expensive part of research (Section 3 puts real numbers on exactly how expensive).</p>
    <p>The Eureka Engine is an attempt to automate both halves of what Darwin did by accident once: <strong>force the collision on purpose, over and over, across a large pool of real subjects</strong> &mdash; and then <strong>honestly check each result</strong>, the way a skeptical colleague would, before anyone spends a year of their life finding out the hard way. Everything after this section describes exactly how.</p>
  </section>

  <section id="psychologists">
    <h2><span class="num">2</span>Two Psychologists, Three Ways to Break Your Thinking Open</h2>
    <p>Darwin&rsquo;s collision has a name. Two researchers, working decades apart, each independently studied how minds actually produce insights like his &mdash; and between them, they described three distinct mechanisms, not one. The Eureka Engine implements all three, faithfully, as three separate operating modes.</p>

    <h3>Koestler and bisociation &mdash; two frames, collided</h3>
    <p>Arthur Koestler was not, by training, a scientist. He was a Hungarian-British novelist and journalist who, in 1964, published a 750-page book called <em>The Act of Creation</em>, trying to find one shared mechanism underneath humor, art, and scientific discovery &mdash; three things that don&rsquo;t obviously belong together. His answer was a word he had to coin himself, because no existing word did the job: <strong>bisociation</strong>.</p>
    <p>Ordinary thinking, Koestler argued, stays inside one habitual &ldquo;matrix&rdquo; &mdash; one self-consistent frame of reference, one set of rules you already know how to follow. <em>Association</em> is finding a new idea inside that one frame. <em>Bisociation</em> is something structurally different: perceiving a situation from inside <em>two</em> self-consistent frames at once, frames that are normally kept completely apart. Koestler&rsquo;s own favorite illustration was the joke: a story appears to be going one way, following one frame &mdash; and the punchline suddenly reveals it fits a second, totally different frame just as well. The laugh is the click of two matrices colliding. Koestler&rsquo;s claim was that the exact same click, taken seriously instead of played for a laugh, is what produces both great art and great science. Darwin&rsquo;s moment with Malthus is a clean, real-world case: population economics is one matrix, natural history is a second, and neither one by itself contains natural selection. The insight lives only in the collision.</p>
    <p>The Eureka Engine&rsquo;s <strong>bisociation mode</strong> does exactly this, mechanically: it takes two genuinely unrelated domains from its pool, forces them together, and asks the model to propose a specific structural correspondence between them &mdash; not a cute metaphor (&ldquo;markets are <em>like</em> ecosystems&rdquo;), but a precise, falsifiable mapping specific enough that it could turn out to be wrong.</p>

    <h3>Rothenberg and Janusian thinking &mdash; two opposites, both true at once</h3>
    <p>Albert Rothenberg is an American psychiatrist who spent decades doing something almost nobody else in creativity research has done: instead of theorizing from an armchair, he got direct access to genuinely eminent scientists and Nobel laureates and studied, from real interviews and primary documents, how they actually described their own thinking in the specific minutes before a breakthrough. From that work he named a second mechanism, distinct from Koestler&rsquo;s: <strong>Janusian thinking</strong>, named for Janus, the Roman god sculpted with two faces looking in opposite directions simultaneously.</p>
    <p>Janusian thinking is actively conceiving two opposite or contradictory ideas as true <em>at the same time, in the same respect</em> &mdash; not &ldquo;it depends on context,&rdquo; not &ldquo;somewhere in between,&rdquo; but genuinely both, held together on purpose rather than resolved away. Rothenberg&rsquo;s clearest example is Einstein. In 1907, years before general relativity, Einstein described what he later called &ldquo;the happiest thought of my life&rdquo;: imagine a person falling freely off a roof. That person feels <em>no gravity at all</em> &mdash; weightless, exactly as if they were floating at rest in empty space. And yet, at that exact same instant, that same person is being pulled by the Earth and is accelerating downward as hard as gravity can pull them. <em>At rest</em> and <em>accelerating</em> are opposites. Ordinary thinking picks one. Einstein held both as completely, simultaneously true &mdash; and that specific act, a deliberate refusal to resolve the contradiction, is the seed Rothenberg traces directly forward to the equivalence principle: the idea, published nine years later, that gravity and acceleration are not just similar but literally indistinguishable, the foundation stone of general relativity.</p>
    <p>The Eureka Engine&rsquo;s <strong>Janusian mode</strong> reproduces this directly: it takes one domain&rsquo;s foundational, load-bearing assumption and forces the system to state &mdash; not hedge, not split into &ldquo;sometimes A, sometimes B&rdquo; &mdash; the exact opposite as also, simultaneously, true, then asks what would have to be real for both to genuinely hold. (Section 10 describes a real failure mode here: models kept quietly smuggling in the &ldquo;it depends&rdquo; version and calling it a paradox anyway &mdash; and what it took to actually stop them.)</p>

    <h3>Rothenberg and homospatial thinking &mdash; two things, superimposed into one</h3>
    <p>Rothenberg&rsquo;s second, less widely known finding came from the same research program: <strong>homospatial thinking</strong> &mdash; actively conceiving two or more distinct entities occupying the exact same space at once, a conception that forces the mind to find or invent a genuinely new relationship between them. He didn&rsquo;t just theorize this; he ran real experiments. He showed subjects pairs of ordinary photographs physically superimposed on top of each other &mdash; two images sharing one rectangle, at the same time &mdash; and asked them to write. Subjects shown the superimposed pair, compared with subjects shown the same two photographs side by side, produced measurably more original and more vivid metaphors. The superimposition itself, not talent alone, was doing creative work.</p>
    <p>A similar &mdash; though historically disputed &mdash; story is often told about the chemist August Kekulé, who claimed decades later that the ring structure of the benzene molecule came to him in a half-waking daydream of a snake biting its own tail: two separate images, a snake and a chain of atoms, briefly occupying one space. Historians of science doubt the story&rsquo;s exact details. But whether or not it happened quite that way, it has exactly the shape of a homospatial insight &mdash; two things fused into one, rather than compared side by side.</p>
    <p>The Eureka Engine&rsquo;s <strong>homospatial mode</strong> is built to force the real thing, not the easy substitute: instead of comparing two domains (&ldquo;X is like Y&rdquo;), it requires the model to fuse them into one new entity that belongs to neither source domain &mdash; and the pipeline mechanically scans the output and rejects any answer that&rsquo;s secretly just a metaphor wearing a made-up name (Section 10, Failure 2, is the real story of how much enforcement that turned out to require).</p>

    <p>None of this required a machine, in principle &mdash; Darwin, Einstein, and Kekulé (real or embellished) each did it with nothing but their own mind, once, after years of immersion in their field. What a machine changes is scale. A single researcher gets, at most, a handful of true collisions in an entire working lifetime, most of them arrived at by accident. The Eureka Engine runs these same three moves deliberately, on demand, against a pool of 170 real domains &mdash; not waiting for the accident, but forcing it, thousands of times.</p>
  </section>

  <section id="cost">
    <h2><span class="num">3</span>Why This Matters &mdash; What a Bad Hypothesis Costs</h2>
    <p>Running the collision, it turns out, is the easy part &mdash; the rest of this report shows a model producing a plausible-sounding cross-domain hypothesis in seconds. The hard, slow, expensive part of science has never been having an idea. It has always been finding out, honestly, whether the idea was actually worth having &mdash; and today, that discovery mostly happens the slow way: a real researcher spends months or years testing it before anyone knows.</p>
    <p>That cost is not hypothetical. It is one of the best-documented, least-discussed facts about how research actually works:</p>
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-num">7.3 yrs</div>
        <div class="stat-label">average time to complete a PhD in the United States</div>
        <div class="stat-src">Council of Graduate Schools completion-rate data</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">40&ndash;60%</div>
        <div class="stat-label">of students who start a PhD program never finish it &mdash; attrition climbs from ~10&ndash;15% in year one to ~50% by year five</div>
        <div class="stat-src">Council of Graduate Schools; multiple doctoral-attrition literature reviews</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">84%</div>
        <div class="stat-label">of surveyed biomedical PhD students had failed to replicate their own prior results at least once</div>
        <div class="stat-src">2023 survey/interview study, biomedical doctoral students</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">$28.2B/yr</div>
        <div class="stat-label">estimated annual cost of irreproducible preclinical biomedical research in the U.S. alone</div>
        <div class="stat-src">Freedman, Cockburn &amp; Simcoe, <em>PLOS Biology</em>, 2015</div>
      </div>
    </div>
    <p>The same 2023 study found that 70% of those students had also failed to replicate a colleague&rsquo;s finding, and 58% had failed to replicate a result from the published literature &mdash; and for roughly a quarter of the students surveyed, the resulting stress was severe enough to interfere with eating, sleeping, or the ability to work. The $28.2 billion figure, from a 2015 economic analysis in <em>PLOS Biology</em>, is deliberately conservative: it assumes only half of preclinical biomedical research is irreproducible, when some independent estimates run as high as 89%.</p>
    <p>There is a second, quieter version of the same problem: research that fails is far less likely to ever be written up at all. This is what researchers call the <strong>file-drawer problem</strong> &mdash; the negative and null results that would honestly tell the field a hypothesis didn&rsquo;t pan out mostly never leave the researcher&rsquo;s own file drawer. One dataset tracking published papers found the share reporting a positive, statistically significant result rose past 80% after 1999 and reached 88.6% by 2005 &mdash; not because negative results are rare in the lab, but because they are dramatically less likely to be written up and submitted for publication in the first place.</p>
    <p>None of these numbers are about the Eureka Engine, or about AI at all. They describe the ordinary, already-existing condition of human research &mdash; an enormous amount of skilled, well-intentioned, expensive effort spent finding out, the slow way, that a particular idea doesn&rsquo;t hold up, with the negative result then largely vanishing rather than sparing the next person the same trip.</p>
    <p>This is exactly the gap the rest of this report&rsquo;s pipeline is built to sit inside. Generation (Phase 1, Section 5) is cheap &mdash; a model proposes a hypothesis in the time it takes to read this sentence. What Phase 2&rsquo;s verification classifier (Section 6) and Phase 3&rsquo;s adversarial refutation (Section 7) exist to do is compress, into minutes and the cost of a handful of search queries, the version of &ldquo;does this actually hold up&rdquo; a human researcher would otherwise spend a year of bench time discovering alone. It cannot and does not replace that year of real experimental work for a hypothesis that survives &mdash; nothing computational substitutes for a real experiment. But for the hypotheses that would have failed anyway, which the numbers above suggest is most of them, catching that earlier and cheaply, before a real person spends a year finding out by hand, is the entire point of everything that follows.</p>
  </section>

  <section id="methodology">
    <h2><span class="num">4</span>How the Machine Does It &mdash; Three Mechanisms</h2>
    <p>Section 2 told these three mechanisms as stories, one researcher at a time. This section describes exactly how the Eureka Engine turns each one into a repeatable step it can run against any two domains pulled from its pool &mdash; not three settings of one prompt, but three structurally different generation modes, each with its own geometry.</p>
    <div class="table-wrap">
      <table>
        <tr><th>Mechanism</th><th>Geometry</th><th>What it produces</th><th>Doctrine source</th></tr>
        <tr><td><strong>Bisociation</strong></td><td>Horizontal &mdash; two domains collide, each stays itself</td><td>A candidate functor mapping between them</td><td>Koestler, <em>The Act of Creation</em> (1964)</td></tr>
        <tr><td><strong>Janusian</strong></td><td>Vertical &mdash; one domain&rsquo;s proposition held against its exact opposite</td><td>A falsifiable paradox &mdash; genuinely both true at once, not a compromise</td><td>Rothenberg, 1976/1979</td></tr>
        <tr><td><strong>Homospatial</strong></td><td>Overlaid &mdash; two domains superimposed in the same conceptual space</td><td>One fused entity belonging to neither source</td><td>Rothenberg, 1976; cognitive-science successor: conceptual blending (Fauconnier &amp; Turner)</td></tr>
      </table>
    </div>
    <p>One term in that table is worth unpacking rather than skating past: a <strong>functor</strong>, borrowed loosely from category theory, just means a structure-preserving map &mdash; a specific, stated rule for translating a concept in one domain into its counterpart in the other, precise enough to be checked and found right or wrong. That precision is what separates a bisociation hypothesis from an ordinary metaphor: &ldquo;markets are like ecosystems&rdquo; is not falsifiable; &ldquo;overcrowding in market X should produce the same boom-bust cycle observed in population Y, on the same rough timescale&rdquo; is.</p>
    <p>Each mechanism turned out to have a real, exploitable failure mode a naive implementation would have missed &mdash; documented in full, with the actual fixes, in <a href="#postmortem">Section 10</a>.</p>
  </section>

  <section id="pipeline">
    <h2><span class="num">5</span>The Four-Phase Pipeline</h2>
    <p>Generation &mdash; the three mechanisms above &mdash; is only Phase 1 of four. A hypothesis is worthless left alone; the rest of the pipeline exists to check it.</p>
    <figure>
      <img src="data:image/jpeg;base64,__PIPELINE_IMG__" alt="Four-phase pipeline diagram: Exploration, Web Verification, Researcher Outreach, Data Update" />
      <figcaption>Figure 1 &mdash; the four-phase pipeline</figcaption>
    </figure>
    <ol class="plain">
      <li><strong>Exploration</strong> &mdash; the three generation mechanisms, drawing domain pairs from the combined 170-domain pool.</li>
      <li><strong>Web Verification</strong> &mdash; the four-way classifier that checks each hypothesis against real search results (<a href="#verification">Section 6</a>).</li>
      <li><strong>Researcher Outreach</strong> &mdash; for hypotheses that clear verification as genuinely fertile, draft (never auto-send) a short email to a real, named researcher active in the adjacent field the verification pass surfaced.</li>
      <li><strong>Data Update</strong> &mdash; reconcile whatever Phase 3 reveals back into the hypothesis&rsquo;s status.</li>
    </ol>
    <div class="callout">
      <span class="callout-label">A fixed constraint, not a per-case judgment call</span>
      Phase 3 produces drafts only. No email is ever sent by this pipeline autonomously. Every draft would carry an explicit &ldquo;NOT SENT&mdash;requires sign-off&rdquo; banner, and contact-confidence tiering follows a strict no-aggregator-as-confirmed discipline. To date, zero Phase 3 drafts have been produced &mdash; no hypothesis has yet reached the bar that would trigger one (see <a href="#results">Section 9</a>).
    </div>
  </section>

  <section id="verification">
    <h2><span class="num">6</span>The Verification Layer</h2>
    <p>Think of this phase as a fact-checker with one job: for a given hypothesis, honestly answer whether someone has already said this, whether real unclaimed territory sits nearby, or whether the underlying premise doesn&rsquo;t even hold up. Every generated hypothesis&rsquo;s own self-critique includes a &ldquo;known prior art: not verified&rdquo; line &mdash; an honest admission that the model that generated it cannot check its own novelty claim. Phase 2 resolves that admission against real web search, sorting each result into one of four outcomes:</p>
    <figure>
      <img src="data:image/jpeg;base64,__CLASSIFIER_IMG__" alt="Four-way verdict classifier: COLLISION, ADJACENT_ACTIVE, FACT_CHECK_FAIL, NO_SIGNAL" />
      <figcaption>Figure 2 &mdash; the four-way classifier</figcaption>
    </figure>
    <p>The design decision underneath this figure is that it&rsquo;s <strong>four buckets, not a pass/fail binary</strong> &mdash; because &ldquo;did the search find something&rdquo; actually collapses two signals that point in opposite directions. Finding the <em>exact</em> connection already published proves the engine&rsquo;s reasoning is sound &mdash; but it also means the specific hypothesis has zero marginal novelty left. Finding real, active research <em>near</em> the domains, without the exact connection having been drawn, is the actual target state: real, fertile, unclaimed ground. Collapsing both into one &ldquo;found something&rdquo; bit would reward the engine for rediscovering consensus over producing discovery.</p>
    <h3>The umbrella-trap rule</h3>
    <p>A second rule, discovered empirically rather than planned upfront: a bridging field only counts as ADJACENT_ACTIVE evidence if it is genuinely <em>specific</em> &mdash; if it would <em>not</em> return the same hit for most other domain pairs in the pool. The first real case this caught: a Neuroscience&times;Climatology hypothesis where the only bridging material found was &ldquo;both are complex adaptive systems&rdquo; &mdash; true of nearly any two nonlinear domains that exist. Treating that as confirmation would have made the ADJACENT_ACTIVE bucket meaningless, since it would confirm almost anything the engine could ever propose. The hypothesis was correctly routed to NO_SIGNAL instead, and later failed independent adversarial refutation on all three lenses (<a href="#refutation">Section 7</a>).</p>
  </section>

  <section id="refutation">
    <h2><span class="num">7</span>Adversarial Refutation</h2>
    <p>If Phase 2 is a fact-checker, this phase is closer to a hostile peer-review panel &mdash; except each reviewer works entirely alone, has never seen the other two&rsquo;s notes, and is specifically trying to find the one flaw that kills the claim. It exists because NO_SIGNAL is the one verdict Phase 2 cannot resolve by design: it looks identical whether a hypothesis is genuinely novel-and-real, or vacuous-and-not-even-wrong, because nothing external exists yet to check it against. Adversarial refutation attacks the claim&rsquo;s own internal structure instead of searching for prior art, through three independent lenses:</p>
    <ul>
      <li><strong>Coherence</strong> &mdash; does the claimed mapping quietly equivocate on a term as it crosses from one domain into the other?</li>
      <li><strong>Testability</strong> &mdash; is the falsifiable prediction actually operationalized, or vague enough that nothing could ever return a clean &ldquo;no&rdquo;?</li>
      <li><strong>Triviality</strong> &mdash; stripped of its domain-specific vocabulary, does the claim reduce to something true of almost any two complex systems?</li>
    </ul>
    <p>Promotion out of NO_SIGNAL requires 2 of 3 lenses to find the claim survives. Every lens defaults to REFUTED under genuine uncertainty &mdash; a deliberate asymmetry against false positives, on the theory that a hypothesis wrongly killed costs nothing, while a hollow one wrongly promoted costs someone real time later.</p>
    <h3>Independence, not just repetition</h3>
    <p>The first refutation round used one reasoner working through all three lenses sequentially &mdash; a real limitation, since a genuine committee has independent reviewers, not one mind switching hats. Re-run with 12 genuinely separate reviewer instances (3 lenses &times; 4 cases, each blind to the original reasoning and to each other): <strong>12 of 12 confirmed REFUTED</strong>, full agreement &mdash; and every single lens surfaced at least one finding the original pass had missed. The sharpest catch: for a Neural-Networks&times;Coral-Reef case study, an independent reviewer was asked simply to check whether the paper&rsquo;s own abstract-promised &ldquo;Section 6: hypothesis and experiment&rdquo; actually existed in the document. It didn&rsquo;t &mdash; the paper cuts off mid-Section-4. The falsifiable content its own abstract promised had never been written. A second round on two more NO_SIGNAL cases came back <strong>6 of 6 REFUTED</strong>, again unanimous. A third round, on the newest NO_SIGNAL case (astronomy &times; album production), came back <strong>3 of 3 REFUTED</strong>.</p>
    <p>Across every refutation attempt to date, <strong>0 of 14 hypotheses have survived</strong>. A control test extends this further: the single strongest hypothesis in the entire pool &mdash; already independently verified ADJACENT_ACTIVE with real, citable evidence &mdash; was run through the exact same three-lens gauntlet specifically to check whether the lenses simply refute everything regardless of quality. It was refuted too (0 of 3), on grounds that held up under inspection: the real-world connection Phase 2 had found was, all three lenses independently noticed, a homonym of the hypothesis's own claim, not the structural match it asserted. This is treated as real, useful signal about the current domain pool and prompt calibration &mdash; disclosed plainly, not smoothed over, and not treated as proof the underlying mechanism is broken (see <a href="#limitations">Section 11</a> for what the control test does and doesn't resolve).</p>
  </section>

  <section id="scoring">
    <h2><span class="num">8</span>Points, Badges, and the Leaderboard</h2>
    <p>Points are tied to what an outcome actually reveals about a hypothesis&rsquo;s real potential, not to how far it made it through the pipeline:</p>
    <div class="table-wrap">
      <table>
        <tr><th>Event</th><th class="num">Points</th><th>Why</th></tr>
        <tr><td>Phase 2: ADJACENT_ACTIVE</td><td class="num">+30</td><td>The actual target state</td></tr>
        <tr><td>Phase 2: COLLISION (genuine)</td><td class="num">+5</td><td>Zero novelty, but real credit for valid reasoning</td></tr>
        <tr><td>Phase 2: COLLISION (not a valid bisociation)</td><td class="num">&minus;5</td><td>Worse than genuine collision &mdash; the pairing itself was flawed</td></tr>
        <tr><td>Phase 2: FACT_CHECK_FAIL</td><td class="num">&minus;10</td><td>Hallucinated domain facts</td></tr>
        <tr><td>Refutation: survives (2&ndash;3 of 3)</td><td class="num">+12 / +20</td><td>Real signal the claim isn&rsquo;t vacuous</td></tr>
        <tr><td>Refutation: REFUTED</td><td class="num">&minus;15</td><td>Worse than a fact-check failure &mdash; the reasoning failed under scrutiny</td></tr>
        <tr><td>Phase 3: researcher confirms novel</td><td class="num">+50</td><td>The single strongest possible signal</td></tr>
        <tr><td>Phase 3: researcher dismisses</td><td class="num">&minus;20</td><td>A real expert said no</td></tr>
      </table>
    </div>
    <a class="cta-link" href="__LEADERBOARD_URL__" target="_blank" rel="noopener">
      <div class="cta-title">Open the Leaderboard Experience &rarr;</div>
      <div class="cta-sub">Every hypothesis this report describes, ranked, filterable by mode and verdict, expandable to the full record &mdash; the actual hypothesis text, verification reasoning, and refutation reasoning where it ran.</div>
    </a>
  </section>

  <section id="results">
    <h2><span class="num">9</span>Results</h2>
    <figure>
      <img src="data:image/jpeg;base64,__VERDICT_IMG__" alt="Bar chart: final status across 58 hypotheses" />
      <figcaption>Figure 3 &mdash; final status, all 58 hypotheses</figcaption>
    </figure>
    <p>All 58 hypotheses in the current pool now carry a canonical verdict &mdash; none are pending. <strong>23 COLLISION</strong> (real prior art already exists), <strong>19 ADJACENT_ACTIVE</strong> (fertile, unclaimed territory &mdash; the target state), <strong>14 NO_SIGNAL</strong> (all 14 subsequently refuted on independent adversarial review), <strong>1 FACT_CHECK_FAIL</strong>, and <strong>1 FLAGGED</strong> (a factual concern with the pairing itself, held out of scoring). A second batch of 18 (6 per mode) was generated and verified in this pass &mdash; the first real production run of the standalone verification script described in Section 5.</p>
    <h3>By generation mechanism</h3>
    <div class="table-wrap">
      <table>
        <tr><th>Mode</th><th class="num">n resolved</th><th class="num">Collision</th><th class="num">Adjacent</th><th class="num">Refuted</th><th class="num">Fact-Fail</th></tr>
        <tr><td>Bisociation</td><td class="num">16</td><td class="num">31%</td><td class="num">38%</td><td class="num">31%</td><td class="num">&mdash;</td></tr>
        <tr><td>Janusian</td><td class="num">16</td><td class="num">56%</td><td class="num">19%</td><td class="num">19%</td><td class="num">6%</td></tr>
        <tr><td>Homospatial</td><td class="num">13</td><td class="num">23%</td><td class="num">54%</td><td class="num">23%</td><td class="num">&mdash;</td></tr>
        <tr><td>Pre-existing case studies</td><td class="num">13</td><td class="num">46%</td><td class="num">23%</td><td class="num">23%</td><td class="num">&mdash;</td></tr>
      </table>
    </div>
    <p><em>Janusian&rsquo;s collision rate settled from an early 100% (n=5) down to 56% (9 of 16) as the sample grew &mdash; still the strongest-colliding mode, but the small-n number was optimistic, exactly as flagged it might be. Bisociation and homospatial both show the more typical pattern: real spread across all three live outcomes. The second batch's Janusian refutations were also the most informative failure of this pass &mdash; three separate Janusian hypotheses in a row (cognitive AI preprocessing, knowledge systems, urban planning zoning) turned out to be the exact same disguised compromise the same-instance test was built to catch, each one's own self-critique quietly conceding "different contexts" or "different datasets" rather than a true same-instance paradox. That the same-instance test let three through in one batch, after already being added specifically to catch this pattern, is a real, unresolved finding &mdash; see Section 11.</em></p>
    <h3>Top of the leaderboard</h3>
    <div class="table-wrap">
      <table>
        <tr><th>Rank</th><th>Pairing</th><th class="num">Points</th><th>Verdict</th></tr>
        <tr><td>1</td><td>Human Trust Variance &times; Cryptography (zero-knowledge proofs)</td><td class="num">+58</td><td><span class="chip adj">ADJACENT_ACTIVE</span></td></tr>
        <tr><td>2</td><td>Physical Bridge Cable Tension &times; Organizational Theory</td><td class="num">+58</td><td><span class="chip adj">ADJACENT_ACTIVE</span></td></tr>
        <tr><td>3</td><td>Informational Hash Collisions &times; Human Social Network Dynamics</td><td class="num">+58</td><td><span class="chip adj">ADJACENT_ACTIVE</span></td></tr>
        <tr><td>4</td><td>Creative Block (Janusian) &mdash; barrier and facilitator, simultaneously</td><td class="num">+58</td><td><span class="chip adj">ADJACENT_ACTIVE</span></td></tr>
        <tr><td>5</td><td>Mechanical Spring Systems &times; Human Emotional Fluctuation</td><td class="num">+58</td><td><span class="chip adj">ADJACENT_ACTIVE</span></td></tr>
        <tr><td>6</td><td>Narrative Arc Development &times; Distributed Consensus</td><td class="num">+58</td><td><span class="chip adj">ADJACENT_ACTIVE</span></td></tr>
        <tr><td>&hellip;</td><td colspan="3">full ranking of all 58 in the <a href="__LEADERBOARD_URL__" target="_blank" rel="noopener">Leaderboard Experience</a></td></tr>
      </table>
    </div>
  </section>

  <section id="postmortem">
    <h2><span class="num">10</span>Postmortem</h2>
    <p>Four real failures were found along the way &mdash; three fixed, one still open &mdash; reported in full rather than smoothed away, since they are the clearest evidence for what actually made this pipeline trustworthy.</p>

    <h3>Failure 1 &mdash; Janusian&rsquo;s soft self-check got talked past</h3>
    <p>All three of the first round of Janusian generations labeled a disguised compromise (&ldquo;beneficial in context A, detrimental in context B&rdquo;) as a genuine paradox &mdash; exactly the failure mode the prompt&rsquo;s own instructions described, just relabeled as success by the model itself. A mechanical &ldquo;same-instance test&rdquo; was added to the prompt (can the claimed paradox be rephrased as two <em>different</em> instances, rather than one instance holding both truths at once?) and the same three domains were regenerated: measurable improvement, 2 of 3 clearly passed.</p>

    <h3>Failure 2 &mdash; homospatial&rsquo;s fusion criterion needed code, not just prompt text</h3>
    <p>The first two homospatial generations were bisociation wearing a coined name &mdash; entities like &ldquo;Crowd Play&rdquo; and &ldquo;Narrative Lattice&rdquo; that were, on inspection, ordinary metaphors (&ldquo;mirrors,&rdquo; &ldquo;akin to,&rdquo; &ldquo;much like&rdquo;) rather than genuine fusions. A written prompt rule banning comparison language was tried first &mdash; it did not hold; the very next generation still used the banned words directly. This was escalated to <strong>code-level enforcement</strong>: after generation, the pipeline now mechanically scans the fused-entity section for comparison words, and if any are found, sends one corrective re-prompt quoting the exact violation back to the model. If the retry still fails, the output is kept but an explicit warning is appended to the file itself, rather than silently presenting a failed fusion as a clean one. Run at scale against 7 homospatial pairs: all 7 eventually passed (5 needed the corrective retry), and the one case where the retry still left a residual violation was flagged transparently in its own output file rather than hidden.</p>
    <div class="callout">
      <span class="callout-label">The general lesson</span>
      A soft, written self-check gets talked past by the model that&rsquo;s supposed to be checking itself. A mechanical, code-level check on the actual output text does not. This is the same finding, one level up, that motivated adversarial refutation in the first place: self-report is not verification.
    </div>

    <h3>Failure 3 &mdash; a real resource constraint, and its actual fix</h3>
    <p>An early session&rsquo;s web-search budget was exhausted (200 of 200 calls used) after only 5 of a planned 15 verification queries. Rather than fabricate the remaining verdicts or drop them silently, they were recorded with an explicit <code>PENDING_VERIFICATION</code> status, held out of scoring with a clear, visible reason. A later dedicated session, spending its own budget on nothing else, resolved all 10: 22 COLLISION and 10 ADJACENT_ACTIVE totals both grew, and one new NO_SIGNAL case went through the same adversarial refutation as every prior one and was REFUTED 0-of-3.</p>
    <p>That closed the immediate backlog, but not the underlying cause: verification still required a live, human-invoked session spending its own search budget by hand, and the same shortage could recur at any batch size a single session&rsquo;s budget couldn&rsquo;t cover. The durable fix &mdash; a standalone script that runs verification unattended &mdash; has since been built: <code>verify_hypothesis.py</code> runs real web search and the same four-bucket classification with no live session and no shared budget, closing this gap structurally rather than by dedicating another session to it. It was proven, not just built: run for the first time in production against a fresh 18-hypothesis batch, it processed all 18 cleanly &mdash; including correctly catching the FACT_CHECK_FAIL below &mdash; with zero manual filename overrides needed downstream, because output filenames are now derived directly from the hypothesis slug (see <a href="#limitations">Section 11</a>).</p>

    <h3>Failure 4 &mdash; the same-instance test let the same failure through three times in one batch (still open)</h3>
    <p>Failure 1&rsquo;s fix &mdash; the mechanical same-instance test added to the Janusian prompt &mdash; was believed closed after the original three-domain regeneration showed 2 of 3 clearly passing. The newest batch says otherwise: of 6 new Janusian hypotheses, 3 (cognitive AI preprocessing, knowledge systems, and urban-planning zoning) turned out, once put through adversarial refutation, to be the exact same disguised compromise Failure 1 was supposed to have fixed &mdash; each one&rsquo;s own §4C paradox claim used language like &ldquo;in <em>some</em> contexts&hellip; in <em>others</em>,&rdquo; and each one&rsquo;s own §7 self-critique went on to concede outright that proposition and inversion &ldquo;apply to different types of models/datasets/areas&rdquo; rather than holding as one true, same-instance contradiction. The test that is supposed to catch exactly this pattern did not catch it in half of this batch&rsquo;s Janusian output.</p>
    <p>A second, smaller instance of the same class of problem: one homospatial hypothesis (Linguistics &oplus; Fluid Dynamics, &ldquo;Phonetic Turbulence&rdquo;) passed its code-level comparison-word scan &mdash; the fix from the earlier homospatial fusion-criterion failure &mdash; on the first attempt, yet its own §2 (the Superimposition) reads, verbatim, &ldquo;<em>akin to</em> laminar flow,&rdquo; &ldquo;<em>reminiscent of</em> turbulence,&rdquo; and &ldquo;<em>similar to</em> how turbulent eddies&rdquo; &mdash; three uses of exactly the banned comparison language the scan exists to catch. The adversarial refutation pass caught it; the code-level scan that should have caught it first did not. The likely cause, not yet fixed: the scan appears to check only §3 (the Emergent Third Thing), not §2 (the Superimposition itself), leaving the section where comparison language is arguably most likely to appear unchecked.</p>
    <div class="callout warn">
      <span class="callout-label">Open, not closed</span>
      Both of these are the same shape as Failure 1 and Failure 2&rsquo;s original findings: a check believed fixed after a small sample turned out to still be beatable at a slightly larger scale. Neither is patched yet as of this report &mdash; disclosed here as open, working engineering debt, not retroactively smoothed into a success story.
    </div>

    <h3>A genuine catch, reported as a positive result too</h3>
    <p>Not every finding from this pass was a failure. The unattended verification script correctly classified one new Janusian hypothesis (Physical Mechanical Spring Systems) as <strong>FACT_CHECK_FAIL</strong> &mdash; its central claim required a spring to be simultaneously elastically-recovering and permanently deformed, which real search results directly contradict (elastic and plastic deformation are established as mutually exclusive states in spring design literature). This is exactly the outcome Phase 2 is supposed to produce when a hypothesis&rsquo;s underlying domain facts, not just its cross-domain claim, are wrong &mdash; caught automatically, with no human in the loop.</p>
  </section>

  <section id="limitations">
    <h2><span class="num">11</span>Limitations</h2>
    <ul>
      <li><strong>Resolved:</strong> the standalone-verification gap described in Section 10&rsquo;s Failure 3 no longer exists. <code>verify_hypothesis.py</code> runs Phase 2 unattended &mdash; real web search plus classification, no live session or shared search budget required &mdash; and has now been run in real production against a full 18-hypothesis batch, not just smoke-tested. All 58 hypotheses in the current pool carry a canonical verdict; none are pending.</li>
      <li><strong>Resolved, with an uncomfortable answer:</strong> the control test this section previously said hadn&rsquo;t been run has now been run. The rank-1 hypothesis in the entire pool &mdash; already independently verified ADJACENT_ACTIVE with real citable evidence &mdash; was put through the same three-lens adversarial refutation as every NO_SIGNAL case and was refuted 0-of-3. Read alongside the 0-of-14 real refutation record, the honest interpretation is <em>not</em> simply &ldquo;the lenses are miscalibrated&rdquo; &mdash; all three lenses independently converged on a specific, checkable finding: the real-world connection Phase 2 had found for that hypothesis used &ldquo;trust&rdquo; in a different sense than the hypothesis itself claimed, a homonym rather than a structural match. That is a specific, falsifiable-in-principle failure mode (hypotheses that name a genuinely fertile pairing but whose functor doesn&rsquo;t actually reach it), not proof the lenses reject everything regardless of quality. Still genuinely open: whether a hypothesis with a tighter, non-equivocal functor would survive &mdash; this control reused a real hypothesis rather than hand-constructing a deliberately airtight one, which is itself a limitation of the test (see `refutations/control-test-calibration.md`).</li>
      <li><strong>New, and still fully open:</strong> the same-instance test (Section 10, Failure 1) and the homospatial comparison-word scan (Failure 2) both let real violations through in this batch &mdash; 3 of 6 new Janusian hypotheses and 1 of 6 new homospatial hypotheses respectively. Both are documented in Section 10&rsquo;s Failure 4 as open engineering debt, not yet patched.</li>
      <li><strong>The domain pool is still far from exhausted.</strong> 170 combined domains yield ~14,365 possible bisociation/homospatial pairs; 58 hypotheses have been explored across all three mechanisms combined &mdash; roughly 0.4% of the possible ground. The remainder is a standing resource for future runs, not implied complete.</li>
      <li><strong>Phase 3 has produced zero real drafts.</strong> No hypothesis to date has reached ADJACENT_ACTIVE-and-durable with a real researcher identified to contact &mdash; the mechanism exists but hasn&rsquo;t been exercised for real yet.</li>
      <li><strong>Verification and refutation remain a check on plausibility, not a substitute for an experiment.</strong> Nothing in this pipeline runs a real test of any hypothesis against the physical or social world &mdash; it only checks whether a hypothesis is novel, coherent, and worth someone&rsquo;s time to actually go test. That check is the entire value proposition described in Section 3; it is not, and was never meant to be, the experiment itself.</li>
    </ul>
  </section>

  <section id="conclusion">
    <h2><span class="num">12</span>Conclusion</h2>
    <p>The four-way verification layer answers two different questions at once, depending on how you read it: whether one specific hypothesis is novel (COLLISION says no), and whether the underlying generative mechanism reliably finds real, legitimate cross-domain territory at all (COLLISION, read this second way, says yes &mdash; 23 of 58 hypotheses collided with genuine, citable prior art, which is evidence the engine is not hallucinating connections, even in the cases where a specific hypothesis turns out to be unoriginal). Nineteen hypotheses currently sit in genuinely fertile, unclaimed territory. Fourteen more looked plausible on generation and did not survive independent adversarial scrutiny &mdash; caught, not hidden &mdash; and neither did the strongest hypothesis in the whole pool, when we deliberately pointed the same scrutiny at it as a control. That last result is the most important sentence in this report to sit with honestly: it is easier to build a system that finds connections than to build one that can be trusted when it says a connection is real.</p>
    <p>The project&rsquo;s working thesis, stated plainly by its principal at the outset: <em>&ldquo;the mere fact that we&rsquo;re getting successful bisociations means we have the beginnings of a university.&rdquo;</em> This report has tried to test that claim honestly rather than assume it &mdash; not by counting every generated hypothesis as a discovery, but by building the same four-way classifier used elsewhere in this pipeline and applying it to results that turn out to be wrong just as rigorously as to the ones that don&rsquo;t. Section 3&rsquo;s numbers are the reason any of this is worth doing at all: PhD researchers spend years, and the field as a whole spends tens of billions of dollars annually, finding out by hand which hypotheses don&rsquo;t hold up. A machine that can run the same collision Darwin stumbled into once, on purpose, thousands of times &mdash; and then honestly tell you, in minutes, which of those collisions are worth a real person&rsquo;s year &mdash; does not replace the scientist. It replaces the coin flip.</p>
  </section>

  </article>

  <footer class="colophon">
    Exponent Labs LLC &middot; scientific-intuition-engine/umpf_pipeline &middot; Generated 2026-08-29 from verification-log.jsonl (58 entries) &middot; Full data: <a href="__LEADERBOARD_URL__" target="_blank" rel="noopener">Leaderboard Experience</a>
  </footer>
</div>
'''

html = html.replace("__PIPELINE_IMG__", pipeline_img)
html = html.replace("__CLASSIFIER_IMG__", classifier_img)
html = html.replace("__VERDICT_IMG__", verdict_img)
html = html.replace("__LEADERBOARD_URL__", LEADERBOARD_URL)

with open("whitepaper.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote whitepaper.html ({len(html)/1024:.1f} KB)")
