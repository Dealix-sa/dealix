"""The two public lead stores must converge on the lead-inbox.

Inbound via POST /api/v1/public/leads is persisted to the revenue-ops-autopilot
store (store B) AND bridged into ``lead_inbox`` (store A) by the orchestrator,
so the daily lead-prep engine (which only reads store A) sees every inbound
lead. This test locks that bridge.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.mark.asyncio
async def test_public_leads_endpoint_reaches_lead_inbox(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_LEAD_INBOX_PATH", str(tmp_path / "inbox.jsonl"))
    monkeypatch.setenv("DEALIX_REVENUE_AUTOPILOT_STORE", str(tmp_path / "autopilot.json"))

    from auto_client_acquisition import lead_inbox
    from dealix.revenue_ops_autopilot.store import (
        clear_autopilot_store_singleton_for_tests,
    )

    # Rebuild the cached store singleton against the isolated tmp path.
    clear_autopilot_store_singleton_for_tests()
    try:
        from api.main import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            r = await client.post("/api/v1/public/leads", json={
                "name": "Sara",
                "email": "sara@northstar.sa",
                "company": "NorthStar",
                "industry": "saas",
                "country": "SA",
                "pain": "بطء الرد على الـ leads",
            })
        assert r.status_code == 200

        # The daily engine reads lead_inbox (store A) with status="new".
        leads = lead_inbox.list_leads(status="new")
        assert any(l.get("company") == "NorthStar" for l in leads), (
            "inbound /public/leads did not reach lead_inbox — bridge broken"
        )
    finally:
        clear_autopilot_store_singleton_for_tests()
