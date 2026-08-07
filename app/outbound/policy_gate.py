"""Policy gate — the single authority for outbound send decisions.

Defaults are fail-closed:
  allowed=False, safe_to_send=False, mode="draft_only",
  reason="external_send_disabled".

Live send is only possible when:
  - EXTERNAL_SEND_ENABLED == "true"
  - OUTBOUND_MODE == "controlled_live"
  - channel-specific flags are enabled
  - message is approved
  - contact is verified and has not opted out
  - consent is recorded where required
  - rate limits are respected
  - the recipient is not on the suppression list

This module never performs a real network send. Provider functions are
dry-run stubs (see provider_router.py).
"""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from app.outbound.consent import has_consent
from app.outbound.rate_limiter import within_rate_limits
from app.outbound.suppression import is_suppressed

BLOCKED_CLAIMS = [
    "guaranteed roi",
    "guaranteed revenue",
    "مضمون",
    "نضمن لك",
    "100%",
    "testimonial",
    "عميل قال",
]

# Recognised channel names. "internal_brief" is deliberately NOT a sendable
# channel — it's an internal-only action handled elsewhere.
CHANNELS = ("email", "whatsapp", "sms")

# ── Backwards-compatible result type used by can_send_email/can_send_whatsapp ──


@dataclass(frozen=True)
class GateResult:
    """Legacy two-field result. Kept for backwards compatibility."""

    allowed: bool
    reasons: list[str]


# ── Authoritative result type for the new evaluate_* API ──────────────────────


@dataclass(frozen=True)
class SendEvaluation:
    """Full evaluation of an outbound send attempt.

    `allowed`        — would the send be permitted at all (draft/approval ok)?
    `safe_to_send`   — would the send actually leave the system right now?
                       False whenever mode != controlled_live or external sends
                       are disabled, even if the draft itself is approved.
    `mode`           — the current outbound mode (draft_only | controlled_live).
    `channel`        — the evaluated channel name.
    `reason`         — primary human-readable reason when blocked.
    `reasons`        — full list of blocking reasons (empty when allowed).
    `contact`        — echo of the contact dict (sanitised).
    `message`        — echo of the message dict (sanitised).
    """

    allowed: bool
    safe_to_send: bool
    mode: str
    channel: str
    reason: str
    reasons: list[str] = field(default_factory=list)
    contact: dict[str, Any] = field(default_factory=dict)
    message: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── Env helpers ───────────────────────────────────────────────────────────────


def _env_true(env: Mapping[str, str], key: str) -> bool:
    return str(env.get(key, "")).lower() == "true"


def _env() -> Mapping[str, str]:
    # Always read os.environ at call time so tests can monkeypatch.
    return os.environ


def is_external_send_enabled(env: Mapping[str, str] | None = None) -> bool:
    """True only when EXTERNAL_SEND_ENABLED=true (default: False)."""
    e = env if env is not None else _env()
    return _env_true(e, "EXTERNAL_SEND_ENABLED")


def get_outbound_mode(env: Mapping[str, str] | None = None) -> str:
    """Return the active outbound mode. Defaults to 'draft_only'."""
    e = env if env is not None else _env()
    return str(e.get("OUTBOUND_MODE", "draft_only")) or "draft_only"


def default_safety_status(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Return the canonical default (fail-closed) safety status dict.

    This is what every endpoint should report when no overrides are applied.
    """
    e = env if env is not None else _env()
    mode = get_outbound_mode(e)
    external = is_external_send_enabled(e)
    return {
        "external_send_enabled": external,
        "outbound_mode": mode,
        "safe_to_send": False,
        "email_send_enabled": _env_true(e, "EMAIL_SEND_ENABLED"),
        "whatsapp_send_enabled": _env_true(e, "WHATSAPP_SEND_ENABLED"),
        "whatsapp_allow_live_send": _env_true(e, "WHATSAPP_ALLOW_LIVE_SEND"),
        "sms_send_enabled": _env_true(e, "SMS_SEND_ENABLED"),
        "reason": "external_send_disabled" if not external else "mode_not_controlled_live",
    }


# ── Content checks ───────────────────────────────────────────────────────────


def _contains_unsubscribe(text: str) -> bool:
    t = text.lower()
    return (
        "unsubscribe" in t
        or "opt out" in t
        or "opt-out" in t
        or "إلغاء الاشتراك" in t
        or "ايقاف" in t
        or "إيقاف" in t
    )


def _has_blocked_claims(text: str) -> bool:
    t = text.lower()
    return any(claim in t for claim in BLOCKED_CLAIMS)


# ── Channel-specific checks ──────────────────────────────────────────────────


def _check_email(contact: Mapping[str, Any], message: Mapping[str, Any], env: Mapping[str, str]) -> list[str]:
    reasons: list[str] = []

    if not is_external_send_enabled(env):
        reasons.append("external_send_disabled")
    if not _env_true(env, "EMAIL_SEND_ENABLED"):
        reasons.append("EMAIL_SEND_ENABLED is not true")
    if get_outbound_mode(env) != "controlled_live":
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

    return reasons


def _check_whatsapp(contact: Mapping[str, Any], message: Mapping[str, Any], env: Mapping[str, str]) -> list[str]:
    reasons: list[str] = []

    if not is_external_send_enabled(env):
        reasons.append("external_send_disabled")
    if not _env_true(env, "WHATSAPP_SEND_ENABLED"):
        reasons.append("WHATSAPP_SEND_ENABLED is not true")
    if not _env_true(env, "WHATSAPP_ALLOW_LIVE_SEND"):
        reasons.append("WHATSAPP_ALLOW_LIVE_SEND is not true")
    if get_outbound_mode(env) != "controlled_live":
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

    return reasons


def _check_sms(contact: Mapping[str, Any], message: Mapping[str, Any], env: Mapping[str, str]) -> list[str]:
    reasons: list[str] = []

    if not is_external_send_enabled(env):
        reasons.append("external_send_disabled")
    if not _env_true(env, "SMS_SEND_ENABLED"):
        reasons.append("SMS_SEND_ENABLED is not true")
    if get_outbound_mode(env) != "controlled_live":
        reasons.append("OUTBOUND_MODE must be controlled_live")
    if message.get("status") != "approved":
        reasons.append("message.status must be approved")
    if not contact.get("phone"):
        reasons.append("phone is required")
    if contact.get("sms_opt_out") is True:
        reasons.append("contact has opted out from SMS")
    if contact.get("verification_status") != "approved_to_send":
        reasons.append("contact.verification_status must be approved_to_send")
    if not contact.get("source_url"):
        reasons.append("source_url is required")

    body = str(message.get("body", ""))
    if not _contains_unsubscribe(body):
        reasons.append("unsubscribe/opt-out wording is required")
    if _has_blocked_claims(body):
        reasons.append("blocked claim detected")

    return reasons


_CHANNEL_CHECKS = {
    "email": _check_email,
    "whatsapp": _check_whatsapp,
    "sms": _check_sms,
}


# ── Cross-cutting guards (suppression, consent, rate limit) ─────────────────


def _apply_cross_cutting(
    channel: str,
    contact: Mapping[str, Any],
    message: Mapping[str, Any],
    reasons: list[str],
) -> None:
    """Append suppression, consent, and rate-limit reasons in-place."""
    identifier = _contact_identifier(channel, contact)
    if is_suppressed(identifier, channel=channel):
        reasons.append("recipient is on suppression list")

    if not has_consent(channel, contact):
        reasons.append("consent not recorded for channel")

    if not within_rate_limits(channel, identifier):
        reasons.append("rate limit exceeded for channel")


def _contact_identifier(channel: str, contact: Mapping[str, Any]) -> str:
    if channel == "email":
        return str(contact.get("email", "")).lower().strip()
    if channel == "whatsapp":
        return str(contact.get("whatsapp", "")).lower().strip()
    if channel == "sms":
        return str(contact.get("phone", "")).lower().strip()
    return str(contact.get("email") or contact.get("whatsapp") or contact.get("phone") or "").lower().strip()


# ── Public evaluate API ──────────────────────────────────────────────────────


def _evaluate(
    channel: str,
    message: Mapping[str, Any],
    contact: Mapping[str, Any],
    env: Mapping[str, str] | None = None,
) -> SendEvaluation:
    e = env if env is not None else _env()
    check = _CHANNEL_CHECKS.get(channel)
    if check is None:
        return SendEvaluation(
            allowed=False,
            safe_to_send=False,
            mode=get_outbound_mode(e),
            channel=channel,
            reason="unknown_channel",
            reasons=["unknown channel: " + channel],
            contact=dict(contact),
            message=dict(message),
        )

    reasons = list(check(contact, message, e))
    _apply_cross_cutting(channel, contact, message, reasons)

    external = is_external_send_enabled(e)
    mode = get_outbound_mode(e)
    allowed = len(reasons) == 0
    # safe_to_send requires allowed AND controlled_live AND external enabled.
    safe_to_send = allowed and external and mode == "controlled_live"

    if reasons:
        reason = reasons[0]
    elif not external:
        reason = "external_send_disabled"
    elif mode != "controlled_live":
        reason = "mode_not_controlled_live"
    else:
        reason = "ok"

    return SendEvaluation(
        allowed=allowed,
        safe_to_send=safe_to_send,
        mode=mode,
        channel=channel,
        reason=reason,
        reasons=reasons,
        contact=dict(contact),
        message=dict(message),
    )


def evaluate_email_send(
    message: Mapping[str, Any],
    contact: Mapping[str, Any],
    env: Mapping[str, str] | None = None,
) -> SendEvaluation:
    """Evaluate whether an email send is allowed."""
    return _evaluate("email", message, contact, env)


def evaluate_whatsapp_send(
    message: Mapping[str, Any],
    contact: Mapping[str, Any],
    env: Mapping[str, str] | None = None,
) -> SendEvaluation:
    """Evaluate whether a WhatsApp send is allowed."""
    return _evaluate("whatsapp", message, contact, env)


def evaluate_sms_send(
    message: Mapping[str, Any],
    contact: Mapping[str, Any],
    env: Mapping[str, str] | None = None,
) -> SendEvaluation:
    """Evaluate whether an SMS send is allowed."""
    return _evaluate("sms", message, contact, env)


def evaluate_channel_send(
    channel: str,
    message: Mapping[str, Any],
    contact: Mapping[str, Any],
    env: Mapping[str, str] | None = None,
) -> SendEvaluation:
    """Evaluate a send for an arbitrary channel name."""
    return _evaluate(channel, message, contact, env)


# ── Legacy backwards-compatible API ──────────────────────────────────────────


def can_send_email(
    contact: Mapping[str, Any],
    message: Mapping[str, Any],
    env: Mapping[str, str],
) -> GateResult:
    """Legacy gate — returns GateResult(allowed, reasons)."""
    reasons = _check_email(contact, message, env)
    _apply_cross_cutting("email", contact, message, reasons)
    return GateResult(allowed=not reasons, reasons=reasons)


def can_send_whatsapp(
    contact: Mapping[str, Any],
    message: Mapping[str, Any],
    env: Mapping[str, str],
) -> GateResult:
    """Legacy gate — returns GateResult(allowed, reasons)."""
    reasons = _check_whatsapp(contact, message, env)
    _apply_cross_cutting("whatsapp", contact, message, reasons)
    return GateResult(allowed=not reasons, reasons=reasons)