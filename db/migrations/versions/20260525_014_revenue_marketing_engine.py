"""Revenue Marketing Engine — SQL contract.

Tables backing dealix/revenue_marketing/ when the engine runs on Postgres
instead of the local JSON store. The JSON store is the source of truth in
dev/test; production may migrate via a sync job.

Revision ID: 014
Revises: 013
Create Date: 2026-05-25
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "014"
down_revision: Union[str, Sequence[str], None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rm_offers",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("name_ar", sa.Text(), nullable=False),
        sa.Column("name_en", sa.Text(), nullable=False),
        sa.Column("tier", sa.Text(), nullable=False),
        sa.Column("price_min_sar", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("price_max_sar", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("promise_ar", sa.Text(), nullable=False, server_default=""),
        sa.Column("deliverables", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("target_segments", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("primary_pain", sa.Text(), nullable=False, server_default=""),
        sa.Column("success_metric", sa.Text(), nullable=False, server_default=""),
        sa.Column("money_quality", sa.Numeric(5, 3), nullable=False, server_default="0.5"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_rm_offers_tier", "rm_offers", ["tier"])

    op.create_table(
        "rm_signals",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("summary_ar", sa.Text(), nullable=False),
        sa.Column("summary_en", sa.Text(), nullable=False, server_default=""),
        sa.Column("segment", sa.Text(), nullable=False),
        sa.Column("pain", sa.Text(), nullable=False),
        sa.Column("suggested_offer_id", sa.Text(), nullable=False, server_default=""),
        sa.Column("why_now", sa.Text(), nullable=False, server_default=""),
        sa.Column("proof_target", sa.Text(), nullable=False, server_default=""),
        sa.Column("confidence", sa.Numeric(4, 3), nullable=False, server_default="0.5"),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_rm_signals_segment", "rm_signals", ["segment"])

    op.create_table(
        "rm_campaigns",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("campaign_name", sa.Text(), nullable=False),
        sa.Column("target_segment", sa.Text(), nullable=False),
        sa.Column("offer_id", sa.Text(), nullable=False),
        sa.Column("channel", sa.Text(), nullable=False),
        sa.Column("message_angle", sa.Text(), nullable=False, server_default=""),
        sa.Column("cta_label_ar", sa.Text(), nullable=False, server_default=""),
        sa.Column("cta_path", sa.Text(), nullable=False, server_default=""),
        sa.Column("success_metric", sa.Text(), nullable=False, server_default=""),
        sa.Column("scale_kill_rule", sa.Text(), nullable=False, server_default=""),
        sa.Column("budget_sar", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("status", sa.Text(), nullable=False, server_default="draft"),
        sa.Column("signal_id", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_rm_campaigns_status", "rm_campaigns", ["status"])
    op.create_index("ix_rm_campaigns_offer", "rm_campaigns", ["offer_id"])

    op.create_table(
        "rm_marketing_touches",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("campaign_id", sa.Text(), nullable=True),
        sa.Column("lead_id", sa.Text(), nullable=True),
        sa.Column("touch_type", sa.Text(), nullable=False),
        sa.Column("channel", sa.Text(), nullable=True),
        sa.Column("content_id", sa.Text(), nullable=True),
        sa.Column("asset_id", sa.Text(), nullable=True),
        sa.Column("agent_id", sa.Text(), nullable=True),
        sa.Column("message_variant", sa.Text(), nullable=False, server_default=""),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_rm_touches_lead", "rm_marketing_touches", ["lead_id"])
    op.create_index("ix_rm_touches_campaign", "rm_marketing_touches", ["campaign_id"])
    op.create_index("ix_rm_touches_occurred", "rm_marketing_touches", ["occurred_at"])

    op.create_table(
        "rm_revenue_attribution",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("revenue_sar", sa.Numeric(14, 2), nullable=False),
        sa.Column("deal_id", sa.Text(), nullable=False),
        sa.Column("primary_source", sa.Text(), nullable=False),
        sa.Column("secondary_source", sa.Text(), nullable=False, server_default=""),
        sa.Column("campaign_id", sa.Text(), nullable=True),
        sa.Column("offer_id", sa.Text(), nullable=True),
        sa.Column("channel", sa.Text(), nullable=True),
        sa.Column("asset_ids", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("agent_ids", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("influenced_by", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("attribution_type", sa.Text(), nullable=False, server_default="multi_touch"),
        sa.Column("payment_confirmed", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("money_quality", sa.Numeric(5, 3), nullable=False, server_default="0.5"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_rm_attribution_deal", "rm_revenue_attribution", ["deal_id"])
    op.create_index("ix_rm_attribution_offer", "rm_revenue_attribution", ["offer_id"])
    op.create_index("ix_rm_attribution_channel", "rm_revenue_attribution", ["channel"])
    op.create_check_constraint(
        "ck_rm_revenue_nonnegative",
        "rm_revenue_attribution",
        "revenue_sar >= 0",
    )

    op.create_table(
        "rm_marketing_experiments",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("experiment_name", sa.Text(), nullable=False),
        sa.Column("target_segment", sa.Text(), nullable=False),
        sa.Column("offer_id", sa.Text(), nullable=False),
        sa.Column("variable_tested", sa.Text(), nullable=False),
        sa.Column("variant_a", sa.Text(), nullable=False),
        sa.Column("variant_b", sa.Text(), nullable=False),
        sa.Column("success_metric", sa.Text(), nullable=False),
        sa.Column("minimum_sample", sa.Integer(), nullable=False, server_default="50"),
        sa.Column("decision_rule", sa.Text(), nullable=False),
        sa.Column("samples_a", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("samples_b", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("wins_a", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("wins_b", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.Text(), nullable=False, server_default="draft"),
        sa.Column("result", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("decision", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "rm_content_cards",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("topic_ar", sa.Text(), nullable=False),
        sa.Column("target_segment", sa.Text(), nullable=False),
        sa.Column("pain", sa.Text(), nullable=False),
        sa.Column("offer_id", sa.Text(), nullable=False),
        sa.Column("cta_ar", sa.Text(), nullable=False),
        sa.Column("channel", sa.Text(), nullable=False),
        sa.Column("success_metric", sa.Text(), nullable=False, server_default="leads_booked"),
        sa.Column("pillar", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.Text(), nullable=False, server_default="idea"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "rm_funnel_snapshots",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("visitors", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("leads", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("qualified_leads", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("calls_booked", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("proposals_sent", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("won", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("lost", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("paid", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("retainers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("period_label", sa.Text(), nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_table("rm_funnel_snapshots")
    op.drop_table("rm_content_cards")
    op.drop_table("rm_marketing_experiments")
    op.drop_index("ix_rm_attribution_channel", table_name="rm_revenue_attribution")
    op.drop_index("ix_rm_attribution_offer", table_name="rm_revenue_attribution")
    op.drop_index("ix_rm_attribution_deal", table_name="rm_revenue_attribution")
    op.drop_table("rm_revenue_attribution")
    op.drop_index("ix_rm_touches_occurred", table_name="rm_marketing_touches")
    op.drop_index("ix_rm_touches_campaign", table_name="rm_marketing_touches")
    op.drop_index("ix_rm_touches_lead", table_name="rm_marketing_touches")
    op.drop_table("rm_marketing_touches")
    op.drop_index("ix_rm_campaigns_offer", table_name="rm_campaigns")
    op.drop_index("ix_rm_campaigns_status", table_name="rm_campaigns")
    op.drop_table("rm_campaigns")
    op.drop_index("ix_rm_signals_segment", table_name="rm_signals")
    op.drop_table("rm_signals")
    op.drop_index("ix_rm_offers_tier", table_name="rm_offers")
    op.drop_table("rm_offers")
