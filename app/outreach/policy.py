from __future__ import annotations

import os
from dataclasses import dataclass


def _true(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class OutreachDecision:
    allowed: bool
    reasons: list[str]


def can_send_email(row: dict[str, str], env: dict[str, str] | None = None) -> OutreachDecision:
    env = env or os.environ
    reasons: list[str] = []

    if not _true(env.get("EMAIL_SEND_ENABLED")):
        reasons.append("EMAIL_SEND_ENABLED is not true")

    if not _true(row.get("email_opt_in")):
        reasons.append("email_opt_in is not true")

    if not row.get("email"):
        reasons.append("missing email")

    if not row.get("source_url"):
        reasons.append("missing source_url")

    if str(row.get("status", "")).lower() in {"unsubscribed", "do_not_contact", "blocked"}:
        reasons.append("contact is suppressed")

    return OutreachDecision(not reasons, reasons)


def can_send_whatsapp(row: dict[str, str], env: dict[str, str] | None = None) -> OutreachDecision:
    env = env or os.environ
    reasons: list[str] = []

    if not _true(env.get("WHATSAPP_SEND_ENABLED")):
        reasons.append("WHATSAPP_SEND_ENABLED is not true")

    if not _true(env.get("WHATSAPP_ALLOW_LIVE_SEND")):
        reasons.append("WHATSAPP_ALLOW_LIVE_SEND is not true")

    if not _true(row.get("whatsapp_opt_in")):
        reasons.append("whatsapp_opt_in is not true")

    if not row.get("phone"):
        reasons.append("missing phone")

    if not row.get("source_url"):
        reasons.append("missing source_url")

    if str(row.get("status", "")).lower() in {"unsubscribed", "do_not_contact", "blocked"}:
        reasons.append("contact is suppressed")

    return OutreachDecision(not reasons, reasons)
