"""Authenticated, tenant-derived customer dashboard.

This route is the narrow browser-facing operating summary used by the Next.js
workspace. It derives tenant identity from the validated JWT user record and
returns only aggregate, evidence-backed values. No browser-supplied tenant
header, simulated metric, payment action, or outbound action is accepted here.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user
from db.models import (
    AuditLogRecord,
    DealRecord,
    LeadRecord,
    TenantRecord,
    UserRecord,
)
from db.models_subscription import PlanRecord, SubscriptionRecord
from db.session import get_db

router = APIRouter(prefix="/api/v1/customer", tags=["customer-dashboard"])


def _normalized_subscription_status(value: str | None) -> str:
    normalized = str(value or "unknown").strip().lower()
    aliases = {
        "cancelled": "canceled",
        "churned": "canceled",
        "suspended": "paused",
    }
    return aliases.get(normalized, normalized or "unknown")


async def _count_rows(db: AsyncSession, model: type[Any], *conditions: Any) -> int:
    query = select(func.count()).select_from(model)
    if conditions:
        query = query.where(*conditions)
    result = await db.execute(query)
    return int(result.scalar_one())


@router.get("/dashboard/")
async def customer_dashboard(
    current_user: UserRecord = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Return an authenticated tenant operating summary with no invented data."""
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="An active tenant workspace is required",
        )

    tenant_result = await db.execute(
        select(TenantRecord).where(
            TenantRecord.id == tenant_id,
            TenantRecord.deleted_at.is_(None),
        )
    )
    tenant = tenant_result.scalar_one_or_none()
    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant workspace not found",
        )

    subscription_result = await db.execute(
        select(SubscriptionRecord, PlanRecord)
        .outerjoin(PlanRecord, PlanRecord.id == SubscriptionRecord.plan_id)
        .where(SubscriptionRecord.tenant_id == tenant_id)
        .order_by(SubscriptionRecord.updated_at.desc())
        .limit(1)
    )
    subscription_row = subscription_result.first()
    subscription = subscription_row[0] if subscription_row else None
    plan = subscription_row[1] if subscription_row else None

    subscription_status = _normalized_subscription_status(
        subscription.status if subscription is not None else tenant.status
    )
    plan_name = (
        (plan.name_ar or plan.name_en or plan.slug)
        if plan is not None
        else tenant.plan
    )

    users_count = await _count_rows(
        db,
        UserRecord,
        UserRecord.tenant_id == tenant_id,
        UserRecord.is_active.is_(True),
        UserRecord.deleted_at.is_(None),
    )
    leads_count = await _count_rows(
        db,
        LeadRecord,
        LeadRecord.tenant_id == tenant_id,
        LeadRecord.deleted_at.is_(None),
    )
    deals_count = await _count_rows(
        db,
        DealRecord,
        DealRecord.tenant_id == tenant_id,
        DealRecord.deleted_at.is_(None),
    )
    audit_count = await _count_rows(
        db,
        AuditLogRecord,
        AuditLogRecord.tenant_id == tenant_id,
    )

    audit_result = await db.execute(
        select(AuditLogRecord)
        .where(AuditLogRecord.tenant_id == tenant_id)
        .order_by(AuditLogRecord.created_at.desc())
        .limit(8)
    )
    recent_activity = [
        {
            "title": event.action,
            "title_ar": f"نشاط موثق: {event.action}",
            "timestamp": event.created_at.isoformat(),
        }
        for event in audit_result.scalars().all()
    ]

    notifications: list[dict[str, Any]] = []
    if subscription is None:
        notifications.append(
            {
                "type": "info",
                "title": "No subscription record is attached to this workspace",
                "title_ar": "لا يوجد سجل اشتراك مرتبط بمساحة العمل",
                "action": {
                    "label": "Review billing settings",
                    "label_ar": "مراجعة إعدادات الفوترة",
                    "href": "/settings/billing",
                },
            }
        )
    elif subscription_status == "past_due":
        notifications.append(
            {
                "type": "warning",
                "title": "Subscription payment is past due",
                "title_ar": "دفعة الاشتراك متأخرة",
                "action": {
                    "label": "Review billing settings",
                    "label_ar": "مراجعة إعدادات الفوترة",
                    "href": "/settings/billing",
                },
            }
        )
    elif subscription_status in {"canceled", "paused"}:
        notifications.append(
            {
                "type": "error",
                "title": f"Subscription status: {subscription_status}",
                "title_ar": "الاشتراك غير نشط ويحتاج مراجعة",
                "action": {
                    "label": "Review billing settings",
                    "label_ar": "مراجعة إعدادات الفوترة",
                    "href": "/settings/billing",
                },
            }
        )

    return {
        "tenant_name": tenant.name,
        "plan_name": plan_name,
        "subscription_status": subscription_status,
        "kpi_cards": [
            {
                "label": "Active users",
                "label_ar": "المستخدمون النشطون",
                "value": users_count,
                "icon": "users",
            },
            {
                "label": "Leads",
                "label_ar": "العملاء المحتملون",
                "value": leads_count,
                "icon": "trending-up",
            },
            {
                "label": "Deals",
                "label_ar": "الصفقات",
                "value": deals_count,
                "icon": "briefcase",
            },
            {
                "label": "Audit events",
                "label_ar": "أحداث التدقيق",
                "value": audit_count,
                "icon": "check-circle",
            },
        ],
        "quick_actions": [
            {
                "id": "review-crm",
                "label": "Review customers and opportunities",
                "label_ar": "مراجعة العملاء والفرص",
                "href": "/crm",
            },
            {
                "id": "review-projects",
                "label": "Review projects",
                "label_ar": "مراجعة المشاريع",
                "href": "/projects",
            },
            {
                "id": "review-documents",
                "label": "Review documents",
                "label_ar": "مراجعة المستندات",
                "href": "/documents",
            },
            {
                "id": "review-billing",
                "label": "Review billing settings",
                "label_ar": "مراجعة إعدادات الفوترة",
                "href": "/settings/billing",
            },
        ],
        "recent_activity": recent_activity,
        "notifications": notifications,
    }
