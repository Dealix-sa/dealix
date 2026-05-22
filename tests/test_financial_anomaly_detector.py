"""Tests for the financial anomaly detector."""
from __future__ import annotations

from auto_client_acquisition.financial_autonomy.anomaly_detector import (
    Anomaly,
    detect_anomalies,
)
from auto_client_acquisition.financial_autonomy.metrics_aggregator import (
    FinancialMetricsSnapshot,
)


def _snapshot(**overrides) -> FinancialMetricsSnapshot:
    defaults: dict = dict(
        period_end="2026-05-22",
        mrr_sar=10_000.0,
        arr_sar=120_000.0,
        nrr_pct=100.0,
        churn_pct_monthly=2.0,
        arpa_sar=2_000.0,
        customers_active=5,
        customers_total_ever=6,
        gross_margin_pct=70.0,
        ltv_sar=24_000.0,
        cac_payback_months=4.0,
        runway_months=24.0,
        capital_assets_this_period=2,
        revenue_truth={},
        warnings=[],
        estimates_flagged=[],
    )
    defaults.update(overrides)
    return FinancialMetricsSnapshot(**defaults)


def test_no_previous_snapshot_returns_empty_list() -> None:
    assert detect_anomalies(_snapshot(), None) == []


def test_revenue_regression_detected() -> None:
    prev = _snapshot(mrr_sar=10_000.0)
    cur = _snapshot(mrr_sar=8_000.0)  # -20%
    out = detect_anomalies(cur, prev)
    kinds = {a.kind for a in out}
    assert "revenue_regression" in kinds


def test_small_mrr_change_is_not_a_regression() -> None:
    prev = _snapshot(mrr_sar=10_000.0)
    cur = _snapshot(mrr_sar=9_500.0)  # -5%
    out = detect_anomalies(cur, prev)
    kinds = {a.kind for a in out}
    assert "revenue_regression" not in kinds


def test_churn_spike_detected() -> None:
    prev = _snapshot(churn_pct_monthly=2.0)
    cur = _snapshot(churn_pct_monthly=9.0)  # +7pp
    out = detect_anomalies(cur, prev)
    kinds = {a.kind for a in out}
    assert "churn_spike" in kinds


def test_runway_dropped_detected() -> None:
    prev = _snapshot(runway_months=18.0)
    cur = _snapshot(runway_months=12.0)  # -6 months
    out = detect_anomalies(cur, prev)
    kinds = {a.kind for a in out}
    assert "runway_dropped" in kinds


def test_low_margin_emergence_detected() -> None:
    prev = _snapshot(gross_margin_pct=60.0)
    cur = _snapshot(gross_margin_pct=30.0)
    out = detect_anomalies(cur, prev)
    kinds = {a.kind for a in out}
    assert "low_margin_emergence" in kinds


def test_low_margin_only_fires_on_floor_crossing() -> None:
    """If margin was already below 35, the emergence rule does not fire."""
    prev = _snapshot(gross_margin_pct=30.0)
    cur = _snapshot(gross_margin_pct=25.0)
    out = detect_anomalies(cur, prev)
    kinds = {a.kind for a in out}
    assert "low_margin_emergence" not in kinds


def test_anomaly_to_dict_is_bilingual() -> None:
    prev = _snapshot(mrr_sar=10_000.0)
    cur = _snapshot(mrr_sar=8_000.0)
    a: Anomaly = detect_anomalies(cur, prev)[0]
    payload = a.to_dict()
    for key in (
        "kind",
        "severity",
        "evidence_ar",
        "evidence_en",
        "suggested_action_ar",
        "suggested_action_en",
    ):
        assert key in payload
    assert payload["evidence_ar"]
    assert payload["evidence_en"]


def test_detect_anomalies_accepts_dict_previous() -> None:
    prev = {"mrr_sar": 10_000.0, "churn_pct_monthly": 2.0}
    out = detect_anomalies(_snapshot(mrr_sar=7_000.0), prev)
    kinds = {a.kind for a in out}
    assert "revenue_regression" in kinds
