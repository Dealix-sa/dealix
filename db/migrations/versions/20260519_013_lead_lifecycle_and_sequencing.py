"""Lead lifecycle stage + transitions + follow-up sequencing tables.

Revision ID: 013
Revises: 012
Create Date: 2026-05-19

Phase 2 of the governed Full Ops build:
  - leads.lifecycle_stage      — canonical lifecycle stage (M8)
  - lead_stage_transitions     — append-only transition history (M8)
  - follow_up_tasks            — persistent sequencing engine (M7)
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "013"
down_revision: Union[str, Sequence[str], None] = "012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── M8: canonical lifecycle stage on the existing leads table ──
    op.add_column(
        "leads",
        sa.Column(
            "lifecycle_stage",
            sa.String(length=32),
            nullable=False,
            server_default="captured",
        ),
    )
    op.create_index("ix_leads_lifecycle_stage", "leads", ["lifecycle_stage"])

    # ── M8: append-only lifecycle transition log ──
    op.create_table(
        "lead_stage_transitions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("lead_id", sa.String(length=64), nullable=False),
        sa.Column("from_stage", sa.String(length=32), nullable=False),
        sa.Column("to_stage", sa.String(length=32), nullable=False),
        sa.Column("actor", sa.String(length=64), nullable=False, server_default="system"),
        sa.Column("reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"]),
    )
    op.create_index(
        "ix_lead_stage_transitions_lead_id", "lead_stage_transitions", ["lead_id"]
    )
    op.create_index(
        "ix_lead_stage_transitions_to_stage", "lead_stage_transitions", ["to_stage"]
    )
    op.create_index(
        "ix_lead_stage_transitions_occurred", "lead_stage_transitions", ["occurred_at"]
    )

    # ── M7: persistent follow-up sequencing tasks ──
    op.create_table(
        "follow_up_tasks",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("lead_id", sa.String(length=64), nullable=False),
        sa.Column("attempt", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("channel", sa.String(length=32), nullable=False, server_default="email"),
        sa.Column("scheduled_for", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="scheduled"),
        sa.Column("draft_approval_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"]),
    )
    op.create_index("ix_follow_up_tasks_lead_id", "follow_up_tasks", ["lead_id"])
    op.create_index("ix_follow_up_tasks_scheduled_for", "follow_up_tasks", ["scheduled_for"])
    op.create_index("ix_follow_up_tasks_status", "follow_up_tasks", ["status"])
    op.create_index(
        "ix_follow_up_tasks_due", "follow_up_tasks", ["status", "scheduled_for"]
    )


def downgrade() -> None:
    op.drop_index("ix_follow_up_tasks_due", table_name="follow_up_tasks")
    op.drop_index("ix_follow_up_tasks_status", table_name="follow_up_tasks")
    op.drop_index("ix_follow_up_tasks_scheduled_for", table_name="follow_up_tasks")
    op.drop_index("ix_follow_up_tasks_lead_id", table_name="follow_up_tasks")
    op.drop_table("follow_up_tasks")

    op.drop_index(
        "ix_lead_stage_transitions_occurred", table_name="lead_stage_transitions"
    )
    op.drop_index(
        "ix_lead_stage_transitions_to_stage", table_name="lead_stage_transitions"
    )
    op.drop_index(
        "ix_lead_stage_transitions_lead_id", table_name="lead_stage_transitions"
    )
    op.drop_table("lead_stage_transitions")

    op.drop_index("ix_leads_lifecycle_stage", table_name="leads")
    op.drop_column("leads", "lifecycle_stage")
