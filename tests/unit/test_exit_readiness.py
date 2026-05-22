"""Unit tests for the Exit Readiness OS router (Wave 17)."""
from __future__ import annotations

import os

os.environ.setdefault("APP_ENV", "test")

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.routers.exit_readiness import router as exit_readiness_router


# ── Fixture: standalone app ───────────────────────────────────────────────────


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def app() -> FastAPI:
    _app = FastAPI()
    _app.include_router(exit_readiness_router)
    return _app


# ── 1. All True → gate passes ─────────────────────────────────────────────────


@pytest.mark.anyio
async def test_venture_gate_all_true(app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/exit-readiness/venture-gate",
            json={
                "paid_clients_5plus": True,
                "retainers_2plus": True,
                "repeatable_delivery": True,
                "product_module_clear": True,
                "playbook_maturity_80plus": True,
                "owner_exists": True,
                "healthy_margin": True,
                "proof_library_exists": True,
                "core_os_dependency_clear": True,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["gate_passes"] is True
    assert data["failed_gates"] == []
    assert data["is_estimate"] is False


# ── 2. All False → gate fails with 9 failed items ────────────────────────────


@pytest.mark.anyio
async def test_venture_gate_all_false(app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/exit-readiness/venture-gate",
            json={
                "paid_clients_5plus": False,
                "retainers_2plus": False,
                "repeatable_delivery": False,
                "product_module_clear": False,
                "playbook_maturity_80plus": False,
                "owner_exists": False,
                "healthy_margin": False,
                "proof_library_exists": False,
                "core_os_dependency_clear": False,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["gate_passes"] is False
    assert len(data["failed_gates"]) == 9
    assert data["is_estimate"] is False


# ── 3. GET /operating-chain returns non-empty list ────────────────────────────


@pytest.mark.anyio
async def test_operating_chain_returns_list(app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/exit-readiness/operating-chain")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["chain"], list)
    assert len(data["chain"]) > 0
    assert data["length"] == len(data["chain"])
    assert data["is_estimate"] is False
    # Known first step in the chain
    assert "signal" in data["chain"]


# ── 4. No completed steps → completion_pct = 0.0 ─────────────────────────────


@pytest.mark.anyio
async def test_chain_progress_empty(app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/exit-readiness/chain-progress",
            json={"completed_steps": []},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["completion_pct"] == 0.0
    assert data["completed"] == 0
    assert data["total_steps"] > 0
    assert data["is_estimate"] is False
    # Every step should be marked incomplete
    for entry in data["chain_status"]:
        assert entry["completed"] is False


# ── 5. GET /exit-readiness-summary returns readiness_dimensions ───────────────


@pytest.mark.anyio
async def test_exit_readiness_summary(app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/exit-readiness/exit-readiness-summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["module"] == "exit_readiness_os"
    assert "readiness_dimensions" in data
    assert isinstance(data["readiness_dimensions"], list)
    assert len(data["readiness_dimensions"]) > 0
    dimensions = [d["dimension"] for d in data["readiness_dimensions"]]
    assert "Venture Gate" in dimensions
    assert "Operating Chain" in dimensions
    assert data["is_estimate"] is False
