"""Tests for the controlled live outbound policy gate."""

from __future__ import annotations

import pytest

from app.outbound.config import OutboundSettings
from app.outbound.models import Channel, OutboundContact, OutboundMessage
from app.outbound.policy_gate import PolicyGate


@pytest.fixture
def base_settings() -> OutboundSettings:
    return OutboundSettings(
        external_send_enabled=True,
        outbound_mode="controlled_live",
        outbound_require_approval=True,
        outbound_require_verified_target=True,
        outbound_require_source_url=True,
        outbound_require_opt_out=True,
        outbound_block_fake_claims=True,
        outbound_block_guaranteed_roi=True,
        email_send_enabled=True,
        email_send_mode="live",
        whatsapp_send_enabled=True,
        whatsapp_allow_live_send=True,
    )


@pytest.fixture
def verified_contact() -> OutboundContact:
    return OutboundContact(
        company_name="Test Co",
        contact_name="Ali",
        email="ali@test.sa",
        phone="+966501234567",
        whatsapp="+966501234567",
        source_url="https://test.sa/about",
        verification_status="verified",
        confidence="high",
        whatsapp_opt_in=True,
    )


def test_approved_email_passes(base_settings, verified_contact):
    gate = PolicyGate(base_settings)
    msg = OutboundMessage(
        contact_id=verified_contact.id,
        channel=Channel.EMAIL,
        subject="Hello",
        body="Hello Ali, quick question. unsubscribe: https://dealix.me/unsubscribe",
    )
    msg = gate.approve(msg, "sami")
    verdict = gate.evaluate(verified_contact, msg, approved_by="sami")
    assert verdict.ok, verdict.reason


def test_unverified_target_blocked(base_settings, verified_contact):
    gate = PolicyGate(base_settings)
    verified_contact.verification_status = "unverified"
    msg = OutboundMessage(
        contact_id=verified_contact.id,
        channel=Channel.EMAIL,
        body="Hello. unsubscribe: https://dealix.me/unsubscribe",
    )
    verdict = gate.evaluate(verified_contact, msg, approved_by="sami")
    assert not verdict.ok
    assert "verification_status" in verdict.reason


def test_missing_source_url_blocked(base_settings, verified_contact):
    gate = PolicyGate(base_settings)
    verified_contact.source_url = ""
    msg = OutboundMessage(
        contact_id=verified_contact.id,
        channel=Channel.EMAIL,
        body="Hello. unsubscribe: https://dealix.me/unsubscribe",
    )
    msg = gate.approve(msg, "sami")
    verdict = gate.evaluate(verified_contact, msg, approved_by="sami")
    assert not verdict.ok
    assert "source_url" in verdict.reason


def test_missing_unsubscribe_blocked(base_settings, verified_contact):
    gate = PolicyGate(base_settings)
    msg = OutboundMessage(
        contact_id=verified_contact.id,
        channel=Channel.EMAIL,
        body="Hello Ali, quick question.",
    )
    msg = gate.approve(msg, "sami")
    verdict = gate.evaluate(verified_contact, msg, approved_by="sami")
    assert not verdict.ok
    assert "unsubscribe" in verdict.reason


def test_whatsapp_without_optin_blocked(base_settings, verified_contact):
    gate = PolicyGate(base_settings)
    verified_contact.whatsapp_opt_in = False
    msg = OutboundMessage(
        contact_id=verified_contact.id,
        channel=Channel.WHATSAPP,
        body="مرحبا",
        template_name="dealix_intro_ar",
    )
    msg = gate.approve(msg, "sami")
    verdict = gate.evaluate(verified_contact, msg, approved_by="sami")
    assert not verdict.ok
    assert "opt-in" in verdict.reason


def test_not_approved_blocked(base_settings, verified_contact):
    gate = PolicyGate(base_settings)
    msg = OutboundMessage(
        contact_id=verified_contact.id,
        channel=Channel.EMAIL,
        body="Hello. unsubscribe: https://dealix.me/unsubscribe",
    )
    verdict = gate.evaluate(verified_contact, msg)
    assert not verdict.ok
    assert "approved" in verdict.reason


def test_external_send_disabled_blocks(base_settings, verified_contact):
    base_settings.external_send_enabled = False
    gate = PolicyGate(base_settings)
    msg = OutboundMessage(
        contact_id=verified_contact.id,
        channel=Channel.EMAIL,
        body="Hello. unsubscribe: https://dealix.me/unsubscribe",
    )
    msg = gate.approve(msg, "sami")
    verdict = gate.evaluate(verified_contact, msg, approved_by="sami")
    assert not verdict.ok
    assert "EXTERNAL_SEND_ENABLED" in verdict.reason
