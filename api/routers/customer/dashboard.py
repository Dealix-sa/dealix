"""Customer Dashboard API — evidence-backed tenant KPIs and next actions."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user
from core.utils import utcnow
from db.models import DealRecord, LeadRecord, TenantRecord, UserRecord
from db.models_subscription import InvoiceRecord
from db.session import get_db as get_db_session
from dealix.billing.service import BillingService

router = APIRouter(
    prefix="/api/v1/customer/dashboard",
    tags=["Customer Dashboard"],
)


class KPICard(BaseModel):
    label: str
    label_ar: str
    value: str | int | float
    change_pct: float | None = None
    trend: str | None = None
    icon: str | None = None


class DashboardOut(BaseModel):
    tenant_name: str
    plan_name: str
    subscription_status: str
    kpi_cards: list[KPICard]
    quick_actions: list[dict[str, Any]]
    recent_activity: list[dict[str, Any]]
    notifications: list[dict[str, Any]]


@router.get("/", response_model=DashboardOut)
async def get_dashboard(
    session: AsyncSession = Depends(get_db_session),
    current_user: UserRecord = Depends(get_current_user),
) -> dict[str, Any]:
    """Return a read-only dashboard derived from the authenticated tenant."""
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="An active tenant workspace is required",
        )

    tenant = await session.get(TenantRecord, tenant_id)
    if tenant is None or tenant.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant workspace not found",
        )

    billing = BillingService(session)
    subscription = await billing.get_active_subscription_for_tenant(tenant_id)
    plan = await billing.get_plan(subscription.plan_id) if subscription else None

    users_result = await session.execute(
        select(func.count(UserRecord.id)).where(
            UserRecord.tenant_id == tenant_id,
            UserRecord.is_active.is_(True),
            UserRecord.deleted_at.is_(None),
        )
    )
    active_users = int(users_result.scalar() or 0)

    leads_result = await session.execute(
        select(func.count(LeadRecord.id)).where(
            LeadRecord.tenant_id == tenant_id,
            LeadRecord.deleted_at.is_(None),
        )
    )
    total_leads = int(leads_result.scalar() or 0)

    deals_result = await session.execute(
        select(func.count(DealRecord.id)).where(
            DealRecord.tenant_id == tenant_id,
            DealRecord.deleted_at.is_(None),
        )
    )
    total_deals = int(deals_result.scalar() or 0)

    value_result = await session.execute(
        select(func.sum(DealRecord.amount)).where(
            DealRecord.tenant_id == tenant_id,
            DealRecord.deleted_at.is_(None),
        )
    )
    pipeline_value = float(value_result.scalar() or 0.0)

    kpi_cards = [
        KPICard(
            label="Active Users",
            label_ar="المستخدمون النشطون",
            value=active_users,
            icon="users",
        ),
        KPICard(
            label="Total Leads",
            label_ar="إجمالي العملاء المحتملين",
            value=total_leads,
            icon="trending-up",
        ),
        KPICard(
            label="Deals",
            label_ar="الصفقات",
            value=total_deals,
            icon="briefcase",
        ),
        KPICard(
            label="Pipeline Value",
            label_ar="قيمة خط الأنابيب",
            value=f"SAR {pipeline_value:,.0f}",
            icon="check-circle",
        ),
    ]

    quick_actions = [
        {
            "id": "add_lead",
            "label": "Add Lead",
            "label_ar": "إضافة عميل محتمل",
            "icon": "plus",
            "href": "/crm/leads/new",
        },
        {
            "id": "create_deal",
            "label": "Create Deal",
            "label_ar": "إنشاء صفقة",
            "icon": "dollar-sign",
            "href": "/crm/deals/new",
        },
        {
            "id": "view_reports",
            "label": "Reports",
            "label_ar": "التقارير",
            "icon": "bar-chart",
            "href": "/reports",
        },
        {
            "id": "invite_team",
            "label": "Invite Team",
            "label_ar": "دعوة فريق",
            "icon": "user-plus",
            "href": "/settings/team",
        },
    ]

    recent_result = await session.execute(
        select(LeadRecord)
        .where(
            LeadRecord.tenant_id == tenant_id,
            LeadRecord.deleted_at.is_(None),
        )
        .order_by(LeadRecord.created_at.desc())
        .limit(5)
    )
    recent_activity = [
        {
            "type": "lead_created",
            "title": f"New lead: {lead.company_name or lead.contact_name}",
            "title_ar": (
                f"عميل محتمل جديد: {lead.company_name or lead.contact_name}"
            ),
            "timestamp": lead.created_at.isoformat() if lead.created_at else None,
        }
        for lead in recent_result.scalars().all()
    ]

    notifications: list[dict[str, Any]] = []
    if subscription and subscription.status == "trialing" and subscription.trial_ends_at:
        days_left = max(0, (subscription.trial_ends_at - utcnow()).days)
        if days_left <= 3:
            notifications.append(
                {
                    "type": "warning",
                    "title": f"Trial ends in {days_left} days",
                    "title_ar": f"تنتهي الفترة التجريبية خلال {days_left} أيام",
                    "action": {
                        "label": "Review billing",
                        "label_ar": "مراجعة الفوترة",
                        "href": "/settings/billing",
                    },
                }
            )

    invoice_result = await session.execute(
        select(InvoiceRecord)
        .where(
            InvoiceRecord.tenant_id == tenant_id,
            InvoiceRecord.status == "open",
        )
        .limit(1)
    )
    unpaid_invoice = invoice_result.scalar_one_or_none()
    if unpaid_invoice:
        notifications.append(
            {
                "type": "warning",
                "title": f"Open invoice: {unpaid_invoice.invoice_number}",
                "title_ar": f"فاتورة مفتوحة: {unpaid_invoice.invoice_number}",
                "action": {
                    "label": "Review invoice",
                    "label_ar": "مراجعة الفاتورة",
                    "href": f"/billing/invoices/{unpaid_invoice.id}",
                },
            }
        )

    return {
        "tenant_name": tenant.name,
        "plan_name": plan.name_en if plan else tenant.plan,
        "subscription_status": subscription.status if subscription else tenant.status,
        "kpi_cards": kpi_cards,
        "quick_actions": quick_actions,
        "recent_activity": recent_activity,
        "notifications": notifications,
    }
