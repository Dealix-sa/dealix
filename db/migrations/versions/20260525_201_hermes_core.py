"""Hermes core persistence tables (Section 56 / Migration 001).

Creates the signal -> opportunity -> decision -> execution -> outcome ->
asset / event spine used by the Hermes operating system.

Revision ID: 201
Revises: 013
Create Date: 2026-05-25
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "201"
down_revision: Union[str, Sequence[str], None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hermes_opportunities",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("customer_id", sa.String(64), nullable=True),
        sa.Column("sector", sa.Text(), nullable=True),
        sa.Column("score", sa.Numeric(5, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("status", sa.String(32), nullable=False, server_default="open"),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_opportunities_customer", "hermes_opportunities", ["customer_id"])
    op.create_index("ix_hermes_opportunities_status", "hermes_opportunities", ["status"])
    op.create_index(
        "ix_hermes_opportunities_created_at",
        "hermes_opportunities",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_signals",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("source", sa.String(64), nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "opportunity_id",
            sa.String(64),
            sa.ForeignKey("hermes_opportunities.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("captured_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_signals_kind", "hermes_signals", ["kind"])
    op.create_index("ix_hermes_signals_opportunity", "hermes_signals", ["opportunity_id"])
    op.create_index(
        "ix_hermes_signals_created_at",
        "hermes_signals",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_decisions",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "opportunity_id",
            sa.String(64),
            sa.ForeignKey("hermes_opportunities.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("sovereignty_level", sa.String(32), nullable=False),
        sa.Column("risk_level", sa.String(32), nullable=False),
        sa.Column(
            "approval_required",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_decisions_opportunity", "hermes_decisions", ["opportunity_id"])
    op.create_index(
        "ix_hermes_decisions_created_at",
        "hermes_decisions",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_executions",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "decision_id",
            sa.String(64),
            sa.ForeignKey("hermes_decisions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("agent_id", sa.String(64), nullable=False),
        sa.Column("workflow_id", sa.String(64), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("ended_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_executions_decision", "hermes_executions", ["decision_id"])
    op.create_index("ix_hermes_executions_status", "hermes_executions", ["status"])
    op.create_index(
        "ix_hermes_executions_created_at",
        "hermes_executions",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_outcomes",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "execution_id",
            sa.String(64),
            sa.ForeignKey("hermes_executions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("value_sar", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("recorded_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_outcomes_execution", "hermes_outcomes", ["execution_id"])
    op.create_index("ix_hermes_outcomes_kind", "hermes_outcomes", ["kind"])
    op.create_index(
        "ix_hermes_outcomes_created_at",
        "hermes_outcomes",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_assets",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("body", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "source_execution_id",
            sa.String(64),
            sa.ForeignKey("hermes_executions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "source_outcome_id",
            sa.String(64),
            sa.ForeignKey("hermes_outcomes.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "revenue_attributed_sar",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column("tags", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_assets_kind", "hermes_assets", ["kind"])
    op.create_index(
        "ix_hermes_assets_created_at",
        "hermes_assets",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_events",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("request_id", sa.String(64), nullable=False),
        sa.Column("stage", sa.String(64), nullable=False),
        sa.Column("actor_id", sa.String(64), nullable=True),
        sa.Column("outcome", sa.String(32), nullable=True),
        sa.Column(
            "payload_summary",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_events_request", "hermes_events", ["request_id"])
    op.create_index("ix_hermes_events_stage", "hermes_events", ["stage"])
    op.create_index(
        "ix_hermes_events_created_at",
        "hermes_events",
        [sa.text("created_at DESC")],
    )


def downgrade() -> None:
    op.drop_index("ix_hermes_events_created_at", table_name="hermes_events")
    op.drop_index("ix_hermes_events_stage", table_name="hermes_events")
    op.drop_index("ix_hermes_events_request", table_name="hermes_events")
    op.drop_table("hermes_events")

    op.drop_index("ix_hermes_assets_created_at", table_name="hermes_assets")
    op.drop_index("ix_hermes_assets_kind", table_name="hermes_assets")
    op.drop_table("hermes_assets")

    op.drop_index("ix_hermes_outcomes_created_at", table_name="hermes_outcomes")
    op.drop_index("ix_hermes_outcomes_kind", table_name="hermes_outcomes")
    op.drop_index("ix_hermes_outcomes_execution", table_name="hermes_outcomes")
    op.drop_table("hermes_outcomes")

    op.drop_index("ix_hermes_executions_created_at", table_name="hermes_executions")
    op.drop_index("ix_hermes_executions_status", table_name="hermes_executions")
    op.drop_index("ix_hermes_executions_decision", table_name="hermes_executions")
    op.drop_table("hermes_executions")

    op.drop_index("ix_hermes_decisions_created_at", table_name="hermes_decisions")
    op.drop_index("ix_hermes_decisions_opportunity", table_name="hermes_decisions")
    op.drop_table("hermes_decisions")

    op.drop_index("ix_hermes_signals_created_at", table_name="hermes_signals")
    op.drop_index("ix_hermes_signals_opportunity", table_name="hermes_signals")
    op.drop_index("ix_hermes_signals_kind", table_name="hermes_signals")
    op.drop_table("hermes_signals")

    op.drop_index("ix_hermes_opportunities_created_at", table_name="hermes_opportunities")
    op.drop_index("ix_hermes_opportunities_status", table_name="hermes_opportunities")
    op.drop_index("ix_hermes_opportunities_customer", table_name="hermes_opportunities")
    op.drop_table("hermes_opportunities")
