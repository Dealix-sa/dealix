"""WhatsApp sender abstraction using Meta Cloud API with dry-run support."""

from __future__ import annotations

import os

import requests

from app.outbound.config import OutboundSettings
from app.outbound.models import Channel, OutboundContact, OutboundMessage, SendResult


class WhatsAppSender:
    """Send WhatsApp messages via Meta Cloud API; template-only by default."""

    BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(self, settings: OutboundSettings | None = None) -> None:
        self.settings = settings or OutboundSettings()
        self.session = requests.Session()

    def send(
        self,
        contact: OutboundContact,
        message: OutboundMessage,
        dry_run: bool = False,
    ) -> SendResult:
        to_number = contact.whatsapp or contact.phone
        if not to_number:
            return SendResult(
                message_id=message.id,
                channel=Channel.WHATSAPP,
                status="failed",
                error_message="Contact has no phone/WhatsApp number",
                dry_run=dry_run,
            )

        if dry_run or not self.settings.live_whatsapp_allowed:
            return SendResult(
                message_id=message.id,
                channel=Channel.WHATSAPP,
                status="sent",
                provider_message_id=f"DRY-RUN-WA-{message.id}",
                dry_run=True,
            )

        try:
            provider_message_id = self._send_meta(to_number, message)
            return SendResult(
                message_id=message.id,
                channel=Channel.WHATSAPP,
                status="sent",
                provider_message_id=provider_message_id,
                dry_run=False,
            )
        except Exception as exc:  # pragma: no cover - exercised via mocks in tests
            return SendResult(
                message_id=message.id,
                channel=Channel.WHATSAPP,
                status="failed",
                error_message=str(exc),
                dry_run=False,
            )

    def _send_meta(self, to_number: str, message: OutboundMessage) -> str:
        phone_id = self.settings.meta_phone_number_id or os.getenv("META_PHONE_NUMBER_ID")
        token = self.settings.meta_wa_access_token or os.getenv("META_WA_ACCESS_TOKEN")
        if not phone_id or not token:
            raise RuntimeError("META_PHONE_NUMBER_ID and META_WA_ACCESS_TOKEN required")

        url = f"{self.BASE_URL}/{phone_id}/messages"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        if self.settings.whatsapp_send_mode == "template_only" or message.template_name:
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "template",
                "template": {
                    "name": message.template_name or "dealix_intro_ar",
                    "language": {"code": "ar"},
                },
            }
        else:
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "text",
                "text": {"body": message.body},
            }

        resp = self.session.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("messages", [{}])[0].get("id", f"wa-{message.id}")
