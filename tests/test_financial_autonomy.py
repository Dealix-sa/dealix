"""Tests for the Financial Autonomy layer.

Covers the metrics aggregator (friction-safe with no DB), the codified
threshold catalogue, anomaly detection, the end-to-end financial cycle,
the monthly board-memo cycle, and the doctrine assertions (no live
charge, every high-stakes decision is approval-gated).
"""
from __future__ import annotations

from auto_client_acquisition.financial_autonomy import (
    FINANCIAL_THRESHOLDS,
    BoardMemoReport,
    FinancialCycleReport,
    FinancialMetricsSnapshot,
    aggregate_financial_metrics,
    detect_anomalies,
    evaluate_thresholds,
    latest_board_memo,
    latest_financial_report,
    run_board_memo_cycle,
    run_financial_cycle,
)


# --- metrics aggregator ----------------------------------------------------

def test_aggregator_returns_snapshot_with_no_db() -> None:
    snap = aggregate_financial_metrics(period_end="2026-05-22")
    assert isinstance(snap, FinancialMetricsSnapshot)
    assert isinstance(snap.warnings, list)
    # estimates_flagged is non-empty when we fell back to defaults.
    assert isinstance(snap.estimates_flagged, list)


def test_aggregator_snapshot_to_dict_shape() -> None:
    snap = aggregate_financial_metrics(period_end="2026-05-22")
    d = snap.to_dict()
    for key in (
        "mrr_sar",
        "arr_sar",
        "nrr_pct",
        "churn_pct_monthly",
        "runway_months",
        "gross_margin_pct",
        "ltv_sar",
        "cac_payback_months",
    ):
        assert key in d


# --- threshold catalogue ---------------------------------------------------

def test_thresholds_catalogue_has_minimum_rules() -> None:
    assert len(FINANCIAL_THRESHOLDS) >= 6
    rule_ids = {r.rule_id for r in FINANCIAL_THRESHOLDS}
    expected = {
        "gross_margin_floor",
        "runway_critical",
        "cac_payback_ceiling",
        "churn_spike",
    }
    assert expected.issubset(rule_ids)


def test_thresholds_bilingual_metadata() -> None:
    for r in FINANCIAL_THRESHOLDS:
        assert r.title_ar and r.title_en, "every rule must be bilingual"
        assert r.severity in {"low", "medium", "high", "critical"}
        assert r.action_on_violation in {"flag", "approval_required", "escalate_board"}


def test_evaluate_thresholds_fires_on_low_margin() -> None:
    import dataclasses as _dc

    snap = aggregate_financial_metrics(period_end="2026-05-22")
    # Override to clearly-violating state (frozen dataclass — use replace).
    bad = _dc.replace(snap, gross_margin_pct=10.0, runway_months=3.0)
    violations = evaluate_thresholds(bad)
    kinds = {v.rule.rule_id for v in violations}
    assert "gross_margin_floor" in kinds
    assert "runway_critical" in kinds


# --- anomaly detector ------------------------------------------------------

def test_anomaly_detector_no_previous_returns_empty() -> None:
    snap = aggregate_financial_metrics(period_end="2026-05-22")
    anomalies = detect_anomalies(snap.to_dict(), None)
    assert anomalies == []


def test_anomaly_detector_flags_revenue_regression() -> None:
    current = {"mrr_sar": 5000.0, "churn_pct_monthly": 5.0, "runway_months": 12.0, "gross_margin_pct": 50.0}
    previous = {"mrr_sar": 10000.0, "churn_pct_monthly": 2.0, "runway_months": 12.0, "gross_margin_pct": 50.0}
    anomalies = detect_anomalies(current, previous)
    kinds = {a.kind for a in anomalies}
    # MRR halved — regression should fire.
    assert "revenue_regression" in kinds


# --- end-to-end financial cycle --------------------------------------------

def test_run_financial_cycle_produces_report() -> None:
    rep = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    assert isinstance(rep, FinancialCycleReport)
    assert rep.cycle_id
    assert rep.cadence == "weekly"
    assert "mrr_sar" in rep.metrics
    assert isinstance(rep.threshold_violations, list)
    assert "approval_required_for_financial_decisions" in rep.hard_gates


def test_financial_cycle_writes_report_files() -> None:
    rep = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    assert rep.report_paths
    assert "json" in rep.report_paths
    assert "md" in rep.report_paths


def test_latest_financial_report_returns_dict_or_none() -> None:
    run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    latest = latest_financial_report()
    assert latest is None or isinstance(latest, dict)


# --- board-memo cycle ------------------------------------------------------

def test_board_memo_cycle_builds_12_sections() -> None:
    rep = run_board_memo_cycle(month="2026-05")
    assert isinstance(rep, BoardMemoReport)
    assert len(rep.sections) >= 12
    # Every section dict carries bilingual titles.
    for slug, block in rep.sections.items():
        assert "title_ar" in block and "title_en" in block, slug


def test_board_memo_routes_approval() -> None:
    rep = run_board_memo_cycle(month="2026-05")
    # An approval is requested for the founder to review before sharing.
    assert rep.approval_id, "board memo must be approval-gated"


def test_board_memo_rejects_bad_month() -> None:
    import pytest as _pytest

    with _pytest.raises(ValueError):
        run_board_memo_cycle(month="2026/05")  # wrong separator
    with _pytest.raises(ValueError):
        run_board_memo_cycle(month="not-a-month")


def test_latest_board_memo_lookup() -> None:
    run_board_memo_cycle(month="2026-05")
    found = latest_board_memo("2026-05")
    assert found is None or isinstance(found, dict)


# --- doctrine assertions ---------------------------------------------------

def test_financial_cycle_never_auto_charges() -> None:
    rep = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    # The doctrine hard gates must always be re-asserted in every report.
    for gate in (
        "no_live_send",
        "no_live_charge",
        "no_auto_refund",
        "approval_required_for_financial_decisions",
    ):
        assert gate in rep.hard_gates


def test_high_severity_violations_create_approvals() -> None:
    rep = run_financial_cycle(period_end="2026-05-22", cadence="weekly")
    high = [v for v in rep.threshold_violations if v.get("severity") in {"high", "critical"}]
    if high:
        # At least one approval must be queued for the founder.
        assert rep.approvals_pending.get("count", 0) >= 1
