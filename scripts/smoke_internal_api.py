#!/usr/bin/env python3
"""Smoke test the Founder Console internal API.

Hits every read endpoint and verifies a 200 response with JSON. Uses
``X-Dealix-Internal-Token`` if ``DEALIX_INTERNAL_TOKEN`` is set in the
environment.

Defaults to ``http://localhost:8000`` (override via ``--base-url`` or
``DEALIX_API_BASE``). Exits 0 if every endpoint returns valid JSON.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

ENDPOINTS = [
    "/api/v1/internal/ceo/summary",
    "/api/v1/internal/sales/funnel",
    "/api/v1/internal/approvals",
    "/api/v1/internal/workers/health",
    "/api/v1/internal/finance/summary",
    "/api/v1/internal/control/summary",
    "/api/v1/internal/sovereign/readiness",
]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--base-url",
        default=os.environ.get("DEALIX_API_BASE", "http://localhost:8000"),
    )
    p.add_argument("--timeout", type=int, default=10)
    args = p.parse_args()

    token = os.environ.get("DEALIX_INTERNAL_TOKEN")

    fails = 0
    for ep in ENDPOINTS:
        url = args.base_url.rstrip("/") + ep
        req = urllib.request.Request(url, method="GET")
        if token:
            req.add_header("X-Dealix-Internal-Token", token)
        try:
            with urllib.request.urlopen(req, timeout=args.timeout) as resp:
                status = resp.status
                body = resp.read().decode("utf-8", errors="replace")
                try:
                    data = json.loads(body)
                    src = data.get("source", "?")
                    print(f"[PASS] {ep}  status={status} source={src}")
                except json.JSONDecodeError:
                    print(f"[FAIL] {ep}  status={status} non-json response", file=sys.stderr)
                    fails += 1
        except urllib.error.HTTPError as e:
            print(f"[FAIL] {ep}  http {e.code}", file=sys.stderr)
            fails += 1
        except Exception as e:
            print(f"[FAIL] {ep}  {e}", file=sys.stderr)
            fails += 1

    print(f"summary: {len(ENDPOINTS) - fails}/{len(ENDPOINTS)} endpoints OK")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
