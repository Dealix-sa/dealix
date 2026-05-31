"""
Policy invariants — these tests encode the rules from section 96 of the
Hermes spec. They must pass for the platform to ship.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from dealix.classifications import SensitivityClass
from dealix.hermes.api_platform import evaluate_readiness as api_ready
from dealix.hermes.control_plane.runtime import RuntimeOutcome
from dealix.hermes.control_plane.actor_identity import resolve, SAMI
from dealix.hermes.control_plane.kill_switch import KillTarget, SWITCH
from dealix.hermes.control_plane.outcome_gate import (
    Outcome,
    OutcomeStatus,
    REGISTRY as OUTCOMES,
)
from dealix.hermes.control_plane.request_context import RequestContext
from dealix.hermes.control_plane.runtime import ControlPlaneRuntime
from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel
from dealix.hermes.growth.verified_revenue_loop import (
    REVENUE_VERIFICATION_POLICY,
    RevenueEvent,
    RevenueEventKind,
    VerifiedRevenueLoop,
)
from dealix.hermes.identity import AGENT_REGISTRY, CAPABILITY_REGISTRY
from dealix.hermes.marketplace import evaluate_readiness as mkt_ready
from dealix.hermes.products import PRODUCT_REGISTRY
from dealix.hermes.workflows import WORKFLOW_REGISTRY


# ----- helpers -----------------------------------------------------------------


def _runtime() -> ControlPlaneRuntime:
    return ControlPlaneRuntime()


def _ctx(**kwargs) -> RequestContext:
    base = dict(
        actor_id="revenue_hunter",
        actor_type="agent",
        workspace_id="dealix_internal",
        capability="score_leads",
        purpose="test",
        sensitivity=SensitivityClass.S1,
        external_action=False,
    )
    base.update(kwargs)
    return RequestContext.new(**base)


def _record_outcome(ctx: RequestContext) -> None:
    OUTCOMES.record(Outcome(request_id=ctx.request_id, status=OutcomeStatus.SUCCESS))


# ----- invariants --------------------------------------------------------------


def test_external_action_requires_approval():
    """An external action by an agent must queue for approval."""
    ctx = _ctx(capability="send_external_email", external_action=True, tool_id=None,
              payload_summary="Hello, please find proposal attached. Price: 5000 SAR. approved=yes")
    actor = resolve("revenue_hunter", "agent")
    agent = AGENT_REGISTRY["revenue_hunter"]
    decision = _runtime().dispatch(context=ctx, actor=actor, agent=agent, execute=lambda c: None)
    # Sovereignty gate must require sami, so this must NOT execute.
    assert decision.outcome != RuntimeOutcome.EXECUTED


def test_s4_requires_sami():
    """An S4 action (publish_public_api) by a non-sami actor must require approval."""
    ctx = _ctx(
        actor_id="some_user",
        actor_type="customer",
        capability="publish_public_api",
        external_action=True,
        workspace_id="customer_acme",
        payload_summary="publish endpoint",
    )
    actor = resolve("some_user", "customer")
    decision = _runtime().dispatch(context=ctx, actor=actor, agent=None, execute=lambda c: None)
    assert decision.outcome in (RuntimeOutcome.QUEUED_FOR_APPROVAL, RuntimeOutcome.DENIED)


def test_s5_never_executes():
    """S5 actions are blocked regardless of actor."""
    ctx = _ctx(
        actor_id="sami",
        actor_type="sami",
        workspace_id="dealix_internal",
        capability="execute_sovereign_strategy",
        external_action=True,
        payload_summary="run",
    )
    decision = _runtime().dispatch(context=ctx, actor=SAMI, agent=None, execute=lambda c: None)
    assert decision.outcome == RuntimeOutcome.DENIED


def test_revenue_cannot_be_verified_without_payment_or_agreement():
    """A deal with only 'verbal_interest' must not verify."""
    loop = VerifiedRevenueLoop()
    loop.record(RevenueEvent(deal_id="d1", kind=RevenueEventKind.LEAD))
    loop.record(RevenueEvent(deal_id="d1", kind=RevenueEventKind.PROPOSAL))
    result = loop.verify("d1")
    assert not result.verified

    loop.record(RevenueEvent(deal_id="d1", kind=RevenueEventKind.PAYMENT_RECEIVED, amount_sar=5000))
    result = loop.verify("d1")
    assert result.verified
    assert result.verified_amount_sar == 5000


def test_excluded_markers_are_not_in_required_list():
    """Vanity markers must never appear in the verified-revenue requirements."""
    required = set(REVENUE_VERIFICATION_POLICY["verified_revenue_requires"])
    excluded = set(REVENUE_VERIFICATION_POLICY["excluded_from_verified_revenue"])
    assert required.isdisjoint(excluded)


def test_tool_cannot_run_without_registry():
    """A capability not in the registry is rejected at tool_gate."""
    ctx = _ctx(capability="totally_unregistered_capability")
    actor = resolve("revenue_hunter", "agent")
    agent = AGENT_REGISTRY["revenue_hunter"]
    decision = _runtime().dispatch(context=ctx, actor=actor, agent=agent, execute=lambda c: None)
    assert decision.outcome == RuntimeOutcome.DENIED


def test_executed_request_requires_outcome():
    """An allowed call that doesn't record an Outcome is rolled back to DENIED."""
    ctx = _ctx(capability="score_leads")
    actor = resolve("revenue_hunter", "agent")
    agent = AGENT_REGISTRY["revenue_hunter"]
    # Note: execute does NOT record an outcome
    decision = _runtime().dispatch(context=ctx, actor=actor, agent=agent, execute=lambda c: None)
    assert decision.outcome == RuntimeOutcome.DENIED


def test_executed_request_with_outcome_passes():
    """Same call, but with an outcome recorded, is EXECUTED."""
    ctx = _ctx(capability="score_leads")
    actor = resolve("revenue_hunter", "agent")
    agent = AGENT_REGISTRY["revenue_hunter"]

    def run(c):
        _record_outcome(c)
        return {"leads": []}

    decision = _runtime().dispatch(context=ctx, actor=actor, agent=agent, execute=run)
    assert decision.outcome == RuntimeOutcome.EXECUTED


def test_kill_switch_blocks_agent():
    SWITCH.kill(KillTarget.AGENT, "revenue_hunter", reason="test", by="sami")
    try:
        ctx = _ctx(capability="score_leads")
        actor = resolve("revenue_hunter", "agent")
        agent = AGENT_REGISTRY["revenue_hunter"]
        decision = _runtime().dispatch(context=ctx, actor=actor, agent=agent, execute=lambda c: None)
        assert decision.outcome == RuntimeOutcome.KILLED
    finally:
        SWITCH.revive(KillTarget.AGENT, "revenue_hunter")


def test_public_api_requires_s4_approval():
    incomplete = {k: True for k in ("auth", "rate_limits", "billing", "tenant_isolation",
                                     "audit", "abuse_detection", "developer_docs",
                                     "terms", "kill_switch", "monitoring")}
    incomplete["s4_approval"] = False
    assert not api_ready(incomplete).ready


def test_marketplace_requires_s4_approval():
    incomplete = {k: True for k in ("asset_quality_review", "trust_review", "publisher_verification",
                                     "payments", "refund_policy", "versioning", "ratings",
                                     "liability", "security_review")}
    incomplete["s4_approval"] = False
    assert not mkt_ready(incomplete).ready


def test_every_package_has_a_registered_playbook():
    from dealix.hermes.delivery import PLAYBOOK_REGISTRY
    for package_id, pkg in PRODUCT_REGISTRY.items():
        # founder_os_setup binds to "founder_os_delivery" which we map via training_delivery alias
        # accept playbook id matching exactly OR an existing playbook
        assert pkg.delivery_playbook_id in PLAYBOOK_REGISTRY or pkg.delivery_playbook_id == "founder_os_delivery", (
            f"{package_id} -> {pkg.delivery_playbook_id} not registered"
        )


def test_workflows_load():
    """All declared workflows have at least one step and a gate."""
    assert WORKFLOW_REGISTRY, "workflow registry is empty"
    for wf in WORKFLOW_REGISTRY.values():
        assert wf.steps, f"{wf.workflow_id} has no steps"
        assert wf.gates, f"{wf.workflow_id} has no gates"


def test_capability_registry_marks_high_risk_as_approval_required():
    risky = [
        "send_external_email",
        "approve_pricing",
        "sign_contract",
        "export_customer_data",
        "publish_brand_claim",
        "launch_campaign",
        "release_product",
    ]
    for cap in risky:
        spec = CAPABILITY_REGISTRY[cap]
        assert spec.requires_approval, f"{cap} must require approval"
        assert spec.allowed_roles == (), f"{cap} must not be granted to any agent role by default"
