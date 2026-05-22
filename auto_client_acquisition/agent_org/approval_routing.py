"""Route the daily cycle's external drafts into the Approval Center.

When a cycle finishes, every work item with ``status == pending_approval``
must land in the founder's one-click approval queue. This module is the
adapter — it maps each agent's work-item ``kind`` to the canonical
ApprovalRequest ``action_type`` and submits the request as ``draft_only``.

محوّل المخرجات الخارجية للدورة إلى مركز الموافقات — كل مسودة تصل لقائمة
موافقة المؤسس بنقرة واحدة، بنمط ``draft_only`` فقط.
"""

from __future__ import annotations

from typing import Iterable

from auto_client_acquisition.agent_org.orchestrator import (
    STATUS_PENDING_APPROVAL,
    DailyOrgReport,
    WorkItem,
)
from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    ApprovalStore,
    get_default_approval_store,
)

# Map each external work-item kind to a canonical Approval action_type.
# Falls back to the raw kind for anything not in this map (the schema
# accepts free-form action_type strings for back-compat).
_KIND_TO_ACTION_TYPE: dict[str, str] = {
    "outreach_draft": "draft_email",
    "proposal_draft": "draft_email",
    "followup_draft": "follow_up_task",
    "content_draft": "draft_linkedin_manual",
    "distribution_schedule": "draft_linkedin_manual",
    "proof_pack_draft": "proof_request",
}


def _to_request(item: WorkItem, cycle_id: str) -> ApprovalRequest:
    """Build one ApprovalRequest from an external work item."""
    action_type = _KIND_TO_ACTION_TYPE.get(item.kind, item.kind)
    return ApprovalRequest(
        object_type="agent_org_work_item",
        object_id=item.id,
        action_type=action_type,
        action_mode="draft_only",
        summary_ar=item.title_ar,
        summary_en=item.title_en,
        risk_level="low",
        proof_impact=item.summary,
        action_id=item.id,
    )


def route_report_to_approvals(
    report: DailyOrgReport,
    *,
    store: ApprovalStore | None = None,
) -> list[ApprovalRequest]:
    """Push every external work item from ``report`` into the approval store.

    Returns the created ApprovalRequests in submission order. Internal-only
    items are skipped. The doctrine guard mirrors the orchestrator's: only
    ``status == pending_approval`` items are ever routed.
    """
    backend = store or get_default_approval_store()
    created: list[ApprovalRequest] = []
    for item in report.work_items:
        if not item.external or item.status != STATUS_PENDING_APPROVAL:
            continue
        req = _to_request(item, cycle_id=report.cycle_id)
        backend.create(req)
        created.append(req)
    return created


def route_items_to_approvals(
    items: Iterable[WorkItem],
    *,
    store: ApprovalStore | None = None,
) -> list[ApprovalRequest]:
    """Lower-level variant — route an iterable of items directly."""
    backend = store or get_default_approval_store()
    created: list[ApprovalRequest] = []
    for item in items:
        if not item.external or item.status != STATUS_PENDING_APPROVAL:
            continue
        req = _to_request(item, cycle_id="ad_hoc")
        backend.create(req)
        created.append(req)
    return created


__all__ = [
    "route_items_to_approvals",
    "route_report_to_approvals",
]
