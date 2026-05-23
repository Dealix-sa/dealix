#!/usr/bin/env python3
"""Hit the internal API on localhost:8000 and report status.

Useful as a post-deploy smoke test. Does NOT call any external service.
If DEALIX_INTERNAL_TOKEN is set it is sent as X-Dealix-Internal-Token.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("DEALIX_BASE_URL", "http://localhost:8000")
TOKEN = os.environ.get("DEALIX_INTERNAL_TOKEN")

ENDPOINTS = [
    "/api/v1/internal/ceo/summary",
    "/api/v1/internal/sales/funnel",
    "/api/v1/internal/approvals",
    "/api/v1/internal/workers/health",
    "/api/v1/internal/finance/summary",
    "/api/v1/internal/control/summary",
]


def hit(path: str) -> tuple[int, str]:
    req = urllib.request.Request(BASE + path)
    if TOKEN:
        req.add_header("X-Dealix-Internal-Token", TOKEN)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8")[:200]
            return resp.status, body
    except urllib.error.HTTPError as exc:
        return exc.code, exc.reason
    except Exception as exc:  # noqa: BLE001
        return 0, repr(exc)


def main() -> int:
    fail = 0
    for path in ENDPOINTS:
        status, body = hit(path)
        if 200 <= status < 300:
            print(f"[smoke_internal_api] {path} → {status}")
        else:
            fail += 1
            print(f"[smoke_internal_api] {path} → {status} {body}")
    if fail:
        print(f"[smoke_internal_api] FAIL  fail={fail}")
        return 1
    print(f"[smoke_internal_api] PASS  endpoints={len(ENDPOINTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
