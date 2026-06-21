#!/usr/bin/env python3
"""
Verify that no unsafe automatic external send configuration is active.

Exits 0 and prints NO_AUTO_EXTERNAL_SEND_GATE=PASS when safe defaults are in effect.
Exits 1 and lists failures when unsafe configuration is detected.
"""
from __future__ import annotations

import os
import sys


def _is_true(key: str) -> bool:
    return os.environ.get(key, "false").lower() in ("true", "1", "yes")


def _mode() -> str:
    return os.environ.get("OUTBOUND_MODE", "draft_only").lower()


def run_checks() -> list[str]:
    failures: list[str] = []

    external_enabled = _is_true("EXTERNAL_SEND_ENABLED")
    mode = _mode()

    if external_enabled and mode != "controlled_live":
        failures.append(
            "FAIL: EXTERNAL_SEND_ENABLED=true requires OUTBOUND_MODE=controlled_live"
        )

    if _is_true("EMAIL_SEND_ENABLED") and not external_enabled:
        failures.append(
            "FAIL: EMAIL_SEND_ENABLED=true while EXTERNAL_SEND_ENABLED is not true"
        )

    if _is_true("WHATSAPP_SEND_ENABLED") and not external_enabled:
        failures.append(
            "FAIL: WHATSAPP_SEND_ENABLED=true while EXTERNAL_SEND_ENABLED is not true"
        )

    if _is_true("WHATSAPP_SEND_ENABLED") and not _is_true("WHATSAPP_ALLOW_LIVE_SEND"):
        failures.append(
            "FAIL: WHATSAPP_SEND_ENABLED=true requires WHATSAPP_ALLOW_LIVE_SEND=true"
        )

    if _is_true("SMS_SEND_ENABLED") and mode != "controlled_live":
        failures.append(
            "FAIL: SMS_SEND_ENABLED=true is not allowed in baseline/draft-only mode"
        )

    return failures


def main() -> int:
    failures = run_checks()

    if failures:
        for f in failures:
            print(f)
        print("NO_AUTO_EXTERNAL_SEND_GATE=FAIL")
        return 1

    print("NO_AUTO_EXTERNAL_SEND_GATE=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
