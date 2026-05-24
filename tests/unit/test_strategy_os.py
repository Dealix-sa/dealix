"""Unit tests for the Strategy OS + Competitive Moat router (Wave 17.0)."""
from __future__ import annotations

import os

os.environ.setdefault("APP_ENV", "test")

import pytest


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


# ── Helpers ────────────────────────────────────────────────────────────────────


def _make_client():
    from httpx import ASGITransport, AsyncClient
    from api.main import create_app

    app = create_app()
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


# ── Tests ──────────────────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ai_readiness_strong() -> None:
    """All axes at 0.9 should produce a readiness_score above 0.8."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/strategy/ai-readiness",
            json={
                "data": 0.9,
                "process": 0.9,
                "governance": 0.9,
                "people": 0.9,
                "tech": 0.9,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["readiness_score"] > 0.8
    assert data["is_estimate"] is True


@pytest.mark.anyio
async def test_ai_readiness_weak_data() -> None:
    """Weak data axis should steer recommendation toward intelligence-type service."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/strategy/ai-readiness",
            json={
                "data": 0.2,
                "process": 0.8,
                "governance": 0.8,
                "people": 0.8,
                "tech": 0.8,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    rec: str = data["recommended_next_service"]
    assert "intelligence" in rec.lower()
    assert data["is_estimate"] is True


@pytest.mark.anyio
async def test_rank_use_cases_sorted() -> None:
    """Ranked use cases must be returned in descending score order."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/strategy/rank-use-cases",
            json={
                "use_cases": [
                    {
                        "name": "low",
                        "revenue_impact": 0.1,
                        "time_save": 0.1,
                        "data_readiness": 0.1,
                        "ease": 0.1,
                        "low_risk": 0.1,
                    },
                    {
                        "name": "high",
                        "revenue_impact": 0.9,
                        "time_save": 0.9,
                        "data_readiness": 0.9,
                        "ease": 0.9,
                        "low_risk": 0.9,
                    },
                    {
                        "name": "mid",
                        "revenue_impact": 0.5,
                        "time_save": 0.5,
                        "data_readiness": 0.5,
                        "ease": 0.5,
                        "low_risk": 0.5,
                    },
                ]
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    ranked = data["ranked"]
    assert len(ranked) == 3
    scores = [item[1] for item in ranked]
    assert scores == sorted(scores, reverse=True)
    assert ranked[0][0] == "high"
    assert "roadmap" in data
    assert data["is_estimate"] is True


@pytest.mark.anyio
async def test_rank_use_cases_empty() -> None:
    """Empty use_cases list must return HTTP 400."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/strategy/rank-use-cases",
            json={"use_cases": []},
        )
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_moat_score_strong() -> None:
    """All dimensions at 90 should produce a strong or emerging tier."""
    async with _make_client() as client:
        resp = await client.post(
            "/api/v1/strategy/moat-score",
            json={
                "governance_depth": 90,
                "proof_strength": 90,
                "product_reuse": 90,
                "saudi_arabic_differentiation": 90,
                "capital_assets_created": 90,
                "partner_academy_distribution": 90,
                "market_language_adoption": 90,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["tier"] in ("strong", "emerging")
    assert data["weighted_score"] > 0
    assert data["is_estimate"] is False


@pytest.mark.anyio
async def test_moat_progress_returns_stages() -> None:
    """GET /moat-progress must return a proof_stages list with the expected stages."""
    async with _make_client() as client:
        resp = await client.get("/api/v1/strategy/moat-progress")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["proof_stages"], list)
    assert len(data["proof_stages"]) > 0
    assert "client_expansion" in data["proof_stages"]
    assert isinstance(data["governance_stages"], list)
    assert data["is_estimate"] is False
