"""Revenue Marketing Engine admin API — draft-first, governed.

All endpoints are admin-key gated. State-changing endpoints append an
evidence event to the autopilot store with an ``event_type`` prefixed
``revenue_marketing_*``. No external publish or send is performed; everything
returns drafts.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from dealix.revenue_marketing.agents import (
    MARKETING_AGENTS,
    propose_via_agent,
)
from dealix.revenue_marketing.attribution import (
    AttrDimension,
    attribution_chain_for_deal,
    record_attribution,
    revenue_by_dimension,
)
from dealix.revenue_marketing.dashboard import dashboard_snapshot
from dealix.revenue_marketing.experiments import (
    create_experiment,
    decide,
    record_result,
)
from dealix.revenue_marketing.marketing_graph import build_graph
from dealix.revenue_marketing.quality_gates import validate_campaign
from dealix.revenue_marketing.revenue_portfolio import portfolio_health
from dealix.revenue_marketing.schemas import (
    AttributionType,
    CampaignStatus,
    CaseStudyDraft,
    MarketingCampaign,
    MarketingTouch,
    MessageVariant,
    Offer,
    OfferRung,
    compute_lead_score,
)
from dealix.revenue_marketing.store import (
    get_revenue_marketing_store,
    uid,
)
from dealix.revenue_ops_autopilot.schemas import EvidenceEvent
from dealix.revenue_ops_autopilot.store import (
    get_autopilot_store,
)
from dealix.revenue_ops_autopilot.store import (
    uid as ev_uid,
)

router = APIRouter(
    prefix="/api/v1/revenue-marketing",
    dependencies=[Depends(require_admin_key)],
    tags=["revenue-marketing"],
)


_ALLOWED_TRANSITIONS: dict[CampaignStatus, set[CampaignStatus]] = {
    "draft": {"approval_pending", "killed"},
    "approval_pending": {"active", "draft", "killed"},
    "active": {"paused", "killed", "completed"},
    "paused": {"active", "killed", "completed"},
    "killed": set(),
    "completed": set(),
}


def _log_evidence(*, event_type: str, summary: str, entity_id: str = "") -> None:
    try:
        get_autopilot_store().append_evidence(
            EvidenceEvent(
                id=ev_uid("ev"),
                event_type=event_type,
                entity_type="revenue_marketing",
                entity_id=entity_id,
                source="revenue_marketing",
                summary=summary,
            ),
        )
    except Exception:
        pass


# ────────────────────────── payloads ─────────────────────────────────


class CampaignCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    campaign_name: str = Field(..., min_length=1, max_length=200)
    target_segment: str = ""
    offer_id: str = ""
    channel: str = ""
    message_angle: str = ""
    budget_sar: float = Field(0.0, ge=0.0)
    success_metric: str = ""
    scale_kill_rule: str = ""
    tracking_url_pattern: str = ""


class CampaignStatusPatchPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: CampaignStatus
    note: str = ""


class OfferCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name_ar: str = Field(..., min_length=1, max_length=200)
    name_en: str = Field(..., min_length=1, max_length=200)
    rung: OfferRung
    price_min_sar: float = Field(0.0, ge=0.0)
    price_max_sar: float = Field(0.0, ge=0.0)
    target_segment: str = Field(..., min_length=1, max_length=200)
    pain_addressed: str = Field(..., min_length=1, max_length=200)
    deliverables_ar: list[str] = Field(default_factory=list)
    deliverables_en: list[str] = Field(default_factory=list)
    success_metric: str = Field(..., min_length=1, max_length=200)
    scale_kill_rule: str = Field(..., min_length=1, max_length=200)


class MessageCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    offer_id: str = Field(..., min_length=1, max_length=64)
    angle: str = Field(..., min_length=1, max_length=64)
    headline_ar: str = ""
    headline_en: str = ""
    body_ar: str = ""
    body_en: str = ""
    cta_ar: str = "احجز جلسة"
    cta_en: str = "Book a session"


class TouchCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    campaign_id: str | None = None
    lead_id: str = ""
    touch_type: str = ""
    channel: str = ""
    content_id: str = ""
    message_variant: str = ""


class AttributionCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    deal_id: str = Field(..., min_length=1, max_length=128)
    revenue_sar: float = Field(..., ge=0.0)
    campaign_id: str | None = None
    offer_id: str | None = None
    channel: str | None = None
    asset_id: str | None = None
    agent_id: str | None = None
    attribution_type: AttributionType = "multi_touch"
    payment_received: bool = False
    signed_agreement: bool = False


class LeadScorePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    icp_fit: float = Field(..., ge=0.0, le=1.0)
    pain: float = Field(..., ge=0.0, le=1.0)
    ability_to_pay: float = Field(..., ge=0.0, le=1.0)
    urgency: float = Field(..., ge=0.0, le=1.0)
    partner_potential: float = Field(..., ge=0.0, le=1.0)
    trust_fit: float = Field(..., ge=0.0, le=1.0)


class ExperimentCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    experiment_name: str = Field(..., min_length=1, max_length=200)
    target_segment: str = Field(..., min_length=1, max_length=200)
    offer_id: str = Field(..., min_length=1, max_length=64)
    variable_tested: str = Field(..., min_length=1, max_length=200)
    variant_a: str = Field(..., min_length=1, max_length=200)
    variant_b: str = Field(..., min_length=1, max_length=200)
    success_metric: str = Field(..., min_length=1, max_length=200)


class ExperimentResultPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    variant: Literal["a", "b"]
    value: float


class AgentProposePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any] = Field(default_factory=dict)


class CaseStudyCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    deal_id: str = Field(..., min_length=1, max_length=128)
    before_ar: str = ""
    before_en: str = ""
    action_ar: str = ""
    action_en: str = ""
    output_ar: str = ""
    output_en: str = ""
    outcome_ar: str = ""
    outcome_en: str = ""
    learning_ar: str = ""
    learning_en: str = ""
    next_steps_ar: str = ""
    next_steps_en: str = ""


# ────────────────────────── campaigns ────────────────────────────────


@router.get("/campaigns")
async def list_campaigns(
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> dict[str, Any]:
    st = get_revenue_marketing_store()
    rows = st.list_campaigns(limit=limit)
    return {
        "count": len(rows),
        "items": [r.model_dump(mode="json") for r in rows],
    }


@router.post("/campaigns")
async def create_campaign(body: CampaignCreatePayload) -> dict[str, Any]:
    st = get_revenue_marketing_store()
    camp = MarketingCampaign(
        id=uid("camp"),
        campaign_name=body.campaign_name,
        target_segment=body.target_segment,
        offer_id=body.offer_id,
        channel=body.channel,
        message_angle=body.message_angle,
        budget_sar=body.budget_sar,
        success_metric=body.success_metric,
        scale_kill_rule=body.scale_kill_rule,
        tracking_url_pattern=body.tracking_url_pattern,
        status="draft",
    )
    missing = validate_campaign(camp)
    if missing:
        raise HTTPException(
            status_code=422,
            detail={"error": "campaign_validation_failed", "missing": missing},
        )
    st.upsert_campaign(camp)
    _log_evidence(
        event_type="revenue_marketing_campaign_created",
        summary=f"campaign={camp.campaign_name} channel={camp.channel}",
        entity_id=camp.id,
    )
    return {"item": camp.model_dump(mode="json")}


@router.patch("/campaigns/{campaign_id}/status")
async def patch_campaign_status(
    campaign_id: Annotated[str, Path(min_length=1, max_length=64)],
    body: CampaignStatusPatchPayload,
) -> dict[str, Any]:
    st = get_revenue_marketing_store()
    hit = next((c for c in st.list_campaigns(limit=10_000) if c.id == campaign_id), None)
    if hit is None:
        raise HTTPException(status_code=404, detail="campaign_not_found")
    allowed = _ALLOWED_TRANSITIONS.get(hit.status, set())
    if body.status not in allowed:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_status_transition",
                "from": hit.status,
                "to": body.status,
            },
        )
    updated = hit.model_copy(update={"status": body.status})
    if body.status == "active":
        missing = validate_campaign(updated)
        if missing:
            raise HTTPException(
                status_code=422,
                detail={"error": "campaign_validation_failed", "missing": missing},
            )
    st.upsert_campaign(updated)
    _log_evidence(
        event_type="revenue_marketing_campaign_status_changed",
        summary=f"id={campaign_id} from={hit.status} to={body.status}",
        entity_id=campaign_id,
    )
    return {"item": updated.model_dump(mode="json")}


# ────────────────────────── offers ───────────────────────────────────


@router.get("/offers")
async def list_offers(
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> dict[str, Any]:
    st = get_revenue_marketing_store()
    st.ensure_seed_loaded()
    rows = st.list_offers(limit=limit)
    return {
        "count": len(rows),
        "items": [r.model_dump(mode="json") for r in rows],
    }


@router.post("/offers")
async def create_offer(body: OfferCreatePayload) -> dict[str, Any]:
    st = get_revenue_marketing_store()
    offer = Offer(
        id=uid("off"),
        name_ar=body.name_ar,
        name_en=body.name_en,
        rung=body.rung,
        price_min_sar=body.price_min_sar,
        price_max_sar=body.price_max_sar,
        target_segment=body.target_segment,
        pain_addressed=body.pain_addressed,
        deliverables_ar=body.deliverables_ar,
        deliverables_en=body.deliverables_en,
        success_metric=body.success_metric,
        scale_kill_rule=body.scale_kill_rule,
    )
    st.upsert_offer(offer)
    _log_evidence(
        event_type="revenue_marketing_offer_created",
        summary=f"offer={offer.name_en} rung={offer.rung}",
        entity_id=offer.id,
    )
    return {"item": offer.model_dump(mode="json")}


# ────────────────────────── messages ─────────────────────────────────


@router.get("/messages")
async def list_messages(
    limit: Annotated[int, Query(ge=1, le=500)] = 200,
) -> dict[str, Any]:
    st = get_revenue_marketing_store()
    st.ensure_seed_loaded()
    rows = st.list_messages(limit=limit)
    return {
        "count": len(rows),
        "items": [r.model_dump(mode="json") for r in rows],
    }


@router.post("/messages")
async def create_message(body: MessageCreatePayload) -> dict[str, Any]:
    st = get_revenue_marketing_store()
    msg = MessageVariant(
        id=uid("msg"),
        offer_id=body.offer_id,
        angle=body.angle,
        headline_ar=body.headline_ar,
        headline_en=body.headline_en,
        body_ar=body.body_ar,
        body_en=body.body_en,
        cta_ar=body.cta_ar,
        cta_en=body.cta_en,
        status="draft",
    )
    st.upsert_message(msg)
    _log_evidence(
        event_type="revenue_marketing_message_created",
        summary=f"offer_id={msg.offer_id} angle={msg.angle}",
        entity_id=msg.id,
    )
    return {"item": msg.model_dump(mode="json")}


# ────────────────────────── touches ──────────────────────────────────


@router.post("/touches")
async def create_touch(body: TouchCreatePayload) -> dict[str, Any]:
    st = get_revenue_marketing_store()
    touch = MarketingTouch(
        id=uid("tch"),
        campaign_id=body.campaign_id,
        lead_id=body.lead_id,
        touch_type=body.touch_type,
        channel=body.channel,
        content_id=body.content_id,
        message_variant=body.message_variant,
    )
    st.append_touch(touch)
    _log_evidence(
        event_type="revenue_marketing_touch_recorded",
        summary=f"channel={touch.channel} type={touch.touch_type}",
        entity_id=touch.id,
    )
    return {"item": touch.model_dump(mode="json")}


# ────────────────────────── attribution ──────────────────────────────


@router.post("/attribution")
async def post_attribution(body: AttributionCreatePayload) -> dict[str, Any]:
    try:
        attr = record_attribution(
            deal_id=body.deal_id,
            revenue_sar=body.revenue_sar,
            sources={
                "campaign_id": body.campaign_id,
                "offer_id": body.offer_id,
                "channel": body.channel,
                "asset_id": body.asset_id,
                "agent_id": body.agent_id,
            },
            payment_received=body.payment_received,
            signed_agreement=body.signed_agreement,
            attribution_type=body.attribution_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    _log_evidence(
        event_type="revenue_marketing_attribution_recorded",
        summary=(f"deal={attr.deal_id} sar={attr.revenue_sar} real={attr.is_real_revenue}"),
        entity_id=attr.id,
    )
    return {"item": attr.model_dump(mode="json")}


@router.get("/attribution/by/{dim}")
async def get_revenue_by_dimension(
    dim: Annotated[str, Path(min_length=1, max_length=32)],
) -> dict[str, Any]:
    if dim not in ("channel", "campaign", "offer", "asset", "agent"):
        raise HTTPException(status_code=400, detail="invalid_dimension")
    typed_dim: AttrDimension = dim  # type: ignore[assignment]
    return {"dimension": dim, "totals_sar": revenue_by_dimension(typed_dim)}


@router.get("/attribution/deal/{deal_id}/chain")
async def get_attribution_chain(
    deal_id: Annotated[str, Path(min_length=1, max_length=128)],
) -> dict[str, Any]:
    chain = attribution_chain_for_deal(deal_id)
    return {"deal_id": deal_id, "chain": chain, "count": len(chain)}


# ────────────────────────── leads ────────────────────────────────────


@router.post("/leads/score")
async def post_lead_score(body: LeadScorePayload) -> dict[str, Any]:
    score = compute_lead_score(
        body.icp_fit,
        body.pain,
        body.ability_to_pay,
        body.urgency,
        body.partner_potential,
        body.trust_fit,
    )
    return {
        "score": score,
        "components": body.model_dump(),
        "weights": {
            "icp_fit": 0.25,
            "pain": 0.20,
            "ability_to_pay": 0.20,
            "urgency": 0.15,
            "partner_potential": 0.10,
            "trust_fit": 0.10,
        },
    }


# ────────────────────────── experiments ──────────────────────────────


@router.post("/experiments")
async def post_experiment(body: ExperimentCreatePayload) -> dict[str, Any]:
    try:
        exp = create_experiment(
            experiment_name=body.experiment_name,
            target_segment=body.target_segment,
            offer_id=body.offer_id,
            variable_tested=body.variable_tested,
            variant_a=body.variant_a,
            variant_b=body.variant_b,
            success_metric=body.success_metric,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    _log_evidence(
        event_type="revenue_marketing_experiment_created",
        summary=f"name={exp.experiment_name} offer={exp.offer_id}",
        entity_id=exp.id,
    )
    return {"item": exp.model_dump(mode="json")}


@router.post("/experiments/{experiment_id}/result")
async def post_experiment_result(
    experiment_id: Annotated[str, Path(min_length=1, max_length=64)],
    body: ExperimentResultPayload,
) -> dict[str, Any]:
    try:
        exp = record_result(experiment_id, body.variant, body.value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    _log_evidence(
        event_type="revenue_marketing_experiment_result_recorded",
        summary=f"id={experiment_id} variant={body.variant} value={body.value}",
        entity_id=experiment_id,
    )
    return {"item": exp.model_dump(mode="json")}


@router.post("/experiments/{experiment_id}/decide")
async def post_experiment_decide(
    experiment_id: Annotated[str, Path(min_length=1, max_length=64)],
) -> dict[str, Any]:
    try:
        decision = decide(experiment_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    _log_evidence(
        event_type="revenue_marketing_experiment_decided",
        summary=f"id={experiment_id} decision={decision}",
        entity_id=experiment_id,
    )
    return {"decision": decision, "experiment_id": experiment_id}


# ────────────────────────── portfolio / graph / dashboard ────────────


@router.get("/portfolio")
async def get_portfolio() -> dict[str, Any]:
    return portfolio_health()


@router.get("/graph")
async def get_graph() -> dict[str, Any]:
    g = build_graph()
    return {"nodes": g["nodes"], "edges": g["edges"]}


@router.get("/dashboard")
async def get_dashboard() -> dict[str, Any]:
    return dashboard_snapshot()


# ────────────────────────── agents ───────────────────────────────────


@router.post("/agents/{agent_name}/propose")
async def post_agent_propose(
    agent_name: Annotated[str, Path(min_length=1, max_length=64)],
    body: AgentProposePayload,
) -> dict[str, Any]:
    if agent_name not in MARKETING_AGENTS:
        raise HTTPException(status_code=404, detail="agent_not_registered")
    try:
        draft = propose_via_agent(agent_name, body.payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return draft


# ────────────────────────── case studies ─────────────────────────────


@router.post("/case-study")
async def post_case_study(body: CaseStudyCreatePayload) -> dict[str, Any]:
    st = get_revenue_marketing_store()
    case = CaseStudyDraft(
        id=uid("cs"),
        deal_id=body.deal_id,
        before_ar=body.before_ar,
        before_en=body.before_en,
        action_ar=body.action_ar,
        action_en=body.action_en,
        output_ar=body.output_ar,
        output_en=body.output_en,
        outcome_ar=body.outcome_ar,
        outcome_en=body.outcome_en,
        learning_ar=body.learning_ar,
        learning_en=body.learning_en,
        next_steps_ar=body.next_steps_ar,
        next_steps_en=body.next_steps_en,
    )
    st.upsert_case_study(case)
    _log_evidence(
        event_type="revenue_marketing_case_study_drafted",
        summary=f"deal={case.deal_id}",
        entity_id=case.id,
    )
    return {
        "item": case.model_dump(mode="json"),
        "draft_only": True,
        "external_send_blocked": True,
        "drafted_at": datetime.now(UTC).isoformat(),
    }
