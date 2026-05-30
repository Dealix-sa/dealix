"""Custom Systems OS router — contract tests + api.main wiring check."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import custom_systems
from auto_client_acquisition.capital_os import capital_ledger
from auto_client_acquisition.custom_systems_os import ledger as cs_ledger


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_CUSTOM_SYSTEMS_PATH", str(tmp_path / "cs.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    monkeypatch.setattr(custom_systems, "_EXPORT_DIR", str(tmp_path / "exports"))
    cs_ledger.clear_for_test()
    capital_ledger.clear_for_test()
    app = FastAPI()
    app.include_router(custom_systems.router)
    return TestClient(app)


def test_health_ok(client):
    resp = client.get("/api/v1/custom-systems/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["system"] == "custom_systems_os"
    assert body["hard_gates"]["min_paid_pilots"] == 3


def test_entry_check_blocks_under_three_pilots(client):
    resp = client.post(
        "/api/v1/custom-systems/entry-check",
        json={"paid_pilots_completed": 1, "workflow_owner_present": True},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["allowed"] is False
    assert "no_customization_before_3_paid_pilots" in body["blocked_reasons"]
    assert body["delivery_mode"] == "founder_assisted"
    assert body["safe_to_send"] is False


def test_run_without_passport_is_governed_not_crash(client):
    resp = client.post(
        "/api/v1/custom-systems/run",
        json={
            "customer_id": "c1",
            "customer_name": "Acme",
            "engagement_id": "e1",
            "paid_pilots_completed": 3,
            "declared_modules": ["m"],
            "declared_workflows": ["w"],
            "workflow_owner_present": True,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["next_step"] == "blocked_source_passport"
    assert body["safe_to_send"] is False


def test_run_happy_path_assembles(client):
    resp = client.post(
        "/api/v1/custom-systems/run",
        json={
            "customer_id": "c1",
            "customer_name": "Acme Corp",
            "engagement_id": "e_ok",
            "paid_pilots_completed": 3,
            "declared_modules": ["sales_inbox", "support_desk"],
            "declared_workflows": ["weekly_growth"],
            "workflow_owner_present": True,
            "adoption_score": 75.0,
            "passport": {
                "source_id": "s1",
                "allowed_use": ["internal_analysis"],
                "ai_access_allowed": True,
            },
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["proof_complete"] is True
    assert len(body["capital_assets"]) >= 1
    assert body["safe_to_send"] is False
    assert body["approval_required"] is True
    assert body["next_step"] == "deliver_for_founder_review"


def test_extra_field_rejected(client):
    resp = client.post(
        "/api/v1/custom-systems/entry-check",
        json={"paid_pilots_completed": 3, "workflow_owner_present": True, "nope": 1},
    )
    assert resp.status_code == 422  # extra="forbid"


def test_engagements_listing(client):
    client.post(
        "/api/v1/custom-systems/run",
        json={
            "customer_id": "c-list",
            "customer_name": "Acme Corp",
            "engagement_id": "e-list",
            "paid_pilots_completed": 3,
            "declared_modules": ["m"],
            "declared_workflows": ["w"],
            "workflow_owner_present": True,
            "passport": {"source_id": "s1", "allowed_use": ["internal_analysis"]},
        },
    )
    resp = client.get("/api/v1/custom-systems/engagements/c-list")
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] >= 1
    assert any(e["engagement_id"] == "e-list" for e in body["engagements"])


def test_router_wired_into_api_main():
    # The optional router must be registered on the real app.
    from api.main import app

    paths = {getattr(r, "path", "") for r in app.routes}
    assert "/api/v1/custom-systems/health" in paths
    assert "/api/v1/custom-systems/run" in paths
