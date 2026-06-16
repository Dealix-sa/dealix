"""Email sender abstraction with dry-run support."""

from __future__ import annotations

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from app.outbound.config import OutboundSettings
from app.outbound.models import Channel, OutboundContact, OutboundMessage, SendResult


class EmailSender:
    """Send emails via SMTP; supports dry-run."""

    def __init__(self, settings: OutboundSettings | None = None) -> None:
        self.settings = settings or OutboundSettings()

    def send(
        self,
        contact: OutboundContact,
        message: OutboundMessage,
        dry_run: bool = False,
    ) -> SendResult:
        if not contact.email:
            return SendResult(
                message_id=message.id,
                channel=Channel.EMAIL,
                status="failed",
                error_message="Contact has no email address",
                dry_run=dry_run,
            )

        if dry_run or not self.settings.live_email_allowed:
            return SendResult(
                message_id=message.id,
                channel=Channel.EMAIL,
                status="sent",
                provider_message_id=f"DRY-RUN-EMAIL-{message.id}",
                dry_run=True,
            )

        try:
            provider_message_id = self._send_smtp(contact, message)
            return SendResult(
                message_id=message.id,
                channel=Channel.EMAIL,
                status="sent",
                provider_message_id=provider_message_id,
                dry_run=False,
            )
        except Exception as exc:  # pragma: no cover - exercised via mocks in tests
            return SendResult(
                message_id=message.id,
                channel=Channel.EMAIL,
                status="failed",
                error_message=str(exc),
                dry_run=False,
            )

    def _send_smtp(self, contact: OutboundContact, message: OutboundMessage) -> str:
        if not self.settings.smtp_host or not self.settings.smtp_user:
            raise RuntimeError("SMTP_HOST and SMTP_USER required for live email send")

        msg = MIMEText(message.body, "plain", "utf-8")
        msg["Subject"] = message.subject or "Dealix"
        msg["From"] = formataddr(("Dealix", self.settings.email_default_from))
        msg["To"] = contact.email
        if self.settings.email_reply_to:
            msg["Reply-To"] = self.settings.email_reply_to

        with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port, timeout=30) as server:
            server.starttls()
            server.login(self.settings.smtp_user, self.settings.smtp_password)
            server.sendmail(
                self.settings.email_default_from,
                [contact.email],
                msg.as_string(),
            )
        return f"smtp-{message.id}"
