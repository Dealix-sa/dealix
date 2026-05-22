"""Unit tests for the Revenue Forecast OS router (Wave 16)."""
from __future__ import annotations

import os

os.environ.setdefault("APP_ENV", "test")

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.routers.revenue_forecast import router as revenue_forecast_router


# ── Fixture: standalone app ───────────────────────────────────────────────────


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def app() -> FastAPI:
    _app = FastAPI()
    _app.include_router(revenue_forecast_router)
    return _app


# ── 1. Empty pipeline → all bands are zero ───────────────────────────────────


@pytest.mark.anyio
async def test_forecast_empty_pipeline(app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/revenue-forecast/forecast",
            json={"customer_id": "cust_001", "open_deals": [], "horizon_days": 30},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_estimate"] is True
    assert data["best"]["revenue_sar"] == 0.0
    assert data["likely"]["revenue_sar"] == 0.0
    assert data["worst"]["revenue_sar"] == 0.0


# ── 2. Deals in proposal stage → likely > 0 ──────────────────────────────────


@pytest.mark.anyio
async def test_forecast_with_deals(app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/revenue-forecast/forecast",
            json={
                "customer_id": "cust_002",
                "open_deals": [
                    {
                        "id": "deal_1",
                        "company_name": "Acme",
                        "stage": "proposal",
                        "value_sar": 50000.0,
                        "days_in_stage": 5,
                        "multi_threaded": False,
                    }
                ],
                "horizon_days": 30,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_estimate"] is True
    assert data["likely"]["revenue_sar"] > 0.0
    assert len(data["deals_breakdown"]) == 1


# ── 3. Attribution linear — 3 touchpoints → returns result ───────────────────


@pytest.mark.anyio
async def test_attribution_linear(app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/revenue-forecast/attribution",
            json={
                "customer_id": "cust_003",
                "touchpoints": [
                    {"channel": "email", "timestamp": "2026-01-01T10:00:00Z", "value_sar": 1000.0},
                    {"channel": "whatsapp", "timestamp": "2026-01-05T12:00:00Z", "value_sar": 0.0},
                    {"channel": "meeting", "timestamp": "2026-01-10T14:00:00Z", "value_sar": 0.0},
                ],
                "model": "linear",
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_estimate"] is True
    assert data["model"] == "linear"
    assert data["touchpoint_count"] == 3
    assert "by_channel" in data


# ── 4. GET /pipeline-health returns stage_probabilities dict ─────────────────


@pytest.mark.anyio
async def test_pipeline_health_returns_stages(app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/revenue-forecast/pipeline-health?horizon_days=30")
    assert resp.status_code == 200
    data = resp.json()
    assert "stage_probabilities" in data
    probs = data["stage_probabilities"]
    assert isinstance(probs, dict)
    assert len(probs) > 0
    # Spot-check known stages
    assert "proposal" in probs
    assert "new" in probs
    assert data["is_estimate"] is False


# ── 5. POST /scenarios returns keys 30, 60, 90 ───────────────────────────────


@pytest.mark.anyio
async def test_scenarios_three_horizons(app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/revenue-forecast/scenarios",
            json={"customer_id": "cust_004", "open_deals": [], "horizon_days": 30},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_estimate"] is True
    scenarios = data["scenarios"]
    # Keys are returned as strings by JSON serialisation
    assert set(str(k) for k in scenarios.keys()) == {"30", "60", "90"}
    for horizon_key in ("30", "60", "90"):
        band = scenarios[horizon_key]
        assert "best" in band
        assert "likely" in band
        assert "worst" in band
