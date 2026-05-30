"""
ASGI smoke tests for the Commercial Engine router.
اختبارات دخانية لراوتر ماكينة التجارة.

Covers: api/routers/commercial.py — validation, happy-path (no LLM), error cases.
"""
from __future__ import annotations

import pytest

# Uses the async_client fixture from tests/conftest.py (no local fixture needed).


# ── diagnostic ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_diagnostic_generate_missing_company(async_client):
    r = await async_client.post("/api/v1/commercial/diagnostic/generate", json={})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_diagnostic_list_empty(async_client):
    r = await async_client.get("/api/v1/commercial/diagnostic/list")
    assert r.status_code == 200
    body = r.json()
    assert "diagnostics" in body
    assert "count" in body


# ── warm intro ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_warm_intro_missing_company(async_client):
    r = await async_client.post("/api/v1/commercial/warm-intro/draft", json={})
    assert r.status_code == 422


# ── pilot ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_pilot_start_missing_company(async_client):
    r = await async_client.post("/api/v1/commercial/pilot/start", json={})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_pilot_start_no_payment(async_client):
    """payment_confirmed=False must be rejected (NO_LIVE_CHARGE gate)."""
    r = await async_client.post(
        "/api/v1/commercial/pilot/start",
        json={
            "company_name": "شركة اختبار",
            "payment_confirmed": False,
            "payment_ref": "",
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_pilot_start_missing_payment_ref(async_client):
    """payment_ref missing must be rejected."""
    r = await async_client.post(
        "/api/v1/commercial/pilot/start",
        json={
            "company_name": "شركة اختبار",
            "payment_confirmed": True,
            "payment_ref": "",
        },
    )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_pilot_start_valid(async_client):
    """Valid payload with payment_confirmed=True should start a pilot."""
    r = await async_client.post(
        "/api/v1/commercial/pilot/start",
        json={
            "company_name": "شركة الاختبار للتسويق",
            "sector": "marketing_agency",
            "pain_points": "بطء الاستجابة للعملاء",
            "contact_name": "أحمد",
            "payment_confirmed": True,
            "payment_ref": "PAY-TEST-001",
            "amount_sar": 499.0,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "started"
    assert "pilot_id" in body
    assert body["days_total"] == 7
    assert "plan_markdown_ar" in body


@pytest.mark.asyncio
async def test_pilot_brief_invalid_id_format(async_client):
    """pilot_id with invalid characters (not matching ^[a-zA-Z0-9_-]+$) → 422."""
    r = await async_client.get("/api/v1/commercial/pilot/invalid%2Fid/brief")
    # FastAPI URL encoding means this won't match the route — 404 is expected
    assert r.status_code in (404, 422)


@pytest.mark.asyncio
async def test_pilot_brief_not_found(async_client):
    r = await async_client.get("/api/v1/commercial/pilot/nonexistent-pilot-id/brief")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_pilot_plan_not_found(async_client):
    r = await async_client.get("/api/v1/commercial/pilot/nonexistent-pilot-id/plan")
    assert r.status_code == 404


# ── proof ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_proof_build_missing_fields(async_client):
    r = await async_client.post("/api/v1/commercial/proof/build", json={})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_proof_build_valid(async_client):
    """Minimal valid proof build — no LLM needed."""
    import uuid
    r = await async_client.post(
        "/api/v1/commercial/proof/build",
        json={
            "pilot_id": str(uuid.uuid4()),
            "account_id": str(uuid.uuid4()),
            "company_name": "شركة اختبار",
            "sector": "consulting",
            "pain_point": "ضعف المبيعات",
            "messages_drafted": 5,
            "messages_approved": 4,
            "messages_sent": 4,
            "replies_received": 2,
            "meetings_booked": 1,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "built"
    assert "pack_id" in body
    assert "evidence_level" in body


# ── upsell ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_upsell_missing_company(async_client):
    r = await async_client.post("/api/v1/commercial/upsell/evaluate", json={})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_upsell_gated_no_pilots(async_client):
    """Zero pilots → all offers should be gated."""
    r = await async_client.post(
        "/api/v1/commercial/upsell/evaluate",
        json={
            "company_name": "شركة اختبار",
            "sector": "other",
            "pain_point": "",
            "pilot_count": 0,
            "proof_event_count": 0,
            "evidence_level": 0,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["eligible_offers"] == []
    assert len(body["gated_offers"]) > 0
    assert "constitutional_note" in body


@pytest.mark.asyncio
async def test_upsell_eligible_after_pilot(async_client):
    """After 1 pilot + 1 proof event, at least one offer becomes eligible."""
    r = await async_client.post(
        "/api/v1/commercial/upsell/evaluate",
        json={
            "company_name": "شركة النجاح",
            "sector": "marketing_agency",
            "pain_point": "تأخر الرد",
            "pilot_count": 1,
            "proof_event_count": 1,
            "evidence_level": 1,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert len(body["eligible_offers"]) > 0
    # All offers must have constitutional pending_approval note
    for offer in body["eligible_offers"]:
        assert offer["status"] == "pending_approval"


# ── daily brief ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_daily_brief(async_client):
    r = await async_client.get("/api/v1/commercial/daily-brief")
    assert r.status_code == 200
    body = r.json()
    assert "date" in body
    assert "diagnostics_total" in body
    assert "pilots_active" in body
    assert "warm_intros_pending" in body
    assert "proof_packs_built" in body
    assert isinstance(body["top_actions"], list)
