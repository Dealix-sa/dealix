from pathlib import Path

path = Path("docs/ops/WEEKLY_PLAYBOOK_UPDATE_RULE.md")

if not path.exists():
    raise SystemExit("Missing WEEKLY_PLAYBOOK_UPDATE_RULE.md")

text = path.read_text(encoding="utf-8", errors="ignore")

required = [
    "Weekly Intelligence Review",
    "Updated playbook",
    "Every week must update",
    "ICP strategy",
    "delivery playbook",
    "trust policy",
    "git commit",
]

for term in required:
    if term not in text:
        raise SystemExit(f"Weekly playbook rule missing: {term}")

print("PASS: weekly playbook update rule is valid.")
