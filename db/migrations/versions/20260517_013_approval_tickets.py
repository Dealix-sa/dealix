"""Approval Command Center durable queue — approval_tickets table.

Migration 013.
Down revision: 012 (value_ledger_and_operational_streams).

The Approval Command Center previously held its queue in process memory,
so every Railway redeploy wiped every pending founder approval. This
table makes the queue durable; the in-memory store hydrates from it on
startup and writes through on every mutation.
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "013"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "012"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "approval_tickets",
        sa.Column("approval_id", sa.String(length=64), nullable=False),
        sa.Column("object_type", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("object_id", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("action_type", sa.String(length=64), nullable=False, server_default=""),
        sa.Column(
            "action_mode", sa.String(length=32), nullable=False,
            server_default="approval_required",
        ),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("risk_level", sa.String(length=16), nullable=False, server_default="low"),
        sa.Column("channel", sa.String(length=32), nullable=True),
        sa.Column("proof_impact", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("customer_id", sa.String(length=64), nullable=True),
        sa.Column("lead_id", sa.String(length=64), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("approval_id", name="pk_approval_tickets"),
    )
    op.create_index("ix_approval_tickets_action_type", "approval_tickets", ["action_type"])
    op.create_index("ix_approval_tickets_status", "approval_tickets", ["status"])
    op.create_index("ix_approval_tickets_customer_id", "approval_tickets", ["customer_id"])
    op.create_index("ix_approval_tickets_lead_id", "approval_tickets", ["lead_id"])
    op.create_index("ix_approval_tickets_created_at", "approval_tickets", ["created_at"])
    op.create_index("ix_approval_tickets_updated_at", "approval_tickets", ["updated_at"])
    op.create_index(
        "ix_approval_tickets_status_created",
        "approval_tickets",
        ["status", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_approval_tickets_status_created", table_name="approval_tickets")
    op.drop_index("ix_approval_tickets_updated_at", table_name="approval_tickets")
    op.drop_index("ix_approval_tickets_created_at", table_name="approval_tickets")
    op.drop_index("ix_approval_tickets_lead_id", table_name="approval_tickets")
    op.drop_index("ix_approval_tickets_customer_id", table_name="approval_tickets")
    op.drop_index("ix_approval_tickets_status", table_name="approval_tickets")
    op.drop_index("ix_approval_tickets_action_type", table_name="approval_tickets")
    op.drop_table("approval_tickets")
