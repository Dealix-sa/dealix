"""Execution hook for approved Approval Command Center items.

When the founder approves (or bulk-approves) an item, this hook decides
whether the approval may trigger an automated send.

Doctrine — the immutable rule:
  - ONLY ``action_type='draft_email'`` AND ``channel='email'`` items may
    enqueue a ``run_outreach_batch`` worker job. That job sends via the
    existing email path which already enforces ``email/compliance.py``
    (opt-out, suppression, daily limit).
  - Items on blocked channels (whatsapp / linkedin / phone) can be
    approved as drafts but are NEVER auto-executed. They are returned in
    ``blocked_from_execution`` for audit and silently skipped.
  - Any non-approved status is skipped.

This module never sends email itself — it only enqueues a job (or returns
a dry-run plan when no Redis pool is supplied).
"""

from __future__ import annotations

import logging
from typing import Any

from auto_client_acquisition.approval_center.founder_rules import (
    _BLOCKED_AUTO_CHANNELS,
)
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)

log = logging.getLogger(__name__)

# The single action_type + channel pair that may auto-execute on approval.
_EXECUTABLE_ACTION_TYPE = "draft_email"
_EXECUTABLE_CHANNEL = "email"


def is_auto_executable(req: ApprovalRequest) -> bool:
    """Is this approved request allowed to trigger an automated send?

    True only for an approved ``draft_email`` on the ``email`` channel.
    Blocked channels (whatsapp/linkedin/phone) always return False even
    when approved — they remain draft+approve only.
    """
    if ApprovalStatus(req.status) != ApprovalStatus.APPROVED:
        return False
    channel = (req.channel or "").lower()
    if channel in _BLOCKED_AUTO_CHANNELS:
        return False
    return req.action_type == _EXECUTABLE_ACTION_TYPE and channel == _EXECUTABLE_CHANNEL


async def dispatch_approved(
    requests: list[ApprovalRequest],
    *,
    redis_pool: Any | None = None,
    tenant_id: str = "default",
) -> dict[str, Any]:
    """Route a set of just-approved requests to the execution path.

    For each ``draft_email`` + ``email`` request, enqueue one
    ``run_outreach_batch`` job (keyed on the approval's ``object_id`` as the
    batch id). Blocked-channel approvals are recorded in
    ``blocked_from_execution`` and never enqueued.

    Returns a summary dict. When ``redis_pool`` is None the job is not
    enqueued (dry-run) but the routing decision is still reported, so the
    doctrine outcome is testable without Redis.
    """
    enqueued: list[dict[str, str]] = []
    blocked_from_execution: list[dict[str, str]] = []
    skipped: list[str] = []

    for req in requests:
        channel = (req.channel or "").lower()
        if ApprovalStatus(req.status) != ApprovalStatus.APPROVED:
            skipped.append(req.approval_id)
            continue
        if channel in _BLOCKED_AUTO_CHANNELS:
            # Approved as a draft, but execution is forbidden by doctrine.
            blocked_from_execution.append({
                "approval_id": req.approval_id,
                "channel": channel,
                "reason": "blocked_auto_channel_draft_only",
            })
            log.info(
                "approval_execution_blocked approval_id=%s channel=%s",
                req.approval_id, channel,
            )
            continue
        if not is_auto_executable(req):
            skipped.append(req.approval_id)
            continue

        batch_id = req.object_id
        if redis_pool is not None:
            await redis_pool.enqueue_job(
                "run_outreach_batch",
                batch_id=batch_id,
                tenant_id=req.customer_id or tenant_id,
            )
        enqueued.append({
            "approval_id": req.approval_id,
            "batch_id": batch_id,
            "job": "run_outreach_batch",
            "dispatched": str(redis_pool is not None),
        })

    return {
        "enqueued": enqueued,
        "enqueued_count": len(enqueued),
        "blocked_from_execution": blocked_from_execution,
        "blocked_count": len(blocked_from_execution),
        "skipped": skipped,
        "dry_run": redis_pool is None,
    }
