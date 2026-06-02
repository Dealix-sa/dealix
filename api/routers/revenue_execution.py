"""Revenue Execution OS Router — approval-first product distribution.

Aggregates the distribution layer:
  target -> draft -> quality -> approval -> follow-up -> proposal ->
  proof -> payment handoff -> renewal -> metrics

All endpoints are admin-gated (X-API-Key). Every response carries a
``governance_decision``. NOTHING here sends, charges, or auto-approves: writes
only prepare drafts/handoffs and record founder decisions. A draft whose
governance decision is BLOCK cannot be approved.

Prefix: /api/v1/revenue-execution
"""

from __future__ import annotations

import logging
import os

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.revenue_execution_os import (
    draft_factory,
    metrics,
    offers,
    payment_handoff,
    proposal_factory,
    sectors,
    stores,
)
from auto_client_acquisition.revenue_execution_os.draft_quality import review_drafts, score_draft
from auto_client_acquisition.revenue_execution_os.followup_engine import build_followup_queue
from auto_client_acquisition.revenue_execution_os.models import (
    OPEN_DRAFT_STATUSES,
    DraftStatus,
    PaymentHandoffStatus,
    Prospect,
    now_iso,
)
from auto_client_acquisition.revenue_execution_os.proof_pack_factory import proof_pack_meets_bar
from auto_client_acquisition.revenue_execution_os.win_loss import weekly_learning

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/revenue-execution", tags=["revenue-execution"])

_ADMIN_KEY = os.getenv("DEALIX_ADMIN_API_KEY", "")


def _require_admin(x_api_key: str = Header(default="")) -> None:
    if not _ADMIN_KEY:
        return  # dev mode — no key configured
    if x_api_key != _ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


def _get_or_create_prospect(
    *, prospect_id: str | None, company: str, contact_name: str, sector: str, lead_source: str
) -> Prospect:
    if prospect_id:
        existing = stores.PROSPECTS.get(prospect_id)
        if existing is not None:
            return existing
    p = Prospect(
        prospect_id=prospect_id or f"prs_{os.urandom(8).hex()}",
        company=company,
        contact_name=contact_name,
        sector=sector,
        lead_source=lead_source,
        created_at=now_iso(),
    )
    return stores.PROSPECTS.add(p)


# ── request models ───────────────────────────────────────────────────────────


class GenerateDraftsRequest(BaseModel):
    prospect_id: str | None = None
    company: str = ""
    contact_name: str = ""
    sector: str = ""
    lead_source: str = "inbound"
    draft_types: list[str] | None = None
    offer_key: str | None = None


class GenerateProposalRequest(BaseModel):
    prospect_id: str | None = None
    company: str = ""
    contact_name: str = ""
    sector: str = ""
    offer_key: str = Field(..., description="An offer ladder key, e.g. revenue_sprint")
    problem: str = ""
    solution: str = ""


class PaymentHandoffRequest(BaseModel):
    proposal_id: str
    price_confirmed: bool = False
    scope_confirmed: bool = False
    terms_confirmed: bool = False
    founder_approved: bool = False


# ── overview / catalog ───────────────────────────────────────────────────────


@router.get("/overview")
async def overview(x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    drafts = stores.DRAFTS.list(limit=1_000_000)
    open_drafts = [d for d in drafts if d.status in OPEN_DRAFT_STATUSES]
    packs = stores.PROOF_PACKS.list(limit=1_000_000)
    handoffs = stores.PAYMENT_HANDOFFS.list(limit=1_000_000)
    return {
        "top_sectors": [s.to_dict() for s in sectors.rank_sectors()[:3]],
        "drafts_open": len(open_drafts),
        "followups_due": len(build_followup_queue()),
        "proposals_open": stores.PROPOSALS.count(),
        "proof_packs": len(packs),
        "proof_packs_meeting_bar": sum(1 for p in packs if proof_pack_meets_bar(p)),
        "payment_handoffs_ready": sum(
            1 for h in handoffs if not h.blocking_reasons and h.status != PaymentHandoffStatus.PAID
        ),
        "renewals_open": stores.RENEWALS.count(status="open"),
        "metrics_daily": metrics.daily_metrics(),
        "no_external_send": True,
        "governance_decision": "ALLOW",
    }


@router.get("/offers")
async def list_offers(x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    return {"offers": offers.ladder_as_dicts(), "governance_decision": "ALLOW"}


@router.get("/sectors")
async def list_sectors(x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    return {
        "sectors": [s.to_dict() for s in sectors.rank_sectors()],
        "governance_decision": "ALLOW",
    }


# ── drafts ───────────────────────────────────────────────────────────────────


@router.get("/drafts")
async def list_drafts(status: str | None = None, x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    drafts = stores.DRAFTS.list(limit=1_000_000)
    if status:
        drafts = [d for d in drafts if d.status == status]
    return {
        "drafts": [d.to_dict() for d in drafts],
        "count": len(drafts),
        "governance_decision": "ALLOW",
    }


@router.post("/drafts/generate")
async def generate_drafts(req: GenerateDraftsRequest, x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    prospect = _get_or_create_prospect(
        prospect_id=req.prospect_id,
        company=req.company,
        contact_name=req.contact_name,
        sector=req.sector,
        lead_source=req.lead_source,
    )
    try:
        drafts = draft_factory.generate_drafts(prospect, req.draft_types, offer_key=req.offer_key)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    report = review_drafts(drafts, {prospect.prospect_id: prospect})
    return {
        "prospect_id": prospect.prospect_id,
        "drafts": [d.to_dict() for d in drafts],
        "quality": report.to_dict(),
        "approval_required": True,
        "governance_decision": "REQUIRE_APPROVAL",
    }


@router.post("/drafts/{draft_id}/approve")
async def approve_draft(draft_id: str, x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    draft = stores.DRAFTS.get(draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="draft not found")
    if draft.governance_decision == "BLOCK":
        raise HTTPException(
            status_code=409, detail="cannot approve a BLOCKed draft — fix the content first"
        )
    updated = stores.DRAFTS.update(draft_id, status=str(DraftStatus.APPROVED), updated_at=now_iso())
    return {
        "draft": updated.to_dict() if updated else None,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/drafts/{draft_id}/reject")
async def reject_draft(draft_id: str, x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    if stores.DRAFTS.get(draft_id) is None:
        raise HTTPException(status_code=404, detail="draft not found")
    updated = stores.DRAFTS.update(draft_id, status=str(DraftStatus.REJECTED), updated_at=now_iso())
    return {"draft": updated.to_dict() if updated else None, "governance_decision": "ALLOW"}


@router.post("/drafts/{draft_id}/mark-copied")
async def mark_copied(draft_id: str, x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    draft = stores.DRAFTS.get(draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="draft not found")
    if draft.status != DraftStatus.APPROVED:
        raise HTTPException(status_code=409, detail="approve the draft before marking it copied")
    updated = stores.DRAFTS.update(
        draft_id, status=str(DraftStatus.COPIED_MANUALLY), updated_at=now_iso()
    )
    return {"draft": updated.to_dict() if updated else None, "governance_decision": "ALLOW"}


# ── follow-ups / proposals / proof / payments / renewals / win-loss / metrics ─


@router.get("/followups")
async def list_followups(x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    queue = build_followup_queue()
    return {
        "followups": [f.to_dict() for f in queue],
        "count": len(queue),
        "governance_decision": "ALLOW",
    }


@router.get("/proposals")
async def list_proposals(x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    props = stores.PROPOSALS.list(limit=1_000_000)
    return {
        "proposals": [p.to_dict() for p in props],
        "count": len(props),
        "governance_decision": "ALLOW",
    }


@router.post("/proposals/generate")
async def generate_proposal(
    req: GenerateProposalRequest, x_api_key: str = Header(default="")
) -> dict:
    _require_admin(x_api_key)
    try:
        offers.offer_by_key(req.offer_key)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"unknown offer_key: {req.offer_key}") from exc
    prospect = _get_or_create_prospect(
        prospect_id=req.prospect_id,
        company=req.company,
        contact_name=req.contact_name,
        sector=req.sector,
        lead_source="inbound",
    )
    proposal = proposal_factory.generate_proposal(
        prospect, req.offer_key, problem=req.problem, solution=req.solution
    )
    return {
        "proposal": proposal.to_dict(),
        "approval_required": True,
        "governance_decision": proposal.governance_decision,
    }


@router.get("/proof-packs")
async def list_proof_packs(x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    packs = stores.PROOF_PACKS.list(limit=1_000_000)
    return {
        "proof_packs": [{**p.to_dict(), "meets_bar": proof_pack_meets_bar(p)} for p in packs],
        "count": len(packs),
        "governance_decision": "ALLOW",
    }


@router.get("/payments")
async def list_payments(x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    handoffs = stores.PAYMENT_HANDOFFS.list(limit=1_000_000)
    return {
        "payment_handoffs": [h.to_dict() for h in handoffs],
        "count": len(handoffs),
        "governance_decision": "REQUIRE_APPROVAL",
    }


@router.post("/payments/handoff")
async def create_payment_handoff(
    req: PaymentHandoffRequest, x_api_key: str = Header(default="")
) -> dict:
    _require_admin(x_api_key)
    proposal = stores.PROPOSALS.get(req.proposal_id)
    if proposal is None:
        raise HTTPException(status_code=404, detail="proposal not found")
    handoff = payment_handoff.generate_payment_handoff(
        proposal,
        price_confirmed=req.price_confirmed,
        scope_confirmed=req.scope_confirmed,
        terms_confirmed=req.terms_confirmed,
        founder_approved=req.founder_approved,
    )
    # Always REQUIRE_APPROVAL: preparing a handoff never sends a payment link.
    return {
        "payment_handoff": handoff.to_dict(),
        "ready_to_send": payment_handoff.handoff_is_ready(handoff),
        "blocking_reasons": handoff.blocking_reasons,
        "governance_decision": "REQUIRE_APPROVAL",
    }


@router.get("/renewals")
async def list_renewals(x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    renewals = stores.RENEWALS.list(limit=1_000_000)
    return {
        "renewals": [r.to_dict() for r in renewals],
        "count": len(renewals),
        "governance_decision": "ALLOW",
    }


@router.get("/win-loss")
async def list_win_loss(x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    return {"learning": weekly_learning(), "governance_decision": "ALLOW"}


@router.get("/metrics")
async def get_metrics(x_api_key: str = Header(default="")) -> dict:
    _require_admin(x_api_key)
    return {
        "daily": metrics.daily_metrics(),
        "weekly": metrics.weekly_metrics(),
        "governance_decision": "ALLOW",
    }
