"""Founder daily brief — the morning command-center call.

Read-only aggregate of the approval queue, the revenue pipeline, and
the next action. Must be safe to call from a phone and never mutate.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store


@pytest.mark.asyncio
async def test_daily_brief_shape(async_client):
    get_default_approval_store().clear()
    r = await async_client.get("/api/v1/founder/daily-brief")
    assert r.status_code == 200
    data = r.json()
    assert data["schema_version"] == 1
    assert {"approvals", "pipeline", "next_action", "headline_ar", "headline_en"} <= data.keys()
    assert data["guardrails"]["read_only"] is True
    assert {"pending", "overdue", "first_3"} <= data["approvals"].keys()


@pytest.mark.asyncio
async def test_daily_brief_counts_pending_approvals(async_client):
    get_default_approval_store().clear()
    await async_client.post("/api/v1/automation/social/draft", json={"count": 4})

    r = await async_client.get("/api/v1/founder/daily-brief")
    data = r.json()
    assert data["approvals"]["pending"] == 4
    assert "4" in data["headline_en"]


@pytest.mark.asyncio
async def test_daily_brief_is_read_only(async_client):
    """Calling the brief must not change the pending count."""
    get_default_approval_store().clear()
    await async_client.post("/api/v1/automation/social/draft", json={"count": 3})

    first = (await async_client.get("/api/v1/founder/daily-brief")).json()
    second = (await async_client.get("/api/v1/founder/daily-brief")).json()
    assert first["approvals"]["pending"] == second["approvals"]["pending"] == 3
