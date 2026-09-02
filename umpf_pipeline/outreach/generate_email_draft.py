#!/usr/bin/env python3
"""
generate_email_draft.py -- COA 8b: automates the exact process that
produced the three hand-drafted emails this pipeline's own template is
now locked to (email-reactive-control-network-enciso.md,
email-creative-versioning-sterman.md,
email-neurogrid-optimization-papageorgiou.md). Same architecture as
find_researcher_contact.py and find_new_evidence.py: one OpenAI
structured call per target, `web_search` enabled so it can verify a
paper's real venue/full author list the same way that was done by hand
for each of the three examples -- never inventing what it can't confirm.

Reads outreach/outreach_queue.json (built by prioritize_outreach.py),
drafts the top N not-yet-drafted candidates, writes each to
outreach/emails/email-<slug>-<surname>.md in the exact locked format:
identity line -> one bolded direct question grounded ONLY in the
hypothesis's own fusion sentence/falsifiable prediction -> one line
citing the real paper -> syndicate line -> sign-off. No Eureka Engine
explainer, no "independent convergence" hedging -- this is the leaner
template that actually survived to real sends (Aronson/Frey/Phillips),
per that email's own note.

Deliberately does NOT add the American Reindustrialization PS
automatically -- that was flagged as an open, undecided design
question (does it apply to every email, or only domains where it's a
plausible fit?) and this script does not resolve it silently. Add it
by hand per email until that's decided.

This script only ever WRITES a file to outreach/emails/. It never
sends anything -- same NOT SENT discipline as every other script in
this pipeline. Every draft needs a human Send checklist pass before
it goes anywhere near an inbox.

Usage:
    python3 outreach/generate_email_draft.py --limit N [--dry-run]
    python3 outreach/generate_email_draft.py --slug <hypothesis_slug> --email <target email>
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from openai import OpenAI

PIPELINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PIPELINE_DIR)
import token_tracker

QUEUE_PATH = os.path.join(PIPELINE_DIR, "outreach", "outreach_queue.json")
EMAILS_DIR = os.path.join(PIPELINE_DIR, "outreach", "emails")
EXPERIENCE_PATH = os.path.join(PIPELINE_DIR, "experience_data.json")

load_dotenv("/Users/michaeljagdeo/Downloads/talentOS-2026/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set — add it to the vault-root .env")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"

DRAFT_SCHEMA = {
    "type": "object",
    "properties": {
        "subject": {
            "type": "string",
            "description": "Short subject line, phrased as a direct question about the specific mechanism -- matches the style of 'Kalman-filtered feedback as a reaction network's own control law?' Never mentions Eureka Engine or the researcher's own paper title verbatim.",
        },
        "opening_question": {
            "type": "string",
            "description": (
                "ONE sentence, phrased as a direct question ('Can X function as Y...'), grounded "
                "STRICTLY in the hypothesis's own fusion sentence and falsifiable prediction as given "
                "-- never a fact, mechanism, or claim not actually present in that text. No hedging "
                "language ('It independently proposed...', 'Flagging it as...', 'with no knowledge of "
                "your paper'). No mention of Eureka Engine, AI, or how the idea was generated -- the "
                "recipient should read this as a sharp scientific question, not a pitch about a system."
            ),
        },
        "paper_authors_verified": {
            "type": "string",
            "description": "Full real author list for the cited paper, found via web_search on its title/URL. Empty string if not confirmable -- never invent names beyond what was already given.",
        },
        "paper_venue": {
            "type": "string",
            "description": "Real journal/conference/preprint-server name for the cited paper, found via web_search. Empty string if not confirmable.",
        },
        "paper_year_verified": {
            "type": "string",
            "description": "Real publication year if found via web_search and different from or absent in the year already given. Empty string if the given year is already correct or nothing better was found.",
        },
        "verification_notes": {
            "type": "string",
            "description": "1-2 sentences: what was actually checked and found (or not found) via web_search for this paper's bibliographic details.",
        },
    },
    "required": ["subject", "opening_question", "paper_authors_verified", "paper_venue", "paper_year_verified", "verification_notes"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = (
    "You are drafting ONE short outreach email's core content -- a subject line and one "
    "bolded opening question -- to a real academic researcher, on behalf of Exponent Labs' "
    "Eureka Engine. You are given: (1) a real, AI-generated cross-domain research hypothesis "
    "(its fusion sentence and falsifiable prediction), and (2) a real paper by the recipient "
    "that a separate discovery step already matched as working related territory.\n\n"
    "Your opening_question must be a single, sharp, direct question -- 'Can X function as Y "
    "...?' -- built ONLY from the hypothesis's own stated fusion sentence and falsifiable "
    "prediction. Do not add mechanism, motivation, or claims that are not actually present in "
    "that text; do not soften it with hedging phrases like 'it was independently proposed' or "
    "'flagging this as convergence, not priority' -- state the question plainly, the way one "
    "scientist would ask another. Never mention Eureka Engine, AI, hypothesis generation, or "
    "how the question was produced inside this sentence -- that context lives elsewhere in the "
    "email, not in the question itself.\n\n"
    "You also have web_search available: use it to verify the cited paper's real publication "
    "venue and full author list from its title/URL. The single most important rule, identical "
    "to this pipeline's other research tools: only report a venue, author name, or year if you "
    "actually found it written on a real page search returned -- an empty string is the correct, "
    "honest answer when nothing is confirmable, never a guess."
)


def load_hypothesis_content(slug):
    with open(EXPERIENCE_PATH, encoding="utf-8") as f:
        data = json.load(f)
    entries = data if isinstance(data, list) else data.get("entries", data.get("rows", []))
    for e in entries:
        if e.get("key") == slug:
            return e.get("hypothesis_content", "")
    return ""


def load_queue():
    with open(QUEUE_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_already_drafted():
    import glob
    slugs = set()
    for path in glob.glob(os.path.join(EMAILS_DIR, "*.md")):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for m in re.finditer(r"\*\*Hypothesis:\*\*\s*`([^`]+)`", text):
            slugs.add(m.group(1))
    return slugs


def draft_one(candidate):
    hyp_content = load_hypothesis_content(candidate["hypothesis_slug"])
    if not hyp_content:
        return None, None

    text = (
        f"HYPOTHESIS (this pipeline's own AI-generated hypothesis -- draw the opening_question "
        f"ONLY from its own final, specific, testable claim below -- labeled 'Fusion sentence' + "
        f"'Falsifiable prediction' for a two-domain hypothesis, or 'Simultaneous-hold sentence' + "
        f"'Falsifiable prediction' for a single-domain Janusian/paradox hypothesis -- never a "
        f"generic restatement of the domain or topic name itself):\n\n"
        f"{hyp_content}\n\n"
        f"---\n\n"
        f"REAL PAPER a separate discovery step matched as related, working territory:\n"
        f"Title: {candidate['source_match_title']}\n"
        f"Authors (as already known): {candidate['source_match_authors']}\n"
        f"Year (as already known): {candidate['source_match_year'] or 'unknown'}\n"
        f"URL: {candidate['source_match_url']}\n\n"
        f"RECIPIENT: {candidate['target_name']}, {candidate['institution'] or '(institution unknown)'}\n\n"
        "Draft the subject line and opening_question. Verify the paper's real venue and full "
        "author list via web_search on its title/URL."
    )
    resp = client.responses.create(
        model=MODEL,
        tools=[{"type": "web_search"}],
        instructions=SYSTEM_PROMPT,
        input=text,
        max_output_tokens=1500,
        text={"format": {"type": "json_schema", "name": "email_draft", "schema": DRAFT_SCHEMA, "strict": True}},
    )
    token_tracker.log_usage("outreach_email_draft", MODEL, resp.usage, hypothesis_slug=candidate["hypothesis_slug"])
    return json.loads(resp.output_text), resp.usage


def _surname(name):
    parts = (name or "unknown").strip().split()
    return re.sub(r"[^a-z0-9]", "", parts[-1].lower()) if parts else "unknown"


def _short_slug(hypothesis_slug):
    s = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", hypothesis_slug)
    s = re.sub(r"^(homospatial|janusian)-", "", s)
    return s[:50].rstrip("-")


_KNOWN_AGGREGATOR_SUFFIXES = {"PMC", "PubMed", "ScienceDirect", "ResearchGate", "SpringerLink"}


def _clean_title(title):
    """Strip a venue/aggregator artifact search results sometimes carry
    on a paper title. Pipe-separated: 'Foo Bar Baz | Microsystems &
    Nanoengineering | Springer Nature Link' -> 'Foo Bar Baz' (found
    2026-09-02, first real generation test run) -- but the junk isn't
    always a trailing segment: 'Frontiers | Toward a dual-pathway
    model of neuroplastic adaptation in sport...' has the venue's own
    BRAND NAME as a PREFIX instead (found the very next batch, same
    day) -- an earlier version of this function that always kept the
    first pipe segment shipped 'Frontiers' itself as the paper's
    title. Neither position is reliable, so instead keep whichever
    pipe segment is actually the longest -- a real title is virtually
    always much longer than a one-or-two-word venue/brand name
    ('Frontiers', 'Springer Nature Link', 'ScienceDirect'), checked
    against every real pipe-separated title seen in this pipeline's
    data before trusting the heuristic.

    Dash-separated ('DynKGRAG: ... - ScienceDirect' -> 'DynKGRAG:
    ...') is NOT safe to cut blindly the same way -- real titles
    legitimately use dashes as internal punctuation ('State-of-the-
    art', subtitle separators) -- so only cut a trailing ' - X' when X
    matches a real, surveyed list of this pipeline's actual
    aggregator-site suffixes (10 real PMC occurrences, 3 ScienceDirect,
    1 PubMed as of 2026-09-02), never a blanket dash split."""
    if not title:
        return title
    if " | " in title:
        title = max(title.split(" | "), key=len).strip()
    for suffix in _KNOWN_AGGREGATOR_SUFFIXES:
        if title.endswith(f" - {suffix}"):
            title = title[: -(len(suffix) + 3)].strip()
            break
    return title


_SURNAME_STOPWORDS = {"jr", "sr", "ii", "iii", "phd", "md"}


_INSTITUTION_WORDS = {
    "university", "universidad", "universit", "institute", "institut", "college",
    "department", "dept", "laboratory", "lab", "labs", "center", "centre", "school",
    "corp", "corporation", "inc", "llc", "gmbh", "ltd", "foundation", "hospital",
    "faculty", "academy", "polytechnic", "national", "research",
}


def _looks_like_person_name(s):
    """Real bug found 2026-09-02, same batch as the JSON-blob one, same
    root cause (the model padding out an author slot with SOMETHING
    rather than admitting it only confirmed one real name): for a
    single-author paper, 'Your paper with Bandirma Onyedi Eylul
    University' shipped -- the recipient's own institution cited as if
    it were a co-author's name. A real person's name is 1-4 words, no
    digits, and never contains an institution-shaped word; check all
    three rather than trust the field's own label."""
    s = s.strip()
    if not s or any(ch.isdigit() or ch in '{}[]":' for ch in s):
        return False
    words = s.split()
    if not (1 <= len(words) <= 4):
        return False
    lower_words = {w.strip(".,").lower() for w in words}
    if lower_words & _INSTITUTION_WORDS:
        return False
    return True


def _clean_author_list(authors_str):
    """Splits a raw authors string on common separators and drops any
    segment that doesn't pass _looks_like_person_name -- the shared
    cleaning step both the metadata citation line and the body's
    co-author clause build on, so an institution name or other
    non-person artifact can never reach either one. Returns a list of
    real name strings (possibly empty)."""
    if not authors_str or authors_str == "authors not specified in excerpt":
        return []
    parts = re.split(r",|&|\band\b", authors_str)
    return [p for p in (p.strip().strip(".") for p in parts) if p and _looks_like_person_name(p)]


def _coauthors_excluding_recipient(authors_str, recipient_name):
    """Real bug found 2026-09-02, first generation test run: an email to
    Junhui Wu cited 'Your paper with Junhui Wu, Guangya Zhou' -- citing
    the recipient as their own co-author, because the equality check
    only caught an exact full-string match, not a name appearing inside
    a real multi-author list. Cleans via _clean_author_list first (so
    an institution-shaped artifact is never treated as a co-author
    either), then drops whoever shares the recipient's surname, and
    returns the real remaining co-authors (or empty if none)."""
    recipient_surname = _surname(recipient_name)
    others = [p for p in _clean_author_list(authors_str) if _surname(p) != recipient_surname]
    return ", ".join(others)


def _looks_like_real_author_list(s):
    """Real bug found 2026-09-02, first 5-candidate batch: for a paper
    with 10 authors where only the first was actually confirmable, the
    model returned paper_authors_verified as a literal, malformed
    JSON-shaped string -- '{"author1":"Adem Korkmaz","author2":"[Author
    2]",...}' -- rather than either the one real name it found or an
    empty string. Nothing in the schema or prompt forbade this shape,
    and it shipped straight into a real email's citation line
    ('Your paper with "author2":"[Author 2]", ...') before being
    caught by hand. A real name list is plain text -- these characters
    should never appear in one; reject and fall back to the
    already-known source_match_authors (or empty) rather than trust it."""
    return not any(ch in s for ch in "{}[]\"")


def write_email_file(candidate, draft):
    surname = _surname(candidate["target_name"])
    short = _short_slug(candidate["hypothesis_slug"])
    fname = f"email-{short}-{surname}.md"
    path = os.path.join(EMAILS_DIR, fname)
    if os.path.exists(path):
        return None  # never overwrite an existing draft

    title = _clean_title(candidate["source_match_title"])
    verified_authors = draft["paper_authors_verified"]
    if verified_authors and not _looks_like_real_author_list(verified_authors):
        verified_authors = ""
    authors = verified_authors or candidate["source_match_authors"] or ""
    year = draft["paper_year_verified"] or candidate["source_match_year"] or ""
    venue = draft["paper_venue"]
    clean_authors = _clean_author_list(authors)  # institution/JSON-artifact-free, recipient still included
    coauthors = _coauthors_excluding_recipient(authors, candidate["target_name"])

    cite_bits = []
    if clean_authors:
        cite_bits.append(", ".join(clean_authors))
    cite_bits.append(f'"{title}"')
    if venue:
        cite_bits.append(f"*{venue}*")
    if year:
        cite_bits.append(str(year))
    citation_line = ", ".join(cite_bits) + f" — {candidate['source_match_url']}"

    # The one-sentence citation used inside the email body itself -- kept
    # separate from the metadata block's fuller citation_line above, same
    # split the three hand-drafted examples use. Uses coauthors (recipient
    # already excluded), never the raw authors string, so the recipient is
    # never cited as their own co-author.
    body_cite_prefix = f"Your{f' {year}' if year else ''} paper{f' with {coauthors}' if coauthors else ''}"

    content = f"""# Email — {candidate['hypothesis_slug']} → {candidate['target_name']}

**Status:** DRAFT — NOT SENT (auto-generated by generate_email_draft.py, needs human review before send)
**Hypothesis:** `{candidate['hypothesis_slug']}`
**Match source:** {citation_line}
**Contact source:** resolved via `find_researcher_contact.py`, HIGH confidence
**Generation notes:** {draft['verification_notes']}

---

**From:** Mike Jagdeo \\<private@exponentlabs.ai\\>
**To:** {candidate['target_name']} \\<{candidate['email']}\\>
**Subject:** {draft['subject']}

---

Prof. {candidate['target_name'].split()[-1] if candidate['target_name'] else 'Researcher'},

I'm with Exponent Labs' Eureka Engine.

**{draft['opening_question']}** {body_cite_prefix}, "{title}," looks like it's addressing exactly this territory.

We have a syndicate of investors.

Michael Jagdeo
Exponent Labs LLC - Eureka Engine
private@exponentlabs.ai

---

## Send checklist

- [x] Real contact info found and verified (`{candidate['email']}`, HIGH confidence)
- [ ] **Human review: does the opening question actually read as sharp and specific, not templated?**
- [ ] Sign-off Michael/Rocky
- [ ] Send
- [ ] Date sent:
- [ ] Log ledger `outreach_status` on reply
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return fname


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=3, help="How many drafts to generate this run (default 3 -- deliberately small, review before scaling)")
    parser.add_argument("--dry-run", action="store_true", help="Print drafts only; do not write files")
    args = parser.parse_args()

    queue = load_queue()
    already = load_already_drafted()
    todo = [c for c in queue if c["hypothesis_slug"] not in already][: args.limit]

    if not todo:
        print("Nothing to draft — queue is empty or everything eligible is already drafted.")
        return

    print(f"Drafting {len(todo)} email(s)...\n")
    written = 0
    for i, c in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {c['hypothesis_slug']} -> {c['target_name']} <{c['email']}> ...")
        draft, usage = draft_one(c)
        if draft is None:
            print("    SKIPPED (no hypothesis_content found)")
            continue
        print(f"    Subject: {draft['subject']}")
        print(f"    Question: {draft['opening_question']}")
        if draft["paper_venue"] or draft["paper_authors_verified"]:
            print(f"    Verified: venue={draft['paper_venue'] or '(none found)'} authors={draft['paper_authors_verified'] or '(none found)'}")
        if not args.dry_run:
            fname = write_email_file(c, draft)
            if fname:
                print(f"    Written: outreach/emails/{fname}")
                written += 1
            else:
                print("    SKIPPED (file already exists)")
        print()

    print(f"Done. {written} draft(s) written. Nothing was sent — every file needs a human Send checklist pass.")


if __name__ == "__main__":
    main()
