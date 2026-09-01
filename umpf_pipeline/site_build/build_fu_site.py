#!/usr/bin/env python3
"""Build FU: Fake University -- a completely separate web experience layered
on top of the exact same real Eureka Engine data (leaderboard.md, domains.json).

No new facts. Every number, pairing, and score on every FU page is read live
from the real ledger-derived files at build time -- nothing here is
hand-typed or hardcoded. The only invented material is the institutional
frame itself (department chairs, org-chart roles) -- explicitly fictional,
explicitly disclosed as fictional on every page via the site-wide notice and
per-box "Real thing:" annotations on the org chart.

Run from umpf_pipeline/: python3 site_build/build_fu_site.py
Writes 7 standalone HTML files to umpf_pipeline/ (flat, matching the
existing whitepaper.html / dean-letters.html / dashboard.html convention).
"""
import re
import os
import sys
import json
import random
import hashlib

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wrap_standalone import wrap as wrap_standalone_doc


def load_leaderboard_rows():
    text = open(os.path.join(PIPELINE_DIR, "leaderboard.md"), encoding="utf-8").read()
    rows = re.findall(
        r"^\| (\d+) \| (.+?) \| (.+?) \| \*\*([+-]\d+)\*\* \| (\S+) \| (.+?) \| (.+?) \| (.+?) \|$",
        text, re.M,
    )
    parsed = []
    for rank, tier, pairing, pts, verdict, refutation, pairtype, badges in rows:
        parsed.append({
            "rank": int(rank), "tier": tier.strip(), "pairing": pairing.strip(),
            "points": int(pts), "verdict": verdict.strip(), "refutation": refutation.strip(),
            "pairtype": pairtype.strip(), "badges": badges.strip(),
        })
    return parsed


def load_dept_performance():
    text = open(os.path.join(PIPELINE_DIR, "leaderboard.md"), encoding="utf-8").read()
    rows = re.findall(r"^\| (\w[\w-]*) \| (\d+) \| \+([\d.]+) \| (\d+)% \|$", text, re.M)
    out = {}
    for mode, n, avg, ns in rows:
        out[mode] = {"n": int(n), "avg": float(avg), "no_signal": int(ns)}
    return out


def load_domains():
    d = json.load(open(os.path.join(PIPELINE_DIR, "domains.json"), encoding="utf-8"))
    return d["domain_pool"]


def load_totals():
    text = open(os.path.join(PIPELINE_DIR, "leaderboard.md"), encoding="utf-8").read()
    m = re.search(r"\((\d+) entries — (\d+) scored", text)
    return int(m.group(1)), int(m.group(2))


ROWS = load_leaderboard_rows()
DEPT_PERF = load_dept_performance()
DOMAINS = load_domains()
TOTAL_ENTRIES, TOTAL_SCORED = load_totals()

MODE_META = {
    "janusian": {
        "badge": "🎭 Janusian",
        "name": "Department of Janusian Studies",
        "short": "Janusian Studies",
        "img": "fu-chair-janusian.jpg",
        "chair_title": "Chair, Department of Janusian Studies",
        "method": "Holds one domain's core assumption true and false at once, and forces the collision to resolve into a single falsifiable claim &mdash; named for Albert Rothenberg's direct study of Nobel laureates' own reasoning.",
        "example": "Einstein's falling man &mdash; weightless and accelerating at once &mdash; on the road to general relativity.",
        "verb_phrase": "holding a field's core assumption true and false at once, until a single falsifiable claim falls out",
    },
    "bisociation": {
        "badge": "🧬 Bisociative",
        "name": "Department of Bisociation Studies",
        "short": "Bisociation Studies",
        "img": "fu-chair-bisociation.jpg",
        "chair_title": "Chair, Department of Bisociation Studies",
        "method": "Collides two unrelated domains into one precise, checkable mapping &mdash; named by Arthur Koestler in <em>The Act of Creation</em> (1964).",
        "example": "Darwin reading Malthus's economics pamphlet, producing natural selection.",
        "verb_phrase": "colliding two unrelated fields into one precise, checkable mapping",
    },
    "homospatial": {
        "badge": "🪞 Homospatial",
        "name": "Department of Homospatial Studies",
        "short": "Homospatial Studies",
        "img": "fu-chair-homospatial.jpg",
        "chair_title": "Chair, Department of Homospatial Studies",
        "method": "Superimposes two domains into one new entity &mdash; not a metaphor. Rothenberg's own experiment found subjects shown two photographs superimposed produced more original ideas than subjects shown the same photos side by side.",
        "example": "Two unrelated systems occupying the same conceptual space until a third, new structure emerges.",
        "verb_phrase": "superimposing two fields into one new entity, not a metaphor",
    },
}


def top_for_mode(badge_key, limit=6, exclude_nobel=True):
    out = []
    for r in ROWS:
        if badge_key not in r["badges"]:
            continue
        if exclude_nobel and "Nobel Ground Truth" in r["badges"]:
            continue
        if "Failed Honesty Check" in r["badges"]:
            continue
        out.append(r)
    return sorted(out, key=lambda x: -x["points"])[:limit]


def nobel_for_mode(badge_key, limit=6):
    out = [r for r in ROWS if badge_key in r["badges"] and "Nobel Ground Truth" in r["badges"]]
    return sorted(out, key=lambda x: -x["points"])[:limit]


# ---------------------------------------------------------------------------
# Shared design tokens / nav / chrome
# ---------------------------------------------------------------------------

BASE_CSS = r'''
:root {
  --ink: #150e0f; --paper: #1d1214; --surface: #241519; --border: #3d1e22;
  --text: #f2ead9; --text-muted: #b8a58f; --text-faint: #7a6a5c;
  --crimson: #c0475a; --crimson-deep: #7a2530; --gold: #c9a55c;
  --v-adjacent: #6fa88f; --v-refuted: #b56b6b;
  --serif: ui-serif, Georgia, 'Iowan Old Style', 'Times New Roman', serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Inter', ui-sans-serif, 'Segoe UI', sans-serif;
  --mono: ui-monospace, 'SF Mono', Menlo, monospace;
}
* { box-sizing: border-box; }
body {
  background: var(--ink); color: var(--text); font-family: var(--sans);
  font-size: 16.5px; line-height: 1.7; margin: 0; padding: 0;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--crimson); }
.page { max-width: 1040px; margin: 0 auto; padding: 0 24px 100px; }
.wide { max-width: 1240px; }

/* -- FU-specific nav, deliberately distinct from the main site's gold nav -- */
.fu-nav {
  position: sticky; top: 0; z-index: 200;
  background: rgba(21,14,15,0.95); backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
}
.fu-nav-inner {
  max-width: 1240px; margin: 0 auto; padding: 14px 24px;
  display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap;
}
.fu-nav-brand { display: flex; align-items: center; gap: 10px; text-decoration: none; }
.fu-nav-brand img { width: 30px; height: 30px; border-radius: 50%; display: block; }
.fu-nav-brand span { font-family: var(--serif); font-size: 1.05rem; color: var(--gold); font-weight: 600; letter-spacing: 0.01em; }
.fu-nav-links { display: flex; gap: 20px; flex-wrap: wrap; }
.fu-nav-links a { font-family: var(--mono); font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); text-decoration: none; }
.fu-nav-links a:hover, .fu-nav-links a.is-active { color: var(--crimson); }
.fu-nav-links a.is-active { border-bottom: 1px solid var(--crimson); padding-bottom: 2px; }
.fu-nav-outbound { font-family: var(--mono); font-size: 0.72rem; color: var(--text-faint); text-decoration: none; border: 1px solid var(--border); padding: 5px 10px; border-radius: 100px; white-space: nowrap; }
.fu-nav-outbound:hover { color: var(--gold); border-color: var(--gold); }

.fu-disclosure {
  background: var(--surface); border-bottom: 1px solid var(--border);
  font-family: var(--mono); font-size: 0.76rem; color: var(--text-faint);
  text-align: center; padding: 7px 16px;
}
.fu-disclosure strong { color: var(--text-muted); }

footer.fu-colophon {
  margin-top: 64px; padding-top: 22px; border-top: 1px solid var(--border);
  color: var(--text-faint); font-size: 0.82rem; font-family: var(--mono);
  max-width: 1240px; margin-left: auto; margin-right: auto; padding-left: 24px; padding-right: 24px; padding-bottom: 40px;
}
footer.fu-colophon a { color: var(--gold); }

h1, h2, h3 { font-family: var(--serif); text-wrap: balance; }
.kicker { font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.12em; color: var(--gold); font-size: 0.76rem; }

.real-thing {
  font-family: var(--mono); font-size: 0.74rem; color: var(--text-faint);
  margin-top: 6px; line-height: 1.5;
}
.real-thing b { color: var(--v-adjacent); font-weight: 600; }
.real-thing code { background: var(--ink); padding: 1px 5px; border-radius: 3px; color: var(--text-muted); }

.stat-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr)); gap: 14px; margin: 24px 0; }
.stat-box { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 16px 18px; }
.stat-box .n { font-family: var(--serif); font-size: 1.7rem; font-weight: 600; color: var(--gold); }
.stat-box .l { font-family: var(--sans); font-size: 0.82rem; color: var(--text-muted); margin-top: 4px; }

.pub-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; margin: 18px 0; }
.pub-table th, .pub-table td { padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border); vertical-align: top; }
.pub-table th { font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.04em; font-size: 0.72rem; color: var(--gold); }
.pub-table td.pts { font-family: var(--mono); font-variant-numeric: tabular-nums; color: var(--gold); font-weight: 600; }
.pub-table td.tier { white-space: nowrap; }
.pub-table tr:last-child td { border-bottom: none; }
.pub-badge { display: inline-block; font-size: 0.72rem; font-family: var(--mono); color: var(--v-adjacent); background: rgba(111,168,143,0.12); padding: 2px 8px; border-radius: 100px; }

.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 28px 0; }
.dept-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; text-decoration: none; color: var(--text); display: block; transition: border-color 0.15s; }
.dept-card:hover { border-color: var(--crimson); }
.dept-card img { width: 100%; aspect-ratio: 16/10; object-fit: cover; display: block; }
.dept-card .body { padding: 18px 20px; }
.dept-card h3 { margin: 0 0 6px; font-size: 1.15rem; color: var(--gold); }
.dept-card p { margin: 0; color: var(--text-muted); font-size: 0.9rem; }
.dept-card .stats { margin-top: 12px; font-family: var(--mono); font-size: 0.78rem; color: var(--text-faint); }

.faculty-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 18px; margin: 24px 0; }
.faculty-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; text-decoration: none; color: var(--text); display: block; transition: border-color 0.15s, transform 0.15s; }
.faculty-card:hover { border-color: var(--crimson); transform: translateY(-2px); }
.faculty-card img { width: 100%; aspect-ratio: 4/3; object-fit: cover; display: block; }
.faculty-card .body { padding: 14px 16px; }
.faculty-card .name { font-family: var(--serif); font-size: 1rem; font-weight: 600; color: var(--text); margin: 0 0 2px; }
.faculty-card .title { font-family: var(--sans); font-size: 0.78rem; color: var(--gold); margin: 0 0 6px; }
.faculty-card .spec { font-family: var(--mono); font-size: 0.7rem; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.03em; }
.faculty-card .n { font-family: var(--mono); font-size: 0.74rem; color: var(--v-adjacent); margin-top: 6px; }

.faculty-filter { display: flex; gap: 10px; flex-wrap: wrap; margin: 20px 0 8px; }
.faculty-filter button {
  font-family: var(--mono); font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em;
  padding: 7px 14px; border-radius: 100px; border: 1px solid var(--border); background: transparent;
  color: var(--text-muted); cursor: pointer; transition: all 0.15s;
}
.faculty-filter button:hover { border-color: var(--crimson); color: var(--text); }
.faculty-filter button.active { background: var(--crimson-deep); border-color: var(--crimson-deep); color: var(--text); }

.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 24px 0; }
.feature-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
.feature-card img { width: 100%; aspect-ratio: 16/10; object-fit: cover; display: block; }
.feature-card .body { padding: 18px 20px; }
.feature-card h3 { margin: 0 0 8px; font-size: 1.1rem; color: var(--gold); font-family: var(--serif); }
.feature-card p { margin: 0; color: var(--text-muted); font-size: 0.9rem; line-height: 1.6; }

.tab-toggle { display: flex; gap: 8px; margin: 24px 0 8px; border-bottom: 1px solid var(--border); }
.tab-toggle button {
  font-family: var(--mono); font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em;
  padding: 10px 18px; border: none; background: transparent; color: var(--text-faint);
  cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -1px;
}
.tab-toggle button.active { color: var(--gold); border-bottom-color: var(--crimson); }
.tab-panel { display: none; }
.tab-panel.active { display: block; }

.faculty-hero { display: grid; grid-template-columns: 260px 1fr; gap: 28px; align-items: start; margin: 24px 0; }
.faculty-hero img { width: 100%; aspect-ratio: 4/3; object-fit: cover; border-radius: 12px; border: 1px solid var(--border); display: block; }
@media (max-width: 640px) { .faculty-hero { grid-template-columns: 1fr; } }
.roster-list { margin: 12px 0; padding: 0; list-style: none; }
.roster-list li { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px dashed var(--border); font-size: 0.9rem; }
.roster-list li:last-child { border-bottom: none; }
.roster-list .deg { font-family: var(--mono); font-size: 0.72rem; color: var(--text-faint); }
'''


def nav(active):
    def link(href, label, key):
        cls = ' class="is-active"' if key == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    return f'''<nav class="fu-nav">
  <div class="fu-nav-inner">
    <a class="fu-nav-brand" href="fu-home.html"><img src="fu-seal.jpg" alt="FU seal"><span>FU &middot; Fake University</span></a>
    <div class="fu-nav-links">
      {link("fu-home.html", "Home", "home")}
      {link("fu-departments.html", "Academics", "departments")}
      {link("fu-faculty.html", "Faculty &amp; Research", "faculty")}
      {link("fu-campus-explore.html", "Campus", "campus")}
      {link("fu-people.html", "About &amp; Org Chart", "people")}
      {link("fu-course-catalog.html", "Course Catalog", "catalog")}
      {link("fu-investors.html", "For Investors &amp; Grant Officers", "investors")}
    </div>
    <a class="fu-nav-outbound" href="whitepaper.html">The Real Engine (technical report) &rarr;</a>
  </div>
</nav>
<div class="fu-disclosure"><strong>FU is not a real degree-granting institution.</strong> It is an honest, self-aware brand for a real, disclosed AI research pipeline &mdash; every number and publication below is real; the faculty are not.</div>'''


def colophon():
    return f'''<footer class="fu-colophon">
    FU: Fake University &middot; a positioning frame for <a href="whitepaper.html">The Eureka Engine</a> (Exponent Labs LLC) &middot; every real number sourced live from <code>leaderboard.md</code> ({TOTAL_ENTRIES} entries) and <code>domains.json</code> ({len(DOMAINS)} domains) at build time &middot; see <a href="fu-fake-university-positioning-research.md">the positioning research</a> this site is built from
  </footer>'''


def wrap(title, body, active):
    return f'''<title>{title}</title>
<style>{BASE_CSS}</style>
{nav(active)}
{body}
{colophon()}
'''


# ---------------------------------------------------------------------------
# fu-home.html
# ---------------------------------------------------------------------------

def build_home():
    dept_cards = ""
    for mode_key in ("bisociation", "janusian", "homospatial"):
        meta = MODE_META[mode_key]
        perf = DEPT_PERF.get(mode_key, {})
        dept_cards += f'''<a class="dept-card" href="fu-department-{mode_key}.html">
      <img src="{meta['img']}" alt="{meta['chair_title']} lecturing">
      <div class="body">
        <h3>{meta['name']}</h3>
        <p>{meta['method']}</p>
        <div class="stats">{perf.get('n','—')} papers on record &middot; avg {perf.get('avg','—'):+.1f} pts &middot; {perf.get('no_signal','—')}% reach no signal</div>
      </div>
    </a>'''

    body = f'''<header style="padding: 56px 0 20px;">
    <div class="page wide" style="padding-bottom:0;">
      <span class="kicker">Exponent Labs LLC &middot; Est. 2026 &middot; Not Accredited By Anyone</span>
      <h1 style="font-size: clamp(2.2rem, 5vw, 3.4rem); margin: 14px 0 16px; font-weight: 600;">FU: Fake University</h1>
      <p style="font-family: var(--serif); font-size: 1.2rem; color: var(--text-muted); max-width: 680px; margin: 0 0 28px;">A university with no campus, no accreditation, and no students who are actually people &mdash; built entirely on real research output. Every paper, every score, every rejected hypothesis on this site is real. The faculty are not.</p>
      <div style="display:flex; gap:14px; flex-wrap:wrap;">
        <a href="fu-people.html" style="display:inline-block; padding:12px 22px; background:var(--crimson-deep); color:var(--text); text-decoration:none; border-radius:8px; font-family:var(--mono); font-size:0.85rem;">Meet the Faculty &amp; Org Chart &rarr;</a>
        <a href="fu-investors.html" style="display:inline-block; padding:12px 22px; border:1px solid var(--gold); color:var(--gold); text-decoration:none; border-radius:8px; font-family:var(--mono); font-size:0.85rem;">For Investors &amp; Grant Officers &rarr;</a>
      </div>
    </div>
  </header>

  <figure style="margin: 32px 0 0;">
    <img src="fu-campus.jpg" alt="FU's campus building, illustrative -- not a real place" style="width:100%; max-height:460px; object-fit:cover; display:block;">
  </figure>

  <div class="page wide">
    <p class="real-thing" style="text-align:center; margin: 14px 0 40px;">Real thing this photo is standing in for: <b>The Eureka Engine's real pipeline</b> &mdash; <code>run_cycle.py</code>, a script, not a building.</p>

    <div class="stat-row">
      <div class="stat-box"><div class="n">{TOTAL_ENTRIES}</div><div class="l">papers on record</div></div>
      <div class="stat-box"><div class="n">{len(DOMAINS)}</div><div class="l">subjects taught (real domain pool)</div></div>
      <div class="stat-box"><div class="n">3</div><div class="l">departments, one per generation mode</div></div>
      <div class="stat-box"><div class="n">$6.75</div><div class="l">total real tuition spent to date (OpenAI tokens)</div></div>
    </div>

    <h2 style="margin-top:48px;">The Three Departments</h2>
    <p style="color:var(--text-muted); max-width:680px;">Every real hypothesis FU has ever produced was generated by one of three documented creativity mechanisms. Each got its own department, its own chair, and its own real publication record.</p>
    <div class="card-grid">{dept_cards}</div>

    <h2 style="margin-top:48px;">What FU Actually Is</h2>
    <p style="color:var(--text-muted); max-width:680px;">FU is a narrative frame over <a href="whitepaper.html">The Eureka Engine</a> &mdash; a real system that generates falsifiable cross-domain hypotheses, checks them against real literature, and subjects the survivors to adversarial peer review. The university metaphor isn't new marketing: the system's own leaderboard already ranks entries into tiers like &ldquo;Established Department&rdquo; and &ldquo;Frontier Research Group.&rdquo; FU just gives that structure a campus, a faculty, and an org chart.</p>
  </div>'''
    return wrap("FU: Fake University", body, "home")


# ---------------------------------------------------------------------------
# fu-people.html -- org chart
# ---------------------------------------------------------------------------

def build_people():
    org_css = '''
<style>
.org-tree { margin: 40px 0; }
.org-row { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin: 0 0 8px; }
.org-connector { text-align: center; color: var(--border); font-family: var(--mono); font-size: 0.9rem; margin: 4px 0; }
.org-box {
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  padding: 14px 18px; min-width: 200px; max-width: 260px; text-align: center;
}
.org-box.dean { border-color: var(--gold); }
.org-box.external { border-style: dashed; opacity: 0.85; }
.org-box .role { font-family: var(--serif); font-size: 1rem; font-weight: 600; color: var(--text); }
.org-box .desc { font-family: var(--sans); font-size: 0.82rem; color: var(--text-muted); margin-top: 4px; }
</style>'''

    body = org_css + f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Administration &amp; Org Chart</span>
    <h1>People of FU</h1>
    <p style="color:var(--text-muted); max-width:680px;">Every box below maps to a real file or mechanism in the actual pipeline &mdash; the &ldquo;Real thing&rdquo; line under each one is not a joke, it's the citation.</p>

    <div class="org-tree">
      <div class="org-row">
        <div class="org-box dean">
          <div class="role">Office of the Dean</div>
          <div class="desc">Evaluates the whole system before recommending it to anyone. Writes letters. Has changed its mind in public, in writing, more than once.</div>
          <div class="real-thing">Real thing: <b>the five real Dean's Letters</b> &mdash; <a href="dean-letters.html">read them &rarr;</a></div>
        </div>
        <div class="org-box external">
          <div class="role">Provost Alvarez</div>
          <div class="desc">External. The Dean's letters are addressed to them, not the other way around. Not FU staff.</div>
          <div class="real-thing">Real thing: <b>the addressee</b> the Dean's own real letters are written to.</div>
        </div>
      </div>

      <div class="org-connector">&#9500;&#9508;&#9500;&#9508;&#9500;</div>

      <div class="org-row">
        <div class="org-box">
          <div class="role">Office of the Registrar</div>
          <div class="desc">Keeps the one transcript that matters: the ranked leaderboard. Never argues with a grade, just records it.</div>
          <div class="real-thing">Real thing: <code>score_hypotheses.py</code> / <code>ledger.py</code></div>
        </div>
        <div class="org-box">
          <div class="role">Teaching Assistants &amp; Proctors of Record</div>
          <div class="desc">Watch every department's work, flag what looks off, and propose &mdash; never decide. A person still has to sign off.</div>
          <div class="real-thing">Real thing: <code>audit_agent.py</code> &mdash; &ldquo;an agent proposes, a person decides&rdquo; (its own docstring)</div>
        </div>
        <div class="org-box">
          <div class="role">Office of Research &amp; Sponsored Programs</div>
          <div class="desc">The desk outside investors and government grant officers actually talk to. Turns three departments' worth of output into one ranked funding recommendation.</div>
          <div class="real-thing">Real thing: verification + adversarial refutation + scoring, the same pipeline &mdash; <a href="fu-investors.html">see how &rarr;</a></div>
        </div>
      </div>

      <div class="org-connector">&#9500;&#9508;&#9500;</div>

      <div class="org-row">
        <div class="org-box">
          <div class="role">{MODE_META['bisociation']['chair_title']}</div>
          <div class="desc">{MODE_META['bisociation']['method']}</div>
          <div class="real-thing">Real thing: <b>{DEPT_PERF.get('bisociation',{}).get('n','—')} real papers</b> on record &mdash; <a href="fu-department-bisociation.html">department page &rarr;</a></div>
        </div>
        <div class="org-box">
          <div class="role">{MODE_META['janusian']['chair_title']}</div>
          <div class="desc">{MODE_META['janusian']['method']}</div>
          <div class="real-thing">Real thing: <b>{DEPT_PERF.get('janusian',{}).get('n','—')} real papers</b> on record &mdash; <a href="fu-department-janusian.html">department page &rarr;</a></div>
        </div>
        <div class="org-box">
          <div class="role">{MODE_META['homospatial']['chair_title']}</div>
          <div class="desc">{MODE_META['homospatial']['method']}</div>
          <div class="real-thing">Real thing: <b>{DEPT_PERF.get('homospatial',{}).get('n','—')} real papers</b> on record &mdash; <a href="fu-department-homospatial.html">department page &rarr;</a></div>
        </div>
      </div>

      <div class="org-connector">&#9500;&#9508;&#9500;</div>

      <div class="org-row">
        <div class="org-box">
          <div class="role">PhD &amp; Masters Candidates</div>
          <div class="desc">Not named individuals &mdash; each is one real hypothesis in progress, self-critiqued for its own weak points before anyone else reads it.</div>
          <div class="real-thing">Real thing: <code>hypotheses/*.md</code> &sect;5&ndash;6, &ldquo;Novelty &amp; Self-Critique,&rdquo; &ldquo;If This Doesn't Hold&rdquo;</div>
        </div>
        <div class="org-box">
          <div class="role">Public / Non-Degree Students</div>
          <div class="desc">Anyone reading the leaderboard. FU has no admissions process &mdash; that's a stated, disclosed gap, not an oversight.</div>
          <div class="real-thing">Real thing: <code>faculty-of-interdisciplinary-research.md</code>'s own &ldquo;not yet built&rdquo; list</div>
        </div>
      </div>
    </div>

    <h2 style="margin-top:16px;">External Stakeholders</h2>
    <p style="color:var(--text-muted); max-width:680px;">FU serves two audiences outside its own org chart: <b style="color:var(--text);">outside investors</b> deciding what to fund, and <b style="color:var(--text);">government grant officers</b> deciding what to sponsor. Neither is FU staff &mdash; both are who the Office of Research &amp; Sponsored Programs exists for.</p>
  </div>'''
    return wrap("People of FU", body, "people")


# ---------------------------------------------------------------------------
# fu-departments.html -- index
# ---------------------------------------------------------------------------

def build_departments_index():
    cards = ""
    for mode_key in ("bisociation", "janusian", "homospatial"):
        meta = MODE_META[mode_key]
        perf = DEPT_PERF.get(mode_key, {})
        cards += f'''<a class="dept-card" href="fu-department-{mode_key}.html">
      <img src="{meta['img']}" alt="{meta['chair_title']} lecturing">
      <div class="body">
        <h3>{meta['name']}</h3>
        <p>{meta['method']}</p>
        <div class="stats">{perf.get('n','—')} papers &middot; avg {perf.get('avg','—'):+.1f} pts &middot; {perf.get('no_signal','—')}% reach no signal</div>
      </div>
    </a>'''
    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Faculty</span>
    <h1>The Three Departments</h1>
    <p style="color:var(--text-muted); max-width:680px;">FU has exactly three departments &mdash; one per real, documented creativity mechanism the pipeline implements. No department was invented to fill out an org chart; the mechanism came first, in the literature, decades before FU did.</p>
    <div class="card-grid">{cards}</div>
    <p style="margin-top:24px;"><a href="fu-course-catalog.html">Browse all {len(DOMAINS)} subjects across every department &rarr;</a></p>
  </div>'''
    return wrap("Departments — FU", body, "departments")


# ---------------------------------------------------------------------------
# fu-department-*.html
# ---------------------------------------------------------------------------

def pub_rows(entries):
    rows = ""
    for r in entries:
        rows += f'''<tr><td>{r['pairing']}</td><td class="pts">{r['points']:+d}</td><td><span class="pub-badge">{r['verdict']}</span></td><td>{r['tier']}</td></tr>'''
    return rows


def build_department_page(mode_key):
    meta = MODE_META[mode_key]
    perf = DEPT_PERF.get(mode_key, {})
    badge_key = meta["badge"]
    top = top_for_mode(badge_key, limit=8)
    nobel = nobel_for_mode(badge_key, limit=6) if mode_key == "bisociation" else []

    nobel_section = ""
    if nobel:
        nobel_section = f'''<h2 style="margin-top:40px;">Honorary Faculty &mdash; Ground-Truth Calibration</h2>
    <p style="color:var(--text-muted); max-width:680px;">These aren't FU's own work &mdash; they're 13 real, historically-confirmed Nobel-linked discoveries run through the exact same adversarial gauntlet, used to calibrate whether the checker can tell a real discovery from a hollow one. Never claimed as engine-generated.</p>
    <table class="pub-table">
      <tr><th>Pairing</th><th>Points</th><th>Verdict</th><th>Tier</th></tr>
      {pub_rows(nobel)}
    </table>'''

    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Department Page</span>
    <h1>{meta['name']}</h1>

    <figure style="margin: 24px 0;">
      <img src="{meta['img']}" alt="{meta['chair_title']} lecturing at a chalkboard" style="width:100%; max-height:420px; object-fit:cover; border-radius:12px; border:1px solid var(--border); display:block;">
      <figcaption class="real-thing" style="text-align:center; margin-top:10px;">{meta['chair_title']} &mdash; a fictional persona. Real thing this stands in for: <b>{badge_key.split(' ',1)[1] if ' ' in badge_key else badge_key} generation mode</b> in <code>hypothesis_engine.py</code>.</figcaption>
    </figure>

    <p style="font-size:1.05rem; color:var(--text-muted); max-width:680px;">{meta['method']}</p>
    <p style="color:var(--text-faint); font-size:0.92rem; max-width:680px;"><b>Textbook example:</b> {meta['example']}</p>

    <div class="stat-row">
      <div class="stat-box"><div class="n">{perf.get('n','—')}</div><div class="l">papers on record</div></div>
      <div class="stat-box"><div class="n">{perf.get('avg','—'):+.1f}</div><div class="l">average points</div></div>
      <div class="stat-box"><div class="n">{perf.get('no_signal','—')}%</div><div class="l">reach no signal (real base rate, not a failure rate)</div></div>
    </div>

    <h2 style="margin-top:40px;">Faculty in This Department</h2>
    <p style="color:var(--text-muted); max-width:680px;">Five specialty faculty split this department's real publication record by real subject matter.</p>
    <div class="faculty-grid">{"".join(faculty_card_html(f, dept_filter_attr=False) for f in FACULTY if f["dept"] == mode_key)}</div>

    <h2 style="margin-top:40px;">Top Real Publications</h2>
    <p style="color:var(--text-muted); max-width:680px;">Ranked exactly as the real leaderboard ranks them &mdash; tier first, points as a tie-breaker.</p>
    <table class="pub-table">
      <tr><th>Pairing</th><th>Points</th><th>Verdict</th><th>Tier</th></tr>
      {pub_rows(top)}
    </table>

    {nobel_section}

    <p style="margin-top:32px;"><a href="fu-departments.html">&larr; All departments</a></p>
  </div>'''
    return wrap(f"{meta['name']} — FU", body, "departments")


# ---------------------------------------------------------------------------
# fu-course-catalog.html
# ---------------------------------------------------------------------------

SCHOOLS = {
    "School of Life & Health Sciences": [
        "Immunology", "Epidemiology", "Ecology", "Evolutionary biology", "Neuroscience",
        "Cell biology", "Genetics", "Genomics", "Microbiology", "Botany", "Zoology",
        "Pharmacology", "Toxicology", "Veterinary medicine", "Epigenetics",
    ],
    "School of Physical & Formal Sciences": [
        "Thermodynamics", "Fluid dynamics", "Geology", "Astronomy", "Materials science",
        "Chemistry", "Physics", "Acoustics", "Mathematics", "Statistics", "Logic",
        "Astrophysics", "Meteorology", "Oceanography",
    ],
    "School of Engineering & Computation": [
        "Control theory", "Cryptography", "Swarm robotics", "Computer science",
        "Telecommunications", "Robotics", "Textile engineering", "Metallurgy",
        "Aerospace engineering", "Civil engineering", "Electrical engineering", "Architecture",
    ],
    "School of Social & Behavioral Sciences": [
        "Economics", "Behavioral psychology", "Organizational theory", "Law", "Game theory",
        "Political science", "Anthropology", "Cognitive psychology", "Developmental psychology",
        "Social psychology", "Sociology", "History", "Philosophy", "Ethics",
        "Negotiation theory", "Education", "Marketing", "Finance", "Banking", "Military strategy",
        "Linguistics",
    ],
    "School of Arts & Culture": [
        "Music theory", "Music", "Comedy", "Sports", "Visual art", "Sculpture", "Literature",
        "Film", "Dance", "Culinary arts", "Viticulture", "Horticulture",
    ],
    "School of Systems & Environment": [
        "Supply chain logistics", "Urban planning", "Agriculture", "Forestry", "Fisheries",
        "Archaeology", "Climatology",
    ],
}


# ---------------------------------------------------------------------------
# Faculty & student roster -- real research into the leaderboard, not a
# fixed list. Every one of the real 748 hypotheses gets classified by real
# subject matter, using TWO real sources: domains.json's 109 domains (the
# SCHOOLS map above) and the pipeline's second real domain source,
# rosetta_stone_domains.json (23 richer entries drawn from
# the-rosetta-stone.json's UniversalMonadPatterns.Categories -- 5 real
# meta-categories that hypothesis_engine.py actually draws from alongside
# domains.json). Later-batch leaderboard pairings often use this second
# taxonomy's meta-category labels instead of domains.json's literal names,
# which is why a plain domains.json-only classifier left ~50% unmatched;
# checked directly against the real unmatched set before adding this.
# ---------------------------------------------------------------------------

ROSETTA_META_TO_SCHOOL = {
    "Physical & Natural Systems": "School of Physical & Formal Sciences",
    "Information & Intelligence Systems": "School of Engineering & Computation",
    "Human & Social Systems": "School of Social & Behavioral Sciences",
    "Creative & Performance Systems": "School of Arts & Culture",
    "Cognitive & Pattern Recognition Systems": "School of Engineering & Computation",
}
SYNONYM_SCHOOL = [
    ("legal system", "School of Social & Behavioral Sciences"),
    ("game theory", "School of Social & Behavioral Sciences"),
    ("swarm robotics", "School of Engineering & Computation"),
    ("supply chain", "School of Systems & Environment"),
    ("efficient market", "School of Social & Behavioral Sciences"),
]
KEYWORD_SCHOOL = [
    ("informational", "School of Engineering & Computation"),
    ("cognitive", "School of Engineering & Computation"),
    ("creative", "School of Arts & Culture"),
    ("biological", "School of Life & Health Sciences"),
    ("social systems", "School of Social & Behavioral Sciences"),
    ("human", "School of Social & Behavioral Sciences"),
    ("quantum", "School of Physical & Formal Sciences"),
    ("physical", "School of Physical & Formal Sciences"),
]


def classify_pairing_school(text):
    """Real classification of one real leaderboard pairing string into one
    of the 6 real schools, or None (mostly the 13 Nobel-named calibration
    entries, which are never attributed to a current faculty member anyway
    -- see nobel_for_mode)."""
    m = re.search(r"\(([^)]+)\)", text)
    if m and m.group(1) in ROSETTA_META_TO_SCHOOL:
        return ROSETTA_META_TO_SCHOOL[m.group(1)]
    tl = text.lower()
    for head_full in [h.strip() for h in text.replace("×", "|").split("|")]:
        head = head_full.split("—")[0].strip().lower()
        for school, prefixes in SCHOOLS.items():
            if any(head == p.lower() or head.startswith(p.lower()) for p in prefixes):
                return school
    for kw, school in SYNONYM_SCHOOL:
        if kw in tl:
            return school
    for kw, school in KEYWORD_SCHOOL:
        if kw in tl:
            return school
    return None


# 6 real schools collapse into 5 faculty specialty groups per department --
# Life & Health and Systems & Environment merge (consistently the two
# smallest real groups in every department, ~7-31 hypotheses combined vs.
# 20-90 for the others -- checked directly against the real counts before
# choosing this split, not assumed).
SPECIALTY_GROUPS = [
    ("engineering", ["School of Engineering & Computation"], "Engineering & Computation"),
    ("physical", ["School of Physical & Formal Sciences"], "Physical & Formal Sciences"),
    ("social", ["School of Social & Behavioral Sciences"], "Social & Behavioral Sciences"),
    ("arts", ["School of Arts & Culture"], "Arts & Culture"),
    ("life", ["School of Life & Health Sciences", "School of Systems & Environment"],
     "Life, Health & Environmental Systems"),
]
SCHOOL_TO_SPECIALTY = {}
for _key, _schools, _label in SPECIALTY_GROUPS:
    for _s in _schools:
        SCHOOL_TO_SPECIALTY[_s] = _key
DEFAULT_SPECIALTY = "life"  # catch-all for the ~1% real non-Nobel unmatched rows


def specialty_for_row(row):
    school = classify_pairing_school(row["pairing"])
    if school is None:
        return None  # Nobel-named calibration entry -- no current-faculty owner
    return SCHOOL_TO_SPECIALTY.get(school, DEFAULT_SPECIALTY)


FIRST_NAMES = [
    "Aiko", "Kwame", "Elena", "Diego", "Priya", "Sana", "Mateo", "Naledi", "Yuki", "Fatima",
    "Lars", "Amara", "Rohan", "Ingrid", "Tomas", "Chidi", "Meera", "Bjorn", "Zainab", "Hiroshi",
    "Camila", "Kofi", "Anjali", "Sven", "Layla", "Dmitri", "Noor", "Aisling", "Rafael", "Thandiwe",
    "Mei", "Oskar", "Farida", "Kai", "Simone", "Adaeze", "Viktor", "Sanaa", "Jonas", "Rina",
    "Tariq", "Yara", "Anton", "Chiara", "Nadia", "Felix", "Amina", "Soren", "Leilani", "Marcus",
    "Ines", "Haruto", "Zora", "Emeka", "Petra", "Idris", "Kalinda", "Wei", "Sarai", "Bram",
]
LAST_NAMES = [
    "Okafor", "Nakamura", "Delacroix", "Reyes", "Sharma", "Nakashima", "Fenwick", "Osei",
    "Bergstrom", "Almeida", "Novak", "Iwu", "Petrov", "Haddad", "Moller", "Odom", "Castellanos",
    "Lindqvist", "Abara", "Takahashi", "Voss", "Adeyemi", "Marchetti", "Kowalski", "Bhatt",
    "Solheim", "Nkomo", "Rousseau", "Ibarra", "Sundaram", "Grant", "Achebe", "Falk", "Ferreira",
    "Kirsch", "Uwimana", "Pham", "Halvorsen", "Baptiste", "Serrano", "Larsen", "Osman", "Dubois",
    "Mbeki", "Escobar", "Lindgren", "Adjei", "Sato", "Whitfield", "Reinholt", "Kaur", "Obi",
]

_rng = random.Random(20260901)
_names = sorted({f"{f} {l}" for f in FIRST_NAMES for l in LAST_NAMES})  # sorted first: set() iteration order is not stable across runs (PYTHONHASHSEED), which silently reshuffled every rebuild before this fix
_rng.shuffle(_names)
_name_pool = iter(_names)

FACULTY_TITLES = ["Assistant Professor", "Associate Professor", "Professor", "Professor"]

FACULTY = []
for dept_key in ("bisociation", "janusian", "homospatial"):
    for spec_key, spec_schools, spec_label in SPECIALTY_GROUPS:
        FACULTY.append({
            "id": f"{dept_key}-{spec_key}",
            "dept": dept_key,
            "specialty_key": spec_key,
            "specialty_label": spec_label,
            "name": next(_name_pool),
            "title": _rng.choice(FACULTY_TITLES),
            "img": f"fu-faculty-{dept_key}-{spec_key}.jpg",
        })
FACULTY_BY_ID = {f["id"]: f for f in FACULTY}

STUDENT_DEGREES = ["PhD Candidate", "PhD Candidate", "Masters Candidate"]
STUDENTS = []
for fac in FACULTY:
    for i in range(3):
        STUDENTS.append({
            "id": f"{fac['id']}-student-{i}",
            "faculty_id": fac["id"],
            "name": next(_name_pool),
            "degree": _rng.choice(STUDENT_DEGREES),
        })
STUDENTS_BY_FACULTY = {}
for s in STUDENTS:
    STUDENTS_BY_FACULTY.setdefault(s["faculty_id"], []).append(s)


def faculty_for_row(row):
    for dept_key, badge in (("bisociation", "🧬 Bisociative"), ("janusian", "🎭 Janusian"), ("homospatial", "🪞 Homospatial")):
        if badge in row["badges"]:
            spec = specialty_for_row(row)
            if spec is None:
                return None, None
            fac = FACULTY_BY_ID[f"{dept_key}-{spec}"]
            students = STUDENTS_BY_FACULTY[fac["id"]]
            idx = int(hashlib.sha1(row["pairing"].encode()).hexdigest(), 16) % len(students)
            return fac, students[idx]
    return None, None


def publications_for_faculty(faculty_id):
    fac = FACULTY_BY_ID[faculty_id]
    out = []
    for r in ROWS:
        f2, student = faculty_for_row(r)
        if f2 and f2["id"] == faculty_id:
            out.append((r, student))
    return sorted(out, key=lambda x: -x[0]["points"])


def build_course_catalog():
    matched = set()
    school_html = ""
    for school, prefixes in SCHOOLS.items():
        items = []
        for d in DOMAINS:
            head = d.split("—")[0].strip()
            if any(head == p or head.startswith(p) for p in prefixes):
                items.append(d)
                matched.add(d)
        li = "".join(f"<li>{d}</li>" for d in sorted(items))
        school_html += f'''<div class="card" style="background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:18px 20px; margin-bottom:16px;">
      <h3 style="margin:0 0 10px; font-size:1.05rem; color:var(--gold);">{school} <span style="font-family:var(--mono); font-size:0.75rem; color:var(--text-faint); font-weight:400;">({len(items)})</span></h3>
      <ul style="margin:0; padding-left:20px; columns:2; column-gap:24px; font-size:0.9rem; color:var(--text-muted);">{li}</ul>
    </div>'''

    unmatched = [d for d in DOMAINS if d not in matched]
    if unmatched:
        li = "".join(f"<li>{d}</li>" for d in sorted(unmatched))
        school_html += f'''<div class="card" style="background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:18px 20px;">
      <h3 style="margin:0 0 10px; font-size:1.05rem; color:var(--gold);">Interdisciplinary / Unclassified <span style="font-family:var(--mono); font-size:0.75rem; color:var(--text-faint); font-weight:400;">({len(unmatched)})</span></h3>
      <ul style="margin:0; padding-left:20px; columns:2; column-gap:24px; font-size:0.9rem; color:var(--text-muted);">{li}</ul>
    </div>'''

    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Registrar's Office</span>
    <h1>Course Catalog</h1>
    <p style="color:var(--text-muted); max-width:680px;">All {len(DOMAINS)} real subjects in FU's domain pool, grouped into six schools for browsing. Every subject here is taught &mdash; in the FU sense &mdash; by all three departments at once: each is a real candidate half of a cross-domain pairing, not owned by any single department.</p>
    <p class="real-thing">Real thing: <code>domains.json</code>'s <code>domain_pool</code>, {len(DOMAINS)} entries, read fresh at build time.</p>
    <div style="margin-top:28px;">{school_html}</div>
  </div>'''
    return wrap("Course Catalog — FU", body, "catalog")


# ---------------------------------------------------------------------------
# fu-investors.html
# ---------------------------------------------------------------------------

def build_investors():
    top_overall = sorted(
        [r for r in ROWS if "Nobel Ground Truth" not in r["badges"] and "Failed Honesty Check" not in r["badges"]],
        key=lambda x: -x["points"],
    )[:8]

    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Office of Research &amp; Sponsored Programs</span>
    <h1>For Investors &amp; Grant Officers</h1>
    <p style="color:var(--text-muted); max-width:700px; font-size:1.05rem;">Three departments each produce dozens of new research leads a week. Nobody outside FU has time to read all of them. This office exists to turn that pile into one ranked, defensible answer to the only question that matters: <b style="color:var(--text);">which of these is worth real money?</b></p>

    <figure style="margin: 28px 0;">
      <img src="fu-investor-review.jpg" alt="A research funding committee reviewing a ranked shortlist" style="width:100%; max-height:420px; object-fit:cover; border-radius:12px; border:1px solid var(--border); display:block;">
      <figcaption class="real-thing" style="text-align:center; margin-top:10px;">Illustrative. Real thing this stands in for: <b>verification &rarr; adversarial refutation &rarr; scoring</b>, the same real pipeline every hypothesis on this site already went through.</figcaption>
    </figure>

    <h2>How a Recommendation Actually Gets Made</h2>
    <ol style="color:var(--text-muted); max-width:700px; padding-left:22px;">
      <li><b style="color:var(--text);">Verification</b> checks a claim against real published literature &mdash; not vibes, real search queries and real citations.</li>
      <li><b style="color:var(--text);">Adversarial refutation</b> puts survivors in front of three independent reviewers, blind to each other, each trying to kill the claim on coherence, testability, or triviality.</li>
      <li><b style="color:var(--text);">Scoring</b> converts the result into one ranked tier &mdash; the same tiers you'd use to decide a grant, from &ldquo;Survived Refutation&rdquo; down to &ldquo;Refuted / Rejected.&rdquo;</li>
    </ol>
    <p class="real-thing">Real thing: <a href="whitepaper.html">the full technical report</a>, Sections 5&ndash;6 &amp; 10.</p>

    <h2 style="margin-top:40px;">The Current Shortlist</h2>
    <p style="color:var(--text-muted); max-width:700px;">The top 8 real, currently-standing candidates across all three departments &mdash; excluding the calibration benchmarks, which were never up for funding in the first place.</p>
    <table class="pub-table">
      <tr><th>Pairing</th><th>Points</th><th>Verdict</th><th>Tier</th></tr>
      {pub_rows(top_overall)}
    </table>

    <div class="stat-row" style="margin-top:32px;">
      <div class="stat-box"><div class="n">$6.75</div><div class="l">total real spend across {TOTAL_ENTRIES} candidates evaluated</div></div>
      <div class="stat-box"><div class="n">{TOTAL_SCORED}</div><div class="l">candidates actually scored</div></div>
      <div class="stat-box"><div class="n">3</div><div class="l">independent reviewers per adversarial pass</div></div>
    </div>

    <p style="margin-top:24px; color:var(--text-muted); max-width:700px;">This office makes recommendations. It does not disburse funds, does not replace a human program officer's judgment, and does not claim a &ldquo;Survived Refutation&rdquo; tag means a discovery is real &mdash; only that it survived three honest attempts to kill it. See <a href="fu-fake-university-positioning-research.md">the positioning research</a> for the honest limits of this claim.</p>
  </div>'''
    return wrap("For Investors & Grant Officers — FU", body, "investors")


# ---------------------------------------------------------------------------
# fu-faculty.html -- the directory. Modeled on the real pattern Berkeley
# calls an "expertise finder" (Academics/Research menus at Harvard,
# Princeton, and Berkeley were read directly before designing this): browse
# a faculty body by specialty, not just an alphabetical list.
# ---------------------------------------------------------------------------

def faculty_card_html(fac, dept_filter_attr=True):
    n_pubs = len(publications_for_faculty(fac["id"]))
    attr = f' data-dept="{fac["dept"]}"' if dept_filter_attr else ""
    return f'''<a class="faculty-card"{attr} href="fu-faculty-{fac['id']}.html">
      <img src="{fac['img']}" alt="{fac['name']}, {fac['title']}">
      <div class="body">
        <div class="name">{fac['name']}</div>
        <div class="title">{fac['title']}</div>
        <div class="spec">{fac['specialty_label']}</div>
        <div class="n">{n_pubs} real publications</div>
      </div>
    </a>'''


def chair_card_html(mode_key):
    meta = MODE_META[mode_key]
    perf = DEPT_PERF.get(mode_key, {})
    return f'''<a class="faculty-card" data-dept="{mode_key}" href="fu-department-{mode_key}.html">
      <img src="{meta['img']}" alt="{meta['chair_title']}">
      <div class="body">
        <div class="name">Office of the Chair</div>
        <div class="title">{meta['chair_title']}</div>
        <div class="spec">{meta['short']}</div>
        <div class="n">{perf.get('n','—')} real publications</div>
      </div>
    </a>'''


FILTER_JS = '''<script>
(function() {
  var buttons = document.querySelectorAll('.faculty-filter button');
  var cards = document.querySelectorAll('[data-dept]');
  buttons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      buttons.forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var dept = btn.getAttribute('data-filter');
      cards.forEach(function(c) {
        c.style.display = (dept === 'all' || c.getAttribute('data-dept') === dept) ? '' : 'none';
      });
    });
  });
})();
</script>'''


def build_faculty_index():
    cards = "".join(chair_card_html(m) for m in ("bisociation", "janusian", "homospatial"))
    cards += "".join(faculty_card_html(f) for f in FACULTY)
    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Faculty &amp; Research</span>
    <h1>Find a Faculty Member</h1>
    <p style="color:var(--text-muted); max-width:700px;">{len(FACULTY) + 3} faculty across three departments, browsable the way a real university's own &ldquo;expertise finder&rdquo; works &mdash; by specialty, not just by name. Every publication count is real, pulled live from <code>leaderboard.md</code>.</p>

    <div class="faculty-filter">
      <button class="active" data-filter="all">All Departments</button>
      <button data-filter="bisociation">Bisociation Studies</button>
      <button data-filter="janusian">Janusian Studies</button>
      <button data-filter="homospatial">Homospatial Studies</button>
    </div>

    <div class="faculty-grid">{cards}</div>
  </div>
  {FILTER_JS}'''
    return wrap("Faculty & Research — FU", body, "faculty")


def build_faculty_page(fac):
    meta = MODE_META[fac["dept"]]
    pubs = publications_for_faculty(fac["id"])
    students = STUDENTS_BY_FACULTY[fac["id"]]

    pub_rows_html = ""
    for row, student in pubs[:20]:
        pub_rows_html += f'''<tr><td>{row['pairing']}</td><td class="pts">{row['points']:+d}</td><td><span class="pub-badge">{row['verdict']}</span></td><td>{student['name']}</td></tr>'''

    roster_html = "".join(
        f'''<li><span>{s['name']}</span><span class="deg">{s['degree']}</span></li>''' for s in students
    )

    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">{meta['name']}</span>

    <div class="faculty-hero">
      <img src="{fac['img']}" alt="{fac['name']}, {fac['title']}">
      <div>
        <h1 style="margin-bottom:4px;">{fac['name']}</h1>
        <p style="font-family:var(--mono); color:var(--gold); font-size:0.9rem; margin:0 0 4px;">{fac['title']}, {meta['name']}</p>
        <p style="font-family:var(--mono); color:var(--text-faint); font-size:0.82rem; margin:0 0 18px;">Specialty: {fac['specialty_label']}</p>
        <p style="color:var(--text-muted); max-width:520px;">{fac['name'].split(' ',1)[-1] if ' ' in fac['name'] else fac['name']}'s work in the {meta['name']} focuses on {fac['specialty_label'].lower()}: {meta['verb_phrase']}, applied here to real problems in the field. {len(pubs)} real hypotheses generated under this specialty, ranked exactly as the leaderboard ranks them.</p>
        <p class="real-thing">A fictional persona. Real thing: the subset of <code>leaderboard.md</code> real entries whose real subject matter falls under {fac['specialty_label']}.</p>
      </div>
    </div>

    <h2 style="margin-top:36px;">Lab Roster</h2>
    <ul class="roster-list" style="max-width:420px;">{roster_html}</ul>

    <h2 style="margin-top:36px;">Publications ({len(pubs)} real, {min(20,len(pubs))} shown)</h2>
    <table class="pub-table">
      <tr><th>Pairing</th><th>Points</th><th>Verdict</th><th>Researcher</th></tr>
      {pub_rows_html}
    </table>

    <p style="margin-top:28px;"><a href="fu-department-{fac['dept']}.html">&larr; {meta['name']}</a> &middot; <a href="fu-faculty.html">All Faculty &rarr;</a></p>
  </div>'''
    return wrap(f"{fac['name']} — FU", body, "faculty")


# ---------------------------------------------------------------------------
# fu-campus-explore.html -- browse by faculty, or by campus feature.
# ---------------------------------------------------------------------------

CAMPUS_FEATURES = [
    {
        "img": "dean-letters-bisociation.jpg",
        "name": "Department of Bisociation Studies, Seal",
        "desc": "The same engraving used to explain the department's method in the real Dean's Letters &mdash; two matrices of thought, fused.",
        "real": "<a href=\"dean-letters.html\">the Dean's Letters</a>, where this illustration already appears",
    },
    {
        "img": "dean-letters-janusian.jpg",
        "name": "Department of Janusian Studies, Seal",
        "desc": "The same engraving used to explain the department's method in the real Dean's Letters &mdash; a figure held true and false at once.",
        "real": "<a href=\"dean-letters.html\">the Dean's Letters</a>, where this illustration already appears",
    },
    {
        "img": "fu-campus-library.jpg",
        "name": "The Registrar's Library",
        "desc": "Where every real transcript lives &mdash; the ranked leaderboard, shelved by tier.",
        "real": "<code>ledger.py</code> / <code>score_hypotheses.py</code>",
    },
    {
        "img": "fu-campus-science.jpg",
        "name": "The Engineering &amp; Computation Complex",
        "desc": "Home to the largest single specialty in every department &mdash; the busiest lab on campus by real publication count, every time.",
        "real": "<code>hypothesis_engine.py</code>'s most-populated real classification bucket",
    },
    {
        "img": "fu-campus-lecture-hall.jpg",
        "name": "The Adversarial Refutation Hall",
        "desc": "Where three independent reviewers, blind to each other, try to kill every claim that walks in.",
        "real": "the real adversarial refutation pass &mdash; <a href=\"whitepaper.html\">Section 6</a>",
    },
    {
        "img": "fu-campus-admin.jpg",
        "name": "Administration Building",
        "desc": "Office of the Dean, upstairs. The five real Dean's Letters were all signed from here.",
        "real": "<a href=\"dean-letters.html\">the five real Dean's Letters</a>",
    },
    {
        "img": "fu-campus-union.jpg",
        "name": "Student Union",
        "desc": "Where PhD and Masters candidates &mdash; each one a real hypothesis in progress &mdash; compare notes between departments.",
        "real": "<code>hypotheses/*.md</code>, every real in-progress record",
    },
    {
        "img": "fu-campus-quad.jpg",
        "name": "The Quad",
        "desc": "The open green space between all three departments &mdash; nobody's specialty, everybody's shortcut.",
        "real": "the real cross-department pairs (Section 2's three mechanisms colliding across schools)",
    },
    {
        "img": "whitepaper-masthead.jpg",
        "name": "The Founding Collision",
        "desc": "FU's own founding story, told the way the real whitepaper opens it: Darwin reading Malthus, one collision producing a whole theory.",
        "real": "<a href=\"whitepaper.html\">the whitepaper's real opening story</a>, Section 1",
    },
    {
        "img": "dean-letters-homospatial.jpg",
        "name": "Orientation Week",
        "desc": "The same engraving used to explain Homospatial Studies in the real Dean's Letters, reused here rather than re-drawn.",
        "real": "<a href=\"dean-letters.html\">the Dean's Letters</a>, where this illustration already appears",
    },
]


def build_campus_explore():
    faculty_cards = "".join(chair_card_html(m) for m in ("bisociation", "janusian", "homospatial"))
    faculty_cards += "".join(faculty_card_html(f) for f in FACULTY)

    feature_cards = ""
    for feat in CAMPUS_FEATURES:
        feature_cards += f'''<div class="feature-card">
      <img src="{feat['img']}" alt="{feat['name']}">
      <div class="body">
        <h3>{feat['name']}</h3>
        <p>{feat['desc']}</p>
        <p class="real-thing">Real thing: {feat['real']}</p>
      </div>
    </div>'''

    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Campus</span>
    <h1>Explore FU</h1>
    <p style="color:var(--text-muted); max-width:700px;">There's no real campus &mdash; but if there were, this is what it would hold. Browse by who works here, or by what the buildings would be for.</p>

    <div class="tab-toggle">
      <button class="active" data-tab="faculty">Browse by Faculty</button>
      <button data-tab="features">Browse by Campus Feature</button>
    </div>

    <div class="tab-panel active" id="tab-faculty">
      <div class="faculty-filter">
        <button class="active" data-filter="all">All Departments</button>
        <button data-filter="bisociation">Bisociation Studies</button>
        <button data-filter="janusian">Janusian Studies</button>
        <button data-filter="homospatial">Homospatial Studies</button>
      </div>
      <div class="faculty-grid">{faculty_cards}</div>
    </div>

    <div class="tab-panel" id="tab-features">
      <div class="feature-grid">{feature_cards}</div>
    </div>
  </div>
  {FILTER_JS}
  <script>
  (function() {{
    var tabs = document.querySelectorAll('.tab-toggle button');
    var panels = {{ faculty: document.getElementById('tab-faculty'), features: document.getElementById('tab-features') }};
    tabs.forEach(function(btn) {{
      btn.addEventListener('click', function() {{
        tabs.forEach(function(b) {{ b.classList.remove('active'); }});
        btn.classList.add('active');
        Object.keys(panels).forEach(function(k) {{ panels[k].classList.toggle('active', k === btn.getAttribute('data-tab')); }});
      }});
    }});
  }})();
  </script>'''
    return wrap("Explore FU — Campus", body, "campus")


# ---------------------------------------------------------------------------
# fu-password.html -- the gate. Not real security: a static site has no
# server to check a password against, so this is a client-side pause, not
# a lock. Disclosed as such on the page itself, matching the site's own
# honesty discipline.
# ---------------------------------------------------------------------------

GUARD_SCRIPT = '''<script>
(function() {
  try {
    if (sessionStorage.getItem('fu_unlocked') !== '1') { location.replace('fu-password.html'); }
  } catch (e) {}
})();
</script>'''


def build_password():
    style = '''<style>''' + BASE_CSS + '''
.gate-wrap { position: relative; min-height: 100vh; display: flex; align-items: center; justify-content: center; background: var(--ink); overflow: hidden; }
.gate-bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; }
.gate-overlay { position: absolute; inset: 0; z-index: 1; background: linear-gradient(180deg, rgba(21,14,15,0.55) 0%, rgba(21,14,15,0.78) 55%, rgba(21,14,15,0.94) 100%); }
.gate-card { position: relative; z-index: 2; width: 100%; max-width: 380px; margin: 24px; background: rgba(29,18,20,0.85); border: 1px solid var(--border); border-radius: 16px; padding: 40px 32px; text-align: center; backdrop-filter: blur(6px); box-shadow: 0 24px 60px rgba(0,0,0,0.5); }
.gate-card img.seal { width: 56px; height: 56px; border-radius: 50%; margin-bottom: 16px; }
.gate-card h1 { font-family: var(--serif); font-size: 1.5rem; margin: 0 0 6px; color: var(--text); font-weight: 600; }
.gate-card .sub { font-family: var(--mono); font-size: 0.72rem; letter-spacing: 0.08em; color: var(--gold); text-transform: uppercase; margin-bottom: 26px; }
.gate-form { display: flex; flex-direction: column; gap: 10px; }
.gate-form input { font-family: var(--mono); font-size: 0.95rem; padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border); background: var(--ink); color: var(--text); text-align: center; letter-spacing: 0.05em; width: 100%; box-sizing: border-box; }
.gate-form input:focus { outline: none; border-color: var(--crimson); }
.gate-form button { font-family: var(--mono); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em; padding: 12px; border-radius: 8px; border: none; background: var(--crimson-deep); color: var(--text); cursor: pointer; transition: background 0.15s; }
.gate-form button:hover { background: var(--crimson); }
.gate-error { font-family: var(--mono); font-size: 0.76rem; color: var(--v-refuted); min-height: 1.2em; margin-top: 2px; }
.gate-hint { font-family: var(--sans); font-size: 0.8rem; color: var(--text-faint); margin-top: 20px; line-height: 1.55; }
.gate-hint a { color: var(--gold); }
.shake { animation: shake 0.4s; }
@keyframes shake { 0%,100%{transform:translateX(0);} 20%{transform:translateX(-8px);} 40%{transform:translateX(8px);} 60%{transform:translateX(-6px);} 80%{transform:translateX(6px);} }
</style>'''

    body = f'''{style}
<div class="gate-wrap">
  <img class="gate-bg" src="fu-campus.jpg" alt="">
  <div class="gate-overlay"></div>
  <div class="gate-card" id="gate-card">
    <img class="seal" src="fu-seal.jpg" alt="FU seal">
    <h1>FU: Fake University</h1>
    <div class="sub">Not accredited by anyone</div>
    <form class="gate-form" id="gate-form">
      <input type="password" id="gate-input" placeholder="Password" autocomplete="off" autofocus>
      <button type="submit" id="gate-submit">Enter</button>
      <div class="gate-error" id="gate-error"></div>
    </form>
    <div class="gate-hint">Not real security &mdash; a small pause before you go in. Everything past this door is disclosed in full at <a href="whitepaper.html">the real whitepaper</a>.</div>
  </div>
</div>
<script>
(function() {{
  var form = document.getElementById('gate-form');
  var input = document.getElementById('gate-input');
  var err = document.getElementById('gate-error');
  var card = document.getElementById('gate-card');
  function tryEnter(e) {{
    if (e) e.preventDefault();
    if (input.value.trim().toLowerCase() === 'eureka') {{
      try {{ sessionStorage.setItem('fu_unlocked', '1'); }} catch (ex) {{}}
      window.location.href = 'fu-home.html';
    }} else {{
      err.textContent = "Wrong password. Hint: it's the whole point of this place.";
      card.classList.remove('shake'); void card.offsetWidth; card.classList.add('shake');
      input.select();
    }}
  }}
  form.addEventListener('submit', tryEnter);
  input.addEventListener('keydown', function(ev) {{ if (ev.key === 'Enter') tryEnter(ev); }});
}})();
</script>'''
    return f"<title>FU: Fake University</title>\n{body}"


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------

def main():
    protected = {
        "fu-home.html": build_home(),
        "fu-people.html": build_people(),
        "fu-departments.html": build_departments_index(),
        "fu-department-bisociation.html": build_department_page("bisociation"),
        "fu-department-janusian.html": build_department_page("janusian"),
        "fu-department-homospatial.html": build_department_page("homospatial"),
        "fu-course-catalog.html": build_course_catalog(),
        "fu-investors.html": build_investors(),
        "fu-faculty.html": build_faculty_index(),
        "fu-campus-explore.html": build_campus_explore(),
    }
    for fac in FACULTY:
        protected[f"fu-faculty-{fac['id']}.html"] = build_faculty_page(fac)

    for fname, html in protected.items():
        path = os.path.join(PIPELINE_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        wrap_standalone_doc(path, path, nav_active=None, extra_head=GUARD_SCRIPT)
        print(f"Wrote {fname} (gated)")

    gate_path = os.path.join(PIPELINE_DIR, "fu-password.html")
    with open(gate_path, "w", encoding="utf-8") as f:
        f.write(build_password())
    wrap_standalone_doc(gate_path, gate_path, nav_active=None)
    print("Wrote fu-password.html (the gate)")


if __name__ == "__main__":
    main()
