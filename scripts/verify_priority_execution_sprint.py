from pathlib import Path

required = [
    "DEALIX_PRIORITY_EXECUTION_SPRINT.md",
    "docs/revenue/REVENUE_CONTROL_SYSTEM.md",
    "docs/trust/TRUST_CONTROL_SYSTEM.md",
    "docs/delivery/revenue_sprint/DELIVERY_CONTROL_SYSTEM.md",
    "docs/ops/WEEKLY_LEARNING_GOVERNANCE.md",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 200:
        failures.append(f"Too short: {file}")

text = Path("DEALIX_PRIORITY_EXECUTION_SPRINT.md").read_text(
    encoding="utf-8",
    errors="ignore",
)

for term in [
    "25 leads",
    "25 DMs",
    "3 samples",
    "1 proposal",
    "payment",
    "weekly review",
    "one system update",
]:
    if term not in text:
        failures.append(f"Priority sprint missing: {term}")

if failures:
    print("Priority execution sprint verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: priority execution sprint is ready.")
