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
