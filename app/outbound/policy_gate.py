from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any


BLOCKED_CLAIMS = [
    "guaranteed roi",
    "guaranteed revenue",
    "مضمون",
    "نضمن لك",
    "100%",
    "testimonial",
    "عميل قال",
]


@dataclass(frozen=True)
class GateResult:
    allowed: bool
    reasons: list[str]


def _env_true(env: Mapping[str, str], key: str) -> bool:
    return str(env.get(key, "")).lower() == "true"


def _contains_unsubscribe(text: str) -> bool:
    t = text.lower()
    return (
        "unsubscribe" in t
        or "opt out" in t
        or "إلغاء الاشتراك" in t
        or "ايقاف" in t
        or "إيقاف" in t
    )


def _has_blocked_claims(text: str) -> bool:
    t = text.lower()
    return any(claim in t for claim in BLOCKED_CLAIMS)


def can_send_email(contact: Mapping[str, Any], message: Mapping[str, Any], env: Mapping[str, str]) -> GateResult:
    reasons: list[str] = []

    if not _env_true(env, "EXTERNAL_SEND_ENABLED"):
        reasons.append("EXTERNAL_SEND_ENABLED is not true")
    if not _env_true(env, "EMAIL_SEND_ENABLED"):
        reasons.append("EMAIL_SEND_ENABLED is not true")
    if env.get("OUTBOUND_MODE") != "controlled_live":
        reasons.append("OUTBOUND_MODE must be controlled_live")
    if message.get("status") != "approved":
        reasons.append("message.status must be approved")
    if contact.get("verification_status") != "approved_to_send":
        reasons.append("contact.verification_status must be approved_to_send")
    if not contact.get("source_url"):
        reasons.append("source_url is required")
    if not contact.get("email"):
        reasons.append("email is required")
    if contact.get("email_opt_out") is True:
        reasons.append("contact has opted out from email")

    body = str(message.get("body", ""))
    if not _contains_unsubscribe(body):
        reasons.append("unsubscribe/opt-out wording is required")
    if _has_blocked_claims(body):
        reasons.append("blocked claim detected")

    return GateResult(allowed=not reasons, reasons=reasons)


def can_send_whatsapp(contact: Mapping[str, Any], message: Mapping[str, Any], env: Mapping[str, str]) -> GateResult:
    reasons: list[str] = []

    if not _env_true(env, "EXTERNAL_SEND_ENABLED"):
        reasons.append("EXTERNAL_SEND_ENABLED is not true")
    if not _env_true(env, "WHATSAPP_SEND_ENABLED"):
        reasons.append("WHATSAPP_SEND_ENABLED is not true")
    if not _env_true(env, "WHATSAPP_ALLOW_LIVE_SEND"):
        reasons.append("WHATSAPP_ALLOW_LIVE_SEND is not true")
    if env.get("OUTBOUND_MODE") != "controlled_live":
        reasons.append("OUTBOUND_MODE must be controlled_live")
    if env.get("WHATSAPP_SEND_MODE") != "template_only":
        reasons.append("WHATSAPP_SEND_MODE must be template_only")
    if message.get("status") != "approved":
        reasons.append("message.status must be approved")
    if not contact.get("whatsapp"):
        reasons.append("whatsapp is required")
    if contact.get("whatsapp_opt_in") is not True:
        reasons.append("whatsapp opt-in is required")
    if contact.get("whatsapp_opt_out") is True:
        reasons.append("contact has opted out from WhatsApp")
    if not message.get("template_name"):
        reasons.append("approved template_name is required")
    if contact.get("verification_status") != "approved_to_send":
        reasons.append("contact.verification_status must be approved_to_send")
    if not contact.get("source_url"):
        reasons.append("source_url is required")

    body = str(message.get("body", ""))
    if _has_blocked_claims(body):
        reasons.append("blocked claim detected")

    return GateResult(allowed=not reasons, reasons=reasons)
