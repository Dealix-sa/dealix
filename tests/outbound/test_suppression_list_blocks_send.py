"""Suppressed contacts must not be sent to."""

from __future__ import annotations

import pytest

from app.outbound.models import Channel, OutboundContact, OutboundMessage
from app.outbound.runner import ControlledOutboundRunner
from app.outbound.storage import CSVOutboundStorage


@pytest.fixture
def runner(tmp_path):
    storage = CSVOutboundStorage(base_dir=tmp_path / "outbound")
    return ControlledOutboundRunner(storage=storage)


def test_email_opt_out_blocks_send(runner):
    contact = OutboundContact(
        company_name="Test Co",
        email="test@example.sa",
        source_url="https://example.sa",
        verification_status="verified",
        email_opt_out=True,
    )
    runner.storage.save_contact(contact)
    msg = OutboundMessage(
        contact_id=contact.id,
        channel=Channel.EMAIL,
        body="Hello. unsubscribe: https://dealix.me/unsubscribe",
    )
    runner.storage.save_message(msg)
    result = runner.process_one(msg, dry_run=True)
    assert result.status == "failed"
    assert "Suppressed" in result.error_message


def test_whatsapp_opt_out_blocks_send(runner):
    contact = OutboundContact(
        company_name="Test Co",
        phone="+966501234567",
        whatsapp="+966501234567",
        source_url="https://example.sa",
        verification_status="verified",
        whatsapp_opt_in=True,
        whatsapp_opt_out=True,
    )
    runner.storage.save_contact(contact)
    msg = OutboundMessage(
        contact_id=contact.id,
        channel=Channel.WHATSAPP,
        body="مرحبا",
        template_name="dealix_intro_ar",
    )
    runner.storage.save_message(msg)
    result = runner.process_one(msg, dry_run=True)
    assert result.status == "failed"
    assert "Suppressed" in result.error_message
