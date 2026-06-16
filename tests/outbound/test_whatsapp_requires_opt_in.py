"""WhatsApp messages require explicit opt-in."""

from __future__ import annotations

import pytest

from app.outbound.config import OutboundSettings
from app.outbound.models import Channel, OutboundContact, OutboundMessage
from app.outbound.policy_gate import PolicyGate


@pytest.fixture
def settings() -> OutboundSettings:
    return OutboundSettings(
        external_send_enabled=True,
        outbound_mode="controlled_live",
        outbound_require_approval=False,
        outbound_require_verified_target=True,
        outbound_require_source_url=True,
        whatsapp_send_enabled=True,
        whatsapp_allow_live_send=True,
        whatsapp_require_opt_in=True,
        whatsapp_require_approved_template=True,
    )


@pytest.fixture
def contact() -> OutboundContact:
    return OutboundContact(
        company_name="Test Co",
        phone="+966501234567",
        whatsapp="+966501234567",
        source_url="https://example.sa",
        verification_status="verified",
        whatsapp_opt_in=True,
    )


def test_whatsapp_with_optin_and_template_passes(settings, contact):
    gate = PolicyGate(settings)
    msg = OutboundMessage(
        contact_id=contact.id,
        channel=Channel.WHATSAPP,
        body="مرحبا",
        template_name="dealix_intro_ar",
    )
    assert gate.evaluate(contact, msg).ok


def test_whatsapp_without_optin_blocked(settings, contact):
    contact.whatsapp_opt_in = False
    gate = PolicyGate(settings)
    msg = OutboundMessage(
        contact_id=contact.id,
        channel=Channel.WHATSAPP,
        body="مرحبا",
        template_name="dealix_intro_ar",
    )
    verdict = gate.evaluate(contact, msg)
    assert not verdict.ok
    assert "opt-in" in verdict.reason


def test_whatsapp_without_template_blocked(settings, contact):
    gate = PolicyGate(settings)
    msg = OutboundMessage(
        contact_id=contact.id,
        channel=Channel.WHATSAPP,
        body="مرحبا",
    )
    verdict = gate.evaluate(contact, msg)
    assert not verdict.ok
    assert "template" in verdict.reason
