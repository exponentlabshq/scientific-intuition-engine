#!/usr/bin/env python3
"""
build_send_backlog.py -- COA 8d: the actual "which drafted email goes out
first" queue, organized the way Michael asked for it: grouped by FU
department (Janusian / Bisociation / Homospatial Studies -- the same
top-level taxonomy the live site already uses), then by individual real
researcher within each department.

Send priority = leaderboard priority_score (points + paper recency,
same formula as prioritize_outreach.py) + a sharpness bonus from
score_email_sharpness.py's INDEPENDENT judgment (SHARP +15, BORDERLINE
+0, GENERIC -15) -- so a real, well-scored hypothesis with a genuinely
sharp question outranks an equally-well-scored one whose question just
restates the domain name. Run score_email_sharpness.py first (or this
script's own note tells you how many drafts are still unscored, and
scores them as 0 / not-yet-judged rather than silently guessing).

Usage:
    python3 outreach/build_send_backlog.py
"""
import glob
import json
import os
import re
import sys

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PIPELINE_DIR)

EMAILS_DIR = os.path.join(PIPELINE_DIR, "outreach", "emails")
CONTACTS_PATH = os.path.join(PIPELINE_DIR, "outreach", "contacts.jsonl")
EXPERIENCE_PATH = os.path.join(PIPELINE_DIR, "experience_data.json")
SCORES_PATH = os.path.join(PIPELINE_DIR, "outreach", "sharpness_scores.json")
COHERENCE_PATH = os.path.join(PIPELINE_DIR, "outreach", "coherence_scores.json")
BACKLOG_PATH = os.path.join(PIPELINE_DIR, "outreach", "send_backlog.json")

CURRENT_YEAR = 2026
SHARPNESS_BONUS = {"SHARP": 15, "BORDERLINE": 0, "GENERIC": -15}

DEPT_NAMES = {
    "janusian": "Department of Janusian Studies",
    "bisociation": "Department of Bisociation Studies",
    "homospatial": "Department of Homospatial Studies",
}


def recency_bonus(year):
    if not year:
        return 8
    return max(0, 20 - (CURRENT_YEAR - year) * 2)


def load_leaderboard():
    with open(EXPERIENCE_PATH, encoding="utf-8") as f:
        data = json.load(f)
    entries = data if isinstance(data, list) else data.get("entries", data.get("rows", []))
    return {e.get("key"): e for e in entries if e.get("key")}


def load_contacts_by_slug():
    by_slug = {}
    with open(CONTACTS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            c = json.loads(line)
            by_slug.setdefault(c.get("hypothesis_slug"), []).append(c)
    return by_slug


def load_sharpness_scores():
    if os.path.exists(SCORES_PATH):
        with open(SCORES_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_coherence_scores():
    """score_email_coherence.py's own output -- a THIRD, separate axis
    from sharpness (generic-vs-specific). Surfaced for human review,
    same as sharpness -- never auto-excludes a draft from the ranked
    list the way a human FLAGGED status does. The two known real flags
    as of 2026-09-02 (Asaoka: 'drive' vs the source's own 'correlate
    with' -- a minor precision nitpick; Schooler: likely a false
    positive, an older hand-authored draft with human-added narrowing
    context the checker never saw) were both reviewed and judged not
    Vajner-level -- this signal needs a human read every time, same as
    sharpness, not blind trust."""
    if os.path.exists(COHERENCE_PATH):
        with open(COHERENCE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_drafted():
    out = []
    for path in sorted(glob.glob(os.path.join(EMAILS_DIR, "*.md"))):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        slugm = re.search(r"\*\*Hypothesis:\*\*\s*`([^`]+)`", text)
        tom = re.search(r"\*\*To:\*\*\s*(.+?)\s*\\<([^\\>]+)\\>", text)
        statusm = re.search(r"\*\*Status:\*\*\s*(.+)", text)
        status_text = statusm.group(1).strip() if statusm else ""
        # Bug found 2026-09-02: a naive "SENT" in status_text substring
        # check also matches "NOT SENT" and "NOT reviewed... NOT sent"
        # (case-insensitively similar wording) -- silently excluded every
        # one of this session's correctly-labeled "DRAFT — NOT SENT"
        # files from the backlog, while an older stub file's lowercase
        # "NOT sent" slipped through only by accident of casing. A real
        # sent status is anchored at the START of the field ("SENT
        # 2026-08-29"), never preceded by "NOT" -- match that shape only.
        already_sent = bool(re.match(r"^SENT\b", status_text))
        # A human flag overrides the sharpness judge's own verdict --
        # first real case 2026-09-02 (Vajner: rated SHARP by the judge,
        # but flagged on review as physically incoherent, a failure
        # axis the judge isn't built to catch). A flagged draft must
        # never appear as if it's ready to send, regardless of its
        # score -- match the same literal marker written into the
        # Status field by hand ("⚠️ FLAGGED"), not a separate list to
        # drift out of sync with what's actually in the file.
        flagged = "FLAGGED" in status_text
        email = tom.group(2).strip() if tom else ""
        if slugm and email and "TBD" not in email and "fill in" not in email:
            out.append({
                "filename": os.path.basename(path),
                "hypothesis_slug": slugm.group(1),
                "target_name": tom.group(1).strip() if tom else "",
                "email": email,
                "already_sent": already_sent,
                "flagged": flagged,
            })
    return out


def main():
    by_slug_leaderboard = load_leaderboard()
    by_slug_contacts = load_contacts_by_slug()
    scores = load_sharpness_scores()
    coherence = load_coherence_scores()
    drafted = load_drafted()

    unscored = 0
    entries = []
    for d in drafted:
        if d["already_sent"]:
            continue
        e = by_slug_leaderboard.get(d["hypothesis_slug"])
        if not e:
            continue
        points = e.get("points", 0)
        mode = e.get("mode", "calibration")
        # Find this specific contact's matched-paper year (best match on target_name)
        year = None
        for c in by_slug_contacts.get(d["hypothesis_slug"], []):
            if c.get("target_name") == d["target_name"]:
                year = c.get("source_match_year")
                break
        score_entry = scores.get(d["filename"])
        if score_entry:
            sharpness = score_entry["sharpness"]
        else:
            sharpness = None
            unscored += 1
        coherence_entry = coherence.get(d["filename"])
        coherent = coherence_entry["coherent"] if coherence_entry else None
        coherence_concern = coherence_entry.get("concern", "") if coherence_entry else ""
        send_priority = points + recency_bonus(year) + SHARPNESS_BONUS.get(sharpness, 0)
        entries.append({
            "send_priority": send_priority,
            "sharpness": sharpness or "NOT SCORED",
            "coherent": coherent,
            "coherence_concern": coherence_concern,
            "flagged": d["flagged"],
            "points": points,
            "department": DEPT_NAMES.get(mode, mode),
            "dept_slug": mode,
            "target_name": d["target_name"],
            "email": d["email"],
            "hypothesis_slug": d["hypothesis_slug"],
            "filename": d["filename"],
        })

    entries.sort(key=lambda r: r["send_priority"], reverse=True)
    flagged_entries = [e for e in entries if e["flagged"]]
    entries = [e for e in entries if not e["flagged"]]

    by_dept = {}
    for e in entries:
        by_dept.setdefault(e["department"], []).append(e)

    needs_coherence_review = sum(1 for e in entries if e["coherent"] is False)
    print(f"{len(entries)} unsent, unflagged drafted email(s) in the backlog. {len(flagged_entries)} flagged "
          f"(excluded from ranking below -- human review overrode the sharpness score). "
          f"{unscored} not yet sharpness-scored. {needs_coherence_review} flagged by the coherence checker for "
          f"human review (marked ⚠ below -- this is a signal to check, not an auto-exclude; see coherence_concern "
          f"in send_backlog.json).\n")

    if flagged_entries:
        print(f"=== ⚠️ FLAGGED — not send-ready regardless of score ({len(flagged_entries)}) ===")
        for r in flagged_entries:
            print(f"  ({r['sharpness']:10s} points={r['points']:3d}) {r['target_name']} <{r['email']}> -- {r['filename']}")
        print()

    for dept, rows in sorted(by_dept.items(), key=lambda kv: -max(r["send_priority"] for r in kv[1])):
        print(f"=== {dept} ({len(rows)}) ===")
        for r in rows:
            mark = " ⚠ coherence" if r["coherent"] is False else ""
            print(f"  [{r['send_priority']:+4d}] ({r['sharpness']:10s} points={r['points']:3d}) "
                  f"{r['target_name']} <{r['email']}> -- {r['filename']}{mark}")
        print()

    with open(BACKLOG_PATH, "w", encoding="utf-8") as f:
        json.dump({"ready": entries, "flagged": flagged_entries}, f, indent=2)
    print(f"Wrote {len(entries)} ready + {len(flagged_entries)} flagged entries to {BACKLOG_PATH}")


if __name__ == "__main__":
    main()
