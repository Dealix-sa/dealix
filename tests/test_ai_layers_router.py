"""Router-level tests for /api/v1/ai-layers/*."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.routers.ai_layers import router as ai_layers_router
from fastapi import FastAPI


@pytest.fixture()
def client() -> TestClient:
    app = FastAPI()
    app.include_router(ai_layers_router)
    return TestClient(app)


def test_catalog_lists_all_nine_layers(client: TestClient) -> None:
    r = client.get("/api/v1/ai-layers/")
    assert r.status_code == 200
    body = r.json()
    assert body["layer_count"] == 9
    assert "lead_scoring" in body["layers"]
    assert body["hard_gates"]["no_live_send"] is True


def test_layer_spec_known(client: TestClient) -> None:
    r = client.get("/api/v1/ai-layers/compliance_reasoning")
    assert r.status_code == 200
    body = r.json()
    assert body["layer"] == "compliance_reasoning"
    assert "spec" in body


def test_layer_spec_unknown_returns_404(client: TestClient) -> None:
    r = client.get("/api/v1/ai-layers/banana")
    assert r.status_code == 404


def test_run_lead_scoring(client: TestClient) -> None:
    r = client.post(
        "/api/v1/ai-layers/lead_scoring/run",
        json={
            "customer_id": "acme",
            "payload": {
                "title_founder_exec": True,
                "b2b_company": True,
                "crm_or_pipeline": True,
                "uses_or_plans_ai": True,
                "saudi_or_gcc": True,
                "urgent_within_30d": True,
            },
            "source_refs": ["founder://list/1"],
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["result"]["governance_decision"] == "ALLOW"
    assert body["result"]["output"]["route"] == "qualified_a"


def test_run_pipeline_with_block(client: TestClient) -> None:
    # PII without lawful_basis → compliance_reasoning blocks.
    r = client.post(
        "/api/v1/ai-layers/pipeline/run",
        json={
            "customer_id": "acme",
            "payload": {
                "contains_pii": True,
                "topic": "outreach",
                "action": "send_email",
                "evidence_refs": ["proof://1"],
                "account_name": "X",
                "data_classification": "internal",
                "processing_region": "sa",
            },
            "source_refs": ["founder://list/1"],
            "contains_pii_hint": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["result"]["overall_decision"] in ("BLOCK", "REQUIRE_APPROVAL")


def test_run_pipeline_subset(client: TestClient) -> None:
    r = client.post(
        "/api/v1/ai-layers/pipeline/run",
        json={
            "customer_id": "acme",
            "payload": {"title_founder_exec": True, "b2b_company": True},
            "source_refs": ["founder://x"],
            "layers": ["lead_scoring"],
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["result"]["layers_run"] == ["lead_scoring"]


def test_run_pipeline_unknown_layer_400(client: TestClient) -> None:
    r = client.post(
        "/api/v1/ai-layers/pipeline/run",
        json={
            "customer_id": "acme",
            "payload": {},
            "source_refs": ["x"],
            "layers": ["lead_scoring", "banana"],
        },
    )
    assert r.status_code == 400
