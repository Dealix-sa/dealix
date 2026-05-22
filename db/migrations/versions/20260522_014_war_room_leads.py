"""war_room_leads table — Postgres home for war-room leads (M-WR).

Before this, war-room leads lived in a JSON file
(``dealix/revenue_ops_autopilot/store.py``), inconsistent with the rest of
the Postgres data plane. This migration creates the table that
:class:`PostgresWarRoomLeadsStore` writes to when
``war_room_store_backend=postgres``. JSON fallback remains the default.

The table mirrors the leads slice of the
:class:`FunnelLeadRecord` contract — full record persisted as JSON in
``payload``, with a handful of scalar columns mirrored out for indexed
querying.

Revision ID: 014
Revises: 013
"""
from __future__ import annotations

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

revision: str = "014"
down_revision: Union[str, Sequence[str], None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "war_room_leads",
        sa.Column("lead_id", sa.String(64), primary_key=True),
        sa.Column("company", sa.String(255), nullable=False, server_default=""),
        sa.Column("industry", sa.String(128), nullable=False, server_default=""),
        sa.Column("stage", sa.String(64), index=True, nullable=False, server_default=""),
        sa.Column(
            "war_room_status",
            sa.String(64),
            index=True,
            nullable=False,
            server_default="",
        ),
        sa.Column("offer_id", sa.String(64), nullable=False, server_default=""),
        sa.Column("next_action_due", sa.String(64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            index=True,
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            index=True,
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "payload",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )


def downgrade() -> None:
    op.drop_table("war_room_leads")
