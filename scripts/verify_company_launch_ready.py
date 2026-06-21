#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    external = truthy("EXTERNAL_SEND_ENABLED")
    mode = os.getenv("OUTBOUND_MODE", "draft_only")

    if external and mode != "controlled_live":
        failures.append("EXTERNAL_SEND_ENABLED=true requires OUTBOUND_MODE=controlled_live")

    if truthy("EMAIL_SEND_ENABLED") and not external:
        failures.append("EMAIL_SEND_ENABLED=true requires EXTERNAL_SEND_ENABLED=true")

    if truthy("WHATSAPP_SEND_ENABLED") and not external:
        failures.append("WHATSAPP_SEND_ENABLED=true requires EXTERNAL_SEND_ENABLED=true")

    if truthy("WHATSAPP_SEND_ENABLED") and not truthy("WHATSAPP_ALLOW_LIVE_SEND"):
        failures.append("WHATSAPP_SEND_ENABLED=true requires WHATSAPP_ALLOW_LIVE_SEND=true")

    if truthy("SMS_SEND_ENABLED"):
        failures.append("SMS_SEND_ENABLED=true is blocked in baseline launch mode")

    if not (ROOT / "scripts/run_company_launch_day.sh").exists():
        warnings.append("scripts/run_company_launch_day.sh not found")

    if failures:
        print("COMPANY_LAUNCH_READY=BLOCKED")
        for f in failures:
            print(f"FAIL: {f}")
        for w in warnings:
            print(f"WARN: {w}")
        return 1

    print("COMPANY_LAUNCH_READY=READY_FOR_MANUAL_OUTREACH")
    print("Mode: draft/review-first unless controlled-live gates are explicitly enabled.")
    for w in warnings:
        print(f"WARN: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
