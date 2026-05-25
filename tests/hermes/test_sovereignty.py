"""Doctrine tests for sovereignty levels and the classifier."""

from __future__ import annotations

from dealix.hermes.sovereignty.classifier import ActionContext, classify_action
from dealix.hermes.sovereignty.levels import (
    SovereigntyLevel,
    is_autonomous,
    is_never_autonomous,
    requires_human,
    requires_memo,
)


def test_money_transfer_is_never_autonomous():
    """No 14: لا Sovereign Decision بلا سامي."""
    ctx = ActionContext(action_type="transfer_money", moves_money=True)
    assert classify_action(ctx) == SovereigntyLevel.S5_NEVER_AUTONOMOUS
    assert is_never_autonomous(SovereigntyLevel.S5_NEVER_AUTONOMOUS)


def test_contract_sign_is_never_autonomous():
    ctx = ActionContext(action_type="sign_contract", binds_contract=True)
    assert classify_action(ctx) == SovereigntyLevel.S5_NEVER_AUTONOMOUS


def test_marketplace_publish_is_sovereign_only():
    ctx = ActionContext(action_type="launch_marketplace", affects_marketplace=True)
    assert classify_action(ctx) == SovereigntyLevel.S4_SOVEREIGN_ONLY


def test_pricing_change_requires_memo():
    ctx = ActionContext(action_type="approve_enterprise_pricing", affects_pricing=True)
    level = classify_action(ctx)
    assert level == SovereigntyLevel.S3_SOVEREIGN_MEMO
    assert requires_memo(level)


def test_external_message_requires_sami_approval():
    ctx = ActionContext(action_type="send_external_message", external=True, customer_visible=True)
    level = classify_action(ctx)
    assert level == SovereigntyLevel.S2_SAMI_APPROVAL
    assert requires_human(level)


def test_internal_action_is_autonomous():
    ctx = ActionContext(action_type="draft_proposal", workspace_id="dealix_internal")
    level = classify_action(ctx)
    assert level == SovereigntyLevel.S1_INTERNAL
    assert is_autonomous(level)


def test_blocks_s4_actions(orch):
    """Doctrine: S4+ actions require human approval before dispatch."""
    from dealix.hermes.kernel.schemas import (
        AssetType,
        OpportunityType,
        OutcomeStatus,
        SignalSource,
        SignalType,
    )
    from dealix.hermes.kernel.signals import capture_signal

    sig = capture_signal(
        store=orch.kernel.signals,
        source=SignalSource.system,
        signal_type=SignalType.api,
        title="Publish public API",
        content="Plan to publish public API surface",
    )
    opp = orch.kernel.opportunities.create_from_signal(
        sig,
        opportunity_type=OpportunityType.api,
        title="Publish API v1",
        sovereignty_level=SovereigntyLevel.S4_SOVEREIGN_ONLY,
    )
    decision = orch.kernel.decisions.create_memo(opp, memo="Publish API v1")
    assert decision.requires_approval is True

    execution = orch.kernel.executions.plan(decision, agent_id="execution_planner", tools=[])
    # Cannot dispatch without approval.
    orch.kernel.executions.mark_trust_check(execution.execution_id, passed=True)
    import pytest

    with pytest.raises(PermissionError):
        orch.kernel.executions.dispatch(execution.execution_id)


def test_kill_switch_is_idempotent(orch):
    from dealix.hermes.sovereignty.kill_switch import KillTarget

    orch.kill_switch.kill(KillTarget.agent, "rogue", reason="experiment")
    orch.kill_switch.kill(KillTarget.agent, "rogue", reason="experiment again")
    assert orch.kill_switch.is_killed(KillTarget.agent, "rogue")
    orch.kill_switch.restore(KillTarget.agent, "rogue")
    assert not orch.kill_switch.is_killed(KillTarget.agent, "rogue")
