#!/usr/bin/env python3
"""Verify Railway deploy surfaces for API and web services.

This is intentionally dependency-free so it can run in CI before Docker builds.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "Dockerfile",
    "railway.json",
    "api/routers/health.py",
    "frontend/Dockerfile",
    "frontend/railway.json",
    "frontend/next.config.js",
    "frontend/src/app/healthz/route.ts",
    "apps/web/Dockerfile",
    "apps/web/railway.json",
    "apps/web/next.config.js",
    "apps/web/app/healthz/route.ts",
]


def fail(message: str) -> None:
    raise SystemExit(f"RAILWAY_SURFACES_FAIL: {message}")


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        fail(f"missing {path}")
    return target.read_text(encoding="utf-8")


def load_railway_config(path: str) -> dict[str, object]:
    try:
        return json.loads(read(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")


def verify_railway_json(path: str, *, allow_predeploy: bool) -> None:
    cfg = load_railway_config(path)
    build = cfg.get("build")
    deploy = cfg.get("deploy")
    if not isinstance(build, dict) or build.get("builder") != "DOCKERFILE":
        fail(f"{path} must use build.builder=DOCKERFILE")
    if build.get("dockerfilePath") != "Dockerfile":
        fail(f"{path} must use Dockerfile relative to service root")
    if not isinstance(deploy, dict) or deploy.get("healthcheckPath") != "/healthz":
        fail(f"{path} must healthcheck /healthz")
    if not allow_predeploy and "preDeployCommand" in deploy:
        fail(f"{path} must not run API predeploy commands for web images")


def main() -> None:
    for path in REQUIRED_FILES:
        read(path)

    verify_railway_json("railway.json", allow_predeploy=True)
    verify_railway_json("frontend/railway.json", allow_predeploy=False)
    verify_railway_json("apps/web/railway.json", allow_predeploy=False)

    for path in ("frontend/next.config.js", "apps/web/next.config.js"):
        content = read(path)
        if "output: 'standalone'" not in content and 'output: "standalone"' not in content:
            fail(f"{path} must enable standalone output")

    for path in ("frontend/Dockerfile", "apps/web/Dockerfile"):
        content = read(path)
        if ".next/standalone" not in content:
            fail(f"{path} must copy .next/standalone")
        if "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY" in content:
            fail(f"{path} must not expose admin keys through NEXT_PUBLIC env")

    for path in ("frontend/src/app/healthz/route.ts", "apps/web/app/healthz/route.ts"):
        content = read(path)
        if "status" not in content or "ok" not in content:
            fail(f"{path} must return a simple ok payload")

    print("RAILWAY_SURFACES_OK")


if __name__ == "__main__":
    main()
