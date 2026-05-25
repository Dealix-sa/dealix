from pathlib import Path

required = [
    "docs/founder/CEO_OPERATING_MODEL.md",
    "docs/founder/CEO_KPI_TREE.md",
    "docs/finance/FINANCIAL_MODEL_V1.md",
    "docs/finance/CAPITAL_ALLOCATION_SYSTEM.md",
    "docs/strategy/DEALIX_GROWTH_SYSTEM.md",
    "docs/ops/MANAGEMENT_CADENCE.md",
]

failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 300:
        failures.append(f"Too short: {file}")

checks = {
    "docs/finance/FINANCIAL_MODEL_V1.md": ["cash_collected", "MRR", "runway", "gross_margin"],
    "docs/strategy/DEALIX_GROWTH_SYSTEM.md": ["Lead", "DM", "Reply", "Sample", "Proposal", "Payment"],
    "docs/founder/CEO_KPI_TREE.md": ["Cash Collected", "MRR", "Proposals Sent"],
    "docs/ops/MANAGEMENT_CADENCE.md": ["Daily", "Weekly", "Monthly", "Quarterly"],
}
for file, terms in checks.items():
    path = Path(file)
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for term in terms:
        if term not in text:
            failures.append(f"{file} missing: {term}")

if failures:
    print("CEO business systems verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: CEO business systems are ready.")
