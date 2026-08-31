#!/usr/bin/env python3
import json
import os

with open("experience_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2026-08-31, leaderboard rearchitecture: mode-performance / pre-filter
# correlation, written by assemble_experience_data.py alongside the main
# entry list. Optional read -- an older experience_data.json without a
# sibling meta file still renders (empty panel), never a hard failure.
meta = {}
meta_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experience_meta.json")
if os.path.exists(meta_path):
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

data_json = json.dumps(data, ensure_ascii=False)
meta_json = json.dumps(meta, ensure_ascii=False)
# Defensive: a literal "</script" inside embedded content would prematurely
# close the script tag. Escape it so the JSON stays inert data.
data_json_safe = data_json.replace("</script", "<\\/script")
meta_json_safe = meta_json.replace("</script", "<\\/script")

html = r'''<title>Faculty of Interdisciplinary Research</title>

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
  --gold-soft: #8a6f2e;
  --v-adjacent: #5fa88f;
  --v-adjacent-bg: rgba(95, 168, 143, 0.14);
  --v-collision: #6f93bd;
  --v-collision-bg: rgba(111, 147, 189, 0.14);
  --v-collision-flag: #b98a4a;
  --v-collision-flag-bg: rgba(185, 138, 74, 0.14);
  --v-refuted: #b56b6b;
  --v-refuted-bg: rgba(181, 107, 107, 0.14);
  --v-pending: #8a8577;
  --v-pending-bg: rgba(138, 133, 119, 0.14);
  --serif: ui-serif, Georgia, 'Iowan Old Style', 'Times New Roman', serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Inter', ui-sans-serif, 'Segoe UI', sans-serif;
  --mono: ui-monospace, 'SF Mono', Menlo, monospace;
}
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    --ink: #f6f2ea;
    --paper: #ffffff;
    --surface: #f6f2ea;
    --surface-hover: #efe8da;
    --border: #ddd2bd;
    --text: #241f1a;
    --text-muted: #6b5f4d;
    --text-faint: #948a76;
    --gold: #8a6f2e;
    --gold-soft: #c89b3c;
  }
}
:root[data-theme="light"] {
  --ink: #f6f2ea;
  --paper: #ffffff;
  --surface: #f6f2ea;
  --surface-hover: #efe8da;
  --border: #ddd2bd;
  --text: #241f1a;
  --text-muted: #6b5f4d;
  --text-faint: #948a76;
  --gold: #8a6f2e;
  --gold-soft: #c89b3c;
}

* { box-sizing: border-box; }
body {
  background: var(--ink);
  color: var(--text);
  font-family: var(--sans);
  font-size: 15px;
  line-height: 1.5;
  margin: 0;
  padding: 0 20px 80px;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 980px; margin: 0 auto; }

header.top { padding: 48px 0 28px; border-bottom: 1px solid var(--border); }
header.top h1 {
  font-family: var(--serif);
  font-size: clamp(1.9rem, 4vw, 2.6rem);
  font-weight: 600;
  margin: 0 0 8px;
  text-wrap: balance;
  letter-spacing: -0.01em;
}
header.top p.sub {
  color: var(--text-muted);
  margin: 0;
  font-size: 1.02rem;
  max-width: 640px;
}
header.top .backlink {
  display: inline-block;
  margin-top: 18px;
  color: var(--gold);
  text-decoration: none;
  font-size: 0.9rem;
  border-bottom: 1px solid transparent;
}
header.top .backlink:hover { border-bottom-color: var(--gold); }

.stat-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  margin: 26px 0 0;
}
.stat {
  background: var(--surface);
  padding: 16px 14px;
  text-align: center;
}
.stat .n {
  font-family: var(--mono);
  font-variant-numeric: tabular-nums;
  font-size: 1.5rem;
  font-weight: 600;
  display: block;
}
.stat .l {
  color: var(--text-muted);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-top: 2px;
  display: block;
}
.stat.adjacent .n { color: var(--v-adjacent); }
.stat.collision .n { color: var(--v-collision); }
.stat.refuted .n { color: var(--v-refuted); }
.stat.pending .n { color: var(--v-pending); }

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin: 26px 0 18px;
  padding: 14px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
}
.controls label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-faint);
  margin-right: 4px;
}
.controls select, .controls input[type="text"] {
  background: var(--paper);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 7px 10px;
  font-family: var(--sans);
  font-size: 0.86rem;
}
.controls input[type="text"] { flex: 1; min-width: 160px; }
.controls .count { margin-left: auto; color: var(--text-faint); font-size: 0.82rem; font-variant-numeric: tabular-nums; }

.chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 9px;
  border-radius: 100px;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  white-space: nowrap;
}
.chip.v-adjacent_active { color: var(--v-adjacent); background: var(--v-adjacent-bg); }
.chip.v-collision { color: var(--v-collision); background: var(--v-collision-bg); }
.chip.v-collision-flag { color: var(--v-collision-flag); background: var(--v-collision-flag-bg); }
.chip.v-refuted { color: var(--v-refuted); background: var(--v-refuted-bg); }
.chip.v-pending_verification { color: var(--v-pending); background: var(--v-pending-bg); }
.chip.v-fact_check_fail { color: var(--v-refuted); background: var(--v-refuted-bg); }
.chip.v-other { color: var(--text-muted); background: var(--surface-hover); }
.chip.tier-chip { color: var(--gold); background: rgba(200, 155, 60, 0.12); }

.meta-panel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin: 18px 0 0;
}
.meta-block {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 18px;
}
.meta-block h3 {
  margin: 0 0 6px;
  font-size: 0.92rem;
  color: var(--text);
}
.meta-note {
  color: var(--text-muted);
  font-size: 0.78rem;
  margin: 0 0 10px;
  line-height: 1.4;
}
.meta-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}
.meta-table th, .meta-table td {
  text-align: left;
  padding: 4px 8px 4px 0;
  border-bottom: 1px solid var(--border);
  color: var(--text-muted);
}
.meta-table th {
  color: var(--text-faint);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.68rem;
  letter-spacing: 0.03em;
}
.meta-table td:first-child { color: var(--text); }
.meta-table + .meta-table { margin-top: 12px; }

.row {
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-bottom: 8px;
  background: var(--surface);
  overflow: hidden;
}
.row-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 16px;
  cursor: pointer;
  user-select: none;
}
.row-head:hover { background: var(--surface-hover); }
.row-head .rank {
  font-family: var(--mono);
  color: var(--text-faint);
  font-size: 0.82rem;
  width: 28px;
  flex-shrink: 0;
  text-align: right;
}
.row-head .pairing {
  flex: 1;
  min-width: 0;
  font-weight: 600;
  font-size: 0.94rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.row-head .mode-icon { font-size: 0.95rem; margin-right: 2px; }
.row-head .points {
  font-family: var(--mono);
  font-variant-numeric: tabular-nums;
  font-weight: 600;
  font-size: 0.94rem;
  width: 52px;
  text-align: right;
  flex-shrink: 0;
}
.row-head .points.pos { color: var(--v-adjacent); }
.row-head .points.neg { color: var(--v-refuted); }
.row-head .points.zero { color: var(--text-faint); }
.row-head .caret {
  color: var(--text-faint);
  transition: transform 0.15s ease;
  flex-shrink: 0;
  font-size: 0.75rem;
}
.row.open .caret { transform: rotate(90deg); }
.row-head .chips { display: flex; gap: 5px; flex-shrink: 0; flex-wrap: nowrap; }

.row-body {
  display: none;
  padding: 4px 20px 22px;
  border-top: 1px solid var(--border);
}
.row.open .row-body { display: block; }

.row-body h4 {
  font-family: var(--serif);
  font-size: 0.95rem;
  color: var(--gold);
  margin: 18px 0 8px;
  font-weight: 600;
}
.row-body .domains-line {
  color: var(--text-muted);
  font-size: 0.86rem;
  margin-top: 14px;
}
.badge-list { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.md-block {
  font-size: 0.88rem;
  color: var(--text);
  line-height: 1.65;
}
.md-block h1, .md-block h2 { font-family: var(--serif); font-size: 1rem; color: var(--text); margin: 14px 0 6px; }
.md-block h1:first-child, .md-block h2:first-child { margin-top: 0; }
.md-block strong { color: var(--gold); font-weight: 600; }
.md-block ul { margin: 6px 0; padding-left: 20px; }
.md-block li { margin: 3px 0; }
.md-block p { margin: 8px 0; }
.md-block table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 0.84rem; }
.md-block th, .md-block td { border: 1px solid var(--border); padding: 6px 8px; text-align: left; vertical-align: top; }
.md-block th { background: var(--surface-hover); font-weight: 600; }
.md-block hr { border: none; border-top: 1px solid var(--border); margin: 14px 0; }
.md-block code { font-family: var(--mono); font-size: 0.85em; background: var(--surface-hover); padding: 1px 5px; border-radius: 4px; }

.breakdown-list { list-style: none; padding: 0; margin: 6px 0; }
.breakdown-list li {
  font-family: var(--mono);
  font-size: 0.82rem;
  color: var(--text-muted);
  padding: 3px 0;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-faint);
}

footer.foot {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
  color: var(--text-faint);
  font-size: 0.8rem;
}

@media (max-width: 560px) {
  .row-head .chips { display: none; }
  .row-head .pairing { font-size: 0.86rem; }
}
</style>

<div class="wrap">
  <header class="top">
    <h1>The Faculty of Interdisciplinary Research</h1>
    <p class="sub">Every hypothesis the Eureka Engine has generated or verified this session — bisociation, Janusian, and homospatial thinking, run through web verification and, where the signal was ambiguous, independent adversarial refutation. Click any row to open its full record.</p>
    <a class="backlink" href="#" onclick="return false;">&larr; Referenced from the Eureka Engine whitepaper</a>
  </header>

  <div class="stat-strip" id="statStrip"></div>

  <div class="meta-panel" id="metaPanel"></div>

  <div class="controls">
    <label for="modeFilter">Mode</label>
    <select id="modeFilter"><option value="">All</option></select>
    <label for="verdictFilter">Verdict</label>
    <select id="verdictFilter"><option value="">All</option></select>
    <label for="pairTypeFilter">Pair type</label>
    <select id="pairTypeFilter"><option value="">All</option></select>
    <input type="text" id="searchBox" placeholder="Search pairings…" />
    <span class="count" id="resultCount"></span>
  </div>

  <div id="rows"></div>

  <footer class="foot">
    Generated 2026-08-28 from <code>verification-log.jsonl</code> — 40 entries, static snapshot, not a live feed. Points schema and full methodology in the accompanying whitepaper.
  </footer>
</div>

<script type="application/json" id="raw-data">__DATA_JSON__</script>
<script type="application/json" id="raw-meta">__META_JSON__</script>

<script>
(function () {
  var DATA = JSON.parse(document.getElementById('raw-data').textContent);
  var META = JSON.parse(document.getElementById('raw-meta').textContent || '{}');

  var MODE_ICON = { bisociation: '🧬', janusian: '🎭', homospatial: '🪞' };
  var MODE_LABEL = { bisociation: 'Bisociation', janusian: 'Janusian', homospatial: 'Homospatial' };

  function verdictClass(v, notValid) {
    if (!v) return 'v-other';
    var key = v.toLowerCase();
    if (key === 'collision' && notValid) return 'v-collision-flag';
    if (['adjacent_active', 'collision', 'refuted', 'pending_verification', 'fact_check_fail'].indexOf(key) >= 0) {
      return 'v-' + key;
    }
    return 'v-other';
  }
  function verdictLabel(v, notValid) {
    if (!v) return 'UNSCORED';
    if (v === 'COLLISION' && notValid) return 'COLLISION (flagged)';
    return v.replace(/_/g, ' ');
  }

  // Minimal, dependency-free markdown -> HTML for our own controlled content
  function mdToHtml(md) {
    if (!md) return '';
    var lines = md.split('\n');
    var html = [];
    var inList = false;
    var inTable = false;
    var tableRows = [];
    function flushList() { if (inList) { html.push('</ul>'); inList = false; } }
    function flushTable() {
      if (inTable) {
        var rows = tableRows.filter(function (r) { return !/^\s*\|?\s*-{2,}/.test(r); });
        html.push('<table>');
        rows.forEach(function (r, i) {
          var cells = r.split('|').map(function (c) { return c.trim(); }).filter(function (c, idx, arr) {
            return !(idx === 0 && c === '') && !(idx === arr.length - 1 && c === '');
          });
          var tag = i === 0 ? 'th' : 'td';
          html.push('<tr>' + cells.map(function (c) { return '<' + tag + '>' + inline(c) + '</' + tag + '>'; }).join('') + '</tr>');
        });
        html.push('</table>');
        inTable = false; tableRows = [];
      }
    }
    function inline(s) {
      s = s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
      s = s.replace(/`(.+?)`/g, '<code>$1</code>');
      s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
      return s;
    }
    lines.forEach(function (line) {
      if (/^\s*\|/.test(line)) {
        flushList();
        inTable = true;
        tableRows.push(line);
        return;
      } else if (inTable) {
        flushTable();
      }
      if (/^#{1,2}\s/.test(line)) {
        flushList();
        html.push('<h2>' + inline(line.replace(/^#{1,2}\s/, '')) + '</h2>');
      } else if (/^#{3,6}\s/.test(line)) {
        flushList();
        html.push('<h1>' + inline(line.replace(/^#{3,6}\s/, '')) + '</h1>');
      } else if (/^---+\s*$/.test(line)) {
        flushList();
        html.push('<hr/>');
      } else if (/^\s*[-*]\s/.test(line)) {
        if (!inList) { html.push('<ul>'); inList = true; }
        html.push('<li>' + inline(line.replace(/^\s*[-*]\s/, '')) + '</li>');
      } else if (line.trim() === '') {
        flushList();
      } else {
        flushList();
        html.push('<p>' + inline(line) + '</p>');
      }
    });
    flushList();
    flushTable();
    return html.join('\n');
  }

  function computeStats() {
    var counts = { total: DATA.length, adjacent_active: 0, collision: 0, refuted: 0, pending_verification: 0 };
    DATA.forEach(function (e) {
      var v = (e.verdict || '').toLowerCase();
      if (counts.hasOwnProperty(v)) counts[v]++;
    });
    return counts;
  }

  function renderStats() {
    var c = computeStats();
    var strip = document.getElementById('statStrip');
    var items = [
      { n: c.total, l: 'Total Entries', cls: '' },
      { n: c.adjacent_active, l: 'Frontier (Adjacent)', cls: 'adjacent' },
      { n: c.collision, l: 'Established (Collision)', cls: 'collision' },
      { n: c.refuted, l: 'Refuted', cls: 'refuted' },
      { n: c.pending_verification, l: 'Pending', cls: 'pending' }
    ];
    strip.innerHTML = items.map(function (it) {
      return '<div class="stat ' + it.cls + '"><span class="n">' + it.n + '</span><span class="l">' + it.l + '</span></div>';
    }).join('');
  }

  function renderMeta() {
    var panel = document.getElementById('metaPanel');
    var modePerf = META.mode_performance || [];
    var corr = META.prefilter_correlation || {};
    var pairTypeRows = corr.pair_type || [];
    var recRows = corr.recommendation || [];
    if (!modePerf.length && !pairTypeRows.length) { panel.innerHTML = ''; return; }

    var html = '';
    if (modePerf.length) {
      html += '<div class="meta-block"><h3>Department performance</h3>' +
        '<p class="meta-note">Real, live per-mode averages — a high NO_SIGNAL rate isn\'t a mode failing, ' +
        'it\'s that mode\'s real base rate for reaching a novel, unresolved claim.</p>' +
        '<table class="meta-table"><tr><th>Mode</th><th>n</th><th>Avg pts</th><th>NO_SIGNAL rate</th></tr>' +
        modePerf.map(function (r) {
          return '<tr><td>' + (MODE_LABEL[r.mode] || r.mode) + '</td><td>' + r.n + '</td><td>' +
            (r.avg_points >= 0 ? '+' : '') + r.avg_points + '</td><td>' + Math.round(r.no_signal_rate * 100) + '%</td></tr>';
        }).join('') + '</table></div>';
    }
    if (pairTypeRows.length || recRows.length) {
      html += '<div class="meta-block"><h3>Pre-filter signal (Phase 0.5, observe-only)</h3>' +
        '<p class="meta-note">Never gates generation, only logs a signal. Live correlation with real downstream outcome, joined fresh every run.</p>';
      if (pairTypeRows.length) {
        html += '<table class="meta-table"><tr><th>Pair type</th><th>n</th><th>Good outcome</th></tr>' +
          pairTypeRows.map(function (r) {
            return '<tr><td>' + r.key + '</td><td>' + r.n + '</td><td>' + r.rate_pct + '%</td></tr>';
          }).join('') + '</table>';
      }
      if (recRows.length) {
        html += '<table class="meta-table"><tr><th>Recommendation</th><th>n</th><th>Good outcome</th></tr>' +
          recRows.map(function (r) {
            return '<tr><td>' + r.key.replace(/_/g, ' ') + '</td><td>' + r.n + '</td><td>' + r.rate_pct + '%</td></tr>';
          }).join('') + '</table>';
      }
      html += '</div>';
    }
    panel.innerHTML = html;
  }

  function populateFilters() {
    var modes = Array.from(new Set(DATA.map(function (e) { return e.mode; }).filter(Boolean))).sort();
    var verdicts = Array.from(new Set(DATA.map(function (e) { return e.verdict; }).filter(Boolean))).sort();
    var pairTypes = Array.from(new Set(DATA.map(function (e) { return e.pair_type; }).filter(Boolean))).sort();
    var modeSel = document.getElementById('modeFilter');
    modes.forEach(function (m) {
      var o = document.createElement('option');
      o.value = m; o.textContent = MODE_LABEL[m] || m;
      modeSel.appendChild(o);
    });
    var vSel = document.getElementById('verdictFilter');
    verdicts.forEach(function (v) {
      var o = document.createElement('option');
      o.value = v; o.textContent = v.replace(/_/g, ' ');
      vSel.appendChild(o);
    });
    var ptSel = document.getElementById('pairTypeFilter');
    pairTypes.forEach(function (pt) {
      var o = document.createElement('option');
      o.value = pt; o.textContent = pt;
      ptSel.appendChild(o);
    });
  }

  function pairingName(e) {
    return (e.domains && e.domains.length) ? e.domains.join(' × ') : e.key;
  }

  function badgeChips(e) {
    return (e.badges || []).map(function (b) {
      return '<span class="chip v-other" style="background:transparent;border:1px solid var(--border);color:var(--text-muted)">' + b + '</span>';
    }).join(' ');
  }

  function renderRowBody(e) {
    var out = '';
    out += '<div class="domains-line"><strong style="color:var(--text)">Domains:</strong> ' + (e.domains || []).join(' &times; ') + '</div>';
    out += '<div class="badge-list">' + badgeChips(e) + '</div>';

    if (e.breakdown && e.breakdown.length) {
      out += '<h4>Score breakdown (' + (e.points >= 0 ? '+' : '') + e.points + ' pts)</h4>';
      out += '<ul class="breakdown-list">' + e.breakdown.map(function (b) { return '<li>' + b.replace(/</g, '&lt;') + '</li>'; }).join('') + '</ul>';
    }
    if (e.notes) {
      out += '<h4>Notes</h4><div class="md-block">' + mdToHtml(e.notes) + '</div>';
    }
    if (e.hypothesis_content) {
      out += '<h4>The Hypothesis</h4><div class="md-block">' + mdToHtml(e.hypothesis_content) + '</div>';
    }
    if (e.verification_content) {
      out += '<h4>Phase 2 Verification</h4><div class="md-block">' + mdToHtml(e.verification_content) + '</div>';
    }
    if (e.refutation_content) {
      out += '<h4>Adversarial Refutation' + (e.refutation_independently_confirmed ? ' (independently confirmed)' : '') + '</h4><div class="md-block">' + mdToHtml(e.refutation_content) + '</div>';
    }
    return out;
  }

  function render() {
    var mode = document.getElementById('modeFilter').value;
    var verdict = document.getElementById('verdictFilter').value;
    var pairType = document.getElementById('pairTypeFilter').value;
    var q = document.getElementById('searchBox').value.trim().toLowerCase();

    var filtered = DATA.filter(function (e) {
      if (mode && e.mode !== mode) return false;
      if (verdict && e.verdict !== verdict) return false;
      if (pairType && e.pair_type !== pairType) return false;
      if (q && pairingName(e).toLowerCase().indexOf(q) === -1) return false;
      return true;
    });
    // Tier first (real confidence signal — Peer-Endorsed > Survived
    // Refutation > Verified/Unrefuted > Pending > Refuted/Rejected), points
    // as a tie-breaker within a tier only. A missing tier_rank (held-out,
    // non-standard verdict) sorts last. 2026-08-31, leaderboard rearchitecture.
    filtered.sort(function (a, b) {
      var ta = (a.tier_rank == null) ? 99 : a.tier_rank;
      var tb = (b.tier_rank == null) ? 99 : b.tier_rank;
      if (ta !== tb) return ta - tb;
      return (b.points || 0) - (a.points || 0);
    });

    document.getElementById('resultCount').textContent = filtered.length + ' of ' + DATA.length;

    var container = document.getElementById('rows');
    if (!filtered.length) {
      container.innerHTML = '<div class="empty-state">No hypotheses match these filters.</div>';
      return;
    }

    container.innerHTML = filtered.map(function (e, i) {
      var vClass = verdictClass(e.verdict, e.not_valid_bisociation);
      var vLabel = verdictLabel(e.verdict, e.not_valid_bisociation);
      var ptsClass = (e.points > 0 ? 'pos' : e.points < 0 ? 'neg' : 'zero');
      var rowId = 'row-' + i;
      return (
        '<div class="row" id="' + rowId + '">' +
          '<div class="row-head" onclick="window.__toggleRow(\'' + rowId + '\')">' +
            '<span class="rank">' + (i + 1) + '</span>' +
            '<span class="mode-icon">' + (MODE_ICON[e.mode] || '📜') + '</span>' +
            '<span class="pairing">' + pairingName(e).replace(/</g, '&lt;') + '</span>' +
            '<span class="chips">' +
              (e.tier_label ? '<span class="chip tier-chip" title="Confidence tier">' + e.tier_label + '</span>' : '') +
              '<span class="chip ' + vClass + '">' + vLabel + '</span>' +
            '</span>' +
            '<span class="points ' + ptsClass + '">' + (e.points > 0 ? '+' : '') + e.points + '</span>' +
            '<span class="caret">▶</span>' +
          '</div>' +
          '<div class="row-body">' + renderRowBody(e) + '</div>' +
        '</div>'
      );
    }).join('');
  }

  window.__toggleRow = function (id) {
    var el = document.getElementById(id);
    if (el) el.classList.toggle('open');
  };

  document.getElementById('modeFilter').addEventListener('change', render);
  document.getElementById('verdictFilter').addEventListener('change', render);
  document.getElementById('pairTypeFilter').addEventListener('change', render);
  document.getElementById('searchBox').addEventListener('input', render);

  renderStats();
  renderMeta();
  populateFilters();
  render();
})();
</script>
'''

html = html.replace('__DATA_JSON__', data_json_safe)
html = html.replace('__META_JSON__', meta_json_safe)

with open("leaderboard-experience.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote leaderboard-experience.html ({len(html)/1024:.1f} KB)")
