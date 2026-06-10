"""
Billing API — subscriptions, invoices, plans, upgrades.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db as get_db_session
from api.security.auth_deps import get_current_user
from dealix.billing.service import BillingService
from dealix.payments.payment_link import PaymentLinkRequest, create_payment_link as create_moyasar_payment_link

router = APIRouter(prefix="/api/v1/billing", tags=["Billing"])


# ── Schemas ──────────────────────────────────────────────────────

class PlanOut(BaseModel):
    id: str
    name_ar: str
    name_en: str
    slug: str
    price_sar_monthly: float
    price_sar_yearly: float | None
    yearly_discount_pct: float
    max_users: int
    max_leads_per_month: int
    max_storage_gb: float
    max_api_calls_per_month: int
    features: dict[str, bool]
    sort_order: int

    class Config:
        from_attributes = True


class SubscriptionOut(BaseModel):
    id: str
    plan_id: str
    billing_cycle: str
    status: str
    trial_ends_at: datetime | None
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    seat_count: int
    mrr_sar: float

    class Config:
        from_attributes = True


class InvoiceOut(BaseModel):
    id: str
    invoice_number: str
    status: str
    total_sar: float
    due_date: datetime | None
    paid_at: datetime | None
    line_items: list[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class SubscribeRequest(BaseModel):
    plan_slug: str = Field(..., description="Plan slug to subscribe to")
    billing_cycle: str = Field(default="monthly", pattern="^(monthly|yearly)$")
    seat_count: int = Field(default=1, ge=1)


class UpgradeRequest(BaseModel):
    plan_slug: str
    billing_cycle: str | None = None


class CancelRequest(BaseModel):
    reason: str | None = None
    immediate: bool = False


# ── Endpoints ────────────────────────────────────────────────────

@router.get("/plans", response_model=list[PlanOut])
async def list_plans(
    session: AsyncSession = Depends(get_db_session),
) -> list[Any]:
    """List all public SaaS plans."""
    svc = BillingService(session)
    return await svc.list_plans()


@router.get("/subscription", response_model=SubscriptionOut)
async def get_subscription(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> Any:
    """Get current tenant subscription."""
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    svc = BillingService(session)
    sub = await svc.get_active_subscription_for_tenant(tenant_id)
    if sub is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscription")
    return sub


@router.post("/subscribe", response_model=SubscriptionOut)
async def subscribe(
    req: SubscribeRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> Any:
    """Create or upgrade subscription."""
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    svc = BillingService(session)
    plan = await svc.get_plan_by_slug(req.plan_slug)
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    existing = await svc.get_active_subscription_for_tenant(tenant_id)
    if existing:
        # Upgrade
        sub = await svc.upgrade_subscription(
            existing.id, plan.id, req.billing_cycle
        )
    else:
        # New
        sub = await svc.create_subscription(
            tenant_id=tenant_id,
            plan_id=plan.id,
            billing_cycle=req.billing_cycle,
            seat_count=req.seat_count,
        )
    await session.commit()
    return sub


@router.post("/upgrade", response_model=SubscriptionOut)
async def upgrade(
    req: UpgradeRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> Any:
    """Upgrade current subscription."""
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    svc = BillingService(session)
    sub = await svc.get_active_subscription_for_tenant(tenant_id)
    if sub is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscription")

    plan = await svc.get_plan_by_slug(req.plan_slug)
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    updated = await svc.upgrade_subscription(
        sub.id, plan.id, req.billing_cycle or sub.billing_cycle
    )
    await session.commit()
    return updated


@router.post("/cancel")
async def cancel(
    req: CancelRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    """Cancel subscription."""
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    svc = BillingService(session)
    sub = await svc.get_active_subscription_for_tenant(tenant_id)
    if sub is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscription")

    await svc.cancel_subscription(sub.id, req.reason, req.immediate)
    await session.commit()

    return {
        "status": "cancelled" if req.immediate else "scheduled",
        "message": "Subscription cancelled" if req.immediate else "Subscription will cancel at period end",
        "message_ar": "تم إلغاء الاشتراك" if req.immediate else "سيتم إلغاء الاشتراك في نهاية الفترة",
    }


@router.get("/invoices", response_model=list[InvoiceOut])
async def list_invoices(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> list[Any]:
    """List invoices for current tenant."""
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    svc = BillingService(session)
    return await svc.get_invoices_for_tenant(tenant_id)


@router.post("/invoices/{invoice_id}/pay")
async def pay_invoice(
    invoice_id: str,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    """Generate payment link for an invoice."""
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    # Get invoice
    from db.models_subscription import InvoiceRecord
    invoice = await session.get(InvoiceRecord, invoice_id)
    if invoice is None or invoice.tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")

    # Create Moyasar payment link
    link = await create_moyasar_payment_link(
        PaymentLinkRequest.model_validate(
            {
                "amount_halalas": int(invoice.total_sar * 100),
                "customer_name": getattr(current_user, "name", "Dealix Customer") or "Dealix Customer",
                "customer_email": getattr(current_user, "email", "") or "",
                "callback_url": "/api/v1/webhooks/moyasar",
                "description": f"Dealix Invoice {invoice.invoice_number}",
            }
        )  # type: ignore[arg-type]
    )

    invoice.payment_link_id = link.invoice_id
    invoice.payment_link_url = link.payment_url
    await session.commit()

    return {
        "payment_url": link.payment_url,
        "invoice_id": invoice_id,
    }


@router.get("/features")
async def list_features(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, bool]:
    """List all features enabled for current tenant."""
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    svc = BillingService(session)
    return await svc.list_features_for_tenant(tenant_id)
