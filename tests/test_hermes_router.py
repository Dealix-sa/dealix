"""HTTP surface smoke tests for the Hermes router.

These tests mount the Hermes router on a minimal FastAPI app so the full
project dependency stack is not required to exercise the surface.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.routers.hermes import router as hermes_router


@pytest_asyncio.fixture
async def hermes_client():
    app = FastAPI()
    app.include_router(hermes_router)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
def _isolate_global_state():
    """Reset every Hermes singleton between router tests."""
    import dealix.hermes.core.assets as a_mod
    import dealix.hermes.core.decisions as d_mod
    import dealix.hermes.core.executions as e_mod
    import dealix.hermes.core.opportunities as o_mod
    import dealix.hermes.core.outcomes as out_mod
    import dealix.hermes.core.signals as s_mod
    import dealix.hermes.orchestrator as orch_mod
    import dealix.hermes.sovereignty as sov_mod
    import dealix.hermes.trust.approvals as appr_mod
    import dealix.hermes.trust.audit as aud_mod
    import dealix.hermes.trust.incident_response as inc_mod

    for mod in (s_mod, o_mod, d_mod, e_mod, out_mod, a_mod, orch_mod, sov_mod, appr_mod, aud_mod, inc_mod):
        for attr in ("_default_store", "_default_orchestrator", "_default_layer", "_default_center", "_default_log"):
            if hasattr(mod, attr):
                setattr(mod, attr, None)
    yield


@pytest.mark.asyncio
async def test_status_endpoint(hermes_client):
    resp = await hermes_client.get("/api/v1/hermes/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["kernel"] == "Hermes Universal Kernel"
    assert "S5_NEVER_AUTONOMOUS" in body["sovereignty_levels"]


@pytest.mark.asyncio
async def test_signal_ingest_and_pipeline(hermes_client):
    resp = await hermes_client.post(
        "/api/v1/hermes/signals",
        json={
            "source": "sami",
            "signal_type": "customer",
            "title": "Lead",
            "content": "An agency wants AI service.",
            "confidence": 0.8,
        },
    )
    assert resp.status_code == 200
    sig = resp.json()
    assert sig["id"].startswith("sig_")

    resp = await hermes_client.post(
        f"/api/v1/hermes/opportunities/from-signal/{sig['id']}",
        json={"estimated_value_sar": 10_000},
    )
    assert resp.status_code == 200
    opp = resp.json()
    assert opp["score"] > 0

    resp = await hermes_client.post(
        f"/api/v1/hermes/decisions/from-opportunity/{opp['id']}",
        json={"recommendation": "Proceed"},
    )
    assert resp.status_code == 200
    dec = resp.json()
    assert dec["opportunity_id"] == opp["id"]


@pytest.mark.asyncio
async def test_offers_catalog_endpoint(hermes_client):
    resp = await hermes_client.get("/api/v1/hermes/products/offers")
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] >= 3
    for o in body["items"]:
        assert o["price_range_sar"]
        assert o["outcome_metric"]


@pytest.mark.asyncio
async def test_mcp_review_endpoint_blocks_broad_scope(hermes_client):
    resp = await hermes_client.post(
        "/api/v1/hermes/trust/mcp/review",
        json={
            "server_name": "github",
            "owner": "Sami",
            "data_scope": "*",
            "tools": ["read"],
            "s4_approved": False,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["approved"] is False


@pytest.mark.asyncio
async def test_sovereignty_classify_endpoint(hermes_client):
    resp = await hermes_client.get(
        "/api/v1/hermes/sovereignty/classify",
        params={"action_type": "money_transfer"},
    )
    assert resp.status_code == 200
    assert resp.json()["sovereignty_level"] == "S5_NEVER_AUTONOMOUS"


@pytest.mark.asyncio
async def test_run_pipeline_shortcut(hermes_client):
    resp = await hermes_client.post(
        "/api/v1/hermes/pipeline/run",
        json={
            "source": "customer",
            "signal_type": "customer",
            "title": "Hot lead",
            "content": "Wants pilot.",
            "estimated_value_sar": 8_000,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["signal"] is not None
    assert body["opportunity"] is not None
    assert body["decision"] is not None
    assert body["execution"] is not None
