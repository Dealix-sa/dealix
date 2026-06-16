"""Routes messages to the correct provider by channel."""

from __future__ import annotations

from app.outbound.config import OutboundSettings
from app.outbound.email_sender import EmailSender
from app.outbound.models import Channel, OutboundContact, OutboundMessage, SendResult
from app.outbound.whatsapp_sender import WhatsAppSender


class ProviderRouter:
    """Dispatches an outbound message to the right sender."""

    def __init__(self, settings: OutboundSettings | None = None) -> None:
        self.settings = settings or OutboundSettings()
        self._email = EmailSender(self.settings)
        self._whatsapp = WhatsAppSender(self.settings)

    def send(
        self,
        contact: OutboundContact,
        message: OutboundMessage,
        dry_run: bool = False,
    ) -> SendResult:
        if message.channel == Channel.EMAIL:
            return self._email.send(contact, message, dry_run=dry_run)
        if message.channel == Channel.WHATSAPP:
            return self._whatsapp.send(contact, message, dry_run=dry_run)
        return SendResult(
            message_id=message.id,
            channel=message.channel,
            status="failed",
            error_message=f"Unsupported channel: {message.channel}",
            dry_run=dry_run,
        )
