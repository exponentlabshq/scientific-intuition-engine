# Eureka Engine — Site Build

The web-experience build tooling, committed here (2026-08-29) after living only in an ephemeral
session scratchpad for the site's entire history up to this point — which meant nothing about the
public site could survive or run without that specific session. It can now.

## What's automated vs. not — read `../publish_site.py`'s own docstring for the full reasoning

- **`build_experience.py`** (→ `leaderboard-experience.html`) — fully automated. Pure data render off
  `experience_data.json`, no hand-written prose, always safe to regenerate from the current ledger.
- **`build_landing.py`** (→ `landing.html`) — partially automated. Its stat pills and the
  whitepaper-teaser lede sentence are template placeholders filled by `compute_live_stats()` (reads
  `../verification-log.jsonl` directly) every run. Everything else on the page — hero copy, the
  Darwin/Koestler/Rothenberg story sections, Featured Hypotheses' per-entry "why it matters" prose —
  is untouched hand-written content. `publish_site.py` calls this one.
- **`build_whitepaper.py`** (→ the canonical `umpf_pipeline/whitepaper.html` fragment) — **not**
  wired into `publish_site.py`. Its real numbers are woven into flowing prose sentences ("22
  collided... 10 found... 7 were tested, every one of them, a real 0% survival rate") — a blind
  substitution risks a grammatically or factually broken sentence the moment a count changes in a
  way the original prose didn't anticipate (a refutation surviving, for instance, would falsify "every
  one of them... 0%"). Kept here, committed and runnable, for a deliberate human-reviewed pass —
  same discipline as this whole project applies to anything narrative.
- **`wrap_standalone.py`** — shared by the other two: wraps an Artifact-format fragment (title + style
  + body, no `<html>`/`<head>`) into a full standalone document with the shared site nav injected.

## Running any of these by hand

All three build scripts expect their asset images in `assets/` (relative to `site_build/`, already
committed alongside them) and, for `build_landing.py`, the real ledger one directory up. Run from
`site_build/`:

```
python3 build_experience.py      # writes ../leaderboard-experience.html
python3 build_landing.py         # writes ./landing.html
python3 build_whitepaper.py      # writes ../whitepaper.html (the canonical fragment)
python3 wrap_standalone.py <fragment.html> <output.html> <landing|whitepaper|leaderboard>
```

`output/` (gitignored) is `publish_site.py`'s own staging directory for the two pages it deploys —
not meant to be committed; the deployed copies live in the separate `eureka-engine-web` repo.
