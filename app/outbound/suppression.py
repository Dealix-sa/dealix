"""Suppression list checks for email and WhatsApp."""

from __future__ import annotations

from app.outbound.models import Channel, OutboundContact

# Normalized stop keywords for email + WhatsApp.
STOP_KEYWORDS = {
    "stop",
    "unsubscribe",
    "cancel",
    "إيقاف",
    "الغاء",
    "إلغاء",
    "توقف",
    "لا ترسل",
    "remove",
    "opt out",
    "opt-out",
}


def is_suppressed(contact: OutboundContact, channel: Channel) -> tuple[bool, str]:
    """Return (True, reason) if the contact is suppressed on this channel."""
    if channel == Channel.EMAIL:
        if contact.email_opt_out:
            return True, "email_opt_out=true"
        if not contact.email:
            return True, "no email address"
    if channel == Channel.WHATSAPP:
        if contact.whatsapp_opt_out:
            return True, "whatsapp_opt_out=true"
        if not contact.whatsapp and not contact.phone:
            return True, "no phone/whatsapp number"
    return False, ""


def contains_stop_request(text: str) -> bool:
    """Detect opt-out/stop language in a reply."""
    lowered = text.lower()
    return any(keyword in lowered for keyword in STOP_KEYWORDS)
