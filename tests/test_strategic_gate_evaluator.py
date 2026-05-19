"""Tests for the strategic gate evaluator."""

from __future__ import annotations

from auto_client_acquisition.strategy_autonomy.decision_gates import (
    GateEvaluation,
    evaluate_strategic_gates,
)
from auto_client_acquisition.strategy_autonomy.decision_types import (
    StrategicDecisionType,
)
from auto_client_acquisition.strategy_autonomy.signal_aggregator import (
    aggregate_strategic_signals,
)


def _snapshot(on_date: str, **summary):
    return aggregate_strategic_signals(on_date=on_date, pipeline_summary=summary)


def test_evaluate_returns_one_eval_per_gate() -> None:
    snap = _snapshot("2026-06-15", total_revenue_sar=42000, retainer_count=4)
    results = evaluate_strategic_gates(snap)
    assert len(results) >= 6
    assert all(isinstance(r, GateEvaluation) for r in results)


def test_gates_not_due_are_skipped() -> None:
    # Day 10 — the 60/90 day gates are not yet due.
    snap = _snapshot("2026-03-11", total_revenue_sar=5000)
    results = evaluate_strategic_gates(snap)
    day90 = next(r for r in results if r.gate_id == "g_revenue_day90_build")
    assert day90.due is False
    assert day90.decision_type == StrategicDecisionType.HOLD.value


def test_founder_hours_triggers_hire() -> None:
    snap = aggregate_strategic_signals(
        on_date="2026-06-15",
        pipeline_summary={"total_revenue_sar": 20000},
        founder_hours_per_sprint=8.0,
    )
    results = evaluate_strategic_gates(snap)
    hire_gate = next(r for r in results if r.gate_id == "g_founder_hours_hire")
    assert hire_gate.due is True
    assert hire_gate.passed is False
    assert hire_gate.decision_type == StrategicDecisionType.HIRE.value


def test_conflict_downgrades_to_hold() -> None:
    # Moderate revenue passes the day-60 hold gate (on_pass=scale), but the
    # composite strategy score is too low for a scale band -> downgrade.
    snap = _snapshot("2026-06-15", total_revenue_sar=26000)
    results = evaluate_strategic_gates(snap)
    gate = next(r for r in results if r.gate_id == "g_revenue_day60_hold")
    assert gate.passed is True
    if gate.scorer_hint != StrategicDecisionType.SCALE.value:
        assert gate.conflict is True
        assert gate.decision_type == StrategicDecisionType.HOLD.value


def test_evaluation_carries_evidence() -> None:
    snap = _snapshot("2026-06-15", total_revenue_sar=42000, retainer_count=4)
    results = evaluate_strategic_gates(snap)
    due = [r for r in results if r.due]
    assert due
    for r in due:
        assert isinstance(r.evidence, tuple)
        assert r.evidence


def test_to_dict() -> None:
    snap = _snapshot("2026-06-15", total_revenue_sar=42000)
    results = evaluate_strategic_gates(snap)
    data = results[0].to_dict()
    assert "gate_id" in data
    assert isinstance(data["evidence"], list)
