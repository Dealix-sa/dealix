"""Unit tests for the Retainer Conversion Engine router (Wave 17.0)."""
from __future__ import annotations

import os

import pytest

os.environ.setdefault("APP_ENV", "test")

from httpx import ASGITransport, AsyncClient


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


# ─── helper ───────────────────────────────────────────────────────────────────


def _make_app():
    from api.main import create_app
    return create_app()


# ─── Test 1: eligible customer with proof ─────────────────────────────────────


@pytest.mark.anyio
async def test_eligible_with_proof() -> None:
    """3 months, 1 proof event, NPS 8, healthy engagement → eligible + strong_signal."""
    app = _make_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/retainer-conversion/check-eligibility",
            json={
                "customer_id": "cust_001",
                "current_tier": "sprint_499",
                "months_as_customer": 3,
                "proof_events_completed": 1,
                "monthly_engagement_drop_pct": 0.1,
                "nps": 8,
                "pipeline_added_drop_pct": 0.1,
                "churn_band": "safe",
                "arr_so_far_sar": 1500.0,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["eligible"] is True
    assert data["signal"] == "strong_signal"
    assert data["proof_gate_passed"] is True
    assert data["is_estimate"] is True
    assert data["recommended_retainer_sar"] == 2999


# ─── Test 2: blocked — no proof events ────────────────────────────────────────


@pytest.mark.anyio
async def test_blocked_no_proof() -> None:
    """proof_events_completed=0 → eligible=False, signal='blocked'."""
    app = _make_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/retainer-conversion/check-eligibility",
            json={
                "customer_id": "cust_002",
                "current_tier": "sprint_499",
                "months_as_customer": 6,
                "proof_events_completed": 0,
                "monthly_engagement_drop_pct": 0.0,
                "nps": 9,
                "churn_band": "safe",
                "arr_so_far_sar": 5000.0,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["eligible"] is False
    assert data["signal"] == "blocked"
    assert data["proof_gate_passed"] is False
    assert "no_proof_events" in data["reason"]
    assert data["recommended_retainer_sar"] is None
    assert data["is_estimate"] is True


# ─── Test 3: blocked — critical churn band ────────────────────────────────────


@pytest.mark.anyio
async def test_blocked_critical_churn() -> None:
    """churn_band='critical' → eligible=False even with proof events."""
    app = _make_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/retainer-conversion/check-eligibility",
            json={
                "customer_id": "cust_003",
                "current_tier": "sprint_499",
                "months_as_customer": 4,
                "proof_events_completed": 2,
                "monthly_engagement_drop_pct": 0.05,
                "nps": 8,
                "churn_band": "critical",
                "arr_so_far_sar": 2000.0,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["eligible"] is False
    assert data["churn_band"] == "critical"
    assert data["is_estimate"] is True


# ─── Test 4: batch sorted strong_signal first ─────────────────────────────────


@pytest.mark.anyio
async def test_batch_sorted_strong_first() -> None:
    """Batch of 3 customers with different signals — strong_signal must come first."""
    app = _make_app()
    customers = [
        # customer B: no proof → blocked
        {
            "customer_id": "cust_batch_b",
            "current_tier": "sprint_499",
            "months_as_customer": 5,
            "proof_events_completed": 0,
            "monthly_engagement_drop_pct": 0.0,
            "churn_band": "safe",
            "arr_so_far_sar": 0.0,
        },
        # customer C: 2 months, proof, no NPS → potential
        {
            "customer_id": "cust_batch_c",
            "current_tier": "sprint_499",
            "months_as_customer": 2,
            "proof_events_completed": 1,
            "monthly_engagement_drop_pct": 0.1,
            "pipeline_added_drop_pct": 0.5,
            "churn_band": "safe",
            "arr_so_far_sar": 500.0,
        },
        # customer A: 3 months, proof, NPS 9 → strong_signal
        {
            "customer_id": "cust_batch_a",
            "current_tier": "sprint_499",
            "months_as_customer": 3,
            "proof_events_completed": 1,
            "monthly_engagement_drop_pct": 0.05,
            "nps": 9,
            "pipeline_added_drop_pct": 0.1,
            "churn_band": "safe",
            "arr_so_far_sar": 1500.0,
        },
    ]
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/retainer-conversion/batch-check",
            json={"customers": customers},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    assert data["strong_signals"] == 1
    assert data["potential"] >= 1
    assert data["blocked_no_proof"] == 1
    assert data["is_estimate"] is True

    results = data["results"]
    assert results[0]["signal"] == "strong_signal"
    # blocked should come last
    signals = [r["signal"] for r in results]
    assert signals.index("strong_signal") < signals.index("blocked")


# ─── Test 5: draft outreach — eligible customer ───────────────────────────────


@pytest.mark.anyio
async def test_draft_outreach_eligible() -> None:
    """Eligible customer gets non-empty bilingual draft; draft_only=True always."""
    app = _make_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/retainer-conversion/draft-outreach",
            json={
                "customer_id": "cust_004",
                "current_tier": "sprint_499",
                "months_as_customer": 3,
                "proof_events_completed": 1,
                "monthly_engagement_drop_pct": 0.1,
                "nps": 7,
                "churn_band": "safe",
                "arr_so_far_sar": 1000.0,
                "founder_name": "أحمد",
                "retainer_tier_sar": 2999,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["eligible"] is True
    assert data["draft_ar"] is not None and len(data["draft_ar"]) > 10
    assert data["draft_en"] is not None and len(data["draft_en"]) > 10
    assert data["draft_only"] is True
    assert data["approval_required"] is True
    assert data["is_estimate"] is True
    assert data["retainer_sar"] == 2999
    # Governance label must appear in both drafts
    assert "draft_only=True" in data["draft_ar"]
    assert "draft_only=True" in data["draft_en"]


# ─── Test 6: draft outreach — not eligible (no proof) ────────────────────────


@pytest.mark.anyio
async def test_draft_outreach_not_eligible() -> None:
    """Customer with no proof events → draft is None."""
    app = _make_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/retainer-conversion/draft-outreach",
            json={
                "customer_id": "cust_005",
                "current_tier": "sprint_499",
                "months_as_customer": 4,
                "proof_events_completed": 0,
                "monthly_engagement_drop_pct": 0.0,
                "churn_band": "safe",
                "arr_so_far_sar": 0.0,
                "founder_name": "المؤسس",
                "retainer_tier_sar": 2999,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["eligible"] is False
    assert data["draft_ar"] is None
    assert data["draft_en"] is None
    assert data["draft_only"] is True
    assert data["approval_required"] is True


# ─── Test 7: log-conversion requires founder approval ────────────────────────


@pytest.mark.anyio
async def test_log_conversion_requires_approval() -> None:
    """founder_approved=False must return HTTP 422."""
    app = _make_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/v1/retainer-conversion/log-conversion",
            json={
                "customer_id": "cust_006",
                "from_tier": "sprint_499",
                "to_tier": "managed_growth_ops",
                "retainer_sar_per_month": 2999,
                "proof_events_count": 1,
                "founder_approved": False,
                "notes": "attempted without approval",
            },
        )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert "no_auto_execute_offer" in detail
    assert "founder_approved" in detail


# ─── Test 8: conversion-playbook returns structured data ─────────────────────


@pytest.mark.anyio
async def test_conversion_playbook() -> None:
    """GET /conversion-playbook returns playbook dict with retainer_tiers list."""
    app = _make_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/v1/retainer-conversion/conversion-playbook")
    assert resp.status_code == 200
    data = resp.json()
    assert "playbook" in data
    playbook = data["playbook"]
    assert "retainer_tiers" in playbook
    tiers = playbook["retainer_tiers"]
    assert isinstance(tiers, list)
    assert len(tiers) == 3
    tier_sars = [t["sar_per_month"] for t in tiers]
    assert 2999 in tier_sars
    assert 3999 in tier_sars
    assert 4999 in tier_sars
    assert "trigger_conditions" in playbook
    assert "governance" in playbook
    assert "no_upsell_without_proof" in playbook["governance"]
    assert data["is_estimate"] is False
