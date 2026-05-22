"""Tests for the autonomous financial router."""
from __future__ import annotations

import asyncio

import pytest

from api.routers.autonomous_financial import (
    _RunBody,
    board_memo,
    board_memo_run,
    latest,
    router,
    run,
    thresholds,
)
from api.security.api_key import require_admin_key
from auto_client_acquisition.approval_center import get_default_approval_store


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


def test_router_prefix() -> None:
    assert router.prefix == "/api/v1/financial/autonomous"


def test_latest_empty_state() -> None:
    payload = asyncio.run(latest())
    assert payload["empty"] is True
    assert payload["governance_decision"] == "allow"
    assert "title_en" in payload
    assert "title_ar" in payload


def test_run_returns_report() -> None:
    payload = asyncio.run(
        run(_RunBody(period_end="2026-05-22", cadence="weekly"))
    )
    for key in (
        "cycle_id",
        "period_end",
        "cadence",
        "metrics",
        "anomalies",
        "threshold_violations",
        "approvals_pending",
        "hard_gates",
        "warnings",
    ):
        assert key in payload
    assert payload["governance_decision"] == "allow_with_review"


def test_run_is_admin_gated() -> None:
    run_route = next(
        r for r in router.routes if r.path.endswith("/run") and "POST" in r.methods
    )
    dep_calls = [d.call for d in run_route.dependant.dependencies]
    assert require_admin_key in dep_calls


def test_board_memo_run_is_admin_gated() -> None:
    memo_route = next(
        r
        for r in router.routes
        if r.path.endswith("/board-memo/run") and "POST" in r.methods
    )
    dep_calls = [d.call for d in memo_route.dependant.dependencies]
    assert require_admin_key in dep_calls


def test_latest_after_run() -> None:
    asyncio.run(run(_RunBody(period_end="2026-05-22", cadence="weekly")))
    payload = asyncio.run(latest())
    assert payload["empty"] is False
    assert payload["period_end"] == "2026-05-22"


def test_thresholds_endpoint() -> None:
    payload = asyncio.run(thresholds())
    assert "thresholds" in payload
    rule_ids = {t["rule_id"] for t in payload["thresholds"]}
    for required in ("gross_margin_floor", "runway_critical", "refund_per_request"):
        assert required in rule_ids
    assert payload["governance_decision"] == "allow"


def test_board_memo_get_empty_state() -> None:
    payload = asyncio.run(board_memo("2026-05"))
    assert payload["empty"] is True
    assert payload["governance_decision"] == "allow"


def test_board_memo_invalid_month_handled() -> None:
    payload = asyncio.run(board_memo("not-a-month"))
    assert payload["empty"] is True
    assert payload["governance_decision"] == "block"


def test_board_memo_run_persists_and_get_returns_it() -> None:
    created = asyncio.run(board_memo_run("2026-05"))
    assert created["month"] == "2026-05"
    fetched = asyncio.run(board_memo("2026-05"))
    assert fetched["empty"] is False
    assert fetched["approval_id"]
