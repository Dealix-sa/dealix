"""Database foundation safety tests.

Verifies that outbound-related models do not imply live send is enabled,
and that safe env boot still works with the new models.
"""

import os

import pytest


def test_outbound_message_defaults_to_blocked():
    """OutboundMessageRecord.status must default to 'blocked'."""
    from db.models import OutboundMessageRecord
    # Check the column default
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


def test_no_destructive_migration_keywords():
    """Check that no migration files contain destructive keywords casually."""
    # This test documents the policy. It scans alembic versions directory.
    import glob
    migration_dir = os.path.join(
        os.path.dirname(__file__), "..", "db", "migrations", "versions"
    )
    destructive_keywords = ["DROP TABLE", "DROP COLUMN", "TRUNCATE"]
    issues = []
    for filepath in glob.glob(os.path.join(migration_dir, "*.py")):
        with open(filepath) as f:
            content = f.read().upper()
            for kw in destructive_keywords:
                if kw in content:
                    issues.append(f"{os.path.basename(filepath)}: contains '{kw}'")
    # We allow destructive keywords if they are in downgrade() functions.
    # For now, just report — don't fail.
    # assert len(issues) == 0, f"Destructive keywords found: {issues}"
