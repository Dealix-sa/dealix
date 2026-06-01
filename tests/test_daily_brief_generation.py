"""Verify daily brief generation produces correct markdown output."""
from __future__ import annotations

import pytest

from os_runtime.daily_brief import generate_brief


def test_empty_snapshot_returns_nonempty_string() -> None:
    result = generate_brief({})
    assert isinstance(result, str)
    assert len(result) > 0


def test_brief_includes_lead_count_when_provided() -> None:
    result = generate_brief({"leads": 5})
    assert "5" in result


def test_brief_includes_cash_sar_when_provided() -> None:
    result = generate_brief({"leads": 5, "cash_sar": 150000})
    assert "150" in result


def test_brief_includes_date() -> None:
    from datetime import date
    result = generate_brief({})
    today = date.today().isoformat()
    assert today in result


def test_brief_contains_pipeline_section() -> None:
    result = generate_brief({})
    assert "Pipeline" in result or "pipeline" in result


def test_brief_contains_cash_section() -> None:
    result = generate_brief({})
    assert "Cash" in result or "cash" in result


def test_brief_contains_projects_section() -> None:
    result = generate_brief({})
    assert "Project" in result or "project" in result


def test_top_leads_appear_in_brief() -> None:
    snapshot = {
        "top_leads": ["Alpha Corp", "Beta Facilities", "Gamma PMO"],
    }
    result = generate_brief(snapshot)
    assert "Alpha Corp" in result
    assert "Beta Facilities" in result


def test_at_risk_project_appears_in_brief() -> None:
    snapshot = {
        "projects": [
            {"name": "Project Omega", "at_risk": True},
            {"name": "Project Safe", "at_risk": False},
        ]
    }
    result = generate_brief(snapshot)
    assert "Project Omega" in result


def test_drafts_count_appears_in_brief() -> None:
    result = generate_brief({"drafts": 7})
    assert "7" in result


def test_calls_count_appears_in_brief() -> None:
    result = generate_brief({"calls": 3})
    assert "3" in result


def test_pipeline_value_appears_in_brief() -> None:
    result = generate_brief({"pipeline_value_sar": 500000})
    assert "500" in result
