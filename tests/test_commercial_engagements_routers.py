"""HTTP smoke tests for commercial engagement sprint routers."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_delivery_catalog_http() -> None:
    r = client.get("/api/v1/commercial/engagements/delivery-catalog")
    assert r.status_code == 200
    body = r.json()
    assert body.get("service_lines")
    assert body["hard_gates"]["draft_approval_first"] is True


def test_lead_intelligence_sprint_http() -> None:
    r = client.post(
        "/api/v1/commercial/engagements/lead-intelligence-sprint",
        json={
            "accounts": [
                {"company_name": "Acme", "sector": "tech", "city": "Riyadh"},
            ],
            "top_n": 10,
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["data_quality"]["row_count"] == 1
    assert body["accounts_ranked"]


def test_support_desk_sprint_http() -> None:
    r = client.post(
        "/api/v1/commercial/engagements/support-desk-sprint",
        json={"messages": ["أريد استرداد المبلغ", "سؤال عن الفاتورة"]},
    )
    assert r.status_code == 200, r.text
    assert len(r.json()["items"]) == 2


def test_quick_win_ops_http() -> None:
    r = client.post(
        "/api/v1/commercial/engagements/quick-win-ops",
        json={
            "weekly_rows": [{"channel": "email", "count": 3}],
            "group_by": "channel",
        },
    )
    assert r.status_code == 200, r.text
    assert "rollup" in r.json()


def test_campaign_intelligence_sprint_http() -> None:
    r = client.post(
        "/api/v1/commercial/engagements/campaign-intelligence-sprint",
        json={
            "offer_title": "Lead Intelligence Sprint",
            "sector": "b2b_services",
            "locale": "ar",
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("angles") and len(body["angles"]) >= 1
