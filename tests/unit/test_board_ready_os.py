"""Unit tests for the Board Ready OS router (Wave 17.0)."""

from __future__ import annotations

import os

os.environ.setdefault("APP_ENV", "test")

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_dashboard_metrics_returns_list() -> None:
    """GET /dashboard-metrics returns exactly 12 metric names."""
    from api.main import create_app

    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/board-ready/dashboard-metrics")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["metrics"], list)
    assert data["count"] == 12
    assert len(data["metrics"]) == 12
    assert data["is_estimate"] is False


@pytest.mark.anyio
async def test_dashboard_coverage_zero() -> None:
    """Empty metrics_reported yields coverage_score=0."""
    from api.main import create_app

    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/board-ready/dashboard-coverage",
            json={"metrics_reported": []},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["coverage_score"] == 0
    assert data["is_estimate"] is True
    assert len(data["missing"]) == 12


@pytest.mark.anyio
async def test_dashboard_coverage_full() -> None:
    """Reporting all 12 metrics yields coverage_score=100."""
    from api.main import create_app
    from auto_client_acquisition.board_ready_os import BOARD_DASHBOARD_METRICS

    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/board-ready/dashboard-coverage",
            json={"metrics_reported": list(BOARD_DASHBOARD_METRICS)},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["coverage_score"] == 100
    assert data["missing"] == []


@pytest.mark.anyio
async def test_unit_economics_gate_fails_low_margin() -> None:
    """gross_margin_pct=20 with proof ok and no scope creep → scale_ok=False."""
    from api.main import create_app

    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/board-ready/unit-economics-gate",
            json={
                "gross_margin_pct": 20.0,
                "proof_strength_ok": True,
                "scope_creep_high": False,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["scale_ok"] is False
    assert "gross_margin_too_low_for_scale" in data["errors"]
    assert data["is_estimate"] is False


@pytest.mark.anyio
async def test_unit_economics_gate_passes() -> None:
    """gross_margin_pct=50 with proof ok and no scope creep → scale_ok=True."""
    from api.main import create_app

    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/board-ready/unit-economics-gate",
            json={
                "gross_margin_pct": 50.0,
                "proof_strength_ok": True,
                "scope_creep_high": False,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["scale_ok"] is True
    assert data["errors"] == []


@pytest.mark.anyio
async def test_memo_skeleton_returns_markdown() -> None:
    """GET /memo-skeleton returns a non-empty skeleton_markdown string."""
    from api.main import create_app

    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/board-ready/memo-skeleton")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["skeleton_markdown"], str)
    assert len(data["skeleton_markdown"]) > 0
    assert data["draft_only"] is True
    assert data["is_estimate"] is False
