"""AI Learning Events — shadow-mode feedback ledger for the AI Stack.

Revision ID: 014
Revises: 013
Create Date: 2026-05-25

Stores decision-outcome pairs from every AI Stack run so the Self-Evolving OS
(L11) can compute improvement proposals. Strictly append-only — no rows are
updated or deleted. The router NEVER reads from this table for runtime
decisions; it is shadow-mode learning material only, surfaced to humans via
``/api/v1/ai-stack/proposals`` for explicit approval.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "014"
down_revision: Union[str, Sequence[str], None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ai_learning_events",
        sa.Column("event_id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("run_id", sa.Text(), nullable=False),
        sa.Column("layer", sa.Text(), nullable=False),
        sa.Column("decision_id", sa.Text(), nullable=True),
        sa.Column("agent_name", sa.Text(), nullable=True),
        sa.Column("model_task", sa.Text(), nullable=True),
        sa.Column("outcome_kind", sa.Text(), nullable=False),
        sa.Column("outcome_value", sa.Float(), nullable=True),
        sa.Column("doctrine_clean", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("learnings", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("event_id"),
        sa.CheckConstraint(
            "layer IN ("
            "'L1_source_passport','L2_data_quality','L3_intelligence','L4_model_router',"
            "'L5_agent_mesh','L6_governance','L7_proof_pack','L8_value_ledger',"
            "'L9_capital_ledger','L10_adoption','L11_self_evolving'"
            ")",
            name="ck_ai_learning_events_layer",
        ),
        sa.CheckConstraint(
            "outcome_kind IN ("
            "'success','partial','failure','blocked_by_governance','blocked_by_doctrine',"
            "'customer_confirmed','customer_rejected','no_signal'"
            ")",
            name="ck_ai_learning_events_outcome_kind",
        ),
    )
    op.create_index(
        "ix_ai_learning_events_tenant_run",
        "ai_learning_events",
        ["tenant_id", "run_id"],
    )
    op.create_index(
        "ix_ai_learning_events_tenant_layer_created",
        "ai_learning_events",
        ["tenant_id", "layer", "created_at"],
    )
    op.create_index(
        "ix_ai_learning_events_doctrine_clean",
        "ai_learning_events",
        ["doctrine_clean"],
    )

    op.create_table(
        "ai_improvement_proposals",
        sa.Column("proposal_id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("target_layer", sa.Text(), nullable=False),
        sa.Column("proposed_change", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("evidence_event_ids", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("state", sa.Text(), nullable=False, server_default="pending_approval"),
        sa.Column("approved_by", sa.Text(), nullable=True),
        sa.Column("applied_by", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("proposal_id"),
        sa.CheckConstraint(
            "state IN ('pending_approval','approved','applied','rejected')",
            name="ck_ai_improvement_proposals_state",
        ),
    )
    op.create_index(
        "ix_ai_improvement_proposals_tenant_state",
        "ai_improvement_proposals",
        ["tenant_id", "state"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_ai_improvement_proposals_tenant_state",
        table_name="ai_improvement_proposals",
    )
    op.drop_table("ai_improvement_proposals")
    op.drop_index("ix_ai_learning_events_doctrine_clean", table_name="ai_learning_events")
    op.drop_index(
        "ix_ai_learning_events_tenant_layer_created",
        table_name="ai_learning_events",
    )
    op.drop_index("ix_ai_learning_events_tenant_run", table_name="ai_learning_events")
    op.drop_table("ai_learning_events")
