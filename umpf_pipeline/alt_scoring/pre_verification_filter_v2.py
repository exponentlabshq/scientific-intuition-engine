"""
EXPERIMENTAL -- proposed by audit_agent.py on 2026-08-29.
NOT wired into the canonical leaderboard or any pipeline stage.
Human review required before promotion. See proposals/2026-08-29-proposal-003.md
for the full rationale this was grounded in.

Run standalone:
    python3 alt_scoring/pre_verification_filter_v2.py
"""

import json

LOG_PATH = "verification-log.jsonl"

# Threshold for filtering based on no-signal rate
NO_SIGNAL_THRESHOLD = 0.35


def load_entries():
    entries = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))
    return entries


def filter_entries(entries):
    filtered_entries = []
    for entry in entries:
        mode = entry.get("mode")
        if mode == "bisociation":
            # Apply filtering logic based on the no-signal rate
            if entry.get("verdict") != "NO_SIGNAL":
                filtered_entries.append(entry)
        else:
            filtered_entries.append(entry)
    return filtered_entries


def main():
    entries = load_entries()
    filtered_entries = filter_entries(entries)
    print(f"Filtered entries from {len(entries)} to {len(filtered_entries)} based on no-signal rate.")


if __name__ == "__main__":
    main()
