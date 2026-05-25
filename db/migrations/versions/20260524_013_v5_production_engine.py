"""v5 production engine — approvals, workers, evidence, support, marketing, knowledge.

Adds the 6 tables the v5 plan declares missing, plus AI-score columns on
the existing `leads` table. Idempotent at the table level (will refuse
to overwrite anything that already exists in a previous head).

Revision ID: 013
Revises: 012
Create Date: 2026-05-24
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "013"
down_revision: Union[str, Sequence[str], None] = "012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── approvals ───────────────────────────────────────────────
    op.create_table(
        "approvals",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), sa.ForeignKey("tenants.id"), nullable=True),
        sa.Column("action_type", sa.String(64), nullable=False),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("requester", sa.String(128), nullable=False, server_default="system"),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("approval_class", sa.String(2), nullable=False, server_default="A2"),
        sa.Column("reversibility", sa.String(2), nullable=False, server_default="R2"),
        sa.Column("sensitivity", sa.String(2), nullable=False, server_default="S2"),
        sa.Column("evidence_ref", sa.String(255), nullable=True),
        sa.Column("risk_level", sa.String(16), nullable=False, server_default="medium"),
        sa.Column("approver", sa.String(128), nullable=True),
        sa.Column("decision_reason", sa.Text(), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_approvals_tenant_id", "approvals", ["tenant_id"])
    op.create_index("ix_approvals_action_type", "approvals", ["action_type"])
    op.create_index("ix_approvals_status", "approvals", ["status"])
    op.create_index("ix_approvals_approval_class", "approvals", ["approval_class"])
    op.create_index("ix_approvals_requester", "approvals", ["requester"])
    op.create_index("ix_approvals_decided_at", "approvals", ["decided_at"])
    op.create_index("ix_approvals_expires_at", "approvals", ["expires_at"])
    op.create_index("ix_approvals_created_at", "approvals", ["created_at"])
    op.create_index("ix_approvals_tenant_status", "approvals", ["tenant_id", "status"])
    op.create_index("ix_approvals_action_status", "approvals", ["action_type", "status"])

    # ── workers ─────────────────────────────────────────────────
    op.create_table(
        "workers",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("worker_name", sa.String(128), nullable=False),
        sa.Column("host", sa.String(255), nullable=False, server_default=""),
        sa.Column("pid", sa.Integer(), nullable=True),
        sa.Column("queue", sa.String(64), nullable=True),
        sa.Column("capabilities", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("version", sa.String(32), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="active"),
        sa.Column("last_heartbeat", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("runs_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("worker_name", "host", "pid", name="uq_worker_name_host_pid"),
    )
    op.create_index("ix_workers_worker_name", "workers", ["worker_name"])
    op.create_index("ix_workers_queue", "workers", ["queue"])
    op.create_index("ix_workers_status", "workers", ["status"])
    op.create_index("ix_workers_last_heartbeat", "workers", ["last_heartbeat"])

    # ── evidence_events ─────────────────────────────────────────
    op.create_table(
        "evidence_events",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), sa.ForeignKey("tenants.id"), nullable=True),
        sa.Column("lead_id", sa.String(64), sa.ForeignKey("leads.id"), nullable=True),
        sa.Column("deal_id", sa.String(64), sa.ForeignKey("deals.id"), nullable=True),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("source", sa.String(64), nullable=False, server_default="system"),
        sa.Column("actor", sa.String(128), nullable=True),
        sa.Column("motion", sa.String(64), nullable=True),
        sa.Column("offer_id", sa.String(64), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("redaction_status", sa.String(16), nullable=False, server_default="clean"),
        sa.Column("content_hash", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_evidence_tenant_id", "evidence_events", ["tenant_id"])
    op.create_index("ix_evidence_lead_id", "evidence_events", ["lead_id"])
    op.create_index("ix_evidence_deal_id", "evidence_events", ["deal_id"])
    op.create_index("ix_evidence_event_type", "evidence_events", ["event_type"])
    op.create_index("ix_evidence_source", "evidence_events", ["source"])
    op.create_index("ix_evidence_content_hash", "evidence_events", ["content_hash"])
    op.create_index("ix_evidence_created_at", "evidence_events", ["created_at"])
    op.create_index("ix_evidence_tenant_type", "evidence_events", ["tenant_id", "event_type"])
    op.create_index("ix_evidence_lead_created", "evidence_events", ["lead_id", "created_at"])

    # ── support_tickets ─────────────────────────────────────────
    op.create_table(
        "support_tickets",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), sa.ForeignKey("tenants.id"), nullable=True),
        sa.Column("customer_id", sa.String(64), sa.ForeignKey("customers.id"), nullable=True),
        sa.Column("subject", sa.String(500), nullable=False),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("locale", sa.String(4), nullable=False, server_default="ar"),
        sa.Column("channel", sa.String(32), nullable=False, server_default="email"),
        sa.Column("category", sa.String(64), nullable=True),
        sa.Column("priority", sa.String(8), nullable=False, server_default="P3"),
        sa.Column("status", sa.String(16), nullable=False, server_default="open"),
        sa.Column("ai_classification", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("ai_draft_response", sa.Text(), nullable=True),
        sa.Column("ai_confidence", sa.Float(), nullable=True),
        sa.Column("assignee", sa.String(128), nullable=True),
        sa.Column("contact_email", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_tickets_tenant_id", "support_tickets", ["tenant_id"])
    op.create_index("ix_tickets_customer_id", "support_tickets", ["customer_id"])
    op.create_index("ix_tickets_channel", "support_tickets", ["channel"])
    op.create_index("ix_tickets_category", "support_tickets", ["category"])
    op.create_index("ix_tickets_priority", "support_tickets", ["priority"])
    op.create_index("ix_tickets_status", "support_tickets", ["status"])
    op.create_index("ix_tickets_assignee", "support_tickets", ["assignee"])
    op.create_index("ix_tickets_contact_email", "support_tickets", ["contact_email"])
    op.create_index("ix_tickets_created_at", "support_tickets", ["created_at"])
    op.create_index("ix_tickets_tenant_status", "support_tickets", ["tenant_id", "status"])
    op.create_index("ix_tickets_priority_status", "support_tickets", ["priority", "status"])

    # ── marketing_calendar ──────────────────────────────────────
    op.create_table(
        "marketing_calendar",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), sa.ForeignKey("tenants.id"), nullable=True),
        sa.Column("slot_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("channel", sa.String(32), nullable=False, server_default="linkedin"),
        sa.Column("theme", sa.String(255), nullable=True),
        sa.Column("title_ar", sa.String(500), nullable=True),
        sa.Column("title_en", sa.String(500), nullable=True),
        sa.Column("copy_ar", sa.Text(), nullable=True),
        sa.Column("copy_en", sa.Text(), nullable=True),
        sa.Column("locale", sa.String(4), nullable=False, server_default="ar"),
        sa.Column("cta_url", sa.String(500), nullable=True),
        sa.Column("utm_payload", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("evidence_refs", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("publish_kit", JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("status", sa.String(16), nullable=False, server_default="draft"),
        sa.Column("approval_id", sa.String(64), sa.ForeignKey("approvals.id"), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_mcal_tenant_id", "marketing_calendar", ["tenant_id"])
    op.create_index("ix_mcal_slot_date", "marketing_calendar", ["slot_date"])
    op.create_index("ix_mcal_channel", "marketing_calendar", ["channel"])
    op.create_index("ix_mcal_status", "marketing_calendar", ["status"])
    op.create_index("ix_mcal_approval_id", "marketing_calendar", ["approval_id"])
    op.create_index("ix_mcal_tenant_date", "marketing_calendar", ["tenant_id", "slot_date"])
    op.create_index("ix_mcal_channel_status", "marketing_calendar", ["channel", "status"])

    # ── knowledge_base ──────────────────────────────────────────
    op.create_table(
        "knowledge_base",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("tenant_id", sa.String(64), sa.ForeignKey("tenants.id"), nullable=True),
        sa.Column("slug", sa.String(128), nullable=False),
        sa.Column("title_ar", sa.String(500), nullable=True),
        sa.Column("title_en", sa.String(500), nullable=True),
        sa.Column("body_ar", sa.Text(), nullable=True),
        sa.Column("body_en", sa.Text(), nullable=True),
        sa.Column("locale", sa.String(4), nullable=False, server_default="ar"),
        sa.Column("tags", JSONB, nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("category", sa.String(64), nullable=True),
        sa.Column("visibility", sa.String(16), nullable=False, server_default="public"),
        sa.Column("embedding_ref", sa.String(64), nullable=True),
        sa.Column("views_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("helpful_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("slug", name="uq_kb_slug"),
    )
    op.create_index("ix_kb_tenant_id", "knowledge_base", ["tenant_id"])
    op.create_index("ix_kb_slug", "knowledge_base", ["slug"])
    op.create_index("ix_kb_category", "knowledge_base", ["category"])
    op.create_index("ix_kb_visibility", "knowledge_base", ["visibility"])
    op.create_index("ix_kb_tenant_visibility", "knowledge_base", ["tenant_id", "visibility"])

    # ── ai_score columns on leads ───────────────────────────────
    op.add_column("leads", sa.Column("ai_score", sa.Float(), nullable=True))
    op.add_column("leads", sa.Column("ai_score_reasoning", sa.Text(), nullable=True))
    op.add_column("leads", sa.Column("ai_scored_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_leads_ai_score", "leads", ["ai_score"])


def downgrade() -> None:
    op.drop_index("ix_leads_ai_score", table_name="leads")
    op.drop_column("leads", "ai_scored_at")
    op.drop_column("leads", "ai_score_reasoning")
    op.drop_column("leads", "ai_score")

    op.drop_table("knowledge_base")
    op.drop_table("marketing_calendar")
    op.drop_table("support_tickets")
    op.drop_table("evidence_events")
    op.drop_table("workers")
    op.drop_table("approvals")
