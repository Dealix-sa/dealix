#!/usr/bin/env python3
"""Smoke-test the internal founder-console API surface.

Uses FastAPI's TestClient against the in-process app — no network. Verifies
that every documented internal endpoint responds 200 (or 401 when the auth
token is required and absent) without throwing.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

# Ensure the repository root is importable so 'api.*' resolves regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ENDPOINTS = [
    "/api/v1/internal/founder/ceo",
    "/api/v1/internal/founder/sales",
    "/api/v1/internal/founder/approvals",
    "/api/v1/internal/founder/workers",
    "/api/v1/internal/founder/trust",
    "/api/v1/internal/founder/finance",
    "/api/v1/internal/founder/distribution",
    "/api/v1/internal/founder/delivery",
    "/api/v1/internal/founder/retention",
    "/api/v1/internal/founder/proof",
    "/api/v1/internal/founder/audit",
    "/api/v1/internal/founder/evals",
    "/api/v1/internal/founder/product",
    "/api/v1/internal/founder/security",
    "/api/v1/internal/founder/growth",
    "/api/v1/internal/founder/marketing",
    "/api/v1/internal/founder/sovereign",
    "/api/v1/internal/control/summary",
    "/api/v1/internal/control/policies",
    "/api/v1/internal/control/agents",
    "/api/v1/internal/control/scorecard",
    "/api/v1/internal/control/risks",
]


def main() -> int:
    os.environ.setdefault("INTERNAL_API_TOKEN", "")  # dev mode -> allow

    try:
        fastapi = importlib.import_module("fastapi.testclient")
    except Exception as exc:  # pragma: no cover
        print(f"[smoke-internal-api] skipping (fastapi not installed): {exc}")
        return 0

    try:
        # Only import the router (avoids loading the entire app graph + its
        # optional heavy dependencies). Mount on a tiny FastAPI just for smoke.
        from fastapi import FastAPI

        router_mod = importlib.import_module("api.routers.internal.founder_console")
        app = FastAPI()
        app.include_router(router_mod.router, prefix="/api/v1/internal")
    except Exception as exc:
        print(f"[smoke-internal-api] FAIL to import router: {exc}")
        return 1

    client = fastapi.TestClient(app)
    failures = 0
    for ep in ENDPOINTS:
        try:
            resp = client.get(ep)
        except Exception as exc:  # pragma: no cover
            print(f"FAIL {ep} (exception: {exc})")
            failures += 1
            continue
        if resp.status_code in (200, 401, 403):
            print(f"PASS {ep} ({resp.status_code})")
        else:
            print(f"FAIL {ep} ({resp.status_code})")
            failures += 1

    print(f"\n[smoke-internal-api] {len(ENDPOINTS) - failures} pass / {failures} fail")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
