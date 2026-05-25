"""
Revenue Marketing OS HTTP surface — the Hermes Growth endpoints.

Every external action is draft-first. Every revenue write is verified
or refused. Every campaign decision goes through the founder
Approval Center. No live sends and no paid spend bypass.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from dealix.revenue_marketing_os.attribution import (
    compute_attribution,
    summarize_attribution,
)
from dealix.revenue_marketing_os.dashboard import (
    build_dashboard,
    evaluate_campaign,
)
from dealix.revenue_marketing_os.governance import (
    HARD_GATES,
    check_action,
    check_claim,
    check_revenue,
)
from dealix.revenue_marketing_os.schemas import (
    AttributionRecord,
    CampaignRecord,
    ExperimentRecord,
    LeadRecord,
    OfferRecord,
    RevenueRecord,
    TouchRecord,
)
from dealix.revenue_marketing_os.scoring import (
    compute_lead_score,
    compute_revenue_quality_score,
    funnel_metrics,
)
from dealix.revenue_marketing_os.seed import seed_if_empty
from dealix.revenue_marketing_os.store import (
    get_revenue_marketing_store,
    uid,
)

router = APIRouter(
    prefix="/api/v1/hermes/growth",
    dependencies=[Depends(require_admin_key)],
    tags=["revenue-marketing-os"],
)

router_public = APIRouter(
    prefix="/api/v1/hermes/growth/public",
    tags=["revenue-marketing-os-public"],
)


# ── Payloads ────────────────────────────────────────────────────────


class _CampaignPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., min_length=1)
    target_icp_id: str = ""
    target_segment: str = ""
    pain: str = ""
    offer_id: str = ""
    message_id: str = ""
    message_angle: str = ""
    channel: str = "direct_outreach"
    cta: str = ""
    success_metric: str = "paid_diagnostics"
    target_accounts: int = Field(default=100, ge=1, le=10_000)
    scale_rule: str = ""
    kill_rule: str = ""
    tracking_enabled: bool = True


class _LeadPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: str = Field(..., min_length=1)
    campaign_id: str = ""
    company_name: str = ""
    contact_name: str = ""
    contact_email: str = ""
    contact_role: str = ""
    icp_id: str = ""
    pain_hypothesis: str = ""
    consent_marketing: bool = False
    # 0.0-1.0 scoring inputs
    icp_fit: float = 0.0
    pain_likelihood: float = 0.0
    ability_to_pay: float = 0.0
    urgency: float = 0.0
    partner_potential: float = 0.0
    trust_fit: float = 0.0


class _TouchPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    lead_id: str = Field(..., min_length=1)
    campaign_id: str = ""
    channel: str = "direct_outreach"
    touch_type: str = "outbound_draft"
    message_variant: str = ""
    outcome: str = ""
    next_action: str = ""
    # Optional move of lead status when this touch implies it.
    advance_lead_status: str | None = None


class _ExperimentPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hypothesis: str = Field(..., min_length=1)
    campaign_id: str = ""
    variants: list[str] = Field(default_factory=list)
    success_metric: str = "paid_diagnostics"
    target_sample: int = Field(default=100, ge=1, le=10_000)


class _RevenuePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    amount_sar: float = Field(..., ge=0.0)
    status: str = "pipeline"
    source_offer_id: str = ""
    customer_id: str = ""
    lead_id: str = ""
    deal_id: str = ""
    campaign_id: str = ""
    channel: str = "direct_outreach"
    payment_verified: bool = False
    invoice_verified: bool = False
    agreement_signed: bool = False
    margin: float = 0.5
    repeatability: float = 0.5
    retainer_potential: float = 0.5
    data_moat: float = 0.3
    partner_potential: float = 0.3
    delivery_burden: float = 0.3
    notes: str = ""


class _AttributionPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    revenue_id: str = Field(..., min_length=1)
    model: str = Field(default="multi_touch")


class _CampaignApprovePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    approver: str = "founder"


class _ClaimCheckPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(..., min_length=1, max_length=8000)


# ── Status + seed ───────────────────────────────────────────────────


@router.get("/status")
async def status() -> dict[str, Any]:
    store = get_revenue_marketing_store()
    return {
        "service": "revenue_marketing_os",
        "version": "v1",
        "status": "operational",
        "hard_gates": HARD_GATES,
        "counts": {
            "offers": len(store.list_offers()),
            "icps": len(store.list_icps()),
            "campaigns": len(store.list_campaigns()),
            "leads": len(store.list_leads(limit=10_000)),
            "touches": len(store.list_touches()),
            "revenue_records": len(store.list_revenue()),
            "attribution_rows": len(store.list_attribution()),
            "experiments": len(store.list_experiments()),
            "scale_kill_decisions": len(store.list_decisions()),
        },
    }


@router.post("/seed")
async def seed() -> dict[str, Any]:
    """Idempotently load the offer-ladder + ICP seed."""
    added = seed_if_empty(get_revenue_marketing_store())
    return {"seeded": True, **added}


# ── Offers / ICPs ───────────────────────────────────────────────────


@router.get("/offers")
async def list_offers() -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_offers()
    return {"offers": [r.model_dump(mode="json") for r in rows]}


@router.get("/icps")
async def list_icps() -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_icps()
    return {"icps": [r.model_dump(mode="json") for r in rows]}


# ── Campaigns ───────────────────────────────────────────────────────


@router.post("/campaigns")
async def create_campaign(body: _CampaignPayload) -> dict[str, Any]:
    store = get_revenue_marketing_store()
    rec = CampaignRecord(
        id=uid("camp"),
        name=body.name,
        target_icp_id=body.target_icp_id,
        target_segment=body.target_segment,
        pain=body.pain,
        offer_id=body.offer_id,
        message_id=body.message_id,
        message_angle=body.message_angle,
        channel=body.channel,  # type: ignore[arg-type]
        cta=body.cta,
        success_metric=body.success_metric,
        target_accounts=body.target_accounts,
        tracking_enabled=body.tracking_enabled,
        scale_rule=body.scale_rule,
        kill_rule=body.kill_rule,
        status="draft",
        approval_required=True,
    )
    saved = store.upsert_campaign(rec)
    return {"campaign": saved.model_dump(mode="json")}


@router.get("/campaigns")
async def list_campaigns() -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_campaigns()
    return {"campaigns": [r.model_dump(mode="json") for r in rows]}


@router.post("/campaigns/{campaign_id}/approve")
async def approve_campaign(
    campaign_id: str, body: _CampaignApprovePayload
) -> dict[str, Any]:
    store = get_revenue_marketing_store()
    rec = store.get_campaign(campaign_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="campaign_not_found")
    updated = rec.model_copy(
        update={
            "status": "active",
            "approved_by": body.approver,
            "approved_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
        }
    )
    saved = store.upsert_campaign(updated)
    return {"campaign": saved.model_dump(mode="json")}


# ── Leads ───────────────────────────────────────────────────────────


@router.post("/leads")
async def create_lead(body: _LeadPayload) -> dict[str, Any]:
    score, breakdown = compute_lead_score(body.model_dump())
    store = get_revenue_marketing_store()
    rec = LeadRecord(
        id=uid("lead"),
        campaign_id=body.campaign_id,
        source=body.source,
        company_name=body.company_name,
        contact_name=body.contact_name,
        contact_email=body.contact_email,
        contact_role=body.contact_role,
        icp_id=body.icp_id,
        fit_score=score,
        score_breakdown=breakdown,
        pain_hypothesis=body.pain_hypothesis,
        consent_marketing=body.consent_marketing,
        status="new",
    )
    saved = store.upsert_lead(rec)
    return {
        "lead": saved.model_dump(mode="json"),
        "fit_score": score,
        "score_breakdown": breakdown,
    }


@router.get("/leads")
async def list_leads(
    campaign_id: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=2000),
) -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_leads(campaign_id=campaign_id, limit=limit)
    return {"leads": [r.model_dump(mode="json") for r in rows], "count": len(rows)}


# ── Touches ─────────────────────────────────────────────────────────


_ALLOWED_LEAD_STATUSES = {
    "new",
    "mql",
    "sql",
    "discovery_booked",
    "discovery_done",
    "proposal_sent",
    "closed_won",
    "closed_lost",
    "nurture",
}


@router.post("/touches")
async def create_touch(body: _TouchPayload) -> dict[str, Any]:
    store = get_revenue_marketing_store()
    lead = store.get_lead(body.lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="lead_not_found")
    touch = TouchRecord(
        id=uid("touch"),
        lead_id=lead.id,
        campaign_id=body.campaign_id or lead.campaign_id,
        channel=body.channel,  # type: ignore[arg-type]
        touch_type=body.touch_type,  # type: ignore[arg-type]
        message_variant=body.message_variant,
        outcome=body.outcome,
        next_action=body.next_action,
    )
    saved_touch = store.append_touch(touch)

    advanced = None
    if body.advance_lead_status and body.advance_lead_status in _ALLOWED_LEAD_STATUSES:
        advanced = store.upsert_lead(
            lead.model_copy(update={"status": body.advance_lead_status})
        )

    return {
        "touch": saved_touch.model_dump(mode="json"),
        "lead": (advanced or lead).model_dump(mode="json"),
    }


# ── Experiments ─────────────────────────────────────────────────────


@router.post("/experiments")
async def create_experiment(body: _ExperimentPayload) -> dict[str, Any]:
    rec = ExperimentRecord(
        id=uid("exp"),
        campaign_id=body.campaign_id,
        hypothesis=body.hypothesis,
        variants=body.variants,
        success_metric=body.success_metric,
        target_sample=body.target_sample,
    )
    saved = get_revenue_marketing_store().upsert_experiment(rec)
    return {"experiment": saved.model_dump(mode="json")}


@router.get("/experiments")
async def list_experiments() -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_experiments()
    return {"experiments": [r.model_dump(mode="json") for r in rows]}


# ── Revenue ─────────────────────────────────────────────────────────


@router.post("/revenue")
async def record_revenue(body: _RevenuePayload) -> dict[str, Any]:
    """
    Record a revenue event. Refuses to mark a record as paid/invoiced/
    committed without the matching verification flag.
    """
    decision = check_revenue(
        status=body.status,
        payment_verified=body.payment_verified,
        invoice_verified=body.invoice_verified,
        agreement_signed=body.agreement_signed,
    )
    if not decision.allowed:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "revenue_assurance_block",
                "reason_ar": decision.reason_ar,
                "reason_en": decision.reason_en,
                "triggered_gates": list(decision.triggered_gates),
            },
        )

    quality_score, _ = compute_revenue_quality_score(body.model_dump())
    rec = RevenueRecord(
        id=uid("rev"),
        amount_sar=body.amount_sar,
        status=body.status,  # type: ignore[arg-type]
        source_offer_id=body.source_offer_id,
        customer_id=body.customer_id,
        lead_id=body.lead_id,
        deal_id=body.deal_id,
        campaign_id=body.campaign_id,
        channel=body.channel,  # type: ignore[arg-type]
        payment_verified=body.payment_verified,
        invoice_verified=body.invoice_verified,
        agreement_signed=body.agreement_signed,
        received_at=datetime.now(UTC) if body.payment_verified else None,
        margin=body.margin,
        repeatability=body.repeatability,
        retainer_potential=body.retainer_potential,
        data_moat=body.data_moat,
        partner_potential=body.partner_potential,
        delivery_burden=body.delivery_burden,
        quality_score=float(quality_score),
        notes=body.notes,
    )
    saved = get_revenue_marketing_store().upsert_revenue(rec)
    return {
        "revenue": saved.model_dump(mode="json"),
        "quality_score": quality_score,
    }


@router.get("/revenue")
async def list_revenue() -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_revenue()
    return {"revenue": [r.model_dump(mode="json") for r in rows]}


@router.get("/revenue-quality")
async def revenue_quality() -> dict[str, Any]:
    """Per-record revenue-quality scores + aggregate average."""
    rows = get_revenue_marketing_store().list_revenue()
    scored: list[dict[str, Any]] = []
    for r in rows:
        score, breakdown = compute_revenue_quality_score(r.model_dump())
        scored.append(
            {
                "revenue_id": r.id,
                "status": r.status,
                "amount_sar": r.amount_sar,
                "quality_score": score,
                "breakdown": breakdown,
            }
        )
    avg = round(sum(s["quality_score"] for s in scored) / len(scored), 2) if scored else 0.0
    return {"scored": scored, "average_quality_score": avg}


# ── Attribution ─────────────────────────────────────────────────────


@router.post("/attribution")
async def create_attribution(body: _AttributionPayload) -> dict[str, Any]:
    store = get_revenue_marketing_store()
    rev = store.get_revenue(body.revenue_id)
    if rev is None:
        raise HTTPException(status_code=404, detail="revenue_not_found")
    touches = store.list_touches(lead_id=rev.lead_id) if rev.lead_id else []
    rows = compute_attribution(revenue=rev, touches=touches, model=body.model)
    if not rows:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "revenue_not_verified",
                "reason_en": "Cannot attribute unverified revenue.",
            },
        )
    saved = [store.append_attribution(r) for r in rows]
    return {
        "attribution": [r.model_dump(mode="json") for r in saved],
        "summary": summarize_attribution(saved),
    }


@router.get("/attribution")
async def list_attribution(
    revenue_id: str | None = Query(default=None),
    campaign_id: str | None = Query(default=None),
) -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_attribution(
        revenue_id=revenue_id, campaign_id=campaign_id
    )
    return {
        "attribution": [r.model_dump(mode="json") for r in rows],
        "summary": summarize_attribution(rows),
    }


# ── Dashboard + scale/kill ──────────────────────────────────────────


@router.get("/dashboard")
async def dashboard() -> dict[str, Any]:
    return build_dashboard(get_revenue_marketing_store())


@router.post("/scale-kill/{campaign_id}")
async def scale_kill(campaign_id: str) -> dict[str, Any]:
    store = get_revenue_marketing_store()
    rec = store.get_campaign(campaign_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="campaign_not_found")
    decision = evaluate_campaign(rec, store=store)
    saved = store.append_decision(decision)
    return {
        "decision": saved.model_dump(mode="json"),
        "requires_founder_approval": True,
    }


# ── Governance ─────────────────────────────────────────────────────


@router.post("/governance/claim-check")
async def claim_check(body: _ClaimCheckPayload) -> dict[str, Any]:
    decision = check_claim(body.text)
    return {
        "allowed": decision.allowed,
        "reason_ar": decision.reason_ar,
        "reason_en": decision.reason_en,
        "requires_approval": decision.requires_approval,
        "triggered_gates": list(decision.triggered_gates),
    }


@router.post("/governance/action-check")
async def action_check(
    action: str = Query(..., min_length=1),
    has_approval: bool = Query(default=False),
) -> dict[str, Any]:
    decision = check_action(action, has_approval=has_approval)
    return {
        "allowed": decision.allowed,
        "reason_ar": decision.reason_ar,
        "reason_en": decision.reason_en,
        "requires_approval": decision.requires_approval,
        "triggered_gates": list(decision.triggered_gates),
    }


# ── Funnel ─────────────────────────────────────────────────────────


@router.get("/funnel")
async def funnel() -> dict[str, Any]:
    """Compute the B2B funnel ratios from lead status counts."""
    leads = get_revenue_marketing_store().list_leads(limit=10_000)
    counts: dict[str, int] = {
        "visitor": 0,
        "lead": len(leads),
        "mql": 0,
        "sql": 0,
        "call": 0,
        "proposal": 0,
        "win": 0,
        "payment": 0,
        "retainer": 0,
        "expansion": 0,
    }
    for lead in leads:
        if lead.status == "mql":
            counts["mql"] += 1
        if lead.status in (
            "sql",
            "discovery_booked",
            "discovery_done",
            "proposal_sent",
            "closed_won",
        ):
            counts["sql"] += 1
        if lead.status in ("discovery_booked", "discovery_done", "proposal_sent", "closed_won"):
            counts["call"] += 1
        if lead.status in ("proposal_sent", "closed_won"):
            counts["proposal"] += 1
        if lead.status == "closed_won":
            counts["win"] += 1
    revenue = get_revenue_marketing_store().list_revenue()
    counts["payment"] = sum(1 for r in revenue if r.payment_verified)
    counts["retainer"] = sum(1 for r in revenue if r.status == "retainer_active")
    counts["expansion"] = sum(1 for r in revenue if r.status == "expanded")
    return {"counts": counts, "ratios": funnel_metrics(counts)}


# ── Public marketing endpoint (no admin key) ────────────────────────


@router_public.get("/offer-ladder")
async def public_offer_ladder() -> dict[str, Any]:
    """Public read-only view of the offer ladder (for landing pages)."""
    store = get_revenue_marketing_store()
    rows = store.list_offers()
    rows.sort(key=lambda x: x.ladder_step)
    return {
        "offers": [
            {
                "id": r.id,
                "name": r.name,
                "tier": r.tier,
                "ladder_step": r.ladder_step,
                "starting_price_sar": r.starting_price_sar,
            }
            for r in rows
        ]
    }


ROUTERS = (router, router_public)
