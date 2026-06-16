"""Rate limits must be enforced."""

from __future__ import annotations

import pytest

from app.outbound.config import OutboundSettings
from app.outbound.models import Channel, OutboundContact, OutboundMessage
from app.outbound.rate_limiter import RateLimiter
from app.outbound.runner import ControlledOutboundRunner
from app.outbound.storage import CSVOutboundStorage


@pytest.fixture
def limited_runner(tmp_path):
    settings = OutboundSettings(
        external_send_enabled=True,
        outbound_mode="controlled_live",
        outbound_require_approval=False,
        outbound_require_verified_target=True,
        outbound_require_source_url=True,
        outbound_require_opt_out=True,
        email_send_enabled=True,
        email_send_mode="live",
        email_daily_limit=2,
        email_batch_limit=2,
        email_min_seconds_between_sends=0,
        email_require_unsubscribe=True,
    )
    storage = CSVOutboundStorage(base_dir=tmp_path / "outbound")
    return ControlledOutboundRunner(settings=settings, storage=storage)


def test_daily_email_limit_enforced(limited_runner):
    contact = OutboundContact(
        company_name="Test Co",
        email="test@example.sa",
        source_url="https://example.sa",
        verification_status="verified",
    )
    limited_runner.storage.save_contact(contact)

    for i in range(3):
        msg = OutboundMessage(
            contact_id=contact.id,
            channel=Channel.EMAIL,
            body=f"Hello {i}. unsubscribe: https://dealix.me/unsubscribe",
        )
        limited_runner.storage.save_message(msg)

    results = [limited_runner.process_one(msg, dry_run=True) for msg in limited_runner.load_drafts()]
    sent = [r for r in results if r.status == "sent"]
    failed = [r for r in results if r.status == "failed"]
    assert len(sent) == 2
    assert len(failed) == 1
    assert "Daily limit" in failed[0].error_message


def test_batch_limit_rejected(limited_runner):
    contact = OutboundContact(
        company_name="Test Co",
        email="test@example.sa",
        source_url="https://example.sa",
        verification_status="verified",
    )
    limited_runner.storage.save_contact(contact)
    messages = []
    for i in range(5):
        msg = OutboundMessage(
            contact_id=contact.id,
            channel=Channel.EMAIL,
            body=f"Hello {i}. unsubscribe: https://dealix.me/unsubscribe",
        )
        limited_runner.storage.save_message(msg)
        messages.append(msg)
    results = limited_runner.process_batch(messages, dry_run=True)
    assert all(r.status == "failed" for r in results)
    assert "Batch size" in results[0].error_message


def test_rate_limiter_summary():
    settings = OutboundSettings(email_daily_limit=10, whatsapp_daily_limit=5)
    limiter = RateLimiter(settings)
    assert limiter.remaining_today(Channel.EMAIL) == 10
    assert limiter.remaining_today(Channel.WHATSAPP) == 5
