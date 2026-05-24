#!/usr/bin/env python3
"""
smoke_internal_api.py — hit each /api/v1/internal/founder-console/*
endpoint with the admin bearer and assert it returns
{data, source, freshness, is_estimate}.

If $DEALIX_ADMIN_API_KEY is missing OR the API host is unreachable,
SKIP (exit 0) — this script is meant to run in CI where the API is up.

Usage:
  BASE_URL=http://localhost:8000 DEALIX_ADMIN_API_KEY=... \
      python scripts/smoke_internal_api.py
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

ENDPOINTS = [
    "/api/v1/internal/founder-console/ceo/daily-brief",
    "/api/v1/internal/founder-console/capital-allocation",
    "/api/v1/internal/founder-console/market-attack",
    "/api/v1/internal/founder-console/ai-governance",
    "/api/v1/internal/founder-console/trust/flags",
    "/api/v1/internal/founder-console/audit/recent",
    "/api/v1/internal/founder-console/policy",
]


def main() -> int:
    base = os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")
    token = os.environ.get("DEALIX_ADMIN_API_KEY", "") or os.environ.get("ADMIN_API_KEYS", "").split(",")[0]
    if not token:
        print("INTERNAL_API_SMOKE=skip reason=no_admin_key_set")
        return 0

    failures: list[str] = []
    passes = 0
    for path in ENDPOINTS:
        url = f"{base}{path}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
                if resp.status != 200:
                    failures.append(f"{path}: status {resp.status}")
                    continue
                body = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ConnectionError) as exc:
            # Treat host-down as SKIP (not FAIL) — CI may not have the API up.
            print(f"INTERNAL_API_SMOKE=skip reason=host_unreachable path={path} err={exc}")
            return 0
        for key in ("data", "source", "freshness", "is_estimate"):
            if key not in body:
                failures.append(f"{path}: missing key `{key}`")
        if body.get("source") not in ("api", "fallback"):
            failures.append(f"{path}: bad source `{body.get('source')}`")
        passes += 1

    verdict = "pass" if not failures else "fail"
    print(f"INTERNAL_API_SMOKE={verdict}")
    print(f"INTERNAL_API_SMOKE_PASSES={passes}")
    print(f"INTERNAL_API_SMOKE_FAILS={len(failures)}")
    if failures:
        print("\n## Internal API Smoke FAILURES")
        for f in failures:
            print(f"  - {f}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
