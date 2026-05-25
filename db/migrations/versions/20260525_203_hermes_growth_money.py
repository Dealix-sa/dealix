"""Hermes growth + money tables (Section 56 / Migration 003).

Growth campaigns, leads, touches, experiments, attribution, revenue
events, deal rooms, invoices.

Revision ID: 203
Revises: 202
Create Date: 2026-05-25
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "203"
down_revision: Union[str, Sequence[str], None] = "202"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hermes_growth_campaigns",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="draft"),
        sa.Column("owner", sa.String(64), nullable=False),
        sa.Column("offer_id", sa.String(64), nullable=True),
        sa.Column("icp_id", sa.String(64), nullable=True),
        sa.Column("hypothesis", sa.Text(), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("ended_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_hermes_growth_campaigns_offer",
        "hermes_growth_campaigns",
        ["offer_id"],
    )
    op.create_index(
        "ix_hermes_growth_campaigns_status",
        "hermes_growth_campaigns",
        ["status"],
    )
    op.create_index(
        "ix_hermes_growth_campaigns_kind",
        "hermes_growth_campaigns",
        ["kind"],
    )

    op.create_table(
        "hermes_growth_leads",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "campaign_id",
            sa.String(64),
            sa.ForeignKey("hermes_growth_campaigns.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("customer_id", sa.String(64), nullable=True),
        sa.Column("source", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="new"),
        sa.Column("score", sa.Numeric(5, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_growth_leads_customer", "hermes_growth_leads", ["customer_id"])
    op.create_index("ix_hermes_growth_leads_status", "hermes_growth_leads", ["status"])
    op.create_index("ix_hermes_growth_leads_campaign", "hermes_growth_leads", ["campaign_id"])

    op.create_table(
        "hermes_growth_touches",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "lead_id",
            sa.String(64),
            sa.ForeignKey("hermes_growth_leads.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("channel", sa.String(32), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="drafted"),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("sent_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_growth_touches_lead", "hermes_growth_touches", ["lead_id"])
    op.create_index("ix_hermes_growth_touches_kind", "hermes_growth_touches", ["kind"])
    op.create_index(
        "ix_hermes_growth_touches_created_at",
        "hermes_growth_touches",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_growth_experiments",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "campaign_id",
            sa.String(64),
            sa.ForeignKey("hermes_growth_campaigns.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("hypothesis", sa.Text(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="planned"),
        sa.Column("variant", sa.String(64), nullable=True),
        sa.Column("metric", sa.String(64), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("ended_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_hermes_growth_experiments_campaign",
        "hermes_growth_experiments",
        ["campaign_id"],
    )
    op.create_index(
        "ix_hermes_growth_experiments_status",
        "hermes_growth_experiments",
        ["status"],
    )

    op.create_table(
        "hermes_growth_attribution",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "lead_id",
            sa.String(64),
            sa.ForeignKey("hermes_growth_leads.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "campaign_id",
            sa.String(64),
            sa.ForeignKey("hermes_growth_campaigns.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("customer_id", sa.String(64), nullable=True),
        sa.Column("offer_id", sa.String(64), nullable=True),
        sa.Column("model", sa.String(32), nullable=False, server_default="first_touch"),
        sa.Column("weight", sa.Numeric(5, 4), nullable=False, server_default=sa.text("1.0")),
        sa.Column(
            "attributed_sar",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("attributed_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_hermes_growth_attribution_customer",
        "hermes_growth_attribution",
        ["customer_id"],
    )
    op.create_index(
        "ix_hermes_growth_attribution_offer",
        "hermes_growth_attribution",
        ["offer_id"],
    )
    op.create_index(
        "ix_hermes_growth_attribution_campaign",
        "hermes_growth_attribution",
        ["campaign_id"],
    )

    op.create_table(
        "hermes_revenue_events",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("customer_id", sa.String(64), nullable=True),
        sa.Column("offer_id", sa.String(64), nullable=True),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("tier", sa.String(32), nullable=False),
        sa.Column(
            "amount_sar",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column("source_ref", sa.Text(), nullable=True),
        sa.Column("confirmation_ref", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("occurred_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_revenue_events_customer", "hermes_revenue_events", ["customer_id"])
    op.create_index("ix_hermes_revenue_events_offer", "hermes_revenue_events", ["offer_id"])
    op.create_index("ix_hermes_revenue_events_kind", "hermes_revenue_events", ["kind"])
    op.create_index(
        "ix_hermes_revenue_events_created_at",
        "hermes_revenue_events",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_deal_rooms",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("customer_id", sa.String(64), nullable=False),
        sa.Column("offer_id", sa.String(64), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="open"),
        sa.Column("stage", sa.String(64), nullable=True),
        sa.Column("owner", sa.String(64), nullable=True),
        sa.Column(
            "expected_value_sar",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("opened_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("closed_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_deal_rooms_customer", "hermes_deal_rooms", ["customer_id"])
    op.create_index("ix_hermes_deal_rooms_offer", "hermes_deal_rooms", ["offer_id"])
    op.create_index("ix_hermes_deal_rooms_status", "hermes_deal_rooms", ["status"])

    op.create_table(
        "hermes_invoices",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("customer_id", sa.String(64), nullable=False),
        sa.Column("offer_id", sa.String(64), nullable=True),
        sa.Column(
            "deal_room_id",
            sa.String(64),
            sa.ForeignKey("hermes_deal_rooms.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("status", sa.String(32), nullable=False, server_default="draft"),
        sa.Column(
            "amount_sar",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column("currency", sa.String(8), nullable=False, server_default="SAR"),
        sa.Column("external_ref", sa.Text(), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("issued_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("paid_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("due_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_invoices_customer", "hermes_invoices", ["customer_id"])
    op.create_index("ix_hermes_invoices_offer", "hermes_invoices", ["offer_id"])
    op.create_index("ix_hermes_invoices_status", "hermes_invoices", ["status"])
    op.create_index(
        "ix_hermes_invoices_created_at",
        "hermes_invoices",
        [sa.text("created_at DESC")],
    )


def downgrade() -> None:
    op.drop_index("ix_hermes_invoices_created_at", table_name="hermes_invoices")
    op.drop_index("ix_hermes_invoices_status", table_name="hermes_invoices")
    op.drop_index("ix_hermes_invoices_offer", table_name="hermes_invoices")
    op.drop_index("ix_hermes_invoices_customer", table_name="hermes_invoices")
    op.drop_table("hermes_invoices")

    op.drop_index("ix_hermes_deal_rooms_status", table_name="hermes_deal_rooms")
    op.drop_index("ix_hermes_deal_rooms_offer", table_name="hermes_deal_rooms")
    op.drop_index("ix_hermes_deal_rooms_customer", table_name="hermes_deal_rooms")
    op.drop_table("hermes_deal_rooms")

    op.drop_index(
        "ix_hermes_revenue_events_created_at",
        table_name="hermes_revenue_events",
    )
    op.drop_index("ix_hermes_revenue_events_kind", table_name="hermes_revenue_events")
    op.drop_index("ix_hermes_revenue_events_offer", table_name="hermes_revenue_events")
    op.drop_index(
        "ix_hermes_revenue_events_customer",
        table_name="hermes_revenue_events",
    )
    op.drop_table("hermes_revenue_events")

    op.drop_index(
        "ix_hermes_growth_attribution_campaign",
        table_name="hermes_growth_attribution",
    )
    op.drop_index(
        "ix_hermes_growth_attribution_offer",
        table_name="hermes_growth_attribution",
    )
    op.drop_index(
        "ix_hermes_growth_attribution_customer",
        table_name="hermes_growth_attribution",
    )
    op.drop_table("hermes_growth_attribution")

    op.drop_index(
        "ix_hermes_growth_experiments_status",
        table_name="hermes_growth_experiments",
    )
    op.drop_index(
        "ix_hermes_growth_experiments_campaign",
        table_name="hermes_growth_experiments",
    )
    op.drop_table("hermes_growth_experiments")

    op.drop_index(
        "ix_hermes_growth_touches_created_at",
        table_name="hermes_growth_touches",
    )
    op.drop_index("ix_hermes_growth_touches_kind", table_name="hermes_growth_touches")
    op.drop_index("ix_hermes_growth_touches_lead", table_name="hermes_growth_touches")
    op.drop_table("hermes_growth_touches")

    op.drop_index("ix_hermes_growth_leads_campaign", table_name="hermes_growth_leads")
    op.drop_index("ix_hermes_growth_leads_status", table_name="hermes_growth_leads")
    op.drop_index("ix_hermes_growth_leads_customer", table_name="hermes_growth_leads")
    op.drop_table("hermes_growth_leads")

    op.drop_index("ix_hermes_growth_campaigns_kind", table_name="hermes_growth_campaigns")
    op.drop_index(
        "ix_hermes_growth_campaigns_status",
        table_name="hermes_growth_campaigns",
    )
    op.drop_index(
        "ix_hermes_growth_campaigns_offer",
        table_name="hermes_growth_campaigns",
    )
    op.drop_table("hermes_growth_campaigns")
