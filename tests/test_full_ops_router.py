"""Smoke tests for the Full Ops Sales System API router (Wave 20)."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from auto_client_acquisition.agent_os import clear_agent_registry_for_tests
from auto_client_acquisition.full_ops_os import audit_store
import api.routers.full_ops_os as full_ops_router


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FULL_OPS_AUDIT_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    audit_store.clear_for_test()
    clear_agent_registry_for_tests()
    full_ops_router._ORCHESTRATOR = None  # fresh in-memory orchestrator
    yield
    audit_store.clear_for_test()
    clear_agent_registry_for_tests()
    full_ops_router._ORCHESTRATOR = None


@pytest.fixture()
def client() -> TestClient:
    app = FastAPI()
    app.include_router(full_ops_router.router)
    return TestClient(app)


def test_status_endpoint(client: TestClient) -> None:
    resp = client.get("/api/v1/full-ops-os/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["stages"] == 12
    assert body["governance_decision"] == "ok"


def test_agents_endpoint_lists_pyramid(client: TestClient) -> None:
    resp = client.get("/api/v1/full-ops-os/agents")
    assert resp.status_code == 200
    assert resp.json()["count"] == 18


def test_create_run_requires_customer_id(client: TestClient) -> None:
    resp = client.post("/api/v1/full-ops-os/runs", json={})
    assert resp.status_code == 400


def test_full_run_lifecycle(client: TestClient) -> None:
    created = client.post(
        "/api/v1/full-ops-os/runs",
        json={"customer_id": "acme", "lead": {"company_name": "Acme", "source": "referral"}},
    )
    assert created.status_code == 200
    run_id = created.json()["run"]["run_id"]

    run_all = client.post(f"/api/v1/full-ops-os/runs/{run_id}/run-all")
    assert run_all.status_code == 200
    body = run_all.json()
    assert body["stages_run"] == 12
    assert body["stages_gated"] >= 1  # the approval gate stage
    assert body["run"]["state"] == "completed"

    detail = client.get(f"/api/v1/full-ops-os/runs/{run_id}")
    assert detail.status_code == 200
    assert detail.json()["audit_entries"] >= 14


def test_advance_steps_one_stage(client: TestClient) -> None:
    run_id = client.post(
        "/api/v1/full-ops-os/runs", json={"customer_id": "acme"}
    ).json()["run"]["run_id"]
    resp = client.post(f"/api/v1/full-ops-os/runs/{run_id}/advance")
    assert resp.status_code == 200
    assert resp.json()["result"]["stage"] == "SIGNAL_INTAKE"


def test_run_approvals_lists_gated_stages(client: TestClient) -> None:
    run_id = client.post(
        "/api/v1/full-ops-os/runs", json={"customer_id": "acme"}
    ).json()["run"]["run_id"]
    client.post(f"/api/v1/full-ops-os/runs/{run_id}/run-all")
    resp = client.get(f"/api/v1/full-ops-os/runs/{run_id}/approvals")
    assert resp.status_code == 200
    assert resp.json()["count"] >= 1


def test_unknown_run_returns_404(client: TestClient) -> None:
    resp = client.get("/api/v1/full-ops-os/runs/run_does_not_exist")
    assert resp.status_code == 404
