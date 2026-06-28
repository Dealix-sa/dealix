"""Safety doctrine for the Commercial Growth OS v2.

This module is the single authority that decides whether *any* outbound
action (email, WhatsApp, calendar write, proposal finalisation) may leave
the system. It is **fail-closed**: the default answer is always "no".

Live action is only ever permitted when, in combination:

  * the relevant feature flag is enabled (default: disabled), AND
  * ``OUTBOUND_MODE == "controlled_live"``, AND
  * the channel is legally/contractually allowed for the account, AND
  * the contact is verified and contactable, AND
  * opt-out is respected (and opt-in exists for WhatsApp), AND
  * the action carries an explicit owner decision / approval, AND
  * no blocked claim is present.

No function here performs a network send, a calendar write, or a payment.
They only *evaluate* and return a :class:`SafetyDecision`.
"""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

# Feature flags. Every one of these defaults to the SAFE value when unset.
SAFE_DEFAULT_FLAGS: dict[str, str] = {
    "EXTERNAL_SEND_ENABLED": "false",
    "EMAIL_SEND_ENABLED": "false",
    "WHATSAPP_SEND_ENABLED": "false",
    "WHATSAPP_ALLOW_LIVE_SEND": "false",
    "SMS_SEND_ENABLED": "false",
    "CALENDAR_WRITE_ENABLED": "false",
    "PROPOSAL_FINALIZATION_ENABLED": "false",
    "OUTBOUND_MODE": "draft_only",
}

# Claim guard — phrases we will never put on the wire.
BLOCKED_CLAIMS = (
    "guarantee",  # covers "guarantee", "guaranteed", "we guarantee", etc.
    "risk-free",
    "risk free",
    "100%",
    "double your revenue",
    "we promise",
    "نضمن",
    "مضمون",
    "ضمان النتائج",
    "أرباح مضمونة",
)


@dataclass
class SafetyDecision:
    """The result of a safety evaluation.

    ``allowed``           — may this action actually leave the system *now*?
    ``reason``            — primary human-readable reason.
    ``required_approvals``— approvals that must be recorded before going live.
    ``blocked_by``        — every failing gate (empty only when allowed).
    ``audit_level``       — how loudly this action must be logged.
    """

    allowed: bool
    reason: str
    required_approvals: list[str] = field(default_factory=list)
    blocked_by: list[str] = field(default_factory=list)
    audit_level: str = "standard"  # standard | elevated | critical

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── Env helpers ────────────────────────────────────────────────────────────────


def _env(env: Mapping[str, str] | None) -> Mapping[str, str]:
    return env if env is not None else os.environ


def _flag(env: Mapping[str, str] | None, key: str) -> bool:
    e = _env(env)
    default = SAFE_DEFAULT_FLAGS.get(key, "false")
    return str(e.get(key, default)).strip().lower() == "true"


def outbound_mode(env: Mapping[str, str] | None = None) -> str:
    e = _env(env)
    return str(e.get("OUTBOUND_MODE", "draft_only")).strip() or "draft_only"


def is_controlled_live(env: Mapping[str, str] | None = None) -> bool:
    return outbound_mode(env) == "controlled_live"


def safe_defaults(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Report the live state of every safety flag (for the command room)."""
    return {
        "outbound_mode": outbound_mode(env),
        "external_send_enabled": _flag(env, "EXTERNAL_SEND_ENABLED"),
        "email_send_enabled": _flag(env, "EMAIL_SEND_ENABLED"),
        "whatsapp_send_enabled": _flag(env, "WHATSAPP_SEND_ENABLED"),
        "whatsapp_allow_live_send": _flag(env, "WHATSAPP_ALLOW_LIVE_SEND"),
        "sms_send_enabled": _flag(env, "SMS_SEND_ENABLED"),
        "calendar_write_enabled": _flag(env, "CALENDAR_WRITE_ENABLED"),
        "proposal_finalization_enabled": _flag(env, "PROPOSAL_FINALIZATION_ENABLED"),
    }


def is_safe_default_environment(env: Mapping[str, str] | None = None) -> bool:
    """True when the environment is in the fully fail-closed default state."""
    s = safe_defaults(env)
    return (
        s["outbound_mode"] == "draft_only"
        and not s["external_send_enabled"]
        and not s["email_send_enabled"]
        and not s["whatsapp_send_enabled"]
        and not s["whatsapp_allow_live_send"]
        and not s["sms_send_enabled"]
        and not s["calendar_write_enabled"]
        and not s["proposal_finalization_enabled"]
    )


# ── Claim guard ──────────────────────────────────────────────────────────────


def contains_blocked_claim(text: str | None) -> str | None:
    """Return the first blocked claim found in ``text``, else ``None``."""
    if not text:
        return None
    low = text.lower()
    for claim in BLOCKED_CLAIMS:
        if claim in low:
            return claim
    return None


def _account_get(account: Any, key: str, default: Any = None) -> Any:
    if isinstance(account, Mapping):
        return account.get(key, default)
    return getattr(account, key, default)


def _opted_out(account: Any) -> bool:
    status = str(_account_get(account, "contactability_status", "unknown")).lower()
    return status in ("opted_out", "blocked") or bool(_account_get(account, "email_opt_out", False))


# ── Channel / action gates ─────────────────────────────────────────────────────


def _base_gate(
    *,
    flag_key: str,
    channel_label: str,
    account: Any,
    action: Mapping[str, Any] | None,
    client_rules: Mapping[str, Any] | None,
    extra_blockers: list[str],
    required_approvals: list[str],
    audit_level: str = "elevated",
) -> SafetyDecision:
    """Shared evaluation skeleton for all live-send gates."""
    action = action or {}
    client_rules = client_rules or {}
    blocked: list[str] = list(extra_blockers)

    if not is_controlled_live():
        blocked.append(f"outbound_mode={outbound_mode()} (need controlled_live)")
    if not _flag(None, "EXTERNAL_SEND_ENABLED"):
        blocked.append("EXTERNAL_SEND_ENABLED=false")
    if not _flag(None, flag_key):
        blocked.append(f"{flag_key}=false")

    # Channel must be contractually allowed for this client.
    allowed_channels = client_rules.get("allowed_channels")
    if allowed_channels is not None and channel_label not in allowed_channels:
        blocked.append(f"channel {channel_label} not in client allowed_channels")

    if _opted_out(account):
        blocked.append("contact opted out / not contactable")

    if str(_account_get(account, "verification_status", "unverified")).lower() != "verified":
        blocked.append("account not verified")

    if not _account_get(account, "source_url"):
        blocked.append("missing source_url")

    # Approval / owner decision must be present on the action.
    if str(action.get("message_status", "")).lower() != "approved":
        blocked.append("message.status != approved")
    if str(action.get("owner_decision", "")).lower() not in ("send", "book"):
        blocked.append("owner_decision not send/book")

    claim = contains_blocked_claim(action.get("text") or action.get("draft_message"))
    if claim:
        blocked.append(f"blocked claim: {claim}")

    allowed = not blocked
    reason = "all gates passed" if allowed else blocked[0]
    return SafetyDecision(
        allowed=allowed,
        reason=reason,
        required_approvals=required_approvals,
        blocked_by=blocked,
        audit_level=audit_level if allowed else "critical",
    )


def can_send_email(
    action: Mapping[str, Any] | None,
    account: Any,
    client_rules: Mapping[str, Any] | None = None,
) -> SafetyDecision:
    """Decide whether an email may actually be sent. Default: denied."""
    extra: list[str] = []
    # Email must carry an unsubscribe / opt-out affordance.
    if action and not action.get("has_unsubscribe", False):
        extra.append("email missing unsubscribe/opt-out")
    return _base_gate(
        flag_key="EMAIL_SEND_ENABLED",
        channel_label="email",
        account=account,
        action=action,
        client_rules=client_rules,
        extra_blockers=extra,
        required_approvals=["founder_or_client_send_approval"],
    )


def can_send_whatsapp(
    action: Mapping[str, Any] | None,
    account: Any,
    client_rules: Mapping[str, Any] | None = None,
) -> SafetyDecision:
    """Decide whether a WhatsApp message may be sent. Default: denied.

    WhatsApp additionally requires explicit opt-in and the WhatsApp-specific
    live flag. Cold WhatsApp is never permitted.
    """
    extra: list[str] = []
    if not _flag(None, "WHATSAPP_ALLOW_LIVE_SEND"):
        extra.append("WHATSAPP_ALLOW_LIVE_SEND=false")
    if not _account_get(account, "whatsapp_opt_in", False):
        extra.append("no WhatsApp opt-in (cold WhatsApp forbidden)")
    return _base_gate(
        flag_key="WHATSAPP_SEND_ENABLED",
        channel_label="whatsapp",
        account=account,
        action=action,
        client_rules=client_rules,
        extra_blockers=extra,
        required_approvals=["whatsapp_opt_in", "founder_or_client_send_approval"],
        audit_level="critical",
    )


def can_write_calendar(
    action: Mapping[str, Any] | None,
    account: Any,
    client_rules: Mapping[str, Any] | None = None,
) -> SafetyDecision:
    """Decide whether a calendar event may be written. Default: denied."""
    action = action or {}
    blocked: list[str] = []
    if not _flag(None, "CALENDAR_WRITE_ENABLED"):
        blocked.append("CALENDAR_WRITE_ENABLED=false")
    if not is_controlled_live():
        blocked.append(f"outbound_mode={outbound_mode()} (need controlled_live)")
    if str(action.get("owner_decision", "")).lower() != "book":
        blocked.append("owner_decision != book")
    if _opted_out(account):
        blocked.append("contact opted out / not contactable")
    allowed = not blocked
    return SafetyDecision(
        allowed=allowed,
        reason="all gates passed" if allowed else blocked[0],
        required_approvals=["owner_book_decision"],
        blocked_by=blocked,
        audit_level="elevated" if allowed else "critical",
    )


def can_finalize_proposal(
    action: Mapping[str, Any] | None,
    account: Any,
    client_rules: Mapping[str, Any] | None = None,
) -> SafetyDecision:
    """Decide whether a proposal may be *finalised* with a binding price.

    This is an A3-restricted action and is denied unless the finalisation
    flag is on AND a recorded founder approval is present. It never sets a
    price by itself.
    """
    action = action or {}
    blocked: list[str] = []
    if not _flag(None, "PROPOSAL_FINALIZATION_ENABLED"):
        blocked.append("PROPOSAL_FINALIZATION_ENABLED=false")
    if not action.get("founder_approved", False):
        blocked.append("no recorded founder approval for final price")
    if not action.get("pricing_within_guardrails", False):
        blocked.append("price not confirmed within guardrails")
    allowed = not blocked
    return SafetyDecision(
        allowed=allowed,
        reason="all gates passed" if allowed else blocked[0],
        required_approvals=["founder_pricing_approval"],
        blocked_by=blocked,
        audit_level="critical",
    )
