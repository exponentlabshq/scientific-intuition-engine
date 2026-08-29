"""
ledger.py — the single, shared "latest entry per slug wins" read for
verification-log.jsonl.

Added 2026-08-29, to settle a design question the previous session's
PENDING_VERIFICATION fix raised but deliberately did not resolve: the
ledger is append-only on write, by design -- a correction is always a NEW
line, never an edit or delete of an old one, because that's what makes
"the ledger is append-only, safe to rescore regardless" true elsewhere in
this project. But until this file existed, every reader (score_hypotheses.py,
assemble_experience_data.py via score_hypotheses.py, refute_hypothesis.py,
verify_hypothesis.py) treated EVERY line as an independent, equally-valid
entry. Concretely: 11 real hypotheses were verified during a Tavily
rate-limit incident and landed on a spurious NO_SIGNAL built on zero real
search evidence (fixed going forward in a separate commit). Re-verifying
those 11 for real, the append-only way, means appending a SECOND ledger
line for each of those slugs -- and without this module, every downstream
script would then show BOTH the old, wrong entry and the new, correct one
as separate leaderboard rows, double-counting the hypothesis and leaving
the wrong verdict still visible as if valid.

This module is the one place "which entry is authoritative" gets decided:
read every line, keep only the LAST one written for each slug (file order
== chronological order, since the ledger is only ever appended to), return
that. It never mutates the file itself -- the append-only write invariant
is completely untouched; only the read side changes.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER_PATH = os.path.join(HERE, "verification-log.jsonl")


def key_for(rec: dict) -> str:
    """The identity a ledger entry is deduplicated on. Case-study entries
    (imported from the-rosetta-stone's pre-existing pairs) use 'case_study'
    instead of 'hypothesis_slug' -- same convention score_hypotheses.py
    already used before this file existed."""
    return rec.get("hypothesis_slug") or rec.get("case_study") or "unknown"


def read_raw_entries(path: str = None) -> list:
    """Every line, in file order, no dedup -- for the rare caller that
    genuinely wants full history (an audit, a manual inspection of what
    actually happened to a slug over time) rather than current state."""
    path = path or LEDGER_PATH
    entries = []
    if not os.path.exists(path):
        return entries
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))
    return entries


def load_latest_entries(path: str = None) -> list:
    """The real, current state of the ledger: one entry per slug, the LAST
    one written for it. Preserves each surviving entry's first-seen
    position in the file, so rank/sort behavior downstream that assumes
    roughly-chronological order doesn't shuffle unexpectedly just because
    a correction happened to land later for an early slug."""
    latest_by_key = {}
    order = []
    for rec in read_raw_entries(path):
        k = key_for(rec)
        if k not in latest_by_key:
            order.append(k)
        latest_by_key[k] = rec  # a later occurrence always overwrites -- "latest wins"
    return [latest_by_key[k] for k in order]
