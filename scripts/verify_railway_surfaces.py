#!/usr/bin/env python3
"""Verify Railway deploy surfaces for API and canonical web services.

apps/web is the canonical frontend surface. A legacy frontend/ service may remain
in historical config while it is being retired; it is validated only when its
root directory exists. This keeps CI focused on real production surfaces instead
of requiring stale compatibility files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SERVICE_MATRIX = ROOT / "dealix/config/railway_services.json"

REQUIRED_FILES = [
    "Dockerfile",
    "railway.json",
    "api/routers/health.py",
    "dealix/config/railway_services.json",
    "apps/web/Dockerfile",
    "apps/web/railway.json",
    "apps/web/next.config.js",
    "apps/web/app/healthz/route.ts",
]

OPTIONAL_LEGACY_FRONTEND_FILES = [
    "frontend/Dockerfile",
    "frontend/railway.json",
    "frontend/next.config.ts",
    "frontend/src/app/healthz/route.ts",
]

FORBIDDEN_PUBLIC_SECRET_MARKERS = [
    "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY",
    "NEXT_PUBLIC_ADMIN_API_KEY",
    "NEXT_PUBLIC_API_KEY=",
]


def fail(message: str) -> None:
    raise SystemExit(f"RAILWAY_SURFACES_FAIL: {message}")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        fail(f"missing {path}")
    return target.read_text(encoding="utf-8")


def load_json(path: str) -> dict[str, Any]:
    try:
        return json.loads(read(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")


def service_path(root_dir: str, path: str) -> str:
    prefix = root_dir.rstrip("/")
    return f"{prefix}/{path}" if prefix not in ("", ".") else path


def verify_railway_json(path: str, *, allow_predeploy: bool) -> None:
    cfg = load_json(path)
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


def verify_service_matrix() -> None:
    matrix = load_json("dealix/config/railway_services.json")
    services = matrix.get("services")
    if not isinstance(services, list) or len(services) < 3:
        fail("dealix/config/railway_services.json must list API, apps/web, and background services")

    names = {svc.get("name") for svc in services if isinstance(svc, dict)}
    required = {"dealix-api", "dealix-apps-web"}
    if not required.issubset(names):
        missing = sorted(required - names)
        fail(f"railway service names missing required services: {missing} not in {sorted(names)}")

    core_services = {"dealix-api", "dealix-apps-web"}

    for svc in services:
        if not isinstance(svc, dict):
            fail("railway service entry must be an object")
        name = str(svc.get("name", ""))
        railway_config = str(svc.get("railwayConfig", ""))
        dockerfile = str(svc.get("dockerfilePath", ""))
        root_dir = str(svc.get("rootDirectory", ""))
        healthcheck = str(svc.get("healthcheckPath", ""))
        required_env = svc.get("requiredEnv")

        if not name or not dockerfile:
            fail(f"{name or '<unnamed>'}: missing name or dockerfilePath")

        if name == "dealix-frontend" and not exists(root_dir):
            # Legacy frontend service may remain documented while apps/web is canonical.
            continue

        if name in core_services or name == "dealix-frontend":
            if not railway_config:
                fail(f"{name}: missing railwayConfig")
            if healthcheck != "/healthz":
                fail(f"{name}: healthcheckPath must be /healthz")
            if not isinstance(required_env, list):
                fail(f"{name}: requiredEnv must be a list")
            read(railway_config)
            read(service_path(root_dir, dockerfile))


def verify_web_surface(prefix: str, *, next_config: str, dockerfile: str, healthz: str) -> None:
    content = read(next_config)
    if "output: 'standalone'" not in content and 'output: "standalone"' not in content:
        fail(f"{next_config} must enable standalone output")

    docker = read(dockerfile)
    if ".next/standalone" not in docker:
        fail(f"{dockerfile} must copy .next/standalone")
    for marker in FORBIDDEN_PUBLIC_SECRET_MARKERS:
        if marker in docker:
            fail(f"{dockerfile} must not expose secrets through public env marker {marker}")

    health = read(healthz)
    if "status" not in health or "ok" not in health:
        fail(f"{healthz} must return a simple ok payload")


def main() -> None:
    for path in REQUIRED_FILES:
        read(path)

    legacy_present = exists("frontend")
    if legacy_present:
        for path in OPTIONAL_LEGACY_FRONTEND_FILES:
            read(path)

    verify_service_matrix()
    verify_railway_json("railway.json", allow_predeploy=True)
    verify_railway_json("apps/web/railway.json", allow_predeploy=False)
    verify_web_surface(
        "apps/web",
        next_config="apps/web/next.config.js",
        dockerfile="apps/web/Dockerfile",
        healthz="apps/web/app/healthz/route.ts",
    )

    if legacy_present:
        verify_railway_json("frontend/railway.json", allow_predeploy=False)
        verify_web_surface(
            "frontend",
            next_config="frontend/next.config.ts",
            dockerfile="frontend/Dockerfile",
            healthz="frontend/src/app/healthz/route.ts",
        )

    print("RAILWAY_SURFACES_OK")


if __name__ == "__main__":
    main()
