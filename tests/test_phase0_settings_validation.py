"""Phase 0 — autonomous distribution foundation settings.

Validates that the new Phase 0 fields exist on Settings, default to the
safest possible value, and that the live-mode composite gate behaves
correctly.

Plan ref: /root/.claude/plans/typed-brewing-pebble.md (Phase 0).
Non-Negotiable #6: NO live charge without approval.
"""

from __future__ import annotations

from core.config.settings import Settings


def test_phase0_fields_present():
    """All Phase 0 fields must exist on Settings."""
    fields = Settings.model_fields
    required = [
        "moyasar_secret_key",
        "moyasar_public_key",
        "moyasar_webhook_secret",
        "moyasar_mode",
        "moyasar_live_verified",
        "scheduler_backend",
        "ksa_residency_enforce",
        "ksa_residency_allowlist",
        "email_deliverability_ok",
        "sbom_sign_key_id",
        "offers_self_serve_enabled",
        "sprint_auto_delivery",
        "subscriptions_auto_renew",
        "partners_portal_enabled",
    ]
    missing = [f for f in required if f not in fields]
    assert not missing, f"Missing Phase 0 fields on Settings: {missing}"


def test_moyasar_mode_defaults_to_test():
    """Mode must default to test — never live."""
    assert Settings().moyasar_mode == "test"


def test_moyasar_live_verified_defaults_false():
    """Live verification must default to False."""
    assert Settings().moyasar_live_verified is False


def test_moyasar_live_enabled_composite_gate():
    """moyasar_live_enabled is True only when BOTH mode==live AND verified==True."""
    s = Settings()
    assert s.moyasar_live_enabled is False  # both default False
    # Cannot just set attributes (Pydantic v2 model is frozen by default
    # only when configured so). Re-instantiate with overrides.
    s_live_only = Settings(moyasar_mode="live", moyasar_live_verified=False)
    assert s_live_only.moyasar_live_enabled is False
    s_verified_only = Settings(moyasar_mode="test", moyasar_live_verified=True)
    assert s_verified_only.moyasar_live_enabled is False
    s_both = Settings(moyasar_mode="live", moyasar_live_verified=True)
    assert s_both.moyasar_live_enabled is True


def test_scheduler_backend_defaults_apscheduler():
    """Default scheduler is in-process APScheduler (with Postgres jobstore)."""
    assert Settings().scheduler_backend == "apscheduler"


def test_self_serve_flags_default_off():
    """All Phase 1-4 self-serve flags must default to OFF for safety."""
    s = Settings()
    assert s.offers_self_serve_enabled is False
    assert s.sprint_auto_delivery is False
    assert s.subscriptions_auto_renew is False
    assert s.partners_portal_enabled is False


def test_ksa_residency_defaults_safe():
    """Residency enforcement off-by-default; allowlist empty."""
    s = Settings()
    assert s.ksa_residency_enforce is False
    assert s.ksa_residency_allowlist == ""
    assert s.ksa_residency_hosts == []


def test_ksa_residency_parsing():
    """Comma-separated allowlist parses to a stripped list."""
    s = Settings(ksa_residency_allowlist="db1.ksa.example, db2.ksa.example , db3.ksa.example")
    assert s.ksa_residency_hosts == ["db1.ksa.example", "db2.ksa.example", "db3.ksa.example"]


def test_email_deliverability_defaults_false():
    """SPF/DKIM/DMARC attestation defaults False — must be explicitly set."""
    assert Settings().email_deliverability_ok is False
