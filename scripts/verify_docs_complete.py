from pathlib import Path
REQUIRED_FILES = [
    "DEALIX_STAGE_STATUS.md",
    "DEALIX_ARCHITECTURE_MAP.md",
    "DEALIX_EXECUTION_LEDGER.md",
    "docs/company/FOUNDER_CLARITY.md",
    "docs/company/DEALIX_POSITIONING.md",
    "docs/company/ICP.md",
    "docs/company/DO_NOT_SELL_YET.md",
    "docs/company/DECISION_RULES.md",
    "docs/offers/revenue_sprint/OFFER.md",
    "docs/offers/revenue_sprint/PRICING.md",
    "docs/offers/revenue_sprint/SCOPE.md",
    "docs/offers/revenue_sprint/FAQ.md",
    "docs/offers/revenue_sprint/PROPOSAL_TEMPLATE.md",
    "docs/offers/revenue_sprint/TERMS.md",
    "docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md",
    "docs/delivery/revenue_sprint/CLIENT_INTAKE.md",
    "docs/delivery/revenue_sprint/LEAD_TABLE_SCHEMA.md",
    "docs/delivery/revenue_sprint/REPORT_TEMPLATE.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/delivery/revenue_sprint/HANDOFF_TEMPLATE.md",
    "docs/trust/APPROVAL_MATRIX.md",
    "docs/trust/NO_OVERCLAIM_POLICY.md",
    "docs/trust/DATA_RETENTION_POLICY.md",
    "docs/trust/SUPPRESSION_LIST_POLICY.md",
    "docs/trust/INCIDENT_RESPONSE.md",
    "docs/trust/PUBLIC_REPO_SAFETY.md",
    "docs/public_sales/REVENUE_SPRINT_ONE_PAGER.md",
    "docs/public_sales/CASE_STUDY_TEMPLATE.md",
    "docs/public_sales/PARTNER_PROGRAM.md",
    "docs/ops/SOP_INDEX.md",
    "docs/ops/DAILY_OPERATING_LOOP.md",
    "docs/ops/WEEKLY_OPERATING_REVIEW.md",
    "landing/revenue-sprint.html",
    ".github/workflows/dealix-control.yml",
]
missing = [file for file in REQUIRED_FILES if not Path(file).exists()]
if missing:
    print("Missing required files:")
    for file in missing:
        print(f"- {file}")
    raise SystemExit(1)
empty = []
for file in REQUIRED_FILES:
    path = Path(file)
    if path.exists() and path.is_file() and path.stat().st_size == 0:
        empty.append(file)
if empty:
    print("Empty required files:")
    for file in empty:
        print(f"- {file}")
    raise SystemExit(1)
print("PASS: all required Dealix control files exist and are not empty.")
