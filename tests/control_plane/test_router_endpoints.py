"""HTTP surface for the Control Plane router (`/api/v1/control-plane/...`).

Verifies every read-only endpoint returns the documented shape so the
router code path stays covered.
"""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_control_plane_health(async_client) -> None:
    res = await async_client.get("/api/v1/control-plane/health")
    assert res.status_code == 200
    body = res.json()
    assert body["system"] == "26_control_plane"
    assert body["status"] == "ok"


@pytest.mark.asyncio
async def test_control_plane_snapshot_contains_all_layers(async_client) -> None:
    res = await async_client.get("/api/v1/control-plane/snapshot")
    assert res.status_code == 200
    body = res.json()
    for key in (
        "sovereignty_order",
        "security_mode",
        "identities",
        "tenants",
        "money",
        "intelligence_graph",
        "scale_kill",
        "public_api",
        "marketplace",
        "health",
        "commercial_packaging",
        "memory_stats",
        "open_incidents",
        "pending_approvals",
    ):
        assert key in body


@pytest.mark.asyncio
async def test_sovereignty_order_endpoint(async_client) -> None:
    res = await async_client.get("/api/v1/control-plane/sovereignty")
    assert res.status_code == 200
    body = res.json()
    assert body["sovereignty_order"][0] == "sami"
    assert body["sovereignty_order"][-1] == "tool"


@pytest.mark.asyncio
async def test_security_mode_endpoint(async_client) -> None:
    res = await async_client.get("/api/v1/control-plane/security-mode")
    assert res.status_code == 200
    assert res.json()["security_mode"] in {
        "draft_only",
        "approval_gated",
        "low_risk_autonomy",
        "enterprise_controlled",
        "sovereign_lockdown",
    }


@pytest.mark.asyncio
async def test_commercial_packaging_endpoint(async_client) -> None:
    res = await async_client.get("/api/v1/control-plane/commercial-packaging")
    assert res.status_code == 200
    body = res.json()
    assert "Revenue Hunter Pilot" in body["entry"]
    assert "AI Control Plane" in body["enterprise"]


@pytest.mark.asyncio
async def test_health_flags_endpoint(async_client) -> None:
    res = await async_client.get("/api/v1/control-plane/health-flags")
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body["flags"], list)
    assert "agent_runs" in body["metrics"]


@pytest.mark.asyncio
async def test_scale_kill_board_endpoint(async_client) -> None:
    res = await async_client.get("/api/v1/control-plane/scale-kill-board")
    assert res.status_code == 200
    body = res.json()
    assert {"scale", "kill", "pause"}.issubset(body.keys())


@pytest.mark.asyncio
async def test_money_snapshot_endpoint(async_client) -> None:
    res = await async_client.get("/api/v1/control-plane/money-snapshot")
    assert res.status_code == 200
    body = res.json()
    assert "best_next_action" in body


@pytest.mark.asyncio
async def test_intelligence_graph_summary_endpoint(async_client) -> None:
    res = await async_client.get("/api/v1/control-plane/intelligence-graph/summary")
    assert res.status_code == 200
    body = res.json()
    assert "total_nodes" in body
    assert "total_edges" in body


@pytest.mark.asyncio
async def test_public_api_and_marketplace_readiness_endpoints(async_client) -> None:
    api = await async_client.get("/api/v1/control-plane/public-api-readiness")
    assert api.status_code == 200
    assert api.json()["launched"] is False

    market = await async_client.get("/api/v1/control-plane/marketplace-readiness")
    assert market.status_code == 200
    assert market.json()["launched"] is False
