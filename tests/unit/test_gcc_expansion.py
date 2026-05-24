"""Unit tests for the GCC Expansion Intelligence router (Wave 16.0)."""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("APP_ENV", "test")

from httpx import ASGITransport, AsyncClient


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


# ── Helper ────────────────────────────────────────────────────────────────────

async def _client():
    from api.main import create_app
    return create_app()


# ── Test 1: market-scan default SA ───────────────────────────────────────────

@pytest.mark.anyio
async def test_market_scan_default_sa() -> None:
    """GET /market-scan returns 200 with is_estimate=True for default SA."""
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/gcc-expansion/market-scan")
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_estimate"] is True
    assert data["country"] == "SA"
    assert "sectors_hot" in data
    assert isinstance(data["sectors_hot"], list)


# ── Test 2: market-scan with explicit country ─────────────────────────────────

@pytest.mark.anyio
async def test_market_scan_explicit_country() -> None:
    """GET /market-scan?country=AE returns 200 for UAE."""
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/gcc-expansion/market-scan?country=AE")
    assert resp.status_code == 200
    data = resp.json()
    assert data["country"] == "AE"
    assert data["is_estimate"] is True


# ── Test 3: opportunity-feed returns list ─────────────────────────────────────

@pytest.mark.anyio
async def test_opportunity_feed_returns_list() -> None:
    """GET /opportunity-feed returns a list (may be empty in zero-input mode)."""
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/gcc-expansion/opportunity-feed")
    assert resp.status_code == 200
    data = resp.json()
    assert "opportunities" in data
    assert isinstance(data["opportunities"], list)
    assert data["is_estimate"] is True


# ── Test 4: hot-cities returns cities key ────────────────────────────────────

@pytest.mark.anyio
async def test_hot_cities_returns_cities() -> None:
    """GET /hot-cities returns dict with 'cities' key."""
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/gcc-expansion/hot-cities")
    assert resp.status_code == 200
    data = resp.json()
    assert "cities" in data
    assert isinstance(data["cities"], list)
    assert data["is_estimate"] is True


# ── Test 5: signal-detect hiring ─────────────────────────────────────────────

@pytest.mark.anyio
async def test_signal_detect_hiring() -> None:
    """POST /signal-detect with hiring signal_type returns 200."""
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/gcc-expansion/signal-detect",
            json={
                "signal_type": "hiring",
                "raw_data": {"company": "Acme", "jobs_count": 5},
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["signal_type"] == "hiring"
    assert isinstance(data["detected"], bool)
    assert isinstance(data["confidence"], float)
    assert data["is_estimate"] is True


# ── Test 6: signal-detect invalid type returns 400 ───────────────────────────

@pytest.mark.anyio
async def test_signal_detect_invalid_type() -> None:
    """POST /signal-detect with invalid signal_type returns 400."""
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/gcc-expansion/signal-detect",
            json={"signal_type": "invalid_xyz", "raw_data": {}},
        )
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["error"] == "invalid_signal_type"


# ── Test 7: gcc-overview returns all 6 countries ─────────────────────────────

@pytest.mark.anyio
async def test_gcc_overview_all_countries() -> None:
    """GET /gcc-overview returns exactly 6 country entries."""
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/gcc-expansion/gcc-overview")
    assert resp.status_code == 200
    data = resp.json()
    assert "countries" in data
    assert len(data["countries"]) == 6
    assert data["is_estimate"] is True
    codes = {c["country_code"] for c in data["countries"]}
    assert codes == {"SA", "AE", "KW", "BH", "QA", "OM"}


# ── Test 8: market-scan invalid country returns 400 ──────────────────────────

@pytest.mark.anyio
async def test_market_scan_invalid_country() -> None:
    """GET /market-scan?country=XX returns 400 for unknown country code."""
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/gcc-expansion/market-scan?country=XX")
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["error"] == "invalid_country"


# ── Test 9: sector-pulse detail ───────────────────────────────────────────────

@pytest.mark.anyio
async def test_sector_pulse_detail() -> None:
    """GET /sector-pulse returns pulse detail with is_estimate=True."""
    from api.main import create_app
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get(
            "/api/v1/gcc-expansion/sector-pulse?sector=real_estate&country=SA"
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["sector"] == "real_estate"
    assert data["is_estimate"] is True
