"""Database foundation safety tests.

Verifies that outbound-related models do not imply live send is enabled,
and that safe env boot still works with the new models.
"""

import os


def test_outbound_message_defaults_to_blocked():
    """OutboundMessageRecord.status must default to 'blocked'."""
    from db.models import OutboundMessageRecord

    col = OutboundMessageRecord.__table__.c.status
    assert col.default is not None
    assert col.default.arg == "blocked", f"Expected 'blocked', got {col.default.arg}"


def test_outbound_message_safety_check_defaults_false():
    """OutboundMessageRecord.safety_check_passed must default to False."""
    from db.models import OutboundMessageRecord

    col = OutboundMessageRecord.__table__.c.safety_check_passed
    assert col.default is not None
    assert col.default.arg is False


def test_outreach_draft_defaults_to_draft():
    """OutreachDraftRecord.status must default to 'draft'."""
    from db.models import OutreachDraftRecord

    col = OutreachDraftRecord.__table__.c.status
    assert col.default is not None
    assert col.default.arg == "draft", f"Expected 'draft', got {col.default.arg}"


def test_outbound_mode_defaults_to_draft_only():
    """OutboundMessageRecord.mode must default to 'draft_only'."""
    from db.models import OutboundMessageRecord

    col = OutboundMessageRecord.__table__.c.mode
    assert col.default is not None
    assert col.default.arg == "draft_only"


def test_safe_env_boot():
    """Backend must boot under safe env with the new models."""
    os.environ.setdefault("APP_ENV", "test")
    os.environ.setdefault("ENVIRONMENT", "test")
    os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./dealix_db_safety_test.db")
    os.environ.setdefault("APP_SECRET_KEY", "test-secret")
    os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")
    os.environ.setdefault("API_KEYS", "test")
    os.environ.setdefault("ADMIN_API_KEYS", "admin")
    os.environ.setdefault("EXTERNAL_SEND_ENABLED", "false")
    os.environ.setdefault("OUTBOUND_MODE", "draft_only")

    from api.main import app

    assert app is not None


def test_foundation_pr_is_additive_by_contract():
    """The database foundation PR is ORM-only and intentionally migration-free."""
    from db.models import Base

    table_names = {mapper.local_table.name for mapper in Base.registry.mappers if mapper.local_table is not None}
    expected_tables = {
        "prospects",
        "outreach_drafts",
        "outbound_messages",
        "outbound_events",
        "deals_pipeline",
        "proposals",
        "clients",
        "client_projects",
        "proof_reports",
    }
    assert expected_tables.issubset(table_names)
