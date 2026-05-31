"""
Sovereign Value Control Plane router — §81–§110.

Exposes the SovereignControlPlane facade over HTTP at
``/api/v1/sovereign/*``. Pydantic v2 request/response models are
declared inline; all I/O delegates to the in-memory facade.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from dealix.sovereign_control_plane import get_control_plane
from dealix.sovereign_control_plane.assets import Asset
from dealix.sovereign_control_plane.offers import Offer, OfferGateError
from dealix.sovereign_control_plane.types import OfferState, SecurityMode

router = APIRouter(
    prefix="/api/v1/sovereign",
    tags=["sovereign-control-plane"],
    dependencies=[Depends(require_admin_key)],
)


# ─── Pydantic models ─────────────────────────────────────────────
class SignalIn(BaseModel):
    opportunity_id: str | None = None
    workspace_kind: str = "DEALIX_INTERNAL"
    action_type: str = "internal"
    agent_id: str = "hermes"
    engine: str = "value_engine_os"
    risk_level: str = "low"
    payload: dict[str, Any] = Field(default_factory=dict)
    tools_requested: list[str] = Field(default_factory=list)
    summary: str = "hermes routing"


class ApprovalActionIn(BaseModel):
    approver_id: str
    reason: str | None = None
    notes: str | None = None


class OfferIn(BaseModel):
    name: str
    buyer: str
    pain: str
    promise: str
    deliverables: list[str]
    price_sar: float
    metric: str
    upsell: str
    trust_risks: list[str]


class OfferTransitionIn(BaseModel):
    new_state: str


class AssetIn(BaseModel):
    kind: str
    title: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_by: str
    tags: list[str] = Field(default_factory=list)


class AssetReuseIn(BaseModel):
    revenue_attributed: float = 0.0


class SecurityModeIn(BaseModel):
    mode: str
    actor_id: str
    reason: str = ""


# ─── Health / events / signals ──────────────────────────────────
@router.get("/health")
def health() -> dict[str, Any]:
    return get_control_plane().health()


@router.get("/events")
def events(limit: int = Query(100, ge=1, le=10_000)) -> dict[str, Any]:
    cp = get_control_plane()
    return {"events": [e.to_dict() for e in cp.events_tail(limit)]}


@router.post("/signals")
def submit_signal(signal: SignalIn) -> dict[str, Any]:
    plan = get_control_plane().submit_signal(signal.model_dump())
    return plan.to_dict()


# ─── Approvals ──────────────────────────────────────────────────
@router.get("/approvals/pending")
def list_pending(workspace_id: str | None = None) -> dict[str, Any]:
    cp = get_control_plane()
    return {"items": [a.to_dict() for a in cp.pending_approvals(workspace_id)]}


def _get_approval_or_404(approval_id: str):
    cp = get_control_plane()
    req = cp.approvals.get(approval_id)
    if req is None:
        raise HTTPException(status_code=404, detail="approval not found")
    return cp, req


@router.post("/approvals/{approval_id}/approve")
def approve(approval_id: str, body: ApprovalActionIn) -> dict[str, Any]:
    cp, _ = _get_approval_or_404(approval_id)
    return cp.approvals.approve(approval_id, body.approver_id).to_dict()


@router.post("/approvals/{approval_id}/deny")
def deny(approval_id: str, body: ApprovalActionIn) -> dict[str, Any]:
    if not body.reason:
        raise HTTPException(status_code=400, detail="reason required")
    cp, _ = _get_approval_or_404(approval_id)
    return cp.approvals.deny(approval_id, body.approver_id, body.reason).to_dict()


@router.post("/approvals/{approval_id}/changes")
def request_changes(approval_id: str, body: ApprovalActionIn) -> dict[str, Any]:
    if not body.notes:
        raise HTTPException(status_code=400, detail="notes required")
    cp, _ = _get_approval_or_404(approval_id)
    return cp.approvals.request_changes(
        approval_id, body.approver_id, body.notes
    ).to_dict()


@router.post("/approvals/{approval_id}/kill")
def kill(approval_id: str) -> dict[str, Any]:
    cp, _ = _get_approval_or_404(approval_id)
    return cp.approvals.kill(approval_id).to_dict()


# ─── Money command ──────────────────────────────────────────────
@router.get("/money/snapshot")
def money_snapshot() -> dict[str, Any]:
    return get_control_plane().money()


@router.get("/money/best-next-action")
def money_best_next_action() -> dict[str, Any]:
    best = get_control_plane().money_command.best_next_action()
    return {"best_next_action": best}


# ─── Offers ─────────────────────────────────────────────────────
@router.post("/offers")
def create_offer(body: OfferIn) -> dict[str, Any]:
    try:
        offer = Offer(offer_id="", **body.model_dump())
        return get_control_plane().offer_registry.register(offer).to_dict()
    except OfferGateError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@router.get("/offers")
def list_offers() -> dict[str, Any]:
    return {"items": [o.to_dict() for o in get_control_plane().offers()]}


@router.post("/offers/{offer_id}/transition")
def transition_offer(offer_id: str, body: OfferTransitionIn) -> dict[str, Any]:
    try:
        offer = get_control_plane().offer_registry.transition(
            offer_id, OfferState(body.new_state)
        )
        return offer.to_dict()
    except KeyError:
        raise HTTPException(status_code=404, detail="offer not found")
    except (OfferGateError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc))


# ─── Assets ─────────────────────────────────────────────────────
@router.post("/assets")
def create_asset(body: AssetIn) -> dict[str, Any]:
    asset = get_control_plane().asset_library.register(**body.model_dump())
    return asset.to_dict()


@router.get("/assets")
def list_assets() -> dict[str, Any]:
    return {"items": [a.to_dict() for a in get_control_plane().assets()]}


@router.post("/assets/{asset_id}/reuse")
def reuse_asset(asset_id: str, body: AssetReuseIn) -> dict[str, Any]:
    try:
        return get_control_plane().asset_library.mark_reused(
            asset_id, body.revenue_attributed,
        ).to_dict()
    except KeyError:
        raise HTTPException(status_code=404, detail="asset not found")


# ─── Incidents / security / readiness ──────────────────────────
@router.get("/incidents")
def incidents() -> dict[str, Any]:
    return {"items": [i.to_dict() for i in get_control_plane().incidents_list()]}


@router.post("/security-mode")
def set_security_mode(body: SecurityModeIn) -> dict[str, Any]:
    try:
        return get_control_plane().set_security_mode(
            SecurityMode(body.mode), body.actor_id,
        )
    except (PermissionError, ValueError) as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@router.get("/readiness/public-api")
def public_api_readiness() -> dict[str, Any]:
    ready, missing = get_control_plane().public_api.assess()
    return {"ready": ready, "missing": missing}


@router.get("/readiness/marketplace")
def marketplace_readiness() -> dict[str, Any]:
    ready, missing = get_control_plane().marketplace.assess()
    return {"ready": ready, "missing": missing}


# ─── Graph / loops ──────────────────────────────────────────────
@router.get("/graph/insights")
def graph_insights() -> dict[str, Any]:
    g = get_control_plane().intelligence
    return {
        "best_sector": g.best_sector(),
        "best_message": g.best_message(),
        "most_profitable_offer": g.most_profitable_offer(),
        "best_partner": g.best_partner(),
        "revenue_producing_agents": g.revenue_producing_agents(),
        "risky_tools": g.risky_tools(),
        "recurring_objections": g.recurring_objections(),
        "accepted_prices": g.accepted_prices(),
    }


@router.get("/customers/{customer_id}/value-report")
def customer_value_report(customer_id: str) -> dict[str, Any]:
    try:
        return get_control_plane().customers.monthly_value_report(customer_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="customer not found")


@router.get("/partners/{partner_id}/performance")
def partner_performance(partner_id: str) -> dict[str, Any]:
    cp = get_control_plane()
    if cp.partners.get(partner_id) is None:
        raise HTTPException(status_code=404, detail="partner not found")
    return cp.partners.performance_review(partner_id)


@router.get("/ventures/{venture_id}/recommendation")
def venture_recommendation(venture_id: str) -> dict[str, Any]:
    cp = get_control_plane()
    if cp.ventures.get(venture_id) is None:
        raise HTTPException(status_code=404, detail="venture not found")
    return {"recommendation": cp.ventures.recommend_action(venture_id)}
