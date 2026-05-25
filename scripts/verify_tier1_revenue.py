"""Verify Tier-1 (Revenue) command-centre is in place.

Public-side checks only. Live pipeline data is verified by the private
audit script — see `templates/private_ops_audit_template.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REVENUE_DOC = REPO_ROOT / "docs" / "revenue" / "REVENUE_COMMAND_CENTER.md"

REQUIRED_SECTIONS = (
    "## Inputs",
    "## Required columns",
    "## Operating rules",
    "## Daily cadence",
    "## Weekly cadence",
)

REQUIRED_PIPELINE_COLUMNS = (
    "id",
    "lead_name",
    "company",
    "stage",
    "next_action",
)

REQUIRED_LOG_COLUMNS = (
    "date",
    "action_type",
    "lead_id",
    "summary",
)


def _check_revenue_doc() -> list[str]:
    if not REVENUE_DOC.exists():
        return [f"Missing: {REVENUE_DOC.relative_to(REPO_ROOT)}"]
    body = REVENUE_DOC.read_text(encoding="utf-8")
    failures: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in body:
            failures.append(f"Section missing in revenue doc: {section}")
    for col in REQUIRED_PIPELINE_COLUMNS:
        if col not in body:
            failures.append(f"Pipeline column not documented: {col}")
    for col in REQUIRED_LOG_COLUMNS:
        if col not in body:
            failures.append(f"Action-log column not documented: {col}")
    return failures


def main() -> None:
    print("== Tier 1 — Revenue Command Centre ==")
    failures = _check_revenue_doc()
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print("PASS: Tier 1 revenue command centre verified.")


if __name__ == "__main__":
    main()
