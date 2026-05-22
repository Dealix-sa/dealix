"""Doctrine guardrails for the financial autonomy layer.

These tests are the wired-in proof that the 11 non-negotiables hold:
- no live send / no live charge / no auto-refund
- every high-stakes financial signal is gated on a founder approval
- no forbidden marketing language in any draft
- the hard-gates list is asserted in every report
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.financial_autonomy.board_memo_cycle import (
    run_board_memo_cycle,
)
from auto_client_acquisition.financial_autonomy.financial_cycle import (
    run_financial_cycle,
)
from auto_client_acquisition.financial_autonomy.threshold_rules import (
    FINANCIAL_THRESHOLDS,
)


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "DEALIX_FINANCIAL_CYCLES_PATH",
        str(tmp_path / "financial_cycles"),
    )
    monkeypatch.setenv(
        "DEALIX_BOARD_MEMOS_PATH",
        str(tmp_path / "board_memos"),
    )
    monkeypatch.setenv(
        "DEALIX_CAPITAL_LEDGER_PATH",
        str(tmp_path / "capital-ledger.jsonl"),
    )
    monkeypatch.setenv(
        "DEALIX_FRICTION_LOG_PATH",
        str(tmp_path / "friction.jsonl"),
    )
    get_default_approval_store().clear()
    yield
    get_default_approval_store().clear()


_FORBIDDEN_PATTERNS: tuple[str, ...] = (
    r"\bguaranteed\b",
    r"\bblast\b",
    r"\bscraping\b",
    "نضمن",
)


def _scan_text(text: str) -> None:
    for pattern in _FORBIDDEN_PATTERNS:
        assert not re.search(
            pattern, text, flags=re.IGNORECASE
        ), f"forbidden token matched: {pattern!r}"


def test_financial_cycle_hard_gates_assert_doctrine() -> None:
    report = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    assert "no_live_send" in report.hard_gates
    assert "no_live_charge" in report.hard_gates
    assert "no_auto_refund" in report.hard_gates
    assert "approval_required_for_financial_decisions" in report.hard_gates
    assert "no_fake_revenue" in report.hard_gates


def test_financial_cycle_routes_signals_to_approval_queue() -> None:
    """Every high-stakes signal must produce a pending approval."""
    report = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    # Margin floor breach must always create an approval in the zero-state
    # default snapshot.
    assert report.approvals_pending["count"] >= 1
    # No approval is ever in ``approved_execute`` mode for a financial
    # decision — they must all be founder-gated.
    pending = get_default_approval_store().list_pending()
    for item in pending:
        if item.object_type == "financial_decision":
            assert item.action_mode == "approval_required"


def test_board_memo_cycle_creates_founder_approval() -> None:
    """The memo is never shared automatically — it carries a pending gate."""
    report = run_board_memo_cycle(month="2026-05")
    assert report.approval_id.startswith("apr_")
    pending = get_default_approval_store().list_pending()
    target = next(p for p in pending if p.approval_id == report.approval_id)
    assert target.object_type == "board_memo"
    assert target.action_mode == "approval_required"


def test_no_forbidden_marketing_language_in_threshold_catalog() -> None:
    for rule in FINANCIAL_THRESHOLDS:
        _scan_text(rule.title_en)
        _scan_text(rule.title_ar)
        _scan_text(rule.reason_en)
        _scan_text(rule.reason_ar)


def test_no_forbidden_marketing_language_in_persisted_memo() -> None:
    report = run_board_memo_cycle(month="2026-05")
    md_path = report.report_paths.get("md")
    assert md_path
    text = Path(md_path).read_text(encoding="utf-8")
    _scan_text(text)


def test_refund_rule_requires_founder_approval() -> None:
    """Documented-only refund rule must be approval-gated, never auto."""
    rule = next(r for r in FINANCIAL_THRESHOLDS if r.rule_id == "refund_per_request")
    assert rule.action_on_violation == "approval_required"
    assert rule.severity == "high"


def test_price_change_rule_requires_founder_approval() -> None:
    rule = next(
        r for r in FINANCIAL_THRESHOLDS if r.rule_id == "price_change_significant"
    )
    assert rule.action_on_violation == "approval_required"


def test_runway_critical_escalates_to_board() -> None:
    rule = next(r for r in FINANCIAL_THRESHOLDS if r.rule_id == "runway_critical")
    assert rule.action_on_violation == "escalate_board"
    assert rule.severity == "critical"
