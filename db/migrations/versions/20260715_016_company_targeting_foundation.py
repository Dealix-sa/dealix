"""Company directory targeting, agent evals, and governed campaign plans.

Revision ID: 20260715_016_company_targeting
Revises: 20260610_015_simplify_product_for_launch
Create Date: 2026-07-15
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20260715_016_company_targeting"
down_revision: Union[str, None] = "20260610_015_simplify_product_for_launch"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "company_directory_imports",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("source_name", sa.String(255), nullable=False),
        sa.Column("source_file_name", sa.String(255), nullable=False),
        sa.Column("source_file_sha256", sa.String(64), nullable=False),
        sa.Column("source_sheet", sa.String(255), nullable=False),
        sa.Column("source_type", sa.String(32), nullable=False),
        sa.Column("allowed_use", sa.String(128), nullable=False),
        sa.Column("source_terms_status", sa.String(32), nullable=False),
        sa.Column("consent_status", sa.String(32), nullable=False),
        sa.Column("retention_until", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("rows_total", sa.Integer(), nullable=False),
        sa.Column("rows_unique", sa.Integer(), nullable=False),
        sa.Column("rows_duplicate", sa.Integer(), nullable=False),
        sa.Column("rows_research_only", sa.Integer(), nullable=False),
        sa.Column("rows_target_ready", sa.Integer(), nullable=False),
        sa.Column("stats_json", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint(
            "tenant_id",
            "source_file_sha256",
            "source_sheet",
            name="uq_company_directory_import_source",
        ),
    )
    op.create_index(
        "ix_company_directory_imports_tenant_id",
        "company_directory_imports",
        ["tenant_id"],
    )
    op.create_index(
        "ix_company_directory_imports_source_sha",
        "company_directory_imports",
        ["source_file_sha256"],
    )
    op.create_index(
        "ix_company_directory_imports_terms",
        "company_directory_imports",
        ["source_terms_status"],
    )

    op.create_table(
        "company_directory_entries",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("import_id", sa.String(64), nullable=False),
        sa.Column("promoted_account_id", sa.String(64), nullable=True),
        sa.Column("company_name", sa.String(255), nullable=False),
        sa.Column("normalized_name", sa.String(255), nullable=False),
        sa.Column("city", sa.String(128), nullable=True),
        sa.Column("activity", sa.String(255), nullable=True),
        sa.Column("has_valid_email", sa.Boolean(), nullable=False),
        sa.Column("has_valid_phone", sa.Boolean(), nullable=False),
        sa.Column("email_masked", sa.String(255), nullable=True),
        sa.Column("phone_masked", sa.String(32), nullable=True),
        sa.Column("email_hmac", sa.String(64), nullable=True),
        sa.Column("phone_hmac", sa.String(64), nullable=True),
        sa.Column("source_sheet", sa.String(255), nullable=False),
        sa.Column("source_row_number", sa.Integer(), nullable=False),
        sa.Column("source_fingerprint", sa.String(64), nullable=False),
        sa.Column("data_quality_score", sa.Float(), nullable=False),
        sa.Column("fit_score", sa.Float(), nullable=False),
        sa.Column("research_priority_score", sa.Float(), nullable=False),
        sa.Column("priority", sa.String(32), nullable=False),
        sa.Column("recommended_offer_id", sa.String(64), nullable=False),
        sa.Column("value_angle_ar", sa.Text(), nullable=False),
        sa.Column("relationship_status", sa.String(32), nullable=False),
        sa.Column("consent_status", sa.String(32), nullable=False),
        sa.Column("targeting_status", sa.String(32), nullable=False),
        sa.Column(
            "suppression_reasons_json",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint(
            "tenant_id",
            "source_fingerprint",
            name="uq_company_directory_entry_fingerprint",
        ),
    )
    for name, columns in (
        ("ix_company_directory_entries_tenant_id", ["tenant_id"]),
        ("ix_company_directory_entries_import_id", ["import_id"]),
        ("ix_company_directory_entries_company_name", ["company_name"]),
        ("ix_company_directory_entries_normalized_name", ["normalized_name"]),
        ("ix_company_directory_entries_city", ["city"]),
        ("ix_company_directory_entries_activity", ["activity"]),
        ("ix_company_directory_entries_priority_score", ["research_priority_score"]),
        ("ix_company_directory_entries_priority", ["priority"]),
        ("ix_company_directory_entries_offer", ["recommended_offer_id"]),
        ("ix_company_directory_entries_status", ["targeting_status"]),
        ("ix_company_directory_entries_email_hmac", ["email_hmac"]),
        ("ix_company_directory_entries_phone_hmac", ["phone_hmac"]),
        ("ix_company_directory_entries_account", ["promoted_account_id"]),
    ):
        op.create_index(name, "company_directory_entries", columns)
    op.create_index(
        "ix_company_directory_target_queue",
        "company_directory_entries",
        ["tenant_id", "targeting_status", "research_priority_score"],
    )

    op.create_table(
        "agent_capability_evaluations",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("run_id", sa.String(64), nullable=False),
        sa.Column("agent_name", sa.String(64), nullable=False),
        sa.Column("capability", sa.String(64), nullable=False),
        sa.Column("scenario_id", sa.String(128), nullable=False),
        sa.Column("evaluator_version", sa.String(32), nullable=False),
        sa.Column("model_name", sa.String(128), nullable=True),
        sa.Column("prompt_version", sa.String(64), nullable=True),
        sa.Column("dimension_scores_json", JSONB, nullable=False),
        sa.Column("total_score", sa.Float(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("critical_failures_json", JSONB, nullable=False),
        sa.Column("evidence_json", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    for name, columns in (
        ("ix_agent_capability_evaluations_tenant_id", ["tenant_id"]),
        ("ix_agent_capability_evaluations_run_id", ["run_id"]),
        ("ix_agent_capability_evaluations_agent", ["agent_name"]),
        ("ix_agent_capability_evaluations_capability", ["capability"]),
        ("ix_agent_capability_evaluations_scenario", ["scenario_id"]),
        ("ix_agent_capability_evaluations_passed", ["passed"]),
        ("ix_agent_capability_evaluations_created", ["created_at"]),
    ):
        op.create_index(name, "agent_capability_evaluations", columns)
    op.create_index(
        "ix_agent_capability_eval_gate",
        "agent_capability_evaluations",
        ["tenant_id", "capability", "passed"],
    )

    op.create_table(
        "commercial_campaign_plans",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("offer_id", sa.String(64), nullable=False),
        sa.Column("mode", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("segment_filter_json", JSONB, nullable=False),
        sa.Column("audience_count", sa.Integer(), nullable=False),
        sa.Column("experiment_hypothesis", sa.Text(), nullable=False),
        sa.Column("success_metric", sa.String(128), nullable=False),
        sa.Column("guardrails_json", JSONB, nullable=False),
        sa.Column("approval_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index(
        "ix_commercial_campaign_plans_tenant_id",
        "commercial_campaign_plans",
        ["tenant_id"],
    )
    op.create_index(
        "ix_commercial_campaign_plans_offer",
        "commercial_campaign_plans",
        ["offer_id"],
    )
    op.create_index(
        "ix_commercial_campaign_plans_status",
        "commercial_campaign_plans",
        ["status"],
    )

    op.create_table(
        "commercial_campaign_items",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), nullable=False),
        sa.Column("campaign_id", sa.String(64), nullable=False),
        sa.Column("directory_entry_id", sa.String(64), nullable=False),
        sa.Column("account_id", sa.String(64), nullable=True),
        sa.Column("channel", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("qualification_json", JSONB, nullable=False),
        sa.Column("value_case_json", JSONB, nullable=False),
        sa.Column("objections_json", JSONB, nullable=False),
        sa.Column("negotiation_policy_json", JSONB, nullable=False),
        sa.Column("draft_json", JSONB, nullable=False),
        sa.Column("approval_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint(
            "campaign_id",
            "directory_entry_id",
            name="uq_campaign_directory_entry",
        ),
    )
    for name, columns in (
        ("ix_commercial_campaign_items_tenant_id", ["tenant_id"]),
        ("ix_commercial_campaign_items_campaign_id", ["campaign_id"]),
        ("ix_commercial_campaign_items_directory", ["directory_entry_id"]),
        ("ix_commercial_campaign_items_status", ["status"]),
    ):
        op.create_index(name, "commercial_campaign_items", columns)


def downgrade() -> None:
    op.drop_table("commercial_campaign_items")
    op.drop_table("commercial_campaign_plans")
    op.drop_table("agent_capability_evaluations")
    op.drop_table("company_directory_entries")
    op.drop_table("company_directory_imports")
