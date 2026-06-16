"""Environment-based configuration for controlled live outbound."""

from __future__ import annotations

import os
from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass
class OutboundSettings:
    """All outbound-related env settings in one place."""

    # ── Global mode ─────────────────────────────────────────────────
    app_env: str = field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    environment: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))

    external_send_enabled: bool = field(
        default_factory=lambda: os.getenv("EXTERNAL_SEND_ENABLED", "false").lower() == "true"
    )
    outbound_mode: str = field(default_factory=lambda: os.getenv("OUTBOUND_MODE", "dry"))
    outbound_require_approval: bool = field(
        default_factory=lambda: os.getenv("OUTBOUND_REQUIRE_APPROVAL", "true").lower() == "true"
    )
    outbound_require_verified_target: bool = field(
        default_factory=lambda: os.getenv("OUTBOUND_REQUIRE_VERIFIED_TARGET", "true").lower()
        == "true"
    )
    outbound_require_source_url: bool = field(
        default_factory=lambda: os.getenv("OUTBOUND_REQUIRE_SOURCE_URL", "true").lower() == "true"
    )
    outbound_require_opt_out: bool = field(
        default_factory=lambda: os.getenv("OUTBOUND_REQUIRE_OPT_OUT", "true").lower() == "true"
    )
    outbound_block_fake_claims: bool = field(
        default_factory=lambda: os.getenv("OUTBOUND_BLOCK_FAKE_CLAIMS", "true").lower() == "true"
    )
    outbound_block_guaranteed_roi: bool = field(
        default_factory=lambda: os.getenv("OUTBOUND_BLOCK_GUARANTEED_ROI", "true").lower()
        == "true"
    )

    # ── Email ───────────────────────────────────────────────────────
    email_send_enabled: bool = field(
        default_factory=lambda: os.getenv("EMAIL_SEND_ENABLED", "false").lower() == "true"
    )
    email_send_mode: str = field(default_factory=lambda: os.getenv("EMAIL_SEND_MODE", "dry"))
    email_provider: str = field(default_factory=lambda: os.getenv("EMAIL_PROVIDER", "smtp"))
    email_daily_limit: int = field(
        default_factory=lambda: int(os.getenv("EMAIL_DAILY_LIMIT", "25"))
    )
    email_batch_limit: int = field(
        default_factory=lambda: int(os.getenv("EMAIL_BATCH_LIMIT", "10"))
    )
    email_min_seconds_between_sends: int = field(
        default_factory=lambda: int(os.getenv("EMAIL_MIN_SECONDS_BETWEEN_SENDS", "90"))
    )
    email_require_unsubscribe: bool = field(
        default_factory=lambda: os.getenv("EMAIL_REQUIRE_UNSUBSCRIBE", "true").lower() == "true"
    )
    email_track_replies: bool = field(
        default_factory=lambda: os.getenv("EMAIL_TRACK_REPLIES", "true").lower() == "true"
    )
    email_reply_to: str = field(default_factory=lambda: os.getenv("EMAIL_REPLY_TO", ""))
    smtp_host: str = field(default_factory=lambda: os.getenv("SMTP_HOST", ""))
    smtp_port: int = field(default_factory=lambda: int(os.getenv("SMTP_PORT", "587")))
    smtp_user: str = field(default_factory=lambda: os.getenv("SMTP_USER", ""))
    smtp_password: str = field(default_factory=lambda: os.getenv("SMTP_PASSWORD", ""))
    email_default_from: str = field(
        default_factory=lambda: os.getenv("EMAIL_DEFAULT_FROM", "sami@dealix.me")
    )

    # ── WhatsApp ────────────────────────────────────────────────────
    whatsapp_send_enabled: bool = field(
        default_factory=lambda: os.getenv("WHATSAPP_SEND_ENABLED", "false").lower() == "true"
    )
    whatsapp_allow_live_send: bool = field(
        default_factory=lambda: os.getenv("WHATSAPP_ALLOW_LIVE_SEND", "false").lower() == "true"
    )
    whatsapp_provider: str = field(
        default_factory=lambda: os.getenv("WHATSAPP_PROVIDER", "meta_cloud")
    )
    whatsapp_send_mode: str = field(
        default_factory=lambda: os.getenv("WHATSAPP_SEND_MODE", "template_only")
    )
    whatsapp_daily_limit: int = field(
        default_factory=lambda: int(os.getenv("WHATSAPP_DAILY_LIMIT", "10"))
    )
    whatsapp_batch_limit: int = field(
        default_factory=lambda: int(os.getenv("WHATSAPP_BATCH_LIMIT", "5"))
    )
    whatsapp_min_seconds_between_sends: int = field(
        default_factory=lambda: int(os.getenv("WHATSAPP_MIN_SECONDS_BETWEEN_SENDS", "120"))
    )
    whatsapp_require_opt_in: bool = field(
        default_factory=lambda: os.getenv("WHATSAPP_REQUIRE_OPT_IN", "true").lower() == "true"
    )
    whatsapp_require_approved_template: bool = field(
        default_factory=lambda: os.getenv("WHATSAPP_REQUIRE_APPROVED_TEMPLATE", "true").lower()
        == "true"
    )
    whatsapp_stop_keywords: Sequence[str] = field(
        default_factory=lambda: tuple(
            k.strip().upper()
            for k in os.getenv(
                "WHATSAPP_STOP_KEYWORDS", "STOP,UNSUBSCRIBE,إيقاف,الغاء,إلغاء"
            ).split(",")
            if k.strip()
        )
    )
    meta_phone_number_id: str = field(
        default_factory=lambda: os.getenv("META_PHONE_NUMBER_ID", "")
    )
    meta_wa_access_token: str = field(
        default_factory=lambda: os.getenv("META_WA_ACCESS_TOKEN", "")
    )

    # ── Operational ─────────────────────────────────────────────────
    outreach_timezone: str = field(
        default_factory=lambda: os.getenv("OUTREACH_TIMEZONE", "Asia/Riyadh")
    )
    command_room_enabled: bool = field(
        default_factory=lambda: os.getenv("COMMAND_ROOM_ENABLED", "true").lower() == "true"
    )
    ceo_daily_report_enabled: bool = field(
        default_factory=lambda: os.getenv("CEO_DAILY_REPORT_ENABLED", "true").lower() == "true"
    )
    reply_classification_enabled: bool = field(
        default_factory=lambda: os.getenv("REPLY_CLASSIFICATION_ENABLED", "true").lower()
        == "true"
    )
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production" or self.app_env.lower() == "production"

    @property
    def live_email_allowed(self) -> bool:
        return (
            self.external_send_enabled
            and self.email_send_enabled
            and self.email_send_mode == "live"
            and self.outbound_mode in ("controlled_live", "live")
        )

    @property
    def live_whatsapp_allowed(self) -> bool:
        return (
            self.external_send_enabled
            and self.whatsapp_send_enabled
            and self.whatsapp_allow_live_send
            and self.whatsapp_send_mode in ("template_only", "live")
            and self.outbound_mode in ("controlled_live", "live")
        )

    def as_safe_dict(self) -> dict:
        """Return a dict safe for logging (no secrets)."""
        return {
            "app_env": self.app_env,
            "environment": self.environment,
            "external_send_enabled": self.external_send_enabled,
            "outbound_mode": self.outbound_mode,
            "outbound_require_approval": self.outbound_require_approval,
            "outbound_require_verified_target": self.outbound_require_verified_target,
            "outbound_require_source_url": self.outbound_require_source_url,
            "outbound_require_opt_out": self.outbound_require_opt_out,
            "outbound_block_fake_claims": self.outbound_block_fake_claims,
            "outbound_block_guaranteed_roi": self.outbound_block_guaranteed_roi,
            "email_send_enabled": self.email_send_enabled,
            "email_send_mode": self.email_send_mode,
            "email_provider": self.email_provider,
            "email_daily_limit": self.email_daily_limit,
            "email_batch_limit": self.email_batch_limit,
            "email_min_seconds_between_sends": self.email_min_seconds_between_sends,
            "email_require_unsubscribe": self.email_require_unsubscribe,
            "email_track_replies": self.email_track_replies,
            "whatsapp_send_enabled": self.whatsapp_send_enabled,
            "whatsapp_allow_live_send": self.whatsapp_allow_live_send,
            "whatsapp_provider": self.whatsapp_provider,
            "whatsapp_send_mode": self.whatsapp_send_mode,
            "whatsapp_daily_limit": self.whatsapp_daily_limit,
            "whatsapp_batch_limit": self.whatsapp_batch_limit,
            "whatsapp_min_seconds_between_sends": self.whatsapp_min_seconds_between_sends,
            "whatsapp_require_opt_in": self.whatsapp_require_opt_in,
            "whatsapp_require_approved_template": self.whatsapp_require_approved_template,
            "outreach_timezone": self.outreach_timezone,
            "command_room_enabled": self.command_room_enabled,
            "ceo_daily_report_enabled": self.ceo_daily_report_enabled,
            "reply_classification_enabled": self.reply_classification_enabled,
            "live_email_allowed": self.live_email_allowed,
            "live_whatsapp_allowed": self.live_whatsapp_allowed,
        }
