"""Report the Dealix implementation sprint status.

Walks the canonical sprint list and reports per-sprint completion plus
overall percentage. Exits non-zero if any required file is missing so the
status command can be used as a gate in CI.
"""

from pathlib import Path

SPRINTS = {
    "Sprint 0 — Repo Safety": [
        ".gitignore",
        ".env.example",
        "SECURITY.md",
        "docs/security/SECURITY_BASELINE.md",
        "scripts/verify_public_safety_v2.py",
        "scripts/verify_data_boundary.py",
    ],
    "Sprint 1 — Master Blueprint": [
        "DEALIX_MASTER_OPERATING_BLUEPRINT.md",
        "DEALIX_INTEGRATION_MAP.md",
        "DEALIX_FINAL_REPO_TREE.md",
        "DEALIX_DEFINITION_OF_DONE.md",
        "scripts/verify_master_operating_blueprint.py",
    ],
    "Sprint 2 — Data Architecture": [
        "docs/data/COMPANY_DATA_ARCHITECTURE.md",
        "ops_runtime/data_validator.py",
        "scripts/audit_private_data_quality.py",
        "scripts/export_company_snapshot.py",
    ],
    "Sprint 3 — CEO Control": [
        "control_plane/priority_router.py",
        "control_plane/control_tower.py",
        "scripts/generate_mission_control.py",
        "scripts/generate_ceo_business_score.py",
        "ops_runtime/business_audit.py",
    ],
    "Sprint 4 — Revenue Ops": [
        "docs/revenue/REVENUE_OPERATIONS_PLAYBOOK.md",
        "docs/strategy/ICP_OPERATING_SYSTEM.md",
        "docs/acquisition/LEAD_SOURCING_SYSTEM.md",
        "scripts/verify_revenue_operations_playbook.py",
    ],
    "Sprint 5 — Delivery + Client Success": [
        "docs/client_success/DELIVERY_CLIENT_SUCCESS_OS.md",
        "docs/delivery/KICKOFF_PROTOCOL.md",
        "docs/delivery/DELIVERY_QA_SCORE.md",
        "scripts/verify_delivery_client_success_os.py",
    ],
    "Sprint 6 — Finance + Trust": [
        "docs/finance/FINANCE_PRICING_CAPITAL_OS.md",
        "docs/trust/TRUST_COMPLIANCE_AI_RISK_OS.md",
        "scripts/verify_finance_pricing_os.py",
        "scripts/verify_trust_ai_risk_os.py",
    ],
    "Sprint 7 — Content + Proof": [
        "docs/content/BRAND_PROOF_CONTENT_OS.md",
        "docs/content/PROOF_LEVEL_POLICY.md",
        "scripts/verify_brand_proof_content_os.py",
    ],
    "Sprint 8 — Productization + People": [
        "docs/product/PRODUCTIZATION_ENGINEERING_OS.md",
        "docs/people/PEOPLE_DELEGATION_PARTNER_OS.md",
        "scripts/verify_productization_engineering_os.py",
        "scripts/verify_people_partner_os.py",
    ],
}


def main() -> None:
    total = 0
    done = 0
    print("# Dealix Implementation Sprint Status\n")
    for sprint, files in SPRINTS.items():
        sprint_done = 0
        print(f"## {sprint}")
        for file in files:
            total += 1
            exists = Path(file).exists()
            if exists:
                done += 1
                sprint_done += 1
            print(f"- {'PASS' if exists else 'MISSING'} {file}")
        pct = round((sprint_done / len(files)) * 100)
        print(f"Status: {pct}%\n")
    total_pct = round((done / total) * 100) if total else 0
    print(f"TOTAL: {total_pct}%")
    if total_pct < 100:
        raise SystemExit(1)
    print("PASS: all implementation sprint files exist.")


if __name__ == "__main__":
    main()
