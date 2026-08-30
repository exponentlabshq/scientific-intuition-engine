#!/usr/bin/env python3
"""
check_ledger_consumers.py -- 10X fix #1 (of the ranked list in
eureka-engine-system-prd.md / the whitepaper's own Limitations section),
built 2026-08-30 specifically to stop Failures 11 and 13 from becoming
Failure 14.

Both of those were the SAME bug, found twice: a script read
verification-log.jsonl itself, raw, line by line, instead of calling
ledger.py's load_latest_entries() -- so a slug that was ever re-verified
counted twice (the old wrong entry and its correction both counted), and
an outreach_sent event (no verdict, but still a raw line) got counted or
even treated as authoritative. ledger.py existed specifically to give
every reader one shared, correct answer to "which entry is current per
slug" -- and two different scripts still found their own way around it,
independently, on the same day. Fixing the two known instances doesn't
stop a third one from happening the same way; only checking for the
*pattern* does.

What this checks, mechanically: every .py file in this pipeline (except
ledger.py itself, and except alt_scoring/ -- see below) that appears to
open verification-log.jsonl and iterate it line by line must also import
from ledger. A file that references the filename only in a comment,
docstring, or prompt string (no real file I/O) is not flagged -- this is
a real, if imperfect, heuristic, not a full static analyzer; it is meant
to catch the actual shape Failures 11 and 13 took, not every conceivable
misuse.

alt_scoring/ is deliberately excluded, not overlooked: per Section 10 of
the whitepaper, that directory holds the self-audit agent's own proposed
scripts, which the pipeline's own hard constraint (audit_agent.py) never
imports or executes automatically. Both files in it (pre_verification_
filter.py, pre_verification_filter_v2.py) are exactly the two real,
disclosed, NOT-adopted proposals Section 10 and Failure 5 describe --
editing them to use ledger.py would misrepresent what actually happened
(a rejected proposal, kept as the honest record of why it was rejected),
not fix a live risk. They are real raw-ledger readers and would fail this
check if it applied to them; it deliberately does not, and this file says
so rather than silently excluding them.

Usage:
    python3 check_ledger_consumers.py          # human-readable report, exit 1 if any violation
    python3 check_ledger_consumers.py --quiet  # exit code only, for a pre-publish hook
"""
import ast
import os
import sys

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
LEDGER_FILENAME = "verification-log.jsonl"

# Directories this check does not walk into, and why. Not a general-purpose
# ignore list -- every entry needs the same disclosed reasoning alt_scoring/
# gets above, or it doesn't belong here.
EXCLUDED_DIRS = {
    "alt_scoring",   # self-audit agent's own rejected proposals -- see module docstring
    ".git",
    "__pycache__",
    "node_modules",
}

RAW_ITERATION_MARKERS = ("for line in", "readlines()", ".splitlines()")


def find_py_files():
    for root, dirs, files in os.walk(PIPELINE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for fn in files:
            if fn.endswith(".py"):
                yield os.path.join(root, fn)


def references_ledger_filename_as_code(source: str) -> bool:
    """True if the ledger filename appears somewhere other than a comment,
    docstring, or module-level string literal that's never opened -- i.e.
    real evidence the file does its own I/O against it, not just mentions
    it. Heuristic: parse the AST, look for the literal string as an
    argument to open(), or assigned to a name that is later passed to
    open()."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return LEDGER_FILENAME in source  # fall back to the crude check rather than silently skip

    literal_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for arg in ast.walk(node.value):
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and LEDGER_FILENAME in arg.value:
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            literal_names.add(target.id)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
            if node.args:
                first = node.args[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str) and LEDGER_FILENAME in first.value:
                    return True
                if isinstance(first, ast.Name) and first.id in literal_names:
                    return True
    return False


def imports_ledger(source: str) -> bool:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return "ledger" in source
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "ledger":
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "ledger":
                    return True
    return False


def check_file(path: str):
    """Returns None if clean/not applicable, else a violation reason string."""
    if os.path.basename(path) == "ledger.py":
        return None
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    if LEDGER_FILENAME not in source:
        return None
    if not references_ledger_filename_as_code(source):
        return None  # mentioned only in a comment/docstring/prompt string -- not a real reader
    if imports_ledger(source):
        return None
    # One more real exception: a file that only ever WRITES (appends new
    # lines) never needs dedup -- the ledger's append-only write side is
    # always safe regardless of reader logic. But every real case found so
    # far (Failures 11, 13) was a reader, and distinguishing write-only from
    # read-then-aggregate reliably from source alone isn't safe to automate
    # -- a false negative here is exactly how this bug slips through again.
    # Flag it; a human reviewing the report makes the call, same discipline
    # as every other check in this pipeline that defaults to raising a flag
    # over staying silent.
    return "reads verification-log.jsonl directly, iterating raw lines, with no `from ledger import` anywhere in the file"


def main():
    quiet = "--quiet" in sys.argv
    violations = []
    checked = 0
    for path in sorted(find_py_files()):
        checked += 1
        reason = check_file(path)
        if reason:
            violations.append((os.path.relpath(path, PIPELINE_DIR), reason))

    if not quiet:
        print(f"Checked {checked} Python files under {PIPELINE_DIR} (excluding {', '.join(sorted(EXCLUDED_DIRS))}).")
        if violations:
            print(f"\n{len(violations)} ledger-consumer contract violation(s):\n")
            for relpath, reason in violations:
                print(f"  {relpath}\n    {reason}\n")
            print("Fix: import load_latest_entries from ledger.py instead of reading verification-log.jsonl")
            print("raw, or -- if this really is write-only/append-only access that never needs dedup --")
            print("confirm that by hand and add a one-line comment saying so explicitly, next to the open() call.")
        else:
            print("\nClean: every consumer of verification-log.jsonl outside ledger.py and alt_scoring/ goes through ledger.py.")

    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
