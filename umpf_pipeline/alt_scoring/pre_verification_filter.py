"""
EXPERIMENTAL -- proposed by audit_agent.py on 2026-08-29.
NOT wired into the canonical leaderboard or any pipeline stage.
Human review required before promotion. See proposals/2026-08-29-proposal-001.md
for the full rationale this was grounded in.

Run standalone:
    python3 alt_scoring/pre_verification_filter.py
"""

import json

# Load the verification log
with open('verification-log.jsonl', 'r', encoding='utf-8') as f:
    entries = [json.loads(line) for line in f if line.strip()]

# Define a threshold for filtering 'case-study' mode hypotheses
THRESHOLD = 10  # Example threshold; adjust based on further analysis

# Filter function
filtered_entries = [entry for entry in entries if not (entry.get('mode') == 'case-study' and entry.get('self_reported_distance', 0) * 2 < THRESHOLD)]

# Output the filtered entries
with open('filtered_verification_log.jsonl', 'w', encoding='utf-8') as f:
    for entry in filtered_entries:
        f.write(json.dumps(entry) + '\n')

print(f"Filtered {len(entries) - len(filtered_entries)} 'case-study' entries below threshold.")