"""Shared pytest fixtures for the Launch OS test suite.

All fixtures return plain Python dicts or lightweight objects so they work
even before the implementation modules exist.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


# ---------------------------------------------------------------------------
# Account / lead fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_account() -> dict[str, Any]:
    """Return a fully-populated, valid account dict suitable for ICP scoring."""
    return {
        "account_id": "acc_001",
        "company_name": "شركة النخبة للتقنية",
        "sector": "saas",
        "sub_sector": "hr_tech",
        "city": "Riyadh",
        "region": "Riyadh",
        "country": "SA",
        "employee_count": 120,
        "annual_revenue_sar": 5_000_000,
        "decision_maker_title": "CEO",
        "decision_maker_present": True,
        "has_crm": True,
        "has_data_team": False,
        "tech_stack": ["salesforce", "slack", "python"],
        "pain_statement": "يعانون من بطء في تحويل العملاء المحتملين",
        "pain_statement_en": "Slow lead-to-customer conversion rate",
        "budget_sar": 60_000,
        "accepts_governance": True,
        "wants_safe_methods": True,
        "source": "warm_referral",
        "contact_email": "ceo@elite-tech.sa",
    }


@pytest.fixture()
def sample_accounts() -> list[dict[str, Any]]:
    """Return 5 diverse accounts covering different sectors and fit levels."""
    return [
        {
            "account_id": "acc_a",
            "company_name": "Riyadh FinTech Co",
            "sector": "fintech",
            "city": "Riyadh",
            "employee_count": 200,
            "annual_revenue_sar": 12_000_000,
            "budget_sar": 90_000,
            "decision_maker_present": True,
            "accepts_governance": True,
            "wants_safe_methods": True,
            "pain_statement": "Slow reconciliation pipeline",
            "source": "inbound",
        },
        {
            "account_id": "acc_b",
            "company_name": "Jeddah Logistics Ltd",
            "sector": "logistics",
            "city": "Jeddah",
            "employee_count": 450,
            "annual_revenue_sar": 25_000_000,
            "budget_sar": 120_000,
            "decision_maker_present": True,
            "accepts_governance": True,
            "wants_safe_methods": True,
            "pain_statement": "Manual route planning costs time",
            "source": "event",
        },
        {
            "account_id": "acc_c",
            "company_name": "Small Clinic Khobar",
            "sector": "healthcare",
            "city": "Khobar",
            "employee_count": 15,
            "annual_revenue_sar": 800_000,
            "budget_sar": 18_000,
            "decision_maker_present": False,
            "accepts_governance": True,
            "wants_safe_methods": True,
            "pain_statement": "No-shows waste appointment slots",
            "source": "cold_outreach",
        },
        {
            "account_id": "acc_d",
            "company_name": "Real Estate Developer Dammam",
            "sector": "real_estate",
            "city": "Dammam",
            "employee_count": 80,
            "annual_revenue_sar": 40_000_000,
            "budget_sar": 200_000,
            "decision_maker_present": True,
            "accepts_governance": True,
            "wants_safe_methods": True,
            "pain_statement": "Pipeline visibility is poor",
            "source": "warm_referral",
        },
        {
            "account_id": "acc_e",
            "company_name": "Education Platform KSA",
            "sector": "edtech",
            "city": "Riyadh",
            "employee_count": 30,
            "annual_revenue_sar": 2_000_000,
            "budget_sar": 0,
            "decision_maker_present": False,
            "accepts_governance": False,
            "wants_safe_methods": True,
            "pain_statement": "Low student retention",
            "source": "unknown",
        },
    ]


@pytest.fixture()
def sample_draft() -> dict[str, Any]:
    """Return a clean outreach draft dict with no governance violations."""
    return {
        "draft_id": "dft_001",
        "account_id": "acc_001",
        "channel": "email",
        "subject": "كيف تحول بياناتك إلى فرص مبيعات؟",
        "body_ar": (
            "السلام عليكم،\n\n"
            "لاحظنا أن شركتكم تعمل في مجال التقنية وقد تواجه تحديات في تحويل العملاء المحتملين. "
            "نود أن نشارككم تشخيصاً مجانياً لمنظومة المبيعات لديكم.\n\n"
            "هل يناسبكم لقاء قصير هذا الأسبوع؟"
        ),
        "body_en": (
            "Hello,\n\n"
            "We noticed that your company may face challenges converting leads. "
            "We would like to share a free sales diagnostic with you.\n\n"
            "Would a brief meeting this week work?"
        ),
        "sender_name": "فريق Dealix",
        "cta": "احجز تشخيصك المجاني",
        "has_whatsapp_consent": False,
        "approved_by_human": False,
        "pricing_range_sar": None,
    }


@pytest.fixture()
def sample_pipeline(sample_accounts: list[dict[str, Any]]) -> Any:
    """Return a PipelineTracker populated with 5 accounts in various stages.

    Returns the tracker instance directly; tests should use its public API.
    If PipelineTracker is not yet implemented this fixture will raise an
    ImportError — that is intentional (red-green cycle).
    """
    from dealix.launch_os.pipeline_tracker import PipelineTracker

    tracker = PipelineTracker()
    stages = ["RESEARCH", "OUTREACH", "DISCOVERY", "PROPOSAL", "WON"]
    for account, stage in zip(sample_accounts, stages):
        tracker.add(account_id=account["account_id"], company_name=account["company_name"], stage=stage)
    return tracker


@pytest.fixture()
def tmp_pipeline_file(tmp_path: Path) -> Path:
    """Return a temporary file path for pipeline persistence tests."""
    return tmp_path / "pipeline.json"
