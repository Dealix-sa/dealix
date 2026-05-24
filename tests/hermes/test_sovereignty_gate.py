"""Sovereignty gate enforcement tests."""

from __future__ import annotations

import pytest

from dealix.hermes.sovereignty import (
    Action,
    GateVerdict,
    SovereigntyGate,
    SovereigntyLevel,
)


def _action(**kwargs):
    defaults = dict(
        action_type="draft_proposal",
        payload={},
        proposed_by="proposal_agent",
        sovereignty_level=SovereigntyLevel.S0_AUTONOMOUS,
        risk_level=0.1,
    )
    defaults.update(kwargs)
    return Action(**defaults)


def test_internal_action_allowed():
    gate = SovereigntyGate()
    d = gate.evaluate(_action())
    assert d.verdict is GateVerdict.ALLOW
    assert d.approval_required is False


def test_send_external_message_floor_is_s3():
    gate = SovereigntyGate()
    # Agent claimed S0 — gate must lift it to S3 (sovereign memo).
    d = gate.evaluate(
        _action(
            action_type="send_external_message",
            sovereignty_level=SovereigntyLevel.S0_AUTONOMOUS,
        )
    )
    assert d.verdict is GateVerdict.QUEUE_APPROVAL
    assert d.enforced_level is SovereigntyLevel.S3_SOVEREIGN_MEMO
    assert d.memo_required is True


def test_publish_public_api_is_s4_reserved():
    gate = SovereigntyGate()
    d = gate.evaluate(
        _action(
            action_type="publish_public_api",
            sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        )
    )
    assert d.verdict is GateVerdict.QUEUE_APPROVAL
    assert d.enforced_level is SovereigntyLevel.S4_SOVEREIGN_RESERVED
    assert d.memo_required is True


def test_high_risk_routine_lifts_to_s2():
    gate = SovereigntyGate()
    d = gate.evaluate(_action(risk_level=0.85))
    assert d.verdict is GateVerdict.QUEUE_APPROVAL
    assert d.enforced_level is SovereigntyLevel.S2_SAMI_APPROVAL


def test_invalid_risk_rejected():
    with pytest.raises(ValueError):
        _action(risk_level=1.5)
