#!/usr/bin/env python3
"""Verify the Dealix Master Operating Blueprint integration is in place."""
from __future__ import annotations

from pathlib import Path
import sys

REQUIRED = [
    "DEALIX_MASTER_OPERATING_BLUEPRINT.md",
    "DEALIX_INTEGRATION_MAP.md",
    "DEALIX_FINAL_REPO_TREE.md",
    "DEALIX_SYSTEM_COMPLETION_MATRIX.md",
    "DEALIX_EXECUTION_ROADMAP_FINAL.md",
    "DEALIX_DEFINITION_OF_DONE.md",
    "docs/ops/MASTER_COMMAND_SYSTEM.md",
    "docs/ops/GITHUB_GOVERNANCE_SYSTEM.md",
]

MIN_BYTES = 50


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED:
        p = Path(rel)
        if not p.exists():
            failures.append(f"Missing: {rel}")
        elif p.stat().st_size < MIN_BYTES:
            failures.append(f"Too short: {rel}")

    # Blueprint must reference each of the 10 OS doc paths.
    blueprint = Path("DEALIX_MASTER_OPERATING_BLUEPRINT.md")
    if blueprint.exists():
        text = blueprint.read_text(encoding="utf-8", errors="ignore")
        for marker in (
            "docs/security/SECURITY_RELIABILITY_SUPPLY_CHAIN_OS.md",
            "docs/data/COMPANY_DATA_ARCHITECTURE.md",
            "docs/control_plane/EXECUTIVE_CONTROL_PLANE.md",
            "docs/revenue/REVENUE_OPERATIONS_PLAYBOOK.md",
            "docs/client_success/DELIVERY_CLIENT_SUCCESS_OS.md",
            "docs/finance/FINANCE_PRICING_CAPITAL_OS.md",
            "docs/trust/TRUST_COMPLIANCE_AI_RISK_OS.md",
            "docs/content/BRAND_PROOF_CONTENT_OS.md",
            "docs/product/PRODUCTIZATION_ENGINEERING_OS.md",
            "docs/people/PEOPLE_DELEGATION_PARTNER_OS.md",
        ):
            if marker not in text:
                failures.append(f"Blueprint missing OS reference: {marker}")

    if failures:
        print("Master operating blueprint verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Master Operating Blueprint is integrated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
