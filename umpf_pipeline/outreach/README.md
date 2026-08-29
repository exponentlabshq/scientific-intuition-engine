# Eureka Engine — Researcher Outreach (Phase 3)

**Status across the board: not yet sent, and never auto-sent.** This mirrors `Deals/sayve/outreach/`'s
exact discipline — one file per contact, explicit confidence-tiered contact info, drafts only, sending
is Michael's call every time, not a pipeline default. This isn't a per-hypothesis judgment call; it's a
fixed property of the system.

## When a hypothesis gets a draft

Only hypotheses that clear Phase 2 as **ADJACENT_ACTIVE** (real, fertile, unclaimed territory — the
actual target state) or **survive adversarial refutation** (2-or-3-of-3 lenses fail to kill the claim)
are candidates for Phase 3. COLLISION, FACT_CHECK_FAIL, and REFUTED hypotheses don't get drafts — there's
no one to write to about a claim that's already established, factually wrong, or didn't survive scrutiny.

## What goes in a draft file

One file per candidate researcher, `[hypothesis-slug]-[researcher-lastname].md`:

1. **The hypothesis** — one paragraph, plain terms, what's being proposed and why it might matter to them specifically.
2. **Why this researcher** — the real, cited connection from Phase 2's search (e.g. "you're a co-author on
   [paper found during verification]") — never a generic "I saw you work in this field."
3. **Contact info + confidence tier** — same discipline as Sayve: "Confirmed, direct" only for an email
   found on the researcher's own institutional page or a paper's own correspondence line; anything
   aggregator-sourced (ResearchGate, ContactOut-style sites) is flagged "unconfirmed" and routed to a
   safer channel (institutional contact form, a co-author's confirmed address) instead of guessed.
4. **The draft itself** — short, respectful, low-pressure. Not a pitch. A real question: "I came across
   this potential connection while doing cross-domain research on [X] and would value your read on it,
   given your work on [Y]." One clear ask: does this collision-check hold up, or is there something
   obvious being missed.
5. **Send Notes** — explicit "NOT SENT — requires Michael's sign-off" banner, every file, no exceptions.

## Sources

- `../verification-log.jsonl` — the ledger this outreach queue is drawn from
- `../faculty-of-interdisciplinary-research.md` — the Frontier Research Group list this queue tracks against
- `../../../Deals/sayve/outreach/README.md` — the pattern this folder is built from
