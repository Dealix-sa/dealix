"""Tests for opportunity scoring + the orchestrator's signal mapping."""

from __future__ import annotations

from dealix.hermes.core.schemas import HermesOpportunity, HermesSignal
from dealix.hermes.core.scoring import (
    opportunity_score,
    score_breakdown,
    should_execute_now,
)
from dealix.hermes.orchestrator import HermesOrchestrator


def _opp(**overrides: int) -> HermesOpportunity:
    base = {
        "opportunity_type": "customer",
        "title": "test",
        "description": "test",
        "cash_speed_score": 3,
        "strategic_score": 3,
        "difficulty_score": 3,
        "risk_score": 2,
        "repeatability_score": 3,
        "data_moat_score": 3,
        "sovereignty_level": "S1_INTERNAL",
        "recommended_action": "x",
        "recommended_agent": "opportunity_mapper",
    }
    base.update(overrides)
    return HermesOpportunity(**base)


def test_high_cash_opportunity_executes_now() -> None:
    opp = _opp(
        cash_speed_score=5,
        strategic_score=5,
        repeatability_score=5,
        data_moat_score=5,
        difficulty_score=1,
        risk_score=1,
    )
    assert should_execute_now(opp) is True
    assert opportunity_score(opp) > 2.7


def test_low_value_opportunity_does_not_execute_now() -> None:
    opp = _opp(
        cash_speed_score=1,
        strategic_score=1,
        repeatability_score=1,
        data_moat_score=1,
        difficulty_score=5,
        risk_score=5,
    )
    assert should_execute_now(opp) is False


def test_score_breakdown_sums_to_total() -> None:
    opp = _opp()
    parts = score_breakdown(opp)
    pieces = [
        parts["cash_speed"],
        parts["strategic"],
        parts["repeatability"],
        parts["data_moat"],
        parts["difficulty_penalty"],
        parts["risk_penalty"],
    ]
    assert round(sum(pieces), 6) == round(parts["total"], 6)


def test_signal_to_opportunity_maps_type() -> None:
    orchestrator = HermesOrchestrator()
    signal = HermesSignal(
        source="sami",
        signal_type="partner",
        title="Agency intro",
        content="A marketing agency wants to white-label Dealix.",
    )
    opp = orchestrator.signal_to_opportunity(signal)
    assert opp.opportunity_type == "partner"
    assert opp.title.startswith("Opportunity from:")


def test_decision_memo_marks_approval_for_sovereign_levels() -> None:
    orchestrator = HermesOrchestrator()
    opp = _opp(sovereignty_level="S4_SOVEREIGN_ONLY")
    memo = orchestrator.create_decision_memo(opp)
    assert memo.approval_required is True


def test_decision_memo_allows_internal_levels() -> None:
    orchestrator = HermesOrchestrator()
    opp = _opp(sovereignty_level="S1_INTERNAL")
    memo = orchestrator.create_decision_memo(opp)
    assert memo.approval_required is False
