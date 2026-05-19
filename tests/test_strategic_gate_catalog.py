"""Tests for the codified strategic gate catalog."""

from __future__ import annotations

from auto_client_acquisition.strategy_autonomy.decision_types import (
    StrategicDecisionType,
)
from auto_client_acquisition.strategy_autonomy.gate_catalog import (
    STRATEGIC_GATE_CATALOG,
    GateRule,
    get_gate,
    list_gates,
)

_VALID_TYPES = {d.value for d in StrategicDecisionType}
_VALID_COMPARATORS = {"gte", "lte", "eq"}


def test_catalog_not_empty() -> None:
    assert len(STRATEGIC_GATE_CATALOG) >= 6


def test_every_gate_is_well_formed() -> None:
    seen_ids: set[str] = set()
    for gate in STRATEGIC_GATE_CATALOG:
        assert isinstance(gate, GateRule)
        assert gate.gate_id not in seen_ids, "duplicate gate_id"
        seen_ids.add(gate.gate_id)
        assert gate.comparator in _VALID_COMPARATORS
        assert gate.on_pass in _VALID_TYPES
        assert gate.on_fail in _VALID_TYPES
        assert gate.window_day is None or gate.window_day in (7, 30, 60, 90)
        assert gate.title_ar and gate.title_en
        assert gate.source


def test_codifies_day90_build_gate() -> None:
    gate = get_gate("g_revenue_day90_build")
    assert gate is not None
    assert gate.window_day == 90
    assert gate.threshold == 40000.0
    assert gate.on_pass == StrategicDecisionType.BUILD.value


def test_codifies_day60_hold_gate() -> None:
    gate = get_gate("g_revenue_day60_hold")
    assert gate is not None
    assert gate.window_day == 60
    assert gate.threshold == 25000.0
    assert gate.on_fail == StrategicDecisionType.HOLD.value


def test_codifies_founder_hire_gate() -> None:
    gate = get_gate("g_founder_hours_hire")
    assert gate is not None
    assert gate.on_fail == StrategicDecisionType.HIRE.value
    assert gate.comparator == "lte"
    assert gate.threshold == 5.0


def test_get_gate_missing() -> None:
    assert get_gate("g_does_not_exist") is None


def test_list_gates() -> None:
    assert list_gates() == STRATEGIC_GATE_CATALOG


def test_gate_to_dict() -> None:
    gate = STRATEGIC_GATE_CATALOG[0]
    data = gate.to_dict()
    assert data["gate_id"] == gate.gate_id
    assert "comparator" in data
