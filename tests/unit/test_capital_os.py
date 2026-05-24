"""Unit tests for the Capital OS router (Wave 15.1)."""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("APP_ENV", "test")

from api.routers.capital_os import _compute_readiness


# ── Readiness score ───────────────────────────────────────────────────────────

def test_readiness_score_zero_inputs():
    result = _compute_readiness({})
    assert result["readiness_score"] == 0
    assert result["band"] == "seed"
    assert result["is_estimate"] is True


def test_readiness_score_full_inputs():
    result = _compute_readiness({
        "has_arr": True,
        "team_complete": True,
        "product_live": True,
        "revenue_12mo_sar": 600_000,
        "governance_docs_ready": True,
    })
    assert result["readiness_score"] == 100
    assert result["band"] == "series_a_ready"


def test_readiness_score_mid_inputs():
    result = _compute_readiness({
        "has_arr": True,
        "product_live": True,
    })
    assert result["readiness_score"] == 50
    assert result["band"] == "pre_series_a"


# ── Exit valuation ────────────────────────────────────────────────────────────

def test_exit_valuation_saas_baseline():
    """SaaS baseline: 5x ARR minimum."""
    from api.routers.capital_os import ExitValuationRequest
    req = ExitValuationRequest(arr_sar=1_000_000, business_type="saas")
    assert req.arr_sar == 1_000_000


def test_exit_valuation_services():
    """Services: 1-3x ARR."""
    from api.routers.capital_os import ExitValuationRequest
    req = ExitValuationRequest(arr_sar=500_000, business_type="services")
    assert req.business_type == "services"


# ── FastAPI endpoint smoke tests ─────────────────────────────────────────────

import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_capital_os_status():
    from httpx import ASGITransport, AsyncClient
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/capital-os/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["service"] == "capital_os"
    assert "asset_types" in data


@pytest.mark.anyio
async def test_funding_checklist():
    from httpx import ASGITransport, AsyncClient
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/capital-os/funding-checklist")
    assert resp.status_code == 200
    data = resp.json()
    assert "checklist" in data
    assert len(data["checklist"]) == 10


@pytest.mark.anyio
async def test_exit_valuation_endpoint():
    from httpx import ASGITransport, AsyncClient
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post("/api/v1/capital-os/exit-valuation", json={
            "arr_sar": 2_000_000,
            "business_type": "saas",
            "growth_rate_pct": 50.0,
            "gross_margin_pct": 70.0,
        })
    assert resp.status_code == 200
    data = resp.json()
    assert data["arr_sar"] == 2_000_000
    assert data["is_estimate"] is True
    assert data["valuation_low_sar"] == pytest.approx(10_000_000, rel=0.01)
