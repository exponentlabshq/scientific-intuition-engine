#!/usr/bin/env python3
"""
COA 2d — Sharpen → re-verify ritual (operator tool).

Raw ADJACENT_ACTIVE often encodes a *soft* fusion that looks sendable but
collapses to near-known prior art under denser search. Lightning ×2
(Resonant Swarm, Magneto-Operant, 2026-08-29): closed-loop sharpen +
denser re-verify splits soft (near-COLLISION) from hard (still adjacent)
before Phase 3 packets waste a researcher's time.

This script does NOT invent science unsupervised. It:
  1. Extracts soft claim from §3/§4
  2. Requires --hard-claim / --chimera / --soft-retired (or --checklist-only)
  3. Writes revision banner + hard search-query block into the hyp file
  4. Emits verification stub path + checklist for Exa/Tavily re-verify

Usage:
    python3 sharpen_hypothesis.py path/to/hyp.md --checklist-only
    python3 sharpen_hypothesis.py path/to/hyp.md \\
        --soft-retired "robots communicate with sound" \\
        --chimera "Resonant Swarm (acoustic blackboard)" \\
        --hard-claim "S↔R closed loop; chamber geometry change" \\
        --apply

Exemplars:
    hypotheses/2026-08-29-homospatial-swarm-robotics-x-physical-acoustic-resonance.md
    hypotheses/2026-08-29-homospatial-behavioral-psychology-x-physical-magnetic-field-control.md

Send-ready gate: see outreach/README.md — no packet without hypothesis_revision
banner AND a sharpened verification that names soft vs hard.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
HYP_DIR = os.path.join(HERE, "hypotheses")
VER_DIR = os.path.join(HERE, "verifications")


def resolve_path(arg: str) -> str:
    if os.path.isfile(arg):
        return os.path.abspath(arg)
    slug = arg.replace(".md", "")
    candidate = os.path.join(HYP_DIR, f"{slug}.md")
    if os.path.isfile(candidate):
        return candidate
    raise SystemExit(f"Hypothesis not found: {arg}")


def extract_section(text: str, heading_substr: str) -> str:
    """Pull body under a ## heading containing heading_substr until next ##."""
    pattern = rf"(^##[^\n]*{re.escape(heading_substr)}[^\n]*\n)(.*?)(?=^##|\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return (m.group(2).strip() if m else "")


def soft_claim_preview(text: str) -> dict:
    return {
        "section3": extract_section(text, "Emergent") or extract_section(text, "Third Thing")
                    or extract_section(text, "Hypothesis")[:800],
        "section4": extract_section(text, "The Hypothesis") or extract_section(text, "Hypothesis"),
        "already_sharpened": bool(re.search(r"\*\*Revision\*\*:", text))
                             or "human-sharpened" in text.lower()
                             or "closed-loop" in text[:1200].lower(),
    }


def slug_from_path(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def print_checklist(path: str, preview: dict) -> None:
    print("=" * 60)
    print("COA 2d — Sharpen → re-verify checklist")
    print("=" * 60)
    print(f"File: {path}")
    print(f"Already sharpened banner: {preview['already_sharpened']}")
    print()
    print("--- Soft claim (§3 / emergent) ---")
    print(preview["section3"][:900] or "(empty)")
    print()
    print("--- Soft claim (§4 / hypothesis) ---")
    print(preview["section4"][:900] or "(empty)")
    print()
    print("Required before --apply:")
    print("  [ ] Name soft claim to retire (one line)")
    print("  [ ] Name hard chimera (one closed-loop identity)")
    print("  [ ] Hard claim: both directions nonzero (∂Y/∂X and ∂X/∂Y)")
    print("  [ ] Controls: A/B, yoked, chamber-geometry, or schedule remapping")
    print("  [ ] Hard search queries (not the soft ones)")
    print("  [ ] Exa/Tavily re-verify soft vs hard; append ledger")
    print("  [ ] Packet ONLY if hard still ADJACENT_ACTIVE — hard claim only")
    print()
    print("Exemplars: Swarm Robotics × Acoustic Resonance; Magneto-Operant Schedule")


def build_revision_banner(soft_retired: str, note: str) -> str:
    today = date.today().isoformat()
    return (
        f"**Revision**: {today} — human-sharpened closed-loop formulation "
        f"(COA 2d). Soft “{soft_retired}” framing retired; {note}"
    )


def inject_revision_banner(text: str, banner: str) -> str:
    """Insert or replace **Revision**: line after Framework line."""
    if re.search(r"\*\*Revision\*\*:", text):
        return re.sub(r"\*\*Revision\*\*:.*", banner, text, count=1)
    # After Framework line
    if "**Framework**:" in text:
        return re.sub(
            r"(\*\*Framework\*\*:[^\n]*\n)",
            r"\1" + banner + "\n",
            text,
            count=1,
        )
    # After first heading block
    parts = text.split("\n\n", 1)
    if len(parts) == 2:
        return parts[0] + "\n" + banner + "\n\n" + parts[1]
    return banner + "\n\n" + text


def append_hard_query_block(
    text: str, soft_retired: str, chimera: str, hard_claim: str, slug: str
) -> str:
    today = date.today().isoformat()
    block = f"""

---

## COA 2d — Soft vs Hard (operator)

**Sharpened**: {today}  
**Soft claim retired**: {soft_retired}  
**Hard chimera**: {chimera}  
**Hard claim**: {hard_claim}

### Hard search queries (re-verify these — not the soft ones)

1. "{chimera} {hard_claim}"
2. "{soft_retired} prior art OR review"
3. "yoked control OR chamber geometry OR schedule remapping {chimera}"
4. Named adjacent labs / frameworks from first denser search pass

### Re-verify stub

Write: `verifications/{slug}-verification.md` with sections:
Soft near-COLLISION neighbors | Hard claim status | Actively researched contact

Packet send-ready only if hard verdict remains ADJACENT_ACTIVE.
"""
    if "## COA 2d — Soft vs Hard" in text:
        text = re.sub(
            r"\n---\n\n## COA 2d — Soft vs Hard \(operator\).*",
            "",
            text,
            flags=re.DOTALL,
        )
    return text.rstrip() + block


def write_verification_stub(
    slug: str, soft_retired: str, chimera: str, hard_claim: str
) -> str:
    os.makedirs(VER_DIR, exist_ok=True)
    path = os.path.join(VER_DIR, f"{slug}-verification.md")
    # Do not overwrite a full sharpened verification
    if os.path.exists(path):
        existing = open(path, encoding="utf-8").read()
        if "Sharpened" in existing or "soft vs hard" in existing.lower() or "Lightning" in existing:
            print(f"  (keeping existing verification: {path})")
            return path
    stub = f"""# Verification: {slug} (COA 2d stub — fill after Exa)

**Verifies**: `hypotheses/{slug}.md`  
**Verified**: {date.today().isoformat()} · **Method**: Exa (operator COA 2d) — STUB, not a verdict  
**Hypothesis revision**: closed-loop / hard chimera

## Soft claim retired
{soft_retired}

## Hard chimera
{chimera}

## Hard claim
{hard_claim}

## Verdict: **PENDING_SHARPEN_REVERIFY**

Replace this stub after denser search:

| Soft neighbors (near-COLLISION?) | Hard claim status | Contact lab |
|---|---|---|
| _fill_ | ADJACENT_ACTIVE / COLLISION / dismiss | _fill_ |

## Queries
1. (hard) 
2. (soft prior art)
3. (controls / yoked / chamber)
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(stub)
    return path


def main():
    parser = argparse.ArgumentParser(description="COA 2d sharpen → re-verify ritual")
    parser.add_argument("hypothesis", help="Path or slug of hypothesis .md")
    parser.add_argument("--checklist-only", action="store_true", help="Print checklist; write nothing")
    parser.add_argument("--soft-retired", type=str, help="One-line soft claim to retire")
    parser.add_argument("--chimera", type=str, help="Named hard chimera identity")
    parser.add_argument("--hard-claim", type=str, help="Bidirectional closed-loop hard claim")
    parser.add_argument(
        "--note",
        type=str,
        default="bidirectional closed-loop claim is load-bearing.",
        help="Short clause after 'retired;' in revision banner",
    )
    parser.add_argument("--apply", action="store_true", help="Write banner + soft/hard block + verification stub")
    args = parser.parse_args()

    path = resolve_path(args.hypothesis)
    text = open(path, encoding="utf-8").read()
    preview = soft_claim_preview(text)
    print_checklist(path, preview)

    if args.checklist_only or not args.apply:
        if not args.apply:
            print("(pass --apply with --soft-retired/--chimera/--hard-claim to write)")
        return

    missing = [k for k, v in {
        "--soft-retired": args.soft_retired,
        "--chimera": args.chimera,
        "--hard-claim": args.hard_claim,
    }.items() if not v]
    if missing:
        raise SystemExit(f"--apply requires: {', '.join(missing)}")

    slug = slug_from_path(path)
    banner = build_revision_banner(args.soft_retired, args.note)
    new_text = inject_revision_banner(text, banner)
    new_text = append_hard_query_block(
        new_text, args.soft_retired, args.chimera, args.hard_claim, slug
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"\n✅ Wrote revision into {path}")

    stub = write_verification_stub(slug, args.soft_retired, args.chimera, args.hard_claim)
    print(f"✅ Verification stub: {stub}")
    print("Next: Exa denser search → fill verification → append ledger → packet if hard ADJACENT.")


if __name__ == "__main__":
    main()
