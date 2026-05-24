"""Sovereignty hard-rule tests — these must never regress."""

from __future__ import annotations

import pytest

from dealix.hermes.core.schemas import RiskLevel, SovereigntyLevel
from dealix.hermes.sovereignty import (
    S4_SOVEREIGN_ACTIONS,
    S5_NEVER_AUTONOMOUS_ACTIONS,
    SovereignLayer,
    classify_action,
)
from dealix.hermes.trust.approvals import ApprovalCenter
from dealix.hermes.trust.audit import AuditLog


@pytest.fixture(autouse=True)
def _isolate_state(monkeypatch):
    """Replace global singletons with fresh instances for every test."""
    import dealix.hermes.sovereignty as sov_mod
    import dealix.hermes.trust.approvals as appr_mod
    import dealix.hermes.trust.audit as aud_mod

    sov_mod._default_layer = SovereignLayer()
    appr_mod._default_center = ApprovalCenter()
    aud_mod._default_log = AuditLog()
    yield
    sov_mod._default_layer = None
    appr_mod._default_center = None
    aud_mod._default_log = None


def test_sovereignty_classifies_s5_never_autonomous():
    for action in S5_NEVER_AUTONOMOUS_ACTIONS:
        assert classify_action(action) == SovereigntyLevel.S5_NEVER_AUTONOMOUS


def test_sovereignty_classifies_s4_sovereign_only():
    for action in S4_SOVEREIGN_ACTIONS:
        assert classify_action(action) == SovereigntyLevel.S4_SOVEREIGN_ONLY


def test_sovereignty_blocks_s4_actions():
    from dealix.hermes.sovereignty import get_sovereign_layer

    verdict = get_sovereign_layer().evaluate(
        action_type="launch_marketplace",
        agent_id="revenue_hunter",
        risk_level=RiskLevel.HIGH,
    )
    assert verdict.allowed is False
    assert verdict.requires_approval is True
    assert verdict.sovereignty_level == SovereigntyLevel.S4_SOVEREIGN_ONLY
    assert verdict.approval_id is not None


def test_never_autonomous_actions_blocked():
    from dealix.hermes.sovereignty import get_sovereign_layer

    verdict = get_sovereign_layer().evaluate(
        action_type="money_transfer",
        agent_id="revenue_hunter",
        risk_level=RiskLevel.CRITICAL,
    )
    assert verdict.allowed is False
    assert verdict.requires_approval is False
    assert verdict.reason == "s5_never_autonomous"


def test_kill_switch_blocks_all_actions():
    from dealix.hermes.sovereignty import get_sovereign_layer

    layer = get_sovereign_layer()
    layer.engage_kill_switch("test")
    verdict = layer.evaluate(action_type="draft_outreach", agent_id="revenue_hunter")
    assert verdict.allowed is False
    assert verdict.reason == "kill_switch_engaged"
    layer.disengage_kill_switch("test")


def test_s2_requires_approval_and_routes_to_center():
    from dealix.hermes.sovereignty import get_sovereign_layer
    from dealix.hermes.trust.approvals import get_approval_center

    verdict = get_sovereign_layer().evaluate(
        action_type="send_external_email",
        agent_id="revenue_hunter",
    )
    assert verdict.requires_approval is True
    assert verdict.sovereignty_level == SovereigntyLevel.S2_SAMI_APPROVAL
    assert get_approval_center().get(verdict.approval_id) is not None
