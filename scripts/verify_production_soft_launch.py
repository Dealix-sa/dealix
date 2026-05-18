#!/usr/bin/env python3
"""Production Soft Launch verify — live api.dealix.me + local gates."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = "https://api.dealix.me"


def _get(url: str, headers: dict[str, str] | None = None) -> int:
    req = Request(url, headers=headers or {}, method="GET")
    try:
        with urlopen(req, timeout=15) as resp:
            return resp.status
    except HTTPError as exc:
        return exc.code
    except URLError:
        return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=os.environ.get("DEALIX_API_BASE", DEFAULT_BASE))
    p.add_argument("--admin-key", default=os.environ.get("DEALIX_ADMIN_API_KEY", ""))
    args = p.parse_args()
    base = args.api_base.rstrip("/")
    failures: list[str] = []

    print(f"== production soft launch ==\n  {base}")
    for path in ("/healthz", "/readyz"):
        code = _get(f"{base}{path}")
        if code == 200:
            print(f"  ok: {path}")
        else:
            failures.append(f"{path} got {code}")

    if args.admin_key:
        h = {"X-Admin-API-Key": args.admin_key}
        for path in ("/api/v1/founder/dashboard", "/api/v1/founder/agent-queue"):
            code = _get(f"{base}{path}", h)
            if code == 200:
                print(f"  ok: {path}")
            else:
                failures.append(f"{path} got {code}")

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/verify_railway_production_config.py"), "--api-base", base],
        cwd=str(ROOT),
    )
    if proc.returncode != 0:
        failures.append("verify_railway_production_config")

    if failures:
        print("PRODUCTION_SOFT_LAUNCH_VERIFY=FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PRODUCTION_SOFT_LAUNCH_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
