"""Governed social-content drafts — draft-and-queue only, never published.

The social/draft endpoint must produce approval-gated drafts and queue
them in the Approval Command Center. There is no auto-publish path.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store


@pytest.mark.asyncio
async def test_social_draft_queues_governed_posts(async_client):
    get_default_approval_store().clear()

    r = await async_client.post(
        "/api/v1/automation/social/draft",
        json={"count": 5, "sectors": ["real_estate", "logistics"]},
    )
    assert r.status_code == 200
    data = r.json()

    assert data["status"] == "ok"
    assert data["drafted"] == 5
    # Doctrine: every social post is a draft, never an autonomous publish.
    assert data["approval_mode"] == "draft_only"
    assert len(data["approvals"]) == 5
    for item in data["approvals"]:
        assert item["approval_id"].startswith("apr_")
        assert item["suggested_publish_date"] is not None


@pytest.mark.asyncio
async def test_social_drafts_appear_in_approval_queue(async_client):
    get_default_approval_store().clear()

    await async_client.post("/api/v1/automation/social/draft", json={"count": 3})

    pending = await async_client.get("/api/v1/approvals/pending")
    assert pending.status_code == 200
    rows = pending.json()["approvals"]
    social = [r for r in rows if r["action_type"] == "social_post"]
    assert len(social) == 3
    for row in social:
        # Never auto-published: draft_only mode, pending status.
        assert row["action_mode"] == "draft_only"
        assert row["status"] == "pending"
        assert row["summary_ar"]


@pytest.mark.asyncio
async def test_social_draft_count_is_bounded(async_client):
    get_default_approval_store().clear()
    r = await async_client.post("/api/v1/automation/social/draft", json={"count": 999})
    assert r.status_code == 200
    assert r.json()["drafted"] == 30  # capped
