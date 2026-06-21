"""
Dealix Central Configuration — safety config, env bindings, safe defaults.

Usage:
    from company.config import SafetyConfig
    cfg = SafetyConfig.from_env()
    cfg.assert_safe()   # raises RuntimeError if any gate is open
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyConfig:
    """Immutable safety configuration. All gates default to closed (safe)."""

    external_send_enabled: bool = False
    outbound_mode: str = "draft_only"
    email_send_enabled: bool = False
    whatsapp_send_enabled: bool = False
    whatsapp_allow_live_send: bool = False
    sms_send_enabled: bool = False

    @classmethod
    def from_env(cls) -> "SafetyConfig":
        def _bool(key: str) -> bool:
            return os.getenv(key, "false").strip().lower() in ("true", "1", "yes")
        return cls(
            external_send_enabled=_bool("EXTERNAL_SEND_ENABLED"),
            outbound_mode=os.getenv("OUTBOUND_MODE", "draft_only").strip().lower(),
            email_send_enabled=_bool("EMAIL_SEND_ENABLED"),
            whatsapp_send_enabled=_bool("WHATSAPP_SEND_ENABLED"),
            whatsapp_allow_live_send=_bool("WHATSAPP_ALLOW_LIVE_SEND"),
            sms_send_enabled=_bool("SMS_SEND_ENABLED"),
        )

    @property
    def is_safe(self) -> bool:
        return (
            not self.external_send_enabled
            and self.outbound_mode == "draft_only"
            and not self.email_send_enabled
            and not self.whatsapp_send_enabled
            and not self.whatsapp_allow_live_send
            and not self.sms_send_enabled
        )

    def assert_safe(self) -> None:
        if not self.is_safe:
            violations = []
            if self.external_send_enabled:
                violations.append("EXTERNAL_SEND_ENABLED=true")
            if self.outbound_mode != "draft_only":
                violations.append(f"OUTBOUND_MODE={self.outbound_mode}")
            if self.email_send_enabled:
                violations.append("EMAIL_SEND_ENABLED=true")
            if self.whatsapp_send_enabled:
                violations.append("WHATSAPP_SEND_ENABLED=true")
            if self.whatsapp_allow_live_send:
                violations.append("WHATSAPP_ALLOW_LIVE_SEND=true")
            if self.sms_send_enabled:
                violations.append("SMS_SEND_ENABLED=true")
            raise RuntimeError(
                f"Safety gate violation — live sending may occur: {', '.join(violations)}"
            )

    def gate_status(self) -> str:
        return "PASS" if self.is_safe else "FAIL"


# Module-level singleton — safe by default, override via env vars
_default_cfg: SafetyConfig | None = None


def get_safety_config() -> SafetyConfig:
    global _default_cfg
    if _default_cfg is None:
        _default_cfg = SafetyConfig.from_env()
    return _default_cfg
