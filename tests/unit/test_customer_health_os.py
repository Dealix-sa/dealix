"""Unit tests for the Customer Health OS router (Wave 16.0)."""
from __future__ import annotations

import os

import pytest

os.environ.setdefault("APP_ENV", "test")


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


# ── Helpers ──────────────────────────────────────────────────────────────────


def _make_client():
    """Return an AsyncClient wired to the test app."""
    from httpx import ASGITransport, AsyncClient
    from api.main import create_app

    app = create_app()
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


# ── Test 1: healthy customer → band = safe ───────────────────────────────────


@pytest.mark.anyio
async def test_churn_predict_safe() -> None:
    """A customer with no negative signals scores in the 'safe' band."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/customer-health/churn-predict",
            json={
                "customer_id": "cust_safe_001",
                "days_since_last_login": 2,
                "monthly_engagement_drop_pct": 0.0,
                "support_tickets_open": 0,
                "billing_failures_last_90d": 0,
                "nps": 9,
                "pipeline_added_drop_pct": 0.0,
                "months_as_customer": 12,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["customer_id"] == "cust_safe_001"
    assert data["band"] == "safe"
    assert data["is_estimate"] is True
    assert data["score"] < 0.25


# ── Test 2: distressed customer → band = critical ───────────────────────────


@pytest.mark.anyio
async def test_churn_predict_critical() -> None:
    """45 days no login + 3 open tickets + NPS=3 → 'critical' band."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/customer-health/churn-predict",
            json={
                "customer_id": "cust_critical_001",
                "days_since_last_login": 45,
                "monthly_engagement_drop_pct": 0.6,
                "support_tickets_open": 3,
                "billing_failures_last_90d": 2,
                "nps": 3,
                "pipeline_added_drop_pct": 0.6,
                "months_as_customer": 8,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["band"] == "critical"
    assert data["score"] >= 0.65
    assert data["is_estimate"] is True


# ── Test 3: batch sorted by score DESC ───────────────────────────────────────


@pytest.mark.anyio
async def test_churn_batch_sorted() -> None:
    """Batch endpoint returns results sorted by score descending."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/customer-health/churn-batch",
            json={
                "customers": [
                    {
                        "customer_id": "cust_healthy",
                        "days_since_last_login": 1,
                        "nps": 10,
                    },
                    {
                        "customer_id": "cust_critical",
                        "days_since_last_login": 45,
                        "support_tickets_open": 3,
                        "nps": 2,
                        "billing_failures_last_90d": 2,
                        "monthly_engagement_drop_pct": 0.6,
                    },
                    {
                        "customer_id": "cust_mid",
                        "days_since_last_login": 20,
                        "support_tickets_open": 1,
                    },
                ]
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    results = data["results"]
    assert len(results) == 3
    # Verify descending order
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)
    # Critical customer should be first
    assert results[0]["customer_id"] == "cust_critical"
    assert data["is_estimate"] is True
    assert "critical_count" in data
    assert "at_risk_count" in data


# ── Test 4: forecast with no deals → likely.revenue_sar == 0 ─────────────────


@pytest.mark.anyio
async def test_forecast_empty_deals() -> None:
    """Forecast with zero open deals returns likely revenue = 0."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/customer-health/forecast",
            json={
                "customer_id": "cust_forecast_001",
                "open_deals": [],
                "horizon_days": 30,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["customer_id"] == "cust_forecast_001"
    assert data["likely"]["revenue_sar"] == 0.0
    assert data["is_estimate"] is True
    assert "period_label" in data


# ── Test 5: critical customer → playbook priority P0 ─────────────────────────


@pytest.mark.anyio
async def test_intervention_playbook_critical() -> None:
    """Critical churn band yields a P0 playbook."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/customer-health/intervention-playbook",
            json={
                "customer_id": "cust_playbook_001",
                "days_since_last_login": 45,
                "support_tickets_open": 3,
                "billing_failures_last_90d": 2,
                "nps": 2,
                "monthly_engagement_drop_pct": 0.7,
                "months_as_customer": 10,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["churn_band"] == "critical"
    assert data["playbook"]["priority"] == "P0"
    assert len(data["playbook"]["actions_en"]) > 0
    assert len(data["playbook"]["actions_ar"]) > 0
    assert data["is_estimate"] is True


# ── Test 6: long-tenure healthy customer → expansion band ────────────────────


@pytest.mark.anyio
async def test_expansion_signals_healthy() -> None:
    """Long-tenure, high NPS, no issues customer is flagged for expansion."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/customer-health/expansion-signals",
            json={
                "customer_id": "cust_expand_001",
                "days_since_last_login": 1,
                "monthly_engagement_drop_pct": 0.0,
                "support_tickets_open": 0,
                "billing_failures_last_90d": 0,
                "nps": 9,
                "pipeline_added_drop_pct": 0.0,
                "months_as_customer": 12,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["customer_id"] == "cust_expand_001"
    assert data["band"] in ("expand_now", "potential")
    assert data["is_estimate"] is True
    assert 0.0 <= data["expansion_score"] <= 1.0
