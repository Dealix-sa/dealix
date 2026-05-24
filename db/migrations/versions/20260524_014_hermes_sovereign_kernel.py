"""Hermes Sovereign Universal Kernel — canonical tables.

Revision ID: 014
Revises: 013
Create Date: 2026-05-24

The in-memory stores in :mod:`dealix.hermes` are the runtime source of
truth for fast iteration; this migration adds DB persistence for the
9 core / trust tables described in the canonical specification.
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
        "hermes_signals",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("signal_type", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        sa.Column("confidence", sa.Numeric(), nullable=False, server_default="0.5"),
        sa.Column("sensitivity", sa.Text(), nullable=False, server_default="internal"),
        sa.Column("raw_payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("owner", sa.Text(), nullable=False, server_default="Sami"),
        sa.Column("processed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_hermes_signals_processed", "hermes_signals", ["processed"])
    op.create_index("ix_hermes_signals_type", "hermes_signals", ["signal_type"])

    op.create_table(
        "hermes_opportunities",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("signal_id", sa.Text(), sa.ForeignKey("hermes_signals.id"), nullable=False),
        sa.Column("opportunity_type", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("estimated_value_sar", sa.Numeric(), nullable=False, server_default="0"),
        sa.Column("cash_speed_score", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("strategic_score", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("repeatability_score", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("data_moat_score", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("difficulty_score", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("risk_score", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("sovereignty_level", sa.Text(), nullable=False, server_default="S1_INTERNAL"),
        sa.Column("recommended_action", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.Text(), nullable=False, server_default="open"),
        sa.Column("score", sa.Numeric(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_hermes_opportunities_status", "hermes_opportunities", ["status"])
    op.create_index("ix_hermes_opportunities_sovereignty", "hermes_opportunities", ["sovereignty_level"])

    op.create_table(
        "hermes_decisions",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("opportunity_id", sa.Text(), sa.ForeignKey("hermes_opportunities.id"), nullable=False),
        sa.Column("decision_type", sa.Text(), nullable=False),
        sa.Column("context", sa.Text(), nullable=False, server_default=""),
        sa.Column("options", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("recommendation", sa.Text(), nullable=False, server_default=""),
        sa.Column("risk_level", sa.Text(), nullable=False, server_default="low"),
        sa.Column("sovereignty_level", sa.Text(), nullable=False, server_default="S1_INTERNAL"),
        sa.Column("requires_approval", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("approved_by", sa.Text(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "hermes_executions",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("decision_id", sa.Text(), sa.ForeignKey("hermes_decisions.id"), nullable=False),
        sa.Column("agent_id", sa.Text(), nullable=False),
        sa.Column("action_type", sa.Text(), nullable=False),
        sa.Column("permission_level", sa.Text(), nullable=False, server_default="L1_DRAFT"),
        sa.Column("external_action", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("requires_approval", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("expected_result", sa.Text(), nullable=False, server_default=""),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("status", sa.Text(), nullable=False, server_default="planned"),
        sa.Column("block_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "hermes_outcomes",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("execution_id", sa.Text(), sa.ForeignKey("hermes_executions.id"), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("actual_result", sa.Text(), nullable=False, server_default=""),
        sa.Column("revenue_sar", sa.Numeric(), nullable=False, server_default="0"),
        sa.Column("time_saved_minutes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("risk_reduced", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("learning", sa.Text(), nullable=False, server_default=""),
        sa.Column("asset_review_required", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("asset_id", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "hermes_assets",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("outcome_id", sa.Text(), sa.ForeignKey("hermes_outcomes.id"), nullable=False),
        sa.Column("asset_type", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("reusable", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("commercializable", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("asset_location", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "hermes_agents",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("mission", sa.Text(), nullable=False),
        sa.Column("domain", sa.Text(), nullable=False),
        sa.Column("owner", sa.Text(), nullable=False),
        sa.Column("max_sovereignty_level", sa.Text(), nullable=False),
        sa.Column("allowed_tools", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("forbidden_tools", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("kpis", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("status", sa.Text(), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "hermes_tools",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("tool_type", sa.Text(), nullable=False),
        sa.Column("owner", sa.Text(), nullable=False),
        sa.Column("risk_level", sa.Text(), nullable=False),
        sa.Column("requires_approval", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("data_scope", sa.Text(), nullable=False, server_default="tenant_only"),
        sa.Column("allowed_agents", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("audit_required", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "hermes_approvals",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("requested_by_agent", sa.Text(), nullable=False),
        sa.Column("action_type", sa.Text(), nullable=False),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("sovereignty_level", sa.Text(), nullable=False),
        sa.Column("risk_level", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False, server_default="pending"),
        sa.Column("approved_by", sa.Text(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_hermes_approvals_status", "hermes_approvals", ["status"])

    op.create_table(
        "hermes_audit_events",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("agent_id", sa.Text(), nullable=False, server_default=""),
        sa.Column("tool_id", sa.Text(), nullable=False, server_default=""),
        sa.Column("action_type", sa.Text(), nullable=False),
        sa.Column("payload_hash", sa.Text(), nullable=False, server_default=""),
        sa.Column("risk_level", sa.Text(), nullable=False, server_default="low"),
        sa.Column("sovereignty_level", sa.Text(), nullable=False, server_default="S0_AGENT_FREE"),
        sa.Column("approval_id", sa.Text(), nullable=True),
        sa.Column("result", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_hermes_audit_action_type", "hermes_audit_events", ["action_type"])
    op.create_index("ix_hermes_audit_created_at", "hermes_audit_events", ["created_at"])


def downgrade() -> None:
    for table in (
        "hermes_audit_events",
        "hermes_approvals",
        "hermes_tools",
        "hermes_agents",
        "hermes_assets",
        "hermes_outcomes",
        "hermes_executions",
        "hermes_decisions",
        "hermes_opportunities",
        "hermes_signals",
    ):
        op.drop_table(table)
