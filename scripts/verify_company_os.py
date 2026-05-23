#!/usr/bin/env python3
"""Verify the Dealix Company OS — the 12 operating systems documented in docs/.

Exit codes:
  0 = PASS
  1 = FIX  (one or more systems are incomplete)
  2 = BLOCKED (one or more core systems are missing entirely)

This script checks that the directory exists, contains the expected canonical
files for each system, and that none of those files are empty.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class System:
    name: str
    directory: Path
    required_files: tuple[str, ...]
    core: bool


SYSTEMS: tuple[System, ...] = (
    System(
        name="Founder OS",
        directory=REPO_ROOT / "docs" / "founder",
        required_files=(
            "CEO_CONTROL_TOWER.md",
            "DAILY_COMMAND_BRIEF.md",
            "WEEKLY_CEO_REVIEW.md",
            "MONTHLY_STRATEGY_REVIEW.md",
            "DECISION_LOG.md",
            "RISK_REGISTER.md",
            "FOUNDER_FOCUS_RULES.md",
            "COMPANY_HEALTH_SCORE.md",
        ),
        core=True,
    ),
    System(
        name="Revenue OS",
        directory=REPO_ROOT / "docs" / "revenue",
        required_files=(
            "REVENUE_MODEL.md",
            "OFFER_LADDER.md",
            "PIPELINE_STAGES.md",
            "SALES_FUNNEL.md",
            "QUALIFICATION_RULES.md",
            "PROPOSAL_RULES.md",
            "CLOSING_PLAYBOOK.md",
            "PRICING_EXPERIMENTS.md",
            "REVENUE_METRICS.md",
        ),
        core=True,
    ),
    System(
        name="Delivery OS",
        directory=REPO_ROOT / "docs" / "delivery" / "revenue_sprint",
        required_files=(
            "DELIVERY_PLAYBOOK.md",
            "CLIENT_INTAKE.md",
            "RESEARCH_PROCESS.md",
            "LEAD_TABLE_SCHEMA.md",
            "SCORING_RULES.md",
            "OUTREACH_PACK_TEMPLATE.md",
            "REPORT_TEMPLATE.md",
            "QA_CHECKLIST.md",
            "HANDOFF_TEMPLATE.md",
            "CASE_STUDY_CAPTURE.md",
        ),
        core=True,
    ),
    System(
        name="Trust OS",
        directory=REPO_ROOT / "docs" / "trust",
        required_files=(
            "APPROVAL_MATRIX.md",
            "CLAIM_GUARD.md",
            "NO_OVERCLAIM_POLICY.md",
            "DATA_RETENTION_POLICY.md",
            "SUPPRESSION_LIST_POLICY.md",
            "CLIENT_DATA_HANDLING.md",
            "INCIDENT_RESPONSE.md",
            "PUBLIC_REPO_SAFETY.md",
            "AUDIT_POLICY.md",
        ),
        core=True,
    ),
    System(
        name="Learning OS",
        directory=REPO_ROOT / "docs" / "learning",
        required_files=(
            "EXPERIMENT_LOG.md",
            "WIN_LOSS_REVIEW.md",
            "MESSAGE_PERFORMANCE.md",
            "SECTOR_PERFORMANCE.md",
            "PRICING_LEARNING.md",
            "AGENT_EVALS.md",
            "MONTHLY_STRATEGY_UPDATE.md",
        ),
        core=True,
    ),
    System(
        name="Finance OS",
        directory=REPO_ROOT / "docs" / "finance",
        required_files=(
            "BILLING_POLICY.md",
            "PAYMENT_RULES.md",
            "INVOICE_WORKFLOW.md",
            "REFUND_POLICY.md",
            "MRR_DEFINITION.md",
            "CASH_CONTROL.md",
            "FINANCIAL_DASHBOARD.md",
        ),
        core=False,
    ),
    System(
        name="Client Success OS",
        directory=REPO_ROOT / "docs" / "client_success",
        required_files=(
            "ONBOARDING.md",
            "WEEKLY_REPORT_TEMPLATE.md",
            "CLIENT_HEALTH_SCORE.md",
            "FEEDBACK_LOOP.md",
            "RETENTION_PLAYBOOK.md",
            "UPSELL_PLAYBOOK.md",
            "RENEWAL_PLAYBOOK.md",
        ),
        core=False,
    ),
    System(
        name="Acquisition OS",
        directory=REPO_ROOT / "docs" / "acquisition",
        required_files=(
            "LEAD_SOURCING_SYSTEM.md",
            "ICP_SCORING_MODEL.md",
            "OUTREACH_CADENCE.md",
            "MESSAGE_QUALITY_STANDARD.md",
            "SAMPLE_GENERATION_SYSTEM.md",
            "FOLLOWUP_RULES.md",
        ),
        core=False,
    ),
    System(
        name="Product OS",
        directory=REPO_ROOT / "docs" / "product",
        required_files=(
            "PRODUCT_PRINCIPLES.md",
            "ROADMAP.md",
            "FEATURE_INTAKE.md",
            "BUILD_DEFER_KILL.md",
            "CUSTOMER_FEEDBACK_LOOP.md",
            "RELEASE_POLICY.md",
            "PRODUCT_METRICS.md",
        ),
        core=False,
    ),
    System(
        name="Content OS",
        directory=REPO_ROOT / "docs" / "content",
        required_files=(
            "CONTENT_STRATEGY.md",
            "FOUNDER_VOICE.md",
            "LINKEDIN_SYSTEM.md",
            "X_SYSTEM.md",
            "CASE_STUDY_SYSTEM.md",
            "SECTOR_REPORT_SYSTEM.md",
            "PROOF_LIBRARY.md",
        ),
        core=False,
    ),
    System(
        name="People OS",
        directory=REPO_ROOT / "docs" / "people",
        required_files=(
            "ROLE_MAP.md",
            "HIRING_TRIGGERS.md",
            "SDR_SCORECARD.md",
            "DELIVERY_ANALYST_SCORECARD.md",
            "OPS_MANAGER_SCORECARD.md",
            "CONTRACTOR_ONBOARDING.md",
            "DELEGATION_RULES.md",
        ),
        core=False,
    ),
    System(
        name="Investor / Partner OS",
        directory=REPO_ROOT / "docs" / "investor",
        required_files=(
            "DATA_ROOM_INDEX.md",
            "COMPANY_OVERVIEW.md",
            "METRICS.md",
            "ROADMAP.md",
            "FINANCIAL_MODEL.md",
            "MARKET_THESIS.md",
            "RISK_REGISTER.md",
            "PITCH_DECK_OUTLINE.md",
        ),
        core=False,
    ),
)


def _check_file(path: Path) -> str | None:
    """Return None if the file is present and non-empty, else an error string."""
    if not path.exists():
        return "missing"
    if not path.is_file():
        return "not a file"
    if path.stat().st_size == 0:
        return "empty"
    return None


def main() -> int:
    print("Dealix Company OS verification")
    print("=" * 50)

    missing_core = 0
    incomplete = 0
    passing = 0

    for system in SYSTEMS:
        if not system.directory.exists():
            tag = "BLOCKED" if system.core else "FIX"
            print(f"[{tag}] {system.name}: directory missing ({system.directory.relative_to(REPO_ROOT)})")
            if system.core:
                missing_core += 1
            else:
                incomplete += 1
            continue

        problems: list[str] = []
        for filename in system.required_files:
            problem = _check_file(system.directory / filename)
            if problem:
                problems.append(f"{filename} ({problem})")

        if problems:
            tag = "BLOCKED" if system.core else "FIX"
            print(f"[{tag}] {system.name}: " + ", ".join(problems))
            if system.core:
                missing_core += 1
            else:
                incomplete += 1
        else:
            print(f"[PASS] {system.name}")
            passing += 1

    print("=" * 50)
    print(f"PASS: {passing} / {len(SYSTEMS)}")

    if missing_core:
        print("Status: BLOCKED — core Company OS systems are missing.")
        return 2
    if incomplete:
        print("Status: FIX — non-core systems are incomplete.")
        return 1

    print("Status: PASS — Company OS exists.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
