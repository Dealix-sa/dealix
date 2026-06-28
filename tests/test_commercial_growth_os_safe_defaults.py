"""The Commercial Growth OS must be safe-by-default (fail-closed)."""

from __future__ import annotations

import pytest

from app.commercial import safety


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    yield


def test_default_environment_is_safe():
    assert safety.is_safe_default_environment() is True


def test_default_outbound_mode_is_draft_only():
    assert safety.outbound_mode() == "draft_only"
    assert safety.is_controlled_live() is False


def test_all_send_flags_default_false():
    s = safety.safe_defaults()
    assert s["external_send_enabled"] is False
    assert s["email_send_enabled"] is False
    assert s["whatsapp_send_enabled"] is False
    assert s["whatsapp_allow_live_send"] is False
    assert s["sms_send_enabled"] is False
    assert s["calendar_write_enabled"] is False
    assert s["proposal_finalization_enabled"] is False


def test_flag_set_breaks_safe_default(monkeypatch):
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")
    assert safety.is_safe_default_environment() is False
