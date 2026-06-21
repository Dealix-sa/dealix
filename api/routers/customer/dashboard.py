"""
Customer Dashboard API — KPIs, quick actions, notifications.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db as get_db_session
from api.security.auth_deps import get_current_user
from dealix.billing.service import BillingService
from db.models import LeadRecord, DealRecord, TaskRecord, TenantRecord
from db.models_subscription import SubscriptionRecord, InvoiceRecord

router = APIRouter(prefix="/api/v1/customer/dashboard", tags=["Customer Dashboard"])


# ── Schemas ──────────────────────────────────────────────────────

class KPICard(BaseModel):
    label: str
    label_ar: str
    value: str | int | float
    change_pct: float | None = None
    trend: str | None = None  # up / down / flat
    icon: str | None = None


class DashboardOut(BaseModel):
    tenant_name: str
    plan_name: str
    subscription_status: str
    kpi_cards: list[KPICard]
    quick_actions: list[dict[str, Any]]
    recent_activity: list[dict[str, Any]]
    notifications: list[dict[str, Any]]


# ── Endpoints ────────────────────────────────────────────────────

@router.get("/", response_model=DashboardOut)
async def get_dashboard(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    """
    Main customer dashboard — KPIs, quick actions, activity feed.
    """
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    tenant = await session.get(TenantRecord, tenant_id)
    if tenant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")

    billing = BillingService(session)
    sub = await billing.get_active_subscription_for_tenant(tenant_id)
    plan = await billing.get_plan(sub.plan_id) if sub else None

    # KPIs
    kpi_cards: list[KPICard] = []

    # Total leads
    stmt = select(func.count(LeadRecord.id)).where(
        LeadRecord.tenant_id == tenant_id,
        LeadRecord.deleted_at.is_(None),
    )
    result = await session.execute(stmt)
    total_leads = result.scalar() or 0
    kpi_cards.append(KPICard(
        label="Total Leads",
        label_ar="إجمالي العملاء المحتملين",
        value=total_leads,
        icon="users",
    ))

    # Total deals
    stmt = select(func.count(DealRecord.id)).where(
        DealRecord.tenant_id == tenant_id,
        DealRecord.deleted_at.is_(None),
    )
    result = await session.execute(stmt)
    total_deals = result.scalar() or 0
    kpi_cards.append(KPICard(
        label="Active Deals",
        label_ar="الصفقات النشطة",
        value=total_deals,
        icon="briefcase",
    ))

    # Deal value
    stmt = select(func.sum(DealRecord.amount)).where(
        DealRecord.tenant_id == tenant_id,
        DealRecord.deleted_at.is_(None),
    )
    result = await session.execute(stmt)
    deal_value = result.scalar() or 0.0
    kpi_cards.append(KPICard(
        label="Pipeline Value",
        label_ar="قيمة خط الأنابيب",
        value=f"SAR {deal_value:,.0f}",
        icon="trending-up",
    ))

    # Pending tasks
    stmt = select(func.count(TaskRecord.id)).where(
        TaskRecord.tenant_id == tenant_id,
        TaskRecord.status == "pending",
        TaskRecord.deleted_at.is_(None),
    )
    result = await session.execute(stmt)
    pending_tasks = result.scalar() or 0
    kpi_cards.append(KPICard(
        label="Pending Tasks",
        label_ar="المهام المعلقة",
        value=pending_tasks,
        icon="check-circle",
    ))

    # Subscription info
    if sub:
        kpi_cards.append(KPICard(
            label="Plan",
            label_ar="الخطة",
            value=plan.name_en if plan else "Unknown",
            icon="package",
        ))

    # Quick actions
    quick_actions = [
        {"id": "add_lead", "label": "Add Lead", "label_ar": "إضافة عميل محتمل", "icon": "plus", "href": "/crm/leads/new"},
        {"id": "create_deal", "label": "Create Deal", "label_ar": "إنشاء صفقة", "icon": "dollar-sign", "href": "/crm/deals/new"},
        {"id": "view_reports", "label": "Reports", "label_ar": "التقارير", "icon": "bar-chart", "href": "/reports"},
        {"id": "invite_team", "label": "Invite Team", "label_ar": "دعوة فريق", "icon": "user-plus", "href": "/settings/team"},
    ]

    # Recent activity (last 5 leads)
    stmt = (
        select(LeadRecord)
        .where(LeadRecord.tenant_id == tenant_id, LeadRecord.deleted_at.is_(None))
        .order_by(LeadRecord.created_at.desc())
        .limit(5)
    )
    result = await session.execute(stmt)
    recent_leads = result.scalars().all()
    recent_activity = [
        {
            "type": "lead_created",
            "title": f"New lead: {lead.company_name or lead.contact_name}",
            "title_ar": f"عميل محتمل جديد: {lead.company_name or lead.contact_name}",
            "timestamp": lead.created_at.isoformat() if lead.created_at else None,
        }
        for lead in recent_leads
    ]

    # Notifications
    notifications = []
    if sub and sub.status == "trialing" and sub.trial_ends_at:
        from datetime import datetime
        days_left = (sub.trial_ends_at - datetime.now()).days
        if days_left <= 3:
            notifications.append({
                "type": "warning",
                "title": f"Trial ends in {days_left} days",
                "title_ar": f"تنتهي الفترة التجريبية خلال {days_left} أيام",
                "action": {"label": "Upgrade Now", "label_ar": "ترقية الآن", "href": "/settings/billing"},
            })

    # Check for unpaid invoices
    stmt = (
        select(InvoiceRecord)
        .where(
            InvoiceRecord.tenant_id == tenant_id,
            InvoiceRecord.status == "open",
        )
        .limit(1)
    )
    result = await session.execute(stmt)
    unpaid = result.scalar_one_or_none()
    if unpaid:
        notifications.append({
            "type": "alert",
            "title": f"Unpaid invoice: {unpaid.invoice_number}",
            "title_ar": f"فاتورة غير مدفوعة: {unpaid.invoice_number}",
            "action": {"label": "Pay Now", "label_ar": "ادفع الآن", "href": f"/billing/invoices/{unpaid.id}"},
        })

    return {
        "tenant_name": tenant.name,
        "plan_name": plan.name_en if plan else "Free",
        "subscription_status": sub.status if sub else "none",
        "kpi_cards": kpi_cards,
        "quick_actions": quick_actions,
        "recent_activity": recent_activity,
        "notifications": notifications,
    }
