#!/usr/bin/env python3
"""
build_dashboard.py — The Eureka Engine's live operations dashboard.

Restyled 2026-08-29 per Michael's direct request: "styled like the driving
digital dashboard from that show with Kit & David Hasselhoff... Digital LED
RED light dots, gauges, radial speed dial large... 75% less text." A KITT
instrument-cluster reskin -- Orbitron/Share Tech Mono (Google Fonts, real
digital-HUD faces, not system serif/sans), a continuous red LED scanner bar
doubling as the real last-cycle phase indicator, one large radial gauge for
mission success rate, small arc gauges for mode performance, and verdict
counts as blocky LED digit readouts instead of labeled bars. Every number is
still the same real, computed data as before -- only the treatment changed,
prose cut hard everywhere it wasn't load-bearing information.

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
import re
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
    proposals_dir = os.path.join(PIPELINE_DIR, "proposals")
    if os.path.exists(audit_log_path):
        with open(audit_log_path, "r", encoding="utf-8") as f:
            audits = [json.loads(l) for l in f if l.strip()]
        if audits:
            a = audits[-1]
            proposal_name = a.get("proposal_file") or ""
            proposal_file = os.path.join(proposals_dir, proposal_name)
            rationale = ""
            status = "unreviewed"
            if proposal_name and os.path.exists(proposal_file):
                text = open(proposal_file, encoding="utf-8").read()
                # Status line lives in the header block (before first ##)
                header = text.split("##", 1)[0]
                m_status = re.search(r"\*\*Status\*\*:\s*(.+)", header)
                if m_status:
                    status = m_status.group(1).strip()
                m = text.split("## Rationale", 1)
                if len(m) > 1:
                    rationale = m[1].split("##", 1)[0].strip()
                # If rejected/superseded, prefer the correction write-up as the
                # spotlight so the dashboard doesn't pitch a dead filter as live advice.
                status_l = status.lower()
                if "rejected" in status_l or "superseded" in status_l:
                    stem = proposal_name.replace(".md", "")
                    # e.g. 2026-08-29-proposal-003 → 2026-08-29-correction-to-proposal-003.md
                    parts = stem.split("-proposal-")
                    if len(parts) == 2:
                        corr_name = f"{parts[0]}-correction-to-proposal-{parts[1]}.md"
                        corr_path = os.path.join(proposals_dir, corr_name)
                        if os.path.exists(corr_path):
                            corr = open(corr_path, encoding="utf-8").read()
                            proposal_name = corr_name
                            # First prose block after the title/status header
                            body = corr.split("\n\n", 2)
                            rationale = (body[2] if len(body) > 2 else corr)[:600].strip()
                            # Keep rejected marker visible in the title line
                            a = dict(a)
                            a["title"] = f"[REJECTED] {a.get('title', 'Untitled')} — see correction"
            latest_proposal = {
                "title": a.get("title", "Untitled"),
                "proposal_file": proposal_name,
                "code_file": a.get("code_file"),
                "status": status,
                "rationale": rationale[:600],
            }

    total_scored_for_rate = sum(v for k, v in verdict_counts.items() if k != "NO_SIGNAL_UNRESOLVED")
    dead_end_count = verdict_counts.get("COLLISION", 0) + verdict_counts.get("REFUTED", 0) + verdict_counts.get("FACT_CHECK_FAIL", 0)
    success_rate_pct = round((verdict_counts.get("ADJACENT_ACTIVE", 0) / total_scored_for_rate) * 100, 1) if total_scored_for_rate else 0

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_hypotheses": len(entries),
        "verdict_counts": dict(verdict_counts),
        "success_rate_pct": success_rate_pct,
        "dead_end_count": dead_end_count,
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #030202; --panel: #0b0706; --panel-2: #130c0a; --bezel: #3d1210;
  --led-red: #ff2020; --led-red-bright: #ff5a3c; --led-red-dim: #3a0808;
  --led-amber: #ffa500; --led-green: #00ff6a; --led-green-dim: #063d1f;
  --text: #ffcabf; --text-dim: #8a4d45; --text-faint: #5a2f2a; --white: #fff1e8;
  --display: 'Orbitron', sans-serif; --mono: 'Share Tech Mono', ui-monospace, monospace;
}
* { box-sizing: border-box; }
body {
  background: var(--bg); color: var(--text); font-family: var(--mono);
  font-size: 14px; line-height: 1.5; margin: 0; padding: 0 16px 60px;
}
.wrap { max-width: 1180px; margin: 0 auto; }

/* nav (site-wide, matches other pages but restyled to fit) */
.site-nav {
  position: sticky; top: 0; z-index: 200; margin: 0 -16px 0;
  background: rgba(3,2,2,0.95); border-bottom: 1px solid var(--bezel);
}
.site-nav-inner { max-width: 1180px; margin: 0 auto; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; gap: 20px; }
.site-nav-brand { font-family: var(--display); font-size: 0.9rem; color: var(--led-red); text-decoration: none; font-weight: 700; letter-spacing: 0.04em; }
.site-nav-links { display: flex; gap: 20px; }
.site-nav-links a { font-family: var(--mono); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-dim); text-decoration: none; }
.site-nav-links a:hover { color: var(--led-red); }
.site-nav-links a.is-active { color: var(--led-red); border-bottom: 1px solid var(--led-red); padding-bottom: 2px; }

/* console header */
.console-header { padding: 20px 0 14px; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 10px; }
.console-header .id { font-family: var(--mono); font-size: 0.85rem; letter-spacing: 0.12em; color: var(--text-dim); text-transform: uppercase; }
.console-header h1 { font-family: var(--display); font-weight: 900; font-size: clamp(1.3rem, 3vw, 1.9rem); margin: 4px 0 0; color: var(--white); letter-spacing: 0.02em; }
.status-tag { font-family: var(--mono); font-size: 0.85rem; letter-spacing: 0.08em; color: var(--led-green); border: 1px solid var(--led-green-dim); background: rgba(0,255,106,0.06); padding: 5px 12px; border-radius: 3px; }
.status-tag .dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: var(--led-green); margin-right: 6px; box-shadow: 0 0 6px var(--led-green); animation: blink 1.6s ease-in-out infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

/* KITT scanner bar */
.scanner-panel { background: var(--panel); border: 1px solid var(--bezel); border-radius: 6px; padding: 10px 14px 14px; margin-bottom: 16px; }
.scanner-track { display: flex; gap: 3px; height: 22px; margin-bottom: 8px; }
.scanner-led { flex: 1; background: var(--led-red-dim); border-radius: 2px; transition: background 0.06s linear, box-shadow 0.06s linear; }
.scanner-led.lit { background: var(--led-red); box-shadow: 0 0 8px 1px var(--led-red-bright); }
.phase-row { display: flex; justify-content: space-between; }
.phase-chip { display: flex; flex-direction: column; align-items: center; gap: 4px; flex: 1; }
.phase-chip .ring { width: 30px; height: 30px; border-radius: 50%; border: 2px solid var(--text-faint); display: flex; align-items: center; justify-content: center; font-size: 0.85rem; background: var(--panel-2); }
.phase-chip .ring.ok { border-color: var(--led-green); box-shadow: 0 0 8px rgba(0,255,106,0.4); }
.phase-chip .ring.fail { border-color: var(--led-red); box-shadow: 0 0 8px rgba(255,32,32,0.4); }
.phase-chip .lbl { font-family: var(--mono); font-size: 0.9rem; font-weight: 700; letter-spacing: 0.06em; color: var(--text); text-transform: uppercase; }
.phase-chip .val { font-family: var(--display); font-size: 0.8rem; color: var(--led-red); min-height: 1em; }
.cycle-meta { font-family: var(--mono); font-size: 0.82rem; color: var(--text-dim); text-align: center; margin-top: 10px; }

/* instrument cluster */
.cluster { display: grid; grid-template-columns: 1fr 1.3fr 1fr; gap: 16px; align-items: center; margin: 20px 0; }
@media (max-width: 780px) { .cluster { grid-template-columns: 1fr; } }
.mini-gauges { display: flex; flex-direction: column; gap: 14px; }
.gauge-panel { background: var(--panel); border: 1px solid var(--bezel); border-radius: 6px; padding: 14px; text-align: center; }
.gauge-panel svg { display: block; margin: 0 auto; }
.gauge-num { font-family: var(--display); font-weight: 700; fill: var(--led-red); }
.gauge-label { font-family: var(--mono); font-size: 0.92rem; font-weight: 700; letter-spacing: 0.06em; color: var(--text); text-transform: uppercase; margin-top: 8px; }
.hero-gauge { background: var(--panel); border: 1px solid var(--bezel); border-radius: 10px; padding: 20px; text-align: center; }
.hero-gauge .gauge-label { font-size: 1.15rem; margin-top: 10px; }

/* LED digit readouts (verdict counts) */
.led-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(90px,1fr)); gap: 10px; margin: 16px 0; }
.led-box { background: var(--panel); border: 1px solid var(--bezel); border-radius: 6px; padding: 12px 8px; text-align: center; }
.led-box .n { font-family: var(--display); font-size: 1.6rem; font-weight: 700; text-shadow: 0 0 10px currentColor; }
.led-box .l { font-family: var(--mono); font-size: 0.85rem; font-weight: 700; letter-spacing: 0.06em; color: var(--text); margin-top: 6px; text-transform: uppercase; }
.led-box.red .n { color: var(--led-red); } .led-box.green .n { color: var(--led-green); } .led-box.amber .n { color: var(--led-amber); }

section.block { margin: 24px 0; }
section.block h2 { font-family: var(--display); font-size: 0.85rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text); margin: 0 0 10px; border-bottom: 1px solid var(--bezel); padding-bottom: 8px; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: start; }
.grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; }
@media (max-width: 780px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } }
.card { background: var(--panel); border: 1px solid var(--bezel); border-radius: 6px; padding: 14px 16px; }

/* mode mini gauges row */
.mode-gauge { text-align: center; }
.mode-gauge .name { font-family: var(--mono); font-size: 0.9rem; font-weight: 700; letter-spacing: 0.06em; color: var(--text); text-transform: uppercase; margin-top: 8px; }
.mode-gauge .stat { font-family: var(--display); font-size: 0.95rem; color: var(--led-red); margin-top: 2px; }

/* leaderboard terminal list */
.term-row { display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px dashed var(--text-faint); font-size: 0.92rem; }
.term-row:last-child { border-bottom: none; }
.term-row .pts { font-family: var(--display); color: var(--led-red); font-weight: 700; }
.term-link { display: inline-block; margin-top: 10px; font-family: var(--mono); font-size: 0.85rem; letter-spacing: 0.06em; color: var(--led-red); text-decoration: none; border: 1px solid var(--bezel); padding: 7px 14px; border-radius: 4px; }
.term-link:hover { background: rgba(255,32,32,0.08); }

/* roti table */
.roti-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.roti-table th, .roti-table td { padding: 5px 6px; text-align: right; border-bottom: 1px solid var(--text-faint); }
.roti-table th:first-child, .roti-table td:first-child { text-align: left; }
.roti-table th { font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.04em; color: var(--text); font-size: 0.82rem; }
.roti-table td { color: var(--text); }
.roti-note { margin-top: 10px; font-size: 0.85rem; color: var(--text-dim); line-height: 1.6; }
.roti-note b { color: var(--led-red); }

/* audit feed as terminal log */
.log-line { font-size: 0.9rem; padding: 5px 0; color: var(--text); }
.log-line .ts { color: var(--text-faint); margin-right: 6px; }
.log-line::before { content: '>'; color: var(--led-red); margin-right: 6px; }

.proposal-alert { border-color: var(--led-amber); }
.proposal-alert .tag { font-family: var(--mono); font-size: 0.8rem; letter-spacing: 0.06em; color: var(--led-amber); text-transform: uppercase; border: 1px solid var(--led-amber); padding: 3px 10px; border-radius: 3px; }
.proposal-alert .t { font-family: var(--display); font-size: 0.85rem; color: var(--white); margin: 8px 0 4px; }
.proposal-alert .f { font-family: var(--mono); font-size: 0.85rem; color: var(--text-dim); }

@media (prefers-reduced-motion: reduce) { .status-tag .dot { animation: none; } }
</style>
</head>
<body>
<nav class="site-nav">
  <div class="site-nav-inner">
    <a class="site-nav-brand" href="landing.html">THE EUREKA ENGINE</a>
    <div class="site-nav-links">
      <a href="landing.html">Home</a>
      <a href="dashboard.html" class="is-active">Dashboard</a>
      <a href="whitepaper.html">Whitepaper</a>
      <a href="dean-letters.html">Dean's Letters</a>
      <a href="leaderboard.html">Leaderboard</a>
    </div>
  </div>
</nav>
<div class="wrap">

  <div class="console-header">
    <div>
      <div class="id">EXPONENT LABS // FACULTY OF INTERDISCIPLINARY RESEARCH</div>
      <h1>OPERATIONS CONSOLE</h1>
    </div>
    <div class="status-tag"><span class="dot"></span>ONLINE</div>
  </div>

  <div class="scanner-panel">
    <div class="scanner-track" id="scanner-track"></div>
    <div class="phase-row" id="phase-row"></div>
    <div class="cycle-meta" id="cycle-meta"></div>
  </div>

  <div class="cluster">
    <div class="mini-gauges">
      <div class="gauge-panel" id="gauge-total"></div>
      <div class="gauge-panel" id="gauge-cost"></div>
    </div>
    <div class="hero-gauge" id="gauge-hero"></div>
    <div class="mini-gauges">
      <div class="gauge-panel" id="gauge-deadend"></div>
      <div class="gauge-panel" id="gauge-tpp"></div>
    </div>
  </div>

  <div class="led-row" id="verdict-leds"></div>

  <section class="block">
    <h2>Mode Performance</h2>
    <div class="grid-3" id="mode-gauges"></div>
  </section>

  <section class="block grid-2">
    <div class="card">
      <h2 style="border:none;margin:0 0 8px;">Leaderboard Top 5</h2>
      <div id="leaderboard-list"></div>
      <a class="term-link" href="leaderboard.html">FULL LEADERBOARD →</a>
    </div>
    <div class="card">
      <h2 style="border:none;margin:0 0 8px;">Return on Token Investment</h2>
      <div id="roti-table"></div>
      <div class="roti-note" id="roti-note"></div>
    </div>
  </section>

  <section class="block grid-2">
    <div class="card">
      <h2 style="border:none;margin:0 0 8px;">Audit Log</h2>
      <div id="audit-log"></div>
    </div>
    <div class="card proposal-alert" id="proposal-card">
      <span class="tag">Unreviewed Proposal</span>
      <div class="t" id="proposal-title"></div>
      <div class="f" id="proposal-file"></div>
    </div>
  </section>

</div>

<script>
const DATA = __DATA_JSON__;
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- KITT scanner bar (ambient) + real phase status ---------- */
const NUM_LEDS = 24;
const track = document.getElementById('scanner-track');
const leds = [];
for (let i = 0; i < NUM_LEDS; i++) {
  const d = document.createElement('div');
  d.className = 'scanner-led';
  track.appendChild(d);
  leds.push(d);
}
let scanPos = 0, scanDir = 1;
function scanTick() {
  leds.forEach((led, i) => {
    const dist = Math.abs(i - scanPos);
    led.classList.toggle('lit', dist <= 1);
  });
  scanPos += scanDir;
  if (scanPos >= NUM_LEDS - 1 || scanPos <= 0) scanDir *= -1;
}
if (!reducedMotion) { scanTick(); setInterval(scanTick, 55); }
else { leds.forEach(l => l.classList.add('lit')); }

const STAGE_ICON = { generation: '🧬', verification: '🔍', refutation: '⚖', scoring: '🏆', publish: '📡' };
const STAGE_LABEL = { generation: 'GEN', verification: 'VER', refutation: 'REF', scoring: 'SCR', publish: 'PUB' };
const phaseRow = document.getElementById('phase-row');
const cycleMeta = document.getElementById('cycle-meta');
if (DATA.last_cycle) {
  const lc = DATA.last_cycle;
  ['generation','verification','refutation','scoring','publish'].forEach(key => {
    const st = lc.stages[key] || { ran: false };
    const chip = document.createElement('div');
    chip.className = 'phase-chip';
    const ringClass = st.ran ? (st.ok === false ? 'fail' : 'ok') : '';
    const val = key === 'generation' ? lc.generated : '';
    chip.innerHTML = `<div class="ring ${ringClass}">${STAGE_ICON[key]}</div><div class="lbl">${STAGE_LABEL[key]}</div><div class="val">${val}</div>`;
    phaseRow.appendChild(chip);
  });
  const when = new Date(lc.timestamp);
  cycleMeta.textContent = `LAST CYCLE ${when.toLocaleString()} — ${lc.status.toUpperCase()}`;
} else {
  cycleMeta.textContent = 'NO CYCLE DATA';
}

/* ---------- Radial gauge builder (SVG arc + big digital number) ---------- */
function buildGauge(container, { value, max, label, color, size, sub }) {
  const strokeWidth = size * 0.1;
  const r = (size - strokeWidth) / 2;
  const circ = 2 * Math.PI * r;
  const pct = Math.max(0, Math.min(1, max ? value / max : 0));
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', size); svg.setAttribute('height', size);
  svg.innerHTML = `
    <circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="var(--led-red-dim)" stroke-width="${strokeWidth}" />
    <circle class="arc" cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="${color}" stroke-width="${strokeWidth}"
      stroke-linecap="round" stroke-dasharray="${circ}" stroke-dashoffset="${circ}"
      transform="rotate(-90 ${size/2} ${size/2})" style="filter:drop-shadow(0 0 6px ${color});" />
    <text x="50%" y="46%" text-anchor="middle" dominant-baseline="middle" class="gauge-num" font-size="${size*0.22}">${sub ? '' : Math.round(value)}</text>
    ${sub ? `<text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" class="gauge-num" font-size="${size*0.16}">${sub}</text>` : ''}
  `;
  container.innerHTML = '';
  container.appendChild(svg);
  const label_el = document.createElement('div');
  label_el.className = 'gauge-label';
  label_el.textContent = label;
  container.appendChild(label_el);
  const arc = svg.querySelector('.arc');
  requestAnimationFrame(() => {
    arc.style.transition = reducedMotion ? 'none' : 'stroke-dashoffset 1.1s cubic-bezier(0.16,1,0.3,1)';
    arc.style.strokeDashoffset = circ - (circ * pct);
  });
}

buildGauge(document.getElementById('gauge-hero'), {
  value: DATA.success_rate_pct, max: 100, label: 'MISSION SUCCESS RATE', color: 'var(--led-red)', size: 210, sub: DATA.success_rate_pct + '%'
});
buildGauge(document.getElementById('gauge-total'), { value: DATA.total_hypotheses, max: Math.max(DATA.total_hypotheses, 100), label: 'HYPOTHESES', color: 'var(--led-amber)', size: 120 });
buildGauge(document.getElementById('gauge-deadend'), { value: DATA.dead_end_count, max: DATA.total_hypotheses || 1, label: 'DEAD ENDS CAUGHT', color: 'var(--led-red)', size: 120 });
buildGauge(document.getElementById('gauge-cost'), { value: DATA.total_cost, max: Math.max(DATA.total_cost * 1.4, 1), label: 'COST $', color: 'var(--led-green)', size: 120, sub: '$' + DATA.total_cost.toFixed(2) });
buildGauge(document.getElementById('gauge-tpp'), { value: DATA.tokens_per_point || 0, max: Math.max((DATA.tokens_per_point||0) * 1.4, 1), label: 'TOKENS / POINT', color: 'var(--led-amber)', size: 120 });

/* ---------- Verdict LED digit readouts ---------- */
const VERDICT_META = {
  ADJACENT_ACTIVE: { code: 'ADJ', cls: 'green' }, COLLISION: { code: 'COL', cls: 'amber' },
  REFUTED: { code: 'REF', cls: 'red' }, FACT_CHECK_FAIL: { code: 'FCF', cls: 'red' },
  NO_SIGNAL_UNRESOLVED: { code: 'PND', cls: 'amber' }, OTHER: { code: 'FLG', cls: 'amber' },
};
const ledRow = document.getElementById('verdict-leds');
Object.entries(DATA.verdict_counts).sort((a,b)=>b[1]-a[1]).forEach(([key, count]) => {
  if (!count) return;
  const meta = VERDICT_META[key] || { code: key.slice(0,3).toUpperCase(), cls: 'red' };
  const box = document.createElement('div');
  box.className = 'led-box ' + meta.cls;
  box.innerHTML = `<div class="n">${count}</div><div class="l">${meta.code}</div>`;
  ledRow.appendChild(box);
});

/* ---------- Mode mini gauges ---------- */
const modeEl = document.getElementById('mode-gauges');
DATA.mode_summary.forEach(m => {
  const panel = document.createElement('div');
  panel.className = 'card mode-gauge';
  const gaugeDiv = document.createElement('div');
  panel.appendChild(gaugeDiv);
  const extra = document.createElement('div');
  extra.className = 'stat';
  extra.textContent = `${m.avg_points} PTS AVG · n=${m.n}`;
  panel.appendChild(extra);
  modeEl.appendChild(panel);
  buildGauge(gaugeDiv, { value: Math.round((1-m.no_signal_rate)*100), max: 100, label: m.label.toUpperCase(), color: 'var(--led-red)', size: 100 });
});

/* ---------- Leaderboard ---------- */
const lbEl = document.getElementById('leaderboard-list');
DATA.top5.forEach((row, i) => {
  const div = document.createElement('div');
  div.className = 'term-row';
  const short = row.domains.length > 42 ? row.domains.slice(0, 40) + '…' : row.domains;
  div.innerHTML = `<span>${i+1}. ${short}</span><span class="pts">${row.points > 0 ? '+' : ''}${row.points}</span>`;
  lbEl.appendChild(div);
});

/* ---------- ROTI table ---------- */
const rotiEl = document.getElementById('roti-table');
let tbl = '<table class="roti-table"><tr><th>Phase</th><th>Calls</th><th>Avg Tok</th><th>Cost</th></tr>';
DATA.roti_phases.forEach(p => {
  tbl += `<tr><td>${p.phase}</td><td>${p.n_calls}</td><td>${p.avg_tokens.toLocaleString()}</td><td>$${p.cost.toFixed(4)}</td></tr>`;
});
tbl += '</table>';
rotiEl.innerHTML = tbl;
document.getElementById('roti-note').innerHTML = DATA.claude_tokens_avoided > 0
  ? `Refutation on OpenAI: <b>${DATA.real_refutation_tokens.toLocaleString()}</b> real tokens vs. est. <b>${DATA.claude_tokens_avoided.toLocaleString()}</b> Claude tokens for the same work.`
  : `Tokens per point, pool-wide: <b>${DATA.tokens_per_point ?? '—'}</b>`;

/* ---------- Audit log ---------- */
const logEl = document.getElementById('audit-log');
if (!DATA.observations.length) {
  logEl.innerHTML = '<div class="log-line" style="color:var(--text-faint)">— no observations logged yet —</div>';
} else {
  DATA.observations.forEach(o => {
    const when = new Date(o.timestamp);
    const div = document.createElement('div');
    div.className = 'log-line';
    div.innerHTML = `<span class="ts">${when.toLocaleTimeString()}</span>${o.text}`;
    logEl.appendChild(div);
  });
}

/* ---------- Proposal spotlight ---------- */
if (DATA.latest_proposal) {
  document.getElementById('proposal-title').textContent = DATA.latest_proposal.title;
  document.getElementById('proposal-file').textContent = 'proposals/' + (DATA.latest_proposal.proposal_file || '');
} else {
  document.getElementById('proposal-card').style.display = 'none';
}
</script>
</body>
</html>
'''

html = html.replace("__DATA_JSON__", json.dumps(DATA))

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote dashboard.html ({len(html)/1024:.1f} KB)")
