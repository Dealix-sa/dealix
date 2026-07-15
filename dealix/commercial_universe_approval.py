"""Adapter from the Commercial Universe Wave A contract to the canonical approval queue.

The Company OS already has one approval schema. This adapter intentionally
reuses it instead of creating a second queue, sender, scheduler, or CRM write
path. It produces a reviewable request only; it never authorizes an external
action.
"""

from __future__ import annotations

from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus as QueueApprovalStatus,
    is_canonical_action_type,
)

from dealix.commercial_universe import (
    ApprovalEnvelope,
    ApprovalStatus,
    CommercialAccount,
    RelationshipType,
)


def _canonical_action(account: CommercialAccount, envelope: ApprovalEnvelope) -> str:
    """Map a product action label to one of the existing queue action types."""
    requested = envelope.action.strip()
    if is_canonical_action_type(requested):
        return requested

    if account.relationship in {
        RelationshipType.STRATEGIC_PARTNER,
        RelationshipType.REFERRAL_PARTNER,
        RelationshipType.CHANNEL_DISTRIBUTOR,
        RelationshipType.IMPLEMENTATION_PARTNER,
        RelationshipType.TECHNOLOGY_PARTNER,
        RelationshipType.CO_MARKETING_PARTNER,
    }:
        return "partner_intro"

    if envelope.channel in {"linkedin", "linkedin_manual"}:
        return "draft_linkedin_manual"
    if envelope.channel in {"email", "email_draft"}:
        return "draft_email"
    return "follow_up_task"


def _risk_level(account: CommercialAccount) -> str:
    if account.relationship in {
        RelationshipType.GOVERNMENT_STAKEHOLDER,
        RelationshipType.INVESTOR,
    }:
        return "high"
    if account.relationship in {
        RelationshipType.STRATEGIC_PARTNER,
        RelationshipType.CHANNEL_DISTRIBUTOR,
        RelationshipType.IMPLEMENTATION_PARTNER,
        RelationshipType.TECHNOLOGY_PARTNER,
    }:
        return "medium"
    return "low"


def to_approval_request(
    account: CommercialAccount,
    envelope: ApprovalEnvelope,
    *,
    approval_id: str | None = None,
    action_id: str | None = None,
) -> ApprovalRequest:
    """Create the canonical queue record for founder review.

    A blocked envelope is terminal for research-only or unknown permission.
    A permitted account is still pending and requires human approval before
    any external execution.
    """
    if account.tenant_id != envelope.tenant_id or account.account_id != envelope.account_id:
        raise ValueError("account and envelope must share tenant and account scope")

    blocked = envelope.status is ApprovalStatus.BLOCKED
    status = QueueApprovalStatus.BLOCKED if blocked else QueueApprovalStatus.PENDING
    mode = "blocked" if blocked else "approval_required"
    action_type = _canonical_action(account, envelope)

    return ApprovalRequest(
        approval_id=approval_id or f"apr_cu_{account.account_id}",
        action_id=action_id or f"act_cu_{account.account_id}",
        object_type="commercial_account",
        object_id=account.account_id,
        action_type=action_type,
        action_mode=mode,
        channel=envelope.channel,
        summary_ar=(
            f"مراجعة تجارية: {account.company_name} — "
            f"{account.department.value} — {account.relationship.value}"
        ),
        summary_en=(
            f"Commercial review: {account.company_name} — "
            f"{account.department.value} — {account.relationship.value}"
        ),
        risk_level=_risk_level(account),
        proof_impact=f"Expected proof: {envelope.proof_target}",
        status=status,
        customer_id=account.tenant_id,
        audit_ref=f"commercial-universe:{account.tenant_id}:{account.source_ref}",
        proof_target=envelope.proof_target,
    )


__all__ = ["to_approval_request"]
