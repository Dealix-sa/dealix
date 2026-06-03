"""Verify Dealix master tree skeleton.

Master Content Pack v1 prerequisite. Checks that the operating-doctrine
folders and anchor files exist so the rest of the verification pipeline
has something to bind to.
"""

from pathlib import Path

REQUIRED_DIRS = [
    "docs/founder",
    "docs/strategy",
    "docs/revenue",
    "docs/acquisition",
    "docs/sales",
    "docs/offers",
    "docs/delivery",
    "docs/delivery/revenue_sprint",
    "docs/trust",
    "docs/finance",
    "docs/client_success",
    "docs/product",
    "docs/content",
    "docs/learning",
    "docs/people",
    "docs/agents",
    "docs/ai_management",
    "docs/control_plane",
    "docs/ops",
    "docs/partners",
    "docs/investor",
    "docs/brand",
    "docs/api",
    "docs/deployment",
    "scripts",
    ".github/workflows",
]

REQUIRED_FILES = [
    "DEALIX_OPERATING_DOCTRINE.md",
    "DEALIX_COMPANY_OS_SCORECARD.md",
    "docs/ops/DOCUMENT_STANDARD.md",
    "docs/ops/OPERATING_LOOPS.md",
    "docs/founder/DAILY_COMMAND_BRIEF.md",
    "docs/revenue/OFFER_LADDER.md",
    "docs/revenue/PIPELINE_STAGES.md",
    "docs/trust/APPROVAL_MATRIX.md",
    "docs/trust/AUTONOMY_POLICY.md",
    "docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md",
    "docs/control_plane/COMPANY_STATE_SCHEMA.md",
    "scripts/fill_empty_docs_with_standard.py",
    "scripts/verify_document_quality.py",
    "scripts/verify_company_os_deep.py",
    "scripts/verify_full_ops.py",
    ".github/workflows/dealix-company-os.yml",
]

failures = []

for directory in REQUIRED_DIRS:
    if not Path(directory).is_dir():
        failures.append(f"Missing directory: {directory}")

for file in REQUIRED_FILES:
    path = Path(file)
    if not path.is_file():
        failures.append(f"Missing file: {file}")
    elif path.stat().st_size == 0:
        failures.append(f"Empty file: {file}")

if failures:
    print("Master tree verification failed:")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("PASS: Dealix master tree skeleton verified.")
