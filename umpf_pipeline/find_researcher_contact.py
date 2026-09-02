#!/usr/bin/env python3
"""
find_researcher_contact.py -- COA A (2026-09-02): the one real gap
outreach/emails/README.md's own "Phase 4" section already named and
explicitly refused to paper over: active_research_check.py already finds
real researchers/papers genuinely working the same territory as this
pipeline's own hypotheses (verified 2026-09-02: 20/20 of the current
top-scoring hypotheses already have real active_research_matches) -- but
turning "Jonathan Schooler wrote this paper" into a real, current,
sourced institutional email has, until now, been 100% manual, one
recipient at a time (that is literally how Schooler's, Aronson's,
Frey's, and Phillips's contact info was found).

This script is that missing link, not a new system: same architecture as
active_research_check.py and verify_hypothesis.py (OpenAI web_search,
one structured call per target, token_tracker logging, an append-only
ledger). Same non-negotiable discipline as every other real-fact field in
this pipeline: an email is only ever real if the model found it literally
written on a real, cited public page (a university faculty directory, a
lab site, a departmental staff listing) -- never a firstname.lastname@
university.edu pattern-guess from a name and an institution, which is
the specific, named failure mode the system prompt below exists to rule
out. When nothing real can be found, the honest result is `resolved:
false` / empty email, written down as such -- not a plausible guess.

This script only ever WRITES a record to outreach/contacts.jsonl. It
does not touch outreach/emails/, outreach/packets/, or send anything --
matching this whole pipeline's standing NOT SENT discipline. Turning a
resolved contact into an actual draft is still the existing, separate,
human-in-the-loop step in outreach/README.md.

Usage:
    python3 find_researcher_contact.py <slug> [<slug> ...]
    python3 find_researcher_contact.py --all-shortlist [--limit N]
    python3 find_researcher_contact.py --all-shortlist --dry-run
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from openai import OpenAI

import token_tracker

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTACTS_PATH = os.path.join(PIPELINE_DIR, "outreach", "contacts.jsonl")
SHORTLIST_PATH = os.path.join(PIPELINE_DIR, "outreach", "shortlist.json")

load_dotenv("/Users/michaeljagdeo/Downloads/talentOS-2026/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"

CONTACT_SCHEMA = {
    "type": "object",
    "properties": {
        "resolved": {"type": "boolean", "description": "True only if a real, current-or-most-recently-known institutional affiliation was found for a specific named individual."},
        "target_name": {"type": "string", "description": "The one specific individual this result is about -- must be a real name from the input author list, or a real corresponding author found via search. Never invented."},
        "institution": {"type": "string", "description": "Real institutional affiliation (university, lab, company). Empty string if unknown."},
        "department": {"type": "string", "description": "Empty string if unknown."},
        "role_title": {"type": "string", "description": "e.g. 'Associate Professor', 'PhD Candidate', 'Research Scientist'. Empty string if unknown."},
        "email": {
            "type": "string",
            "description": (
                "A real email address ONLY if it was found literally written on a real public "
                "page returned by search (a faculty directory, lab page, or staff listing). "
                "NEVER construct, guess, or pattern-match an email from a name and an "
                "institution's domain -- if you did not see this exact address written on a "
                "real page, leave this empty."
            ),
        },
        "email_source_url": {"type": "string", "description": "The real URL where the email above was found, verbatim. Empty string if email is empty."},
        "profile_url": {"type": "string", "description": "A real faculty/lab/personal-academic page for this person, if found, even if it had no email on it. Empty string if none."},
        "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
        "notes": {"type": "string", "description": "1-2 sentences: what was actually found, and any real caveat (e.g. page undated, appears to have since moved institutions, email found but on a 2019-dated page)."},
    },
    "required": ["resolved", "target_name", "institution", "department", "role_title", "email", "email_source_url", "profile_url", "confidence", "notes"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = (
    "You are resolving real, current contact information for ONE specific researcher, given "
    "a paper or project they are a real author or contributor on. Your only job is to find "
    "where they actually are now (or most recently were) and how to actually reach them, "
    "using real web search -- not to guess.\n\n"
    "The single most important rule: an email address is only real if you found it literally "
    "written, character for character, on a real page search returned to you -- a university "
    "faculty directory, a lab or group website, a departmental staff listing, or a personal "
    "academic homepage. Universities very often do publish faculty and staff emails on "
    "exactly these kinds of pages, so a genuine search frequently succeeds -- but the address "
    "must come from a page you can cite, not from combining a name with an institution's "
    "domain into a plausible-looking pattern (firstname.lastname@, first-initial-lastname@, "
    "etc.). That specific shortcut is exactly what you must never do, no matter how standard "
    "the institution's email format looks from other real examples on the same page -- a "
    "pattern is not a citation. If you cannot find the actual address written down, leave the "
    "email field empty and say so in notes; an honest empty result is correct, a guessed "
    "address is not.\n\n"
    "If the author list has multiple names, use judgment to identify the single best real "
    "contact -- typically a corresponding author, a PI, or whoever the paper/page itself "
    "identifies as the point of contact -- rather than an arbitrary first name. Prefer a "
    "person whose current institutional page you can actually find and cite. Report their "
    "institution, department, and role/title only if you find real, current (or most "
    "recently known) evidence of them -- leave any field empty rather than infer it."
)


def resolve_one(researcher_or_authors, title, year, source_url, domains, slug=None):
    text = (
        f"Author(s) on the real paper/project: {researcher_or_authors}\n"
        f"Title: {title}\n"
        f"Year: {year if year else 'unknown'}\n"
        f"Original source URL: {source_url or '(none given)'}\n"
        f"Domain(s) this relates to: {', '.join(domains) if domains else '(none given)'}\n\n"
        "Find the single best real, current contact for this work."
    )
    resp = client.responses.create(
        model=MODEL,
        tools=[{"type": "web_search"}],
        instructions=SYSTEM_PROMPT,
        input=text,
        max_output_tokens=1200,
        text={"format": {"type": "json_schema", "name": "researcher_contact", "schema": CONTACT_SCHEMA, "strict": True}},
    )
    token_tracker.log_usage("outreach_contact", MODEL, resp.usage, hypothesis_slug=slug)
    return json.loads(resp.output_text), resp.usage


_BARE_DOMAIN_RE = re.compile(r"^https?://(?:www\.)?([^/]+?)/?$")


def _domain_matches_person(host, name):
    """True if the domain's own first label plausibly belongs to the
    named person (a personal vanity domain or username-style GitHub
    Pages site) rather than an institution's shared root domain.
    'zzlang-c.github.io' for 'Lang Cao' -> True ('lang' is in both);
    'avi.press' for 'Avi Press' -> True ('avi' is in both);
    'berkeley.edu' for 'Zijiao Zhang' -> False (no real overlap)."""
    label = re.sub(r"[^a-z]", "", host.split(".")[0].lower())
    name_parts = re.sub(r"[^a-z ]", "", name.lower()).split()
    return any(len(p) >= 3 and p in label for p in name_parts)


def _sanity_check(result, title):
    """Catch two real, observed failure modes before either is ever
    persisted, both found 2026-09-02 on the same real batch, the second
    one refined the same day after a real, concrete counter-example
    (a genuine Berkeley department page for a different real person,
    'Yi Jiao', confirmed a real firstname+lastname @berkeley.edu
    address pattern legitimately exists and is discoverable -- just
    never on the university's own bare root homepage):

    1. target_name is actually the SOURCE PAPER'S OWN TITLE, not a
       person ('Humor Analysis in Interactive Stand-up Comedy Based on
       Cooperative Principle' as a target_name, with a real, resolved
       email attached to it).
    2. email_source_url is a bare domain homepage with no path AND that
       domain has no real connection to the person's own name --
       'https://www.berkeley.edu/' for 'Zijiao Zhang' is a large shared
       institutional root that cannot plausibly display one specific
       person's email, confirmed by direct follow-up search: real
       records for a person by that name point to a different current
       institution entirely, so this was very likely the exact
       firstname@domain pattern-guess the system prompt explicitly
       forbids. A personal vanity domain or username-based GitHub Pages
       site ('avi.press' for Avi Press, 'zzlang-c.github.io' for Lang
       Cao) is NOT flagged -- a person's own homepage plausibly does
       show their own contact info on its front page, the same real
       shape as the Yi Jiao counter-example, just self-hosted instead
       of on a department page.

    Either failure downgrades the result to an honest not-found with
    the reason recorded, rather than silently shipping a fabricated or
    misattributed contact. Deliberately narrow so a real, if unusual,
    real name or a real personal homepage is never wrongly flagged."""
    name = (result.get("target_name") or "").strip()
    # Deliberately excludes "" -- an already-empty field is the correct,
    # honest representation of "not found," not a placeholder needing
    # rejection. Found and fixed within the hour of writing the first
    # version of this check: it included "" in this set, so it fired on
    # every already-legitimate empty target_name/email in the file and
    # overwrote their real notes with a false rejection message on a
    # retroactive re-scan, before any of that reached a live batch.
    PLACEHOLDER_WORDS = {"not specified", "n/a", "na", "none", "unknown", "unspecified", "tbd"}
    if name and name.lower().strip(".") in PLACEHOLDER_WORDS:
        # The model is supposed to leave a field genuinely empty when it
        # doesn't know, per the schema -- but one real result instead
        # wrote the literal text "Not specified" into target_name AND
        # email AND email_source_url, which (being non-empty strings)
        # read as a truthy, "found" result to every caller checking
        # `if result.get("email")`. A schema and a prompt asking for an
        # empty string is not the same as the model actually producing
        # one; this catches the placeholder-as-if-real-data case
        # directly rather than trusting the field was used correctly.
        return {
            **result,
            "resolved": False,
            "target_name": "",
            "email": "",
            "email_source_url": "",
            "profile_url": "",
            "confidence": "LOW",
            "notes": f"Sanity check rejected this result: target_name was a placeholder string ('{name}'), not a real name. Original notes: {result.get('notes', '')}",
        }
    title_norm = (title or "").strip().lower()
    name_norm = name.lower()
    if title_norm and name_norm and (
        name_norm == title_norm
        or (len(name_norm) > 15 and name_norm in title_norm)
        or (len(title_norm) > 3 and title_norm in name_norm)
    ):
        # Bidirectional on purpose: the first real catch of this failure
        # ('Humor Analysis in Interactive Stand-up Comedy...' as a
        # target_name) had the full paper title AS the name. A later
        # real case ('LibRA 2019' as a target_name for a paper titled
        # 'LibRA') has it the other way around -- the paper's own short
        # title sits INSIDE a name-shaped string, with a year tacked on
        # like a person's name might have a suffix. Checking only
        # name-in-title missed that second real shape.
        return {
            **result,
            "resolved": False,
            "target_name": "",
            "email": "",
            "email_source_url": "",
            "profile_url": "",
            "confidence": "LOW",
            "notes": f"Sanity check rejected this result: target_name ('{name}') and the source paper's own title ('{title}') overlap too closely for this to be a real person's name. Original notes: {result.get('notes', '')}",
        }
    email_src = (result.get("email_source_url") or "").strip()
    m = _BARE_DOMAIN_RE.match(email_src) if email_src else None
    if result.get("email") and m and name and not _domain_matches_person(m.group(1), name):
        return {
            **result,
            "email": "",
            "email_source_url": "",
            "confidence": "LOW",
            "notes": f"Sanity check rejected the email in this result: its cited source ('{email_src}') is a bare domain homepage unconnected to {name}'s own name, which cannot actually display one specific person's email -- almost certainly a pattern-guessed address, not a real citation. Original notes: {result.get('notes', '')}",
        }
    email = (result.get("email") or "")
    if email and email.lower().strip(".") in PLACEHOLDER_WORDS:
        # Same placeholder-as-if-real-data failure as target_name above,
        # caught independently here since a real name can still come
        # paired with a placeholder email (the two are set by the model
        # somewhat independently, not always both-or-neither).
        return {
            **result,
            "email": "",
            "email_source_url": "",
            "confidence": "LOW",
            "notes": f"Sanity check rejected this result: email was a placeholder string ('{email}'), not a real address. Original notes: {result.get('notes', '')}",
        }
    if "protected" in email.lower() and "email" in email.lower():
        # Third real failure mode, same day: ResearchGate (and other
        # sites) render an obfuscated contact as literal page text --
        # "[email protected]" (real pages use a non-breaking space, not
        # an ASCII one) -- decoded client-side by JS the model's page
        # fetch never runs. Two separate real results both lifted that
        # literal placeholder string as if it were the actual address,
        # both marked HIGH confidence. This is not a guessed pattern
        # like the berkeley.edu case; it's mistaking a website's own
        # anti-scraping stub for real data.
        return {
            **result,
            "email": "",
            "email_source_url": "",
            "confidence": "LOW",
            "notes": f"Sanity check rejected the email in this result: it was the literal text '{email}' -- a site's email-obfuscation placeholder (e.g. ResearchGate's anti-scraping stub), not a real decoded address. Original notes: {result.get('notes', '')}",
        }
    return result


def _clean(s):
    """Strip stray control characters (observed for real 2026-09-02: a
    NUL byte in place of an accented character -- "El\\x00as Castellanos"
    for "Elías Castellanos" -- in one structured response's target_name,
    likely a rare tokenizer/encoding edge case on the API side, not
    anything this script did). Leaves real text untouched; only removes
    C0/C1 control codes a JSON string should never legitimately contain."""
    if not isinstance(s, str):
        return s
    return "".join(c for c in s if c == "\n" or c == "\t" or not (0 <= ord(c) < 32 or 127 <= ord(c) < 160))


def append_contact_record(slug, match, result):
    entry = {
        "hypothesis_slug": slug,
        "source_match_title": match.get("title"),
        "source_match_authors": match.get("researcher_or_authors"),
        "source_match_year": match.get("year"),
        "source_match_url": match.get("url"),
        "resolved": result["resolved"],
        "target_name": _clean(result["target_name"]),
        "institution": _clean(result["institution"]),
        "department": _clean(result["department"]),
        "role_title": _clean(result["role_title"]),
        "email": _clean(result["email"]),
        "email_source_url": result["email_source_url"],
        "profile_url": result["profile_url"],
        "confidence": result["confidence"],
        "notes": _clean(result["notes"]),
        "checked_date": datetime.now(timezone.utc).date().isoformat(),
        "method": "find_researcher_contact.py (gpt-4o-mini + web_search, structured)",
    }
    os.makedirs(os.path.dirname(CONTACTS_PATH), exist_ok=True)
    with open(CONTACTS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def _match_key(hypothesis_slug, authors, url):
    """The real identity of one source match: which hypothesis, which
    real paper (by its real URL -- always unique per paper, unlike the
    author string). Found and fixed 2026-09-02, twice on the same day:

    Fix 1 -- keyed on source_match_authors alone, NOT the resolved
    target_name: the skip-check at call time only ever has the raw
    match's author-list string available (target_name doesn't exist yet
    -- resolving it is the whole point of the call), so a
    target_name-keyed index silently never matched any multi-author
    match.

    Fix 2 -- authors alone still wasn't enough: find_new_evidence.py's
    own honest "never invent a name" discipline means many of its real
    matches legitimately share the exact literal string 'authors not
    specified in excerpt' -- so an authors-only key collapsed every
    such match, across completely different real papers and
    hypotheses, onto one dedup entry. The very next real batch after
    Fix 1 shipped hit this directly: 4 brand-new matches from 4
    different hypotheses all skipped as 'already resolved' because an
    earlier, unrelated match happened to share that same placeholder
    string. A real paper's URL is unique in a way an author string
    is not, so the URL -- scoped to the hypothesis, since the same
    real paper could legitimately be a real match for more than one
    hypothesis -- is the actual identity a 'have we tried this exact
    match before' check needs."""
    return (hypothesis_slug, (url or authors or "").strip().lower())


def load_resolved_matches():
    """Source matches already resolved (successfully or not) in a prior
    run, so a re-run over the same or an overlapping shortlist doesn't
    re-spend real API cost re-searching the same paper again. See
    _match_key's own docstring for the two real dedup-key bugs found
    and fixed here, in order, on the same day."""
    seen = {}
    if os.path.exists(CONTACTS_PATH):
        with open(CONTACTS_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                key = _match_key(rec.get("hypothesis_slug"), rec.get("source_match_authors"), rec.get("source_match_url"))
                if key[1]:
                    seen[key] = rec
    return seen


def matches_for_slug(slug, by_slug):
    e = by_slug.get(slug)
    if not e:
        return None, []
    return e, (e.get("active_research_matches") or [])


def main():
    parser = argparse.ArgumentParser(description="Resolve real institutional contact info for researchers behind this pipeline's own active_research_matches")
    parser.add_argument("slugs", nargs="*")
    parser.add_argument("--all-shortlist", action="store_true", help="Resolve for every slug in outreach/shortlist.json")
    parser.add_argument("--limit", type=int, default=None, help="Cap how many researcher lookups to run this pass")
    parser.add_argument("--force", action="store_true", help="Re-resolve even a name already found in outreach/contacts.jsonl")
    parser.add_argument("--dry-run", action="store_true", help="Print results only; do not write to outreach/contacts.jsonl")
    args = parser.parse_args()

    sys.path.insert(0, PIPELINE_DIR)
    from ledger import load_latest_entries
    by_slug = {e.get("hypothesis_slug"): e for e in load_latest_entries() if e.get("hypothesis_slug")}

    slugs = list(args.slugs)
    if args.all_shortlist:
        if not os.path.exists(SHORTLIST_PATH):
            raise SystemExit(f"{SHORTLIST_PATH} not found — run: python3 score_hypotheses.py --outreach")
        shortlist = json.load(open(SHORTLIST_PATH, encoding="utf-8"))
        slugs.extend(row["slug"] for row in shortlist.get("rows", []) if row.get("slug"))
    if not slugs:
        raise SystemExit("Pass one or more hypothesis slugs, or use --all-shortlist.")

    already = {} if args.force else load_resolved_matches()

    # Flatten to one (slug, match) pair per real active_research_match,
    # skipping slugs with none and (unless --force) names already resolved.
    jobs = []
    skipped_no_matches = []
    for slug in dict.fromkeys(slugs):  # de-dupe, preserve order
        e, matches = matches_for_slug(slug, by_slug)
        if e is None:
            print(f"SKIPPED (not in ledger): {slug}")
            continue
        if not matches:
            skipped_no_matches.append(slug)
            continue
        for m in matches:
            key = _match_key(slug, m.get("researcher_or_authors"), m.get("url"))
            if key in already:
                continue
            jobs.append((slug, e.get("domains", []), m))

    if skipped_no_matches:
        print(f"{len(skipped_no_matches)} slug(s) have no active_research_matches yet (run active_research_check.py first): {', '.join(skipped_no_matches[:5])}{'...' if len(skipped_no_matches) > 5 else ''}")

    if args.limit:
        jobs = jobs[: args.limit]

    if not jobs:
        print("Nothing to resolve (everything already in outreach/contacts.jsonl — pass --force to re-check).")
        return

    print(f"Resolving {len(jobs)} researcher contact(s)...")
    resolved_count = 0
    for i, (slug, domains, m) in enumerate(jobs, 1):
        authors = m.get("researcher_or_authors") or "(unknown)"
        print(f"[{i}/{len(jobs)}] {slug} — {authors[:60]} ...", flush=True)
        try:
            result, usage = resolve_one(authors, m.get("title"), m.get("year"), m.get("url"), domains, slug=slug)
            result = _sanity_check(result, m.get("title"))
            status = "FOUND EMAIL" if result.get("email") else ("RESOLVED (no email)" if result["resolved"] else "NOT FOUND")
            print(f"    {status} — {result.get('target_name')} · {result.get('institution') or '(institution unknown)'} · {usage.total_tokens} tokens", flush=True)
            if result.get("email"):
                print(f"      {result['email']}  (source: {result.get('email_source_url')})")
                resolved_count += 1
            if not args.dry_run:
                append_contact_record(slug, m, result)
        except Exception as ex:
            print(f"    ERROR: {ex}", flush=True)

    print()
    print(f"Done. {resolved_count}/{len(jobs)} real emails found this pass.")
    if not args.dry_run:
        print(f"Written to {CONTACTS_PATH}")
    print("Nothing was sent. Turning a resolved contact into a draft is still the existing outreach/ step.")


if __name__ == "__main__":
    main()
