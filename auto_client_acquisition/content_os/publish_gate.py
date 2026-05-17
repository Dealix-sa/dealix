"""Single chokepoint that decides whether a social post may be published.

A post is publishable only when it is a ``draft_social_post`` approval
request that the founder has explicitly APPROVED. This is enforced
independently of the live-gate setting and the n8n handoff, so no code
path can publish an un-approved or non-social request.
"""
from __future__ import annotations

from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)


def is_publishable(req: ApprovalRequest) -> bool:
    """True only for an APPROVED ``draft_social_post`` request."""
    return (
        req.action_type == "draft_social_post"
        and ApprovalStatus(req.status) == ApprovalStatus.APPROVED
    )


def assert_publishable(req: ApprovalRequest) -> None:
    """Raise ``ValueError`` unless ``req`` is an approved social post."""
    if req.action_type != "draft_social_post":
        raise ValueError(
            f"approval {req.approval_id} is not a social post "
            f"(action_type={req.action_type!r})"
        )
    if ApprovalStatus(req.status) != ApprovalStatus.APPROVED:
        raise ValueError(
            f"approval {req.approval_id} is {req.status}; only APPROVED "
            "social posts may be published"
        )


__all__ = ["assert_publishable", "is_publishable"]
