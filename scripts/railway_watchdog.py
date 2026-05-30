#!/usr/bin/env python3
"""Dealix Railway watchdog.

Designed for a Railway *Cron* service (e.g. ``*/15 * * * *``). Probes the
public API health endpoint and exits non-zero when it is unhealthy so the
Cron run is recorded as failed and alerting can fire.

Environment:
    APP_URL / DEALIX_API_URL   base URL (default https://api.dealix.me)
    DEALIX_HEALTH_PATH         health path (default /healthz)

Run on Railway (Cron service, no public domain):
    Start Command: python scripts/railway_watchdog.py
    Cron Schedule: */15 * * * *
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from datetime import UTC, datetime
from urllib.parse import urlparse

API_URL = (os.getenv("APP_URL") or os.getenv("DEALIX_API_URL") or "https://api.dealix.me").rstrip("/")
HEALTH_PATH = os.getenv("DEALIX_HEALTH_PATH", "/healthz")
HEALTH_URL = f"{API_URL}{HEALTH_PATH}"
TIMEOUT_SECONDS = int(os.getenv("DEALIX_WATCHDOG_TIMEOUT_SECONDS", "15"))


def check_health() -> dict[str, object]:
    started = time.time()
    parsed = urlparse(HEALTH_URL)
    if parsed.scheme not in ("http", "https"):
        return {"ok": False, "error": f"unsupported_scheme:{parsed.scheme}"}
    try:
        req = urllib.request.Request(  # noqa: S310 - scheme validated above
            HEALTH_URL,
            headers={"User-Agent": "dealix-railway-watchdog/1.0"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:  # noqa: S310
            body = response.read(4096).decode("utf-8", errors="replace")
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                payload = {"raw": body[:1000]}
            return {
                "ok": 200 <= response.status < 300,
                "status": int(response.status),
                "latency_ms": round((time.time() - started) * 1000),
                "body": payload,
            }
    except Exception as exc:
        return {
            "ok": False,
            "error": repr(exc),
            "latency_ms": round((time.time() - started) * 1000),
        }


def main() -> int:
    result = check_health()
    payload = {
        "service": "dealix-watchdog",
        "checked_at": datetime.now(UTC).isoformat(),
        "health_url": HEALTH_URL,
        "result": result,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
