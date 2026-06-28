"""Multi-channel preparation: correct payloads, correct gating, no send."""

from __future__ import annotations

import pytest

from app.commercial import channels, safety
from app.commercial.schemas import CommercialAccount


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    yield


def _account(**kw):
    base = dict(
        account_id="a1",
        company_name="Acme",
        source_url="https://x.sa/c",
        source_type="client_provided",
        verification_status="verified",
        contactability_status="contactable",
        public_email="a@x.sa",
        whatsapp="+966500000000",
        whatsapp_opt_in=True,
    )
    base.update(kw)
    return CommercialAccount(**base)


_DRAFT = {"body_ar": "مرحبا", "body_en": "hello", "owner_decision": "pending"}


def test_email_always_has_unsubscribe():
    p = channels.prepare_email(
        conversation_id="c1", account_id="a1", draft=_DRAFT, account=_account()
    )
    assert "List-Unsubscribe" in p.headers
    assert "unsubscribe" in p.body_en.lower() or "STOP" in p.body_en
    assert p.send_status == "draft"  # draft-only env


def test_whatsapp_caps_buttons():
    p = channels.prepare_whatsapp(
        conversation_id="c1", account_id="a1", draft=_DRAFT, account=_account(),
        buttons=[{"id": f"b{i}", "title": f"opt {i}"} for i in range(5)],
    )
    assert len(p.buttons) == 3


def test_linkedin_is_manual_only_and_blocked():
    p = channels.prepare_linkedin(
        conversation_id="c1", account_id="a1", draft=_DRAFT, account=_account()
    )
    assert p.channel == "linkedin_manual"
    assert p.safety["allowed"] is False
    assert p.manual_instructions


def test_unknown_channel_is_blocked():
    p = channels.prepare_for_channel(
        "telegram", conversation_id="c1", account_id="a1", draft=_DRAFT, account=_account()
    )
    assert p.send_status == "blocked"
    assert p.safety["allowed"] is False


def test_email_can_be_approved_only_when_fully_gated(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "true")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    draft = {**_DRAFT, "message_status": "approved", "owner_decision": "send"}
    p = channels.prepare_email(
        conversation_id="c1", account_id="a1", draft=draft, account=_account(),
        client_rules={"allowed_channels": ["email"]},
    )
    assert p.safety["allowed"] is True
    assert p.send_status == "approved"
