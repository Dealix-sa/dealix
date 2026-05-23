#!/usr/bin/env python3
"""Smoke-test the Dealix internal API on http://localhost:8000.

Reads DEALIX_INTERNAL_TOKEN from env if present and sends it as the
X-Dealix-Internal-Token header. Exits 0 if all probed endpoints return
200, non-zero otherwise. Designed to be run against a local `make run`.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("DEALIX_INTERNAL_BASE", "http://localhost:8000")
TOKEN = os.environ.get("DEALIX_INTERNAL_TOKEN")

ENDPOINTS = [
    "/api/v1/internal/ceo/summary",
    "/api/v1/internal/sales/funnel",
    "/api/v1/internal/approvals",
    "/api/v1/internal/workers/health",
    "/api/v1/internal/finance/summary",
    "/api/v1/internal/distribution/summary",
    "/api/v1/internal/trust/flags",
    "/api/v1/internal/audit/events",
    "/api/v1/internal/control/summary",
    "/api/v1/internal/control/policies",
    "/api/v1/internal/control/agents",
    "/api/v1/internal/control/scorecard",
    "/api/v1/internal/evals/status",
    "/api/v1/internal/security/status",
]


def hit(path: str) -> tuple[int, str]:
    req = urllib.request.Request(BASE + path, method="GET")
    if TOKEN:
        req.add_header("X-Dealix-Internal-Token", TOKEN)
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body[:200]
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")[:200]
    except urllib.error.URLError as exc:
        return 0, f"URLError: {exc.reason}"


def main() -> int:
    print(f"== smoke against {BASE} (token: {'yes' if TOKEN else 'no'}) ==")
    failures = 0
    for path in ENDPOINTS:
        status, snippet = hit(path)
        if status == 200:
            print(f"  OK   {status} {path}")
        else:
            failures += 1
            print(f"  FAIL {status} {path} -> {snippet!r}")
    if failures:
        print(f"\nFAIL: {failures} endpoint(s) failed")
        return 1
    print(f"\nOK: {len(ENDPOINTS)} endpoints returned 200")
    # As a final sanity check, ensure ceo/summary contains a 'source' field.
    status, body = hit("/api/v1/internal/ceo/summary")
    try:
        data = json.loads(body)
        if "source" not in data:
            print("FAIL: ceo/summary missing 'source'")
            return 1
    except json.JSONDecodeError:
        # Already counted above if status != 200
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
