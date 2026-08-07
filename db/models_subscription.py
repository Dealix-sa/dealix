"""
Subscription & Billing models for SaaS self-serve.
نماذج الاشتراكات والفوترة للـ SaaS الذاتي.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.utils import utcnow
from db.models import Base


class PlanRecord(Base):
    """
    Canonical SaaS plan definition — the single source of truth for pricing.
    ت definición خطة SaaS الأساسية — مصدر الحقيقة الوحيد للتسعير.
    """

    __tablename__ = "plans"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name_ar: Mapped[str] = mapped_column(String(128), default="")
    name_en: Mapped[str] = mapped_column(String(128), default="")
    slug: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    # Pricing
    price_sar_monthly: Mapped[float] = mapped_column(Float, default=0.0)
    price_sar_yearly: Mapped[float | None] = mapped_column(Float, nullable=True)
    yearly_discount_pct: Mapped[float] = mapped_column(Float, default=0.0)
    # Limits
    max_users: Mapped[int] = mapped_column(Integer, default=1)
    max_leads_per_month: Mapped[int] = mapped_column(Integer, default=0)
    max_storage_gb: Mapped[float] = mapped_column(Float, default=0.0)
    max_api_calls_per_month: Mapped[int] = mapped_column(Integer, default=0)
    # Feature flags enabled for this plan
    features: Mapped[dict] = mapped_column(JSON, default=dict)
    # e.g. {"crm": true, "projects": true, "hr": false, "inventory": false}
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class SubscriptionRecord(Base):
    """
    One row per tenant subscription.
    صف واحد لكل اشتراك مستأجر.
    """

    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), index=True
    )
    plan_id: Mapped[str] = mapped_column(ForeignKey("plans.id"), index=True)
    # Billing cycle
    billing_cycle: Mapped[str] = mapped_column(String(16), default="monthly")
    # monthly | yearly
    status: Mapped[str] = mapped_column(String(32), default="trialing", index=True)
    # trialing | active | past_due | cancelled | paused
    # Trial
    trial_ends_at: Mapped[datetime | None] = mapped_column(nullable=True)
    trial_extended_days: Mapped[int] = mapped_column(Integer, default=0)
    # Current period
    current_period_start: Mapped[datetime] = mapped_column(default=utcnow)
    current_period_end: Mapped[datetime] = mapped_column(default=utcnow)
    # Cancellation
    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, default=False)
    cancelled_at: Mapped[datetime | None] = mapped_column(nullable=True)
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Payment method
    default_payment_method_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # Metrics
    mrr_sar: Mapped[float] = mapped_column(Float, default=0.0)
    total_invoiced_sar: Mapped[float] = mapped_column(Float, default=0.0)
    total_paid_sar: Mapped[float] = mapped_column(Float, default=0.0)
    # Seat management
    seat_count: Mapped[int] = mapped_column(Integer, default=1)
    seat_overrides: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_subscriptions_tenant_status", "tenant_id", "status"),
    )


class InvoiceRecord(Base):
    """
    SaaS recurring invoice — separate from ZATCA e-invoice.
    فاتورة دورية SaaS — منفصلة عن فاتورة ZATCA.
    """

    __tablename__ = "invoices"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    subscription_id: Mapped[str | None] = mapped_column(
        ForeignKey("subscriptions.id"), nullable=True, index=True
    )
    # Invoice details
    invoice_number: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    # draft | open | paid | void | uncollectible
    currency: Mapped[str] = mapped_column(String(8), default="SAR")
    subtotal_sar: Mapped[float] = mapped_column(Float, default=0.0)
    vat_amount_sar: Mapped[float] = mapped_column(Float, default=0.0)
    discount_sar: Mapped[float] = mapped_column(Float, default=0.0)
    total_sar: Mapped[float] = mapped_column(Float, default=0.0)
    # Line items (JSON array of dicts)
    line_items: Mapped[list] = mapped_column(JSON, default=list)
    # e.g. [{"description": "Growth Plan - monthly", "amount": 599.0, "quantity": 1}]
    # Due date
    due_date: Mapped[datetime | None] = mapped_column(nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(nullable=True)
    paid_amount_sar: Mapped[float] = mapped_column(Float, default=0.0)
    # Payment link (Moyasar)
    payment_link_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    payment_link_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    # ZATCA e-invoice relation
    zatca_invoice_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Metadata
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    meta_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_invoices_tenant_status", "tenant_id", "status"),
        Index("ix_invoices_due_date", "due_date"),
    )


class FeatureFlagRecord(Base):
    """
    Feature flags per tenant — can override plan defaults.
    مفاتيح الميزات لكل مستأجر — يمكن أن تتجاوz defaults الخطة.
    """

    __tablename__ = "feature_flags"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    feature_key: Mapped[str] = mapped_column(String(64), index=True)
    # e.g. "crm", "projects", "hr", "inventory", "api_access"
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    source: Mapped[str] = mapped_column(String(32), default="plan")
    # plan | manual_override | trial | addon
    expires_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        UniqueConstraint("tenant_id", "feature_key", name="uq_feature_flag_tenant_key"),
    )


class UsageRecord(Base):
    """
    Metered usage tracking per tenant.
    تتبع الاستهلاك لكل مستأجر.
    """

    __tablename__ = "usage_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    metric_name: Mapped[str] = mapped_column(String(64), index=True)
    # leads, api_calls, storage_gb, messages, documents
    period_start: Mapped[datetime] = mapped_column(index=True)
    period_end: Mapped[datetime] = mapped_column(index=True)
    quantity_used: Mapped[float] = mapped_column(Float, default=0.0)
    quantity_limit: Mapped[float] = mapped_column(Float, default=0.0)
    overage_quantity: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (
        Index("ix_usage_tenant_metric_period", "tenant_id", "metric_name", "period_start"),
    )
