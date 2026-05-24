#!/usr/bin/env python3
"""Verify AI Governance: governance module + policy file + governance eval +
docs all present."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import must_exist, report, file_contains  # noqa: E402

LAYER = "AI Governance"


def main() -> None:
    reasons = must_exist(
        "dealix/governance/__init__.py",
        "dealix/governance/approvals.py",
        "policies/dealix_control_policy.yaml",
        "evals/governance_eval.yaml",
        "docs/company/DEALIX_AI_GOVERNANCE.md",
    )
    reasons += file_contains(
        "docs/company/DEALIX_AI_GOVERNANCE.md",
        "governance_decision",
        "approval_center",
        "non-negotiable",
    )
    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
