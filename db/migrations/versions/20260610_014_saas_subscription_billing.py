"""
Add SaaS subscription billing tables.

Revision ID: 20260610_014_saas_subscription_billing
Revises: 013
Create Date: 2026-06-10 08:52:33
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260610_014_saas_subscription_billing"
down_revision: Union[str, None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Plans ──────────────────────────────────────────────────────
    op.create_table(
        "plans",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name_ar", sa.String(128), default=""),
        sa.Column("name_en", sa.String(128), default=""),
        sa.Column("slug", sa.String(32), unique=True, index=True),
        sa.Column("price_sar_monthly", sa.Float, default=0.0),
        sa.Column("price_sar_yearly", sa.Float, nullable=True),
        sa.Column("yearly_discount_pct", sa.Float, default=0.0),
        sa.Column("max_users", sa.Integer, default=1),
        sa.Column("max_leads_per_month", sa.Integer, default=0),
        sa.Column("max_storage_gb", sa.Float, default=0.0),
        sa.Column("max_api_calls_per_month", sa.Integer, default=0),
        sa.Column("features", postgresql.JSONB, default=dict),
        sa.Column("is_public", sa.Boolean, default=True),
        sa.Column("is_custom", sa.Boolean, default=False),
        sa.Column("sort_order", sa.Integer, default=0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), onupdate=sa.text("now()")),
    )

    # ── Subscriptions ──────────────────────────────────────────────
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), sa.ForeignKey("tenants.id", ondelete="CASCADE"), index=True),
        sa.Column("plan_id", sa.String(64), sa.ForeignKey("plans.id"), index=True),
        sa.Column("billing_cycle", sa.String(16), default="monthly"),
        sa.Column("status", sa.String(32), default="trialing", index=True),
        sa.Column("trial_ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("trial_extended_days", sa.Integer, default=0),
        sa.Column("current_period_start", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("current_period_end", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("cancel_at_period_end", sa.Boolean, default=False),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancellation_reason", sa.Text, nullable=True),
        sa.Column("default_payment_method_id", sa.String(128), nullable=True),
        sa.Column("mrr_sar", sa.Float, default=0.0),
        sa.Column("total_invoiced_sar", sa.Float, default=0.0),
        sa.Column("total_paid_sar", sa.Float, default=0.0),
        sa.Column("seat_count", sa.Integer, default=1),
        sa.Column("seat_overrides", postgresql.JSONB, default=dict),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), onupdate=sa.text("now()")),
    )
    op.create_index("ix_subscriptions_tenant_status", "subscriptions", ["tenant_id", "status"])

    # ── Invoices ───────────────────────────────────────────────────
    op.create_table(
        "invoices",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), sa.ForeignKey("tenants.id"), index=True),
        sa.Column("subscription_id", sa.String(64), sa.ForeignKey("subscriptions.id"), nullable=True, index=True),
        sa.Column("invoice_number", sa.String(64), unique=True, index=True),
        sa.Column("status", sa.String(32), default="draft", index=True),
        sa.Column("currency", sa.String(8), default="SAR"),
        sa.Column("subtotal_sar", sa.Float, default=0.0),
        sa.Column("vat_amount_sar", sa.Float, default=0.0),
        sa.Column("discount_sar", sa.Float, default=0.0),
        sa.Column("total_sar", sa.Float, default=0.0),
        sa.Column("line_items", postgresql.JSONB, default=list),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("paid_amount_sar", sa.Float, default=0.0),
        sa.Column("payment_link_id", sa.String(128), nullable=True),
        sa.Column("payment_link_url", sa.String(512), nullable=True),
        sa.Column("zatca_invoice_id", sa.String(64), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("metadata", postgresql.JSONB, default=dict),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), onupdate=sa.text("now()")),
    )
    op.create_index("ix_invoices_tenant_status", "invoices", ["tenant_id", "status"])
    op.create_index("ix_invoices_due_date", "invoices", ["due_date"])

    # ── Feature Flags ──────────────────────────────────────────────
    op.create_table(
        "feature_flags",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), sa.ForeignKey("tenants.id"), index=True),
        sa.Column("feature_key", sa.String(64), index=True),
        sa.Column("enabled", sa.Boolean, default=False),
        sa.Column("source", sa.String(32), default="plan"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), onupdate=sa.text("now()")),
    )
    op.create_unique_constraint("uq_feature_flag_tenant_key", "feature_flags", ["tenant_id", "feature_key"])

    # ── Usage Records ──────────────────────────────────────────────
    op.create_table(
        "usage_records",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), sa.ForeignKey("tenants.id"), index=True),
        sa.Column("metric_name", sa.String(64), index=True),
        sa.Column("period_start", sa.DateTime(timezone=True), index=True),
        sa.Column("period_end", sa.DateTime(timezone=True), index=True),
        sa.Column("quantity_used", sa.Float, default=0.0),
        sa.Column("quantity_limit", sa.Float, default=0.0),
        sa.Column("overage_quantity", sa.Float, default=0.0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), onupdate=sa.text("now()")),
    )
    op.create_index("ix_usage_tenant_metric_period", "usage_records", ["tenant_id", "metric_name", "period_start"])

    # ── Seed default plans ─────────────────────────────────────────
    op.execute("""
        INSERT INTO plans (id, slug, name_ar, name_en, price_sar_monthly, max_users, max_leads_per_month, max_storage_gb, max_api_calls_per_month, features, sort_order)
        VALUES
        ('plan_free', 'free', 'مجاني', 'Free', 0, 1, 50, 1, 100, '{\"crm\": true, \"projects\": false, \"support\": false, \"documents\": false, \"hr\": false, \"inventory\": false, \"finance\": false, \"api_access\": false}', 1),
        ('plan_starter', 'starter', 'بداية', 'Starter', 199, 3, 500, 10, 10000, '{\"crm\": true, \"projects\": true, \"support\": true, \"documents\": true, \"hr\": false, \"inventory\": false, \"finance\": false, \"api_access\": false}', 2),
        ('plan_growth', 'growth', 'نمو', 'Growth', 599, 10, 5000, 50, 50000, '{\"crm\": true, \"projects\": true, \"support\": true, \"documents\": true, \"hr\": true, \"inventory\": true, \"finance\": true, \"api_access\": true}', 3),
        ('plan_scale', 'scale', 'توسع', 'Scale', 1499, 25, 20000, 200, 200000, '{\"crm\": true, \"projects\": true, \"support\": true, \"documents\": true, \"hr\": true, \"inventory\": true, \"finance\": true, \"api_access\": true, \"advanced_reports\": true, \"white_label\": false}', 4),
        ('plan_enterprise', 'enterprise', 'مؤسسي', 'Enterprise', 0, 9999, 999999, 9999, 9999999, '{\"crm\": true, \"projects\": true, \"support\": true, \"documents\": true, \"hr\": true, \"inventory\": true, \"finance\": true, \"api_access\": true, \"advanced_reports\": true, \"white_label\": true, \"dedicated_support\": true}', 5)
    """)


def downgrade() -> None:
    op.drop_table("usage_records")
    op.drop_table("feature_flags")
    op.drop_table("invoices")
    op.drop_table("subscriptions")
    op.drop_table("plans")
