"""Guaranteed ROI claims are blocked."""

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
        outbound_block_guaranteed_roi=True,
        email_send_enabled=True,
        email_send_mode="live",
        email_require_unsubscribe=False,
    )


@pytest.fixture
def contact() -> OutboundContact:
    return OutboundContact(
        company_name="Test Co",
        email="test@example.sa",
        source_url="https://example.sa",
        verification_status="verified",
    )


@pytest.mark.parametrize(
    "body",
    [
        "ضمان عائد 100%",
        "نضمن لك مضمون ربح",
        "guaranteed ROI in 30 days",
        "Double your revenue in 7 days",
    ],
)
def test_guaranteed_roi_blocked(settings, contact, body):
    gate = PolicyGate(settings)
    msg = OutboundMessage(contact_id=contact.id, channel=Channel.EMAIL, body=body)
    verdict = gate.evaluate(contact, msg)
    assert not verdict.ok
    assert "ROI" in verdict.reason or "overclaim" in verdict.reason


def test_no_guarantee_passes(settings, contact):
    gate = PolicyGate(settings)
    msg = OutboundMessage(
        contact_id=contact.id,
        channel=Channel.EMAIL,
        body="We can help you organize follow-ups and improve response rates.",
    )
    assert gate.evaluate(contact, msg).ok
