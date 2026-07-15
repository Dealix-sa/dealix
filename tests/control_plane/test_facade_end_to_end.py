"""ControlPlane facade — Level Max end-to-end (sections 79–80)."""

from __future__ import annotations

import pytest

from dealix.control_plane import (
    AllowedUse,
    ApprovalDecision,
    ControlPlane,
    DataClass,
    Identity,
    IdentityKind,
    MemoryKind,
    SecurityMode,
    SovereigntyLevel,
    build_default_control_plane,
)


def test_default_control_plane_initialises_sami_and_workspaces() -> None:
    cp = build_default_control_plane()
    sami = cp.sami()
    assert sami.kind is IdentityKind.SAMI
    assert cp.security_mode_manager.mode is SecurityMode.DRAFT_ONLY
    assert any(
        w.workspace_id == cp.sovereign_workspace_id for w in cp.tenants.workspaces_for(cp.sovereign_tenant_id)
    )


def test_external_action_blocked_in_draft_only_mode() -> None:
    cp = build_default_control_plane()
    with pytest.raises(PermissionError):
        cp.assert_can_send_external(data_class=DataClass.CONFIDENTIAL)


def test_approval_only_sami_can_approve_external_action() -> None:
    cp = build_default_control_plane()
    cp.identities.register(
        Identity(
            identity_id="agent_proposal",
            kind=IdentityKind.AGENT,
            display_name="Proposal Factory",
        )
    )
    requester = cp.identities.get("agent_proposal")
    card = cp.request_external_action(
        requester=requester,
        action_type="send_proposal",
        risk_level="medium",
        summary="Send proposal to Acme",
    )
    with pytest.raises(PermissionError):
        cp.approvals.approve(approval_id=card.approval_id, actor=requester)
    cp.approvals.approve(approval_id=card.approval_id, actor=cp.sami())
    assert cp.approvals.get(card.approval_id).decision is ApprovalDecision.APPROVED


def test_context_packet_enforces_allowed_use_and_ttl() -> None:
    cp = build_default_control_plane()
    packet = cp.issue_context(
        agent_id="proposal_factory",
        purpose="draft_proposal",
        workspace_id="ws_internal_dealix",
        sensitivity=DataClass.CONFIDENTIAL,
        allowed_use=[AllowedUse.DRAFT_ONLY],
        seed={"opportunity_id": "opp_1"},
    )
    packet.assert_use(AllowedUse.DRAFT_ONLY)
    with pytest.raises(PermissionError):
        packet.assert_use(AllowedUse.EXTERNAL_SEND)


def test_memory_kinds_keep_sensitivity_defaults() -> None:
    cp = build_default_control_plane()
    personal = cp.memory.remember(
        kind=MemoryKind.PERSONAL,
        workspace_id=cp.sovereign_workspace_id,
        title="founder voice",
        body="Direct, sovereign tone",
    )
    customer = cp.memory.remember(
        kind=MemoryKind.CUSTOMER,
        workspace_id="ws_customer_acme",
        title="Acme onboarding",
        body="prefers Arabic",
    )
    assert personal.sensitivity is DataClass.SOVEREIGN
    assert customer.sensitivity is DataClass.CONFIDENTIAL


def test_snapshot_returns_all_layers() -> None:
    cp = build_default_control_plane()
    snap = cp.snapshot()
    for key in (
        "sovereignty_order",
        "security_mode",
        "identities",
        "tenants",
        "money",
        "intelligence_graph",
        "scale_kill",
        "public_api",
        "marketplace",
        "health",
        "commercial_packaging",
        "memory_stats",
        "open_incidents",
        "pending_approvals",
    ):
        assert key in snap


def test_kill_switch_engages_lockdown_and_disables_tools() -> None:
    cp = build_default_control_plane()
    cp.kill_switch()
    assert cp.security_mode_manager.mode is SecurityMode.SOVEREIGN_LOCKDOWN
    assert cp.mcp_gateway.kill_switch_engaged is True


def test_refresh_health_flags_picks_up_pending_external_action() -> None:
    cp = build_default_control_plane()
    cp.identities.register(
        Identity(
            identity_id="agent_y", kind=IdentityKind.AGENT, display_name="Agent Y"
        )
    )
    cp.request_external_action(
        requester=cp.identities.get("agent_y"),
        action_type="send_proposal",
        risk_level="medium",
        summary="proposal to BetaCo",
    )
    flags = cp.refresh_health_flags()
    flag_values = {f.value for f in flags}
    assert "external_actions_without_approval" in flag_values
