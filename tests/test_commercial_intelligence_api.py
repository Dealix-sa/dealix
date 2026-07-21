"""Integration tests for the new commercial intelligence API surface."""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from api.routers.ceo_brief import router as ceo_brief_router
from api.routers.customer_onboarding import router as onboarding_router
from api.routers.intelligence_health import router as health_router
from api.routers.lead_ingestion import router as lead_ingestion_router
from api.routers.market_intelligence import router as market_intel_router


@pytest.fixture
def client():
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(market_intel_router)
    app.include_router(ceo_brief_router)
    app.include_router(onboarding_router)
    app.include_router(health_router)
    app.include_router(lead_ingestion_router)
    return TestClient(app)


def test_score_prospect(client):
    response = client.post("/api/v1/market-intelligence/score-prospect", json={
        "company_name": "Najm Tech",
        "sector": "software",
        "city": "Riyadh",
        "employees_estimate": 45,
        "website": "https://najmtech.sa",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "Najm Tech"
    assert data["score"] >= 80
    assert data["recommended_package"] in ["Lead Sprint", "Pilot Service Pack", "Revenue Diagnostic"]


def test_analyze_pipeline(client):
    response = client.post("/api/v1/market-intelligence/analyze-pipeline", json={
        "deals": [
            {
                "deal_id": "d1",
                "company_name": "Test Co",
                "stage": "qualified",
                "value_sar": 5000,
                "created_at": datetime.utcnow().isoformat(),
                "last_activity_at": datetime.utcnow().isoformat(),
            }
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert "pipeline_health" in data
    assert data["total_pipeline_sar"] == 5000


def test_synthesize_decision(client):
    response = client.post("/api/v1/market-intelligence/synthesize-decision", json={
        "question": "Should we proceed?",
        "evidence": [
            {
                "evidence_id": "e1",
                "evidence_type": "metric",
                "title": "Uplift",
                "description": "30% revenue uplift",
                "source": "pilot",
                "created_at": datetime.utcnow().isoformat(),
                "verified": True,
            }
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert "decision_type" in data
    assert data["confidence"] > 0


def test_intelligence_health(client):
    response = client.get("/api/v1/intelligence-health/status")
    assert response.status_code == 200
    data = response.json()
    assert data["overall"] in ["healthy", "degraded"]
    assert "checks" in data


def test_lead_ingestion(client):
    response = client.post("/api/v1/ingest/lead", json={
        "source": "manual",
        "company": "Test Co",
        "name": "Test User",
        "email": "test@example.sa",
        "sector": "software",
        "city": "Riyadh",
        "employees": 30,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] in ["qualified", "nurture"]
    assert data["icp_score"] >= 0


def test_customer_onboarding_start(client):
    response = client.post("/api/v1/onboarding/start", json={
        "company_name": "Test Co",
        "package": "Revenue Diagnostic",
        "primary_contact_name": "Ahmed",
        "primary_contact_email": "ahmed@test.sa",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"]
    assert data["current_stage"] == "kickoff"
    assert len(data["milestones"]) > 0


def test_ceo_brief_generate(client):
    response = client.post("/api/v1/ceo-brief/generate")
    assert response.status_code == 200
    data = response.json()
    assert "markdown" in data
    assert "json_data" in data
    assert "pipeline" in data["json_data"]
