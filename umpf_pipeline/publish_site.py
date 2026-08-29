#!/usr/bin/env python3
"""
publish_site.py — keep the published Eureka Engine site in sync with the
real ledger, unattended.

Scope, deliberately bounded:

  - leaderboard-experience.html / the deployed leaderboard.html: FULLY
    automated. This page is a pure render of experience_data.json -- no
    hand-written prose lives in it, so regenerating it from the current
    ledger is always safe and always correct.

  - landing.html: PARTIALLY automated. Its stat pills and the
    whitepaper-teaser lede sentence are now template placeholders
    (site_build/build_landing.py's compute_live_stats()) that get filled
    from the real ledger every run. Everything else on the page -- the
    hero copy, the Koestler/Rothenberg story sections, the Featured
    Hypotheses "why it matters" prose -- is untouched hand-written content,
    deliberately left alone. Rewriting narrative prose to match new rankings
    is a job for a human (or an explicit future session), not a silent
    string-replace.

  - whitepaper.html: NOT included. Its numbers are woven into flowing
    prose sentences ("22 collided... 10 found... 7 were tested..."), not
    isolated fields -- a blind number substitution would produce
    grammatically or factually broken sentences the moment counts change
    in a way the original prose didn't anticipate (e.g. a refutation
    survival, which would falsify "every one of them... 0% survival").
    Regenerating it stays a deliberate, human-reviewed pass.
    build_whitepaper.py is committed to site_build/ for that manual use,
    but this script never calls it.

Deployment: writes are staged under site_build/output/ first, diffed
against the current eureka-engine-web/ files, and only copied over (then
committed + pushed in that separate repo) if something actually changed --
never a no-op commit.

Usage:
    python3 publish_site.py                 # build, deploy, commit+push
    python3 publish_site.py --dry-run        # build to site_build/output/, diff, change nothing
    python3 publish_site.py --no-push        # build + commit locally, skip git push
"""
import argparse
import filecmp
import os
import subprocess
import sys
from datetime import datetime, timezone

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_BUILD_DIR = os.path.join(PIPELINE_DIR, "site_build")
OUTPUT_DIR = os.path.join(SITE_BUILD_DIR, "output")
WEB_REPO_DIR = os.path.abspath(os.path.join(PIPELINE_DIR, "..", "eureka-engine-web"))
PUBLISH_LOG_PATH = os.path.join(PIPELINE_DIR, "publish_log.jsonl")
PYTHON = sys.executable


def run(cmd, cwd):
    print(f"$ (cwd={os.path.relpath(cwd, PIPELINE_DIR)}) {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"Command failed ({result.returncode}): {' '.join(cmd)}")
    return result.stdout


def build():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Refresh the raw data behind the leaderboard experience -- canonical
    #    location is the pipeline root, matching every prior manual run.
    run([PYTHON, "assemble_experience_data.py"], cwd=PIPELINE_DIR)

    # 2. Rebuild the full interactive leaderboard fragment from that data.
    run([PYTHON, "site_build/build_experience.py"], cwd=PIPELINE_DIR)
    # build_experience.py writes leaderboard-experience.html to its cwd (PIPELINE_DIR).

    # 3. Wrap it into a deployable standalone doc (adds the shared nav, <head>, etc.)
    leaderboard_fragment = os.path.join(PIPELINE_DIR, "leaderboard-experience.html")
    leaderboard_deployed = os.path.join(OUTPUT_DIR, "leaderboard.html")
    run([PYTHON, "site_build/wrap_standalone.py", leaderboard_fragment, leaderboard_deployed, "leaderboard"], cwd=PIPELINE_DIR)

    # 4. Rebuild landing.html -- template placeholders filled from the live
    #    ledger by build_landing.py's own compute_live_stats(); everything
    #    else on the page is unchanged hand-written content.
    run([PYTHON, "build_landing.py"], cwd=SITE_BUILD_DIR)
    landing_built = os.path.join(SITE_BUILD_DIR, "landing.html")
    landing_deployed = os.path.join(OUTPUT_DIR, "landing.html")
    with open(landing_built, "r", encoding="utf-8") as f:
        content = f.read()
    with open(landing_deployed, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nBuilt: {leaderboard_deployed}\nBuilt: {landing_deployed}")
    print("(whitepaper.html intentionally not rebuilt -- see this script's own docstring)")
    return {"leaderboard.html": leaderboard_deployed, "landing.html": landing_deployed}


def changed_files(built: dict) -> dict:
    """Diff each freshly-built file against what's currently deployed.
    Returns only the ones that actually differ -- never stage a no-op copy
    or an empty commit."""
    changed = {}
    for name, built_path in built.items():
        deployed_path = os.path.join(WEB_REPO_DIR, name)
        if not os.path.exists(deployed_path) or not filecmp.cmp(built_path, deployed_path, shallow=False):
            changed[name] = built_path
    return changed


def deploy(changed: dict, no_push: bool):
    for name, built_path in changed.items():
        deployed_path = os.path.join(WEB_REPO_DIR, name)
        with open(built_path, "rb") as src, open(deployed_path, "wb") as dst:
            dst.write(src.read())
        print(f"Deployed: {name}")

    run(["git", "add"] + list(changed.keys()), cwd=WEB_REPO_DIR)
    commit_msg = (
        f"Auto-publish: {', '.join(changed.keys())} regenerated from ledger\n\n"
        f"Generated by publish_site.py, {datetime.now(timezone.utc).isoformat()}. "
        f"Data-driven pages only (leaderboard experience, landing page stat fields) -- "
        f"whitepaper.html is never touched by this script.\n\n"
        f"Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
    )
    run(["git", "commit", "-m", commit_msg], cwd=WEB_REPO_DIR)
    if not no_push:
        run(["git", "push"], cwd=WEB_REPO_DIR)
    else:
        print("(--no-push: committed locally, not pushed)")


def main():
    parser = argparse.ArgumentParser(description="Rebuild and deploy the data-driven parts of the Eureka Engine site")
    parser.add_argument("--dry-run", action="store_true", help="Build to site_build/output/ and report what would change; deploy nothing")
    parser.add_argument("--no-push", action="store_true", help="Commit in eureka-engine-web but don't git push")
    args = parser.parse_args()

    built = build()
    changed = changed_files(built)

    if not changed:
        print("\nNo changes vs. currently deployed site -- nothing to publish.")
        return

    print(f"\nChanged: {list(changed.keys())}")
    if args.dry_run:
        print("(dry run -- not deploying or committing)")
        return

    deploy(changed, args.no_push)

    with open(PUBLISH_LOG_PATH, "a", encoding="utf-8") as f:
        import json
        f.write(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "changed": list(changed.keys()),
            "pushed": not args.no_push,
        }) + "\n")
    print("\nPublish complete.")


if __name__ == "__main__":
    main()
