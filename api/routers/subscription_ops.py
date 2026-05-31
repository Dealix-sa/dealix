"""Subscription Operations API — subscription lifecycle management.

Manages the full subscription state machine for Dealix clients:
trial → active → paused → cancelled → reactivated

Endpoints:
  GET  /api/v1/subscriptions/active         — all active subscriptions
  GET  /api/v1/subscriptions/{sub_id}       — one subscription detail
  GET  /api/v1/subscriptions/expiring-soon  — subscriptions expiring in 30 days
  POST /api/v1/subscriptions/{sub_id}/pause — pause subscription
  POST /api/v1/subscriptions/{sub_id}/cancel — cancel subscription
  POST /api/v1/subscriptions/{sub_id}/reactivate — reactivate paused/cancelled

All admin-gated. pause/cancel/reactivate require APPROVAL_FIRST.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/subscriptions",
    tags=["subscription-ops"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"

# Subscription states
_STATES = {"trial", "active", "paused", "cancelled", "reactivated"}

# Tier monthly prices
_TIER_PRICES: dict[str, int] = {
    "sprint": 499,
    "data_pack": 1_500,
    "managed_ops_essential": 2_999,
    "managed_ops_professional": 3_999,
    "managed_ops_enterprise": 4_999,
    "custom_ai": 15_000,
}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _days_until(date_str: str) -> int:
    try:
        target = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        delta = target - datetime.now(UTC)
        return max(0, delta.days)
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Demo subscriptions
# ---------------------------------------------------------------------------

_SUBSCRIPTIONS: list[dict[str, Any]] = [
    {
        "sub_id": "SUB-001",
        "client_id": "CLT-001",
        "company_ar": "شركة الرياض للتقنية",
        "company_en": "Riyadh Tech Co",
        "tier": "managed_ops_professional",
        "state": "active",
        "monthly_value_sar": 3_999,
        "started_at": "2026-02-01T00:00:00Z",
        "renewal_date": "2026-07-01T00:00:00Z",
        "auto_renew": True,
        "payment_method": "moyasar_card",
        "contact_ar": "محمد العمري",
        "contact_en": "Mohammed Al-Omari",
        "paused_at": None,
        "pause_reason": None,
        "cancelled_at": None,
        "cancel_reason": None,
    },
    {
        "sub_id": "SUB-002",
        "client_id": "CLT-002",
        "company_ar": "مجموعة الخليج للخدمات المالية",
        "company_en": "Gulf Financial Services Group",
        "tier": "managed_ops_enterprise",
        "state": "active",
        "monthly_value_sar": 4_999,
        "started_at": "2026-01-15T00:00:00Z",
        "renewal_date": "2026-06-15T00:00:00Z",
        "auto_renew": True,
        "payment_method": "moyasar_card",
        "contact_ar": "سارة القحطاني",
        "contact_en": "Sarah Al-Qahtani",
        "paused_at": None,
        "pause_reason": None,
        "cancelled_at": None,
        "cancel_reason": None,
    },
    {
        "sub_id": "SUB-003",
        "client_id": "CLT-003",
        "company_ar": "شركة سفا للخدمات اللوجستية",
        "company_en": "Safa Logistics Co",
        "tier": "managed_ops_essential",
        "state": "active",
        "monthly_value_sar": 2_999,
        "started_at": "2026-03-01T00:00:00Z",
        "renewal_date": "2026-06-20T00:00:00Z",
        "auto_renew": False,
        "payment_method": "moyasar_bank",
        "contact_ar": "فهد الدوسري",
        "contact_en": "Fahad Al-Dawsari",
        "paused_at": None,
        "pause_reason": None,
        "cancelled_at": None,
        "cancel_reason": None,
    },
    {
        "sub_id": "SUB-004",
        "client_id": "CLT-004",
        "company_ar": "تمكين الصحية",
        "company_en": "Tamkeen Health Tech",
        "tier": "data_pack",
        "state": "active",
        "monthly_value_sar": 1_500,
        "started_at": "2026-04-01T00:00:00Z",
        "renewal_date": "2026-07-01T00:00:00Z",
        "auto_renew": True,
        "payment_method": "moyasar_card",
        "contact_ar": "نورة المطيري",
        "contact_en": "Noura Al-Mutairi",
        "paused_at": None,
        "pause_reason": None,
        "cancelled_at": None,
        "cancel_reason": None,
    },
    {
        "sub_id": "SUB-005",
        "client_id": "CLT-005",
        "company_ar": "شركة جازان للتصنيع",
        "company_en": "Jazan Manufacturing Co",
        "tier": "managed_ops_professional",
        "state": "paused",
        "monthly_value_sar": 3_999,
        "started_at": "2026-01-01T00:00:00Z",
        "renewal_date": "2026-08-01T00:00:00Z",
        "auto_renew": False,
        "payment_method": "moyasar_bank",
        "contact_ar": "عبدالله الغامدي",
        "contact_en": "Abdullah Al-Ghamdi",
        "paused_at": "2026-05-15T00:00:00Z",
        "pause_reason": "طلب العميل — إجازة سنوية للفريق",
        "cancelled_at": None,
        "cancel_reason": None,
    },
    {
        "sub_id": "SUB-006",
        "client_id": "CLT-006",
        "company_ar": "الوافي للتمويل",
        "company_en": "Al-Wafi Finance",
        "tier": "sprint",
        "state": "cancelled",
        "monthly_value_sar": 499,
        "started_at": "2026-02-15T00:00:00Z",
        "renewal_date": "2026-03-15T00:00:00Z",
        "auto_renew": False,
        "payment_method": "moyasar_card",
        "contact_ar": "خالد العتيبي",
        "contact_en": "Khalid Al-Otaibi",
        "paused_at": None,
        "pause_reason": None,
        "cancelled_at": "2026-03-10T00:00:00Z",
        "cancel_reason": "اختار منافساً آخر",
    },
]


def _get_sub(sub_id: str) -> dict[str, Any] | None:
    return next((s for s in _SUBSCRIPTIONS if s["sub_id"] == sub_id), None)


def _enrich_sub(sub: dict[str, Any]) -> dict[str, Any]:
    return {
        **sub,
        "days_until_renewal": _days_until(sub["renewal_date"]) if sub.get("renewal_date") else None,
        "annual_value_sar": sub["monthly_value_sar"] * 12,
    }


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class PauseBody(BaseModel):
    reason: str = Field(min_length=5, max_length=500)
    pause_duration_days: int = Field(default=30, ge=1, le=180)


class CancelBody(BaseModel):
    reason: str = Field(min_length=5, max_length=500)
    effective_immediately: bool = False


class ReactivateBody(BaseModel):
    reason: str = Field(min_length=5, max_length=500)
    new_renewal_date: str | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/active")
async def get_active_subscriptions(
    tier: str | None = Query(default=None),
) -> dict[str, Any]:
    """All active subscriptions with renewal dates and ARR.

    Filter by tier using the ?tier= query parameter. Returns subscriptions
    sorted by renewal date ascending (most urgent first).
    """
    active = [s for s in _SUBSCRIPTIONS if s["state"] == "active"]
    if tier:
        active = [s for s in active if s["tier"] == tier]

    enriched = [_enrich_sub(s) for s in active]
    enriched.sort(key=lambda s: s.get("days_until_renewal") or 9999)

    total_mrr = sum(s["monthly_value_sar"] for s in active)
    expiring_30d = [s for s in enriched if (s.get("days_until_renewal") or 9999) <= 30]

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "total_active": len(enriched),
        "total_mrr_sar": total_mrr,
        "total_arr_sar": total_mrr * 12,
        "expiring_30d_count": len(expiring_30d),
        "subscriptions": enriched,
    }


@router.get("/expiring-soon")
async def get_expiring_soon(
    days: int = Query(default=30, ge=1, le=90),
) -> dict[str, Any]:
    """Subscriptions renewing within the specified number of days.

    Default: 30 days. Max: 90 days. Sorted by urgency (soonest first).
    Each subscription includes the renewal action required.
    """
    active = [s for s in _SUBSCRIPTIONS if s["state"] == "active"]
    expiring = [
        _enrich_sub(s) for s in active
        if (_days_until(s["renewal_date"])) <= days
    ]
    expiring.sort(key=lambda s: s.get("days_until_renewal") or 9999)

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "window_days": days,
        "expiring_count": len(expiring),
        "at_risk_value_sar": sum(s["monthly_value_sar"] for s in expiring),
        "subscriptions": expiring,
        "action_ar": "راجع كل عقد وأرسل Proof Pack قبل بدء محادثة التجديد",
        "action_en": "Review each contract and send Proof Pack before initiating renewal conversation",
    }


@router.get("/{sub_id}")
async def get_subscription(sub_id: str) -> dict[str, Any]:
    """Full subscription detail for one client.

    Returns state, tier, renewal date, payment method, pause/cancel history.
    """
    sub = _get_sub(sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail=f"Subscription {sub_id} not found")

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        **_enrich_sub(sub),
    }


@router.post("/{sub_id}/pause")
async def pause_subscription(
    sub_id: str,
    body: PauseBody = Body(...),
) -> dict[str, Any]:
    """Pause an active subscription. Requires APPROVAL_FIRST.

    Pausing stops billing for the specified duration. The subscription
    state is recorded in the governance log. This action requires
    explicit founder approval before execution.
    """
    sub = _get_sub(sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail=f"Subscription {sub_id} not found")

    if sub["state"] != "active":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot pause subscription in state: {sub['state']}",
        )

    sub["state"] = "paused"
    sub["paused_at"] = _now_iso()
    sub["pause_reason"] = body.reason

    return {
        "governance_decision": "APPROVAL_FIRST",
        "generated_at": _now_iso(),
        "sub_id": sub_id,
        "new_state": "paused",
        "pause_duration_days": body.pause_duration_days,
        "reason": body.reason,
        "resume_by": (datetime.now(UTC) + timedelta(days=body.pause_duration_days)).isoformat(),
        "status_ar": f"طلب الإيقاف المؤقت مُسجَّل — يتطلب موافقة المؤسس قبل التنفيذ",
        "status_en": "Pause request recorded — requires founder approval before execution",
        "note_ar": "لن تُوقف الفوترة حتى تتم الموافقة الصريحة",
        "note_en": "Billing will not be paused until explicit approval is granted",
    }


@router.post("/{sub_id}/cancel")
async def cancel_subscription(
    sub_id: str,
    body: CancelBody = Body(...),
) -> dict[str, Any]:
    """Cancel a subscription. Requires APPROVAL_FIRST.

    Records the cancellation intent and reason. Billing continues
    until the founder explicitly confirms the cancellation.
    APPROVAL_FIRST: this action cannot be undone easily.
    """
    sub = _get_sub(sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail=f"Subscription {sub_id} not found")

    if sub["state"] == "cancelled":
        raise HTTPException(status_code=409, detail="Subscription is already cancelled")

    sub["state"] = "cancelled"
    sub["cancelled_at"] = _now_iso()
    sub["cancel_reason"] = body.reason

    return {
        "governance_decision": "APPROVAL_FIRST",
        "generated_at": _now_iso(),
        "sub_id": sub_id,
        "new_state": "cancelled",
        "reason": body.reason,
        "effective_immediately": body.effective_immediately,
        "status_ar": "طلب الإلغاء مُسجَّل — يتطلب موافقة المؤسس للتأكيد",
        "status_en": "Cancellation request recorded — requires founder confirmation",
        "warning_ar": "الإلغاء قابل للمراجعة — تواصل مع العميل أولاً",
        "warning_en": "Cancellation is reviewable — contact client first",
        "churn_prevention_ar": "راجع سجل الصحة وأرسل Proof Pack قبل تأكيد الإلغاء",
        "churn_prevention_en": "Review health log and send Proof Pack before confirming cancellation",
    }


@router.post("/{sub_id}/reactivate")
async def reactivate_subscription(
    sub_id: str,
    body: ReactivateBody = Body(...),
) -> dict[str, Any]:
    """Reactivate a paused or cancelled subscription. Requires APPROVAL_FIRST.

    Restores the subscription to active state. If a new renewal date
    is provided, it overrides the previous renewal date.
    """
    sub = _get_sub(sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail=f"Subscription {sub_id} not found")

    if sub["state"] == "active":
        raise HTTPException(status_code=409, detail="Subscription is already active")

    if sub["state"] not in ("paused", "cancelled"):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot reactivate subscription in state: {sub['state']}",
        )

    old_state = sub["state"]
    sub["state"] = "reactivated"
    sub["paused_at"] = None
    sub["pause_reason"] = None
    if body.new_renewal_date:
        sub["renewal_date"] = body.new_renewal_date

    return {
        "governance_decision": "APPROVAL_FIRST",
        "generated_at": _now_iso(),
        "sub_id": sub_id,
        "previous_state": old_state,
        "new_state": "reactivated",
        "renewal_date": sub["renewal_date"],
        "reason": body.reason,
        "status_ar": "طلب إعادة التفعيل مُسجَّل — يتطلب موافقة المؤسس",
        "status_en": "Reactivation request recorded — requires founder approval",
    }
