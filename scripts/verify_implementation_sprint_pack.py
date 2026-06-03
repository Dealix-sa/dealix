#!/usr/bin/env python3
"""Verify the Dealix Implementation Sprint Pack as a whole."""
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    "DEALIX_IMPLEMENTATION_SPRINT_PACK.md",
    "DEALIX_IMPLEMENTATION_MASTER_CHECKLIST.md",
    "DEALIX_MASTER_OPERATING_BLUEPRINT.md",
    "DEALIX_INTEGRATION_MAP.md",
    "DEALIX_FINAL_REPO_TREE.md",
    "DEALIX_SYSTEM_COMPLETION_MATRIX.md",
    "DEALIX_EXECUTION_ROADMAP_FINAL.md",
    "DEALIX_DEFINITION_OF_DONE.md",
    "scripts/verify_master_operating_blueprint.py",
    "scripts/verify_security_reliability_os.py",
    "scripts/verify_public_safety_v2.py",
    "scripts/verify_data_boundary.py",
    "scripts/verify_company_data_architecture.py",
    "scripts/verify_revenue_operations_playbook.py",
    "scripts/verify_delivery_client_success_os.py",
    "scripts/verify_finance_pricing_os.py",
    "scripts/verify_trust_ai_risk_os.py",
    "scripts/verify_brand_proof_content_os.py",
    "scripts/verify_productization_engineering_os.py",
    "scripts/verify_people_partner_os.py",
    "scripts/bootstrap_private_ops.py",
    ".github/workflows/dealix-implementation-sprint-pack.yml",
]


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED:
        p = Path(rel)
        if not p.exists():
            failures.append(f"Missing: {rel}")
        elif p.stat().st_size < 50:
            failures.append(f"Too short: {rel}")

    if failures:
        print("Implementation Sprint Pack verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Implementation Sprint Pack is ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
