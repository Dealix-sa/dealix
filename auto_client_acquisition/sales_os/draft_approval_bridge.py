"""Draft → approval auto-wire (M9).

Before this, agent-produced drafts (outreach messages, follow-up touches)
were returned in memory and never reached the governed queue — a draft
that no one can see or approve is not governed. This bridge is the single
helper every draft producer calls to put a draft into the approval queue.

Nothing here sends. It only creates an :class:`ApprovalRequest`; the
founder (or a founder auto-approve rule) decides. ``create_with_founder_rules``
runs the safety policy + channel gates, so whatsapp / linkedin / phone can
never be silently auto-approved.
"""
from __future__ import annotations

from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    get_default_approval_store,
)


def queue_draft_for_approval(
    *,
    action_type: str,
    object_type: str,
    object_id: str,
    summary_ar: str = "",
    summary_en: str = "",
    channel: str | None = None,
    risk_level: str = "low",
    lead_id: str | None = None,
    proof_impact: str = "",
    content: str = "",
    confidence: float = 1.0,
) -> ApprovalRequest:
    """Put one agent draft into the governed approval queue.

    ``content`` is the draft body — passed to the founder-rule matcher so a
    pre-approved rule may auto-approve low-risk drafts (still recorded).
    Returns the stored :class:`ApprovalRequest` (pending, auto-approved, or
    blocked by policy).
    """
    req = ApprovalRequest.model_validate(
        {
            "object_type": object_type,
            "object_id": object_id,
            "action_type": action_type,
            "action_mode": "approval_required",
            "channel": channel,
            "summary_ar": summary_ar,
            "summary_en": summary_en,
            "risk_level": risk_level,
            "proof_impact": proof_impact,
            "lead_id": lead_id,
        }
    )
    return get_default_approval_store().create_with_founder_rules(
        req, confidence=confidence, content=content
    )


def queue_follow_up_for_approval(
    *,
    task_id: str,
    lead_id: str,
    attempt: int,
    channel: str,
    draft_ar: str = "",
    draft_en: str = "",
) -> ApprovalRequest:
    """Convenience wrapper for the sequencing engine: queue one follow-up
    touch. The caller then records ``approval_id`` on the follow_up_task."""
    return queue_draft_for_approval(
        action_type="follow_up_task",
        object_type="follow_up_task",
        object_id=task_id,
        summary_ar=draft_ar or f"متابعة #{attempt} عبر {channel}",
        summary_en=draft_en or f"Follow-up #{attempt} via {channel}",
        channel=channel,
        lead_id=lead_id,
        proof_impact=f"leadops: follow-up touch {attempt} for {lead_id}",
        content=draft_en or draft_ar,
    )


__all__ = ["queue_draft_for_approval", "queue_follow_up_for_approval"]
