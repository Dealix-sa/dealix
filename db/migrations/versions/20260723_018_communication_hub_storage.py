"""Durable Communication OS snapshot storage.

Revision ID: 20260723_018_communication_hub_storage
Revises: 20260715_017_commercial_intelligence
Create Date: 2026-07-23
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20260723_018_communication_hub_storage"
down_revision: str | None = "20260715_017_commercial_intelligence"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "communication_hub_snapshots",
        sa.Column("collection", sa.String(32), primary_key=True),
        sa.Column(
            "data",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "collection IN ('contact_log', 'sequences')",
            name="ck_communication_hub_collection",
        ),
    )
    snapshot_table = sa.table(
        "communication_hub_snapshots",
        sa.column("collection", sa.String(32)),
        sa.column("data", JSONB),
    )
    op.bulk_insert(
        snapshot_table,
        [
            {"collection": "contact_log", "data": []},
            {"collection": "sequences", "data": []},
        ],
    )


def downgrade() -> None:
    op.drop_table("communication_hub_snapshots")
