"""Policy Engine + Approval Center + Audit & Evidence (sections 58, 59, 60)."""

from __future__ import annotations

import pytest

from dealix.control_plane.approval_center import (
    ApprovalCenter,
    ApprovalDecision,
    SovereigntyLevel,
)
from dealix.control_plane.audit_evidence import AuditLog, EvidenceTrigger
from dealix.control_plane.identity_access import (
    Identity,
    IdentityKind,
    IdentityRegistry,
    Permission,
)
from dealix.control_plane.policy_engine import (
    PolicyDecision,
    PolicyEngine,
    standard_policies,
)


def _sami_registry() -> IdentityRegistry:
    registry = IdentityRegistry()
    registry.register(
        Identity(identity_id="sami", kind=IdentityKind.SAMI, display_name="Sami")
    )
    registry.register(
        Identity(identity_id="agent_x", kind=IdentityKind.AGENT, display_name="Agent X")
    )
    return registry


def test_external_action_policy_escalates() -> None:
    engine = PolicyEngine()
    for policy in standard_policies():
        engine.register(policy)
    result = engine.evaluate({"external_action": True})
    assert result.decision is PolicyDecision.ESCALATE
    assert result.requires_approval_role == "sami"


def test_sovereign_data_export_is_denied() -> None:
    engine = PolicyEngine()
    for policy in standard_policies():
        engine.register(policy)
    result = engine.evaluate({"data_class": "SOVEREIGN", "export": True})
    assert result.decision is PolicyDecision.DENY


def test_pricing_floor_policy_denies_below_floor() -> None:
    engine = PolicyEngine()
    for policy in standard_policies():
        engine.register(policy)
    result = engine.evaluate(
        {"action_type": "set_price", "offer_floor_sar": 5000.0, "price_sar": 1000.0}
    )
    assert result.decision is PolicyDecision.DENY


def test_approval_center_routes_to_sami_only() -> None:
    registry = _sami_registry()
    centre = ApprovalCenter()
    card = centre.request(
        requested_by="agent_x",
        action_type="external_proposal",
        sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        risk_level="medium",
        summary="Outbound to Acme",
    )
    assert card.decision is ApprovalDecision.PENDING

    agent = registry.get("agent_x")
    with pytest.raises(PermissionError):
        centre.approve(approval_id=card.approval_id, actor=agent)

    sami = registry.get("sami")
    centre.approve(approval_id=card.approval_id, actor=sami)
    assert centre.get(card.approval_id).decision is ApprovalDecision.APPROVED


def test_audit_log_emits_event_and_pack() -> None:
    audit = AuditLog()
    event = audit.record(
        actor_type="agent",
        actor_id="agent_x",
        action_type="draft_proposal",
        sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        result="approval_requested",
    )
    pack = audit.open_pack(
        trigger=EvidenceTrigger.ENTERPRISE_PROPOSAL,
        decision={"action": "send_proposal"},
        context={"customer": "Acme"},
        recommended_action="approve",
    )
    assert event in audit.events(actor_id="agent_x")
    assert audit.get_pack(pack.pack_id).pack_id == pack.pack_id
