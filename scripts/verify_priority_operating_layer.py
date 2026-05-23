from pathlib import Path

required = [
    "DEALIX_PRIORITY_EXECUTION_SPRINT.md",
    "docs/revenue/REVENUE_CONTROL_SYSTEM.md",
    "docs/trust/TRUST_CONTROL_SYSTEM.md",
    "docs/delivery/revenue_sprint/DELIVERY_CONTROL_SYSTEM.md",
    "docs/ops/WEEKLY_LEARNING_GOVERNANCE.md",
    "docs/revenue/PIPELINE_STAGES.md",
    "docs/revenue/CASH_RULES.md",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 150:
        failures.append(f"Too short: {file}")

if failures:
    print("Priority operating layer failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: priority operating layer is ready.")
