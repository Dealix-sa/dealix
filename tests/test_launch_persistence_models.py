"""Sanity tests for the launch-persistence ORM models + migration 013."""

from __future__ import annotations

import importlib

from db.models import (
    ApprovalRequestRecord,
    ManualPaymentRecord,
    SocialPostRecord,
)


def test_approval_request_record_table_and_columns() -> None:
    assert ApprovalRequestRecord.__tablename__ == "approval_requests"
    cols = {c.name for c in ApprovalRequestRecord.__table__.columns}
    expected = {
        "approval_id", "object_type", "object_id", "action_type",
        "action_mode", "channel", "summary_ar", "summary_en", "risk_level",
        "proof_impact", "status", "reject_reason", "edit_history",
        "expires_at", "action_id", "lead_id", "customer_id", "due_date",
        "audit_ref", "proof_target", "created_at", "updated_at",
    }
    assert expected.issubset(cols)


def test_approval_request_record_has_customer_status_index() -> None:
    index_names = {idx.name for idx in ApprovalRequestRecord.__table__.indexes}
    assert "ix_approval_requests_customer_status" in index_names


def test_manual_payment_record_table_and_columns() -> None:
    assert ManualPaymentRecord.__tablename__ == "manual_payments"
    cols = {c.name for c in ManualPaymentRecord.__table__.columns}
    expected = {
        "payment_id", "customer_handle", "service_session_id",
        "invoice_intent_id", "amount_sar", "currency", "method", "state",
        "evidence_reference", "confirmed_by", "confirmed_at",
        "delivery_kickoff_id", "safety_summary", "created_at", "updated_at",
    }
    assert expected.issubset(cols)


def test_social_post_record_table_and_columns() -> None:
    assert SocialPostRecord.__tablename__ == "social_posts"
    cols = {c.name for c in SocialPostRecord.__table__.columns}
    expected = {
        "id", "channel", "body", "media_url", "scheduled_for", "status",
        "external_post_id", "approval_request_id", "created_at", "updated_at",
    }
    assert expected.issubset(cols)


def test_migration_013_revision_links() -> None:
    mod = importlib.import_module(
        "db.migrations.versions.20260518_013_launch_persistence"
    )
    assert mod.revision == "013"
    assert mod.down_revision == "012"
