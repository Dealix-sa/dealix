#!/usr/bin/env python3
"""
verify_railway_readiness.py — Railway production config audit.

Understands this repo's actual convention:
  - railway.toml / railway.json both point at the Dockerfile
  - start.sh is GENERATED inside the Dockerfile via HEREDOC at /app/start.sh
    (so the absence of start.sh on disk is correct — checking for it on disk
     would be a false alarm)
  - /healthz lives in api/routers/health.py
  - preDeployCommand runs scripts/railway_predeploy.sh
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return ""


def main() -> int:
    failures: list[str] = []
    ok: list[str] = []

    # railway.toml
    rt = read(ROOT / "railway.toml")
    if not rt:
        failures.append("railway.toml is missing")
    else:
        if "DOCKERFILE" not in rt:
            failures.append("railway.toml: builder is not DOCKERFILE")
        else:
            ok.append("railway.toml uses DOCKERFILE builder")
        if "healthcheckPath" not in rt or "/healthz" not in rt:
            failures.append("railway.toml: healthcheckPath is not /healthz")
        else:
            ok.append("railway.toml healthcheckPath=/healthz")
        if "preDeployCommand" not in rt or "railway_predeploy" not in rt:
            failures.append("railway.toml: preDeployCommand does not run railway_predeploy")
        else:
            ok.append("railway.toml runs scripts/railway_predeploy.sh on predeploy")

    # railway.json must agree with toml
    rj = read(ROOT / "railway.json")
    if not rj:
        failures.append("railway.json is missing")
    elif "/healthz" not in rj or "DOCKERFILE" not in rj:
        failures.append("railway.json disagrees with railway.toml (healthcheck or builder)")
    else:
        ok.append("railway.json agrees with railway.toml")

    # Dockerfile + generated start.sh
    df = read(ROOT / "Dockerfile")
    if not df:
        failures.append("Dockerfile is missing")
    else:
        if "EXPOSE" not in df:
            failures.append("Dockerfile has no EXPOSE")
        if "HEALTHCHECK" not in df:
            failures.append("Dockerfile has no HEALTHCHECK")
        if "/app/start.sh" not in df:
            failures.append("Dockerfile does not reference /app/start.sh")
        elif not re.search(r"COPY[^\n]*<<['\"]?EOF['\"]?\s+/app/start\.sh", df):
            failures.append("Dockerfile does not generate /app/start.sh via HEREDOC")
        else:
            ok.append("Dockerfile generates /app/start.sh via HEREDOC")
        if "uvicorn" not in df.lower():
            failures.append("Dockerfile does not invoke uvicorn")
        if "USER app" not in df and "USER 1000" not in df:
            failures.append("Dockerfile does not drop to non-root user")
        else:
            ok.append("Dockerfile runs as non-root user")
        if "${PORT" not in df and "$PORT" not in df:
            failures.append("Dockerfile does not bind to Railway $PORT")
        else:
            ok.append("Dockerfile binds to $PORT")

    # Predeploy script
    pd = read(ROOT / "scripts/railway_predeploy.sh")
    if not pd:
        failures.append("scripts/railway_predeploy.sh is missing")
    elif "alembic upgrade head" not in pd:
        failures.append("railway_predeploy.sh does not run 'alembic upgrade head'")
    elif "RUN_RAILWAY_PRE_DEPLOY_MIGRATE" not in pd:
        failures.append("railway_predeploy.sh is not gated by RUN_RAILWAY_PRE_DEPLOY_MIGRATE")
    else:
        ok.append("railway_predeploy.sh runs gated alembic upgrade head")

    # /healthz on the actual app
    h = read(ROOT / "api/routers/health.py")
    if not h:
        failures.append("api/routers/health.py is missing")
    elif "/healthz" not in h:
        failures.append("api/routers/health.py does not expose /healthz")
    else:
        ok.append("api/routers/health.py exposes /healthz")

    for line in ok:
        print(f"  ok   {line}")
    for line in failures:
        print(f"  FAIL {line}")

    if failures:
        print(f"RAILWAY READINESS: FAIL ({len(failures)} issues)")
        return 1
    print(f"RAILWAY READINESS: PASS ({len(ok)} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
