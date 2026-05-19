"""Tests for the code-backed strategic decision ledger."""

from __future__ import annotations

import pytest

from auto_client_acquisition.strategy_autonomy.decision_ledger import (
    StrategicDecision,
    clear_for_test,
    get_decision,
    latest_decisions,
    query_decisions,
    record_decision,
)
from auto_client_acquisition.strategy_autonomy.decision_types import (
    StrategicDecisionType,
)


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "DEALIX_STRATEGIC_DECISION_LEDGER_PATH",
        str(tmp_path / "strategic-decision-ledger.jsonl"),
    )
    clear_for_test()
    yield
    clear_for_test()


def test_record_decision_reversible() -> None:
    decision = record_decision(
        cycle_id="cyc_1",
        decision_type=StrategicDecisionType.SCALE,
        target="total_revenue_sar",
        rationale_ar="سبب",
        rationale_en="reason",
        score=88.0,
        decision_band="scale",
        gate_ref="g_revenue_day90_build",
        evidence=["revenue=42000"],
    )
    assert isinstance(decision, StrategicDecision)
    assert decision.decision_type == "scale"
    assert decision.irreversible is False
    assert decision.requires_approval is False
    assert decision.status == "recommended"
    assert decision.decision_id.startswith("sd_")


def test_record_decision_irreversible_sets_flags() -> None:
    decision = record_decision(
        cycle_id="cyc_1",
        decision_type=StrategicDecisionType.HIRE,
        target="founder_hours_per_sprint",
        rationale_ar="سبب",
        rationale_en="reason",
        score=40.0,
        decision_band="hold",
        evidence=["founder_hours=8"],
        status="pending_approval",
    )
    assert decision.irreversible is True
    assert decision.requires_approval is True


def test_record_irreversible_refuses_empty_evidence() -> None:
    with pytest.raises(ValueError):
        record_decision(
            cycle_id="cyc_1",
            decision_type=StrategicDecisionType.KILL,
            target="offer",
            rationale_ar="سبب",
            rationale_en="reason",
            score=10.0,
            decision_band="kill",
            evidence=[],
        )


def test_query_and_get_decision() -> None:
    d1 = record_decision(
        cycle_id="cyc_1",
        decision_type=StrategicDecisionType.SCALE,
        target="rev",
        rationale_ar="a",
        rationale_en="a",
        score=90.0,
        decision_band="scale",
        evidence=["e"],
    )
    record_decision(
        cycle_id="cyc_2",
        decision_type=StrategicDecisionType.HIRE,
        target="hours",
        rationale_ar="b",
        rationale_en="b",
        score=40.0,
        decision_band="hold",
        evidence=["e"],
        status="pending_approval",
    )
    scale_rows = query_decisions(decision_type=StrategicDecisionType.SCALE)
    assert len(scale_rows) == 1
    pending = query_decisions(status="pending_approval")
    assert len(pending) == 1
    assert pending[0].decision_type == "hire"
    fetched = get_decision(d1.decision_id)
    assert fetched is not None and fetched.decision_id == d1.decision_id
    assert get_decision("sd_missing") is None


def test_latest_decisions() -> None:
    for i in range(5):
        record_decision(
            cycle_id=f"cyc_{i}",
            decision_type=StrategicDecisionType.HOLD,
            target="rev",
            rationale_ar="a",
            rationale_en="a",
            score=50.0,
            decision_band="hold",
        )
    rows = latest_decisions(limit=3)
    assert len(rows) == 3


def test_to_dict_round_trip() -> None:
    decision = record_decision(
        cycle_id="cyc_1",
        decision_type=StrategicDecisionType.HOLD,
        target="rev",
        rationale_ar="a",
        rationale_en="a",
        score=50.0,
        decision_band="hold",
    )
    data = decision.to_dict()
    assert isinstance(data["evidence"], list)
    assert data["decision_type"] == "hold"
