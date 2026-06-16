"""Controlled live outbound tables.

Revision ID: 014
Revises: 013
Create Date: 2026-06-16
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

from alembic import op

revision: str = "014"
down_revision: str | Sequence[str] | None = "013"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "outbound_contacts",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("company_name", sa.Text(), nullable=False),
        sa.Column("contact_name", sa.Text(), nullable=True),
        sa.Column("email", sa.Text(), nullable=True),
        sa.Column("phone", sa.Text(), nullable=True),
        sa.Column("whatsapp", sa.Text(), nullable=True),
        sa.Column("sector", sa.Text(), nullable=True),
        sa.Column("city", sa.Text(), nullable=True),
        sa.Column("website", sa.Text(), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column(
            "verification_status",
            sa.Text(),
            nullable=False,
            server_default="unverified",
        ),
        sa.Column("confidence", sa.Text(), nullable=True, server_default="low"),
        sa.Column("pain_hypothesis", sa.Text(), nullable=True),
        sa.Column("dealix_angle", sa.Text(), nullable=True),
        sa.Column("email_opt_out", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("whatsapp_opt_in", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("whatsapp_opt_out", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("consent_source", sa.Text(), nullable=True),
        sa.Column("consent_timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_table(
        "outbound_messages",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "contact_id",
            UUID(as_uuid=True),
            sa.ForeignKey("outbound_contacts.id"),
            nullable=True,
        ),
        sa.Column("channel", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False, server_default="draft"),
        sa.Column("subject", sa.Text(), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("template_name", sa.Text(), nullable=True),
        sa.Column("provider_message_id", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("approved_by", sa.Text(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("queued_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("replied_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_index("ix_outbound_messages_status", "outbound_messages", ["status"])
    op.create_index("ix_outbound_messages_channel", "outbound_messages", ["channel"])
    op.create_index("ix_outbound_messages_contact_id", "outbound_messages", ["contact_id"])

    op.create_table(
        "outbound_events",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "message_id",
            UUID(as_uuid=True),
            sa.ForeignKey("outbound_messages.id"),
            nullable=True,
        ),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("payload", JSONB, nullable=True, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_outbound_events_message_id", "outbound_events", ["message_id"])
    op.create_index("ix_outbound_events_event_type", "outbound_events", ["event_type"])

    op.create_table(
        "suppression_list",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("channel", sa.Text(), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("channel", "value", name="uq_suppression_channel_value"),
    )

    op.create_table(
        "deals_pipeline",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "contact_id",
            UUID(as_uuid=True),
            sa.ForeignKey("outbound_contacts.id"),
            nullable=True,
        ),
        sa.Column("stage", sa.Text(), nullable=False, server_default="new"),
        sa.Column("value_sar", sa.Numeric(), nullable=True, server_default="0"),
        sa.Column("next_action", sa.Text(), nullable=True),
        sa.Column("next_action_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("owner", sa.Text(), nullable=False, server_default="sami"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_table("deals_pipeline")
    op.drop_table("suppression_list")
    op.drop_index("ix_outbound_events_event_type", table_name="outbound_events")
    op.drop_index("ix_outbound_events_message_id", table_name="outbound_events")
    op.drop_table("outbound_events")
    op.drop_index("ix_outbound_messages_contact_id", table_name="outbound_messages")
    op.drop_index("ix_outbound_messages_channel", table_name="outbound_messages")
    op.drop_index("ix_outbound_messages_status", table_name="outbound_messages")
    op.drop_table("outbound_messages")
    op.drop_table("outbound_contacts")
