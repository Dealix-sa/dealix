"""Verify the Revenue Sprint Delivery Control system is in place."""

from pathlib import Path

required = [
    "docs/delivery/revenue_sprint/DELIVERY_CONTROL_SYSTEM.md",
    "docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/delivery/revenue_sprint/REPORT_TEMPLATE.md",
    "docs/delivery/revenue_sprint/HANDOFF_TEMPLATE.md",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 150:
        failures.append(f"Too short: {file}")

text = Path("docs/delivery/revenue_sprint/DELIVERY_CONTROL_SYSTEM.md").read_text(encoding="utf-8", errors="ignore")
for term in ["QA", "A-priority", "evidence", "approval", "private"]:
    if term not in text:
        failures.append(f"DELIVERY_CONTROL_SYSTEM missing: {term}")

if failures:
    print("Delivery control verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: delivery control system is ready.")
