"""Hermes advanced tables (Section 56 / Migration 005).

MCP servers, MCP reviews, agent runs, tool calls, traces, cost events.

Revision ID: 205
Revises: 204
Create Date: 2026-05-25
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "205"
down_revision: Union[str, Sequence[str], None] = "204"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hermes_mcp_servers",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("vendor", sa.String(64), nullable=True),
        sa.Column("endpoint", sa.Text(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending_review"),
        sa.Column("sensitivity", sa.String(16), nullable=False, server_default="medium"),
        sa.Column(
            "capabilities",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("owner", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("registered_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_mcp_servers_status", "hermes_mcp_servers", ["status"])
    op.create_index("ix_hermes_mcp_servers_owner", "hermes_mcp_servers", ["owner"])

    op.create_table(
        "hermes_mcp_reviews",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "server_id",
            sa.String(64),
            sa.ForeignKey("hermes_mcp_servers.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("reviewer", sa.String(64), nullable=False),
        sa.Column("verdict", sa.String(16), nullable=False),
        sa.Column("risk_level", sa.String(16), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("reviewed_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_mcp_reviews_server", "hermes_mcp_reviews", ["server_id"])
    op.create_index("ix_hermes_mcp_reviews_verdict", "hermes_mcp_reviews", ["verdict"])

    op.create_table(
        "hermes_agent_runs",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "agent_id",
            sa.String(64),
            sa.ForeignKey("hermes_agents.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "execution_id",
            sa.String(64),
            sa.ForeignKey("hermes_executions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("input_summary", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("output_summary", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
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
    op.create_index("ix_hermes_agent_runs_agent", "hermes_agent_runs", ["agent_id"])
    op.create_index("ix_hermes_agent_runs_execution", "hermes_agent_runs", ["execution_id"])
    op.create_index("ix_hermes_agent_runs_status", "hermes_agent_runs", ["status"])
    op.create_index(
        "ix_hermes_agent_runs_created_at",
        "hermes_agent_runs",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_tool_calls",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "agent_run_id",
            sa.String(64),
            sa.ForeignKey("hermes_agent_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "tool_id",
            sa.String(64),
            sa.ForeignKey("hermes_tools.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("input_summary", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("output_summary", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
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
    op.create_index("ix_hermes_tool_calls_agent_run", "hermes_tool_calls", ["agent_run_id"])
    op.create_index("ix_hermes_tool_calls_tool", "hermes_tool_calls", ["tool_id"])
    op.create_index("ix_hermes_tool_calls_status", "hermes_tool_calls", ["status"])

    op.create_table(
        "hermes_traces",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("request_id", sa.String(64), nullable=False),
        sa.Column("parent_id", sa.String(64), nullable=True),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column(
            "attributes",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("ended_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_traces_request", "hermes_traces", ["request_id"])
    op.create_index("ix_hermes_traces_parent", "hermes_traces", ["parent_id"])
    op.create_index("ix_hermes_traces_kind", "hermes_traces", ["kind"])
    op.create_index(
        "ix_hermes_traces_created_at",
        "hermes_traces",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_cost_events",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "agent_run_id",
            sa.String(64),
            sa.ForeignKey("hermes_agent_runs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "tool_call_id",
            sa.String(64),
            sa.ForeignKey("hermes_tool_calls.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("provider", sa.String(64), nullable=True),
        sa.Column("units", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unit", sa.String(32), nullable=False, server_default="token"),
        sa.Column("cost_sar", sa.Numeric(12, 4), nullable=False, server_default=sa.text("0")),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("incurred_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_cost_events_kind", "hermes_cost_events", ["kind"])
    op.create_index(
        "ix_hermes_cost_events_agent_run",
        "hermes_cost_events",
        ["agent_run_id"],
    )
    op.create_index(
        "ix_hermes_cost_events_tool_call",
        "hermes_cost_events",
        ["tool_call_id"],
    )
    op.create_index(
        "ix_hermes_cost_events_created_at",
        "hermes_cost_events",
        [sa.text("created_at DESC")],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_hermes_cost_events_created_at",
        table_name="hermes_cost_events",
    )
    op.drop_index("ix_hermes_cost_events_tool_call", table_name="hermes_cost_events")
    op.drop_index("ix_hermes_cost_events_agent_run", table_name="hermes_cost_events")
    op.drop_index("ix_hermes_cost_events_kind", table_name="hermes_cost_events")
    op.drop_table("hermes_cost_events")

    op.drop_index("ix_hermes_traces_created_at", table_name="hermes_traces")
    op.drop_index("ix_hermes_traces_kind", table_name="hermes_traces")
    op.drop_index("ix_hermes_traces_parent", table_name="hermes_traces")
    op.drop_index("ix_hermes_traces_request", table_name="hermes_traces")
    op.drop_table("hermes_traces")

    op.drop_index("ix_hermes_tool_calls_status", table_name="hermes_tool_calls")
    op.drop_index("ix_hermes_tool_calls_tool", table_name="hermes_tool_calls")
    op.drop_index("ix_hermes_tool_calls_agent_run", table_name="hermes_tool_calls")
    op.drop_table("hermes_tool_calls")

    op.drop_index("ix_hermes_agent_runs_created_at", table_name="hermes_agent_runs")
    op.drop_index("ix_hermes_agent_runs_status", table_name="hermes_agent_runs")
    op.drop_index("ix_hermes_agent_runs_execution", table_name="hermes_agent_runs")
    op.drop_index("ix_hermes_agent_runs_agent", table_name="hermes_agent_runs")
    op.drop_table("hermes_agent_runs")

    op.drop_index("ix_hermes_mcp_reviews_verdict", table_name="hermes_mcp_reviews")
    op.drop_index("ix_hermes_mcp_reviews_server", table_name="hermes_mcp_reviews")
    op.drop_table("hermes_mcp_reviews")

    op.drop_index("ix_hermes_mcp_servers_owner", table_name="hermes_mcp_servers")
    op.drop_index("ix_hermes_mcp_servers_status", table_name="hermes_mcp_servers")
    op.drop_table("hermes_mcp_servers")
