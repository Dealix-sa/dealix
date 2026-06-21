"""
Billing Service — subscription lifecycle, invoicing, proration.
خدمة الفوترة — دورة حياة الاشتراك، الفواتير، التناسب.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models_subscription import (
    FeatureFlagRecord,
    InvoiceRecord,
    PlanRecord,
    SubscriptionRecord,
    UsageRecord,
)
from db.models import TenantRecord
from core.utils import utcnow


PLAN_DEFAULTS: dict[str, dict[str, Any]] = {
    "free": {"trial_days": 0, "can_trial": False},
    "starter": {"trial_days": 14, "can_trial": True},
    "growth": {"trial_days": 14, "can_trial": True},
    "scale": {"trial_days": 14, "can_trial": True},
    "enterprise": {"trial_days": 30, "can_trial": True},
}


class BillingService:
    """
    Central billing orchestrator for Dealix SaaS.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    # ── Plans ──────────────────────────────────────────────────────

    async def list_plans(self, include_custom: bool = False) -> list[PlanRecord]:
        stmt = select(PlanRecord).where(PlanRecord.is_public == True)
        if not include_custom:
            stmt = stmt.where(PlanRecord.is_custom == False)
        stmt = stmt.order_by(PlanRecord.sort_order)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_plan(self, plan_id: str) -> PlanRecord | None:
        return await self.session.get(PlanRecord, plan_id)

    async def get_plan_by_slug(self, slug: str) -> PlanRecord | None:
        stmt = select(PlanRecord).where(PlanRecord.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # ── Subscriptions ──────────────────────────────────────────────

    async def create_subscription(
        self,
        tenant_id: str,
        plan_id: str,
        billing_cycle: str = "monthly",
        seat_count: int = 1,
    ) -> SubscriptionRecord:
        plan = await self.get_plan(plan_id)
        if plan is None:
            raise ValueError(f"Plan {plan_id} not found")

        trial_days = PLAN_DEFAULTS.get(plan.slug, {}).get("trial_days", 14)
        now = utcnow()
        trial_ends = now + timedelta(days=trial_days) if trial_days > 0 else None

        if billing_cycle == "yearly" and plan.price_sar_yearly:
            mrr = plan.price_sar_yearly / 12
        else:
            mrr = plan.price_sar_monthly

        sub = SubscriptionRecord(
            id=f"sub_{uuid.uuid4().hex[:16]}",
            tenant_id=tenant_id,
            plan_id=plan_id,
            billing_cycle=billing_cycle,
            status="trialing" if trial_days > 0 else "active",
            trial_ends_at=trial_ends,
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
            seat_count=seat_count,
            mrr_sar=mrr,
        )
        self.session.add(sub)
        await self.session.flush()

        # Sync feature flags from plan
        await self._sync_feature_flags(tenant_id, plan)
        return sub

    async def _sync_feature_flags(self, tenant_id: str, plan: PlanRecord) -> None:
        # Remove old plan-sourced flags
        stmt = select(FeatureFlagRecord).where(
            FeatureFlagRecord.tenant_id == tenant_id,
            FeatureFlagRecord.source == "plan",
        )
        result = await self.session.execute(stmt)
        for old in result.scalars().all():
            await self.session.delete(old)

        # Insert new flags from plan.features
        features: dict = plan.features or {}
        for key, enabled in features.items():
            ff = FeatureFlagRecord(
                id=f"ff_{uuid.uuid4().hex[:12]}",
                tenant_id=tenant_id,
                feature_key=key,
                enabled=bool(enabled),
                source="plan",
            )
            self.session.add(ff)

    async def get_subscription(self, subscription_id: str) -> SubscriptionRecord | None:
        return await self.session.get(SubscriptionRecord, subscription_id)

    async def get_active_subscription_for_tenant(
        self, tenant_id: str
    ) -> SubscriptionRecord | None:
        stmt = (
            select(SubscriptionRecord)
            .where(
                SubscriptionRecord.tenant_id == tenant_id,
                SubscriptionRecord.status.in_(["trialing", "active", "past_due"]),
            )
            .order_by(SubscriptionRecord.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def upgrade_subscription(
        self, subscription_id: str, new_plan_id: str, new_cycle: str | None = None
    ) -> SubscriptionRecord:
        sub = await self.get_subscription(subscription_id)
        if sub is None:
            raise ValueError("Subscription not found")

        old_plan = await self.get_plan(sub.plan_id)
        new_plan = await self.get_plan(new_plan_id)
        if new_plan is None:
            raise ValueError("New plan not found")

        # Proration
        now = utcnow()
        days_remaining = (sub.current_period_end - now).days
        total_days = (sub.current_period_end - sub.current_period_start).days or 30

        old_mrr = sub.mrr_sar
        new_mrr = new_plan.price_sar_yearly / 12 if new_cycle == "yearly" and new_plan.price_sar_yearly else new_plan.price_sar_monthly

        proration_credit = (old_mrr / 30) * days_remaining if old_mrr else 0
        proration_charge = (new_mrr / 30) * days_remaining if new_mrr else 0
        proration_adjustment = proration_charge - proration_credit

        # Create proration invoice if charge > 0
        if proration_adjustment > 0:
            await self._create_invoice(
                tenant_id=sub.tenant_id,
                subscription_id=sub.id,
                line_items=[
                    {
                        "description": f"Proration: {old_plan.name_en} → {new_plan.name_en}",
                        "amount": round(proration_adjustment, 2),
                        "quantity": 1,
                    }
                ],
                total_sar=round(proration_adjustment * 1.15, 2),
                due_date=now,
            )

        # Update subscription
        sub.plan_id = new_plan_id
        sub.billing_cycle = new_cycle or sub.billing_cycle
        sub.mrr_sar = new_mrr
        sub.updated_at = now

        # Sync feature flags
        await self._sync_feature_flags(sub.tenant_id, new_plan)
        await self.session.flush()
        return sub

    async def cancel_subscription(
        self, subscription_id: str, reason: str | None = None, immediate: bool = False
    ) -> SubscriptionRecord:
        sub = await self.get_subscription(subscription_id)
        if sub is None:
            raise ValueError("Subscription not found")

        now = utcnow()
        if immediate:
            sub.status = "cancelled"
            sub.cancelled_at = now
        else:
            sub.cancel_at_period_end = True
        sub.cancellation_reason = reason or sub.cancellation_reason
        sub.updated_at = now
        await self.session.flush()
        return sub

    # ── Invoicing ──────────────────────────────────────────────────

    async def _create_invoice(
        self,
        tenant_id: str,
        subscription_id: str | None,
        line_items: list[dict],
        total_sar: float,
        due_date: datetime | None = None,
    ) -> InvoiceRecord:
        now = utcnow()
        subtotal = sum(item.get("amount", 0) * item.get("quantity", 1) for item in line_items)
        vat = round(subtotal * 0.15, 2)
        inv = InvoiceRecord(
            id=f"inv_{uuid.uuid4().hex[:16]}",
            tenant_id=tenant_id,
            subscription_id=subscription_id,
            invoice_number=f"DEALIX-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}",
            status="open",
            subtotal_sar=subtotal,
            vat_amount_sar=vat,
            total_sar=subtotal + vat,
            line_items=line_items,
            due_date=due_date or now + timedelta(days=7),
            created_at=now,
            updated_at=now,
        )
        self.session.add(inv)
        await self.session.flush()
        return inv

    async def generate_recurring_invoice(self, subscription_id: str) -> InvoiceRecord | None:
        sub = await self.get_subscription(subscription_id)
        if sub is None or sub.status not in ("active", "trialing"):
            return None

        plan = await self.get_plan(sub.plan_id)
        if plan is None:
            return None

        now = utcnow()
        period_label = now.strftime("%B %Y")
        line_items = [
            {
                "description": f"{plan.name_en} Plan — {period_label}",
                "amount": sub.mrr_sar,
                "quantity": 1,
            }
        ]

        # Add seat overages
        if sub.seat_count > plan.max_users:
            extra_seats = sub.seat_count - plan.max_users
            seat_price = 49.0  # SAR per extra seat
            line_items.append({
                "description": f"Extra seats ({extra_seats})",
                "amount": seat_price,
                "quantity": extra_seats,
            })

        total = sum(item["amount"] * item["quantity"] for item in line_items)
        inv = await self._create_invoice(
            tenant_id=sub.tenant_id,
            subscription_id=sub.id,
            line_items=line_items,
            total_sar=round(total, 2),
            due_date=now + timedelta(days=7),
        )

        # Advance period
        sub.current_period_start = now
        sub.current_period_end = now + timedelta(days=30)
        sub.total_invoiced_sar += inv.total_sar
        await self.session.flush()
        return inv

    async def get_invoices_for_tenant(self, tenant_id: str) -> list[InvoiceRecord]:
        stmt = (
            select(InvoiceRecord)
            .where(InvoiceRecord.tenant_id == tenant_id)
            .order_by(InvoiceRecord.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ── Feature Gating ─────────────────────────────────────────────

    async def is_feature_enabled(self, tenant_id: str, feature_key: str) -> bool:
        stmt = select(FeatureFlagRecord).where(
            FeatureFlagRecord.tenant_id == tenant_id,
            FeatureFlagRecord.feature_key == feature_key,
        )
        result = await self.session.execute(stmt)
        ff = result.scalar_one_or_none()
        if ff is None:
            return False
        if ff.expires_at and ff.expires_at < utcnow():
            return False
        return ff.enabled

    async def list_features_for_tenant(self, tenant_id: str) -> dict[str, bool]:
        stmt = select(FeatureFlagRecord).where(
            FeatureFlagRecord.tenant_id == tenant_id,
        )
        result = await self.session.execute(stmt)
        out: dict[str, bool] = {}
        for ff in result.scalars().all():
            if ff.expires_at and ff.expires_at < utcnow():
                out[ff.feature_key] = False
            else:
                out[ff.feature_key] = ff.enabled
        return out

    async def set_feature_override(
        self, tenant_id: str, feature_key: str, enabled: bool, expires_at: datetime | None = None
    ) -> FeatureFlagRecord:
        stmt = select(FeatureFlagRecord).where(
            FeatureFlagRecord.tenant_id == tenant_id,
            FeatureFlagRecord.feature_key == feature_key,
        )
        result = await self.session.execute(stmt)
        ff = result.scalar_one_or_none()
        if ff is None:
            ff = FeatureFlagRecord(
                id=f"ff_{uuid.uuid4().hex[:12]}",
                tenant_id=tenant_id,
                feature_key=feature_key,
                enabled=enabled,
                source="manual_override",
                expires_at=expires_at,
            )
            self.session.add(ff)
        else:
            ff.enabled = enabled
            ff.source = "manual_override"
            ff.expires_at = expires_at
            ff.updated_at = utcnow()
        await self.session.flush()
        return ff

    # ── Usage ──────────────────────────────────────────────────────

    async def record_usage(
        self, tenant_id: str, metric_name: str, quantity: float, period: datetime | None = None
    ) -> None:
        now = utcnow()
        period = period or now
        period_start = period.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        period_end = (period_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

        stmt = select(UsageRecord).where(
            UsageRecord.tenant_id == tenant_id,
            UsageRecord.metric_name == metric_name,
            UsageRecord.period_start == period_start,
        )
        result = await self.session.execute(stmt)
        usage = result.scalar_one_or_none()

        if usage is None:
            # Get limit from subscription plan
            sub = await self.get_active_subscription_for_tenant(tenant_id)
            limit = 0
            if sub:
                plan = await self.get_plan(sub.plan_id)
                if plan and hasattr(plan, f"max_{metric_name}"):
                    limit = getattr(plan, f"max_{metric_name}", 0) or 0

            usage = UsageRecord(
                id=f"usg_{uuid.uuid4().hex[:12]}",
                tenant_id=tenant_id,
                metric_name=metric_name,
                period_start=period_start,
                period_end=period_end,
                quantity_used=quantity,
                quantity_limit=limit,
                overage_quantity=max(0, quantity - limit),
            )
            self.session.add(usage)
        else:
            usage.quantity_used += quantity
            usage.overage_quantity = max(0, usage.quantity_used - usage.quantity_limit)
            usage.updated_at = now

        await self.session.flush()

    async def get_usage_for_tenant(self, tenant_id: str, metric_name: str) -> UsageRecord | None:
        now = utcnow()
        period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        stmt = select(UsageRecord).where(
            UsageRecord.tenant_id == tenant_id,
            UsageRecord.metric_name == metric_name,
            UsageRecord.period_start == period_start,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
