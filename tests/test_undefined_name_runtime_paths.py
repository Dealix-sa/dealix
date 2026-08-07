"""Regression coverage for runtime paths previously hidden by the F821 ignore."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_mounted_discovery_and_workflow_endpoints_execute(monkeypatch):
    from api.main import app

    for key in ("GOOGLE_SEARCH_API_KEY", "GOOGLE_SEARCH_CX", "TAVILY_API_KEY"):
        monkeypatch.delenv(key, raising=False)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        discovery = await client.post(
            "/api/v1/leads/discover/web",
            json={"query": "Saudi B2B software"},
        )
        steps = await client.get(
            "/api/v1/workflow-os-v10/service-session/steps",
        )
        execution = await client.post(
            "/api/v1/workflow-os-v10/service-session/execute-step",
            json={
                "step": "day_1_kickoff_diagnostic",
                "customer_id": "cust_test",
                "lead_id": "lead_test",
            },
        )

    assert discovery.status_code == 200, discovery.text
    assert discovery.json()["provider"] == "static_fallback"
    assert steps.status_code == 200, steps.text
    assert len(steps.json()["steps"]) == 7
    assert execution.status_code == 200, execution.text
    assert execution.json()["ok"] is True


@pytest.mark.asyncio
async def test_gulf_validation_clients_reach_their_http_adapter(monkeypatch):
    from integrations import bahrain, kuwait, oman

    calls: list[str] = []

    class _Response:
        is_error = False
        status_code = 200

        @staticmethod
        def json():
            return {"record": {"isValid": True, "status": "active"}}

    class _Client:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, traceback):
            return False

        async def get(self, url, **kwargs):
            calls.append(url)
            return _Response()

    for module in (bahrain, kuwait, oman):
        monkeypatch.setattr(module.httpx, "AsyncClient", _Client)

    results = [
        await bahrain.BahrainLayer(api_key="test").validate_cr("BH-1"),
        await kuwait.KuwaitLayer(api_key="test").validate_license("KW-1"),
        await oman.OmanLayer(api_key="test").validate_cr("OM-1"),
    ]

    assert all(result.is_valid for result in results)
    assert len(calls) == 3
