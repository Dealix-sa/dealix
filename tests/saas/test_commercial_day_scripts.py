"""Tests for commercial day scripts and CRM account manager."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure scripts/commercial is importable
_SCRIPTS_COMMERCIAL = Path(__file__).parents[2] / "scripts" / "commercial"
if str(_SCRIPTS_COMMERCIAL) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_COMMERCIAL))


# ---------------------------------------------------------------------------
# Import smoke tests
# ---------------------------------------------------------------------------


def test_run_commercial_day_imports() -> None:
    """Verify run_commercial_day.py can be imported without side effects."""
    import importlib
    spec = importlib.util.spec_from_file_location(
        "run_commercial_day", _SCRIPTS_COMMERCIAL / "run_commercial_day.py"
    )
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert mod is not None


def test_score_accounts_imports() -> None:
    """Verify score_accounts.py can be imported."""
    import importlib
    spec = importlib.util.spec_from_file_location(
        "score_accounts", _SCRIPTS_COMMERCIAL / "score_accounts.py"
    )
    assert spec is not None


def test_generate_ceo_brief_imports() -> None:
    """Verify generate_ceo_brief.py can be imported."""
    import importlib
    spec = importlib.util.spec_from_file_location(
        "generate_ceo_brief", _SCRIPTS_COMMERCIAL / "generate_ceo_brief.py"
    )
    assert spec is not None


# ---------------------------------------------------------------------------
# Account scoring logic
# ---------------------------------------------------------------------------


def test_score_accounts_logic() -> None:
    """Score a sample account and verify tier and breakdown fields."""
    from score_accounts import score_account

    account = {
        "company_name": "Al-Test Automotive",
        "sector": "automotive",
        "employee_count": 50,
        "pain_signals": ["manual_followup", "missed_leads", "no_crm"],
        "has_whatsapp": True,
        "has_email": True,
        "prior_contact": False,
    }
    result = score_account(account)
    assert result["score"] == 30 + 20 + 30 + 15  # sector + size + pain + whatsapp+email
    assert result["tier"] == "HOT"
    assert "score_breakdown" in result
    assert result["score_breakdown"]["sector_fit"] == 30
    assert result["score_breakdown"]["size_fit"] == 20
    assert result["score_breakdown"]["pain_signal"] == 30


def test_score_accounts_cold_tier() -> None:
    """An account with no signals should be COLD."""
    from score_accounts import score_account

    account = {
        "sector": "unknown_sector_xyz",
        "employee_count": 2,
        "pain_signals": [],
        "has_whatsapp": False,
        "has_email": False,
        "prior_contact": False,
    }
    result = score_account(account)
    assert result["tier"] == "COLD"
    assert result["score"] < 40


def test_score_accounts_tier_thresholds() -> None:
    """Verify WARM tier boundary."""
    from score_accounts import score_account

    account = {
        "sector": "professional_services",  # 18 pts
        "employee_count": 50,              # 20 pts
        "pain_signals": ["one_pain"],      # 12 pts
        "has_whatsapp": True,              # 10 pts
        "has_email": False,
        "prior_contact": False,
    }
    result = score_account(account)
    # 18 + 20 + 12 + 10 = 60 -> WARM
    assert result["score"] == 60
    assert result["tier"] == "WARM"


# ---------------------------------------------------------------------------
# CRM AccountManager
# ---------------------------------------------------------------------------


def test_account_manager_add_get() -> None:
    """Add an account and retrieve it."""
    from company.crm.account_manager import AccountManager, AccountRecord

    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "accounts.json"
        mgr = AccountManager(accounts_path=path)

        rec = AccountRecord(
            company_name="Test Co",
            sector="automotive",
            size="50-100",
            city="Riyadh",
            pain_hypothesis="manual WhatsApp follow-up",
            score=85,
            tier="HOT",
            status="prospect",
        )
        mgr.add_account(rec)
        hot = mgr.get_hot_accounts()
        assert len(hot) == 1
        assert hot[0]["company_name"] == "Test Co"


def test_account_manager_update_status() -> None:
    """update_status changes the stage of the matching account."""
    from company.crm.account_manager import AccountManager, AccountRecord

    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "accounts.json"
        mgr = AccountManager(accounts_path=path)

        rec = AccountRecord(
            company_name="Beta Corp",
            sector="retail",
            size="10-50",
            city="Jeddah",
            pain_hypothesis="no review management",
            score=65,
            tier="WARM",
            status="prospect",
        )
        mgr.add_account(rec)
        result = mgr.update_status(rec.id, "qualified")
        assert result is True
        accounts = mgr.get_accounts_by_stage("qualified")
        assert len(accounts) == 1


def test_account_manager_export_markdown() -> None:
    """export_to_markdown returns non-empty markdown string."""
    from company.crm.account_manager import AccountManager, AccountRecord

    with tempfile.TemporaryDirectory() as td:
        accounts_path = Path(td) / "accounts.json"
        report_path = Path(td) / "accounts_report.md"
        mgr = AccountManager(accounts_path=accounts_path)

        mgr.add_account(
            AccountRecord(
                company_name="Gamma LLC",
                sector="hospitality",
                size="20-50",
                city="Dammam",
                pain_hypothesis="WhatsApp ops chaos",
                score=90,
                tier="HOT",
            )
        )
        content = mgr.export_to_markdown(report_path=report_path)
        assert "Gamma LLC" in content
        assert "HOT" in content


# ---------------------------------------------------------------------------
# CEO brief generation
# ---------------------------------------------------------------------------


def test_ceo_brief_generates_output() -> None:
    """build_brief returns a dict with required keys."""
    from generate_ceo_brief import build_brief

    brief = build_brief(today="2026-06-26")
    assert brief["date"] == "2026-06-26"
    assert "revenue" in brief
    assert "pipeline" in brief
    assert "top_priorities" in brief
    assert "risk_flags" in brief
    assert "founder_decisions_needed" in brief
    assert "what_not_to_do_today" in brief


def test_ceo_brief_render_markdown() -> None:
    """render_markdown returns non-empty markdown with expected sections."""
    from generate_ceo_brief import build_brief, render_markdown

    brief = build_brief(today="2026-06-26")
    md = render_markdown(brief)
    assert "CEO Brief" in md
    assert "Risk Flags" in md
    assert "Founder Decisions" in md


# ---------------------------------------------------------------------------
# Safety gate enforcement
# ---------------------------------------------------------------------------


def test_safety_gate_enforced() -> None:
    """run_commercial_day must raise AssertionError if EXTERNAL_SEND_ENABLED is True."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "run_commercial_day_test",
        _SCRIPTS_COMMERCIAL / "run_commercial_day.py",
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)

    # Inject a True value for EXTERNAL_SEND_ENABLED before executing module
    original = os.environ.get("EXTERNAL_SEND_ENABLED")
    os.environ["EXTERNAL_SEND_ENABLED"] = "true"
    try:
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        with pytest.raises(AssertionError):
            mod._assert_safe()
    finally:
        if original is None:
            os.environ.pop("EXTERNAL_SEND_ENABLED", None)
        else:
            os.environ["EXTERNAL_SEND_ENABLED"] = original
