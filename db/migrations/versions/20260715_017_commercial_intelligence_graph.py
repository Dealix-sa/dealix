"""Commercial Intelligence sources, signals, objectives, relationships, and opportunities.

Revision ID: 20260715_017_commercial_intelligence
Revises: 20260715_016_company_targeting
Create Date: 2026-07-15
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20260715_017_commercial_intelligence"
down_revision: str | None = "20260715_016_company_targeting"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "commercial_intelligence_sources",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("source_url", sa.String(1000), nullable=True),
        sa.Column("policy_status", sa.String(32), nullable=False),
        sa.Column("allowed_use", sa.String(255), nullable=False),
        sa.Column("authority_score", sa.Integer(), nullable=False),
        sa.Column("verifiability_score", sa.Integer(), nullable=False),
        sa.Column("freshness_days", sa.Integer(), nullable=False),
        sa.Column("retention_days", sa.Integer(), nullable=False),
        sa.Column("terms_reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("metadata_json", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("tenant_id", "name", name="uq_commercial_intel_source_name"),
    )
    for name, columns in (
        ("ix_commercial_intelligence_sources_tenant_id", ["tenant_id"]),
        ("ix_commercial_intelligence_sources_kind", ["kind"]),
        ("ix_commercial_intelligence_sources_policy_status", ["policy_status"]),
        ("ix_commercial_intelligence_sources_active", ["active"]),
    ):
        op.create_index(name, "commercial_intelligence_sources", columns)

    op.create_table(
        "commercial_intelligence_signals",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("account_id", sa.String(64), nullable=False),
        sa.Column(
            "source_id",
            sa.String(64),
            sa.ForeignKey("commercial_intelligence_sources.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("signal_type", sa.String(64), nullable=False),
        sa.Column("claim", sa.Text(), nullable=False),
        sa.Column("evidence_ref", sa.String(1000), nullable=False),
        sa.Column("evidence_level", sa.String(32), nullable=False),
        sa.Column("confidence", sa.Integer(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("payload_json", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "tenant_id", "account_id", "source_id", "evidence_ref",
            name="uq_commercial_intel_signal_evidence",
        ),
    )
    for name, columns in (
        ("ix_commercial_intelligence_signals_tenant_id", ["tenant_id"]),
        ("ix_commercial_intelligence_signals_account_id", ["account_id"]),
        ("ix_commercial_intelligence_signals_source_id", ["source_id"]),
        ("ix_commercial_intelligence_signals_signal_type", ["signal_type"]),
        ("ix_commercial_intelligence_signals_evidence_level", ["evidence_level"]),
        ("ix_commercial_intelligence_signals_observed_at", ["observed_at"]),
        ("ix_commercial_intelligence_signals_expires_at", ["expires_at"]),
        ("ix_commercial_intelligence_signals_status", ["status"]),
    ):
        op.create_index(name, "commercial_intelligence_signals", columns)
    op.create_index(
        "ix_commercial_intel_signal_account_active",
        "commercial_intelligence_signals",
        ["tenant_id", "account_id", "status", "observed_at"],
    )

    op.create_table(
        "commercial_department_objectives",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("department", sa.String(64), nullable=False),
        sa.Column("objective", sa.Text(), nullable=False),
        sa.Column("metric", sa.String(128), nullable=False),
        sa.Column("target_value", sa.Float(), nullable=True),
        sa.Column("target_unit", sa.String(64), nullable=True),
        sa.Column("horizon", sa.String(32), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("evidence_required", sa.String(32), nullable=False),
        sa.Column("owner_role", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "tenant_id", "department", "metric",
            name="uq_commercial_department_objective_metric",
        ),
    )
    for name, columns in (
        ("ix_commercial_department_objectives_tenant_id", ["tenant_id"]),
        ("ix_commercial_department_objectives_department", ["department"]),
        ("ix_commercial_department_objectives_priority", ["priority"]),
        ("ix_commercial_department_objectives_status", ["status"]),
    ):
        op.create_index(name, "commercial_department_objectives", columns)

    op.create_table(
        "commercial_strategic_relationships",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("account_id", sa.String(64), nullable=False),
        sa.Column("company_name", sa.String(255), nullable=False),
        sa.Column("relationship_type", sa.String(64), nullable=False),
        sa.Column("stage", sa.String(32), nullable=False),
        sa.Column("permission_state", sa.String(32), nullable=False),
        sa.Column("mutual_value", sa.Text(), nullable=False),
        sa.Column("relationship_strength", sa.Integer(), nullable=False),
        sa.Column("owner_role", sa.String(64), nullable=False),
        sa.Column("evidence_refs_json", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("last_interaction_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_review_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "tenant_id", "account_id", "relationship_type",
            name="uq_commercial_strategic_relationship",
        ),
    )
    for name, columns in (
        ("ix_commercial_strategic_relationships_tenant_id", ["tenant_id"]),
        ("ix_commercial_strategic_relationships_account_id", ["account_id"]),
        ("ix_commercial_strategic_relationships_company_name", ["company_name"]),
        ("ix_commercial_strategic_relationships_relationship_type", ["relationship_type"]),
        ("ix_commercial_strategic_relationships_stage", ["stage"]),
        ("ix_commercial_strategic_relationships_relationship_strength", ["relationship_strength"]),
        ("ix_commercial_strategic_relationships_next_review_at", ["next_review_at"]),
    ):
        op.create_index(name, "commercial_strategic_relationships", columns)

    op.create_table(
        "commercial_intelligence_opportunities",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("account_id", sa.String(64), nullable=False),
        sa.Column("company_name", sa.String(255), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column(
            "department_objective_id",
            sa.String(64),
            sa.ForeignKey("commercial_department_objectives.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "relationship_id",
            sa.String(64),
            sa.ForeignKey("commercial_strategic_relationships.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column("offer_id", sa.String(64), nullable=False),
        sa.Column("stage", sa.String(32), nullable=False),
        sa.Column("evidence_level", sa.String(32), nullable=False),
        sa.Column("source_signal_ids_json", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("score_components_json", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("confidence_band", sa.String(16), nullable=False),
        sa.Column("blockers_json", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("next_action", sa.Text(), nullable=False),
        sa.Column("proof_target", sa.Text(), nullable=False),
        sa.Column("approval_required", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("external_action_allowed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "tenant_id", "account_id", "department_objective_id", "offer_id",
            name="uq_commercial_intel_opportunity",
        ),
    )
    for name, columns in (
        ("ix_commercial_intelligence_opportunities_tenant_id", ["tenant_id"]),
        ("ix_commercial_intelligence_opportunities_account_id", ["account_id"]),
        ("ix_commercial_intelligence_opportunities_company_name", ["company_name"]),
        ("ix_commercial_intel_opportunity_objective_id", ["department_objective_id"]),
        ("ix_commercial_intelligence_opportunities_relationship_id", ["relationship_id"]),
        ("ix_commercial_intelligence_opportunities_offer_id", ["offer_id"]),
        ("ix_commercial_intelligence_opportunities_stage", ["stage"]),
        ("ix_commercial_intelligence_opportunities_evidence_level", ["evidence_level"]),
        ("ix_commercial_intelligence_opportunities_score", ["score"]),
        ("ix_commercial_intelligence_opportunities_confidence_band", ["confidence_band"]),
        ("ix_commercial_intelligence_opportunities_status", ["status"]),
    ):
        op.create_index(name, "commercial_intelligence_opportunities", columns)
    op.create_index(
        "ix_commercial_intel_opportunity_queue",
        "commercial_intelligence_opportunities",
        ["tenant_id", "status", "stage", "score"],
    )

    op.create_table(
        "commercial_opportunity_signals",
        sa.Column(
            "opportunity_id",
            sa.String(64),
            sa.ForeignKey("commercial_intelligence_opportunities.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "signal_id",
            sa.String(64),
            sa.ForeignKey("commercial_intelligence_signals.id", ondelete="RESTRICT"),
            primary_key=True,
        ),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_commercial_opportunity_signals_tenant_id",
        "commercial_opportunity_signals",
        ["tenant_id"],
    )
    op.create_index(
        "ix_commercial_opportunity_signal_tenant_opportunity",
        "commercial_opportunity_signals",
        ["tenant_id", "opportunity_id"],
    )

    op.create_table(
        "commercial_opportunity_finance_cases",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column(
            "opportunity_id",
            sa.String(64),
            sa.ForeignKey("commercial_intelligence_opportunities.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "parent_case_id",
            sa.String(64),
            sa.ForeignKey("commercial_opportunity_finance_cases.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column("offer_id", sa.String(64), nullable=False),
        sa.Column("offer_class", sa.String(32), nullable=False),
        sa.Column("pricing_status", sa.String(32), nullable=False),
        sa.Column("decision", sa.String(32), nullable=False),
        sa.Column("currency", sa.String(8), nullable=False, server_default="SAR"),
        sa.Column("proposed_price_sar", sa.Numeric(14, 2), nullable=False),
        sa.Column("gross_margin_pct", sa.Numeric(7, 2), nullable=False),
        sa.Column("contribution_margin_pct", sa.Numeric(7, 2), nullable=False),
        sa.Column("readiness_score", sa.Integer(), nullable=False),
        sa.Column("approval_required", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "external_action_allowed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "created_by_user_id",
            sa.String(64),
            sa.ForeignKey("users.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "approved_by_user_id",
            sa.String(64),
            sa.ForeignKey("users.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column("approval_ref", sa.String(128), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("inputs_json", JSONB, nullable=False),
        sa.Column("assessment_json", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "tenant_id", "parent_case_id",
            name="uq_commercial_finance_parent_case",
        ),
        sa.UniqueConstraint(
            "tenant_id", "approval_ref",
            name="uq_commercial_finance_approval_ref",
        ),
        sa.CheckConstraint(
            "readiness_score >= 0 AND readiness_score <= 100",
            name="ck_commercial_finance_readiness_score",
        ),
        sa.CheckConstraint(
            "approval_required IS TRUE",
            name="ck_commercial_finance_approval_required",
        ),
        sa.CheckConstraint(
            "external_action_allowed IS FALSE",
            name="ck_commercial_finance_no_external_action",
        ),
        sa.CheckConstraint(
            "pricing_status IN ('draft', 'founder_approved')",
            name="ck_commercial_finance_pricing_status",
        ),
        sa.CheckConstraint(
            "decision IN ('pursue', 'review', 'stop')",
            name="ck_commercial_finance_decision",
        ),
    )
    for name, columns in (
        ("ix_commercial_finance_tenant_id", ["tenant_id"]),
        ("ix_commercial_finance_opportunity_id", ["opportunity_id"]),
        ("ix_commercial_finance_parent_case_id", ["parent_case_id"]),
        ("ix_commercial_finance_offer_id", ["offer_id"]),
        ("ix_commercial_finance_offer_class", ["offer_class"]),
        ("ix_commercial_finance_pricing_status", ["pricing_status"]),
        ("ix_commercial_finance_decision", ["decision"]),
        ("ix_commercial_finance_created_by", ["created_by_user_id"]),
        ("ix_commercial_finance_approved_by", ["approved_by_user_id"]),
    ):
        op.create_index(name, "commercial_opportunity_finance_cases", columns)
    op.create_index(
        "ix_commercial_finance_latest_case",
        "commercial_opportunity_finance_cases",
        ["tenant_id", "opportunity_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_table("commercial_opportunity_finance_cases")
    op.drop_table("commercial_opportunity_signals")
    op.drop_table("commercial_intelligence_opportunities")
    op.drop_table("commercial_strategic_relationships")
    op.drop_table("commercial_department_objectives")
    op.drop_table("commercial_intelligence_signals")
    op.drop_table("commercial_intelligence_sources")
