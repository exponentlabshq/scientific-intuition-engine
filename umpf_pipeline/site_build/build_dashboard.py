#!/usr/bin/env python3
"""
build_dashboard.py — The Eureka Engine's live operations dashboard.

Fully automated, unlike landing.html: everything on this page is real,
computed data (verdict distribution, mode performance, ROTI, the last
cycle's actual phase-by-phase journey, the audit agent's running
commentary) -- no hand-written narrative prose to preserve, so
publish_site.py can safely rebuild this one every cycle the same way it
already does leaderboard-experience.html.

Data sources, all real, none invented:
  - ../verification-log.jsonl   (ledger -- verdicts, points, badges)
  - ../token_usage.jsonl        (real ROTI -- tokens per phase, per call)
  - ../cycle_log.jsonl          (the last cycle's real per-stage outcome,
                                  drives the phase-flow replay animation)
  - ../audit_observations.jsonl (the audit agent's lightweight per-cycle
                                  commentary)
  - ../proposals/, ../audit_log.jsonl (the latest deep, grounded proposal)

Run from site_build/ (matches build_landing.py's own convention):
    python3 build_dashboard.py     # writes ./dashboard.html
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone

PIPELINE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PIPELINE_DIR)

from score_hypotheses import load_entries, score_entry, CANONICAL_VERDICTS  # noqa: E402
from token_tracker import summarize_by_phase, load_usage  # noqa: E402

MODES = ["bisociation", "janusian", "homospatial"]
MODE_LABEL = {"bisociation": "Bisociation", "janusian": "Janusian", "homospatial": "Homospatial", "case-study": "Pre-existing"}

# Same published-rate assumptions used in the ROTI audit turn this session,
# kept here rather than re-guessed: gpt-4o-mini ~$0.15/$0.60 per 1M
# input/output tokens, gpt-4o ~$2.50/$10.00. Applied per-phase using each
# phase's real logged model.
PRICE_PER_1M = {
    "gpt-4o-mini": {"in": 0.15, "out": 0.60},
    "gpt-4o": {"in": 2.50, "out": 10.00},
}
# Claude subagent tokens per refutation lens, measured directly from this
# session's own real subagent_tokens figures before refute_hypothesis.py
# existed -- the real number the "tokens avoided" comparison is built on.
CLAUDE_TOKENS_PER_LENS = 34700


def b64(path):
    import base64
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def compute_dashboard_data():
    entries = load_entries()

    verdict_counts = defaultdict(int)
    mode_stats = defaultdict(lambda: {"n": 0, "points": 0, "no_signal": 0})
    scored_rows = []
    for e in entries:
        v = e.get("verdict", "")
        canonical_v = v if v in CANONICAL_VERDICTS else ("REFUTED" if e.get("refutation_verdict") == "REFUTED" else "OTHER")
        if e.get("refutation_verdict") == "REFUTED":
            verdict_counts["REFUTED"] += 1
        elif v in ("COLLISION", "ADJACENT_ACTIVE", "FACT_CHECK_FAIL"):
            verdict_counts[v] += 1
        elif v == "NO_SIGNAL":
            verdict_counts["NO_SIGNAL_UNRESOLVED"] += 1
        else:
            verdict_counts["OTHER"] += 1

        mode = e.get("mode") or ("case-study" if e.get("source") == "rosetta-stone-case-study" else "other")
        points, badges, breakdown, held_out = score_entry(e)
        if held_out is None:
            mode_stats[mode]["n"] += 1
            mode_stats[mode]["points"] += points
            if v == "NO_SIGNAL":
                mode_stats[mode]["no_signal"] += 1
            domains_str = " × ".join(e.get("domains", [])) or e.get("hypothesis_slug", e.get("case_study", "?"))
            scored_rows.append({"domains": domains_str, "points": points, "verdict": v, "badges": badges, "mode": mode})

    scored_rows.sort(key=lambda r: r["points"], reverse=True)
    top5 = scored_rows[:5]

    mode_summary = []
    for m in MODES + ["case-study"]:
        s = mode_stats.get(m)
        if not s or s["n"] == 0:
            continue
        mode_summary.append({
            "mode": m,
            "label": MODE_LABEL.get(m, m),
            "n": s["n"],
            "avg_points": round(s["points"] / s["n"], 1),
            "no_signal_rate": round(s["no_signal"] / s["n"], 2),
        })

    # --- ROTI: real tokens per phase, real estimated cost ---
    usage = load_usage()
    by_phase = defaultdict(lambda: {"n_calls": 0, "prompt": 0, "completion": 0, "models": defaultdict(int)})
    for r in usage:
        p = r.get("phase", "unknown")
        by_phase[p]["n_calls"] += 1
        by_phase[p]["prompt"] += r.get("prompt_tokens") or 0
        by_phase[p]["completion"] += r.get("completion_tokens") or 0
        by_phase[p]["models"][r.get("model", "?")] += 1

    roti_phases = []
    total_cost = 0.0
    total_tokens = 0
    for phase, d in sorted(by_phase.items()):
        model = max(d["models"], key=d["models"].get) if d["models"] else "?"
        price = PRICE_PER_1M.get(model, {"in": 0, "out": 0})
        cost = (d["prompt"] / 1_000_000) * price["in"] + (d["completion"] / 1_000_000) * price["out"]
        total_cost += cost
        total_tokens += d["prompt"] + d["completion"]
        roti_phases.append({
            "phase": phase,
            "model": model,
            "n_calls": d["n_calls"],
            "total_tokens": d["prompt"] + d["completion"],
            "avg_tokens": round((d["prompt"] + d["completion"]) / d["n_calls"]) if d["n_calls"] else 0,
            "cost": round(cost, 4),
        })

    refutation_calls = by_phase.get("refutation", {}).get("n_calls", 0)
    claude_tokens_avoided = refutation_calls * CLAUDE_TOKENS_PER_LENS
    real_refutation_tokens = by_phase.get("refutation", {}).get("prompt", 0) + by_phase.get("refutation", {}).get("completion", 0)

    total_points = sum(r["points"] for r in scored_rows)
    tokens_per_point = round(total_tokens / total_points, 1) if total_points else None

    # --- Last cycle: the real phase-by-phase journey to replay ---
    last_cycle = None
    cycle_history = []
    cycle_log_path = os.path.join(PIPELINE_DIR, "cycle_log.jsonl")
    if os.path.exists(cycle_log_path):
        with open(cycle_log_path, "r", encoding="utf-8") as f:
            cycles = [json.loads(l) for l in f if l.strip() and not json.loads(l).get("dry_run")]
        if cycles:
            last_cycle = cycles[-1]
            cycle_history = cycles[-12:]  # last 12 real cycles for a trend view

    def stage_summary(cycle, stage_name):
        if not cycle or stage_name not in cycle.get("stages", {}):
            return {"ran": False}
        s = cycle["stages"][stage_name]
        if isinstance(s, list):
            ok = all(r.get("returncode", 0) == 0 for r in s)
            return {"ran": True, "ok": ok}
        return {"ran": True, "ok": s.get("returncode", 0) == 0}

    last_cycle_summary = None
    if last_cycle:
        last_cycle_summary = {
            "timestamp": last_cycle.get("timestamp"),
            "status": last_cycle.get("status", "unknown"),
            "generated": len(last_cycle.get("new_hypothesis_files", [])),
            "plan": last_cycle.get("plan", {}),
            "stages": {
                "generation": stage_summary(last_cycle, "generation"),
                "verification": stage_summary(last_cycle, "verification"),
                "refutation": stage_summary(last_cycle, "refutation"),
                "scoring": stage_summary(last_cycle, "scoring"),
                "publish": stage_summary(last_cycle, "publish"),
            },
            "degraded_reasons": last_cycle.get("degraded_reasons", []),
        }

    cycle_trend = [{"timestamp": c.get("timestamp"), "status": c.get("status", "unknown"),
                     "generated": len(c.get("new_hypothesis_files", []))} for c in cycle_history]

    # --- Audit commentary ---
    observations = []
    obs_path = os.path.join(PIPELINE_DIR, "audit_observations.jsonl")
    if os.path.exists(obs_path):
        with open(obs_path, "r", encoding="utf-8") as f:
            all_obs = [json.loads(l) for l in f if l.strip()]
        observations = [{"timestamp": o["timestamp"], "text": o["observation"]} for o in all_obs[-8:]][::-1]

    latest_proposal = None
    audit_log_path = os.path.join(PIPELINE_DIR, "audit_log.jsonl")
    if os.path.exists(audit_log_path):
        with open(audit_log_path, "r", encoding="utf-8") as f:
            audits = [json.loads(l) for l in f if l.strip()]
        if audits:
            a = audits[-1]
            proposal_file = os.path.join(PIPELINE_DIR, "proposals", a.get("proposal_file", ""))
            rationale = ""
            if a.get("proposal_file") and os.path.exists(proposal_file):
                text = open(proposal_file, encoding="utf-8").read()
                m = text.split("## Rationale", 1)
                if len(m) > 1:
                    rationale = m[1].split("##", 1)[0].strip()
            latest_proposal = {
                "title": a.get("title", "Untitled"),
                "proposal_file": a.get("proposal_file"),
                "code_file": a.get("code_file"),
                "rationale": rationale[:600],
            }

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_hypotheses": len(entries),
        "verdict_counts": dict(verdict_counts),
        "mode_summary": mode_summary,
        "top5": top5,
        "roti_phases": roti_phases,
        "total_cost": round(total_cost, 2),
        "total_tokens": total_tokens,
        "tokens_per_point": tokens_per_point,
        "total_points": total_points,
        "claude_tokens_avoided": claude_tokens_avoided,
        "real_refutation_tokens": real_refutation_tokens,
        "last_cycle": last_cycle_summary,
        "cycle_trend": cycle_trend,
        "observations": observations,
        "latest_proposal": latest_proposal,
    }


DATA = compute_dashboard_data()

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="robots" content="noindex, nofollow" />
<title>The Eureka Engine — Live Operations</title>
<style>
:root {
  --ink: #14110f; --surface: #241f1a; --surface-2: #2c261f; --border: #3a3229;
  --text: #ede6d8; --text-muted: #a89a86; --text-faint: #6f6455;
  --gold: #c89b3c; --gold-bright: #e0b954;
  --v-adjacent: #5fa88f; --v-collision: #6f93bd; --v-refuted: #b56b6b; --v-pending: #8a8577;
  --serif: ui-serif, Georgia, 'Iowan Old Style', 'Times New Roman', serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Inter', ui-sans-serif, 'Segoe UI', sans-serif;
  --mono: ui-monospace, 'SF Mono', Menlo, monospace;
}
* { box-sizing: border-box; }
body {
  background: var(--ink); color: var(--text); font-family: var(--sans);
  font-size: 16px; line-height: 1.6; margin: 0; padding: 0 20px 80px;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 1180px; margin: 0 auto; position: relative; }

/* ambient background, same visual family as the landing hero's collision motif */
.ambient {
  position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background:
    radial-gradient(600px circle at 15% 10%, rgba(200,155,60,0.08), transparent 60%),
    radial-gradient(500px circle at 90% 30%, rgba(95,168,143,0.05), transparent 60%);
}

header.top { padding: 48px 0 28px; border-bottom: 2px solid var(--gold); }
header.top .kicker {
  font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.14em;
  color: var(--gold); font-size: 0.76rem; margin-bottom: 12px;
}
header.top h1 {
  font-family: var(--serif); font-weight: 600; font-size: clamp(1.8rem, 4vw, 2.6rem);
  margin: 0 0 12px; text-wrap: balance;
}
header.top .mission {
  color: var(--text-muted); font-size: 1.02rem; max-width: 720px; margin: 0;
}
.live-dot {
  display: inline-block; width: 8px; height: 8px; border-radius: 50%;
  background: var(--v-adjacent); margin-right: 8px; vertical-align: middle;
  animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }

/* headline stat row */
.stat-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 32px 0; }
.stat-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
  padding: 22px 24px; opacity: 0; transform: translateY(10px);
  animation: rise 0.5s ease-out forwards;
}
.stat-card .n {
  font-family: var(--serif); font-size: 2.2rem; font-weight: 600; color: var(--gold);
  font-variant-numeric: tabular-nums; line-height: 1;
}
.stat-card .l { color: var(--text-muted); font-size: 0.86rem; margin-top: 8px; }
@keyframes rise { to { opacity: 1; transform: translateY(0); } }

section.block { margin: 48px 0; }
section.block h2 {
  font-family: var(--serif); font-size: 1.35rem; font-weight: 600; margin: 0 0 6px;
}
section.block .sub { color: var(--text-faint); font-size: 0.88rem; margin: 0 0 20px; font-family: var(--mono); }

/* pipeline flow replay */
.pipeline-flow {
  display: flex; align-items: center; justify-content: space-between; gap: 4px;
  background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
  padding: 28px 20px; overflow-x: auto;
}
.pf-node { display: flex; flex-direction: column; align-items: center; gap: 10px; min-width: 110px; position: relative; }
.pf-circle {
  width: 52px; height: 52px; border-radius: 50%; border: 2px solid var(--border);
  background: var(--ink); display: flex; align-items: center; justify-content: center;
  font-size: 1.3rem; transition: all 0.4s ease; opacity: 0.4;
}
.pf-circle.active { border-color: var(--gold); background: rgba(200,155,60,0.12); opacity: 1; transform: scale(1.08); box-shadow: 0 0 0 4px rgba(200,155,60,0.15); }
.pf-circle.fail { border-color: var(--v-refuted); background: rgba(181,107,107,0.14); opacity: 1; }
.pf-label { font-family: var(--mono); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); text-align: center; }
.pf-value { font-family: var(--serif); font-size: 1rem; color: var(--gold); font-weight: 600; min-height: 1.2em; }
.pf-line { flex: 1; height: 2px; background: var(--border); margin: 0 -4px 32px; position: relative; min-width: 24px; }
.pf-line .fill { position: absolute; inset: 0; background: var(--gold); width: 0%; transition: width 0.6s ease; }

/* card grid */
.grid-2 { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 20px; align-items: start; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; align-items: start; }
@media (max-width: 860px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 22px 24px; }
.card h3 { font-family: var(--serif); font-size: 1.05rem; margin: 0 0 16px; font-weight: 600; }

/* verdict distribution bars */
.vbar-row { display: flex; align-items: center; gap: 12px; margin: 10px 0; }
.vbar-label { width: 130px; font-family: var(--mono); font-size: 0.78rem; color: var(--text-muted); flex-shrink: 0; }
.vbar-track { flex: 1; height: 20px; background: var(--ink); border-radius: 6px; overflow: hidden; }
.vbar-fill { height: 100%; width: 0%; border-radius: 6px; transition: width 1s cubic-bezier(0.16,1,0.3,1); }
.vbar-n { width: 34px; text-align: right; font-family: var(--mono); font-size: 0.82rem; color: var(--text); font-variant-numeric: tabular-nums; }

/* mode performance */
.mode-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid var(--border); }
.mode-row:last-child { border-bottom: none; }
.mode-name { font-family: var(--mono); font-size: 0.88rem; }
.mode-metrics { display: flex; gap: 18px; font-family: var(--mono); font-size: 0.82rem; color: var(--text-muted); }
.mode-metrics .hi { color: var(--gold); }

/* leaderboard snippet */
.lb-row { display: flex; justify-content: space-between; align-items: center; padding: 9px 0; border-bottom: 1px solid var(--border); gap: 12px; }
.lb-row:last-child { border-bottom: none; }
.lb-domains { font-size: 0.9rem; }
.lb-points { font-family: var(--mono); font-weight: 600; color: var(--gold); flex-shrink: 0; }

/* ROTI */
.roti-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.roti-table th, .roti-table td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border); }
.roti-table th { font-family: var(--mono); text-transform: uppercase; font-size: 0.68rem; letter-spacing: 0.04em; color: var(--gold); }
.roti-table td.num, .roti-table th.num { text-align: right; font-family: var(--mono); font-variant-numeric: tabular-nums; }
.roti-callout {
  margin-top: 16px; padding: 14px 16px; background: rgba(200,155,60,0.08);
  border-left: 3px solid var(--gold); border-radius: 0 8px 8px 0; font-size: 0.88rem;
}

/* audit commentary feed */
.feed-item { padding: 12px 0; border-bottom: 1px solid var(--border); font-size: 0.88rem; }
.feed-item:last-child { border-bottom: none; }
.feed-item .ts { font-family: var(--mono); font-size: 0.7rem; color: var(--text-faint); display: block; margin-bottom: 4px; }
.feed-item.newest { position: relative; padding-left: 14px; }
.feed-item.newest::before { content: ''; position: absolute; left: 0; top: 16px; width: 6px; height: 6px; border-radius: 50%; background: var(--v-adjacent); animation: pulse-dot 2s ease-in-out infinite; }

.proposal-card { border-color: var(--gold); }
.proposal-card .status-chip {
  display: inline-block; font-family: var(--mono); font-size: 0.68rem; text-transform: uppercase;
  letter-spacing: 0.05em; color: var(--v-pending); background: rgba(138,133,119,0.16);
  padding: 2px 8px; border-radius: 100px; margin-bottom: 10px;
}

.cta-row { display: flex; gap: 14px; margin-top: 12px; flex-wrap: wrap; }
.cta-btn {
  display: inline-flex; align-items: center; gap: 8px; font-family: var(--mono); font-size: 0.8rem;
  text-transform: uppercase; letter-spacing: 0.05em; color: var(--ink); background: var(--gold);
  padding: 10px 18px; border-radius: 8px; text-decoration: none;
}
.cta-btn.secondary { background: transparent; color: var(--gold-bright); border: 1px solid var(--gold); }

@media (prefers-reduced-motion: reduce) {
  .stat-card { animation: none; opacity: 1; transform: none; }
  .live-dot, .feed-item.newest::before { animation: none; }
  .pf-circle, .vbar-fill, .pf-line .fill { transition: none; }
}

.site-nav {
  position: sticky; top: 0; z-index: 200;
  background: rgba(20,17,15,0.94); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border); margin: 0 -20px;
}
.site-nav-inner {
  max-width: 1180px; margin: 0 auto; padding: 14px 24px;
  display: flex; align-items: center; justify-content: space-between; gap: 20px;
}
.site-nav-brand { font-family: var(--serif); font-size: 1rem; color: var(--gold); text-decoration: none; font-weight: 600; white-space: nowrap; }
.site-nav-links { display: flex; gap: 24px; }
.site-nav-links a {
  font-family: var(--mono); font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--text-muted); text-decoration: none; transition: color 0.15s; white-space: nowrap;
}
.site-nav-links a:hover { color: var(--gold); }
.site-nav-links a.is-active { color: var(--gold); border-bottom: 1px solid var(--gold); padding-bottom: 2px; }
@media (max-width: 560px) {
  .site-nav-inner { padding: 12px 16px; } .site-nav-links { gap: 14px; }
  .site-nav-brand { font-size: 0.88rem; } .site-nav-links a { font-size: 0.68rem; }
}
</style>
</head>
<body>
<nav class="site-nav">
  <div class="site-nav-inner">
    <a class="site-nav-brand" href="landing.html">The Eureka Engine</a>
    <div class="site-nav-links">
      <a href="landing.html">Home</a>
      <a href="dashboard.html" class="is-active">Dashboard</a>
      <a href="whitepaper.html">Whitepaper</a>
      <a href="leaderboard.html">Leaderboard</a>
    </div>
  </div>
</nav>
<div class="ambient"></div>
<div class="wrap">

  <header class="top">
    <div class="kicker"><span class="live-dot"></span>Exponent Labs LLC &middot; Faculty of Interdisciplinary Research</div>
    <h1>The Eureka Engine — Live Operations</h1>
    <p class="mission">A research department whose entire job is to tell you before you spend the time, not after. Every hypothesis below is a question a real Master's or PhD researcher could have spent months answering by hand &mdash; checked here in minutes, in the open, wrong answers included.</p>
  </header>

  <div class="stat-row" id="stat-row"></div>

  <section class="block">
    <h2>Last Cycle — What Actually Ran</h2>
    <p class="sub" id="last-cycle-meta">loading…</p>
    <div class="pipeline-flow" id="pipeline-flow"></div>
  </section>

  <section class="block grid-2">
    <div class="card">
      <h3>Leaderboard — Top 5</h3>
      <div id="leaderboard-snippet"></div>
      <div class="cta-row">
        <a class="cta-btn" href="leaderboard.html">Full Leaderboard &rarr;</a>
      </div>
    </div>
    <div class="card">
      <h3>Verdict Distribution</h3>
      <div id="verdict-bars"></div>
    </div>
  </section>

  <section class="block grid-2">
    <div class="card">
      <h3>Mode Performance</h3>
      <div id="mode-performance"></div>
    </div>
    <div class="card">
      <h3>Return on Token Investment</h3>
      <div id="roti-table"></div>
      <div class="roti-callout" id="roti-callout"></div>
    </div>
  </section>

  <section class="block grid-2">
    <div class="card">
      <h3>Audit Agent — Running Commentary</h3>
      <div id="observations-feed"></div>
    </div>
    <div class="card proposal-card" id="proposal-card">
      <div class="status-chip">Unreviewed proposal</div>
      <h3 id="proposal-title">No proposal yet</h3>
      <p id="proposal-rationale" style="color: var(--text-muted); font-size: 0.88rem;"></p>
    </div>
  </section>

</div>

<script>
const DATA = __DATA_JSON__;

function animateCount(el, target, duration=900) {
  const start = performance.now();
  const isFloat = target % 1 !== 0;
  function tick(now) {
    const p = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    const val = target * eased;
    el.textContent = isFloat ? val.toFixed(1) : Math.round(val).toLocaleString();
    if (p < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// --- Headline stats ---
const statRow = document.getElementById('stat-row');
const headline = [
  { n: DATA.total_hypotheses, l: 'Hypotheses Checked' },
  { n: (DATA.verdict_counts.COLLISION||0) + (DATA.verdict_counts.REFUTED||0) + (DATA.verdict_counts.FACT_CHECK_FAIL||0), l: 'Dead Ends Caught Before A Human Would Spend Time' },
  { n: DATA.verdict_counts.ADJACENT_ACTIVE||0, l: 'Genuinely Worth Pursuing' },
  { n: DATA.total_cost, l: 'Total OpenAI Cost ($)', money: true },
];
headline.forEach((s, i) => {
  const card = document.createElement('div');
  card.className = 'stat-card';
  card.style.animationDelay = (i * 0.08) + 's';
  card.innerHTML = `<div class="n">${s.money ? '$0' : '0'}</div><div class="l">${s.l}</div>`;
  statRow.appendChild(card);
  const numEl = card.querySelector('.n');
  if (reducedMotion) {
    numEl.textContent = s.money ? '$' + s.n.toFixed(2) : s.n.toLocaleString();
  } else {
    setTimeout(() => {
      if (s.money) {
        const start = performance.now();
        function tick(now) {
          const p = Math.min((now - start) / 900, 1);
          numEl.textContent = '$' + (s.n * (1 - Math.pow(1-p,3))).toFixed(2);
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      } else {
        animateCount(numEl, s.n);
      }
    }, i * 80 + 200);
  }
});

// --- Pipeline flow replay ---
const flow = document.getElementById('pipeline-flow');
const meta = document.getElementById('last-cycle-meta');
const STAGE_ICONS = { generation: '🧬', verification: '🔍', refutation: '⚖️', scoring: '🏆', publish: '📡' };
const STAGE_LABELS = { generation: 'Generate', verification: 'Verify', refutation: 'Refute', scoring: 'Score', publish: 'Publish' };

if (DATA.last_cycle) {
  const lc = DATA.last_cycle;
  const when = new Date(lc.timestamp);
  meta.textContent = `${when.toLocaleString()} · plan: ${Object.entries(lc.plan).map(([m,c]) => `${c} ${m}`).join(', ')} · status: ${lc.status}`;

  const stageKeys = ['generation','verification','refutation','scoring','publish'];
  stageKeys.forEach((key, i) => {
    const st = lc.stages[key] || { ran: false };
    const node = document.createElement('div');
    node.className = 'pf-node';
    const value = key === 'generation' ? lc.generated : '';
    node.innerHTML = `
      <div class="pf-circle" data-idx="${i}">${STAGE_ICONS[key]}</div>
      <div class="pf-label">${STAGE_LABELS[key]}</div>
      <div class="pf-value">${value !== '' ? value : ''}</div>
    `;
    flow.appendChild(node);
    if (i < stageKeys.length - 1) {
      const line = document.createElement('div');
      line.className = 'pf-line';
      line.innerHTML = '<div class="fill"></div>';
      flow.appendChild(line);
    }
  });

  const circles = flow.querySelectorAll('.pf-circle');
  const lines = flow.querySelectorAll('.pf-line .fill');
  const delay = reducedMotion ? 0 : 380;
  stageKeys.forEach((key, i) => {
    const st = lc.stages[key] || { ran: false };
    setTimeout(() => {
      if (st.ran) {
        circles[i].classList.add(st.ok === false ? 'fail' : 'active');
      }
      if (i > 0 && lines[i-1]) lines[i-1].style.width = '100%';
    }, i * delay);
  });
} else {
  meta.textContent = 'No cycle has run yet.';
}

// --- Leaderboard snippet ---
const lbEl = document.getElementById('leaderboard-snippet');
DATA.top5.forEach(row => {
  const div = document.createElement('div');
  div.className = 'lb-row';
  div.innerHTML = `<span class="lb-domains">${row.domains}</span><span class="lb-points">${row.points > 0 ? '+' : ''}${row.points}</span>`;
  lbEl.appendChild(div);
});

// --- Verdict distribution ---
const VERDICT_META = {
  ADJACENT_ACTIVE: { label: 'Adjacent Active', color: 'var(--v-adjacent)' },
  COLLISION: { label: 'Collision', color: 'var(--v-collision)' },
  REFUTED: { label: 'Refuted', color: 'var(--v-refuted)' },
  FACT_CHECK_FAIL: { label: 'Fact-Check Fail', color: 'var(--v-refuted)' },
  NO_SIGNAL_UNRESOLVED: { label: 'Pending Refutation', color: 'var(--v-pending)' },
  OTHER: { label: 'Flagged', color: 'var(--v-pending)' },
};
const vbarEl = document.getElementById('verdict-bars');
const maxV = Math.max(...Object.values(DATA.verdict_counts));
const sortedVerdicts = Object.entries(DATA.verdict_counts).sort((a, b) => b[1] - a[1]);
sortedVerdicts.forEach(([key, count]) => {
  if (!count) return;
  const meta = VERDICT_META[key] || { label: key, color: 'var(--text-faint)' };
  const row = document.createElement('div');
  row.className = 'vbar-row';
  row.innerHTML = `<span class="vbar-label">${meta.label}</span><div class="vbar-track"><div class="vbar-fill" style="background:${meta.color}"></div></div><span class="vbar-n">${count}</span>`;
  vbarEl.appendChild(row);
  const fill = row.querySelector('.vbar-fill');
  setTimeout(() => { fill.style.width = (count / maxV * 100) + '%'; }, 150);
});

// --- Mode performance ---
const modeEl = document.getElementById('mode-performance');
DATA.mode_summary.forEach(m => {
  const row = document.createElement('div');
  row.className = 'mode-row';
  row.innerHTML = `<span class="mode-name">${m.label}</span><span class="mode-metrics"><span>n=${m.n}</span><span class="hi">${m.avg_points} avg pts</span><span>${Math.round(m.no_signal_rate*100)}% no-signal</span></span>`;
  modeEl.appendChild(row);
});

// --- ROTI table ---
const rotiEl = document.getElementById('roti-table');
let tbl = '<table class="roti-table"><tr><th>Phase</th><th class="num">Calls</th><th class="num">Avg Tokens</th><th class="num">Cost</th></tr>';
DATA.roti_phases.forEach(p => {
  tbl += `<tr><td>${p.phase}</td><td class="num">${p.n_calls}</td><td class="num">${p.avg_tokens.toLocaleString()}</td><td class="num">$${p.cost.toFixed(4)}</td></tr>`;
});
tbl += '</table>';
rotiEl.innerHTML = tbl;

const callout = document.getElementById('roti-callout');
if (DATA.claude_tokens_avoided > 0) {
  callout.textContent = `Refutation now runs on OpenAI instead of Claude subagents: ${DATA.real_refutation_tokens.toLocaleString()} real tokens spent vs. an estimated ${DATA.claude_tokens_avoided.toLocaleString()} Claude tokens the same work would have cost under the old architecture — measured, not guessed, from this session's own real subagent token counts.`;
} else {
  callout.textContent = `Tokens per leaderboard point, pool-wide: ${DATA.tokens_per_point ?? '—'}.`;
}

// --- Audit commentary feed ---
const feedEl = document.getElementById('observations-feed');
if (DATA.observations.length === 0) {
  feedEl.innerHTML = '<p style="color: var(--text-faint); font-size: 0.88rem;">No observations logged yet — runs automatically every cycle.</p>';
} else {
  DATA.observations.forEach((o, i) => {
    const div = document.createElement('div');
    div.className = 'feed-item' + (i === 0 ? ' newest' : '');
    const when = new Date(o.timestamp);
    div.innerHTML = `<span class="ts">${when.toLocaleString()}</span>${o.text}`;
    feedEl.appendChild(div);
  });
}

// --- Latest deep proposal ---
if (DATA.latest_proposal) {
  document.getElementById('proposal-title').textContent = DATA.latest_proposal.title;
  document.getElementById('proposal-rationale').textContent = DATA.latest_proposal.rationale;
}
</script>
</body>
</html>
'''

html = html.replace("__DATA_JSON__", json.dumps(DATA))

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote dashboard.html ({len(html)/1024:.1f} KB)")
