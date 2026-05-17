"""Revenue Pipeline durable storage — pipeline_leads table.

Migration 014.
Down revision: 013 (approval_tickets).

The Revenue Pipeline held its leads in process memory, so every Railway
redeploy wiped every tracked lead and deal — the same restart-data-loss
class fixed for the approval queue in migration 013. This table makes
the pipeline durable; the in-memory store hydrates from it on startup
and writes through on every mutation.

No PII: the Lead model is placeholder-shaped by design.
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

__all__ = ["revision", "down_revision", "branch_labels", "depends_on"]

revision: str = "014"  # noqa: F841
down_revision: Union[str, Sequence[str], None] = "013"  # noqa: F841
branch_labels: Union[str, Sequence[str], None] = None  # noqa: F841
depends_on: Union[str, Sequence[str], None] = None  # noqa: F841


def upgrade() -> None:
    op.create_table(
        "pipeline_leads",
        sa.Column("id", sa.String(length=40), nullable=False),
        sa.Column("slot_id", sa.String(length=40), nullable=False, server_default=""),
        sa.Column("sector", sa.String(length=64), nullable=False, server_default="tbd"),
        sa.Column("region", sa.String(length=64), nullable=False, server_default="tbd"),
        sa.Column(
            "relationship_strength", sa.String(length=32), nullable=False,
            server_default="warm_intro",
        ),
        sa.Column(
            "consent_status", sa.String(length=32), nullable=False,
            server_default="not_yet_asked",
        ),
        sa.Column(
            "stage", sa.String(length=48), nullable=False,
            server_default="warm_intro_selected",
        ),
        sa.Column("last_touch_at", sa.DateTime(), nullable=True),
        sa.Column("expected_amount_sar", sa.Integer(), nullable=True),
        sa.Column("actual_amount_sar", sa.Integer(), nullable=True),
        sa.Column("commitment_evidence", sa.Text(), nullable=False, server_default=""),
        sa.Column("payment_evidence", sa.Text(), nullable=False, server_default=""),
        sa.Column("notes_placeholder", sa.Text(), nullable=False, server_default=""),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_pipeline_leads"),
    )
    op.create_index("ix_pipeline_leads_slot_id", "pipeline_leads", ["slot_id"])
    op.create_index("ix_pipeline_leads_stage", "pipeline_leads", ["stage"])
    op.create_index("ix_pipeline_leads_created_at", "pipeline_leads", ["created_at"])
    op.create_index("ix_pipeline_leads_updated_at", "pipeline_leads", ["updated_at"])
    op.create_index(
        "ix_pipeline_leads_stage_updated",
        "pipeline_leads",
        ["stage", "updated_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_pipeline_leads_stage_updated", table_name="pipeline_leads")
    op.drop_index("ix_pipeline_leads_updated_at", table_name="pipeline_leads")
    op.drop_index("ix_pipeline_leads_created_at", table_name="pipeline_leads")
    op.drop_index("ix_pipeline_leads_stage", table_name="pipeline_leads")
    op.drop_index("ix_pipeline_leads_slot_id", table_name="pipeline_leads")
    op.drop_table("pipeline_leads")
