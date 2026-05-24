"""HTTP-level tests for the AI Stack router (``/api/v1/ai-stack/*``)."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.ai_stack import reset_orchestrator_for_tests, router as ai_stack_router


@pytest.fixture
def client() -> TestClient:
    reset_orchestrator_for_tests()
    app = FastAPI()
    app.include_router(ai_stack_router)
    return TestClient(app)


def _run_body(*, tier: str = "free_diagnostic") -> dict:
    return {
        "tenant_id": "acme",
        "customer_handle": "acme_handle",
        "company_name": "Acme Corp",
        "sector": "technology",
        "challenge_ar": "نحتاج تحسين عملية البيع",
        "challenge_en": "we need to improve our sales process",
        "offer_tier": tier,
        "source_passport": {
            "source_id": "intake_test_001",
            "source_type": "customer_intake",
            "owner": "test_owner",
            "allowed_use": ["ai_assist"],
            "contains_pii": False,
            "sensitivity": "internal",
            "retention_policy": "90d",
            "ai_access_allowed": True,
            "external_use_allowed": False,
        },
    }


class TestStatusEndpoint:
    def test_status_returns_eleven_layers(self, client: TestClient) -> None:
        r = client.get("/api/v1/ai-stack/status")
        assert r.status_code == 200
        data = r.json()
        assert data["overall_healthy"] is True
        assert len(data["layers"]) == 11
        assert data["hard_gates"]["self_evolving_shadow_only"] is True

    def test_status_layer_payload_shape(self, client: TestClient) -> None:
        r = client.get("/api/v1/ai-stack/status")
        assert r.status_code == 200
        layers = r.json()["layers"]
        for layer in layers:
            assert "layer" in layer
            assert "label" in layer
            assert "module" in layer
            assert "healthy" in layer


class TestLayersEndpoint:
    def test_layers_endpoint_lists_all_modules(self, client: TestClient) -> None:
        r = client.get("/api/v1/ai-stack/layers")
        assert r.status_code == 200
        data = r.json()
        assert len(data["layers"]) == 11
        assert data["hard_gates"]["no_live_send"] is True
        assert data["hard_gates"]["bilingual_required"] is True


class TestRunEndpoint:
    def test_run_returns_full_result(self, client: TestClient) -> None:
        r = client.post("/api/v1/ai-stack/run", json=_run_body())
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["tenant_id"] == "acme"
        assert data["proof_pack_id"] is not None
        assert len(data["layers"]) == 11
        assert data["doctrine_clean"] is True
        assert data["governance_blocked"] is False

    def test_run_then_fetch_by_id(self, client: TestClient) -> None:
        r = client.post("/api/v1/ai-stack/run", json=_run_body())
        run_id = r.json()["run_id"]
        fetched = client.get(f"/api/v1/ai-stack/run/{run_id}")
        assert fetched.status_code == 200
        assert fetched.json()["run_id"] == run_id

    def test_fetch_unknown_run_returns_404(self, client: TestClient) -> None:
        r = client.get("/api/v1/ai-stack/run/does_not_exist")
        assert r.status_code == 404

    def test_invalid_body_returns_422(self, client: TestClient) -> None:
        bad = _run_body()
        bad["challenge_ar"] = ""  # too short
        r = client.post("/api/v1/ai-stack/run", json=bad)
        assert r.status_code == 422

    def test_invalid_offer_tier_returns_422(self, client: TestClient) -> None:
        bad = _run_body()
        bad["offer_tier"] = "not_a_tier"
        r = client.post("/api/v1/ai-stack/run", json=bad)
        assert r.status_code == 422

    def test_run_for_managed_ops_tier(self, client: TestClient) -> None:
        r = client.post("/api/v1/ai-stack/run", json=_run_body(tier="managed_ops"))
        assert r.status_code == 200
        data = r.json()
        assert data["offer_tier"] == "managed_ops"


class TestProposalsEndpoint:
    def test_proposals_endpoint_returns_pending_list(self, client: TestClient) -> None:
        # Without any feedback there should be 0 proposals.
        r = client.get("/api/v1/ai-stack/proposals/empty_tenant")
        assert r.status_code == 200
        data = r.json()
        assert data["tenant_id"] == "empty_tenant"
        assert data["proposal_count"] == 0

    def test_proposals_endpoint_rejects_invalid_severity(self, client: TestClient) -> None:
        r = client.get(
            "/api/v1/ai-stack/proposals/x",
            params={"minimum_severity": "yolo"},
        )
        assert r.status_code == 400

    def test_proposals_endpoint_rejects_negative_days(self, client: TestClient) -> None:
        r = client.get(
            "/api/v1/ai-stack/proposals/x",
            params={"since_days": -1},
        )
        assert r.status_code == 400


class TestDoctrineHardGates:
    def test_status_advertises_hard_gates(self, client: TestClient) -> None:
        r = client.get("/api/v1/ai-stack/status")
        gates = r.json()["hard_gates"]
        assert gates["no_live_send"] is True
        assert gates["no_live_charge"] is True
        assert gates["no_invented_kpis"] is True
        assert gates["no_revenue_before_invoice_paid"] is True
        assert gates["source_passport_required"] is True
        assert gates["bilingual_required"] is True
        assert gates["self_evolving_shadow_only"] is True
