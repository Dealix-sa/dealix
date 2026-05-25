"""Revenue Marketing Engine API surface.

Mounted at /api/v1/revenue-marketing/*. Admin-gated by default — nothing
here triggers external sends. Approval/queue is delegated to the existing
Marketing Factory router (/api/v1/ops-autopilot/marketing/*).
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from api.security.api_key import require_admin_key
from dealix.revenue_marketing.attribution import (
    attribute_revenue,
    attribution_dashboard,
    influenced_assets,
    money_quality_score,
)
from dealix.revenue_marketing.experiments import (
    decide_experiment,
    experiment_card,
    experiments_summary,
    record_observation,
)
from dealix.revenue_marketing.funnel import (
    bottleneck_diagnosis,
    funnel_conversion_rates,
    latest_funnel_dashboard,
)
from dealix.revenue_marketing.lead_scoring import revenue_marketing_lead_score
from dealix.revenue_marketing.loop import (
    run_marketing_loop,
    signal_to_offer_recommendations,
)
from dealix.revenue_marketing.offer_ladder import (
    ladder_offer_by_id,
    next_rung_upsell,
    offer_ladder_catalog,
)
from dealix.revenue_marketing.portfolio import portfolio_dashboard
from dealix.revenue_marketing.quality_gates import (
    anti_vanity_review,
    campaign_quality_gate,
    content_quality_gate,
)
from dealix.revenue_marketing.schemas import (
    AttributionType,
    CampaignRecord,
    ContentCardRecord,
    FunnelSnapshotRecord,
    MarketingTouchRecord,
    MarketSignalRecord,
)
from dealix.revenue_marketing.store import get_revenue_marketing_store, uid
from dealix.revenue_ops_autopilot.schemas import EvidenceEvent
from dealix.revenue_ops_autopilot.store import (
    get_autopilot_store,
    uid as ev_uid,
)

router = APIRouter(
    prefix="/api/v1/revenue-marketing",
    tags=["revenue-marketing-engine"],
    dependencies=[Depends(require_admin_key)],
)


def _log_evidence(*, event_type: str, summary: str, entity_id: str = "") -> None:
    get_autopilot_store().append_evidence(
        EvidenceEvent(
            id=ev_uid("ev"),
            event_type=event_type,
            entity_type="revenue_marketing",
            entity_id=entity_id,
            source="revenue_marketing_engine",
            summary=summary,
        ),
    )


# ── Doctrine + catalog ──────────────────────────────────────────────


@router.get("/doctrine")
async def doctrine() -> dict[str, Any]:
    return {
        "name": "Dealix Revenue Marketing Engine",
        "loop": [
            "signal", "segment", "pain", "offer", "message", "channel",
            "lead", "deal", "revenue", "outcome", "learning", "asset",
            "scale_or_kill",
        ],
        "anti_vanity_rule": "Vanity metric بدون conversion = noise.",
        "money_quality_inputs": [
            "margin", "repeatability", "low_delivery_effort",
            "upsell_potential", "data_moat", "partner_potential", "risk (subtract)",
        ],
        "hard_gates": {
            "no_campaign_without_offer": True,
            "no_offer_without_price_range": True,
            "no_lead_without_source": True,
            "no_deal_without_attribution": True,
            "no_revenue_without_outcome": True,
            "no_outcome_without_learning": True,
            "no_external_send": True,
        },
        "ar_summary": (
            "Dealix لا يسوّق ليظهر؛ يسوّق ليحوّل إشارات السوق إلى فرص، "
            "الفرص إلى عروض، العروض إلى صفقات، الصفقات إلى دخل حقيقي، "
            "والدخل إلى بيانات وأصول تزيد قوة النظام كل أسبوع."
        ),
    }


@router.get("/stats")
async def stats() -> dict[str, Any]:
    st = get_revenue_marketing_store()
    return {"counts": st.stats(), "store_path": str(st._path)}


# ── Offer ladder ────────────────────────────────────────────────────


@router.get("/offers/ladder")
async def offers_ladder() -> dict[str, Any]:
    return offer_ladder_catalog()


@router.get("/offers/{offer_id}")
async def get_offer(offer_id: str) -> dict[str, Any]:
    offer = ladder_offer_by_id(offer_id)
    if offer is None:
        raise HTTPException(status_code=404, detail="offer_not_found")
    return offer.model_dump(mode="json")


@router.get("/offers/{offer_id}/upsell-suggestion")
async def offer_upsell(offer_id: str) -> dict[str, Any]:
    suggestion = next_rung_upsell(offer_id)
    return {
        "offer_id": offer_id,
        "next_rung": suggestion.model_dump(mode="json") if suggestion else None,
    }


# ── Signals + loop ──────────────────────────────────────────────────


@router.get("/signals")
async def list_signals() -> dict[str, Any]:
    sigs = get_revenue_marketing_store().list_signals()
    return {"count": len(sigs), "signals": [s.model_dump(mode="json") for s in sigs]}


@router.post("/signals")
async def create_signal(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    payload = {**payload}
    payload.setdefault("id", uid("sig"))
    sig = MarketSignalRecord(**payload)
    rec = get_revenue_marketing_store().append_signal(sig)
    _log_evidence(
        event_type="signal_captured",
        summary=f"signal {sig.id} segment={sig.segment} offer={sig.suggested_offer_id}",
        entity_id=sig.id,
    )
    return rec.model_dump(mode="json")


@router.get("/signals/recommendations")
async def signal_recommendations() -> dict[str, Any]:
    return {"recommendations": signal_to_offer_recommendations()}


@router.post("/loop/run")
async def loop_run(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    try:
        result = run_marketing_loop(
            signal_id=str(payload.get("signal_id") or ""),
            channel_override=payload.get("channel_override"),
            success_metric=payload.get("success_metric", "qualified_calls_booked"),
            scale_kill_rule=payload.get("scale_kill_rule", "scale if reply_rate >= 8% in 7 days, else kill"),
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if "campaign_draft" in result:
        _log_evidence(
            event_type="campaign_drafted",
            summary=f"loop drafted campaign {result['campaign_draft']['id']} from signal {payload.get('signal_id')}",
            entity_id=str(result["campaign_draft"]["id"]),
        )
    return result


# ── Campaigns ───────────────────────────────────────────────────────


@router.get("/campaigns")
async def list_campaigns(
    status: Annotated[str | None, Query()] = None,
) -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_campaigns()
    if status:
        rows = [r for r in rows if r.status == status]
    return {"count": len(rows), "campaigns": [r.model_dump(mode="json") for r in rows]}


@router.post("/campaigns")
async def create_campaign(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    payload = {**payload}
    payload.setdefault("id", uid("cmp"))
    payload.setdefault("status", "draft")
    campaign = CampaignRecord(**payload)
    gate = campaign_quality_gate(campaign)
    rec = get_revenue_marketing_store().upsert_campaign(campaign)
    _log_evidence(
        event_type="campaign_created",
        summary=f"campaign {rec.id} gate_ok={gate['ok']}",
        entity_id=rec.id,
    )
    return {"campaign": rec.model_dump(mode="json"), "quality_gate": gate}


@router.post("/campaigns/{campaign_id}/quality-gate")
async def campaign_gate(campaign_id: str) -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_campaigns()
    target = next((c for c in rows if c.id == campaign_id), None)
    if target is None:
        raise HTTPException(status_code=404, detail="campaign_not_found")
    return campaign_quality_gate(target)


# ── Touches + attribution ───────────────────────────────────────────


@router.post("/touches")
async def record_touch(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    payload = {**payload}
    payload.setdefault("id", uid("tch"))
    t = MarketingTouchRecord(**payload)
    rec = get_revenue_marketing_store().append_touch(t)
    return rec.model_dump(mode="json")


@router.get("/touches/by-lead/{lead_id}")
async def touches_by_lead(lead_id: str) -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_touches(lead_id=lead_id)
    return {
        "lead_id": lead_id,
        "count": len(rows),
        "touches": [r.model_dump(mode="json") for r in rows],
        "influenced": influenced_assets(lead_id=lead_id),
    }


@router.post("/attribution/record")
async def record_attribution(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    deal_id = str(payload.get("deal_id") or "").strip()
    if not deal_id:
        raise HTTPException(status_code=422, detail="deal_id_required")
    if not payload.get("payment_confirmed", True):
        raise HTTPException(
            status_code=422,
            detail="payment_confirmed=False — revenue cannot be attributed (anti-vanity).",
        )
    attr_type: AttributionType = payload.get("attribution_type", "multi_touch")
    try:
        rec = attribute_revenue(
            deal_id=deal_id,
            revenue_sar=float(payload.get("revenue_sar") or 0.0),
            lead_id=payload.get("lead_id"),
            attribution_type=attr_type,
            payment_confirmed=True,
            money_quality=float(payload.get("money_quality") or 0.6),
            primary_source=str(payload.get("primary_source") or ""),
            secondary_source=str(payload.get("secondary_source") or ""),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    _log_evidence(
        event_type="revenue_attributed",
        summary=(
            f"deal {deal_id} revenue {rec.revenue_sar} attr_type={rec.attribution_type} "
            f"channel={rec.channel} offer={rec.offer_id}"
        ),
        entity_id=rec.id,
    )
    return rec.model_dump(mode="json")


@router.get("/attribution/dashboard")
async def attribution_dash() -> dict[str, Any]:
    return attribution_dashboard()


@router.post("/money-quality/score")
async def money_quality_route(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    required = ("margin", "repeatability", "low_delivery_effort", "upsell_potential",
                "data_moat", "partner_potential", "risk")
    missing = [k for k in required if k not in payload]
    if missing:
        raise HTTPException(status_code=422, detail=f"missing_fields: {missing}")
    return money_quality_score(
        margin=float(payload["margin"]),
        repeatability=float(payload["repeatability"]),
        low_delivery_effort=float(payload["low_delivery_effort"]),
        upsell_potential=float(payload["upsell_potential"]),
        data_moat=float(payload["data_moat"]),
        partner_potential=float(payload["partner_potential"]),
        risk=float(payload["risk"]),
    )


# ── Lead scoring ────────────────────────────────────────────────────


@router.post("/leads/score")
async def lead_score(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return revenue_marketing_lead_score(payload)


# ── Experiments ─────────────────────────────────────────────────────


@router.post("/experiments")
async def create_experiment(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    required = ("experiment_name", "target_segment", "offer_id", "variable_tested",
                "variant_a", "variant_b", "success_metric")
    missing = [k for k in required if not payload.get(k)]
    if missing:
        raise HTTPException(status_code=422, detail=f"missing_fields: {missing}")
    rec = experiment_card(
        experiment_name=payload["experiment_name"],
        target_segment=payload["target_segment"],
        offer_id=payload["offer_id"],
        variable_tested=payload["variable_tested"],
        variant_a=payload["variant_a"],
        variant_b=payload["variant_b"],
        success_metric=payload["success_metric"],
        minimum_sample=int(payload.get("minimum_sample") or 50),
        decision_rule=str(payload.get("decision_rule") or "scale variant if 2x conversion vs control"),
    )
    return rec.model_dump(mode="json")


@router.post("/experiments/{experiment_id}/observe")
async def observe_experiment(experiment_id: str, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    try:
        rec = record_observation(
            experiment_id=experiment_id,
            variant=str(payload.get("variant") or ""),
            converted=bool(payload.get("converted") or False),
        )
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return rec.model_dump(mode="json")


@router.post("/experiments/{experiment_id}/decide")
async def decide(experiment_id: str) -> dict[str, Any]:
    try:
        rec = decide_experiment(experiment_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    _log_evidence(
        event_type="experiment_decided",
        summary=f"experiment {rec.id} status={rec.status} decision={rec.decision}",
        entity_id=rec.id,
    )
    return rec.model_dump(mode="json")


@router.get("/experiments/summary")
async def experiments_summary_route() -> dict[str, Any]:
    return experiments_summary()


# ── Funnel ──────────────────────────────────────────────────────────


@router.post("/funnel/snapshot")
async def funnel_snapshot(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    payload = {**payload}
    payload.setdefault("id", uid("fnl"))
    rec = FunnelSnapshotRecord(**payload)
    saved = get_revenue_marketing_store().append_funnel_snapshot(rec)
    return {
        "snapshot": saved.model_dump(mode="json"),
        "rates": funnel_conversion_rates(saved),
        "bottleneck": bottleneck_diagnosis(saved),
    }


@router.get("/funnel/dashboard")
async def funnel_dashboard_route() -> dict[str, Any]:
    return latest_funnel_dashboard()


# ── Content cards ───────────────────────────────────────────────────


@router.get("/content/cards")
async def content_cards() -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_content_cards()
    return {"count": len(rows), "cards": [r.model_dump(mode="json") for r in rows]}


@router.post("/content/cards")
async def content_card_create(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    payload = {**payload}
    payload.setdefault("id", uid("cnt"))
    card = ContentCardRecord(**payload)
    gate = content_quality_gate(card)
    rec = get_revenue_marketing_store().upsert_content_card(card)
    return {"card": rec.model_dump(mode="json"), "quality_gate": gate}


@router.post("/content/anti-vanity-review")
async def anti_vanity_route(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return anti_vanity_review(payload)


# ── Portfolio ───────────────────────────────────────────────────────


@router.get("/portfolio/dashboard")
async def portfolio_route() -> dict[str, Any]:
    return portfolio_dashboard()
