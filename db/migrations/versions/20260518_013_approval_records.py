"""Durable approval queue — approval_records table.

The in-memory ApprovalStore loses the founder's approval queue on every
worker restart. This table is the durable Postgres mirror so the queue
survives restarts and is shared across processes.

Revision ID: 013
Revises: 012
Create Date: 2026-05-18
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
    op.create_table(
        "approval_records",
        sa.Column("approval_id", sa.String(length=64), nullable=False),
        sa.Column("object_type", sa.String(length=64), nullable=False),
        sa.Column("object_id", sa.String(length=128), nullable=False),
        sa.Column("action_type", sa.String(length=64), nullable=False),
        sa.Column("action_mode", sa.String(length=32), nullable=False,
                  server_default="approval_required"),
        sa.Column("channel", sa.String(length=32), nullable=True),
        sa.Column("summary_ar", sa.Text(), nullable=False, server_default=""),
        sa.Column("summary_en", sa.Text(), nullable=False, server_default=""),
        sa.Column("risk_level", sa.String(length=16), nullable=False,
                  server_default="low"),
        sa.Column("proof_impact", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(length=16), nullable=False,
                  server_default="pending"),
        sa.Column("reject_reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("edit_history", sa.JSON(), nullable=False,
                  server_default=sa.text("'[]'")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("action_id", sa.String(length=64), nullable=True),
        sa.Column("lead_id", sa.String(length=64), nullable=True),
        sa.Column("customer_id", sa.String(length=64), nullable=True),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("audit_ref", sa.String(length=128), nullable=True),
        sa.Column("proof_target", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("approval_id"),
    )
    op.create_index("ix_approval_records_object_type", "approval_records",
                    ["object_type"])
    op.create_index("ix_approval_records_object_id", "approval_records",
                    ["object_id"])
    op.create_index("ix_approval_records_action_type", "approval_records",
                    ["action_type"])
    op.create_index("ix_approval_records_channel", "approval_records", ["channel"])
    op.create_index("ix_approval_records_risk_level", "approval_records",
                    ["risk_level"])
    op.create_index("ix_approval_records_status", "approval_records", ["status"])
    op.create_index("ix_approval_records_action_id", "approval_records",
                    ["action_id"])
    op.create_index("ix_approval_records_lead_id", "approval_records", ["lead_id"])
    op.create_index("ix_approval_records_customer_id", "approval_records",
                    ["customer_id"])
    op.create_index("ix_approval_records_created_at", "approval_records",
                    ["created_at"])
    op.create_index("ix_approval_records_status_created", "approval_records",
                    ["status", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_approval_records_status_created", table_name="approval_records")
    op.drop_index("ix_approval_records_created_at", table_name="approval_records")
    op.drop_index("ix_approval_records_customer_id", table_name="approval_records")
    op.drop_index("ix_approval_records_lead_id", table_name="approval_records")
    op.drop_index("ix_approval_records_action_id", table_name="approval_records")
    op.drop_index("ix_approval_records_status", table_name="approval_records")
    op.drop_index("ix_approval_records_risk_level", table_name="approval_records")
    op.drop_index("ix_approval_records_channel", table_name="approval_records")
    op.drop_index("ix_approval_records_action_type", table_name="approval_records")
    op.drop_index("ix_approval_records_object_id", table_name="approval_records")
    op.drop_index("ix_approval_records_object_type", table_name="approval_records")
    op.drop_table("approval_records")
