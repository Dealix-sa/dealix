"""Durable store for the internal strategic automation layer.

The weekly strategic runner generates role briefs, the weekly executive
report, the growth scorecard, the bottleneck sweep, the business-metrics
snapshot, and the strategy-synthesis brief. They must persist to Postgres
so the artifacts survive worker restarts and are not lost to ephemeral
``data/`` files. All artifacts are internal-only (founder-facing).

Revision ID: 014
Revises: 013
Create Date: 2026-05-19
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "014"
down_revision: Union[str, Sequence[str], None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "strategic_briefs",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("artifact_type", sa.String(length=64), nullable=False),
        sa.Column("period_label", sa.String(length=32), nullable=False,
                  server_default=""),
        sa.Column("title", sa.Text(), nullable=False, server_default=""),
        sa.Column("payload", sa.JSON(), nullable=False,
                  server_default=sa.text("'{}'")),
        sa.Column("autonomy_level", sa.Integer(), nullable=False,
                  server_default="3"),
        sa.Column("external_send", sa.Boolean(), nullable=False,
                  server_default=sa.false()),
        sa.Column("emailed_to_founder", sa.Boolean(), nullable=False,
                  server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_strategic_briefs_artifact_type", "strategic_briefs",
                    ["artifact_type"])
    op.create_index("ix_strategic_briefs_period_label", "strategic_briefs",
                    ["period_label"])
    op.create_index("ix_strategic_briefs_created_at", "strategic_briefs",
                    ["created_at"])
    op.create_index("ix_strategic_briefs_type_created", "strategic_briefs",
                    ["artifact_type", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_strategic_briefs_type_created", table_name="strategic_briefs")
    op.drop_index("ix_strategic_briefs_created_at", table_name="strategic_briefs")
    op.drop_index("ix_strategic_briefs_period_label", table_name="strategic_briefs")
    op.drop_index("ix_strategic_briefs_artifact_type", table_name="strategic_briefs")
    op.drop_table("strategic_briefs")
