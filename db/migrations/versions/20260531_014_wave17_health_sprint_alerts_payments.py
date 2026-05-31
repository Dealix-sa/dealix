"""Wave 17 — health snapshots, onboarding records, sprint records,
founder alerts, and payment records.

Revision ID: 014
Revises: 013
Create Date: 2026-05-31
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
    # ── health_snapshots ─────────────────────────────────────────
    op.create_table(
        "health_snapshots",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("account_id", sa.String(64), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("tier", sa.String(32), nullable=False, server_default="unknown"),
        sa.Column("engagement_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("delivery_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("financial_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("satisfaction_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("adoption_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("risk_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("is_churn_risk", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("churn_probability", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_health_snapshots_account_id", "health_snapshots", ["account_id"])
    op.create_index("ix_health_snapshots_computed_at", "health_snapshots", ["computed_at"])
    op.create_index(
        "ix_health_snapshots_account_computed",
        "health_snapshots",
        ["account_id", "computed_at"],
    )

    # ── onboarding_records ───────────────────────────────────────
    op.create_table(
        "onboarding_records",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("onboarding_id", sa.String(128), nullable=False),
        sa.Column("account_id", sa.String(64), nullable=True),
        sa.Column("current_stage", sa.String(64), nullable=False, server_default="welcome"),
        sa.Column("service_tier", sa.String(64), nullable=False, server_default="sprint_499"),
        sa.Column("welcome_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("intake_completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("setup_completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("first_value_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("anchored_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_overdue", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(
            ["account_id"], ["accounts.id"], ondelete="SET NULL", use_alter=True
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("onboarding_id", name="uq_onboarding_records_onboarding_id"),
    )
    op.create_index("ix_onboarding_records_onboarding_id", "onboarding_records", ["onboarding_id"])
    op.create_index("ix_onboarding_records_account", "onboarding_records", ["account_id"])

    # ── sprint_records ───────────────────────────────────────────
    op.create_table(
        "sprint_records",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("sprint_id", sa.String(128), nullable=False),
        sa.Column("account_id", sa.String(64), nullable=False),
        sa.Column("day_completed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("data_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sprint_id", name="uq_sprint_records_sprint_id"),
    )
    op.create_index("ix_sprint_records_sprint_id", "sprint_records", ["sprint_id"])
    op.create_index("ix_sprint_records_account_id", "sprint_records", ["account_id"])
    op.create_index("ix_sprint_records_status", "sprint_records", ["status"])

    # ── founder_alerts ───────────────────────────────────────────
    op.create_table(
        "founder_alerts",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("alert_id", sa.String(128), nullable=False),
        sa.Column("alert_type", sa.String(32), nullable=False),
        sa.Column("title_ar", sa.String(500), nullable=False, server_default=""),
        sa.Column("title_en", sa.String(500), nullable=False, server_default=""),
        sa.Column("body_ar", sa.Text(), nullable=False, server_default=""),
        sa.Column("body_en", sa.Text(), nullable=False, server_default=""),
        sa.Column("priority", sa.String(16), nullable=False, server_default="medium"),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("payment_id", sa.String(128), nullable=True),
        sa.Column("account_id", sa.String(64), nullable=True),
        sa.Column("amount_sar", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reviewed_by", sa.String(64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("alert_id", name="uq_founder_alerts_alert_id"),
    )
    op.create_index("ix_founder_alerts_alert_id", "founder_alerts", ["alert_id"])
    op.create_index("ix_founder_alerts_alert_type", "founder_alerts", ["alert_type"])
    op.create_index("ix_founder_alerts_priority", "founder_alerts", ["priority"])
    op.create_index("ix_founder_alerts_status", "founder_alerts", ["status"])
    op.create_index("ix_founder_alerts_account_id", "founder_alerts", ["account_id"])
    op.create_index("ix_founder_alerts_created_at", "founder_alerts", ["created_at"])
    op.create_index(
        "ix_founder_alerts_status_priority", "founder_alerts", ["status", "priority"]
    )
    op.create_index(
        "ix_founder_alerts_type_created", "founder_alerts", ["alert_type", "created_at"]
    )

    # ── payment_records ──────────────────────────────────────────
    op.create_table(
        "payment_records",
        sa.Column("id", sa.String(64), nullable=False),
        sa.Column("payment_id", sa.String(128), nullable=False),
        sa.Column("invoice_id", sa.String(128), nullable=False, server_default=""),
        sa.Column("status", sa.String(32), nullable=False, server_default="unknown"),
        sa.Column("amount_sar", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("amount_halalas", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("service_tier", sa.String(64), nullable=False, server_default=""),
        sa.Column("account_id", sa.String(64), nullable=False, server_default=""),
        sa.Column("customer_name", sa.String(255), nullable=False, server_default=""),
        sa.Column("customer_email", sa.String(255), nullable=False, server_default=""),
        sa.Column("is_live_mode", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("zatca_status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("onboarding_id", sa.String(128), nullable=False, server_default=""),
        sa.Column("founder_alert_id", sa.String(128), nullable=False, server_default=""),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("payment_id", name="uq_payment_records_payment_id"),
    )
    op.create_index("ix_payment_records_payment_id", "payment_records", ["payment_id"])
    op.create_index("ix_payment_records_invoice_id", "payment_records", ["invoice_id"])
    op.create_index("ix_payment_records_status", "payment_records", ["status"])
    op.create_index("ix_payment_records_account_id", "payment_records", ["account_id"])
    op.create_index("ix_payment_records_occurred_at", "payment_records", ["occurred_at"])
    op.create_index(
        "ix_payment_records_account_status", "payment_records", ["account_id", "status"]
    )
    op.create_index(
        "ix_payment_records_tier_occurred", "payment_records", ["service_tier", "occurred_at"]
    )


def downgrade() -> None:
    op.drop_table("payment_records")
    op.drop_table("founder_alerts")
    op.drop_table("sprint_records")
    op.drop_table("onboarding_records")
    op.drop_table("health_snapshots")
