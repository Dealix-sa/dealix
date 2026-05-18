"""CEO GTM operating system."""

from __future__ import annotations

import yaml
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import health
from dealix.commercial_ops.ceo_gtm_operating_system import (
    build_ceo_gtm_status,
    build_status_snapshot,
    run_backlog_status,
    run_gtm_pipeline,
    run_offers,
    run_railway,
)
from dealix.commercial_ops.paths import REPO_ROOT


def test_ceo_gtm_status_detects_ui_drift() -> None:
    blob = build_ceo_gtm_status(
        api_base=False,
        ui_start="./start.sh",
        ui_predeploy='echo "no migration needed"',
    )
    assert blob["railway_ui"]["founder_railway_ui_action"] == "REQUIRED"
    assert blob["verdict"] == "ACTION_REQUIRED"
    assert blob["railway_ui"]["start_command_hint"]
    assert blob["railway_ui"]["predeploy_hint"]


def test_backlog_has_50_plus_tasks() -> None:
    st = run_backlog_status()
    assert st["ok"] is True
    assert st["task_count"] >= 50


def test_offer_and_gtm_configs() -> None:
    assert run_offers()["ok"] is True
    assert run_gtm_pipeline()["ok"] is True


def test_railway_repo_passes_skip_live() -> None:
    blob = run_railway(skip_live=True)
    assert blob["repo"]["ok"] is True


def test_status_snapshot_keys() -> None:
    snap = build_status_snapshot()
    assert "railway" in snap and "backlog" in snap


def test_version_endpoint_on_health_router() -> None:
    app = FastAPI()
    app.include_router(health.router)
    client = TestClient(app)
    r = client.get("/version")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_backlog_yaml_loads() -> None:
    path = REPO_ROOT / "dealix/config/ceo_founder_execution_backlog.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert len(data["tasks"]) >= 50
