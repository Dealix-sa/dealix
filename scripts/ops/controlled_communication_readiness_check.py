#!/usr/bin/env python3
"""Controlled communication readiness check for Dealix.

This check is intentionally conservative. It does not validate DNS over the
network; it verifies that the production intent and required environment gates
are explicitly present before any future live communication mode can be enabled.
"""
from __future__ import annotations

import json
import os
from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "reports" / "go_live"

REQUIRED_FOR_CONTROLLED_EMAIL = [
    "EMAIL_PROVIDER",
    "EMAIL_FROM",
    "UNSUBSCRIBE_URL",
    "SUPPRESSION_LIST_ENABLED",
    "EMAIL_RATE_LIMIT_PER_DAY",
    "AUDIT_LOG_ENABLED",
]

REQUIRED_FOR_CONTROLLED_WHATSAPP = [
    "WHATSAPP_BUSINESS_ACCOUNT_ID",
    "WHATSAPP_PHONE_NUMBER_ID",
    "WHATSAPP_TEMPLATE_APPROVAL_REQUIRED",
    "WHATSAPP_OPT_IN_REQUIRED",
    "SUPPRESSION_LIST_ENABLED",
    "AUDIT_LOG_ENABLED",
]

SAFE_FALSE_FLAGS = [
    "EXTERNAL_SEND_ENABLED",
    "EMAIL_SEND_ENABLED",
    "WHATSAPP_SEND_ENABLED",
    "WHATSAPP_ALLOW_LIVE_SEND",
    "SMS_SEND_ENABLED",
]


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    for key in SAFE_FALSE_FLAGS:
        if truthy(os.getenv(key)):
            failures.append(f"Unsafe live flag is enabled: {key}")

    if os.getenv("OUTBOUND_MODE", "draft_only") != "draft_only":
        failures.append("OUTBOUND_MODE must stay draft_only until controlled live PR is approved")

    missing_email = [key for key in REQUIRED_FOR_CONTROLLED_EMAIL if not os.getenv(key)]
    missing_whatsapp = [key for key in REQUIRED_FOR_CONTROLLED_WHATSAPP if not os.getenv(key)]

    if missing_email:
        warnings.append("Controlled email not ready: missing " + ", ".join(missing_email))
    if missing_whatsapp:
        warnings.append("Controlled WhatsApp not ready: missing " + ", ".join(missing_whatsapp))

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "blocked" if failures else "draft_only_ready_controlled_live_not_enabled",
        "failures": failures,
        "warnings": warnings,
        "email_gate_requirements": REQUIRED_FOR_CONTROLLED_EMAIL,
        "whatsapp_gate_requirements": REQUIRED_FOR_CONTROLLED_WHATSAPP,
        "safe_false_flags": SAFE_FALSE_FLAGS,
        "next_step": "Keep draft-only. Enable controlled live communication only in a separate reviewed PR.",
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "controlled_communication_readiness.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if failures:
        print("CONTROLLED_COMMUNICATION=BLOCKED")
        for item in failures:
            print(f"FAIL: {item}")
        for item in warnings:
            print(f"WARN: {item}")
        return 1

    print("CONTROLLED_COMMUNICATION=DRAFT_ONLY_READY")
    for item in warnings:
        print(f"WARN: {item}")
    print("Report: reports/go_live/controlled_communication_readiness.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
