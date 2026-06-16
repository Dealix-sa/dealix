"""Email messages must contain an unsubscribe mechanism."""

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
        outbound_require_opt_out=True,
        email_send_enabled=True,
        email_send_mode="live",
        email_require_unsubscribe=True,
    )


@pytest.fixture
def contact() -> OutboundContact:
    return OutboundContact(
        company_name="Test Co",
        email="test@example.sa",
        source_url="https://example.sa",
        verification_status="verified",
    )


def test_email_with_unsubscribe_passes(settings, contact):
    gate = PolicyGate(settings)
    msg = OutboundMessage(
        contact_id=contact.id,
        channel=Channel.EMAIL,
        body="Hello. unsubscribe: https://dealix.me/unsubscribe",
    )
    assert gate.evaluate(contact, msg).ok


def test_email_with_arabic_opt_out_passes(settings, contact):
    gate = PolicyGate(settings)
    msg = OutboundMessage(
        contact_id=contact.id,
        channel=Channel.EMAIL,
        body="مرحبا. لإلغاء الاشتراك: https://dealix.me/unsubscribe",
    )
    assert gate.evaluate(contact, msg).ok


def test_email_without_unsubscribe_blocked(settings, contact):
    gate = PolicyGate(settings)
    msg = OutboundMessage(
        contact_id=contact.id,
        channel=Channel.EMAIL,
        body="Hello, this is a pitch.",
    )
    verdict = gate.evaluate(contact, msg)
    assert not verdict.ok
    assert "unsubscribe" in verdict.reason or "opt-out" in verdict.reason
