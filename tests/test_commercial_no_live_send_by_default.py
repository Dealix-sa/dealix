"""No channel may go live by default; live needs flags + approval + gates."""

from __future__ import annotations

import pytest

from app.commercial import safety


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    yield


def _verified_account(**kw):
    base = {
        "source_url": "https://example.com",
        "verification_status": "verified",
        "contactability_status": "contactable",
        "whatsapp_opt_in": True,
        "email_opt_out": False,
    }
    base.update(kw)
    return base


def _approved_action(**kw):
    base = {
        "message_status": "approved",
        "owner_decision": "send",
        "text": "Hi, can we talk?",
        "has_unsubscribe": True,
    }
    base.update(kw)
    return base


def test_email_denied_by_default():
    d = safety.can_send_email(_approved_action(), _verified_account())
    assert d.allowed is False
    assert any("draft_only" in b or "EXTERNAL_SEND_ENABLED" in b for b in d.blocked_by)


def test_whatsapp_denied_by_default():
    d = safety.can_send_whatsapp(_approved_action(), _verified_account())
    assert d.allowed is False


def test_whatsapp_requires_opt_in_even_when_live(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("WHATSAPP_SEND_ENABLED", "true")
    monkeypatch.setenv("WHATSAPP_ALLOW_LIVE_SEND", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    d = safety.can_send_whatsapp(
        _approved_action(), _verified_account(whatsapp_opt_in=False)
    )
    assert d.allowed is False
    assert any("opt-in" in b for b in d.blocked_by)


def test_email_can_go_live_when_all_gates_pass(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    d = safety.can_send_email(
        _approved_action(), _verified_account(), client_rules={"allowed_channels": ["email"]}
    )
    assert d.allowed is True


def test_email_blocked_without_unsubscribe(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    d = safety.can_send_email(
        _approved_action(has_unsubscribe=False),
        _verified_account(),
        client_rules={"allowed_channels": ["email"]},
    )
    assert d.allowed is False
    assert any("unsubscribe" in b for b in d.blocked_by)


def test_blocked_claim_stops_live_send(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    d = safety.can_send_email(
        _approved_action(text="We guarantee 10x ROI"),
        _verified_account(),
        client_rules={"allowed_channels": ["email"]},
    )
    assert d.allowed is False
    assert any("blocked claim" in b for b in d.blocked_by)


def test_unverified_account_cannot_send(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    d = safety.can_send_email(
        _approved_action(),
        _verified_account(verification_status="unverified"),
        client_rules={"allowed_channels": ["email"]},
    )
    assert d.allowed is False
