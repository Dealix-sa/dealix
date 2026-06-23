"""Consent registry — tracks explicit opt-in consent per channel.

Consent is required for WhatsApp (opt_in must be True) and SMS. For email,
consent is implied by an approved verification_status + source_url, but an
explicit ``email_opt_out=True`` overrides. This module centralises the consent
check so the policy gate can call a single function.

The registry is in-memory. Production deployments should persist consent
records (with timestamps and source) in a database, but the interface
(``has_consent`` / ``record_consent`` / ``withdraw_consent``) stays the same.
"""

from __future__ import annotations

import time
from threading import Lock
from typing import Any, Mapping

_LOCK = Lock()
# _CONSENT[identifier] = {channel: {"ts": float, "source": str}}
_CONSENT: dict[str, dict[str, dict[str, Any]]] = {}


def _norm(identifier: str) -> str:
    return (identifier or "").strip().lower()


def _identifier_for(channel: str, contact: Mapping[str, Any]) -> str:
    if channel == "email":
        return str(contact.get("email", ""))
    if channel == "whatsapp":
        return str(contact.get("whatsapp", ""))
    if channel == "sms":
        return str(contact.get("phone", ""))
    return str(contact.get("email") or contact.get("whatsapp") or contact.get("phone") or "")


def has_consent(channel: str, contact: Mapping[str, Any]) -> bool:
    """True if explicit or implicit consent exists for the channel/contact.

    Rules:
      - email: explicit consent OR (verification_status == "approved_to_send"
                AND not email_opt_out)
      - whatsapp: contact.whatsapp_opt_in is True
      - sms: explicit consent recorded OR contact.sms_opt_in is True
    """
    ident = _norm(_identifier_for(channel, contact))
    with _LOCK:
        entry = _CONSENT.get(ident, {})
        if channel in entry:
            return True

    # Fall back to contact-level flags.
    if channel == "email":
        if contact.get("email_opt_out") is True:
            return False
        return contact.get("verification_status") == "approved_to_send"
    if channel == "whatsapp":
        return contact.get("whatsapp_opt_in") is True
    if channel == "sms":
        return contact.get("sms_opt_in") is True
    return False


def record_consent(channel: str, contact: Mapping[str, Any], source: str = "manual") -> None:
    """Record explicit consent for a channel/contact."""
    ident = _norm(_identifier_for(channel, contact))
    if not ident:
        return
    with _LOCK:
        _CONSENT.setdefault(ident, {})[channel] = {
            "ts": time.time(),
            "source": source,
        }


def withdraw_consent(channel: str, contact: Mapping[str, Any]) -> None:
    """Withdraw consent for a channel/contact."""
    ident = _norm(_identifier_for(channel, contact))
    with _LOCK:
        entry = _CONSENT.get(ident)
        if entry:
            entry.pop(channel, None)
            if not entry:
                _CONSENT.pop(ident, None)


def clear_consent() -> None:
    """Clear all consent state (used by tests)."""
    with _LOCK:
        _CONSENT.clear()


def consent_record(channel: str, contact: Mapping[str, Any]) -> dict[str, Any] | None:
    """Return the stored consent record (or None) for inspection."""
    ident = _norm(_identifier_for(channel, contact))
    with _LOCK:
        return _CONSENT.get(ident, {}).get(channel)