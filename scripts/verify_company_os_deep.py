"""Deep Company OS verification: doctrine roots present and non-empty."""

from pathlib import Path

required = [
    "docs/00_constitution",
    "docs/00_foundation",
    "docs/revenue/REVENUE_CONTROL_SYSTEM.md",
    "docs/trust/TRUST_CONTROL_SYSTEM.md",
    "docs/delivery/revenue_sprint/DELIVERY_CONTROL_SYSTEM.md",
    "docs/ops/WEEKLY_LEARNING_GOVERNANCE.md",
]

failures = []

for entry in required:
    path = Path(entry)
    if not path.exists():
        failures.append(f"Missing: {entry}")
        continue
    if path.is_file() and path.stat().st_size < 100:
        failures.append(f"Too short: {entry}")
    if path.is_dir() and not any(path.iterdir()):
        failures.append(f"Empty directory: {entry}")

if failures:
    print("Company OS deep verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: company OS deep doctrine is present.")
