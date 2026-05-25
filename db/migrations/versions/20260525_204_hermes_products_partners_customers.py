"""Hermes products / partners / customers tables (Section 56 / Migration 004).

Offers, product lines, partners, partner revenue, customers,
customer health, value reports.

Revision ID: 204
Revises: 203
Create Date: 2026-05-25
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "204"
down_revision: Union[str, Sequence[str], None] = "203"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hermes_product_lines",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("owner", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_product_lines_status", "hermes_product_lines", ["status"])

    op.create_table(
        "hermes_offers",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "product_line_id",
            sa.String(64),
            sa.ForeignKey("hermes_product_lines.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("buyer", sa.Text(), nullable=True),
        sa.Column("pain", sa.Text(), nullable=True),
        sa.Column("promise", sa.Text(), nullable=True),
        sa.Column(
            "deliverables",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("price_min_sar", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("price_max_sar", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("entry_cta", sa.Text(), nullable=True),
        sa.Column("upsell", sa.Text(), nullable=True),
        sa.Column(
            "trust_risks",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("outcome_metric", sa.Text(), nullable=True),
        sa.Column(
            "delivery_checklist",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("proof_hypothesis", sa.Text(), nullable=True),
        sa.Column("case_study_url", sa.Text(), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="draft"),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_offers_status", "hermes_offers", ["status"])
    op.create_index("ix_hermes_offers_product_line", "hermes_offers", ["product_line_id"])

    op.create_table(
        "hermes_partners",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("contact_email", sa.Text(), nullable=True),
        sa.Column("revenue_share_pct", sa.Numeric(5, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_partners_kind", "hermes_partners", ["kind"])
    op.create_index("ix_hermes_partners_status", "hermes_partners", ["status"])

    op.create_table(
        "hermes_partner_revenue",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "partner_id",
            sa.String(64),
            sa.ForeignKey("hermes_partners.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("offer_id", sa.String(64), nullable=True),
        sa.Column("customer_id", sa.String(64), nullable=True),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column(
            "amount_sar",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "partner_share_sar",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("settled_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_hermes_partner_revenue_partner",
        "hermes_partner_revenue",
        ["partner_id"],
    )
    op.create_index(
        "ix_hermes_partner_revenue_offer",
        "hermes_partner_revenue",
        ["offer_id"],
    )
    op.create_index(
        "ix_hermes_partner_revenue_customer",
        "hermes_partner_revenue",
        ["customer_id"],
    )
    op.create_index(
        "ix_hermes_partner_revenue_status",
        "hermes_partner_revenue",
        ["status"],
    )

    op.create_table(
        "hermes_customers",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("sector", sa.String(64), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="prospect"),
        sa.Column("icp_id", sa.String(64), nullable=True),
        sa.Column("primary_contact", sa.Text(), nullable=True),
        sa.Column("locale", sa.String(8), nullable=False, server_default="ar"),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("onboarded_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_customers_status", "hermes_customers", ["status"])
    op.create_index("ix_hermes_customers_sector", "hermes_customers", ["sector"])

    op.create_table(
        "hermes_customer_health",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "customer_id",
            sa.String(64),
            sa.ForeignKey("hermes_customers.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("score", sa.Numeric(5, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("status", sa.String(32), nullable=False, server_default="unknown"),
        sa.Column("renewal_risk", sa.String(16), nullable=False, server_default="unknown"),
        sa.Column("adoption_tier", sa.String(32), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("measured_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_hermes_customer_health_customer",
        "hermes_customer_health",
        ["customer_id"],
    )
    op.create_index(
        "ix_hermes_customer_health_status",
        "hermes_customer_health",
        ["status"],
    )
    op.create_index(
        "ix_hermes_customer_health_created_at",
        "hermes_customer_health",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_value_reports",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "customer_id",
            sa.String(64),
            sa.ForeignKey("hermes_customers.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("period", sa.String(32), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False, server_default="monthly"),
        sa.Column(
            "total_value_sar",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "verified_value_sar",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column("status", sa.String(32), nullable=False, server_default="draft"),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("generated_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("sent_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "customer_id",
            "period",
            "kind",
            name="uq_hermes_value_reports_customer_period_kind",
        ),
    )
    op.create_index(
        "ix_hermes_value_reports_customer",
        "hermes_value_reports",
        ["customer_id"],
    )
    op.create_index(
        "ix_hermes_value_reports_status",
        "hermes_value_reports",
        ["status"],
    )
    op.create_index(
        "ix_hermes_value_reports_created_at",
        "hermes_value_reports",
        [sa.text("created_at DESC")],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_hermes_value_reports_created_at",
        table_name="hermes_value_reports",
    )
    op.drop_index("ix_hermes_value_reports_status", table_name="hermes_value_reports")
    op.drop_index(
        "ix_hermes_value_reports_customer",
        table_name="hermes_value_reports",
    )
    op.drop_table("hermes_value_reports")

    op.drop_index(
        "ix_hermes_customer_health_created_at",
        table_name="hermes_customer_health",
    )
    op.drop_index(
        "ix_hermes_customer_health_status",
        table_name="hermes_customer_health",
    )
    op.drop_index(
        "ix_hermes_customer_health_customer",
        table_name="hermes_customer_health",
    )
    op.drop_table("hermes_customer_health")

    op.drop_index("ix_hermes_customers_sector", table_name="hermes_customers")
    op.drop_index("ix_hermes_customers_status", table_name="hermes_customers")
    op.drop_table("hermes_customers")

    op.drop_index(
        "ix_hermes_partner_revenue_status",
        table_name="hermes_partner_revenue",
    )
    op.drop_index(
        "ix_hermes_partner_revenue_customer",
        table_name="hermes_partner_revenue",
    )
    op.drop_index(
        "ix_hermes_partner_revenue_offer",
        table_name="hermes_partner_revenue",
    )
    op.drop_index(
        "ix_hermes_partner_revenue_partner",
        table_name="hermes_partner_revenue",
    )
    op.drop_table("hermes_partner_revenue")

    op.drop_index("ix_hermes_partners_status", table_name="hermes_partners")
    op.drop_index("ix_hermes_partners_kind", table_name="hermes_partners")
    op.drop_table("hermes_partners")

    op.drop_index("ix_hermes_offers_product_line", table_name="hermes_offers")
    op.drop_index("ix_hermes_offers_status", table_name="hermes_offers")
    op.drop_table("hermes_offers")

    op.drop_index("ix_hermes_product_lines_status", table_name="hermes_product_lines")
    op.drop_table("hermes_product_lines")
