"""Hermes sovereignty + trust tables (Section 56 / Migration 002).

Agents, tools, permissions, approvals, audit events, risks, incidents,
and evidence packs.

Revision ID: 202
Revises: 201
Create Date: 2026-05-25
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "202"
down_revision: Union[str, Sequence[str], None] = "201"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hermes_agents",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("role", sa.String(64), nullable=False),
        sa.Column("owner", sa.String(64), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column(
            "allowed_tools",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "required_output_fields",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "max_text_chars",
            sa.Integer(),
            nullable=False,
            server_default="8000",
        ),
        sa.Column(
            "can_call_external",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("locale", sa.String(8), nullable=False, server_default="ar"),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_agents_role", "hermes_agents", ["role"])
    op.create_index("ix_hermes_agents_owner", "hermes_agents", ["owner"])

    op.create_table(
        "hermes_tools",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("sensitivity", sa.String(16), nullable=False),
        sa.Column(
            "allowed_actor_kinds",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "requires_approval",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("owner", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_tools_sensitivity", "hermes_tools", ["sensitivity"])
    op.create_index("ix_hermes_tools_owner", "hermes_tools", ["owner"])

    op.create_table(
        "hermes_permissions",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column(
            "agent_id",
            sa.String(64),
            sa.ForeignKey("hermes_agents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "tool_id",
            sa.String(64),
            sa.ForeignKey("hermes_tools.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("scope", sa.String(64), nullable=False, server_default="read"),
        sa.Column("granted_by", sa.String(64), nullable=False),
        sa.Column("granted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "agent_id",
            "tool_id",
            "scope",
            name="uq_hermes_permissions_agent_tool_scope",
        ),
    )
    op.create_index("ix_hermes_permissions_agent", "hermes_permissions", ["agent_id"])
    op.create_index("ix_hermes_permissions_tool", "hermes_permissions", ["tool_id"])

    op.create_table(
        "hermes_approvals",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("request_id", sa.String(64), nullable=False),
        sa.Column("intent", sa.String(64), nullable=False),
        sa.Column("sovereignty_level", sa.String(32), nullable=False),
        sa.Column("approver_role", sa.String(32), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("decided_by", sa.String(64), nullable=True),
        sa.Column("decided_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("decision_note", sa.Text(), nullable=True),
        sa.Column("summary", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("expires_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_approvals_request", "hermes_approvals", ["request_id"])
    op.create_index("ix_hermes_approvals_status", "hermes_approvals", ["status"])
    op.create_index(
        "ix_hermes_approvals_created_at",
        "hermes_approvals",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_audit_events",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("actor_id", sa.String(64), nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("subject_type", sa.String(64), nullable=True),
        sa.Column("subject_id", sa.String(64), nullable=True),
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
    op.create_index("ix_hermes_audit_events_kind", "hermes_audit_events", ["kind"])
    op.create_index("ix_hermes_audit_events_actor", "hermes_audit_events", ["actor_id"])
    op.create_index(
        "ix_hermes_audit_events_created_at",
        "hermes_audit_events",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_risks",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("severity", sa.String(16), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="open"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("owner", sa.String(64), nullable=True),
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
    op.create_index("ix_hermes_risks_kind", "hermes_risks", ["kind"])
    op.create_index("ix_hermes_risks_status", "hermes_risks", ["status"])

    op.create_table(
        "hermes_incidents",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("severity", sa.String(16), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="open"),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column(
            "risk_id",
            sa.String(64),
            sa.ForeignKey("hermes_risks.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("detected_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hermes_incidents_kind", "hermes_incidents", ["kind"])
    op.create_index("ix_hermes_incidents_status", "hermes_incidents", ["status"])
    op.create_index(
        "ix_hermes_incidents_created_at",
        "hermes_incidents",
        [sa.text("created_at DESC")],
    )

    op.create_table(
        "hermes_evidence_packs",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("customer_id", sa.String(64), nullable=True),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("score", sa.Numeric(5, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("tier", sa.String(32), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("assembled_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_hermes_evidence_packs_customer",
        "hermes_evidence_packs",
        ["customer_id"],
    )
    op.create_index("ix_hermes_evidence_packs_kind", "hermes_evidence_packs", ["kind"])
    op.create_index(
        "ix_hermes_evidence_packs_created_at",
        "hermes_evidence_packs",
        [sa.text("created_at DESC")],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_hermes_evidence_packs_created_at",
        table_name="hermes_evidence_packs",
    )
    op.drop_index("ix_hermes_evidence_packs_kind", table_name="hermes_evidence_packs")
    op.drop_index(
        "ix_hermes_evidence_packs_customer",
        table_name="hermes_evidence_packs",
    )
    op.drop_table("hermes_evidence_packs")

    op.drop_index("ix_hermes_incidents_created_at", table_name="hermes_incidents")
    op.drop_index("ix_hermes_incidents_status", table_name="hermes_incidents")
    op.drop_index("ix_hermes_incidents_kind", table_name="hermes_incidents")
    op.drop_table("hermes_incidents")

    op.drop_index("ix_hermes_risks_status", table_name="hermes_risks")
    op.drop_index("ix_hermes_risks_kind", table_name="hermes_risks")
    op.drop_table("hermes_risks")

    op.drop_index(
        "ix_hermes_audit_events_created_at",
        table_name="hermes_audit_events",
    )
    op.drop_index("ix_hermes_audit_events_actor", table_name="hermes_audit_events")
    op.drop_index("ix_hermes_audit_events_kind", table_name="hermes_audit_events")
    op.drop_table("hermes_audit_events")

    op.drop_index("ix_hermes_approvals_created_at", table_name="hermes_approvals")
    op.drop_index("ix_hermes_approvals_status", table_name="hermes_approvals")
    op.drop_index("ix_hermes_approvals_request", table_name="hermes_approvals")
    op.drop_table("hermes_approvals")

    op.drop_index("ix_hermes_permissions_tool", table_name="hermes_permissions")
    op.drop_index("ix_hermes_permissions_agent", table_name="hermes_permissions")
    op.drop_table("hermes_permissions")

    op.drop_index("ix_hermes_tools_owner", table_name="hermes_tools")
    op.drop_index("ix_hermes_tools_sensitivity", table_name="hermes_tools")
    op.drop_table("hermes_tools")

    op.drop_index("ix_hermes_agents_owner", table_name="hermes_agents")
    op.drop_index("ix_hermes_agents_role", table_name="hermes_agents")
    op.drop_table("hermes_agents")
