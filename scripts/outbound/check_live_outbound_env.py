#!/usr/bin/env python3
"""Validate that all required environment variables for controlled live outbound are set."""

from __future__ import annotations

import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

from app.outbound.config import OutboundSettings  # noqa: E402


def check() -> dict:
    settings = OutboundSettings()
    errors: list[str] = []
    warnings: list[str] = []

    # Master switches must be explicit
    if os.getenv("EXTERNAL_SEND_ENABLED") is None:
        errors.append("EXTERNAL_SEND_ENABLED is not set (must be true or false)")
    if os.getenv("OUTBOUND_MODE") is None:
        errors.append("OUTBOUND_MODE is not set (recommended: controlled_live)")

    if settings.outbound_mode == "controlled_live":
        if not settings.outbound_require_approval:
            warnings.append("OUTBOUND_REQUIRE_APPROVAL=false in controlled_live mode")
        if not settings.outbound_require_verified_target:
            warnings.append("OUTBOUND_REQUIRE_VERIFIED_TARGET=false in controlled_live mode")
        if not settings.outbound_require_source_url:
            warnings.append("OUTBOUND_REQUIRE_SOURCE_URL=false in controlled_live mode")
        if not settings.outbound_block_fake_claims:
            warnings.append("OUTBOUND_BLOCK_FAKE_CLAIMS=false in controlled_live mode")
        if not settings.outbound_block_guaranteed_roi:
            warnings.append("OUTBOUND_BLOCK_GUARANTEED_ROI=false in controlled_live mode")

    # Email provider checks
    if settings.email_send_enabled and settings.email_send_mode == "live":
        if not settings.smtp_host:
            errors.append("EMAIL_SEND_MODE=live requires SMTP_HOST")
        if not settings.smtp_user:
            errors.append("EMAIL_SEND_MODE=live requires SMTP_USER")
        if not settings.email_reply_to:
            warnings.append("EMAIL_REPLY_TO not set (recommended for deliverability)")

    # WhatsApp provider checks
    if settings.whatsapp_send_enabled and settings.whatsapp_allow_live_send:
        if not settings.meta_phone_number_id:
            errors.append("WHATSAPP live send requires META_PHONE_NUMBER_ID")
        if not settings.meta_wa_access_token:
            errors.append("WHATSAPP live send requires META_WA_ACCESS_TOKEN")
        if settings.whatsapp_send_mode not in ("template_only", "live"):
            errors.append("WHATSAPP_SEND_MODE must be template_only or live")

    # Database
    if not settings.database_url:
        warnings.append("DATABASE_URL not set (CSV fallback will be used)")

    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "settings": settings.as_safe_dict(),
    }


def main() -> int:
    result = check()
    print("=== Dealix Controlled Live Outbound — Environment Check ===")
    for key, value in result["settings"].items():
        print(f"  {key}: {value}")
    print()
    if result["errors"]:
        print("❌ ERRORS:")
        for e in result["errors"]:
            print(f"  - {e}")
    if result["warnings"]:
        print("⚠️  WARNINGS:")
        for w in result["warnings"]:
            print(f"  - {w}")
    if result["ok"] and not result["warnings"]:
        print("✅ Environment ready for controlled live outbound.")
    elif result["ok"]:
        print("✅ Environment ready (with warnings).")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
