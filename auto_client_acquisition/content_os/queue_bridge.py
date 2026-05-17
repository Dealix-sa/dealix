"""Bridge social post drafts into the Approval Command Center.

Each ``SocialPostDraft`` becomes an ``ApprovalRequest`` with
``action_type="draft_social_post"``, ``action_mode="draft_only"`` and
``channel="social"`` — deliberately NOT ``"linkedin"``, so the LinkedIn
outreach channel hard-blocks stay reserved for actual outreach messages.
Nothing is sent here; the founder still approves each post in the queue.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    get_default_approval_store,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.content_os.drafting import SocialPostDraft

_SOCIAL_DRAFT_TTL = timedelta(days=3)


def _to_request(draft: SocialPostDraft) -> ApprovalRequest:
    return ApprovalRequest(
        object_type="social_post",
        object_id=f"{draft.platform}:{draft.theme}",
        action_type="draft_social_post",
        action_mode="draft_only",
        channel="social",
        summary_ar=f"بوست {draft.platform} — {draft.theme}\n\n{draft.body_ar}",
        summary_en=f"{draft.platform} post — {draft.theme}\n\n{draft.body_en}",
        risk_level="low",
        proof_impact=draft.proof_impact,
        expires_at=datetime.now(UTC) + _SOCIAL_DRAFT_TTL,
    )


def enqueue_social_drafts(
    drafts: list[SocialPostDraft],
    store: ApprovalStore | None = None,
) -> list[ApprovalRequest]:
    """Create one approval request per draft. Returns the created requests."""
    target = store or get_default_approval_store()
    created: list[ApprovalRequest] = []
    for draft in drafts:
        created.append(target.create(_to_request(draft)))
    return created


__all__ = ["enqueue_social_drafts"]
