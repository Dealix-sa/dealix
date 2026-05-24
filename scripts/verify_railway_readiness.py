#!/usr/bin/env python3
"""verify_railway_readiness.py — Railway deploy contract.

Verifies:
  1. railway.toml + railway.json exist and parse.
  2. Both reference Dockerfile, healthcheckPath /healthz, and a predeploy.
  3. scripts/railway_predeploy.sh exists and respects RUN_RAILWAY_PRE_DEPLOY_MIGRATE.
  4. Dockerfile uses $PORT and a non-root start.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:  # < Python 3.11
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore

REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    failures: list[str] = []

    toml_path = REPO / "railway.toml"
    json_path = REPO / "railway.json"
    docker_path = REPO / "Dockerfile"
    pred_path = REPO / "scripts" / "railway_predeploy.sh"

    for p in (toml_path, json_path, docker_path, pred_path):
        if not p.exists():
            failures.append(f"missing:{p.relative_to(REPO)}")

    # ---- TOML ---------------------------------------------------------
    if toml_path.exists():
        text = toml_path.read_text(encoding="utf-8")
        if tomllib is not None:
            try:
                data = tomllib.loads(text)
            except Exception as exc:
                failures.append(f"toml_parse:{exc}")
                data = {}
        else:
            data = {}
        deploy = (data or {}).get("deploy", {}) if isinstance(data, dict) else {}
        if "/healthz" not in text:
            failures.append("railway_toml_missing_healthz")
        if "preDeployCommand" not in text and not deploy.get("preDeployCommand"):
            failures.append("railway_toml_missing_predeploy")
        if "Dockerfile" not in text:
            failures.append("railway_toml_missing_dockerfile_ref")

    # ---- JSON ---------------------------------------------------------
    if json_path.exists():
        try:
            jdata = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"railway_json_parse:{exc}")
            jdata = {}
        deploy = jdata.get("deploy", {}) if isinstance(jdata, dict) else {}
        if deploy.get("healthcheckPath") != "/healthz":
            failures.append("railway_json_healthcheck_not_healthz")
        if "preDeployCommand" not in deploy:
            failures.append("railway_json_missing_predeploy")

    # ---- Dockerfile ---------------------------------------------------
    if docker_path.exists():
        body = docker_path.read_text(encoding="utf-8", errors="ignore")
        if "$PORT" not in body and "${PORT" not in body:
            failures.append("dockerfile_missing_PORT")
        if "USER " not in body:
            failures.append("dockerfile_runs_as_root")

    # ---- Predeploy ----------------------------------------------------
    if pred_path.exists():
        body = pred_path.read_text(encoding="utf-8", errors="ignore")
        if "RUN_RAILWAY_PRE_DEPLOY_MIGRATE" not in body:
            failures.append("predeploy_missing_skip_env_guard")
        if "DATABASE_URL" not in body:
            failures.append("predeploy_missing_db_guard")

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(f"RAILWAY_READINESS_PASS={'true' if ok else 'false'} (failures={len(failures)})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
