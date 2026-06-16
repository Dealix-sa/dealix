"""Dealix master tree verifier.

Checks that the canonical folder and root-file structure of Dealix exists.

Run:
    python scripts/verify_master_tree.py
"""
from pathlib import Path

REQUIRED_FOLDERS = [
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
]

REQUIRED_FILES = [
    "DEALIX_OPERATING_DOCTRINE.md",
    "DEALIX_COMPANY_OS_SCORECARD.md",
    "docs/ops/DOCUMENT_STANDARD.md",
    "docs/ops/OPERATING_LOOPS.md",
    "docs/founder/DAILY_COMMAND_BRIEF.md",
    "docs/founder/WEEKLY_CEO_REVIEW.md",
    "docs/revenue/OFFER_LADDER.md",
    "docs/revenue/PIPELINE_STAGES.md",
    "docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/trust/APPROVAL_MATRIX.md",
    "docs/trust/AUTONOMY_POLICY.md",
    "docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md",
    "scripts/verify_document_quality.py",
    "scripts/verify_company_os_deep.py",
    "scripts/verify_full_ops.py",
    "scripts/fill_empty_docs_with_standard.py",
]


def main() -> int:
    failures: list[str] = []

    for folder in REQUIRED_FOLDERS:
        if not Path(folder).is_dir():
            failures.append(f"Missing folder: {folder}")

    for file in REQUIRED_FILES:
        if not Path(file).is_file():
            failures.append(f"Missing file: {file}")

    if failures:
        print("Master tree verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Dealix master tree verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
