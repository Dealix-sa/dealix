"""Tests for the strategic signal aggregator."""

from __future__ import annotations

from auto_client_acquisition.intelligence_os.strategy_decision import (
    StrategySignalInputs,
)
from auto_client_acquisition.strategy_autonomy.signal_aggregator import (
    StrategicSignalSnapshot,
    aggregate_strategic_signals,
)


def test_aggregate_returns_snapshot() -> None:
    snap = aggregate_strategic_signals(
        on_date="2026-06-15",
        pipeline_summary={
            "paid": 4,
            "commitments": 5,
            "total_revenue_sar": 42000,
            "mrr_sar": 9000,
            "retainer_count": 4,
            "proof_score": 88,
        },
    )
    assert isinstance(snap, StrategicSignalSnapshot)
    assert snap.total_revenue_sar == 42000
    assert snap.retainer_count == 4
    assert snap.days_since_launch > 0


def test_signal_inputs_are_seven_normalized() -> None:
    snap = aggregate_strategic_signals(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 40000, "retainer_count": 3},
    )
    keys = set(snap.signal_inputs.keys())
    assert keys == {
        "revenue",
        "margin",
        "proof",
        "repeatability",
        "governance",
        "productization",
        "moat",
    }
    for value in snap.signal_inputs.values():
        assert 0.0 <= value <= 100.0
    # 40K revenue and 3 retainers hit the day-90 targets.
    assert snap.signal_inputs["revenue"] == 100.0
    assert snap.signal_inputs["repeatability"] == 100.0


def test_as_strategy_inputs() -> None:
    snap = aggregate_strategic_signals(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 20000},
    )
    inputs = snap.as_strategy_inputs()
    assert isinstance(inputs, StrategySignalInputs)
    assert 0.0 <= inputs.revenue_signal <= 100.0


def test_aggregate_friction_safe_on_bad_input() -> None:
    # An empty pipeline summary must not crash — it falls back to zeros.
    snap = aggregate_strategic_signals(on_date="2026-06-15", pipeline_summary=None)
    assert isinstance(snap, StrategicSignalSnapshot)
    assert snap.total_revenue_sar == 0
    assert isinstance(snap.warnings, list)


def test_to_dict() -> None:
    snap = aggregate_strategic_signals(on_date="2026-06-15")
    data = snap.to_dict()
    assert data["on_date"] == "2026-06-15"
    assert "signal_inputs" in data


def test_snapshot_carries_cs_and_financial_fields() -> None:
    """The strategic snapshot must expose CS+Financial signals as fields.

    They default to safe values when the sister autonomy layers have no
    persisted reports yet, so the aggregator stays friction-safe.
    """
    snap = aggregate_strategic_signals(on_date="2026-06-15")
    # CS fields are always present and integer-typed.
    assert isinstance(snap.cs_at_risk_count, int)
    assert isinstance(snap.cs_expansion_ready_count, int)
    assert isinstance(snap.cs_renewals_due_count, int)
    assert isinstance(snap.cs_nps_detractors_count, int)
    # Financial fields exist with safe defaults.
    assert isinstance(snap.financial_anomaly_count, int)
    assert isinstance(snap.financial_violation_count, int)
    assert isinstance(snap.runway_months, float)
    assert isinstance(snap.gross_margin_pct, float)
    assert isinstance(snap.margin_floor_violation, bool)
    assert isinstance(snap.runway_critical, bool)


def test_snapshot_reads_latest_cs_and_financial_reports(tmp_path, monkeypatch) -> None:
    """When CS + Financial cycles have run, the aggregator picks them up."""
    from auto_client_acquisition.customer_success_autonomy import (
        run_customer_success_cycle,
    )
    from auto_client_acquisition.financial_autonomy import run_financial_cycle

    # Run a CS cycle with churn-prone inputs so at_risk > 0.
    cs_inputs = {
        "C_RISK": {
            "engagement_drop_pct": 60,
            "support_escalations_last_30d": 4,
            "payment_late_count": 2,
            "nps_below_7": True,
            "decision_maker_left": True,
            "recent_nps_score": 3,
        }
    }
    run_customer_success_cycle(
        customer_ids=["C_RISK"],
        on_date="2026-06-14",
        inputs_by_customer=cs_inputs,
    )
    run_financial_cycle(period_end="2026-06-14", cadence="weekly")

    snap = aggregate_strategic_signals(on_date="2026-06-15")
    # Both sister layers have produced a report, so reading them must
    # not append a warning.
    cs_warnings = [w for w in snap.warnings if w.startswith("customer_success_autonomy")]
    fin_warnings = [w for w in snap.warnings if w.startswith("financial_autonomy")]
    assert cs_warnings == []
    assert fin_warnings == []
