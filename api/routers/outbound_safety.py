"""Outbound safety and send endpoints — all blocked by default.

All send endpoints return a safety response with allowed=false when
EXTERNAL_SEND_ENABLED is not explicitly set to true. The default mode
is draft_only, meaning no external sending occurs.
"""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/outbound", tags=["outbound-safety"])


# ── Models ──────────────────────────────────────────────────────


class SafetyStatus(BaseModel):
    external_send_enabled: bool
    outbound_mode: str
    email_send_enabled: bool
    whatsapp_send_enabled: bool
    whatsapp_allow_live_send: bool
    sms_send_enabled: bool
    safe_to_send: bool
    reason: str


class ChannelReadiness(BaseModel):
    channel: str
    enabled: bool
    mode: str
    ready: bool
    reason: str


class SendRequest(BaseModel):
    channel: str = "email"
    to: str = ""
    subject: str = ""
    body: str = ""
    template_id: str | None = None


class SendResponse(BaseModel):
    allowed: bool
    safe_to_send: bool
    mode: str
    reason: str
    channel: str


# ── Helpers ─────────────────────────────────────────────────────


def _get_bool_env(key: str, default: bool = False) -> bool:
    return os.getenv(key, str(default)).lower() in ("true", "1", "yes")


def _get_str_env(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def _default_safety_status() -> dict[str, Any]:
    external_enabled = _get_bool_env("EXTERNAL_SEND_ENABLED", False)
    mode = _get_str_env("OUTBOUND_MODE", "draft_only")
    email_enabled = _get_bool_env("EMAIL_SEND_ENABLED", False)
    wa_enabled = _get_bool_env("WHATSAPP_SEND_ENABLED", False)
    wa_live = _get_bool_env("WHATSAPP_ALLOW_LIVE_SEND", False)
    sms_enabled = _get_bool_env("SMS_SEND_ENABLED", False)

    safe = external_enabled and mode != "draft_only"
    reason = "external_send_disabled" if not external_enabled else (
        "draft_only_mode" if mode == "draft_only" else "ready"
    )

    return {
        "external_send_enabled": external_enabled,
        "outbound_mode": mode,
        "email_send_enabled": email_enabled,
        "whatsapp_send_enabled": wa_enabled,
        "whatsapp_allow_live_send": wa_live,
        "sms_send_enabled": sms_enabled,
        "safe_to_send": safe,
        "reason": reason,
    }


def _evaluate_send(channel: str) -> dict[str, Any]:
    status = _default_safety_status()
    external_ok = status["external_send_enabled"]
    mode_ok = status["outbound_mode"] != "draft_only"

    channel_key = f"{channel}_send_enabled"
    channel_enabled = status.get(channel_key, False) if channel_key in status else False

    if channel == "whatsapp":
        channel_enabled = status["whatsapp_send_enabled"]
        wa_live = status["whatsapp_allow_live_send"]
        if not (channel_enabled and wa_live):
            return {
                "allowed": False,
                "safe_to_send": False,
                "mode": status["outbound_mode"],
                "reason": "whatsapp_not_enabled_or_not_live",
                "channel": channel,
            }

    if not external_ok:
        return {
            "allowed": False,
            "safe_to_send": False,
            "mode": status["outbound_mode"],
            "reason": "external_send_disabled",
            "channel": channel,
        }

    if not mode_ok:
        return {
            "allowed": False,
            "safe_to_send": False,
            "mode": status["outbound_mode"],
            "reason": "draft_only_mode",
            "channel": channel,
        }

    if not channel_enabled:
        return {
            "allowed": False,
            "safe_to_send": False,
            "mode": status["outbound_mode"],
            "reason": f"{channel}_send_disabled",
            "channel": channel,
        }

    return {
        "allowed": True,
        "safe_to_send": True,
        "mode": status["outbound_mode"],
        "reason": "approved",
        "channel": channel,
    }


# ── Endpoints ───────────────────────────────────────────────────


@router.get("/safety")
async def outbound_safety() -> dict[str, Any]:
    """Return the current outbound safety status."""
    return _default_safety_status()


@router.get("/channels")
async def outbound_channels() -> dict[str, Any]:
    """Return per-channel status."""
    status = _default_safety_status()
    return {
        "email": {
            "enabled": status["email_send_enabled"],
            "mode": status["outbound_mode"],
        },
        "whatsapp": {
            "enabled": status["whatsapp_send_enabled"],
            "allow_live": status["whatsapp_allow_live_send"],
            "mode": status["outbound_mode"],
        },
        "sms": {
            "enabled": status["sms_send_enabled"],
            "mode": status["outbound_mode"],
        },
    }


@router.get("/readiness/email")
async def email_readiness() -> dict[str, Any]:
    """Email channel readiness."""
    status = _default_safety_status()
    ready = status["external_send_enabled"] and status["email_send_enabled"]
    return {
        "channel": "email",
        "enabled": status["email_send_enabled"],
        "mode": status["outbound_mode"],
        "ready": ready,
        "reason": "ready" if ready else "email_send_disabled",
    }


@router.get("/readiness/whatsapp")
async def whatsapp_readiness() -> dict[str, Any]:
    """WhatsApp channel readiness."""
    status = _default_safety_status()
    ready = (
        status["external_send_enabled"]
        and status["whatsapp_send_enabled"]
        and status["whatsapp_allow_live_send"]
    )
    return {
        "channel": "whatsapp",
        "enabled": status["whatsapp_send_enabled"],
        "allow_live": status["whatsapp_allow_live_send"],
        "mode": status["outbound_mode"],
        "ready": ready,
        "reason": "ready" if ready else "whatsapp_not_enabled_or_not_live",
    }


@router.get("/readiness/sms")
async def sms_readiness() -> dict[str, Any]:
    """SMS channel readiness."""
    status = _default_safety_status()
    ready = status["external_send_enabled"] and status["sms_send_enabled"]
    return {
        "channel": "sms",
        "enabled": status["sms_send_enabled"],
        "mode": status["outbound_mode"],
        "ready": ready,
        "reason": "ready" if ready else "sms_send_disabled",
    }


@router.post("/send/email")
async def send_email(request: SendRequest) -> dict[str, Any]:
    """Send email — blocked by default."""
    result = _evaluate_send("email")
    if not result["allowed"]:
        return result
    # In a real system, this would queue the email.
    # For now, even if enabled, we just log and return a draft response.
    return {
        "allowed": True,
        "safe_to_send": True,
        "mode": result["mode"],
        "reason": "queued_for_review",
        "channel": "email",
        "to": request.to,
    }


@router.post("/send/whatsapp")
async def send_whatsapp(request: SendRequest) -> dict[str, Any]:
    """Send WhatsApp — blocked by default."""
    result = _evaluate_send("whatsapp")
    if not result["allowed"]:
        return result
    return {
        "allowed": True,
        "safe_to_send": True,
        "mode": result["mode"],
        "reason": "queued_for_review",
        "channel": "whatsapp",
        "to": request.to,
    }


@router.post("/send/sms")
async def send_sms(request: SendRequest) -> dict[str, Any]:
    """Send SMS — blocked by default."""
    result = _evaluate_send("sms")
    if not result["allowed"]:
        return result
    return {
        "allowed": True,
        "safe_to_send": True,
        "mode": result["mode"],
        "reason": "queued_for_review",
        "channel": "sms",
        "to": request.to,
    }
