"""Launch persistence — approval requests, manual payments, social posts.

Moves three launch-critical surfaces off process memory / ephemeral disk
onto Postgres so they survive a restart:

  - approval_requests — backs the ApprovalRequest Pydantic schema
    (auto_client_acquisition/approval_center/schemas.py).
  - manual_payments — backs the bank-transfer state machine
    (auto_client_acquisition/payment_ops/orchestrator.py), previously
    written to the ephemeral data/payment_states.jsonl file.
  - social_posts — own-channel social post drafts + publish lifecycle.

The audit_logs table already exists (AuditLogRecord) and is not recreated.

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
        "approval_requests",
        sa.Column("approval_id", sa.String(64), nullable=False),
        sa.Column("object_type", sa.String(64), nullable=False),
        sa.Column("object_id", sa.String(64), nullable=False),
        sa.Column("action_type", sa.String(64), nullable=False),
        sa.Column("action_mode", sa.String(32), nullable=False, server_default="approval_required"),
        sa.Column("channel", sa.String(32), nullable=True),
        sa.Column("summary_ar", sa.Text(), nullable=False, server_default=""),
        sa.Column("summary_en", sa.Text(), nullable=False, server_default=""),
        sa.Column("risk_level", sa.String(16), nullable=False, server_default="low"),
        sa.Column("proof_impact", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("reject_reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("edit_history", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("action_id", sa.String(64), nullable=True),
        sa.Column("lead_id", sa.String(64), nullable=True),
        sa.Column("customer_id", sa.String(64), nullable=True),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("audit_ref", sa.String(64), nullable=True),
        sa.Column("proof_target", sa.String(128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("approval_id"),
    )
    op.create_index(
        "ix_approval_requests_customer_status",
        "approval_requests",
        ["customer_id", "status"],
    )
    op.create_index("ix_approval_requests_status", "approval_requests", ["status"])
    op.create_index("ix_approval_requests_action_id", "approval_requests", ["action_id"])
    op.create_index("ix_approval_requests_lead_id", "approval_requests", ["lead_id"])

    op.create_table(
        "manual_payments",
        sa.Column("payment_id", sa.String(64), nullable=False),
        sa.Column("customer_handle", sa.String(128), nullable=False),
        sa.Column("service_session_id", sa.String(64), nullable=True),
        sa.Column("invoice_intent_id", sa.String(64), nullable=True),
        sa.Column("amount_sar", sa.Float(), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(8), nullable=False, server_default="SAR"),
        sa.Column("method", sa.String(32), nullable=False),
        sa.Column("state", sa.String(40), nullable=False, server_default="invoice_intent"),
        sa.Column("evidence_reference", sa.Text(), nullable=True),
        sa.Column("confirmed_by", sa.String(128), nullable=True),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivery_kickoff_id", sa.String(64), nullable=True),
        sa.Column("safety_summary", sa.String(64), nullable=False,
                  server_default="no_live_charge_no_fake_revenue"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("payment_id"),
    )
    op.create_index(
        "ix_manual_payments_customer_state",
        "manual_payments",
        ["customer_handle", "state"],
    )
    op.create_index("ix_manual_payments_state", "manual_payments", ["state"])

    op.create_table(
        "social_posts",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("channel", sa.String(32), nullable=False),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("media_url", sa.String(512), nullable=True),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="draft"),
        sa.Column("external_post_id", sa.String(128), nullable=True),
        sa.Column("approval_request_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_social_posts_channel_status", "social_posts", ["channel", "status"])
    op.create_index("ix_social_posts_status_scheduled", "social_posts", ["status", "scheduled_for"])
    op.create_index("ix_social_posts_approval_request", "social_posts", ["approval_request_id"])


def downgrade() -> None:
    op.drop_index("ix_social_posts_approval_request", table_name="social_posts")
    op.drop_index("ix_social_posts_status_scheduled", table_name="social_posts")
    op.drop_index("ix_social_posts_channel_status", table_name="social_posts")
    op.drop_table("social_posts")

    op.drop_index("ix_manual_payments_state", table_name="manual_payments")
    op.drop_index("ix_manual_payments_customer_state", table_name="manual_payments")
    op.drop_table("manual_payments")

    op.drop_index("ix_approval_requests_lead_id", table_name="approval_requests")
    op.drop_index("ix_approval_requests_action_id", table_name="approval_requests")
    op.drop_index("ix_approval_requests_status", table_name="approval_requests")
    op.drop_index("ix_approval_requests_customer_status", table_name="approval_requests")
    op.drop_table("approval_requests")
