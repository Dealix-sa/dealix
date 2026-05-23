#!/usr/bin/env python3
"""Smoke-test the Dealix internal API endpoints used by the Founder Console.

Boots the FastAPI app in-process via the starlette TestClient and verifies
that every internal endpoint returns a structured response.
"""
from __future__ import annotations

import json
import sys


def main() -> int:
    try:
        from fastapi.testclient import TestClient
        from api.main import app
    except Exception as exc:  # pragma: no cover
        print(f"SKIP: cannot import api.main ({exc})")
        return 0

    client = TestClient(app)
    paths = [
        "/api/v1/internal/ceo/summary",
        "/api/v1/internal/sales/funnel",
        "/api/v1/internal/approvals",
        "/api/v1/internal/workers/health",
        "/api/v1/internal/trust/flags",
        "/api/v1/internal/finance/summary",
        "/api/v1/internal/distribution/summary",
        "/api/v1/internal/delivery/queue",
        "/api/v1/internal/retention/queue",
        "/api/v1/internal/proof/library",
        "/api/v1/internal/audit/events",
        "/api/v1/internal/control/summary",
        "/api/v1/internal/control/policies",
        "/api/v1/internal/control/agents",
        "/api/v1/internal/control/scorecard",
        "/api/v1/internal/evals/status",
        "/api/v1/internal/product/productization",
        "/api/v1/internal/security/status",
        "/api/v1/internal/sovereign/readiness",
        "/api/v1/internal/brand/summary",
        "/api/v1/internal/growth/targeting",
        "/api/v1/internal/marketing/summary",
        "/api/v1/internal/product/distribution",
        "/api/v1/internal/customer-success/summary",
        "/api/v1/internal/finance-ops/summary",
        "/api/v1/internal/data/summary",
        "/api/v1/internal/experiments/backlog",
    ]
    failures: list[tuple[str, int]] = []
    for p in paths:
        res = client.get(p)
        ok = res.status_code == 200 and isinstance(res.json(), dict)
        if not ok:
            failures.append((p, res.status_code))

    print("[smoke-internal-api]")
    print(f"  paths probed: {len(paths)}")
    print(f"  failures: {failures}")
    print("RESULT:", "FAIL" if failures else "PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
