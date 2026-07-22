"""Add durable Communication OS state storage.

Revision ID: 20260722_018_communication_state
Revises: 20260715_017_commercial_intelligence
Create Date: 2026-07-22
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20260722_018_communication_state"
down_revision: str | None = "20260715_017_commercial_intelligence"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "communication_state",
        sa.Column("namespace", sa.String(64), primary_key=True),
        sa.Column("state_key", sa.String(64), primary_key=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "state_key IN ('contact_log', 'sequences')",
            name="ck_communication_state_key",
        ),
    )
    op.create_index(
        "ix_communication_state_updated_at",
        "communication_state",
        ["updated_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_communication_state_updated_at",
        table_name="communication_state",
    )
    op.drop_table("communication_state")
