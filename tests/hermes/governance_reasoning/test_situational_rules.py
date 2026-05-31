"""Situational risk doctrine: sensitivity>=3 must escalate."""

from __future__ import annotations

from dealix.hermes.governance_reasoning.situational_rules import must_escalate, score


def test_high_sensitivity_forces_escalation() -> None:
    assert must_escalate({"sensitivity": 3, "magnitude": 1, "irreversibility": 1}) is True
    assert must_escalate({"sensitivity": 2, "magnitude": 1, "irreversibility": 1}) is False
    s = score({"sensitivity": 5, "magnitude": 4, "irreversibility": 4})
    assert s.escalate is True
    assert s.risk_score == 13
