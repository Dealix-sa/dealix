"""Adapter from Commercial Universe actions to the existing Approval Command Center."""

from __future__ import annotations

from auto_client_acquisition.approval_center.schemas import ApprovalRequest

from .contracts import ActionEnvelope, ActionMode, Channel


_ACTION_TYPE_MAP = {
    "partner_intro": "partner_intro",
    "draft_email": "draft_email",
    "call_script": "call_script",
    "meeting_booking": "follow_up_task",
    "calendar_booking": "follow_up_task",
    "support_reply": "support_reply_draft",
    "payment_follow_up": "payment_reminder",
    "delivery_task": "delivery_task",
    "proof_request": "proof_request",
    "expansion_review": "upsell_recommendation",
}


def to_approval_request(envelope: ActionEnvelope) -> ApprovalRequest:
    """Build an ApprovalRequest without writing to the approval store.

    Internal and blocked actions are not approval requests. Callers must keep them
    in their internal action queue or policy log instead.
    """

    if envelope.action_mode is not ActionMode.APPROVAL_REQUIRED:
        raise ValueError("only approval-required actions can enter the Approval Command Center")
    if envelope.channel is Channel.INTERNAL:
        raise ValueError("internal actions do not belong in the external approval center")
    if envelope.external_action_allowed:
        raise ValueError("approval adapter refuses pre-authorized external execution")

    action_type = _ACTION_TYPE_MAP.get(envelope.action_type, "draft_email")
    return ApprovalRequest(
        object_type="commercial_relationship",
        object_id=envelope.relationship_id,
        action_type=action_type,
        action_mode="approval_required",
        channel=envelope.channel.value,
        summary_ar=envelope.summary_ar,
        summary_en=envelope.rationale,
        risk_level=envelope.risk_level.value,
        proof_impact=envelope.proof_target,
        action_id=envelope.action_id,
        customer_id=envelope.tenant_id,
        audit_ref=(envelope.evidence_refs[0] if envelope.evidence_refs else None),
        proof_target=envelope.proof_target,
    )
