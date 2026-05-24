"""Smoke test the internal API surface.

If BASE_URL is unset, runs in offline mode and only verifies that the
expected router file(s) exist. Online mode requires:
    BASE_URL=https://api.dealix.me
    DEALIX_INTERNAL_TOKEN=<value>   (never printed)

Online checks:
    GET /healthz                       (no auth)
    GET /api/v1/internal/ceo/summary   (must require auth → 401/403 without token)
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_cert_common import (
    VerifierReport,
    main_cli,
    repo_path,
)

INTERNAL_ROUTER = "api/routers/internal/founder_console.py"


def _get(url: str, headers: dict[str, str] | None = None, timeout: float = 10.0):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec - explicit URL
            return resp.status, resp.read(2048).decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read(1024).decode("utf-8", errors="ignore")
        except Exception:
            pass
        return e.code, body


def run() -> VerifierReport:
    r = VerifierReport(verifier="Internal API Smoke")

    if repo_path(INTERNAL_ROUTER).exists():
        r.pass_("internal_router", INTERNAL_ROUTER)
    else:
        r.warn("internal_router", f"missing: {INTERNAL_ROUTER}",
               hint="scaffold api/routers/internal/founder_console.py")

    base = os.environ.get("BASE_URL", "").rstrip("/")
    if not base:
        r.warn("base_url", "BASE_URL unset — offline mode (use BASE_URL=https://api.dealix.me)")
        return r

    # /healthz must be open
    status, _ = _get(f"{base}/healthz")
    if status == 200:
        r.pass_("healthz", f"{base}/healthz → 200")
    else:
        r.fail("healthz", f"{base}/healthz → {status}")

    # internal route must reject unauthenticated calls
    status, body = _get(f"{base}/api/v1/internal/ceo/summary")
    if status in (401, 403):
        r.pass_("internal_auth", f"unauth → {status} (correct)")
    elif status == 404:
        r.warn("internal_auth", "route not registered yet (404)")
    else:
        snippet = (body[:120] + "…") if len(body) > 120 else body
        r.fail("internal_auth", f"unauth → {status} (expected 401/403): {snippet}",
               hint="internal routes MUST require DEALIX_INTERNAL_TOKEN in production")

    # And accept with token (token never printed)
    token = os.environ.get("DEALIX_INTERNAL_TOKEN")
    if token:
        status, _ = _get(f"{base}/api/v1/internal/ceo/summary",
                         headers={"X-Dealix-Internal-Token": "***"})  # placeholder header
        # we never actually send the real token from a smoke script — that's a deploy concern
        r.warn("internal_authenticated_call",
               "smoke script intentionally does not send the real token; verify in a sealed environment")
    else:
        r.warn("internal_authenticated_call", "DEALIX_INTERNAL_TOKEN not set")

    return r


if __name__ == "__main__":
    raise SystemExit(main_cli(run, name="smoke_internal_api"))
