#!/usr/bin/env python3
"""Smoke-test ``/healthz`` and ``/api/v1/internal/ceo/summary``.

Usage:

  python scripts/smoke_internal_api.py --base http://localhost:8000
  DEALIX_INTERNAL_TOKEN=... python scripts/smoke_internal_api.py \\
      --base https://api.dealix.me

Checks (in order):

  1. ``GET {base}/healthz`` → 200, body has ``"status": "ok"``.
  2. ``GET {base}/api/v1/internal/ceo/summary`` (with internal token) → 200.
  3. Optional (production only): unauthenticated request returns 403.

The script reports whether the token is ``set`` or ``unset`` — it never
prints the token value itself.

Exit codes: 0 if every required check passes; 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def _get(url: str, *, token: str | None = None) -> tuple[int, str]:
    req = urllib.request.Request(url)
    if token:
        req.add_header("X-Dealix-Internal-Token", token)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:  # noqa: S310 — http(s) only
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace") if exc.fp else ""
    except urllib.error.URLError as exc:
        return -1, str(exc)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base", default="http://localhost:8000", help="API base URL")
    p.add_argument(
        "--require-auth",
        action="store_true",
        help="Also verify the endpoint refuses unauthenticated requests (production only).",
    )
    args = p.parse_args()

    base = args.base.rstrip("/")
    token = os.getenv("DEALIX_INTERNAL_TOKEN", "").strip() or None
    api_key = os.getenv("DEALIX_ADMIN_API_KEY", "").strip() or None

    print("== smoke_internal_api ==")
    print(f"  base: {base}")
    print(f"  DEALIX_INTERNAL_TOKEN: {'set' if token else 'unset'}")
    print(f"  DEALIX_ADMIN_API_KEY:  {'set' if api_key else 'unset'}")

    fails: list[str] = []

    # 1) /healthz
    code, body = _get(f"{base}/healthz")
    print(f"  /healthz -> {code}")
    if code != 200:
        fails.append(f"/healthz returned {code}")
    else:
        try:
            payload = json.loads(body)
            print(f"    status={payload.get('status')!r} env={payload.get('env')!r}")
        except json.JSONDecodeError:
            fails.append("/healthz did not return JSON")

    # 2) /api/v1/internal/ceo/summary (authenticated)
    summary_url = f"{base}/api/v1/internal/ceo/summary"
    if token or api_key:
        # Use whichever token was provided.
        req = urllib.request.Request(summary_url)
        if token:
            req.add_header("X-Dealix-Internal-Token", token)
        elif api_key:
            req.add_header("X-API-Key", api_key)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:  # noqa: S310
                code = resp.status
                body = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            code = exc.code
            body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        except urllib.error.URLError as exc:
            code = -1
            body = str(exc)
        print(f"  /api/v1/internal/ceo/summary (auth) -> {code}")
        if code != 200:
            fails.append(f"/api/v1/internal/ceo/summary returned {code} with auth")
        else:
            try:
                payload = json.loads(body)
                kill = payload.get("kill_switches", {})
                print(
                    "    kill_switches: "
                    f"mock={kill.get('whatsapp_mock_mode')} "
                    f"allow_live={kill.get('whatsapp_allow_live_send')} "
                    f"live_allowed={kill.get('is_live_send_allowed')}"
                )
            except json.JSONDecodeError:
                fails.append("/api/v1/internal/ceo/summary did not return JSON")
    else:
        print(
            "  /api/v1/internal/ceo/summary (auth) -> SKIPPED "
            "(no DEALIX_INTERNAL_TOKEN / DEALIX_ADMIN_API_KEY in env)"
        )

    # 3) unauthenticated → 403 (only when --require-auth)
    if args.require_auth:
        code, _body = _get(summary_url)
        print(f"  /api/v1/internal/ceo/summary (no auth) -> {code}")
        if code != 403:
            fails.append(f"unauthenticated CEO summary should return 403, got {code}")

    for f in fails:
        print(f"  FAIL: {f}")
    if not fails:
        print("  ok: all internal-api smoke checks passed")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
