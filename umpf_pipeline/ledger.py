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


def is_verification_record(rec: dict) -> bool:
    """True for a real Phase 2 verification/re-verification line -- False
    for a different kind of event this same file legitimately also holds,
    keyed by the same hypothesis_slug: an outreach-status update
    (event: "outreach_sent", written when a Phase 3 email actually goes
    out, per outreach/README.md's own "append a new ledger line" rule).

    Found and fixed 2026-08-30, the day it first mattered for real: the
    two hypotheses behind the two real Aronson/Phillips sends each got an
    outreach_sent line appended after their verification line -- and
    load_latest_entries()'s original "last line wins" logic, written before
    any outreach event existed in this file, took that event (no verdict,
    no domains) as the "latest" entry for those slugs. The real effect: on
    the very first cycle run after that event existed, the two hypotheses
    that had actually reached a real researcher silently dropped off the
    scored leaderboard entirely, held out as "non-standard verdict ''."
    Confirmed directly against the real leaderboard output, not assumed.

    The "latest entry wins" principle this module exists for is still
    correct for what it was built for -- correcting a wrong verification
    with a new one. It was never meant to let an unrelated event type
    overwrite one. Now it can't: only real verification records (no
    "event" key, per the actual shape both write paths use) participate in
    the per-slug "latest" dedup at all."""
    return "event" not in rec


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
    """The real, current state of the ledger: one VERIFICATION entry per
    slug, built by MERGING every record written for it, field by field --
    non-verification events (outreach status updates; see
    is_verification_record()) are skipped entirely for this dedup, not
    treated as a competing "latest" record. Preserves each surviving
    entry's first-seen position in the file, so rank/sort behavior
    downstream that assumes roughly-chronological order doesn't shuffle
    unexpectedly just because a correction happened to land later for an
    early slug.

    2026-08-31: fixed a real, second gap in this same "latest wins"
    principle -- the first gap (is_verification_record, above) was about
    which RECORDS should compete for "latest" at all. This one is about
    what happens once one wins: a whole-record overwrite (latest_by_key[k]
    = rec) silently discards any field the newest record simply doesn't
    set, even when an older record for the same slug set it validly and
    nothing has happened to invalidate it. Found for real, at real cost:
    re-running Phase 2 verification on every ADJACENT_ACTIVE entry (the
    umbrella-trap retroactive fix) wrote a fresh record for every slug it
    touched, including slugs that had ALSO already gone through Phase 3
    refutation via the "ADJACENT_ACTIVE that failed its own honesty check"
    path -- verify_hypothesis.py's append_ledger_entry() has no reason to
    know about or carry forward refutation_verdict/refutation_file/
    refutation_survival_count/etc., so those fields were simply absent
    from the new record. The whole-record overwrite then made every
    downstream reader (this function, score_hypotheses.py, the whitepaper's
    own headline numbers) treat 161 real entries -- including 9 of the
    ledger's SURVIVES entries, Hayek and Einstein-Maxwell's Nobel
    ground-truth calibration cases and the flagship unanimous 3-of-3
    compiler-instruction-scheduling entry among them -- as never refuted.
    Nothing was actually destroyed (the log is append-only; the real
    refutation records are still physically present, just no longer
    "latest") -- but every reader of load_latest_entries() was blind to
    them until this fix. Merging field-by-field, instead of replacing the
    whole record, means a field only changes when a later record actually
    sets it -- an older record's field survives being "outrun" by a newer
    record that was never trying to say anything about that field at all."""
    merged_by_key = {}
    order = []
    for rec in read_raw_entries(path):
        if not is_verification_record(rec):
            continue
        k = key_for(rec)
        if k not in merged_by_key:
            order.append(k)
            merged_by_key[k] = {}
        merged_by_key[k].update(rec)  # only keys THIS record actually sets move forward
    return [merged_by_key[k] for k in order]
