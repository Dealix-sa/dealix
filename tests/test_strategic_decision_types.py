"""Tests for the strategic decision taxonomy."""

from __future__ import annotations

from auto_client_acquisition.intelligence_compounding_os import CompoundingDecision
from auto_client_acquisition.strategy_autonomy.decision_types import (
    IRREVERSIBLE,
    StrategicDecisionType,
    from_compounding,
    is_irreversible,
)


def test_decision_type_values() -> None:
    values = {d.value for d in StrategicDecisionType}
    assert values == {
        "scale",
        "build",
        "kill",
        "hold",
        "raise_price",
        "offer_retainer",
        "hire",
        "create_business_unit",
        "create_venture_candidate",
    }


def test_irreversible_set() -> None:
    assert IRREVERSIBLE == frozenset(
        {
            StrategicDecisionType.KILL,
            StrategicDecisionType.HIRE,
            StrategicDecisionType.RAISE_PRICE,
            StrategicDecisionType.CREATE_BUSINESS_UNIT,
            StrategicDecisionType.CREATE_VENTURE_CANDIDATE,
        }
    )


def test_is_irreversible() -> None:
    assert is_irreversible(StrategicDecisionType.KILL) is True
    assert is_irreversible("hire") is True
    assert is_irreversible(StrategicDecisionType.SCALE) is False
    assert is_irreversible("hold") is False
    assert is_irreversible("not_a_decision") is False


def test_from_compounding() -> None:
    assert from_compounding(CompoundingDecision.SCALE) == StrategicDecisionType.SCALE
    assert from_compounding(CompoundingDecision.KILL) == StrategicDecisionType.KILL
    assert (
        from_compounding(CompoundingDecision.CREATE_BUSINESS_UNIT)
        == StrategicDecisionType.CREATE_BUSINESS_UNIT
    )
    # PILOT collapses to the safe HOLD decision.
    assert from_compounding(CompoundingDecision.PILOT) == StrategicDecisionType.HOLD
    # Unknown / missing inputs collapse to HOLD.
    assert from_compounding(None) == StrategicDecisionType.HOLD
    assert from_compounding("garbage") == StrategicDecisionType.HOLD
