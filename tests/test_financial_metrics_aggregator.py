"""Tests for the financial metrics aggregator."""
from __future__ import annotations

import pytest

from auto_client_acquisition.financial_autonomy.metrics_aggregator import (
    FinancialMetricsSnapshot,
    aggregate_financial_metrics,
)


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "DEALIX_CAPITAL_LEDGER_PATH",
        str(tmp_path / "capital-ledger.jsonl"),
    )
    yield


def test_aggregate_returns_snapshot_dataclass() -> None:
    snap = aggregate_financial_metrics(period_end="2026-05-22")
    assert isinstance(snap, FinancialMetricsSnapshot)
    assert snap.period_end == "2026-05-22"


def test_aggregate_zero_state_flags_estimates() -> None:
    """With no DB-backed history the aggregator must flag every estimate."""
    snap = aggregate_financial_metrics(period_end="2026-05-22")
    assert snap.mrr_sar == 0.0
    assert snap.arr_sar == 0.0
    # documented defaults are flagged
    for key in (
        "gross_margin_pct",
        "ltv_sar",
        "cac_payback_months",
        "runway_months",
        "cash_on_hand_estimate",
        "monthly_burn_estimate",
    ):
        assert key in snap.estimates_flagged
    # warnings include the no-paid-history flag
    assert "no_paid_history_available" in snap.warnings


def test_aggregate_period_end_default_is_today() -> None:
    snap = aggregate_financial_metrics(period_end=None)
    # ISO date string YYYY-MM-DD
    assert len(snap.period_end) == 10
    assert snap.period_end[4] == "-"


def test_aggregate_runway_positive() -> None:
    """Runway must always be a positive number when defaults are in use."""
    snap = aggregate_financial_metrics(period_end="2026-05-22")
    assert snap.runway_months > 0.0


def test_snapshot_to_dict_is_serializable() -> None:
    snap = aggregate_financial_metrics(period_end="2026-05-22")
    payload = snap.to_dict()
    for key in (
        "period_end",
        "mrr_sar",
        "arr_sar",
        "nrr_pct",
        "churn_pct_monthly",
        "arpa_sar",
        "customers_active",
        "customers_total_ever",
        "gross_margin_pct",
        "ltv_sar",
        "cac_payback_months",
        "runway_months",
        "capital_assets_this_period",
        "revenue_truth",
        "warnings",
        "estimates_flagged",
    ):
        assert key in payload


def test_aggregate_with_date_object() -> None:
    from datetime import date

    snap = aggregate_financial_metrics(period_end=date(2026, 5, 22))
    assert snap.period_end == "2026-05-22"
