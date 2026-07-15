"""Channel adapter — channel identifiers and CSV-row flattening helpers.

Keeps channel names in one place and flattens per-channel drafts into the rows
written to the email/whatsapp draft CSVs.
"""

from __future__ import annotations

from typing import Any

from dealix.conversation_engine import company_brain

EMAIL = "email"
WHATSAPP = "whatsapp"
LINKEDIN = "linkedin"
CALL = "call"

ALL_CHANNELS = (EMAIL, WHATSAPP, LINKEDIN, CALL)


def channel_requires_approval(channel: str) -> bool:
    cfg = company_brain.channels().get(channel, {})
    # Default to True — approval is the safe default for any external channel.
    return bool(cfg.get("requires_approval", True))


def channel_allows_cold(channel: str) -> bool:
    cfg = company_brain.channels().get(channel, {})
    return bool(cfg.get("allow_cold", False))


def _one_line(text: str) -> str:
    return " ".join(str(text).split())


def email_csv_row(company: str, contact: str, email_draft: dict[str, Any]) -> dict[str, str]:
    return {
        "company": company,
        "contact_name": contact,
        "from_email": str(email_draft.get("from_email", company_brain.founder_email())),
        "subject": str(email_draft.get("subject", "")),
        "short_version": _one_line(email_draft.get("short_version", "")),
        "cta": _one_line(email_draft.get("cta", "")),
        "approval_required": "true",
        "status": "pending_founder_approval",
    }


def whatsapp_csv_row(company: str, contact: str, wa_draft: dict[str, Any]) -> dict[str, str]:
    return {
        "company": company,
        "contact_name": contact,
        "opening_message": _one_line(wa_draft.get("opening_message", "")),
        "short_value_message": _one_line(wa_draft.get("short_value_message", "")),
        "permission_cta": _one_line(wa_draft.get("permission_cta", "")),
        "cold_send_forbidden": "true",
        "approval_required": "true",
        "status": "pending_founder_approval",
    }
