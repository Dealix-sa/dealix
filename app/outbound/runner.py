"""Main orchestrator for controlled live outbound."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from datetime import UTC, datetime

from app.outbound.config import OutboundSettings
from app.outbound.models import (
    Channel,
    MessageStatus,
    OutboundContact,
    OutboundEvent,
    OutboundMessage,
    PolicyVerdict,
    SendResult,
)
from app.outbound.policy_gate import PolicyGate
from app.outbound.provider_router import ProviderRouter
from app.outbound.rate_limiter import RateLimiter
from app.outbound.storage import OutboundStorage, get_default_storage
from app.outbound.suppression import is_suppressed

logger = logging.getLogger(__name__)


class ControlledOutboundRunner:
    """Run the controlled outbound pipeline: load drafts, gate, rate-limit, send, log."""

    def __init__(
        self,
        settings: OutboundSettings | None = None,
        storage: OutboundStorage | None = None,
        gate: PolicyGate | None = None,
        limiter: RateLimiter | None = None,
        router: ProviderRouter | None = None,
    ) -> None:
        self.settings = settings or OutboundSettings()
        self.storage = storage or get_default_storage()
        self.gate = gate or PolicyGate(self.settings)
        self.limiter = limiter or RateLimiter(self.settings)
        self.router = router or ProviderRouter(self.settings)

    def load_drafts(
        self,
        channel: Channel | None = None,
        status: MessageStatus = MessageStatus.DRAFT,
        limit: int = 1000,
    ) -> Sequence[OutboundMessage]:
        return self.storage.list_messages(status=status, channel=channel, limit=limit)

    def approve(self, message_id: str, approved_by: str) -> OutboundMessage | None:
        message = self.storage.get_message(message_id)
        if not message:
            return None
        message = self.gate.approve(message, approved_by)
        return self.storage.save_message(message)

    def process_one(
        self,
        message: OutboundMessage,
        dry_run: bool = False,
        approved_by: str | None = None,
    ) -> SendResult:
        """Process a single message through gates, limits, provider, and logging."""
        contact = self.storage.get_contact(message.contact_id)
        if not contact:
            return self._fail(message, "Contact not found")

        # Suppression list check
        suppressed, reason = is_suppressed(contact, message.channel)
        if suppressed:
            return self._fail(message, f"Suppressed: {reason}")

        # Policy gate
        verdict = self.gate.evaluate(contact, message, approved_by=approved_by)
        if not verdict.ok:
            return self._fail(message, f"Policy gate blocked: {verdict.reason}")

        # Rate limiter
        ok, limit_reason = self.limiter.can_send(message.channel)
        if not ok:
            return self._fail(message, f"Rate limited: {limit_reason}")

        # Send via provider
        result = self.router.send(contact, message, dry_run=dry_run)

        # Update message record
        message.status = result.status
        message.provider_message_id = result.provider_message_id
        message.error_message = result.error_message
        if result.status == "sent":
            message.sent_at = datetime.now(UTC)
            self.limiter.record_send(message.channel)
        self.storage.save_message(message)

        # Log event
        self.storage.save_event(
            OutboundEvent(
                message_id=message.id,
                event_type="sent" if result.status == "sent" else "failed",
                payload={
                    "channel": message.channel,
                    "dry_run": result.dry_run,
                    "provider_message_id": result.provider_message_id,
                    "error_message": result.error_message,
                    "verdict": verdict.reason,
                },
            )
        )

        return result

    def process_batch(
        self,
        messages: Sequence[OutboundMessage],
        dry_run: bool = False,
        approved_by: str | None = None,
    ) -> list[SendResult]:
        """Process a batch, respecting batch and daily limits."""
        if not messages:
            return []
        channel = messages[0].channel
        ok, reason = self.limiter.check_batch(channel, len(messages))
        if not ok:
            logger.warning("Batch rejected: %s", reason)
            return [
                SendResult(
                    message_id=m.id,
                    channel=m.channel,
                    status="failed",
                    error_message=reason,
                    dry_run=dry_run,
                )
                for m in messages
            ]
        return [self.process_one(m, dry_run=dry_run, approved_by=approved_by) for m in messages]

    def run_drafts(
        self,
        channel: Channel | None = None,
        dry_run: bool = False,
        approved_by: str | None = None,
        limit: int = 1000,
    ) -> dict:
        """Load all drafts and attempt to send them."""
        drafts = self.load_drafts(channel=channel, limit=limit)
        results = self.process_batch(drafts, dry_run=dry_run, approved_by=approved_by)
        sent = sum(1 for r in results if r.status == "sent")
        failed = sum(1 for r in results if r.status == "failed")
        return {
            "dry_run": dry_run,
            "total": len(results),
            "sent": sent,
            "failed": failed,
            "remaining": self.limiter.summary(),
        }

    def handle_reply(self, message_id: str, reply_text: str) -> OutboundMessage | None:
        """Classify a reply and update the message + contact records."""
        message = self.storage.get_message(message_id)
        if not message:
            return None
        message.status = "replied"
        message.replied_at = datetime.now(UTC)
        self.storage.save_message(message)

        event_payload: dict = {"reply_text": reply_text}
        lowered = reply_text.lower()
        if any(k in lowered for k in ("unsubscribe", "إلغاء", "إيقاف", "stop")):
            contact = self.storage.get_contact(message.contact_id)
            if contact:
                if message.channel == Channel.EMAIL:
                    contact.email_opt_out = True
                elif message.channel == Channel.WHATSAPP:
                    contact.whatsapp_opt_out = True
                self.storage.save_contact(contact)
            event_payload["opt_out"] = True

        self.storage.save_event(
            OutboundEvent(
                message_id=message.id,
                event_type="reply",
                payload=event_payload,
            )
        )
        return message

    def _fail(self, message: OutboundMessage, error: str) -> SendResult:
        message.status = "failed"
        message.error_message = error
        self.storage.save_message(message)
        self.storage.save_event(
            OutboundEvent(
                message_id=message.id,
                event_type="failed",
                payload={"error": error},
            )
        )
        logger.warning("Message %s failed: %s", message.id, error)
        return SendResult(
            message_id=message.id,
            channel=message.channel,
            status="failed",
            error_message=error,
            dry_run=False,
        )
