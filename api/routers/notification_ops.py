"""Notification Operations — notification management for the Dealix platform.

Endpoints:
  GET  /api/v1/notifications/                 — list all, filterable by unread_only / type
  GET  /api/v1/notifications/unread-summary   — quick unread summary
  POST /api/v1/notifications/mark-all-read    — mark every notification as read
  POST /api/v1/notifications/create           — create a new notification
  POST /api/v1/notifications/{notification_id}/mark-read  — mark one as read
  DELETE /api/v1/notifications/{notification_id}          — delete a notification

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - Bilingual ar/en labels
  - Mutating actions that carry external risk: APPROVAL_FIRST
  - Read-only and low-risk mutations: ALLOW_WITH_REVIEW
"""

from __future__ import annotations

import copy
import uuid
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["notification-ops"],
    dependencies=[Depends(require_admin_key)],
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_MUTATE = "APPROVAL_FIRST"

VALID_TYPES: frozenset[str] = frozenset({
    "health_alert",
    "renewal_reminder",
    "invoice_overdue",
    "proof_pack_ready",
    "churn_signal",
    "approval_required",
    "expansion_opportunity",
})

VALID_PRIORITIES: frozenset[str] = frozenset({"high", "medium", "low"})

# ---------------------------------------------------------------------------
# Demo notification store (NTF-001 through NTF-010)
# Distribution:
#   3 unread "approval_required"
#   2 unread "churn_signal"
#   2 read   "renewal_reminder"
#   2 unread "health_alert"
#   1 read   "proof_pack_ready"
# ---------------------------------------------------------------------------

_NOTIFICATIONS: list[dict[str, Any]] = [
    {
        "notification_id": "NTF-001",
        "type": "approval_required",
        "priority": "high",
        "title_ar": "إجراء بانتظار الموافقة",
        "title_en": "Action Awaiting Approval",
        "body_ar": "يوجد إجراء إرسال Proof Pack للعميل شركة الخدمات اللوجستية يحتاج موافقة المؤسس قبل التنفيذ.",
        "body_en": "A Proof Pack delivery action for Rapid Logistics Co. is pending founder approval before execution.",
        "client_id": "ARC-001",
        "read": False,
        "created_at": "2026-05-28T08:00:00+00:00",
        "read_at": None,
        "requires_action": True,
    },
    {
        "notification_id": "NTF-002",
        "type": "approval_required",
        "priority": "high",
        "title_ar": "إجراء تواصل خارجي بانتظار الموافقة",
        "title_en": "External Outreach Awaiting Approval",
        "body_ar": "رسالة تواصل مع العميل مجموعة التصنيع الصناعي بانتظار مراجعة المؤسس وموافقته.",
        "body_en": "An outreach message to Advanced Industrial Manufacturing Group is pending founder review and approval.",
        "client_id": "ARC-002",
        "read": False,
        "created_at": "2026-05-28T09:00:00+00:00",
        "read_at": None,
        "requires_action": True,
    },
    {
        "notification_id": "NTF-003",
        "type": "approval_required",
        "priority": "medium",
        "title_ar": "طلب تعديل عقد بانتظار الموافقة",
        "title_en": "Contract Amendment Awaiting Approval",
        "body_ar": "طلب تعديل شروط العقد مع العميل أكاديمية التطوير المهني يحتاج مراجعة المؤسس.",
        "body_en": "A contract amendment request for Professional Development Academy is pending founder review.",
        "client_id": "ARC-004",
        "read": False,
        "created_at": "2026-05-29T10:00:00+00:00",
        "read_at": None,
        "requires_action": True,
    },
    {
        "notification_id": "NTF-004",
        "type": "churn_signal",
        "priority": "high",
        "title_ar": "إشارة خطر مرتفعة: خطر توقف العميل",
        "title_en": "High Churn Risk Signal Detected",
        "body_ar": "رُصدت إشارات خطر توقف مرتفعة للعميل شركة الخدمات اللوجستية السريعة. درجة الصحة 18 ولم يُتواصل معه منذ 65 يوماً.",
        "body_en": "High churn risk signals detected for Rapid Logistics Services Co. Health score is 18 and no contact in 65 days.",
        "client_id": "ARC-001",
        "read": False,
        "created_at": "2026-05-29T11:00:00+00:00",
        "read_at": None,
        "requires_action": True,
    },
    {
        "notification_id": "NTF-005",
        "type": "churn_signal",
        "priority": "high",
        "title_ar": "إشارة خطر: انخفاض مستوى التفاعل",
        "title_en": "Churn Signal: Engagement Drop Detected",
        "body_ar": "انخفض مستوى تفاعل العميل مجموعة التصنيع الصناعي المتقدم بشكل حاد خلال آخر 30 يوماً.",
        "body_en": "Engagement level for Advanced Industrial Manufacturing Group dropped sharply in the last 30 days.",
        "client_id": "ARC-002",
        "read": False,
        "created_at": "2026-05-30T07:00:00+00:00",
        "read_at": None,
        "requires_action": True,
    },
    {
        "notification_id": "NTF-006",
        "type": "renewal_reminder",
        "priority": "high",
        "title_ar": "تجديد العقد خلال 12 يوماً",
        "title_en": "Contract Renewing in 12 Days",
        "body_ar": "عقد العميل شركة الخدمات اللوجستية السريعة ينتهي خلال 12 يوماً. ابدأ محادثة التجديد فوراً.",
        "body_en": "Contract for Rapid Logistics Services Co. expires in 12 days. Initiate renewal conversation immediately.",
        "client_id": "ARC-001",
        "read": True,
        "created_at": "2026-05-25T06:00:00+00:00",
        "read_at": "2026-05-25T09:00:00+00:00",
        "requires_action": False,
    },
    {
        "notification_id": "NTF-007",
        "type": "renewal_reminder",
        "priority": "medium",
        "title_ar": "تجديد العقد خلال 18 يوماً",
        "title_en": "Contract Renewing in 18 Days",
        "body_ar": "عقد العميل مجموعة التصنيع الصناعي المتقدم ينتهي خلال 18 يوماً. تأكد من تأكيد التجديد.",
        "body_en": "Contract for Advanced Industrial Manufacturing Group expires in 18 days. Confirm renewal status.",
        "client_id": "ARC-002",
        "read": True,
        "created_at": "2026-05-26T06:00:00+00:00",
        "read_at": "2026-05-26T10:00:00+00:00",
        "requires_action": False,
    },
    {
        "notification_id": "NTF-008",
        "type": "health_alert",
        "priority": "high",
        "title_ar": "تنبيه: انخفاض درجة صحة العميل",
        "title_en": "Alert: Client Health Score Dropped",
        "body_ar": "درجة صحة العميل شركة التجزئة الرقمية الموحدة انخفضت إلى 40 وهي دون الحد الأدنى المقبول.",
        "body_en": "Health score for Unified Digital Retail Co. dropped to 40, falling below the acceptable threshold.",
        "client_id": "ARC-003",
        "read": False,
        "created_at": "2026-05-30T08:00:00+00:00",
        "read_at": None,
        "requires_action": False,
    },
    {
        "notification_id": "NTF-009",
        "type": "health_alert",
        "priority": "medium",
        "title_ar": "تنبيه: درجة صحة العميل أقل من المتوسط",
        "title_en": "Alert: Client Health Score Below Average",
        "body_ar": "درجة صحة العميل أكاديمية التطوير المهني انخفضت إلى 48، وهي تحت المتوسط المستهدف.",
        "body_en": "Health score for Professional Development Academy dropped to 48, below the target average.",
        "client_id": "ARC-004",
        "read": False,
        "created_at": "2026-05-30T09:00:00+00:00",
        "read_at": None,
        "requires_action": False,
    },
    {
        "notification_id": "NTF-010",
        "type": "proof_pack_ready",
        "priority": "low",
        "title_ar": "Proof Pack جاهز للتسليم",
        "title_en": "Proof Pack Ready for Delivery",
        "body_ar": "تمت الموافقة على Proof Pack للعميل شركة الرعاية الصحية المتكاملة وهو جاهز للتسليم الآن.",
        "body_en": "Proof Pack for Integrated Healthcare Co. has been approved and is ready for delivery.",
        "client_id": "ARC-005",
        "read": True,
        "created_at": "2026-05-24T14:00:00+00:00",
        "read_at": "2026-05-24T16:00:00+00:00",
        "requires_action": False,
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(UTC).isoformat()


def _priority_order(p: str) -> int:
    """Return sort key for priority: high=0, medium=1, low=2."""
    return {"high": 0, "medium": 1, "low": 2}.get(p, 99)


def _notification_or_404(notification_id: str) -> dict[str, Any]:
    """Return notification record or raise HTTP 404."""
    for n in _NOTIFICATIONS:
        if n["notification_id"] == notification_id:
            return n
    raise HTTPException(
        status_code=404,
        detail={
            "ar": f"الإشعار '{notification_id}' غير موجود",
            "en": f"Notification '{notification_id}' not found",
        },
    )


def _sorted_notifications(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort notifications by priority then created_at descending."""
    return sorted(
        records,
        key=lambda n: (_priority_order(n["priority"]), n["created_at"]),
        reverse=False,
    )


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------


class CreateNotificationBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = Field(
        description=(
            "One of: health_alert, renewal_reminder, invoice_overdue, "
            "proof_pack_ready, churn_signal, approval_required, expansion_opportunity"
        ),
    )
    priority: str = Field(
        description="One of: high, medium, low",
    )
    title_ar: str = Field(min_length=3)
    title_en: str = Field(min_length=3)
    body_ar: str = Field(min_length=5)
    body_en: str = Field(min_length=5)
    client_id: str | None = None
    requires_action: bool = False


# ---------------------------------------------------------------------------
# Endpoints — fixed paths first, then parameterised
# ---------------------------------------------------------------------------


@router.get("/")
async def list_notifications(
    unread_only: bool = Query(default=False, description="Return only unread notifications"),
    type: str | None = Query(default=None, description="Filter by notification type"),
) -> dict[str, Any]:
    """List all notifications, optionally filtered by unread status or type.

    Sorted by priority (high first) then created_at descending.
    """
    records = list(_NOTIFICATIONS)

    if unread_only:
        records = [n for n in records if not n["read"]]

    if type is not None:
        records = [n for n in records if n["type"] == type]

    sorted_records = _sorted_notifications(records)

    total_count = len(_NOTIFICATIONS)
    unread_count = sum(1 for n in _NOTIFICATIONS if not n["read"])
    requires_action_count = sum(1 for n in _NOTIFICATIONS if n.get("requires_action"))

    _log.info(
        "notifications_listed",
        total=len(sorted_records),
        unread_only=unread_only,
        type_filter=type,
    )

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total_count": total_count,
        "unread_count": unread_count,
        "requires_action_count": requires_action_count,
        "notifications": sorted_records,
    }


@router.get("/unread-summary")
async def get_unread_summary() -> dict[str, Any]:
    """Quick summary of unread notifications for header/badge display."""
    unread = [n for n in _NOTIFICATIONS if not n["read"]]
    high_priority_unread = sum(1 for n in unread if n["priority"] == "high")
    requires_action_count = sum(1 for n in _NOTIFICATIONS if n.get("requires_action"))

    sorted_unread = _sorted_notifications(unread)
    top_3 = sorted_unread[:3]

    _log.info(
        "unread_summary_fetched",
        unread_count=len(unread),
        high_priority=high_priority_unread,
    )

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "unread_count": len(unread),
        "high_priority_unread": high_priority_unread,
        "requires_action_count": requires_action_count,
        "top_3_unread": top_3,
    }


@router.post("/mark-all-read")
async def mark_all_read() -> dict[str, Any]:
    """Mark every unread notification as read."""
    timestamp = _now_iso()
    marked_count = 0

    for n in _NOTIFICATIONS:
        if not n["read"]:
            n["read"] = True
            n["read_at"] = timestamp
            marked_count += 1

    all_read = all(n["read"] for n in _NOTIFICATIONS)

    _log.info("notifications_all_marked_read", marked_count=marked_count)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": timestamp,
        "marked_count": marked_count,
        "all_read": all_read,
    }


@router.post("/create")
async def create_notification(body: CreateNotificationBody) -> dict[str, Any]:
    """Create a new notification.

    For type='approval_required' the governance decision is APPROVAL_FIRST.
    All other types use ALLOW_WITH_REVIEW.
    """
    if body.type not in VALID_TYPES:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"نوع الإشعار '{body.type}' غير صالح",
                "en": f"Invalid notification type '{body.type}'",
                "valid_types": sorted(VALID_TYPES),
            },
        )

    if body.priority not in VALID_PRIORITIES:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"الأولوية '{body.priority}' غير صالحة",
                "en": f"Invalid priority '{body.priority}'",
                "valid_priorities": sorted(VALID_PRIORITIES),
            },
        )

    governance = _GOV_MUTATE if body.type == "approval_required" else _GOV_READ
    timestamp = _now_iso()
    notification_id = f"NTF-{uuid.uuid4().hex[:8].upper()}"

    record: dict[str, Any] = {
        "notification_id": notification_id,
        "type": body.type,
        "priority": body.priority,
        "title_ar": body.title_ar,
        "title_en": body.title_en,
        "body_ar": body.body_ar,
        "body_en": body.body_en,
        "client_id": body.client_id,
        "read": False,
        "created_at": timestamp,
        "read_at": None,
        "requires_action": body.requires_action,
    }
    _NOTIFICATIONS.append(record)

    _log.info(
        "notification_created",
        notification_id=notification_id,
        type=body.type,
        priority=body.priority,
        governance=governance,
    )

    return {
        "governance_decision": governance,
        "generated_at": timestamp,
        "notification": record,
    }


@router.post("/{notification_id}/mark-read")
async def mark_notification_read(notification_id: str) -> dict[str, Any]:
    """Mark a single notification as read.

    Returns 404 if the notification does not exist.
    Returns 409 if the notification is already read.
    """
    record = _notification_or_404(notification_id)

    if record["read"]:
        raise HTTPException(
            status_code=409,
            detail={
                "ar": f"الإشعار '{notification_id}' مقروء بالفعل",
                "en": f"Notification '{notification_id}' is already marked as read",
            },
        )

    timestamp = _now_iso()
    record["read"] = True
    record["read_at"] = timestamp

    _log.info("notification_marked_read", notification_id=notification_id)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": timestamp,
        "notification_id": notification_id,
        "read": True,
        "read_at": timestamp,
    }


@router.delete("/{notification_id}")
async def delete_notification(notification_id: str) -> dict[str, Any]:
    """Delete a notification by ID.

    Returns 404 if the notification does not exist.
    Returns 400 if the notification type is 'approval_required' and requires_action=True
    (approval-required items must be actioned before they can be deleted).
    """
    record = _notification_or_404(notification_id)

    if record["type"] == "approval_required" and record.get("requires_action"):
        raise HTTPException(
            status_code=400,
            detail={
                "ar": (
                    f"لا يمكن حذف الإشعار '{notification_id}': "
                    "يجب إتمام الإجراء المطلوب قبل الحذف"
                ),
                "en": (
                    f"Cannot delete notification '{notification_id}': "
                    "the required action must be completed before deletion"
                ),
                "doctrine_note": "approval_required_notifications_must_be_actioned_before_deletion",
            },
        )

    _NOTIFICATIONS.remove(record)
    timestamp = _now_iso()

    _log.info("notification_deleted", notification_id=notification_id)

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": timestamp,
        "notification_id": notification_id,
        "deleted": True,
        "message_ar": f"تم حذف الإشعار '{notification_id}' بنجاح",
        "message_en": f"Notification '{notification_id}' deleted successfully",
    }
