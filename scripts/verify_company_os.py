#!/usr/bin/env python3
"""
verify_company_os.py — Top-level verifier for the Dealix Company OS.

Confirms that the 12 Super Systems each have their documented files in
place. Run by the `dealix-company-os.yml` GitHub workflow on every PR.

Exit codes:
    0 — every required file present
    1 — one or more required files missing

The script is intentionally minimal — it checks existence only. Per-system
verifiers (`verify_founder_os.py`, `verify_revenue_os.py`, etc.) do the
deeper content + cross-link checks.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# Per-system required files (relative to repo root).
REQUIRED: dict[str, list[str]] = {
    "00_root": [
        "DEALIX_STAGE_STATUS.md",
        "DEALIX_ARCHITECTURE_MAP.md",
        "DEALIX_EXECUTION_LEDGER.md",
        "DEALIX_DECISION_RULES.md",
    ],
    "01_founder_command_os": [
        "docs/founder/CEO_OPERATING_SYSTEM.md",
        "docs/founder/DAILY_COMMAND_BRIEF.md",
        "docs/founder/WEEKLY_CEO_REVIEW.md",
        "docs/founder/DECISION_LOG.md",
        "docs/founder/FOCUS_POLICY.md",
        "docs/founder/RISK_REGISTER.md",
        "docs/founder/KILL_DEFER_BUILD_RULES.md",
        "docs/founder/BOARD_MEMO_TEMPLATE.md",
    ],
    "02_strategy_os": [
        "docs/strategy/NORTH_STAR.md",
        "docs/strategy/POSITIONING.md",
        "docs/strategy/ICP_STRATEGY.md",
        "docs/strategy/COMPETITIVE_STRATEGY.md",
        "docs/strategy/MOAT_STRATEGY.md",
        "docs/strategy/PRICING_STRATEGY.md",
        "docs/strategy/PRODUCT_STRATEGY.md",
        "docs/strategy/GTM_STRATEGY.md",
        "docs/strategy/90_DAY_STRATEGIC_PLAN.md",
    ],
    "03_revenue_os": [
        "docs/revenue/REVENUE_MODEL.md",
        "docs/revenue/SALES_FUNNEL.md",
        "docs/revenue/PIPELINE_STAGES.md",
        "docs/revenue/OFFER_LADDER.md",
        "docs/revenue/OUTBOUND_POLICY.md",
        "docs/revenue/QUALIFICATION_RULES.md",
        "docs/revenue/PROPOSAL_RULES.md",
        "docs/revenue/CLOSING_PLAYBOOK.md",
        "docs/revenue/REVENUE_METRICS.md",
    ],
    "04_acquisition_os": [
        "docs/acquisition/LEAD_SOURCING_SYSTEM.md",
        "docs/acquisition/ICP_SCORING_MODEL.md",
        "docs/acquisition/SECTOR_PLAYBOOKS.md",
        "docs/acquisition/OUTREACH_CADENCE.md",
        "docs/acquisition/SAMPLE_GENERATION_SYSTEM.md",
        "docs/acquisition/CHANNEL_STRATEGY.md",
        "docs/acquisition/PARTNER_ACQUISITION.md",
    ],
    "05_delivery_os": [
        "docs/delivery/DELIVERY_QUALITY_STANDARD.md",
        "docs/delivery/revenue_sprint/OFFER.md",
        "docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md",
        "docs/delivery/revenue_sprint/CLIENT_INTAKE.md",
        "docs/delivery/revenue_sprint/REPORT_TEMPLATE.md",
        "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
        "docs/delivery/revenue_sprint/HANDOFF_TEMPLATE.md",
        "docs/delivery/revenue_sprint/CASE_STUDY_CAPTURE.md",
        "docs/delivery/managed_pilot/OFFER.md",
        "docs/delivery/managed_pilot/DELIVERY_PLAYBOOK.md",
        "docs/delivery/revenue_desk/OFFER.md",
        "docs/delivery/revenue_desk/DELIVERY_PLAYBOOK.md",
    ],
    "06_product_os": [
        "docs/product/PRODUCT_PRINCIPLES.md",
        "docs/product/FEATURE_INTAKE.md",
        "docs/product/BUILD_DEFER_KILL.md",
        "docs/product/CUSTOMER_FEEDBACK_LOOP.md",
        "docs/product/RELEASE_POLICY.md",
        "docs/product/PRODUCT_METRICS.md",
    ],
    "07_trust_os": [
        "docs/trust/APPROVAL_MATRIX.md",
        "docs/trust/NO_OVERCLAIM_POLICY.md",
        "docs/trust/DATA_RETENTION_POLICY.md",
        "docs/trust/SUPPRESSION_LIST_POLICY.md",
        "docs/trust/INCIDENT_RESPONSE.md",
        "docs/trust/CLIENT_DATA_HANDLING.md",
        "docs/trust/CLAIMS_GUIDE.md",
        "docs/trust/PUBLIC_REPO_SAFETY.md",
        "docs/trust/AI_GOVERNANCE.md",
        "docs/trust/AUDIT_POLICY.md",
        "dealix/trust/approval_matrix.py",
        "dealix/trust/claim_guard.py",
        "dealix/trust/suppression.py",
        "dealix/trust/data_retention.py",
        "dealix/trust/evidence_pack.py",
        "dealix/trust/policy_engine.py",
    ],
    "08_finance_os": [
        "docs/finance/BILLING_POLICY.md",
        "docs/finance/PAYMENT_RULES.md",
        "docs/finance/INVOICE_WORKFLOW.md",
        "docs/finance/REFUND_POLICY.md",
        "docs/finance/MRR_DEFINITION.md",
        "docs/finance/FINANCIAL_DASHBOARD.md",
    ],
    "09_client_success_os": [
        "docs/client_success/ONBOARDING.md",
        "docs/client_success/WEEKLY_REPORT_TEMPLATE.md",
        "docs/client_success/CLIENT_HEALTH_SCORE.md",
        "docs/client_success/FEEDBACK_LOOP.md",
        "docs/client_success/RETENTION_PLAYBOOK.md",
        "docs/client_success/RENEWAL_PLAYBOOK.md",
        "docs/client_success/UPSELL_PLAYBOOK.md",
        "docs/client_success/TESTIMONIAL_CAPTURE.md",
    ],
    "10_content_os": [
        "docs/content/CONTENT_STRATEGY.md",
        "docs/content/LINKEDIN_SYSTEM.md",
        "docs/content/X_SYSTEM.md",
        "docs/content/SECTOR_REPORT_SYSTEM.md",
        "docs/content/CASE_STUDY_SYSTEM.md",
        "docs/content/PROOF_LIBRARY.md",
        "docs/content/FOUNDER_VOICE.md",
    ],
    "11_people_os": [
        "docs/people/ROLE_MAP.md",
        "docs/people/HIRING_TRIGGERS.md",
        "docs/people/SDR_SCORECARD.md",
        "docs/people/DELIVERY_ANALYST_SCORECARD.md",
        "docs/people/OPS_MANAGER_SCORECARD.md",
        "docs/people/CONTRACTOR_ONBOARDING.md",
        "docs/people/DELEGATION_RULES.md",
    ],
    "12_learning_os": [
        "docs/learning/EXPERIMENT_LOG.md",
        "docs/learning/WIN_LOSS_REVIEW.md",
        "docs/learning/MESSAGE_PERFORMANCE.md",
        "docs/learning/SECTOR_PERFORMANCE.md",
        "docs/learning/PRICING_LEARNING.md",
        "docs/learning/AGENT_EVALS.md",
        "docs/learning/MONTHLY_STRATEGY_UPDATE.md",
    ],
}


def main() -> int:
    missing: list[tuple[str, str]] = []
    present: int = 0
    for system, files in REQUIRED.items():
        for rel in files:
            path = REPO_ROOT / rel
            if path.exists():
                present += 1
            else:
                missing.append((system, rel))

    total = present + len(missing)
    print(f"Company OS verification: {present}/{total} files present")
    if missing:
        print("\nMISSING:")
        for system, rel in missing:
            print(f"  [{system}] {rel}")
        return 1
    print("\nAll 12 Super Systems documented.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
