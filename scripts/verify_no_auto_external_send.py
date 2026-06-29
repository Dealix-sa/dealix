#!/usr/bin/env python3
"""Verify Dealix does not enable uncontrolled external sending in test/release gates."""

from __future__ import annotations

import os


def truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def main() -> int:
    failures: list[str] = []
    external = truthy("EXTERNAL_SEND_ENABLED")
    email = truthy("EMAIL_SEND_ENABLED")
    whatsapp = truthy("WHATSAPP_SEND_ENABLED")
    whatsapp_live = truthy("WHATSAPP_ALLOW_LIVE_SEND")
    sms = truthy("SMS_SEND_ENABLED")
    mode = os.getenv("OUTBOUND_MODE", "draft_only").strip() or "draft_only"

    if external and mode != "controlled_live":
        failures.append("EXTERNAL_SEND_ENABLED=true requires OUTBOUND_MODE=controlled_live")
    if email and not external:
        failures.append("EMAIL_SEND_ENABLED=true requires EXTERNAL_SEND_ENABLED=true")
    if whatsapp and not external:
        failures.append("WHATSAPP_SEND_ENABLED=true requires EXTERNAL_SEND_ENABLED=true")
    if whatsapp and not whatsapp_live:
        failures.append("WHATSAPP_SEND_ENABLED=true requires WHATSAPP_ALLOW_LIVE_SEND=true")
    if sms:
        failures.append("SMS_SEND_ENABLED=true is blocked by the baseline safety gate")

    if failures:
        print("NO_AUTO_EXTERNAL_SEND_GATE=FAIL")
        for item in failures:
            print(f"FAIL: {item}")
        return 1

    print("NO_AUTO_EXTERNAL_SEND_GATE=PASS")
    print(f"OUTBOUND_MODE={mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
