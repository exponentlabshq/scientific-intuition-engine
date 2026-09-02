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


def load_experience_data():
    """The real, full-fidelity per-hypothesis data the original interactive
    leaderboard experience used (assemble_experience_data.py's output) --
    real hypothesis/verification/refutation markdown, real active-research
    matches, real score breakdown. Reused verbatim, not reassembled."""
    path = os.path.join(PIPELINE_DIR, "experience_data.json")
    with open(path, encoding="utf-8") as f:
        entries = json.load(f)
    by_pairing = {}
    by_domain_head = {}
    for e in entries:
        pairing = " × ".join(e["domains"]) if e.get("domains") else e["key"]
        norm = pairing.strip().lower()
        by_pairing.setdefault(norm, e)  # first entry wins on rare collision
        for d in (e.get("domains") or []):
            head = d.split("—")[0].strip().lower()
            by_domain_head.setdefault(head, []).append(e)
    for head in by_domain_head:
        by_domain_head[head].sort(key=lambda e: -(e.get("points") or 0))
    return entries, by_pairing, by_domain_head


ROWS = load_leaderboard_rows()
DEPT_PERF = load_dept_performance()
DOMAINS = load_domains()
TOTAL_ENTRIES, TOTAL_SCORED = load_totals()
EXP, EXP_BY_PAIRING, EXP_BY_DOMAIN_HEAD = load_experience_data()

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

.hero-section { position: relative; min-height: 68vh; display: flex; align-items: center; overflow: hidden; }
.hero-bg-video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; }
.hero-overlay { position: absolute; inset: 0; z-index: 1; background: linear-gradient(180deg, rgba(21,14,15,0.5) 0%, rgba(21,14,15,0.7) 60%, var(--ink) 100%); }
.hero-content { position: relative; z-index: 2; padding: 40px 24px; }
.hero-unmute {
  position: absolute; z-index: 3; bottom: 20px; right: 20px;
  background: rgba(21,14,15,0.7); border: 1px solid var(--border); color: var(--text);
  font-family: var(--mono); font-size: 0.76rem; padding: 8px 14px; border-radius: 100px; cursor: pointer;
}
@media (max-width: 640px) { .hero-section { min-height: 78vh; } }
.wide { max-width: 1240px; }

/* -- FU-specific nav: unobtrusive by default, every title still a real
   link. Low-contrast translucent bar over the page rather than a solid
   toolbar; gains a touch of solidity on hover/focus so a reader can
   still tell it's there without it competing with hero imagery. -- */
.fu-nav {
  position: sticky; top: 0; z-index: 200;
  background: rgba(21,14,15,0.35); backdrop-filter: blur(6px);
  border-bottom: 1px solid rgba(58,30,34,0.4);
  transition: background 0.2s ease, border-color 0.2s ease;
}
.fu-nav:hover, .fu-nav:focus-within {
  background: rgba(21,14,15,0.85); border-bottom-color: var(--border);
}
.fu-nav-inner {
  max-width: 1240px; margin: 0 auto; padding: 9px 24px;
  display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap;
}
.fu-nav-brand { display: flex; align-items: center; gap: 8px; text-decoration: none; opacity: 0.92; }
.fu-nav-brand img { width: 22px; height: 22px; border-radius: 50%; display: block; }
.fu-nav-brand span { font-family: var(--serif); font-size: 0.92rem; color: var(--gold); font-weight: 600; letter-spacing: 0.01em; }
.fu-nav-links { display: flex; gap: 18px; flex-wrap: wrap; }
.fu-nav-links a { font-family: var(--sans); font-size: 0.8rem; color: var(--text-faint); text-decoration: none; transition: color 0.15s; }
.fu-nav-links a:hover, .fu-nav-links a.is-active { color: var(--gold); }
.fu-nav-links a.is-active { border-bottom: 1px solid var(--gold); padding-bottom: 2px; }
.fu-nav-outbound { font-family: var(--sans); font-size: 0.78rem; color: var(--text-faint); text-decoration: none; white-space: nowrap; opacity: 0.8; }
.fu-nav-outbound:hover { color: var(--gold); opacity: 1; }

.fu-disclosure {
  background: transparent; border-bottom: 1px solid rgba(58,30,34,0.3);
  font-family: var(--mono); font-size: 0.7rem; color: var(--text-faint);
  text-align: center; padding: 5px 16px; opacity: 0.85;
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
.dept-card .hover-media { aspect-ratio: 16/10; }
.dept-card .body { padding: 18px 20px; }
.dept-card h3 { margin: 0 0 6px; font-size: 1.15rem; color: var(--gold); }
.dept-card p { margin: 0; color: var(--text-muted); font-size: 0.9rem; }
.dept-card .stats { margin-top: 12px; font-family: var(--mono); font-size: 0.78rem; color: var(--text-faint); }

/* Hover-to-video media: an img and a video occupy the exact same box
   (position:absolute, inset:0, identical object-fit) so swapping which
   one is visible never changes the element's footprint. The video's
   src is lazy-assigned from data-src on first hover (never fetched on
   page load -- a grid can hold 18 of these) and released back to just
   the poster frame on mouseleave. */
.hover-media { position: relative; width: 100%; overflow: hidden; }
.hover-media img, .hover-media video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.hover-media img { transition: opacity 0.2s ease; }
.hover-media video { opacity: 0; }
.hover-media.is-playing img { opacity: 0; }
.hover-media.is-playing video { opacity: 1; }

.faculty-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 18px; margin: 24px 0; }
.faculty-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; text-decoration: none; color: var(--text); display: block; transition: border-color 0.15s, transform 0.15s; }
.faculty-card:hover { border-color: var(--crimson); transform: translateY(-2px); }
.faculty-card .hover-media { aspect-ratio: 4/3; }
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

.tour-stop { margin: 0 0 64px; }
.tour-stop .tour-imgs { display: grid; grid-template-columns: 1fr; gap: 10px; }
.tour-stop .tour-imgs.pair { grid-template-columns: 1fr 1fr; }
@media (max-width: 720px) { .tour-stop .tour-imgs.pair { grid-template-columns: 1fr; } }
.tour-stop img { width: 100%; aspect-ratio: 16/9; object-fit: cover; border-radius: 14px; border: 1px solid var(--border); display: block; }
.tour-stop .tour-caption { max-width: 680px; margin-top: 18px; }
.tour-stop .tour-caption h2 { margin: 0 0 8px; }
.tour-stop .tour-caption p { color: var(--text-muted); margin: 0 0 6px; }
.tour-video-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 24px 0; }
.tour-video-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }
.tour-video-card video { width: 100%; aspect-ratio: 16/9; display: block; background: #000; }
.tour-video-card .body { padding: 16px 18px; }
.tour-video-card h3 { margin: 0 0 6px; font-size: 1rem; color: var(--gold); font-family: var(--serif); }
.tour-video-card p { margin: 0; color: var(--text-muted); font-size: 0.86rem; line-height: 1.55; }
.seal-row { display: flex; gap: 16px; flex-wrap: wrap; }
.seal-row figure { flex: 1; min-width: 200px; margin: 0; text-align: center; }
.seal-row img { width: 100%; aspect-ratio: 4/3; object-fit: cover; border-radius: 10px; border: 1px solid var(--border); }
.seal-row figcaption { font-family: var(--mono); font-size: 0.76rem; color: var(--text-faint); margin-top: 8px; }
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
      {link("fu-leaderboard.html", "Leaderboard", "leaderboard")}
      {link("fu-investors.html", "For Investors &amp; Grant Officers", "investors")}
    </div>
  </div>
</nav>'''


def colophon():
    return f'''<footer class="fu-colophon">
    FU: Fake University &middot; a positioning frame for <a href="whitepaper.html">The Eureka Engine</a> (Exponent Labs LLC) &middot; every real number sourced live from <code>leaderboard.md</code> ({TOTAL_ENTRIES} entries) and <code>domains.json</code> ({len(DOMAINS)} domains) at build time
  </footer>'''


def wrap(title, body, active):
    return f'''<title>{title}</title>
<style>{BASE_CSS}
{ROW_CSS}
{CHARTER_CSS}</style>
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
      {hover_media_html(meta['img'], f"fu-lecture-chair-{mode_key}.mp4", f"{meta['chair_title']} lecturing")}
      <div class="body">
        <h3>{meta['name']}</h3>
        <p>{meta['method']}</p>
        <div class="stats">{perf.get('n','—')} papers on record &middot; avg {perf.get('avg','—'):+.1f} pts &middot; {perf.get('no_signal','—')}% reach no signal</div>
      </div>
    </a>'''

    body = f'''<header class="hero-section">
    <video id="hero-drone" class="hero-bg-video" src="fu-drone-hero-v2.mp4" poster="fu-campus.jpg" autoplay muted loop playsinline></video>
    <div class="hero-overlay"></div>
    <button id="hero-unmute" class="hero-unmute">&#128264; Sound on</button>
    <div class="page wide hero-content">
      <span class="kicker">Exponent Labs LLC &middot; Est. 2026 &middot; Not Accredited By Anyone</span>
      <h1 style="font-size: clamp(2.2rem, 5vw, 3.4rem); margin: 14px 0 16px; font-weight: 600; color: #fff;">FU: Fake University</h1>
      <p style="font-family: var(--serif); font-size: 1.2rem; color: rgba(255,255,255,0.82); max-width: 680px; margin: 0 0 28px;">A university with no campus, no accreditation, and no students who are actually people &mdash; built entirely on real research output. Every paper, every score, every rejected hypothesis on this site is real. The faculty are not.</p>
      <div style="display:flex; gap:14px; flex-wrap:wrap;">
        <a href="fu-people.html" style="display:inline-block; padding:12px 22px; background:var(--crimson-deep); color:var(--text); text-decoration:none; border-radius:8px; font-family:var(--mono); font-size:0.85rem;">Meet the Faculty &amp; Org Chart &rarr;</a>
        <a href="fu-investors.html" style="display:inline-block; padding:12px 22px; border:1px solid var(--gold); color:var(--gold); text-decoration:none; border-radius:8px; font-family:var(--mono); font-size:0.85rem;">For Investors &amp; Grant Officers &rarr;</a>
      </div>
    </div>
  </header>
  <script>
  (function() {{
    var v = document.getElementById('hero-drone');
    var btn = document.getElementById('hero-unmute');
    if (!v || !btn) return;
    btn.addEventListener('click', function() {{
      v.muted = !v.muted;
      btn.innerHTML = v.muted ? '&#128264; Sound on' : '&#128266; Sound off';
    }});
  }})();
  </script>

  <div class="page wide" style="padding-top:40px;">
    <div class="stat-row">
      <div class="stat-box"><div class="n">{TOTAL_ENTRIES}</div><div class="l">papers on record</div></div>
      <div class="stat-box"><div class="n">{len(DOMAINS)}</div><div class="l">subjects taught (real domain pool)</div></div>
      <div class="stat-box"><div class="n">3</div><div class="l">departments, one per generation mode</div></div>
      <div class="stat-box"><div class="n">$36.61</div><div class="l">total real tuition spent to date (OpenAI tokens) &mdash; <a href="#cost" style="color:inherit;">receipt below &darr;</a></div></div>
    </div>

    <h2 id="story-of-fu" style="margin-top:56px;">The Story of FU</h2>
    <p style="color:var(--text-muted); max-width:680px;">A short documentary: the Dean on why this exists, the real mechanism behind it, three department chairs on real findings, and three students on what a real adversarial review actually felt like. Hover any professor's photo anywhere on this site and it plays the same way &mdash; this is just the cut of it.</p>
    <video controls poster="fu-dean.jpg" preload="none" playsinline style="width:100%; border-radius:14px; border:1px solid var(--border); display:block; margin-top:16px;">
      <source src="fu-documentary-v10.mp4" type="video/mp4">
    </video>
    <p class="real-thing" style="margin-top:10px;">The Dean and the three student testimonials are fictional deliveries of real content &mdash; every number and finding they cite is real, sourced the same way every other page on this site is. Not a real recruiting video; disclosed as such in its own closing frame.</p>

    <h2 id="charter" style="margin-top:56px;">The Charter</h2>
    <p style="color:var(--text-muted); max-width:680px;">FU's own founding document &mdash; twelve Articles, the same real science and the same real citations as the actual Eureka Engine technical report, recast as a constitution. {TOTAL_SCORED} hypotheses carry a canonical verdict as of this build; the Charter explains, from nothing, why that record is worth keeping honestly, and where it has failed along the way.</p>
    <a href="whitepaper.html" style="display:inline-block; margin-top:16px; padding:12px 22px; border:1px solid var(--gold); color:var(--gold); text-decoration:none; border-radius:8px; font-family:var(--mono); font-size:0.85rem;">Read the Charter &rarr;</a>

    <h2 style="margin-top:56px;">The Three Departments</h2>
    <p style="color:var(--text-muted); max-width:680px;">Every real hypothesis FU has ever produced was generated by one of three documented creativity mechanisms. Each got its own department, its own chair, and its own real publication record.</p>
    <div class="card-grid">{dept_cards}</div>

    <h2 id="campus" style="margin-top:56px;">Campus</h2>
    <p style="color:var(--text-muted); max-width:680px;">There's no real campus &mdash; but if there were, this is what walking across it would look like. <a href="fu-campus-explore.html">Take the full tour on its own page &rarr;</a></p>
    {campus_tour_stops()}

    <h2 id="cost" style="margin-top:56px;">The Real Cost</h2>
    <p style="color:var(--text-muted); max-width:680px;">Not an estimate, not a mockup &mdash; the actual OpenAI usage dashboard for the account behind every hypothesis on this site and the real Eureka Engine underneath it. $36.61 in, {TOTAL_ENTRIES} hypotheses out.</p>
    <img src="fu-real-cost.jpg" alt="OpenAI usage dashboard: $36.61 total spend, Exponent Labs LLC, 37,874,804 total tokens, 14,558 total requests" style="width:100%; max-width:900px; border-radius:14px; border:1px solid var(--border); display:block; margin-top:16px;">
    <p class="real-thing" style="margin-top:10px;">Real thing: Exponent Labs LLC's own OpenAI billing dashboard, screenshotted directly.</p>
  </div>
  {HOVER_VIDEO_JS}'''
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
          <div class="real-thing">Real thing: the Dean's own correspondence and findings &mdash; <a href="fu-home.html#story-of-fu">watch her explain them &rarr;</a></div>
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
      {hover_media_html(meta['img'], f"fu-lecture-chair-{mode_key}.mp4", f"{meta['chair_title']} lecturing")}
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
  </div>
  {HOVER_VIDEO_JS}'''
    return wrap("Departments — FU", body, "departments")


# ---------------------------------------------------------------------------
# fu-department-*.html
# ---------------------------------------------------------------------------

def pub_rows(entries):
    rows = ""
    for r in entries:
        rows += f'''<tr><td>{r['pairing']}</td><td class="pts">{r['points']:+d}</td><td><span class="pub-badge">{r['verdict']}</span></td><td>{r['tier']}</td></tr>'''
    return rows


def expandable_pub_rows(rows_list):
    """Same real click-expandable row used on faculty pages and the course
    catalog (full real hypothesis/verification/refutation content), applied
    to a list of leaderboard.md row-dicts -- used wherever a page still had
    the older plain <table> (department pages, investors)."""
    out = ""
    for i, row in enumerate(rows_list):
        exp = EXP_BY_PAIRING.get(row["pairing"].strip().lower())
        if exp:
            out += exp_row_html(exp, rank=i + 1)
        else:
            pts_class = "pos" if row["points"] > 0 else ("neg" if row["points"] < 0 else "zero")
            out += f'''<div class="row"><div class="row-head" style="cursor:default;">
              <span class="rank">{i+1}</span><span class="pairing">{row['pairing']}</span>
              <span class="row-badge" style="color:var(--gold);border-color:var(--gold);">{row['verdict']}</span>
              <span class="r-points {pts_class}">{row['points']:+d}</span>
            </div></div>'''
    return out


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
    {expandable_pub_rows(nobel)}'''

    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Department Page</span>
    <h1>{meta['name']}</h1>

    <figure style="margin: 24px 0;">
      <video src="fu-lecture-chair-{mode_key}.mp4" poster="{meta['img']}" controls preload="metadata" playsinline style="width:100%; max-height:420px; object-fit:cover; border-radius:12px; border:1px solid var(--border); display:block;"></video>
      <figcaption class="real-thing" style="text-align:center; margin-top:10px;">{meta['chair_title']} &mdash; a fictional persona, delivering a real finding. Real thing this stands in for: <b>{badge_key.split(' ',1)[1] if ' ' in badge_key else badge_key} generation mode</b> in <code>hypothesis_engine.py</code>.</figcaption>
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
    <p style="color:var(--text-muted); max-width:680px;">Ranked exactly as the real leaderboard ranks them &mdash; tier first, points as a tie-breaker. Click any row for the full real record.</p>
    {expandable_pub_rows(top)}

    {nobel_section}

    <p style="margin-top:32px;"><a href="fu-departments.html">&larr; All departments</a></p>
  </div>
  {HOVER_VIDEO_JS}
  {ROW_TOGGLE_JS}'''
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


# ---------------------------------------------------------------------------
# Click-expandable publication rows -- porting the real interactive
# leaderboard experience (leaderboard-experience.html: .row/.row-head/
# .row-body, click to expand) rather than reinventing it. Ported server-side
# in Python instead of the original's client-side JSON+JS renderer: the
# content is static once built (same as every other page on this site), so
# pre-rendering the real markdown to HTML at build time means no client-side
# markdown parser or data blob is needed -- lighter pages, same interaction.
# ---------------------------------------------------------------------------

ROW_CSS = '''
.row { border: 1px solid var(--border); border-radius: 10px; margin-bottom: 8px; background: var(--surface); overflow: hidden; }
.row-head { display: flex; align-items: center; gap: 12px; padding: 13px 16px; cursor: pointer; user-select: none; }
.row-head:hover { background: var(--ink); }
.row-head .rank { font-family: var(--mono); color: var(--text-faint); font-size: 0.78rem; width: 24px; flex-shrink: 0; text-align: right; }
.row-head .pairing { flex: 1; min-width: 0; font-weight: 600; font-size: 0.9rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.row-head .researcher { font-family: var(--mono); font-size: 0.72rem; color: var(--text-faint); flex-shrink: 0; }
.row-head .r-points { font-family: var(--mono); font-variant-numeric: tabular-nums; font-weight: 600; font-size: 0.9rem; width: 46px; text-align: right; flex-shrink: 0; }
.row-head .r-points.pos { color: var(--v-adjacent); }
.row-head .r-points.neg { color: var(--v-refuted); }
.row-head .r-points.zero { color: var(--text-faint); }
.row-head .caret { color: var(--text-faint); transition: transform 0.15s ease; flex-shrink: 0; font-size: 0.7rem; }
.row.open .caret { transform: rotate(90deg); }
.row-body { display: none; padding: 4px 18px 20px; border-top: 1px solid var(--border); }
.row.open .row-body { display: block; }
.row-body h4 { font-family: var(--serif); font-size: 0.9rem; color: var(--gold); margin: 16px 0 6px; font-weight: 600; }
.row-body .domains-line { color: var(--text-muted); font-size: 0.84rem; margin-top: 12px; }
.row-badge-list { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.row-badge { font-size: 0.7rem; font-family: var(--mono); color: var(--text-muted); border: 1px solid var(--border); padding: 2px 8px; border-radius: 100px; }
.md-block { font-size: 0.86rem; color: var(--text); line-height: 1.65; }
.md-block h1, .md-block h2 { font-family: var(--serif); font-size: 0.98rem; color: var(--text); margin: 12px 0 6px; }
.md-block h1:first-child, .md-block h2:first-child { margin-top: 0; }
.md-block strong { color: var(--gold); font-weight: 600; }
.md-block ul { margin: 6px 0; padding-left: 20px; }
.md-block li { margin: 3px 0; }
.md-block p { margin: 8px 0; }
.md-block table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 0.82rem; }
.md-block th, .md-block td { border: 1px solid var(--border); padding: 6px 8px; text-align: left; vertical-align: top; }
.md-block th { background: var(--ink); font-weight: 600; }
.md-block hr { border: none; border-top: 1px solid var(--border); margin: 14px 0; }
.md-block code { font-family: var(--mono); font-size: 0.85em; background: var(--ink); padding: 1px 5px; border-radius: 4px; }
.breakdown-list { list-style: none; padding: 0; margin: 6px 0; }
.breakdown-list li { font-family: var(--mono); font-size: 0.8rem; color: var(--text-muted); padding: 3px 0; }
.active-research-block { background: var(--ink); border: 1px solid var(--gold); border-radius: 8px; padding: 12px 14px; margin: 8px 0 14px; }
.ar-note { font-size: 0.84rem; color: var(--text); margin: 0 0 8px; line-height: 1.6; }
.ar-matches { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; }
.ar-matches li { font-size: 0.84rem; }
.ar-matches a { color: var(--gold); text-decoration: none; border-bottom: 1px dotted var(--gold); font-weight: 600; }
.ar-matches a:hover { border-bottom-style: solid; }
.ar-authors { color: var(--text-muted); }
.ar-explanation { color: var(--text-faint); font-size: 0.8rem; margin-top: 3px; line-height: 1.5; }

.course-item { border: 1px solid var(--border); border-radius: 8px; margin-bottom: 6px; background: var(--ink); }
.course-head { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 9px 12px; cursor: pointer; font-size: 0.86rem; }
.course-head:hover { background: var(--surface); }
.course-head .cname { flex: 1; color: var(--text); }
.course-head .ccount { font-family: var(--mono); font-size: 0.72rem; color: var(--text-faint); flex-shrink: 0; }
.course-head .caret { color: var(--text-faint); transition: transform 0.15s; flex-shrink: 0; font-size: 0.7rem; }
.course-item.open > .course-head .caret { transform: rotate(90deg); }
.course-body { display: none; padding: 4px 12px 12px; }
.course-item.open > .course-body { display: block; }

.lb-toolbar { margin: 20px 0 4px; }
.lb-search { width: 100%; max-width: 420px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; color: var(--text); font-family: var(--sans); font-size: 0.9rem; padding: 10px 14px; }
.lb-search:focus { outline: none; border-color: var(--gold); }
.lb-filter-label { font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-faint); font-size: 0.7rem; margin: 16px 0 6px; }
.lb-count { font-family: var(--mono); font-size: 0.78rem; color: var(--text-faint); margin: 10px 0 6px; }
'''

ROW_TOGGLE_JS = '''<script>
document.querySelectorAll('.row-head').forEach(function(h) {
  h.addEventListener('click', function() { h.closest('.row').classList.toggle('open'); });
});
document.querySelectorAll('.course-head').forEach(function(h) {
  h.addEventListener('click', function() { h.closest('.course-item').classList.toggle('open'); });
});
</script>'''


def md_to_html(md):
    """Direct Python port of leaderboard-experience.html's own mdToHtml --
    same minimal, dependency-free markdown renderer, same behavior, so the
    real hypothesis/verification/refutation markdown renders identically to
    how it already rendered there."""
    if not md:
        return ""
    lines = md.split("\n")
    out = []
    in_list = False
    in_table = False
    table_rows = []

    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def inline(s):
        s = esc(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
        return s

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def flush_table():
        nonlocal in_table, table_rows
        if in_table:
            rows = [r for r in table_rows if not re.match(r"^\s*\|?\s*-{2,}", r)]
            out.append("<table>")
            for i, r in enumerate(rows):
                cells = [c.strip() for c in r.split("|")]
                if cells and cells[0] == "":
                    cells = cells[1:]
                if cells and cells[-1] == "":
                    cells = cells[:-1]
                tag = "th" if i == 0 else "td"
                out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
            out.append("</table>")
            in_table = False
            table_rows = []

    for line in lines:
        if re.match(r"^\s*\|", line):
            flush_list()
            in_table = True
            table_rows.append(line)
            continue
        elif in_table:
            flush_table()
        if re.match(r"^#{1,2}\s", line):
            flush_list()
            out.append(f"<h2>{inline(re.sub(r'^#{1,2}\\s', '', line))}</h2>")
        elif re.match(r"^#{3,6}\s", line):
            flush_list()
            out.append(f"<h1>{inline(re.sub(r'^#{3,6}\\s', '', line))}</h1>")
        elif re.match(r"^---+\s*$", line):
            flush_list()
            out.append("<hr/>")
        elif re.match(r"^\s*[-*]\s", line):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(re.sub(r'^\\s*[-*]\\s', '', line))}</li>")
        elif line.strip() == "":
            flush_list()
        else:
            flush_list()
            out.append(f"<p>{inline(line)}</p>")
    flush_list()
    flush_table()
    return "\n".join(out)


def exp_row_html(e, rank=None, researcher=None, compact=False):
    """One real, click-expandable publication row -- exact same content
    the original interactive leaderboard showed (domains, badges, score
    breakdown, real active-research matches, notes, and the full real
    hypothesis / verification / refutation markdown), pre-rendered here
    rather than parsed client-side. compact=True drops the three full
    markdown blocks (hypothesis/verification/refutation content) -- used
    on the course catalog, where one real entry can appear under multiple
    domains and full content repeated that many times, across 109 domains,
    would bloat the page by megabytes for no real benefit over the same
    entry's full page on its faculty member's own publication list."""
    pairing = " × ".join(e["domains"]) if e.get("domains") else e["key"]
    pts = e.get("points") or 0
    pts_class = "pos" if pts > 0 else ("neg" if pts < 0 else "zero")
    verdict = (e.get("verdict") or "UNSCORED").replace("_", " ")

    body = f'<div class="domains-line"><strong style="color:var(--text)">Domains:</strong> {" &times; ".join(e.get("domains") or [])}</div>'
    body += '<div class="row-badge-list">' + "".join(f'<span class="row-badge">{b}</span>' for b in (e.get("badges") or [])) + "</div>"

    if e.get("breakdown"):
        body += f'<h4>Score breakdown ({pts:+d} pts)</h4><ul class="breakdown-list">'
        body += "".join(f"<li>{re.sub('<', '&lt;', b)}</li>" for b in e["breakdown"])
        body += "</ul>"

    matches = e.get("active_research_matches") or []
    if matches:
        body += f'<h4>&#128300; Independent Research Match{"es" if len(matches) > 1 else ""}</h4><div class="active-research-block">'
        if e.get("active_research_note"):
            body += f'<p class="ar-note">{re.sub("<", "&lt;", e["active_research_note"])}</p>'
        body += '<ul class="ar-matches">'
        for m in matches:
            title = re.sub("<", "&lt;", m.get("title") or "Untitled")
            authors = re.sub("<", "&lt;", m.get("researcher_or_authors") or "")
            year = f' ({m["year"]})' if m.get("year") else ""
            url = m.get("url") or ""
            title_html = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>' if url.startswith("http") else title
            body += f"<li>{title_html}{year}" + (f' &mdash; <span class="ar-authors">{authors}</span>' if authors else "")
            if m.get("explanation"):
                body += f'<div class="ar-explanation">{re.sub("<", "&lt;", m["explanation"])}</div>'
            body += "</li>"
        body += "</ul></div>"

    if e.get("notes"):
        body += f'<h4>Notes</h4><div class="md-block">{md_to_html(e["notes"])}</div>'
    if not compact:
        if e.get("hypothesis_content"):
            body += f'<h4>The Hypothesis</h4><div class="md-block">{md_to_html(e["hypothesis_content"])}</div>'
        if e.get("verification_content"):
            body += f'<h4>Verification</h4><div class="md-block">{md_to_html(e["verification_content"])}</div>'
        if e.get("refutation_content"):
            confirmed = " (independently confirmed)" if e.get("refutation_independently_confirmed") else ""
            body += f'<h4>Adversarial Refutation{confirmed}</h4><div class="md-block">{md_to_html(e["refutation_content"])}</div>'
    elif e.get("hypothesis_filename"):
        body += f'<p class="real-thing">Full real record (hypothesis, verification, refutation): <code>{e["hypothesis_filename"]}</code></p>'

    rank_html = f'<span class="rank">{rank}</span>' if rank is not None else ""
    researcher_html = f'<span class="researcher">{researcher}</span>' if researcher else ""

    return f'''<div class="row">
      <div class="row-head">
        {rank_html}
        <span class="pairing">{pairing}</span>
        {researcher_html}
        <span class="row-badge" style="color:var(--gold);border-color:var(--gold);">{verdict}</span>
        <span class="r-points {pts_class}">{pts:+d}</span>
        <span class="caret">&#9656;</span>
      </div>
      <div class="row-body">{body}</div>
    </div>'''


COURSE_ENTRIES_SHOWN = 5


def domain_entries(domain):
    """Real hypotheses touching this real domain, via experience_data.json's
    own real per-entry domains list (head-category match) -- capped, not
    exhaustive: a subject with 20 real touches shows its top 5 by points,
    same 'top N, not all N' convention this whole site already uses on
    department and faculty pages."""
    head = domain.split("—")[0].strip().lower()
    out = EXP_BY_DOMAIN_HEAD.get(head, [])
    return out[:COURSE_ENTRIES_SHOWN]


def course_item_html(domain):
    entries = domain_entries(domain)
    if not entries:
        return f'''<li style="padding:9px 12px; color:var(--text-faint); font-size:0.86rem;">{domain} <span style="font-family:var(--mono); font-size:0.72rem;">(0 real matches)</span></li>'''
    rows = "".join(exp_row_html(e, compact=True) for e in entries)
    return f'''<div class="course-item">
      <div class="course-head">
        <span class="cname">{domain}</span>
        <span class="ccount">{len(entries)} shown</span>
        <span class="caret">&#9656;</span>
      </div>
      <div class="course-body">{rows}</div>
    </div>'''


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
        courses = "".join(course_item_html(d) for d in sorted(items))
        school_html += f'''<div class="card" style="background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:18px 20px; margin-bottom:16px;">
      <h3 style="margin:0 0 10px; font-size:1.05rem; color:var(--gold);">{school} <span style="font-family:var(--mono); font-size:0.75rem; color:var(--text-faint); font-weight:400;">({len(items)})</span></h3>
      {courses}
    </div>'''

    unmatched = [d for d in DOMAINS if d not in matched]
    if unmatched:
        courses = "".join(course_item_html(d) for d in sorted(unmatched))
        school_html += f'''<div class="card" style="background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:18px 20px;">
      <h3 style="margin:0 0 10px; font-size:1.05rem; color:var(--gold);">Interdisciplinary / Unclassified <span style="font-family:var(--mono); font-size:0.75rem; color:var(--text-faint); font-weight:400;">({len(unmatched)})</span></h3>
      {courses}
    </div>'''

    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Registrar's Office</span>
    <h1>Course Catalog</h1>
    <p style="color:var(--text-muted); max-width:680px;">All {len(DOMAINS)} real subjects in FU's domain pool, grouped into six schools for browsing. Every subject here is taught &mdash; in the FU sense &mdash; by all three departments at once: each is a real candidate half of a cross-domain pairing, not owned by any single department. Click any subject to see the real hypotheses that actually touch it.</p>
    <p class="real-thing">Real thing: <code>domains.json</code>'s <code>domain_pool</code> ({len(DOMAINS)} entries) cross-referenced against <code>experience_data.json</code>'s real per-hypothesis domain tags.</p>
    <div style="margin-top:28px;">{school_html}</div>
  </div>
  {ROW_TOGGLE_JS}'''
    return wrap("Course Catalog — FU", body, "catalog")


# ---------------------------------------------------------------------------
# whitepaper.html -- The FU Charter. Not the real Eureka Engine technical
# report (that lives in the separate eureka-engine-web repo, and that repo
# isn't deployed anywhere FU can link to) -- FU's own governing document,
# built natively here so the many "the real whitepaper" links across this
# site actually resolve. Same real science, same real citations, same real
# live numbers (pulled from ROWS/EXP/DOMAINS at build time, never hardcoded)
# as everything else on FU -- recast as a charter with Articles instead of
# a report with Sections, in FU's own institutional voice.
# ---------------------------------------------------------------------------

CHARTER_CSS = '''
.charter-masthead { padding: 48px 0 32px; border-bottom: 2px solid var(--gold); }
.charter-masthead .dek { color: var(--text-muted); font-size: 1.1rem; max-width: 660px; margin: 14px 0 18px; line-height: 1.6; }
.charter-masthead .byline { color: var(--text-faint); font-size: 0.85rem; font-family: var(--mono); }
.charter-abstract { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 24px 26px; margin: 32px 0; font-size: 0.97rem; max-width: 760px; }
.charter-toc { margin: 32px 0; padding: 20px 24px; border: 1px solid var(--border); border-radius: 10px; max-width: 760px; }
.charter-toc ol { margin: 0; padding-left: 0; list-style: none; columns: 2; column-gap: 26px; }
.charter-toc li { margin: 5px 0; font-size: 0.88rem; break-inside: avoid; }
.charter-toc a { color: var(--text); text-decoration: none; border-bottom: 1px solid transparent; }
.charter-toc a:hover { border-bottom-color: var(--gold); color: var(--gold); }
.charter-article { margin: 52px 0; max-width: 760px; }
.charter-article h2 { font-family: var(--serif); font-size: 1.5rem; font-weight: 600; margin: 0 0 16px; padding-bottom: 10px; border-bottom: 1px solid var(--border); text-wrap: balance; }
.charter-article h2 .num { color: var(--gold); font-family: var(--mono); font-size: 0.92rem; margin-right: 10px; }
.charter-article h3 { font-family: var(--serif); font-size: 1.08rem; font-weight: 600; margin: 26px 0 10px; }
.charter-article p { margin: 13px 0; line-height: 1.7; }
.charter-article blockquote { margin: 18px 0; padding: 4px 20px; border-left: 3px solid var(--gold); color: var(--text-muted); font-style: italic; font-size: 1rem; }
.charter-article strong { color: var(--gold); font-weight: 600; }
.charter-story::first-letter { font-family: var(--serif); font-size: 3.1rem; font-weight: 600; color: var(--gold); float: left; line-height: 0.85; margin: 5px 8px 0 0; }
.charter-callout { background: var(--surface); border-left: 3px solid var(--gold); border-radius: 0 8px 8px 0; padding: 15px 18px; margin: 18px 0; font-size: 0.92rem; }
.charter-callout.warn { border-left-color: var(--v-refuted); }
.charter-callout .cl-label { font-family: var(--mono); text-transform: uppercase; font-size: 0.68rem; letter-spacing: 0.08em; color: var(--gold); display: block; margin-bottom: 6px; }
.charter-callout.warn .cl-label { color: var(--v-refuted); }
figure.charter-fig { margin: 26px 0; text-align: center; max-width: 760px; }
figure.charter-fig img { max-width: 100%; border-radius: 10px; border: 1px solid var(--border); }
figure.charter-fig figcaption { color: var(--text-faint); font-size: 0.8rem; margin-top: 8px; font-family: var(--mono); }
'''


def _charter_example(pairing_name, note=""):
    """One real hypothesis, looked up live and rendered as the same
    click-expandable row used everywhere else on FU -- the mechanism this
    whole Charter's Article II-III promise: cite a specific claim, let the
    reader expand it to the real record right there in the text."""
    e = EXP_BY_PAIRING.get(pairing_name.strip().lower())
    if not e:
        return f'<p class="real-thing">(expected real example not found: {pairing_name})</p>'
    html = exp_row_html(e)
    if note:
        html = f'<p style="margin-bottom:8px;">{note}</p>' + html
    return html


def build_whitepaper():
    tier_counts = {}
    dept_counts = {}
    for r in ROWS:
        tier_counts[r["tier"]] = tier_counts.get(r["tier"], 0) + 1
        dept_counts[dept_slug_for_row(r)] = dept_counts.get(dept_slug_for_row(r), 0) + 1
    top_row = max(ROWS, key=lambda r: r["points"])

    body = f'''<div class="page" style="padding-top:0;">
  <header class="charter-masthead">
    <span class="kicker">FU: Fake University &middot; Founding Charter</span>
    <h1>The FU Charter</h1>
    <p class="dek">The governing document of Fake University &mdash; twelve Articles, real science, real citations, real numbers pulled live from the same ledger every other page on this site reads from. This is also, in its bones, verbatim in every fact and every citation, the real technical report the whole university sits on top of.</p>
    <p class="byline">Office of the Dean &middot; Fake University &middot; a positioning frame for the real Eureka Engine (Exponent Labs LLC)</p>
  </header>

  <div class="charter-abstract">
    <span class="kicker" style="display:block; margin-bottom:10px;">Preamble</span>
    <p>Most scientific breakthroughs do not come from staring harder at one field &mdash; they come from smashing two unrelated fields together (Darwin reading an economics pamphlet; Einstein imagining a falling man). FU exists to automate three specific, well-documented ways of forcing that collision &mdash; Arthur Koestler's <em>bisociation</em> and psychiatrist Albert Rothenberg's <em>Janusian</em> and <em>homospatial</em> thinking, one per department &mdash; and then, critically, to check honestly whether each resulting hypothesis is actually worth a researcher's time, the way a fact-checker or a skeptical colleague would, before anyone spends real months finding out by hand. As of this Charter's last build, <strong>{TOTAL_SCORED} hypotheses</strong> carry a canonical verdict across a <strong>{len(DOMAINS)}-domain</strong> pool: {tier_counts.get('🛡️ Survived Refutation', 0)} Survived Refutation, {tier_counts.get('🗺️ Verified, Unrefuted', 0)} Verified and Unrefuted, {tier_counts.get('🌗 Contested', 0)} Contested, and {tier_counts.get('💀 Refuted / Rejected', 0)} Refuted or Rejected &mdash; the full record, unfiltered, lives on <a href="fu-leaderboard.html">the Ledger</a>. This Charter exists to explain, from nothing, why that record is worth keeping honestly &mdash; and to show, in full, what it actually took to build a university that tells the truth about its own failures.</p>
  </div>

  <nav class="charter-toc">
    <span class="kicker" style="display:block; margin-bottom:12px;">Articles</span>
    <ol>
      <li><a href="#founding">I. The Founding Collision</a></li>
      <li><a href="#doctrines">II. The Three Doctrines</a></li>
      <li><a href="#grievance">III. Why FU Was Founded</a></li>
      <li><a href="#mechanisms">IV. The Three Departments, Formally</a></li>
      <li><a href="#curriculum">V. The Four-Phase Curriculum</a></li>
      <li><a href="#evidence">VI. Standing Rules of Evidence</a></li>
      <li><a href="#gauntlet">VII. The Gauntlet</a></li>
      <li><a href="#tenure">VIII. Tenure and the Ledger</a></li>
      <li><a href="#record">IX. The Current Record</a></li>
      <li><a href="#history">X. Founding-Era History</a></li>
      <li><a href="#limitations">XI. Limitations and Open Questions</a></li>
      <li><a href="#closing">XII. The Closing Article</a></li>
    </ol>
  </nav>

  <article>

  <section id="founding" class="charter-article">
    <h2><span class="num">I</span>The Founding Collision</h2>
    <p class="charter-story">In October 1838, Charles Darwin picked up a book that had nothing to do with finches, barnacles, or beetles. It was <em>An Essay on the Principle of Population</em>, an economics pamphlet by Thomas Malthus about the brutal arithmetic of famine &mdash; the observation that human populations grow faster than food supplies ever can, guaranteeing that most of every generation dies before it gets the chance to reproduce. Darwin was reading it, by his own account, &ldquo;for amusement.&rdquo; He wasn&rsquo;t looking for anything.</p>
    <p>He had, by then, spent two years turning over a puzzle from a five-year voyage around the world: why do closely related species on nearby islands differ in small, specific ways &mdash; a slightly different beak here, a slightly different shell there? He had the observations. He didn&rsquo;t have the mechanism. Then, reading Malthus&rsquo;s chapter on the mathematics of overcrowded cities, something clicked. If human populations are held in check by a permanent, brutal excess of births over food, then every wild population must be too. Every generation of every species is born into a competition it mostly loses. And the individuals that happen to carry some small edge survive that competition more often than their siblings, on average, over and over, for millions of generations. No one has to design anything. You get evolution by natural selection.</p>
    <p>Darwin named the collision himself, later, in his autobiography: reading Malthus is where the idea &ldquo;at once occurred to me.&rdquo; The single most consequential idea in the history of biology was not produced by staring harder at finches. It was produced by forcing two fields that had nothing to do with each other &mdash; population economics and natural history &mdash; into the same sentence.</p>
    <p>This is not a freak occurrence. Johannes Kepler spent years trying to explain planetary orbits using the geometry of musical harmony. Claude Shannon founded information theory by noticing that the on/off logic of telephone relay switches was, structurally, the same thing as the true/false logic of Boolean algebra &mdash; a discipline built decades earlier to formalize philosophical logic, with no telephones in mind at all. The pattern recurs often enough across the history of science that FU was founded to ask a genuinely strange question in earnest: <strong>what if the collision itself &mdash; not talent, not luck, not years of immersion in one field &mdash; is the actual mechanism, and it can be done on purpose?</strong></p>
    <p>A <strong>hypothesis</strong>, in the sense this Charter uses the word, is nothing more exotic than a specific, falsifiable guess about how two things are secretly connected &mdash; precise enough that it could turn out to be wrong. Darwin&rsquo;s guess was falsifiable: if population pressure didn&rsquo;t actually produce differential survival, the theory would collapse. Most guesses like this, tried by most people, go nowhere &mdash; a plausible-sounding connection that turns out, on inspection, to already be well known, or to not actually hold up, or to be too vague to ever be wrong. Finding that out is the slow, expensive part of research (Article III puts real numbers on exactly how expensive).</p>
    <p>FU is an attempt to automate both halves of what Darwin did by accident once: <strong>force the collision on purpose, over and over, across a large pool of real subjects</strong> &mdash; and then <strong>honestly check each result</strong>, the way a skeptical colleague would, before anyone spends a year of their life finding out the hard way. Every Article after this one describes exactly how, and exactly where it has failed along the way.</p>
  </section>

  <section id="doctrines" class="charter-article">
    <h2><span class="num">II</span>The Three Doctrines</h2>
    <p>Darwin&rsquo;s collision has a name. Two researchers, working decades apart, each independently studied how minds actually produce insights like his &mdash; and between them, they described three distinct mechanisms, not one. FU's three departments each hold one, faithfully, as their entire discipline.</p>

    <h3>Bisociation &mdash; two frames, collided (Department of Bisociation Studies)</h3>
    <p>Arthur Koestler was not, by training, a scientist. He was a Hungarian-British novelist and journalist who, in 1964, published a 750-page book called <em>The Act of Creation</em>, trying to find one shared mechanism underneath humor, art, and scientific discovery. His answer was a word he had to coin himself: <strong>bisociation</strong> &mdash; perceiving a situation from inside two self-consistent frames of reference at once, frames normally kept completely apart. Koestler&rsquo;s own favorite illustration was the joke: a story appears to be going one way, following one frame &mdash; and the punchline reveals it fits a second, totally different frame just as well. Darwin&rsquo;s moment with Malthus is a clean, real-world case: population economics is one matrix, natural history is a second, and neither one by itself contains natural selection. The insight lives only in the collision.</p>
    <p>The Department of Bisociation Studies does exactly this, mechanically: it takes two genuinely unrelated domains from FU's pool, forces them together, and asks for a precise, falsifiable structural mapping &mdash; not a cute metaphor (&ldquo;markets are <em>like</em> ecosystems&rdquo;), but a claim specific enough that it could turn out to be wrong. One standing member of the record:</p>
    {_charter_example("Language Linguistics × Military Strategy", "Real example, Bisociation Studies &mdash; still standing on the current Ledger:")}

    <h3>Janusian thinking &mdash; two opposites, both true at once (Department of Janusian Studies)</h3>
    <p>Albert Rothenberg is an American psychiatrist who spent decades doing something almost nobody else in creativity research has done: instead of theorizing from an armchair, he got direct access to genuinely eminent scientists and Nobel laureates and studied, from real interviews and primary documents, how they actually described their own thinking in the specific minutes before a breakthrough. From that work he named <strong>Janusian thinking</strong>, for Janus, the Roman god sculpted with two faces looking in opposite directions at once: actively conceiving two opposite or contradictory ideas as true <em>at the same time, in the same respect</em> &mdash; not &ldquo;it depends on context,&rdquo; but genuinely both, held together on purpose. Rothenberg&rsquo;s clearest example is Einstein. In 1907, years before general relativity, Einstein described what he later called &ldquo;the happiest thought of my life&rdquo;: a person falling freely off a roof feels <em>no gravity at all</em> &mdash; weightless, exactly as if floating at rest in empty space &mdash; and yet, at that exact same instant, is <em>accelerating</em> downward as hard as gravity can pull them. Ordinary thinking picks one. Einstein held both as completely, simultaneously true, and that specific act is the seed Rothenberg traces directly forward to the equivalence principle: gravity and acceleration are not just similar but literally indistinguishable, the foundation stone of general relativity, published nine years later.</p>
    <p>The Department of Janusian Studies reproduces this directly: it takes one domain&rsquo;s foundational assumption and forces the exact opposite as also, simultaneously, true &mdash; no hedging, no quiet &ldquo;sometimes A, sometimes B&rdquo; smuggled in as a paradox (Article X, Failure 1 and Failure 4, is the real story of how much enforcement that turned out to require, including a relapse). One standing member of the record:</p>
    {_charter_example("Zoology — animal migration navigation", "Real example, Janusian Studies &mdash; Survived Refutation, one of FU's strongest standing findings:")}

    <h3>Homospatial thinking &mdash; two things, superimposed into one (Department of Homospatial Studies)</h3>
    <p>Rothenberg&rsquo;s second finding, from the same research program: <strong>homospatial thinking</strong> &mdash; actively conceiving two or more distinct entities occupying the exact same space at once, forcing the mind to find or invent a genuinely new relationship between them. He ran real experiments: subjects shown two ordinary photographs physically superimposed, sharing one rectangle, produced measurably more original and vivid metaphors than subjects shown the same two photographs side by side. The superimposition itself, not talent alone, was doing creative work. A similar &mdash; though historically disputed &mdash; story is often told about the chemist August Kekulé, who claimed the ring structure of the benzene molecule came to him in a half-waking daydream of a snake biting its own tail. Historians doubt the exact details; whether or not it happened quite that way, it has exactly the shape of a homospatial insight.</p>
    <p>The Department of Homospatial Studies is built to force the real thing, not the easy substitute: instead of comparing two domains (&ldquo;X is like Y&rdquo;), it requires a fusion into one new entity belonging to neither source domain &mdash; and the pipeline mechanically scans the output and rejects any answer that&rsquo;s secretly just a metaphor wearing a made-up name (Article X, Failure 2, is the real story of how much enforcement that took). One standing member of the record:</p>
    {_charter_example("Law × Informational Database State", "Real example, Homospatial Studies &mdash; Verified and Unrefuted:")}

    <p>None of this required a machine, in principle &mdash; Darwin, Einstein, and Kekulé (real or embellished) each did it with nothing but their own mind, once, after years of immersion in their field. What FU changes is scale. A single researcher gets, at most, a handful of true collisions in an entire working lifetime, most of them arrived at by accident. FU runs these same three moves deliberately, on demand, against a real domain pool &mdash; not waiting for the accident, but forcing it, hundreds of times over, and disclosing exactly how many of those forced collisions actually held up.</p>
  </section>

  <section id="grievance" class="charter-article">
    <h2><span class="num">III</span>Why FU Was Founded</h2>
    <p>FU exists to recover time &mdash; specifically, the years a real Masters or PhD student spends finding out, the slow and expensive way, that a hypothesis doesn&rsquo;t hold up. Running the collision is the easy part; a model proposes a plausible-sounding cross-domain hypothesis in seconds. The hard, slow, expensive part of science has never been having an idea. It has always been finding out, honestly, whether the idea was actually worth having.</p>
    <p>That cost is not hypothetical. It is one of the best-documented, least-discussed facts about how research actually works:</p>
    <div class="stat-row">
      <div class="stat-box"><div class="n">7.3 yrs</div><div class="l">average time to complete a PhD in the United States &mdash; Council of Graduate Schools</div></div>
      <div class="stat-box"><div class="n">40&ndash;60%</div><div class="l">of students who start a PhD never finish it &mdash; attrition climbs from ~10&ndash;15% in year one to ~50% by year five</div></div>
      <div class="stat-box"><div class="n">84%</div><div class="l">of surveyed biomedical PhD students had failed to replicate their own prior results at least once (2023 survey)</div></div>
      <div class="stat-box"><div class="n">$28.2B/yr</div><div class="l">estimated annual cost of irreproducible preclinical biomedical research in the U.S. alone &mdash; Freedman, Cockburn &amp; Simcoe, <em>PLOS Biology</em>, 2015</div></div>
    </div>
    <p>The same 2023 study found that 70% of those students had also failed to replicate a colleague&rsquo;s finding, and 58% had failed to replicate a result from the published literature &mdash; and for roughly a quarter of the students surveyed, the resulting stress was severe enough to interfere with eating, sleeping, or the ability to work. The $28.2 billion figure is deliberately conservative: it assumes only half of preclinical biomedical research is irreproducible, when some independent estimates run as high as 89%.</p>
    <p>There is a second, quieter version of the same problem: research that fails is far less likely to ever be written up at all &mdash; the <strong>file-drawer problem</strong>. One dataset tracking published papers found the share reporting a positive, statistically significant result rose past 80% after 1999 and reached 88.6% by 2005, not because negative results are rare in the lab, but because they are dramatically less likely to be written up and submitted for publication in the first place.</p>
    <p>None of these numbers are about FU, or about AI at all. They describe the ordinary, already-existing condition of human research &mdash; an enormous amount of skilled, well-intentioned, expensive effort spent finding out, the slow way, that a particular idea doesn&rsquo;t hold up, with the negative result then largely vanishing rather than sparing the next student the same trip. This is the gap FU's whole curriculum (Article V) is built to sit inside: generation is cheap; verification (Article VI) and refutation (Article VII) exist to compress, into minutes, the version of &ldquo;does this actually hold up&rdquo; a real researcher would otherwise spend a year of bench time discovering alone. FU does not and cannot replace that year of real experimental work for a hypothesis that survives &mdash; nothing computational substitutes for a real experiment. But for the hypotheses that would have failed anyway, which the numbers above suggest is most of them, catching that earlier and cheaply is the entire founding purpose of this institution.</p>
  </section>

  <section id="mechanisms" class="charter-article">
    <h2><span class="num">IV</span>The Three Departments, Formally</h2>
    <p>Article II told these three mechanisms as stories, one researcher at a time. This Article states exactly how each one becomes a repeatable step FU can run against any two domains pulled from its pool &mdash; not three settings of one prompt, but three structurally different generation modes, each with its own geometry.</p>
    <table class="pub-table">
      <tr><th>Department</th><th>Geometry</th><th>What it produces</th><th>Doctrine source</th></tr>
      <tr><td><strong>Bisociation Studies</strong></td><td>Horizontal &mdash; two domains collide, each stays itself</td><td>A candidate functor mapping between them</td><td>Koestler, <em>The Act of Creation</em> (1964)</td></tr>
      <tr><td><strong>Janusian Studies</strong></td><td>Vertical &mdash; one domain&rsquo;s proposition held against its exact opposite</td><td>A falsifiable paradox &mdash; genuinely both true at once, not a compromise</td><td>Rothenberg, 1976/1979</td></tr>
      <tr><td><strong>Homospatial Studies</strong></td><td>Overlaid &mdash; two domains superimposed in the same conceptual space</td><td>One fused entity belonging to neither source</td><td>Rothenberg, 1976; cognitive-science successor: conceptual blending (Fauconnier &amp; Turner)</td></tr>
    </table>
    <p>One term above is worth unpacking rather than skating past: a <strong>functor</strong>, borrowed loosely from category theory, just means a structure-preserving map &mdash; a specific, stated rule for translating a concept in one domain into its counterpart in the other, precise enough to be checked and found right or wrong. That precision is what separates a Bisociation Studies hypothesis from an ordinary metaphor: &ldquo;markets are like ecosystems&rdquo; is not falsifiable; &ldquo;overcrowding in market X should produce the same boom-bust cycle observed in population Y, on the same rough timescale&rdquo; is.</p>
    <p>Each department turned out to have a real, exploitable failure mode a naive implementation would have missed &mdash; documented in full, with the actual fixes, in <a href="#history">Article X</a>.</p>
  </section>

  <section id="curriculum" class="charter-article">
    <h2><span class="num">V</span>The Four-Phase Curriculum</h2>
    <p>Generation &mdash; the three departments above &mdash; is only the first phase of four. A hypothesis is worthless left alone; the rest of the curriculum exists to check it, the same way a real doctoral candidate's proposal is worthless without a committee.</p>
    <figure class="charter-fig">
      <img src="fu-charter-pipeline.jpg" alt="Four-phase curriculum diagram: Exploration, Web Verification, Researcher Outreach, Data Update">
      <figcaption>Fig. 1 &mdash; the four-phase curriculum every hypothesis passes through</figcaption>
    </figure>
    <ol style="padding-left:22px; line-height:1.8;">
      <li><strong>Exploration</strong> &mdash; the three departments, drawing domain pairs from FU's combined pool.</li>
      <li><strong>Web Verification</strong> &mdash; the four-way classifier that checks each hypothesis against real search results (<a href="#evidence">Article VI</a>).</li>
      <li><strong>Researcher Outreach</strong> &mdash; for hypotheses that clear verification as genuinely fertile, draft (never auto-send) a short email to a real, named researcher active in the adjacent field verification surfaced.</li>
      <li><strong>Data Update</strong> &mdash; reconcile whatever Phase 3 reveals back into the hypothesis&rsquo;s status on the Ledger.</li>
    </ol>
    <div class="charter-callout">
      <span class="cl-label">A fixed constraint, not a per-case judgment call</span>
      Phase 3 produces drafts only. No email is ever sent by this pipeline autonomously. Every draft carries an explicit &ldquo;NOT SENT&mdash;requires sign-off&rdquo; banner. No hypothesis to date has produced a real draft &mdash; none has yet reached the bar that would trigger one (see <a href="#record">Article IX</a>).
    </div>
  </section>

  <section id="evidence" class="charter-article">
    <h2><span class="num">VI</span>Standing Rules of Evidence</h2>
    <p>Think of this phase as a fact-checker with one job: for a given hypothesis, honestly answer whether someone has already said this, whether real unclaimed territory sits nearby, or whether the underlying premise doesn&rsquo;t even hold up. Every generated hypothesis&rsquo;s own self-critique includes a &ldquo;known prior art: not verified&rdquo; line &mdash; an honest admission that the model that generated it cannot check its own novelty claim. This phase resolves that admission against real web search, sorting each result into one of four outcomes:</p>
    <figure class="charter-fig">
      <img src="fu-charter-classifier.jpg" alt="Four-way verdict classifier: COLLISION, ADJACENT_ACTIVE, FACT_CHECK_FAIL, NO_SIGNAL">
      <figcaption>Fig. 2 &mdash; the four-way classifier</figcaption>
    </figure>
    <p>The design decision underneath this figure is that it&rsquo;s <strong>four buckets, not a pass/fail binary</strong> &mdash; because &ldquo;did the search find something&rdquo; actually collapses two signals that point in opposite directions. Finding the <em>exact</em> connection already published proves the reasoning is sound &mdash; but it also means the specific hypothesis has zero marginal novelty left. Finding real, active research <em>near</em> the domains, without the exact connection having been drawn, is the actual target state: real, fertile, unclaimed ground. Collapsing both into one &ldquo;found something&rdquo; bit would reward FU for rediscovering consensus over producing discovery.</p>
    <h3>The umbrella-trap rule</h3>
    <p>A second rule, discovered empirically rather than planned upfront: a bridging field only counts as ADJACENT_ACTIVE evidence if it is genuinely <em>specific</em> &mdash; if it would <em>not</em> return the same hit for most other domain pairs in the pool. The first real case this caught: a Neuroscience&times;Climatology hypothesis where the only bridging material found was &ldquo;both are complex adaptive systems&rdquo; &mdash; true of nearly any two nonlinear domains that exist. Treating that as confirmation would have made the ADJACENT_ACTIVE bucket meaningless. The hypothesis was correctly routed to NO_SIGNAL instead, and failed independent adversarial refutation on all three lenses (<a href="#gauntlet">Article VII</a>).</p>
  </section>

  <section id="gauntlet" class="charter-article">
    <h2><span class="num">VII</span>The Gauntlet</h2>
    <p>If Article VI is a fact-checker, this Article is closer to a hostile peer-review panel &mdash; except each reviewer works entirely alone, has never seen the other two&rsquo;s notes, and is specifically trying to find the one flaw that kills the claim. It exists because NO_SIGNAL is the one verdict Article VI cannot resolve by design: it looks identical whether a hypothesis is genuinely novel-and-real, or vacuous-and-not-even-wrong, because nothing external exists yet to check it against. The Gauntlet attacks the claim&rsquo;s own internal structure instead of searching for prior art, through three independent lenses:</p>
    <ul style="padding-left:22px; line-height:1.8;">
      <li><strong>Coherence</strong> &mdash; does the claimed mapping quietly equivocate on a term as it crosses from one domain into the other?</li>
      <li><strong>Testability</strong> &mdash; is the falsifiable prediction actually operationalized, or vague enough that nothing could ever return a clean &ldquo;no&rdquo;?</li>
      <li><strong>Triviality</strong> &mdash; stripped of its domain-specific vocabulary, does the claim reduce to something true of almost any two complex systems?</li>
    </ul>
    <p>Promotion out of NO_SIGNAL requires 2 of 3 lenses to find the claim survives &mdash; the &ldquo;Survived the Gauntlet&rdquo; badge carried on the Ledger. Every lens defaults to REFUTED under genuine uncertainty, a deliberate asymmetry against false positives: a hypothesis wrongly killed costs nothing, while a hollow one wrongly promoted costs someone real time later.</p>
    <p>One real case from the standing record, still on the Ledger exactly as it was found:</p>
    {_charter_example("Neural networks × Coral reef ecosystems", "An independent reviewer was asked simply to check whether the hypothesis's own document delivered on what its own abstract promised. It didn't:")}
  </section>

  <section id="tenure" class="charter-article">
    <h2><span class="num">VIII</span>Tenure and the Ledger</h2>
    <p>Points are tied to what an outcome actually reveals about a hypothesis&rsquo;s real potential, not to how far it made it through the curriculum:</p>
    <table class="pub-table">
      <tr><th>Event</th><th class="pts">Points</th><th>Why</th></tr>
      <tr><td>Web Verification: ADJACENT_ACTIVE</td><td class="pts">+30</td><td>The actual target state</td></tr>
      <tr><td>Web Verification: COLLISION (genuine)</td><td class="pts">+5</td><td>Zero novelty, but real credit for valid reasoning</td></tr>
      <tr><td>Web Verification: COLLISION (not a valid bisociation)</td><td class="pts">&minus;5</td><td>Worse than genuine collision &mdash; the pairing itself was flawed</td></tr>
      <tr><td>Web Verification: FACT_CHECK_FAIL</td><td class="pts">&minus;10</td><td>Hallucinated domain facts</td></tr>
      <tr><td>The Gauntlet: survives (2&ndash;3 of 3)</td><td class="pts">+12 / +20</td><td>Real signal the claim isn&rsquo;t vacuous</td></tr>
      <tr><td>The Gauntlet: REFUTED</td><td class="pts">&minus;15</td><td>Worse than a fact-check failure &mdash; the reasoning failed under scrutiny</td></tr>
      <tr><td>Researcher Outreach: confirms novel</td><td class="pts">+50</td><td>The single strongest possible signal</td></tr>
      <tr><td>Researcher Outreach: dismisses</td><td class="pts">&minus;20</td><td>A real expert said no</td></tr>
    </table>
    <a class="cta-link" href="fu-leaderboard.html" style="display:block; margin:24px 0; padding:18px 22px; background:var(--surface); border:1px solid var(--gold); border-radius:10px; text-decoration:none; color:var(--text);">
      <div style="font-family:var(--serif); font-size:1.1rem; font-weight:600; color:var(--gold);">Open the Ledger &rarr;</div>
      <div style="color:var(--text-muted); font-size:0.88rem; margin-top:4px;">Every hypothesis this Charter describes, ranked, filterable by tier and department, expandable to the full record &mdash; the actual hypothesis text, verification reasoning, and refutation reasoning where it ran.</div>
    </a>
  </section>

  <section id="record" class="charter-article">
    <h2><span class="num">IX</span>The Current Record</h2>
    <p>As of this Charter's last build: <strong>{TOTAL_SCORED} hypotheses</strong> carry a canonical verdict, none pending, across {len(DOMAINS)} real domains.</p>
    <table class="pub-table">
      <tr><th>Department</th><th class="pts">n resolved</th><th class="pts">Avg. points</th><th class="pts">Reach NO_SIGNAL</th></tr>
      <tr><td>Bisociation Studies</td><td class="pts">{DEPT_PERF.get('bisociation',{}).get('n','—')}</td><td class="pts">{DEPT_PERF.get('bisociation',{}).get('avg','—'):+.1f}</td><td class="pts">{DEPT_PERF.get('bisociation',{}).get('no_signal','—')}%</td></tr>
      <tr><td>Janusian Studies</td><td class="pts">{DEPT_PERF.get('janusian',{}).get('n','—')}</td><td class="pts">{DEPT_PERF.get('janusian',{}).get('avg','—'):+.1f}</td><td class="pts">{DEPT_PERF.get('janusian',{}).get('no_signal','—')}%</td></tr>
      <tr><td>Homospatial Studies</td><td class="pts">{DEPT_PERF.get('homospatial',{}).get('n','—')}</td><td class="pts">{DEPT_PERF.get('homospatial',{}).get('avg','—'):+.1f}</td><td class="pts">{DEPT_PERF.get('homospatial',{}).get('no_signal','—')}%</td></tr>
      <tr><td>Calibration benchmarks (pre-existing case studies)</td><td class="pts">{DEPT_PERF.get('case-study',{}).get('n','—')}</td><td class="pts">{DEPT_PERF.get('case-study',{}).get('avg','—'):+.1f}</td><td class="pts">{DEPT_PERF.get('case-study',{}).get('no_signal','—')}%</td></tr>
    </table>
    <p>&ldquo;Reach NO_SIGNAL&rdquo; is a real base rate, not a failure rate &mdash; it is the share of a department&rsquo;s output that had to go to <a href="#gauntlet">the Gauntlet</a> at all, because nothing external existed yet to check it against one way or the other.</p>
    <h3>Rank one on the Ledger</h3>
    <p>The single highest-scoring hypothesis FU has ever produced, standing as of this build:</p>
    {_charter_example(top_row["pairing"])}
  </section>

  <section id="history" class="charter-article">
    <h2><span class="num">X</span>Founding-Era History</h2>
    <p>Four real failures were found in FU's first working pilot batch &mdash; the original 58-hypothesis pool this university was founded on &mdash; three fixed, one left open at the time. They are reported here in full, dated plainly as founding history rather than restated as current statistics, because they are the clearest evidence for what actually made this institution trustworthy in the first place.</p>
    <figure class="charter-fig">
      <img src="fu-charter-verdict-40.jpg" alt="Bar chart: final status across an early 40-hypothesis snapshot, an even earlier count than the 58-hypothesis pilot pool this history describes">
      <figcaption>Fig. 3 &mdash; an early snapshot from FU's own founding pilot, before the pool grew past 40 hypotheses. Kept here exactly as it was generated at the time, not updated &mdash; the current record lives on <a href="fu-leaderboard.html">the Ledger</a>, not in this figure.</figcaption>
    </figure>

    <h3>Failure 1 &mdash; Janusian&rsquo;s soft self-check got talked past</h3>
    <p>All three of the first round of Janusian generations labeled a disguised compromise (&ldquo;beneficial in context A, detrimental in context B&rdquo;) as a genuine paradox &mdash; exactly the failure mode the prompt&rsquo;s own instructions described, just relabeled as success by the model itself. A mechanical &ldquo;same-instance test&rdquo; was added to the prompt (can the claimed paradox be rephrased as two <em>different</em> instances, rather than one instance holding both truths at once?) and the same three domains were regenerated: measurable improvement, 2 of 3 clearly passed.</p>

    <h3>Failure 2 &mdash; homospatial&rsquo;s fusion criterion needed code, not just prompt text</h3>
    <p>The first two homospatial generations were bisociation wearing a coined name &mdash; entities like &ldquo;Crowd Play&rdquo; and &ldquo;Narrative Lattice&rdquo; that were, on inspection, ordinary metaphors (&ldquo;mirrors,&rdquo; &ldquo;akin to,&rdquo; &ldquo;much like&rdquo;) rather than genuine fusions. A written prompt rule banning comparison language was tried first &mdash; it did not hold; the very next generation still used the banned words directly. This was escalated to <strong>code-level enforcement</strong>: after generation, the pipeline mechanically scans the fused-entity section for comparison words, and if any are found, sends one corrective re-prompt quoting the exact violation back to the model. Run at scale against 7 homospatial pairs: all 7 eventually passed (5 needed the corrective retry), and the one case where the retry still left a residual violation was flagged transparently in its own output file rather than hidden.</p>
    <div class="charter-callout">
      <span class="cl-label">The general lesson</span>
      A soft, written self-check gets talked past by the model that&rsquo;s supposed to be checking itself. A mechanical, code-level check on the actual output text does not. This is the same finding, one level up, that motivated the Gauntlet in the first place: self-report is not verification.
    </div>

    <h3>Failure 3 &mdash; a real resource constraint, and its actual fix</h3>
    <p>An early session&rsquo;s web-search budget was exhausted after only 5 of a planned 15 verification queries. Rather than fabricate the remaining verdicts or drop them silently, they were recorded with an explicit <code>PENDING_VERIFICATION</code> status, held out of scoring with a clear, visible reason, until a dedicated later session resolved the backlog by hand. The durable fix &mdash; a standalone script that runs verification unattended, with no live session and no shared search budget &mdash; has since been built and proven in real production runs.</p>

    <h3>Failure 4 &mdash; the same-instance test let the same failure through three times in one batch</h3>
    <p>Failure 1&rsquo;s fix was believed closed after the original three-domain regeneration showed 2 of 3 clearly passing. A later batch said otherwise: of 6 new Janusian hypotheses, 3 turned out, once put through the Gauntlet, to be the exact same disguised compromise Failure 1 was supposed to have fixed &mdash; each one&rsquo;s own self-critique quietly conceding &ldquo;different contexts&rdquo; or &ldquo;different datasets&rdquo; rather than a true same-instance contradiction. A second, smaller instance of the same class of problem showed up in homospatial output too: one hypothesis passed its code-level comparison-word scan on the first attempt, yet its own text read, verbatim, &ldquo;<em>akin to</em> laminar flow&rdquo; and &ldquo;<em>similar to</em> how turbulent eddies&rdquo; &mdash; exactly the banned comparison language the scan exists to catch. The Gauntlet caught what the earlier code-level scan missed both times.</p>
    <div class="charter-callout warn">
      <span class="cl-label">Open, not closed</span>
      Both of these are the same shape as Failure 1 and Failure 2&rsquo;s original findings: a check believed fixed after a small sample turned out to still be beatable at a slightly larger scale. This is disclosed here as founding-era working engineering debt, not retroactively smoothed into a success story.
    </div>
  </section>

  <section id="limitations" class="charter-article">
    <h2><span class="num">XI</span>Limitations and Open Questions</h2>
    <ul style="padding-left:22px; line-height:1.9;">
      <li><strong>The domain pool is a standing resource, not a finished one.</strong> {len(DOMAINS)} real domains yield many thousands of possible pairings; {TOTAL_SCORED} hypotheses have been explored across all three departments and the calibration benchmarks combined &mdash; a real fraction of the possible ground, not implied complete. The current live count is always <a href="fu-course-catalog.html">the Course Catalog</a>, not any number printed in this Charter.</li>
      <li><strong>Researcher Outreach has produced zero real drafts.</strong> No hypothesis to date has reached ADJACENT_ACTIVE-and-durable with a real researcher identified to contact &mdash; the mechanism exists (Article V) but hasn&rsquo;t been exercised for real yet.</li>
      <li><strong>Verification and the Gauntlet remain a check on plausibility, not a substitute for an experiment.</strong> Nothing in this pipeline runs a real test of any hypothesis against the physical or social world &mdash; it only checks whether a hypothesis is novel, coherent, and worth someone&rsquo;s time to actually go test. That check is the entire value proposition described in Article III; it is not, and was never meant to be, the experiment itself.</li>
      <li><strong>A hypothesis's status can and does change as the pool grows.</strong> Verdicts on this Ledger are not fixed at the moment of first scoring &mdash; a hypothesis judged one way in an earlier pilot batch can read differently once the record around it has grown. Article X's history is deliberately left as it happened rather than reconciled against the current Ledger; where the two disagree, the Ledger is the live truth and the history is the record of how FU got there.</li>
    </ul>
  </section>

  <section id="closing" class="charter-article">
    <h2><span class="num">XII</span>The Closing Article</h2>
    <p>The four-way verification layer answers two different questions at once, depending on how you read it: whether one specific hypothesis is novel (COLLISION says no), and whether the underlying generative mechanism reliably finds real, legitimate cross-domain territory at all (COLLISION, read this second way, says yes &mdash; every genuine collision found is evidence the reasoning is not hallucinated, even in the cases where a specific hypothesis turns out to be unoriginal). A real share of this record sits in genuinely fertile, unclaimed territory. Many more looked plausible on generation and did not survive independent adversarial scrutiny &mdash; caught, not hidden. That is the most important sentence in this Charter to sit with honestly: it is easier to build a system that finds connections than to build one that can be trusted when it says a connection is real.</p>
    <blockquote>&ldquo;The mere fact that we&rsquo;re getting successful bisociations means we have the beginnings of a university.&rdquo;</blockquote>
    <p>That line, from the real technical report this Charter is built on top of, was written before FU existed. It has since been tested rather than assumed &mdash; not by counting every generated hypothesis as a discovery, but by building the same four-way classifier and Gauntlet used throughout this Charter and applying them to results that turn out to be wrong just as rigorously as to the ones that don&rsquo;t. Article III&rsquo;s numbers are the reason any of this is worth doing at all: PhD researchers spend years, and the field as a whole spends tens of billions of dollars annually, finding out by hand which hypotheses don&rsquo;t hold up. A university that can run the same collision Darwin stumbled into once, on purpose, hundreds of times over &mdash; and then honestly tell you, in minutes, which of those collisions are worth a real person&rsquo;s year &mdash; does not replace the scientist. It replaces the coin flip. That, and nothing more elaborate than that, is what FU is chartered to be.</p>
  </section>

  </article>
  </div>
  {ROW_TOGGLE_JS}'''
    return wrap("The Charter — FU", body, None)


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
    <p class="real-thing">Real thing: <a href="whitepaper.html#curriculum">the Charter</a>, Articles V&ndash;VI &amp; VIII.</p>

    <h2 style="margin-top:40px;">The Current Shortlist</h2>
    <p style="color:var(--text-muted); max-width:700px;">The top 8 real, currently-standing candidates across all three departments &mdash; excluding the calibration benchmarks, which were never up for funding in the first place. Click any row for the full real record.</p>
    {expandable_pub_rows(top_overall)}

    <div class="stat-row" style="margin-top:32px;">
      <div class="stat-box"><div class="n">$36.61</div><div class="l">total real spend across {TOTAL_ENTRIES} candidates evaluated &mdash; <a href="fu-home.html#cost" style="color:inherit;">receipt &rarr;</a></div></div>
      <div class="stat-box"><div class="n">{TOTAL_SCORED}</div><div class="l">candidates actually scored</div></div>
      <div class="stat-box"><div class="n">3</div><div class="l">independent reviewers per adversarial pass</div></div>
    </div>

    <p style="margin-top:24px; color:var(--text-muted); max-width:700px;">This office makes recommendations. It does not disburse funds, does not replace a human program officer's judgment, and does not claim a &ldquo;Survived Refutation&rdquo; tag means a discovery is real &mdash; only that it survived three honest attempts to kill it. See <a href="whitepaper.html#gauntlet">the Charter's own Article VII</a> for the honest limits of this claim.</p>
  </div>
  {ROW_TOGGLE_JS}'''
    return wrap("For Investors & Grant Officers — FU", body, "investors")


# ---------------------------------------------------------------------------
# fu-faculty.html -- the directory. Modeled on the real pattern Berkeley
# calls an "expertise finder" (Academics/Research menus at Harvard,
# Princeton, and Berkeley were read directly before designing this): browse
# a faculty body by specialty, not just an alphabetical list.
# ---------------------------------------------------------------------------

def hover_media_html(img_src, video_src, alt):
    """An img and a video sharing one box (see .hover-media CSS) -- hover
    swaps which is visible via HOVER_VIDEO_JS, without ever changing the
    element's footprint. video src is lazy (data-src), never fetched
    until the first real hover."""
    return f'''<div class="hover-media">
        <img src="{img_src}" alt="{alt}">
        <video muted loop playsinline preload="none" data-src="{video_src}"></video>
      </div>'''


def faculty_card_html(fac, dept_filter_attr=True):
    n_pubs = len(publications_for_faculty(fac["id"]))
    attr = f' data-dept="{fac["dept"]}"' if dept_filter_attr else ""
    return f'''<a class="faculty-card"{attr} href="fu-faculty-{fac['id']}.html">
      {hover_media_html(fac['img'], f"fu-lecture-{fac['id']}.mp4", f"{fac['name']}, {fac['title']}")}
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
      {hover_media_html(meta['img'], f"fu-lecture-chair-{mode_key}.mp4", meta['chair_title'])}
      <div class="body">
        <div class="name">Office of the Chair</div>
        <div class="title">{meta['chair_title']}</div>
        <div class="spec">{meta['short']}</div>
        <div class="n">{perf.get('n','—')} real publications</div>
      </div>
    </a>'''


HOVER_VIDEO_JS = '''<script>
document.querySelectorAll('.hover-media').forEach(function(box) {
  var video = box.querySelector('video');
  if (!video) return;
  var loaded = false;
  box.addEventListener('mouseenter', function() {
    if (!loaded) { video.src = video.getAttribute('data-src'); video.load(); loaded = true; }
    box.classList.add('is-playing');
    video.play().catch(function() {});
  });
  box.addEventListener('mouseleave', function() {
    box.classList.remove('is-playing');
    video.pause();
  });
});
</script>'''

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


LEADERBOARD_FILTER_JS = '''<script>
(function() {
  var searchInput = document.getElementById('lb-search');
  var tierButtons = document.querySelectorAll('.lb-tier-filter button');
  var deptButtons = document.querySelectorAll('.lb-dept-filter button');
  var rows = document.querySelectorAll('#lb-rows .row');
  var countEl = document.getElementById('lb-count');
  var state = { tier: 'all', dept: 'all', q: '' };

  function apply() {
    var shown = 0;
    rows.forEach(function(r) {
      var tierOk = state.tier === 'all' || r.getAttribute('data-tier') === state.tier;
      var deptOk = state.dept === 'all' || r.getAttribute('data-dept') === state.dept;
      var pairingEl = r.querySelector('.pairing');
      var text = pairingEl ? pairingEl.textContent.toLowerCase() : '';
      var qOk = state.q === '' || text.indexOf(state.q) !== -1;
      var visible = tierOk && deptOk && qOk;
      r.style.display = visible ? '' : 'none';
      if (visible) shown++;
    });
    if (countEl) countEl.textContent = shown + ' of ' + rows.length + ' shown';
  }

  tierButtons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      tierButtons.forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      state.tier = btn.getAttribute('data-filter');
      apply();
    });
  });
  deptButtons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      deptButtons.forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      state.dept = btn.getAttribute('data-filter');
      apply();
    });
  });
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      state.q = searchInput.value.toLowerCase();
      apply();
    });
  }
})();
</script>'''


TIER_SLUG = {
    "🛡️ Survived Refutation": "survived",
    "🗺️ Verified, Unrefuted": "verified",
    "🌗 Contested": "contested",
    "💀 Refuted / Rejected": "refuted",
}


def dept_slug_for_row(r):
    for k, v in MODE_META.items():
        if v["badge"] in r["badges"]:
            return k
    return "calibration"


def build_leaderboard():
    """The full real record, unfiltered -- every row leaderboard.md has,
    in its own real rank order (tier first, points as tie-breaker), each
    one the same real click-expandable content the faculty pages and course
    catalog use. Curated top-N lists live elsewhere on this site; this page
    is the whole ledger they were each drawn from."""
    tier_counts = {}
    dept_counts = {}
    rows_html = []
    for r in ROWS:
        tier_slug = TIER_SLUG.get(r["tier"], "other")
        dept_slug = dept_slug_for_row(r)
        tier_counts[tier_slug] = tier_counts.get(tier_slug, 0) + 1
        dept_counts[dept_slug] = dept_counts.get(dept_slug, 0) + 1

        e = EXP_BY_PAIRING.get(r["pairing"].strip().lower())
        if e:
            row_html = exp_row_html(e, rank=r["rank"])
        else:
            pts_class = "pos" if r["points"] > 0 else ("neg" if r["points"] < 0 else "zero")
            row_html = f'''<div class="row"><div class="row-head" style="cursor:default;">
              <span class="rank">{r['rank']}</span><span class="pairing">{r['pairing']}</span>
              <span class="row-badge" style="color:var(--gold);border-color:var(--gold);">{r['verdict']}</span>
              <span class="r-points {pts_class}">{r['points']:+d}</span>
            </div></div>'''
        row_html = row_html.replace(
            '<div class="row">',
            f'<div class="row" data-tier="{tier_slug}" data-dept="{dept_slug}">',
            1,
        )
        rows_html.append(row_html)

    tier_defs = [
        ("all", "All Tiers", len(ROWS)),
        ("survived", "🛡️ Survived Refutation", tier_counts.get("survived", 0)),
        ("verified", "🗺️ Verified, Unrefuted", tier_counts.get("verified", 0)),
        ("contested", "🌗 Contested", tier_counts.get("contested", 0)),
        ("refuted", "💀 Refuted / Rejected", tier_counts.get("refuted", 0)),
    ]
    dept_defs = [
        ("all", "All Departments", len(ROWS)),
        ("bisociation", "Bisociation Studies", dept_counts.get("bisociation", 0)),
        ("janusian", "Janusian Studies", dept_counts.get("janusian", 0)),
        ("homospatial", "Homospatial Studies", dept_counts.get("homospatial", 0)),
        ("calibration", "Calibration Benchmarks", dept_counts.get("calibration", 0)),
    ]
    tier_buttons = "".join(
        f'<button class="{"active" if k == "all" else ""}" data-filter="{k}">{label} ({n})</button>'
        for k, label, n in tier_defs
    )
    dept_buttons = "".join(
        f'<button class="{"active" if k == "all" else ""}" data-filter="{k}">{label} ({n})</button>'
        for k, label, n in dept_defs
    )

    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Office of the Registrar</span>
    <h1>The Full Ledger</h1>
    <p style="color:var(--text-muted); max-width:700px;">Every real hypothesis FU has ever produced, in the exact order the university's own scoring system ranks them &mdash; tier first, points as the tie-breaker, nothing curated out. The department, faculty, and course-catalog pages elsewhere on this site each show a curated slice of this record; this is the whole thing, all {len(ROWS)} scored entries. Click any row for its full real hypothesis, verification, and adversarial refutation.</p>
    <p class="real-thing">Real thing: <code>leaderboard.md</code> in full &mdash; every row, in the exact rank order the real automated scoring pipeline produced it. The 12 &ldquo;Calibration Benchmarks&rdquo; are pre-existing, already-known case studies used to sanity-check the scorer, not department output &mdash; excluded from every other page's rankings, included here for completeness.</p>

    <div class="lb-toolbar">
      <input type="text" id="lb-search" class="lb-search" placeholder="Search by pairing (e.g. &ldquo;compiler&rdquo;, &ldquo;immune system&rdquo;)&hellip;" autocomplete="off">
    </div>
    <div class="lb-filter-label">Tier</div>
    <div class="faculty-filter lb-tier-filter">{tier_buttons}</div>
    <div class="lb-filter-label">Department</div>
    <div class="faculty-filter lb-dept-filter">{dept_buttons}</div>
    <div class="lb-count" id="lb-count">{len(ROWS)} of {len(ROWS)} shown</div>

    <div id="lb-rows" style="margin-top:8px;">{"".join(rows_html)}</div>
  </div>
  {ROW_TOGGLE_JS}
  {LEADERBOARD_FILTER_JS}'''
    return wrap("The Full Ledger — FU", body, "leaderboard")


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
  {FILTER_JS}
  {HOVER_VIDEO_JS}'''
    return wrap("Faculty & Research — FU", body, "faculty")


FACULTY_PUBS_SHOWN = 30


def build_faculty_page(fac):
    meta = MODE_META[fac["dept"]]
    pubs = publications_for_faculty(fac["id"])
    students = STUDENTS_BY_FACULTY[fac["id"]]

    pub_rows_html = ""
    for i, (row, student) in enumerate(pubs[:FACULTY_PUBS_SHOWN]):
        exp = EXP_BY_PAIRING.get(row["pairing"].strip().lower())
        if exp:
            pub_rows_html += exp_row_html(exp, rank=i + 1, researcher=student["name"])
        else:
            # Real leaderboard row with no matching experience_data.json
            # record (a handful of held-out/edge entries) -- shown plainly
            # rather than silently dropped.
            pub_rows_html += f'''<div class="row"><div class="row-head" style="cursor:default;">
              <span class="rank">{i+1}</span><span class="pairing">{row['pairing']}</span>
              <span class="researcher">{student['name']}</span>
              <span class="row-badge" style="color:var(--gold);border-color:var(--gold);">{row['verdict']}</span>
              <span class="r-points {'pos' if row['points']>0 else ('neg' if row['points']<0 else 'zero')}">{row['points']:+d}</span>
            </div></div>'''

    roster_html = "".join(
        f'''<li><span>{s['name']}</span><span class="deg">{s['degree']}</span></li>''' for s in students
    )

    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">{meta['name']}</span>

    <div class="faculty-hero">
      <video src="fu-lecture-{fac['id']}.mp4" poster="{fac['img']}" controls preload="metadata" playsinline style="width:100%; aspect-ratio:4/3; object-fit:cover; border-radius:12px; border:1px solid var(--border); display:block;"></video>
      <div>
        <h1 style="margin-bottom:4px;">{fac['name']}</h1>
        <p style="font-family:var(--mono); color:var(--gold); font-size:0.9rem; margin:0 0 4px;">{fac['title']}, {meta['name']}</p>
        <p style="font-family:var(--mono); color:var(--text-faint); font-size:0.82rem; margin:0 0 18px;">Specialty: {fac['specialty_label']}</p>
        <p style="color:var(--text-muted); max-width:520px;">{fac['name'].split(' ',1)[-1] if ' ' in fac['name'] else fac['name']}'s work in the {meta['name']} focuses on {fac['specialty_label'].lower()}: {meta['verb_phrase']}, applied here to real problems in the field. {len(pubs)} real hypotheses generated under this specialty, ranked exactly as the leaderboard ranks them.</p>
        <p class="real-thing">A fictional persona, delivering a real finding: the video above cites {fac['name'].split(' ',1)[-1] if ' ' in fac['name'] else fac['name']}'s own real top-ranked publication, word for word. Real thing: the subset of <code>leaderboard.md</code> real entries whose real subject matter falls under {fac['specialty_label']}.</p>
      </div>
    </div>

    <h2 style="margin-top:36px;">Lab Roster</h2>
    <ul class="roster-list" style="max-width:420px;">{roster_html}</ul>

    <h2 style="margin-top:36px;">Publications ({len(pubs)} real, {min(FACULTY_PUBS_SHOWN,len(pubs))} shown)</h2>
    <p style="color:var(--text-muted); max-width:680px;">Click any row for the full real record &mdash; the actual hypothesis, its real verification search, and its adversarial refutation where one ran.</p>
    {pub_rows_html}

    <p style="margin-top:28px;"><a href="fu-department-{fac['dept']}.html">&larr; {meta['name']}</a> &middot; <a href="fu-faculty.html">All Faculty &rarr;</a></p>
  </div>
  {ROW_TOGGLE_JS}'''
    return wrap(f"{fac['name']} — FU", body, "faculty")


# ---------------------------------------------------------------------------
# fu-campus-explore.html -- a real tour of the imagined campus. Faculty
# directory browsing already lives at fu-faculty.html (Berkeley's own
# "expertise finder" pattern); this page's job is atmosphere -- walk through
# the buildings, the lobbies, a lecture in session -- not a second database
# UI duplicating that one.
# ---------------------------------------------------------------------------

LECTURE_VIDEOS = [
    {
        "file": "fu-lecture-bisociation.mp4",
        "dept": "bisociation",
        "line": "“Overlay social network structure onto team collaboration, and one pattern holds: network density that predicts a healthy social system also predicts a team that ships.”",
        "real_pairing": "Social Systems × Human Team Collaboration",
    },
    {
        "file": "fu-lecture-janusian.mp4",
        "dept": "janusian",
        "line": "“Instruction scheduling improves performance by cutting execution time — and it degrades performance, by adding overhead. Both are true. That contradiction is the real research question.”",
        "real_pairing": "Computer science — compiler instruction scheduling",
    },
    {
        "file": "fu-lecture-homospatial.mp4",
        "dept": "homospatial",
        "line": "“Superimpose immune memory onto city planning, and a city starts to look like an immune system: it remembers past shocks, and defends against what it has already survived.”",
        "real_pairing": "Adaptive Immune Memory × Human Urban Planning",
    },
]


def lecture_video_card(v):
    meta = MODE_META[v["dept"]]
    exp = EXP_BY_PAIRING.get(v["real_pairing"].strip().lower())
    pts = exp.get("points") if exp else None
    verdict = exp.get("verdict") if exp else None
    real_line = f"real hypothesis, {pts:+d} pts, {verdict}" if exp else "real hypothesis on record"
    return f'''<div class="tour-video-card">
      <video src="{v['file']}" controls preload="metadata" playsinline></video>
      <div class="body">
        <h3>{meta['name']}</h3>
        <p>{v['line']}</p>
        <p class="real-thing" style="margin-top:8px;">Real finding cited: <b>{v['real_pairing']}</b> ({real_line}). Delivery is fictional &mdash; the finding is not.</p>
      </div>
    </div>'''


def campus_tour_stops():
    """The tour's actual stops -- shared between the standalone Campus page
    and the Campus section folded into the landing page, so the two never
    drift out of sync with hand-duplicated content."""
    video_cards = "".join(lecture_video_card(v) for v in LECTURE_VIDEOS)
    seal_row = "".join(
        f'<figure><img src="{img}" alt="{label}"><figcaption>{label}</figcaption></figure>'
        for img, label in [
            ("dean-letters-bisociation.jpg", "Bisociation Studies"),
            ("dean-letters-janusian.jpg", "Janusian Studies"),
            ("dean-letters-homospatial.jpg", "Homospatial Studies"),
        ]
    )

    return f'''<div class="tour-stop" style="margin-top:40px;">
      <div class="tour-imgs"><img src="fu-campus.jpg" alt="Arrival at FU"></div>
      <div class="tour-caption">
        <h2>Arrival</h2>
        <p>Ivy, stone, and a walk that gets slower the closer you get. Illustrative &mdash; real thing this stands in for: <code>run_cycle.py</code>, the actual pipeline behind every building on this tour.</p>
      </div>
    </div>

    <div class="tour-stop">
      <div class="tour-imgs"><img src="fu-campus-quad.jpg" alt="The Quad"></div>
      <div class="tour-caption">
        <h2>The Quad</h2>
        <p>The open green space between all three departments &mdash; nobody's specialty, everybody's shortcut. Real thing: the real cross-department pairs, Section 2's three mechanisms colliding across schools.</p>
      </div>
    </div>

    <div class="tour-stop">
      <div class="tour-imgs"><img src="fu-campus-library.jpg" alt="The Registrar's Library"></div>
      <div class="tour-caption">
        <h2>The Registrar's Library</h2>
        <p>Where every real transcript lives &mdash; the ranked leaderboard, shelved by tier. Real thing: <code>ledger.py</code> / <code>score_hypotheses.py</code>.</p>
      </div>
    </div>

    <div class="tour-stop">
      <div class="tour-imgs pair">
        <img src="fu-campus-science.jpg" alt="Engineering & Computation Complex, exterior">
        <img src="fu-campus-lobby-science.jpg" alt="Engineering & Computation Complex, lobby">
      </div>
      <div class="tour-caption">
        <h2>The Engineering &amp; Computation Complex</h2>
        <p>Home to the largest single specialty in every department &mdash; the busiest lab on campus by real publication count, every time. Real thing: <code>hypothesis_engine.py</code>'s most-populated real classification bucket.</p>
      </div>
    </div>

    <div class="tour-stop">
      <div class="tour-imgs"><img src="fu-campus-hall-packed.jpg" alt="A packed lecture hall"></div>
      <div class="tour-caption">
        <h2>A Lecture in Session</h2>
        <p>Three departments, three real findings, delivered the way a real lecture would deliver them. The faculty are fictional. What they're saying, in each clip, is a real result pulled straight from the leaderboard &mdash; not written for the occasion.</p>
      </div>
      <div class="tour-video-grid">{video_cards}</div>
    </div>

    <div class="tour-stop">
      <div class="tour-imgs pair">
        <img src="fu-campus-admin.jpg" alt="Administration Building, exterior">
        <img src="fu-campus-lobby-admin.jpg" alt="Administration Building, lobby">
      </div>
      <div class="tour-caption">
        <h2>Administration Building</h2>
        <p>Office of the Dean, upstairs. Real thing: <a href="fu-home.html#story-of-fu">the Dean's own real correspondence and findings</a>, delivered from here.</p>
      </div>
    </div>

    <div class="tour-stop">
      <div class="tour-imgs"><img src="fu-campus-union.jpg" alt="Student Union"></div>
      <div class="tour-caption">
        <h2>Student Union</h2>
        <p>Where PhD and Masters candidates &mdash; each one a real hypothesis in progress &mdash; compare notes between departments. Real thing: <code>hypotheses/*.md</code>, every real in-progress record.</p>
      </div>
    </div>

    <div class="tour-stop">
      <div class="tour-caption" style="max-width:none;">
        <h2>Department Seals</h2>
        <p>The same three engravings that already explain each department's method in the real Dean's Letters, reused here rather than redrawn.</p>
      </div>
      <div class="seal-row">{seal_row}</div>
    </div>

    <div class="tour-stop" style="margin-bottom:20px;">
      <div class="tour-imgs"><img src="whitepaper-masthead.jpg" alt="The Founding Collision"></div>
      <div class="tour-caption">
        <h2>The Founding Collision</h2>
        <p>FU's own founding story, told the way the Charter opens it: Darwin reading Malthus, one collision producing a whole theory. Real thing: <a href="whitepaper.html#founding">the Charter's own Article I</a>.</p>
      </div>
    </div>'''


def build_campus_explore():
    body = f'''<div class="page wide" style="padding-top:40px;">
    <span class="kicker">Campus</span>
    <h1>A Tour of FU</h1>
    <p style="color:var(--text-muted); max-width:700px;">There's no real campus &mdash; but if there were, this is what walking across it would look like. For the faculty directory, <a href="fu-faculty.html">browse by specialty instead &rarr;</a></p>

    {campus_tour_stops()}
  </div>'''
    return wrap("A Tour of FU — Campus", body, "campus")


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
  <video class="gate-bg" id="gate-video" src="fu-password-teaser.mp4" poster="fu-campus.jpg" autoplay muted loop playsinline webkit-playsinline preload="auto"></video>
  <div class="gate-overlay"></div>
  <button id="gate-unmute" class="hero-unmute">&#128264; Sound on</button>
  <div class="gate-card" id="gate-card">
    <img class="seal" src="fu-seal.jpg" alt="FU seal">
    <h1>FU: Fake University</h1>
    <div class="sub">Not accredited by anyone</div>
    <form class="gate-form" id="gate-form">
      <input type="password" id="gate-input" placeholder="Password" autocomplete="off" autofocus>
      <button type="submit" id="gate-submit">Enter</button>
      <div class="gate-error" id="gate-error"></div>
    </form>
    <div class="gate-hint">Not real security &mdash; a small pause before you go in. Everything past this door is disclosed in full at <a href="whitepaper.html">the real whitepaper</a>. The video behind this card is the real documentary's own first 15 seconds.</div>
  </div>
</div>
<script>
(function() {{
  var v = document.getElementById('gate-video');
  var btn = document.getElementById('gate-unmute');
  if (v) {{
    // Belt-and-suspenders: the autoplay/muted/loop attributes should be
    // enough on their own, but some mobile browsers (iOS Low Power Mode,
    // some Android data-saver modes) silently ignore declarative autoplay
    // and just show the poster frame. Setting .muted via JS too and
    // calling .play() explicitly recovers those cases; a rejected
    // .play() promise (still blocked) is swallowed on purpose -- the
    // poster frame is a fine fallback, not an error to surface.
    v.muted = true;
    var tryPlay = function() {{ v.play().catch(function() {{}}); }};
    if (v.readyState >= 2) {{ tryPlay(); }} else {{ v.addEventListener('loadeddata', tryPlay, {{ once: true }}); }}
    document.addEventListener('visibilitychange', function() {{ if (!document.hidden) tryPlay(); }});
  }}
  if (v && btn) {{
    btn.addEventListener('click', function() {{
      v.muted = !v.muted;
      btn.innerHTML = v.muted ? '&#128264; Sound on' : '&#128266; Sound off';
    }});
  }}
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
        "fu-leaderboard.html": build_leaderboard(),
        "whitepaper.html": build_whitepaper(),
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
