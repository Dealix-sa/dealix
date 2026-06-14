from pathlib import Path

required = [
    "docs/revenue/REVENUE_COMMAND_CENTER.md",
    "docs/trust/TRUST_COMMAND_CENTER.md",
    "docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md",
    "docs/learning/LEARNING_COMMAND_CENTER.md",
    "docs/finance/FINANCE_COMMAND_CENTER.md",
    "docs/client_success/CLIENT_SUCCESS_COMMAND_CENTER.md",
    "docs/product/PRODUCTIZATION_COMMAND_CENTER.md",
    "docs/ai_management/AI_COMMAND_CENTER.md",
    "docs/content/CONTENT_COMMAND_CENTER.md",
    "docs/partners/PARTNER_COMMAND_CENTER.md",
    "docs/people/DELEGATION_COMMAND_CENTER.md",
]

failures = []

for file in required:
    p = Path(file)
    if not p.exists():
        failures.append(f"Missing: {file}")
    elif p.stat().st_size < 250:
        failures.append(f"Too short: {file}")

if failures:
    print("Full spectrum OS failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: Dealix full-spectrum operating system exists.")
