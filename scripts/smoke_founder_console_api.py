"""Smoke test the Founder Console v4 internal API.

Assumes the FastAPI app is running on http://localhost:8000.
Set DEALIX_INTERNAL_API_BASE to override.
"""

from __future__ import annotations

import json
import os
import urllib.request

BASE = os.getenv("DEALIX_INTERNAL_API_BASE", "http://localhost:8000")

ENDPOINTS = [
    "/api/v1/internal/ceo/summary",
    "/api/v1/internal/sales/funnel",
    "/api/v1/internal/approvals",
    "/api/v1/internal/finance/summary",
    "/api/v1/internal/distribution/summary",
]

failures: list[str] = []

for endpoint in ENDPOINTS:
    url = BASE + endpoint
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            print("PASS", endpoint, type(data).__name__)
    except Exception as exc:
        failures.append(f"{endpoint}: {exc}")

if failures:
    print("Founder Console API smoke test failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: Founder Console internal API smoke test passed.")
