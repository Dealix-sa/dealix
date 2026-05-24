#!/usr/bin/env python3
"""Smoke test for the Founder Console internal API.

Spins up an in-process TestClient when possible, otherwise validates that
the router file imports and PAGE_SOURCES is non-empty. Exits 0 on PASS.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


def main() -> int:
    try:
        import fastapi  # noqa: F401
    except ImportError:
        # Static checks only: confirm the router module's source defines PAGE_SOURCES
        # and references the auth + policy + runtime helpers. We avoid importing it
        # because it pulls in FastAPI at module load.
        src = (Path(__file__).resolve().parents[1] / "api/routers/internal/founder_console.py").read_text("utf-8")
        for marker in ("PAGE_SOURCES", "require_internal_key", "contains_forbidden_claim", "@router.get", "@router.post"):
            if marker not in src:
                print(f"FAIL: founder_console.py missing {marker}")
                return 1
        print("PASS (lite): founder_console source verified · fastapi not installed")
        return 0

    try:
        from api.routers.internal.founder_console import PAGE_SOURCES, router  # type: ignore
    except Exception as exc:
        print(f"FAIL: cannot import founder_console router: {exc}")
        return 1

    if not PAGE_SOURCES:
        print("FAIL: PAGE_SOURCES is empty")
        return 1

    # Touch private ops workspace so reads succeed.
    os.environ.setdefault("DEALIX_PRIVATE_OPS", str(REPO_ROOT / "runtime"))
    Path(os.environ["DEALIX_PRIVATE_OPS"]).mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("DEALIX_INTERNAL_KEY", "smoke-key")

    try:
        from fastapi import FastAPI  # type: ignore
        from fastapi.testclient import TestClient  # type: ignore
    except ImportError:
        print(f"PASS (lite): router loaded · {len(PAGE_SOURCES)} pages registered")
        return 0

    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    for slug in list(PAGE_SOURCES.keys())[:5]:
        res = client.get(f"/internal/founder-console/{slug}", headers={"x-internal-key": "smoke-key"})
        if res.status_code != 200:
            print(f"FAIL: /internal/founder-console/{slug} returned {res.status_code}")
            return 1

    res = client.get("/internal/founder-console/ceo", headers={"x-internal-key": "wrong"})
    if res.status_code != 401:
        print(f"FAIL: bad key did not 401 (got {res.status_code})")
        return 1

    res = client.post(
        "/internal/founder-console/approvals/queue",
        headers={"x-internal-key": "smoke-key"},
        json={"action_id": "test", "reason": "we deliver guaranteed revenue for clients"},
    )
    if res.status_code != 400:
        print(f"FAIL: forbidden claim did not 400 (got {res.status_code})")
        return 1

    res = client.post(
        "/internal/founder-console/approvals/queue",
        headers={"x-internal-key": "smoke-key"},
        json={"action_id": "test_ok", "reason": "queue draft outreach for ERP/CRM sector"},
    )
    if res.status_code != 200:
        print(f"FAIL: clean approval request returned {res.status_code}")
        return 1
    if not res.json().get("queued"):
        print("FAIL: clean approval request not queued")
        return 1

    print(f"PASS: founder console smoke ({len(PAGE_SOURCES)} pages, approvals queued)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
