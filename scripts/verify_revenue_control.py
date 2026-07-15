"""Verify the Revenue Control system is in place."""

from pathlib import Path

required = [
    "docs/revenue/REVENUE_CONTROL_SYSTEM.md",
    "docs/revenue/OFFER_LADDER.md",
    "docs/revenue/PIPELINE_STAGES.md",
    "docs/revenue/CASH_RULES.md",
    "docs/revenue/BAD_REVENUE_FILTER.md",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 200:
        failures.append(f"Too short: {file}")

text = Path("docs/revenue/REVENUE_CONTROL_SYSTEM.md").read_text(encoding="utf-8", errors="ignore")
for term in ["cash collected", "next_action", "proposal", "payment", "retainer"]:
    if term not in text:
        failures.append(f"REVENUE_CONTROL_SYSTEM missing: {term}")

if failures:
    print("Revenue control verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: revenue control system is ready.")
