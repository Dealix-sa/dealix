"""Railway config foundation — lock railway.toml/json/Dockerfile to the canonical yaml.

These tests exist so the production start contract cannot silently drift:
- no `startCommand` (app starts via Dockerfile CMD /app/start.sh, which reads $PORT)
- healthcheck, restart policy, retries, and timeout match railway_ui_canonical.yaml
- railway.toml and railway.json stay in agreement
- the canonical cross-check actually detects drift (not a vacuous pass)
"""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

import yaml

from dealix.commercial_ops.railway_production import (
    FORBIDDEN_START_COMMANDS,
    check_config_matches_canonical,
    check_repo_railway_config,
    load_canonical_config,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
RAILWAY_TOML = REPO_ROOT / "railway.toml"
RAILWAY_JSON = REPO_ROOT / "railway.json"
DOCKERFILE = REPO_ROOT / "Dockerfile"


def _toml() -> dict:
    return tomllib.loads(RAILWAY_TOML.read_text(encoding="utf-8"))


def _json() -> dict:
    return json.loads(RAILWAY_JSON.read_text(encoding="utf-8"))


def _canonical_deploy() -> dict:
    return (load_canonical_config().get("deploy") or {})


# --- foundation is internally consistent ----------------------------------


def test_repo_config_ok_and_canonical_clean() -> None:
    repo = check_repo_railway_config()
    assert repo["ok"], repo["issues"]
    assert not repo["warnings"], repo["warnings"]
    canonical = repo.get("canonical") or {}
    assert canonical.get("canonical_loaded") is True
    assert canonical.get("ok") is True, canonical.get("issues")


def test_no_active_start_command_in_toml() -> None:
    # The only permitted mention is the "# NO startCommand" comment marker.
    for line in RAILWAY_TOML.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        assert not re.match(r"^startCommand\s*=", stripped), f"active startCommand: {line!r}"
    assert "startCommand" not in _toml().get("deploy", {})


def test_json_start_command_is_null() -> None:
    assert _json()["deploy"]["startCommand"] is None


def test_no_forbidden_start_command_anywhere() -> None:
    toml_text = RAILWAY_TOML.read_text(encoding="utf-8")
    json_text = RAILWAY_JSON.read_text(encoding="utf-8")
    for bad in FORBIDDEN_START_COMMANDS:
        assert bad not in toml_text, f"railway.toml must not contain {bad!r}"
        assert bad not in json_text, f"railway.json must not contain {bad!r}"


# --- both files match the canonical yaml ----------------------------------


def test_healthcheck_matches_canonical() -> None:
    dep = _canonical_deploy()
    want_path = dep.get("healthcheck_path", "/healthz")
    want_timeout = int(dep.get("healthcheck_timeout_sec", 300))
    for cfg in (_toml(), _json()):
        assert cfg["deploy"]["healthcheckPath"] == want_path
        assert int(cfg["deploy"]["healthcheckTimeout"]) == want_timeout


def test_restart_policy_matches_canonical() -> None:
    dep = _canonical_deploy()
    want_type = dep.get("restart_policy", "ON_FAILURE")
    want_retries = int(dep.get("restart_max_retries", 3))
    for cfg in (_toml(), _json()):
        assert cfg["deploy"]["restartPolicyType"] == want_type
        assert int(cfg["deploy"]["restartPolicyMaxRetries"]) == want_retries


def test_builder_is_dockerfile() -> None:
    for cfg in (_toml(), _json()):
        assert cfg["build"]["builder"].upper() == "DOCKERFILE"


def test_predeploy_invokes_canonical_script() -> None:
    for cfg in (_toml(), _json()):
        assert "railway_predeploy" in cfg["deploy"]["preDeployCommand"]


def test_toml_and_json_agree() -> None:
    td, jd = _toml()["deploy"], _json()["deploy"]
    for key in (
        "healthcheckPath",
        "healthcheckTimeout",
        "restartPolicyType",
        "restartPolicyMaxRetries",
        "numReplicas",
    ):
        assert td.get(key) == jd.get(key), f"disagreement on {key}"


def test_dockerfile_cmd_is_canonical_start() -> None:
    dep = _canonical_deploy()
    want_start = dep.get("start_command_canonical", "/app/start.sh")
    docker = DOCKERFILE.read_text(encoding="utf-8")
    assert want_start in docker
    assert f'CMD ["{want_start}"]' in docker


# --- the guard is not vacuous: it detects real drift ----------------------


def test_cross_check_detects_drift(tmp_path, monkeypatch) -> None:
    import dealix.commercial_ops.railway_production as rp

    drifted = tmp_path / "railway.toml"
    drifted.write_text(
        "\n".join(
            [
                "[build]",
                'builder = "DOCKERFILE"',
                'dockerfilePath = "Dockerfile"',
                "[deploy]",
                'startCommand = "uvicorn api.main:app --host 0.0.0.0 --port 8000"',
                'preDeployCommand = "sh /app/scripts/railway_predeploy.sh"',
                'healthcheckPath = "/healthz"',
                "healthcheckTimeout = 300",
                'restartPolicyType = "ON_FAILURE"',
                "restartPolicyMaxRetries = 10",
                "numReplicas = 1",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(rp, "RAILWAY_TOML", drifted)
    result = rp.check_config_matches_canonical()
    assert result["ok"] is False
    blob = " ".join(result["issues"])
    assert "restartPolicyMaxRetries" in blob
    assert "forbidden" in blob


def test_canonical_yaml_is_parseable() -> None:
    data = yaml.safe_load((REPO_ROOT / "dealix/config/railway_ui_canonical.yaml").read_text("utf-8"))
    assert isinstance(data, dict)
    assert "deploy" in data
