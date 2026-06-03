"""Verify the weekly learning automation contract is in place."""

from pathlib import Path

required = [
    "docs/ops/WEEKLY_LEARNING_GOVERNANCE.md",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 100:
        failures.append(f"Too short: {file}")

text = Path("docs/ops/WEEKLY_LEARNING_GOVERNANCE.md").read_text(encoding="utf-8", errors="ignore")
for term in ["learning decision", "playbook", "weekly", "evidence"]:
    if term not in text:
        failures.append(f"WEEKLY_LEARNING_GOVERNANCE missing: {term}")

if failures:
    print("Weekly automation verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: weekly learning governance is ready.")
