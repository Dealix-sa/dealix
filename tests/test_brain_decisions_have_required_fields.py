"""Test that every decision produced by the brain includes all required fields."""
from __future__ import annotations

import os
import sys

import pytest

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from scripts.brain import DECISION_REQUIRED_FIELDS
from scripts.brain.generate_daily_decision import generate_daily_decision


def test_decision_has_all_required_fields(tmp_path):
    ledger = tmp_path / "decisions_log.csv"
    record = generate_daily_decision(
        decision="Test decision.",
        why_now="Test why now.",
        assumption="Test assumption.",
        confidence="medium",
        owner="Test Owner",
        next_action="Test next action.",
        success_metric="Test success metric.",
        review_date="2026-12-31",
        risk_if_delayed="Test risk.",
        ledger_path=str(ledger),
    )
    for field in DECISION_REQUIRED_FIELDS:
        assert field in record, f"Missing field '{field}' in decision record"
        assert str(record[field]).strip(), f"Field '{field}' is empty in decision record"


def test_decision_rejects_missing_field(tmp_path):
    ledger = tmp_path / "decisions_log.csv"
    with pytest.raises(ValueError, match="missing required field"):
        generate_daily_decision(
            decision="Test decision.",
            why_now="",
            assumption="Test assumption.",
            confidence="medium",
            owner="Test Owner",
            next_action="Test next action.",
            success_metric="Test success metric.",
            review_date="2026-12-31",
            risk_if_delayed="Test risk.",
            ledger_path=str(ledger),
        )


def test_decision_rejects_invalid_confidence(tmp_path):
    ledger = tmp_path / "decisions_log.csv"
    with pytest.raises(ValueError, match="confidence"):
        generate_daily_decision(
            decision="Test decision.",
            why_now="why",
            assumption="assumption",
            confidence="certain",
            owner="Owner",
            next_action="action",
            success_metric="metric",
            review_date="2026-12-31",
            risk_if_delayed="risk",
            ledger_path=str(ledger),
        )


def test_decision_logged_to_csv(tmp_path):
    ledger = tmp_path / "decisions_log.csv"
    generate_daily_decision(
        decision="Logged decision.",
        why_now="why",
        assumption="assumption",
        confidence="high",
        owner="Owner",
        next_action="action",
        success_metric="metric",
        review_date="2026-12-31",
        risk_if_delayed="risk",
        ledger_path=str(ledger),
    )
    assert ledger.exists()
    content = ledger.read_text(encoding="utf-8")
    assert "Logged decision." in content
    # Header should contain all required fields.
    for field in DECISION_REQUIRED_FIELDS:
        assert field in content, f"CSV header missing field '{field}'"