"""Tests for the financial threshold rule catalog and evaluator."""
from __future__ import annotations

from auto_client_acquisition.financial_autonomy.metrics_aggregator import (
    FinancialMetricsSnapshot,
)
from auto_client_acquisition.financial_autonomy.threshold_rules import (
    FINANCIAL_THRESHOLDS,
    ThresholdRule,
    ThresholdViolation,
    evaluate_thresholds,
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


def test_catalog_has_expected_rules() -> None:
    rule_ids = {r.rule_id for r in FINANCIAL_THRESHOLDS}
    for required in (
        "gross_margin_floor",
        "runway_critical",
        "runway_warning",
        "cac_payback_ceiling",
        "churn_spike",
        "nrr_floor",
        "refund_per_request",
        "price_change_significant",
    ):
        assert required in rule_ids


def test_rule_to_dict_round_trip() -> None:
    for rule in FINANCIAL_THRESHOLDS:
        payload = rule.to_dict()
        for key in (
            "rule_id",
            "source",
            "title_ar",
            "title_en",
            "metric",
            "comparator",
            "threshold",
            "severity",
            "action_on_violation",
            "reason_ar",
            "reason_en",
        ):
            assert key in payload


def test_evaluate_thresholds_healthy_snapshot_no_violations() -> None:
    out = evaluate_thresholds(_snapshot())
    # 24-month runway, 70% margin, 2% churn, 100% NRR, 4-month CAC payback
    rule_ids = {v.rule.rule_id for v in out}
    assert "gross_margin_floor" not in rule_ids
    assert "runway_critical" not in rule_ids
    assert "churn_spike" not in rule_ids


def test_evaluate_thresholds_margin_floor() -> None:
    out = evaluate_thresholds(_snapshot(gross_margin_pct=20.0))
    rule_ids = {v.rule.rule_id for v in out}
    assert "gross_margin_floor" in rule_ids


def test_evaluate_thresholds_runway_critical_and_warning_both_fire() -> None:
    """A 5-month runway breaches both <12 (warning) and <6 (critical)."""
    out = evaluate_thresholds(_snapshot(runway_months=5.0))
    rule_ids = {v.rule.rule_id for v in out}
    assert "runway_critical" in rule_ids
    assert "runway_warning" in rule_ids


def test_evaluate_thresholds_churn_spike_high_severity() -> None:
    out = evaluate_thresholds(_snapshot(churn_pct_monthly=12.0))
    violation = next(v for v in out if v.rule.rule_id == "churn_spike")
    assert violation.action_on_violation == "approval_required"
    assert violation.observed_value == 12.0


def test_evaluate_thresholds_documented_rules_not_metric_driven() -> None:
    """``refund_per_request`` has no metric on the snapshot."""
    out = evaluate_thresholds(_snapshot())
    rule_ids = {v.rule.rule_id for v in out}
    # The metric-less rules never fire from a snapshot.
    assert "refund_per_request" not in rule_ids
    assert "price_change_significant" not in rule_ids


def test_violation_to_dict() -> None:
    out = evaluate_thresholds(_snapshot(nrr_pct=50.0))
    violation = next(v for v in out if v.rule.rule_id == "nrr_floor")
    payload = violation.to_dict()
    assert payload["rule"]["rule_id"] == "nrr_floor"
    assert payload["breached"] is True
    assert payload["observed_value"] == 50.0


def test_rule_dataclass_is_frozen() -> None:
    rule = FINANCIAL_THRESHOLDS[0]
    assert isinstance(rule, ThresholdRule)
    try:
        rule.threshold = 0.0  # type: ignore[misc]
    except Exception:
        return
    raise AssertionError("ThresholdRule must be frozen")
