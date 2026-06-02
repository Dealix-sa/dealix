"""API tests for the Revenue Execution OS router.

Verifies the approval-first contract over HTTP: drafts are pending_approval,
a BLOCKed draft cannot be approved, and a payment handoff is never ready
without its preconditions. Uses the shared ``async_client`` fixture.
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.models import Draft, DraftStatus, now_iso


@pytest.fixture(autouse=True)
def _isolated_stores(tmp_path, monkeypatch):
    for env, name in {
        "DEALIX_REVX_PROSPECTS_PATH": "prospects.jsonl",
        "DEALIX_REVX_DRAFTS_PATH": "drafts.jsonl",
        "DEALIX_REVX_FOLLOWUPS_PATH": "followups.jsonl",
        "DEALIX_REVX_PROPOSALS_PATH": "proposals.jsonl",
        "DEALIX_REVX_PROOF_PACKS_PATH": "proof_packs.jsonl",
        "DEALIX_REVX_PAYMENT_HANDOFFS_PATH": "payment_handoffs.jsonl",
        "DEALIX_REVX_RENEWALS_PATH": "renewals.jsonl",
        "DEALIX_REVX_WIN_LOSS_PATH": "win_loss.jsonl",
    }.items():
        monkeypatch.setenv(env, str(tmp_path / name))
    yield


async def test_overview_declares_no_external_send(async_client: AsyncClient):
    resp = await async_client.get("/api/v1/revenue-execution/overview")
    assert resp.status_code == 200
    body = resp.json()
    assert body["no_external_send"] is True
    assert body["governance_decision"] == "ALLOW"
    assert body["top_sectors"][0]["key"] == "marketing_agencies"


async def test_generate_approve_copy_flow(async_client: AsyncClient):
    gen = await async_client.post(
        "/api/v1/revenue-execution/drafts/generate",
        json={"company": "Acme", "contact_name": "Sara", "sector": "marketing_agencies"},
    )
    assert gen.status_code == 200
    body = gen.json()
    assert body["approval_required"] is True
    assert body["drafts"]
    for d in body["drafts"]:
        assert d["status"] == "pending_approval"
        assert d["approval_required"] is True
        assert d["governance_decision"]
    draft_id = body["drafts"][0]["draft_id"]

    appr = await async_client.post(f"/api/v1/revenue-execution/drafts/{draft_id}/approve")
    assert appr.status_code == 200
    assert appr.json()["draft"]["status"] == "approved"

    copied = await async_client.post(f"/api/v1/revenue-execution/drafts/{draft_id}/mark-copied")
    assert copied.status_code == 200
    assert copied.json()["draft"]["status"] == "copied_manually"


async def test_cannot_approve_blocked_draft(async_client: AsyncClient):
    blocked = Draft(
        draft_id="blk1",
        prospect_id="p",
        subject="x",
        body_ar="نضمن لك نتائج مبيعات",
        status=DraftStatus.PENDING_APPROVAL,
        governance_decision="BLOCK",
        issues=["forbidden_claim:نضمن لك"],
        created_at=now_iso(),
    )
    stores.DRAFTS.add(blocked)
    resp = await async_client.post("/api/v1/revenue-execution/drafts/blk1/approve")
    assert resp.status_code == 409


async def test_payment_handoff_requires_preconditions(async_client: AsyncClient):
    prop = await async_client.post(
        "/api/v1/revenue-execution/proposals/generate",
        json={"company": "Acme", "sector": "clinics", "offer_key": "revenue_sprint"},
    )
    assert prop.status_code == 200
    proposal_id = prop.json()["proposal"]["proposal_id"]

    handoff = await async_client.post(
        "/api/v1/revenue-execution/payments/handoff",
        json={"proposal_id": proposal_id},
    )
    assert handoff.status_code == 200
    hb = handoff.json()
    assert hb["ready_to_send"] is False
    assert hb["governance_decision"] == "REQUIRE_APPROVAL"
    assert "proposal_approved" in hb["blocking_reasons"]


async def test_offers_and_sectors_endpoints(async_client: AsyncClient):
    offers_resp = await async_client.get("/api/v1/revenue-execution/offers")
    assert offers_resp.status_code == 200
    keys = {o["key"] for o in offers_resp.json()["offers"]}
    assert {"free_diagnostic", "revenue_sprint", "managed_revenue_ops"} <= keys

    sectors_resp = await async_client.get("/api/v1/revenue-execution/sectors")
    assert sectors_resp.status_code == 200
    assert sectors_resp.json()["sectors"][0]["key"] == "marketing_agencies"
