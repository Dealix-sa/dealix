"""Smoke test — Growth OS revenue router endpoints respond 200."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.growth_os_revenue import router as growth_os_revenue_router


@pytest.fixture()
def client() -> TestClient:
    app = FastAPI()
    app.include_router(growth_os_revenue_router)
    return TestClient(app)


GET_ENDPOINTS = [
    "/api/v1/growth-os/icp-matrix",
    "/api/v1/growth-os/abm/pipeline-stages",
    "/api/v1/growth-os/geo/pages",
    "/api/v1/growth-os/content/cta-matrix",
    "/api/v1/growth-os/revenue/statuses",
    "/api/v1/growth-os/attribution/types",
    "/api/v1/growth-os/dashboard/red-flags-catalog",
    "/api/v1/growth-os/streams/portfolio",
    "/api/v1/growth-os/funnels",
    "/api/v1/growth-os/partners/motion",
    "/api/v1/growth-os/brand/positioning",
    "/api/v1/growth-os/operating-rules",
]


@pytest.mark.parametrize("path", GET_ENDPOINTS)
def test_get_endpoint_returns_200(client: TestClient, path: str) -> None:
    response = client.get(path)
    assert response.status_code == 200, f"{path} -> {response.status_code}"
    body = response.json()
    assert body["governance_decision"] == "ALLOW"
    assert body["hard_gates"]["no_external_send"] is True


def test_post_geo_validate_page(client: TestClient) -> None:
    response = client.post(
        "/api/v1/growth-os/geo/validate-page",
        json={"path": "/x", "sections": {}},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["payload"]["report"]["is_compliant"] is False


def test_post_revenue_verify_rejects_unverified(client: TestClient) -> None:
    payload = {
        "record_id": "rev_001",
        "customer_id": "cust_001",
        "offer_key": "x",
        "amount_usd": 100.0,
        "status": "paid",
    }
    response = client.post("/api/v1/growth-os/revenue/verify", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["payload"]["is_real_revenue"] is False


def test_post_attribution_analyze(client: TestClient) -> None:
    payload = {
        "records": [
            {
                "record_id": "r1",
                "customer_id": "cust_001",
                "offer_key": "ai_trust_kit",
                "amount_usd": 1000.0,
                "status": "paid",
                "verification": {"kind": "payment", "reference": "pay_1"},
                "attributed_channels": ["referral"],
            }
        ],
        "dimensions": ["channel", "offer"],
    }
    response = client.post("/api/v1/growth-os/attribution/analyze", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "channel" in body["payload"]["breakdowns"]
    assert body["payload"]["breakdowns"]["channel"]["totals"]["referral"] == 1000.0


def test_post_experiment_evaluate(client: TestClient) -> None:
    payload = {
        "card": {
            "experiment_id": "e1",
            "hypothesis": "Variant B will win on signups",
            "audience": "founders",
            "variant_a": "a",
            "variant_b": "b",
            "success_metric": "signups",
            "minimum_sample": 100,
        },
        "result": {
            "variant_a_outcome": 10,
            "variant_b_outcome": 25,
            "variant_a_sample": 200,
            "variant_b_sample": 200,
        },
    }
    response = client.post("/api/v1/growth-os/experiments/evaluate", json=payload)
    assert response.status_code == 200
    assert response.json()["payload"]["decision"]["decision"] == "scale_variant_b"


def test_post_dashboard_snapshot(client: TestClient) -> None:
    payload = {
        "metrics": {
            "period_start": datetime(2026, 5, 1, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 5, 31, tzinfo=UTC).isoformat(),
            "real_revenue_usd": 0.0,
        }
    }
    response = client.post("/api/v1/growth-os/dashboard/snapshot", json=payload)
    assert response.status_code == 200
    body = response.json()
    keys = {f["key"] for f in body["payload"]["red_flags"]}
    assert "no_real_revenue" in keys


def test_post_streams_decide(client: TestClient) -> None:
    payload = {
        "stream_key": "x",
        "bucket": "monthly",
        "label_ar": "x",
        "label_en": "x",
        "margin_pct": 0.70,
        "retainer_potential": 0.9,
        "risk": "low",
        "effort_hours_per_unit": 5.0,
        "repeatability": "retainer_native",
    }
    response = client.post("/api/v1/growth-os/streams/decide", json=payload)
    assert response.status_code == 200
    assert response.json()["payload"]["decision"]["action"] == "scale"


def test_post_operating_rules_check(client: TestClient) -> None:
    response = client.post(
        "/api/v1/growth-os/operating-rules/check",
        json={"kind": "campaign", "asset": {"id": "c1"}},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["payload"]["is_clean"] is False
