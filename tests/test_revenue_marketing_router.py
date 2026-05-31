"""Router tests — admin-key, validation, dashboard, agent draft.

These tests mount the ``revenue_marketing`` router on a minimal FastAPI app to
avoid pulling in the full ``api.main`` import tree (which would require Redis,
Sentry, OpenTelemetry, and similar heavy deps just to instantiate). The
endpoints, admin-key dependency, and validation behaviour are identical.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.routers.revenue_marketing import router as revenue_marketing_router
from dealix.revenue_marketing.store import reset_revenue_marketing_store_for_tests

ADMIN_HEADER = "X-Admin-API-Key"
ADMIN_KEY = "test_admin_revenue_marketing"


@pytest.fixture(autouse=True)
def _fresh_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)
    reset_revenue_marketing_store_for_tests(path=tmp_path / "rm.json")


@pytest_asyncio.fixture
async def rm_client():
    app = FastAPI()
    app.include_router(revenue_marketing_router)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


def _h() -> dict[str, str]:
    return {ADMIN_HEADER: ADMIN_KEY}


@pytest.mark.asyncio
async def test_list_campaigns_requires_admin_key(rm_client) -> None:
    # When no header is supplied at all the require_admin_key dep raises 403.
    res = await rm_client.get("/api/v1/revenue-marketing/campaigns")
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_create_campaign_returns_422_when_missing_fields(rm_client) -> None:
    res = await rm_client.post(
        "/api/v1/revenue-marketing/campaigns",
        json={"campaign_name": "X"},
        headers=_h(),
    )
    assert res.status_code == 422
    body = res.json()
    assert "missing" in str(body)


@pytest.mark.asyncio
async def test_create_campaign_passes_when_complete(rm_client) -> None:
    payload = {
        "campaign_name": "Q1 Hunter Pilot",
        "target_segment": "smb_founders",
        "offer_id": "off_entry_revenue_hunter",
        "channel": "linkedin",
        "message_angle": "money",
        "success_metric": "qualified_leads",
        "scale_kill_rule": "kill_if_under_5_pct",
    }
    res = await rm_client.post(
        "/api/v1/revenue-marketing/campaigns",
        json=payload,
        headers=_h(),
    )
    assert res.status_code == 200
    item = res.json()["item"]
    assert item["status"] == "draft"
    assert item["campaign_name"] == "Q1 Hunter Pilot"


@pytest.mark.asyncio
async def test_attribution_400_when_neither_flag_set(rm_client) -> None:
    res = await rm_client.post(
        "/api/v1/revenue-marketing/attribution",
        json={
            "deal_id": "d_x",
            "revenue_sar": 1_000,
            "campaign_id": "c_x",
            "attribution_type": "multi_touch",
            "payment_received": False,
            "signed_agreement": False,
        },
        headers=_h(),
    )
    assert res.status_code == 400
    assert "revenue_not_real_yet" in res.json()["detail"]


@pytest.mark.asyncio
async def test_attribution_200_when_payment_received(rm_client) -> None:
    res = await rm_client.post(
        "/api/v1/revenue-marketing/attribution",
        json={
            "deal_id": "d_paid",
            "revenue_sar": 2_500,
            "campaign_id": "c_paid",
            "attribution_type": "multi_touch",
            "payment_received": True,
            "signed_agreement": False,
        },
        headers=_h(),
    )
    assert res.status_code == 200
    item = res.json()["item"]
    assert item["is_real_revenue"] is True


@pytest.mark.asyncio
async def test_dashboard_returns_expected_keys(rm_client) -> None:
    res = await rm_client.get(
        "/api/v1/revenue-marketing/dashboard",
        headers=_h(),
    )
    assert res.status_code == 200
    body = res.json()
    for key in (
        "top_campaigns_by_revenue",
        "top_channels_by_qualified_leads",
        "top_offers_by_close_rate",
        "best_message_variants",
        "cost_per_lead",
        "cost_per_call",
        "cost_per_won_deal",
        "revenue_attributed_total",
        "assets_influencing_revenue",
        "red_flags",
    ):
        assert key in body


@pytest.mark.asyncio
async def test_agent_propose_returns_draft(rm_client) -> None:
    res = await rm_client.post(
        "/api/v1/revenue-marketing/agents/copywriter/propose",
        json={"payload": {"offer_id": "off_1", "angle": "money"}},
        headers=_h(),
    )
    assert res.status_code == 200
    body = res.json()
    assert body["agent"] == "copywriter"
    assert body["requires_approval"] is True
    assert body["external_send_blocked"] is True


@pytest.mark.asyncio
async def test_agent_propose_unknown_agent_returns_404(rm_client) -> None:
    res = await rm_client.post(
        "/api/v1/revenue-marketing/agents/not_real/propose",
        json={"payload": {}},
        headers=_h(),
    )
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_lead_score_endpoint(rm_client) -> None:
    res = await rm_client.post(
        "/api/v1/revenue-marketing/leads/score",
        json={
            "icp_fit": 1.0,
            "pain": 1.0,
            "ability_to_pay": 1.0,
            "urgency": 1.0,
            "partner_potential": 1.0,
            "trust_fit": 1.0,
        },
        headers=_h(),
    )
    assert res.status_code == 200
    assert res.json()["score"] == pytest.approx(1.0)


@pytest.mark.asyncio
async def test_attribution_by_dimension_invalid(rm_client) -> None:
    res = await rm_client.get(
        "/api/v1/revenue-marketing/attribution/by/bogus",
        headers=_h(),
    )
    assert res.status_code == 400
