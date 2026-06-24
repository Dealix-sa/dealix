#!/usr/bin/env python3
"""Verify SaaS safety environment defaults."""

from __future__ import annotations

import os

SAFE_FALSE = [
    "EXTERNAL_SEND_ENABLED",
    "EMAIL_SEND_ENABLED",
    "WHATSAPP_SEND_ENABLED",
    "WHATSAPP_ALLOW_LIVE_SEND",
    "SMS_SEND_ENABLED",
]


def main() -> int:
    failures: list[str] = []
    for name in SAFE_FALSE:
        value = os.getenv(name, "false").strip().lower()
        if value not in {"", "0", "false", "no", "off"}:
            failures.append(f"{name} must be false by default")
    mode = os.getenv("OUTBOUND_MODE", "draft_only")
    if mode != "draft_only":
        failures.append("OUTBOUND_MODE must default to draft_only")
    if failures:
        print("SAAS_ENV_SAFE=FAIL")
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("SAAS_ENV_SAFE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
