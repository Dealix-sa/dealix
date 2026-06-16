"""Every send attempt must create an event record."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from app.outbound.config import OutboundSettings
from app.outbound.models import Channel, OutboundContact, OutboundMessage
from app.outbound.runner import ControlledOutboundRunner
from app.outbound.storage import CSVOutboundStorage


@pytest.fixture
def runner(tmp_path):
    settings = OutboundSettings(
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
    storage = CSVOutboundStorage(base_dir=tmp_path / "outbound")
    return ControlledOutboundRunner(settings=settings, storage=storage)


def test_send_event_logged(runner, tmp_path):
    contact = OutboundContact(
        company_name="Test Co",
        email="test@example.sa",
        source_url="https://example.sa",
        verification_status="verified",
    )
    runner.storage.save_contact(contact)
    msg = OutboundMessage(
        contact_id=contact.id,
        channel=Channel.EMAIL,
        body="Hello. unsubscribe: https://dealix.me/unsubscribe",
    )
    runner.storage.save_message(msg)
    runner.process_one(msg, dry_run=True)

    events_path = tmp_path / "outbound" / "events.csv"
    with events_path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["message_id"] == msg.id
    assert rows[0]["event_type"] == "sent"


def test_failed_event_logged(runner, tmp_path):
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
    runner.process_one(msg, dry_run=True)

    events_path = tmp_path / "outbound" / "events.csv"
    with events_path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["event_type"] == "failed"
