"""Customer portal feedback table — Track B.4 Customer Portal Backend MVP.

Adds the `customer_feedback` table used by the new
`/api/v1/portal/feedback` endpoint. Idempotent — only creates the table
when it is not already present so re-runs in shared environments are
safe.

Revision ID: 014
Revises: 013
Create Date: 2026-05-24
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision: str = "014"
down_revision: Union[str, Sequence[str], None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_TABLE_NAME = "customer_feedback"


def _table_exists() -> bool:
    bind = op.get_bind()
    insp = inspect(bind)
    return _TABLE_NAME in insp.get_table_names()


def upgrade() -> None:
    if _table_exists():
        return
    op.create_table(
        _TABLE_NAME,
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column(
            "tenant_id",
            sa.String(length=64),
            sa.ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("customer_id", sa.String(length=64), nullable=False),
        sa.Column("sprint_id", sa.String(length=64), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index(
        "ix_customer_feedback_tenant_id",
        _TABLE_NAME,
        ["tenant_id"],
    )
    op.create_index(
        "ix_customer_feedback_customer_id",
        _TABLE_NAME,
        ["customer_id"],
    )
    op.create_index(
        "ix_customer_feedback_sprint_id",
        _TABLE_NAME,
        ["sprint_id"],
    )
    op.create_index(
        "ix_customer_feedback_created_at",
        _TABLE_NAME,
        ["created_at"],
    )
    op.create_index(
        "ix_customer_feedback_tenant_created",
        _TABLE_NAME,
        ["tenant_id", "created_at"],
    )


def downgrade() -> None:
    if not _table_exists():
        return
    op.drop_index("ix_customer_feedback_tenant_created", table_name=_TABLE_NAME)
    op.drop_index("ix_customer_feedback_created_at", table_name=_TABLE_NAME)
    op.drop_index("ix_customer_feedback_sprint_id", table_name=_TABLE_NAME)
    op.drop_index("ix_customer_feedback_customer_id", table_name=_TABLE_NAME)
    op.drop_index("ix_customer_feedback_tenant_id", table_name=_TABLE_NAME)
    op.drop_table(_TABLE_NAME)
