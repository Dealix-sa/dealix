"""
Tests for Revenue Marketing OS — the Hermes Growth surface.

Covers the 11 non-negotiables of the spec:

  - No revenue counts without verification (governance.check_revenue).
  - No claim publishing without trust check (governance.check_claim).
  - Approval-required actions blocked without approval.
  - Lead scoring matches the 0.25/0.20/0.20/0.15/0.10/0.10 weights.
  - Revenue quality scoring matches the 0.25/0.20/0.20/0.15/0.10/-0.10 weights.
  - Attribution rejects unverified revenue.
  - Attribution distributes weight across touches.
  - Campaign created in draft, requires approval.
  - Scale/kill engine emits decisions only — never auto-acts.
  - Funnel ratios stay between 0 and 1.
  - Dashboard read-only aggregates only verified revenue.
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

# ── Helpers ─────────────────────────────────────────────────────────


_ADMIN_KEY = "test_admin_revenue_marketing_os"


@pytest.fixture(autouse=True)
def _isolated_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """
    Point every test at its own tmp JSON store + admin key so the
    singleton in ``dealix.revenue_marketing_os.store`` does not
    bleed state between tests.
    """
    path = tmp_path / f"hermes_{uuid.uuid4().hex}.json"
    monkeypatch.setenv("DEALIX_REVENUE_MARKETING_STORE", str(path))
    monkeypatch.setenv("ADMIN_API_KEYS", _ADMIN_KEY)
    from dealix.revenue_marketing_os.store import reset_revenue_marketing_store_for_tests

    reset_revenue_marketing_store_for_tests(path=path)
    return path


def _admin_headers() -> dict[str, str]:
    return {"X-Admin-API-Key": _ADMIN_KEY}


# ── Scoring laws ────────────────────────────────────────────────────


def test_lead_score_uses_published_weights() -> None:
    from dealix.revenue_marketing_os.scoring import compute_lead_score

    # All inputs at 1.0 → score is sum of weights × 100 = 100.
    score, bd = compute_lead_score(
        {
            "icp_fit": 1.0,
            "pain_likelihood": 1.0,
            "ability_to_pay": 1.0,
            "urgency": 1.0,
            "partner_potential": 1.0,
            "trust_fit": 1.0,
        }
    )
    assert score == 100
    assert bd["icp_fit"] == 25
    assert bd["pain_likelihood"] == 20
    assert bd["ability_to_pay"] == 20
    assert bd["urgency"] == 15
    assert bd["partner_potential"] == 10
    assert bd["trust_fit"] == 10


def test_lead_score_clips_and_handles_bad_input() -> None:
    from dealix.revenue_marketing_os.scoring import compute_lead_score

    score, _ = compute_lead_score(
        {"icp_fit": 1.5, "pain_likelihood": -1.0, "ability_to_pay": "x"}
    )
    # 1.5 clipped to 1.0 → contributes 25; bad string → 0.
    assert 20 <= score <= 30


def test_revenue_quality_law_penalizes_delivery_burden() -> None:
    from dealix.revenue_marketing_os.scoring import compute_revenue_quality_score

    heavy_one_off = {
        "margin": 1.0,
        "repeatability": 0.2,
        "retainer_potential": 0.1,
        "data_moat": 0.2,
        "partner_potential": 0.1,
        "delivery_burden": 1.0,
    }
    recurring = {
        "margin": 0.7,
        "repeatability": 1.0,
        "retainer_potential": 1.0,
        "data_moat": 0.7,
        "partner_potential": 0.5,
        "delivery_burden": 0.2,
    }
    one_off_score, _ = compute_revenue_quality_score(heavy_one_off)
    recurring_score, _ = compute_revenue_quality_score(recurring)
    # Recurring revenue MUST score higher than heavy one-off cash.
    assert recurring_score > one_off_score


# ── Revenue Assurance gate ──────────────────────────────────────────


def test_revenue_assurance_blocks_paid_without_verification() -> None:
    from dealix.revenue_marketing_os.governance import check_revenue

    decision = check_revenue(
        status="paid",
        payment_verified=False,
        invoice_verified=False,
        agreement_signed=False,
    )
    assert decision.allowed is False
    assert "no_unverified_revenue_counted" in decision.triggered_gates


def test_revenue_assurance_allows_paid_with_payment_proof() -> None:
    from dealix.revenue_marketing_os.governance import check_revenue

    decision = check_revenue(
        status="paid",
        payment_verified=True,
        invoice_verified=False,
        agreement_signed=False,
    )
    assert decision.allowed is True


def test_revenue_assurance_requires_signed_for_committed() -> None:
    from dealix.revenue_marketing_os.governance import check_revenue

    decision = check_revenue(
        status="committed",
        payment_verified=False,
        invoice_verified=False,
        agreement_signed=False,
    )
    assert decision.allowed is False


# ── Trust check ─────────────────────────────────────────────────────


def test_claim_check_rejects_forbidden_phrases() -> None:
    from dealix.revenue_marketing_os.governance import check_claim

    decision = check_claim("We give guaranteed results in 30 days.")
    assert decision.allowed is False
    assert "no_claim_without_trust_check" in decision.triggered_gates


def test_claim_check_allows_neutral_text() -> None:
    from dealix.revenue_marketing_os.governance import check_claim

    assert check_claim("Dealix helps you ship a revenue loop.").allowed is True


def test_action_check_blocks_approval_required_actions() -> None:
    from dealix.revenue_marketing_os.governance import check_action

    blocked = check_action("launch_paid_campaign", has_approval=False)
    assert blocked.allowed is False
    allowed = check_action("launch_paid_campaign", has_approval=True)
    assert allowed.allowed is True


# ── Attribution ─────────────────────────────────────────────────────


def test_attribution_refuses_unverified_revenue() -> None:
    from dealix.revenue_marketing_os.attribution import compute_attribution
    from dealix.revenue_marketing_os.schemas import RevenueRecord

    rev = RevenueRecord(
        id="rev_x", amount_sar=1000, status="pipeline", payment_verified=False
    )
    assert compute_attribution(revenue=rev, touches=[]) == []


def test_attribution_multi_touch_spreads_credit() -> None:
    from datetime import UTC, datetime, timedelta

    from dealix.revenue_marketing_os.attribution import compute_attribution
    from dealix.revenue_marketing_os.schemas import RevenueRecord, TouchRecord

    rev = RevenueRecord(
        id="rev_a",
        amount_sar=999.0,
        status="paid",
        lead_id="lead_a",
        payment_verified=True,
    )
    now = datetime.now(UTC)
    touches = [
        TouchRecord(
            id="t1",
            lead_id="lead_a",
            channel="linkedin",
            touch_type="outbound_sent_manual",
            occurred_at=now - timedelta(days=3),
        ),
        TouchRecord(
            id="t2",
            lead_id="lead_a",
            channel="direct_outreach",
            touch_type="inbound_reply",
            occurred_at=now - timedelta(days=2),
        ),
        TouchRecord(
            id="t3",
            lead_id="lead_a",
            channel="direct_outreach",
            touch_type="call_done",
            occurred_at=now,
        ),
    ]
    rows = compute_attribution(revenue=rev, touches=touches, model="multi_touch")
    assert len(rows) == 3
    # Equal credit: 999/3 = 333 per row.
    assert all(abs(r.amount_sar - 333.0) < 0.01 for r in rows)
    # All rows must carry the same attribution_type.
    assert {r.attribution_type for r in rows} == {"multi_touch"}


def test_attribution_first_and_last_touch_pick_one() -> None:
    from datetime import UTC, datetime, timedelta

    from dealix.revenue_marketing_os.attribution import compute_attribution
    from dealix.revenue_marketing_os.schemas import RevenueRecord, TouchRecord

    rev = RevenueRecord(
        id="rev_b",
        amount_sar=500.0,
        status="paid",
        lead_id="lead_b",
        payment_verified=True,
    )
    now = datetime.now(UTC)
    touches = [
        TouchRecord(
            id="t1",
            lead_id="lead_b",
            channel="linkedin",
            touch_type="outbound_sent_manual",
            occurred_at=now - timedelta(days=5),
        ),
        TouchRecord(
            id="t2",
            lead_id="lead_b",
            channel="warm_intro",
            touch_type="call_done",
            occurred_at=now,
        ),
    ]

    first = compute_attribution(revenue=rev, touches=touches, model="first_touch")
    last = compute_attribution(revenue=rev, touches=touches, model="last_touch")
    assert len(first) == 1
    assert len(last) == 1
    assert first[0].channel == "linkedin"
    assert last[0].channel == "warm_intro"


# ── HTTP surface ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/hermes/growth/status", headers=_admin_headers())
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "revenue_marketing_os"
    assert body["hard_gates"]["no_live_send"] is True
    assert body["hard_gates"]["no_unverified_revenue_counted"] is True


@pytest.mark.asyncio
async def test_seed_loads_offer_ladder() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/v1/hermes/growth/seed", headers=_admin_headers())
        offers = await client.get(
            "/api/v1/hermes/growth/offers", headers=_admin_headers()
        )
        public_ladder = await client.get(
            "/api/v1/hermes/growth/public/offer-ladder"
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["seeded"] is True
    assert payload["offers_added"] >= 1
    assert offers.status_code == 200
    names = {o["id"] for o in offers.json()["offers"]}
    assert "revenue_hunter_pilot" in names
    assert "ai_trust_kit" in names
    assert public_ladder.status_code == 200
    ladder = public_ladder.json()["offers"]
    # Public ladder ordered by ladder_step.
    steps = [o["ladder_step"] for o in ladder]
    assert steps == sorted(steps)


@pytest.mark.asyncio
async def test_campaign_creates_in_draft_and_requires_approval() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    headers = _admin_headers()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/hermes/growth/seed", headers=headers)
        r = await client.post(
            "/api/v1/hermes/growth/campaigns",
            headers=headers,
            json={
                "name": "AI Trust Kit for Saudi B2B",
                "target_icp_id": "icp_ai_governance_buyer",
                "pain": "no permissions or approvals",
                "offer_id": "ai_trust_kit",
                "channel": "direct_outreach",
                "cta": "Book AI Trust Diagnostic",
                "target_accounts": 100,
                "scale_rule": "scale if >=3 paid diagnostics from 100",
                "kill_rule": "kill if 0 qualified replies from 100",
            },
        )
        campaign = r.json()["campaign"]
        assert campaign["status"] == "draft"
        assert campaign["approval_required"] is True

        # Approve flips the status to active and stamps approver.
        cid = campaign["id"]
        approve = await client.post(
            f"/api/v1/hermes/growth/campaigns/{cid}/approve",
            headers=headers,
            json={"approver": "founder"},
        )
        assert approve.status_code == 200
        approved = approve.json()["campaign"]
        assert approved["status"] == "active"
        assert approved["approved_by"] == "founder"


@pytest.mark.asyncio
async def test_lead_creation_computes_fit_score() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    headers = _admin_headers()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/hermes/growth/leads",
            headers=headers,
            json={
                "source": "linkedin_post",
                "company_name": "Acme",
                "icp_fit": 1.0,
                "pain_likelihood": 1.0,
                "ability_to_pay": 1.0,
                "urgency": 1.0,
                "partner_potential": 1.0,
                "trust_fit": 1.0,
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body["fit_score"] == 100
    assert body["lead"]["status"] == "new"


@pytest.mark.asyncio
async def test_revenue_endpoint_refuses_unverified_paid_status() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    headers = _admin_headers()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/hermes/growth/revenue",
            headers=headers,
            json={
                "amount_sar": 999.0,
                "status": "paid",
                "payment_verified": False,
                "invoice_verified": False,
            },
        )
    assert r.status_code == 409
    detail = r.json()["detail"]
    assert detail["code"] == "revenue_assurance_block"


@pytest.mark.asyncio
async def test_revenue_endpoint_accepts_paid_with_proof_and_scores_quality() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    headers = _admin_headers()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/hermes/growth/revenue",
            headers=headers,
            json={
                "amount_sar": 8000.0,
                "status": "retainer_active",
                "payment_verified": True,
                "source_offer_id": "monthly_revenue_command",
                "channel": "direct_outreach",
                "margin": 0.7,
                "repeatability": 1.0,
                "retainer_potential": 1.0,
                "data_moat": 0.6,
                "partner_potential": 0.4,
                "delivery_burden": 0.3,
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body["quality_score"] >= 50
    assert body["revenue"]["status"] == "retainer_active"
    assert body["revenue"]["payment_verified"] is True


@pytest.mark.asyncio
async def test_full_money_loop_with_attribution_and_dashboard() -> None:
    """End-to-end: campaign → lead → touch → revenue → attribution → dashboard."""
    from api.main import app

    transport = ASGITransport(app=app)
    headers = _admin_headers()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/hermes/growth/seed", headers=headers)

        campaign_r = await client.post(
            "/api/v1/hermes/growth/campaigns",
            headers=headers,
            json={
                "name": "Agency White-label",
                "target_icp_id": "icp_agency",
                "offer_id": "agency_white_label",
                "channel": "direct_outreach",
                "cta": "Partner call",
            },
        )
        campaign_id = campaign_r.json()["campaign"]["id"]

        lead_r = await client.post(
            "/api/v1/hermes/growth/leads",
            headers=headers,
            json={
                "source": "linkedin",
                "campaign_id": campaign_id,
                "company_name": "Agency X",
                "icp_id": "icp_agency",
                "icp_fit": 0.9,
                "ability_to_pay": 0.8,
                "urgency": 0.8,
            },
        )
        lead_id = lead_r.json()["lead"]["id"]

        for variant, touch_type in (
            ("variant_a", "outbound_sent_manual"),
            ("variant_b", "inbound_reply"),
            ("variant_b", "call_done"),
        ):
            await client.post(
                "/api/v1/hermes/growth/touches",
                headers=headers,
                json={
                    "lead_id": lead_id,
                    "campaign_id": campaign_id,
                    "channel": "direct_outreach",
                    "touch_type": touch_type,
                    "message_variant": variant,
                    "advance_lead_status": (
                        "closed_won" if touch_type == "call_done" else None
                    ),
                },
            )

        rev = await client.post(
            "/api/v1/hermes/growth/revenue",
            headers=headers,
            json={
                "amount_sar": 999.0,
                "status": "paid",
                "payment_verified": True,
                "source_offer_id": "agency_white_label",
                "channel": "direct_outreach",
                "campaign_id": campaign_id,
                "lead_id": lead_id,
            },
        )
        assert rev.status_code == 200
        revenue_id = rev.json()["revenue"]["id"]

        attr = await client.post(
            "/api/v1/hermes/growth/attribution",
            headers=headers,
            json={"revenue_id": revenue_id, "model": "multi_touch"},
        )
        assert attr.status_code == 200
        attr_body = attr.json()
        # Three touches → three attribution rows.
        assert len(attr_body["attribution"]) == 3

        dash = await client.get(
            "/api/v1/hermes/growth/dashboard", headers=headers
        )
        assert dash.status_code == 200
        body = dash.json()
        assert body["totals"]["verified_revenue_sar"] == 999.0
        assert body["totals"]["leads"] >= 1
        assert "agency_white_label" in body["revenue_by_offer"]


@pytest.mark.asyncio
async def test_scale_kill_emits_decision_only_never_acts() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    headers = _admin_headers()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/hermes/growth/seed", headers=headers)

        campaign_r = await client.post(
            "/api/v1/hermes/growth/campaigns",
            headers=headers,
            json={
                "name": "Test scale-kill",
                "offer_id": "revenue_hunter_pilot",
                "target_accounts": 4,
                "channel": "direct_outreach",
            },
        )
        cid = campaign_r.json()["campaign"]["id"]

        # Seed 4 leads with zero replies — should trigger "kill".
        for i in range(4):
            await client.post(
                "/api/v1/hermes/growth/leads",
                headers=headers,
                json={
                    "source": "test",
                    "campaign_id": cid,
                    "company_name": f"Co {i}",
                },
            )

        r = await client.post(
            f"/api/v1/hermes/growth/scale-kill/{cid}", headers=headers
        )
    assert r.status_code == 200
    body = r.json()
    assert body["decision"]["decision"] in {"kill", "pause"}
    assert body["requires_founder_approval"] is True


@pytest.mark.asyncio
async def test_governance_endpoints_block_forbidden_claims_and_actions() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    headers = _admin_headers()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        claim = await client.post(
            "/api/v1/hermes/growth/governance/claim-check",
            headers=headers,
            json={"text": "Dealix nodes give guaranteed results."},
        )
        action = await client.post(
            "/api/v1/hermes/growth/governance/action-check?action=launch_paid_campaign&has_approval=false",
            headers=headers,
        )
    assert claim.status_code == 200
    assert claim.json()["allowed"] is False
    assert action.status_code == 200
    assert action.json()["allowed"] is False
    assert action.json()["requires_approval"] is True


@pytest.mark.asyncio
async def test_funnel_endpoint_returns_ratios_in_zero_one_range() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    headers = _admin_headers()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/hermes/growth/funnel", headers=headers)
    assert r.status_code == 200
    body = r.json()
    for ratio in body["ratios"].values():
        assert 0.0 <= ratio <= 1.0
