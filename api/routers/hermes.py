"""Hermes API — Universal Sovereign Kernel endpoints.

Exposes the orchestrator over HTTP so the Sovereign Console, the agents,
and integration tests can talk to it without booting a database. All
endpoints are admin-key gated — the kernel is operator infrastructure.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from dealix.hermes.core.schemas import (
    DecisionVerdict,
    MoneyActionSource,
    Outcome,
    OutcomeKind,
    Signal,
    SignalSource,
)
from dealix.hermes.money.cashflow import build_brief as build_cashflow_brief
from dealix.hermes.money.followup import plan_followups
from dealix.hermes.money.pricing import recommend_band
from dealix.hermes.money.proposal_factory import (
    ProposalRequest,
    list_templates,
    render_proposal,
)
from dealix.hermes.money.revenue_hunter import HunterRequest, run_hunter
from dealix.hermes.money.upsell import suggest as suggest_upsell
from dealix.hermes.orchestrator import default_orchestrator
from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.hermes.sovereignty import evaluate as evaluate_sov
from dealix.hermes.trust.guardrails import TrustContext
from dealix.hermes.trust.mcp_security import MCPToolDescriptor
from dealix.hermes.trust.mcp_security import default_registry as mcp_registry

router = APIRouter(
    prefix="/api/v1/hermes",
    tags=["hermes"],
    dependencies=[Depends(require_admin_key)],
)


# ── Request models ────────────────────────────────────────────────────


class CaptureSignalBody(BaseModel):
    source: SignalSource
    sector: str | None = None
    region: str = "SA"
    payload: dict[str, Any] = Field(default_factory=dict)
    raw_text: str | None = None


class DecideBody(BaseModel):
    opportunity_id: str
    verdict: DecisionVerdict
    rationale: str
    next_action: str


class ExecuteBody(BaseModel):
    decision_id: str
    agent_id: str
    tool_id: str | None = None
    artifact: dict[str, Any] = Field(default_factory=dict)


class TrustCheckBody(BaseModel):
    target_id: str
    target_kind: str
    text: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    action: str | None = None
    verified_partners: list[str] = Field(default_factory=list)


class OutcomeBody(BaseModel):
    kind: OutcomeKind
    decision_id: str | None = None
    execution_id: str | None = None
    opportunity_id: str | None = None
    value_sar: float | None = None
    sector: str | None = None
    offer: str | None = None
    notes: str | None = None


class HunterBody(BaseModel):
    sector: str
    region: str = "SA"
    icp: str | None = None
    offer: str = "Revenue Hunter Pilot"
    price_sar: float = 999.0
    message_style: str = "direct"
    leads: list[dict[str, Any]] = Field(default_factory=list)


class ProposalBody(BaseModel):
    template: str
    opportunity_id: str
    client_name: str
    contact: str | None = None
    custom_price_sar: float | None = None
    custom_scope: list[str] = Field(default_factory=list)
    notes: str | None = None


class FollowupBody(BaseModel):
    opportunity_id: str
    client_name: str
    offer: str
    channel: str = "email"


class PriceBandBody(BaseModel):
    opportunity_id: str
    base_price_sar: float


class CashflowBody(BaseModel):
    horizon_days: int = 14
    items: list[dict[str, Any]]


class UpsellBody(BaseModel):
    kind: OutcomeKind
    offer: str | None = None
    sector: str | None = None
    value_sar: float | None = None


class MCPVetBody(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any] = Field(default_factory=dict)
    server: str = "unknown"
    version: str = "0.0.0"


class SovereigntyEvalBody(BaseModel):
    action: str
    agent_max_level: SovereigntyLevel = SovereigntyLevel.L2_INTERNAL_TASK


# ── Signal / Opportunity ──────────────────────────────────────────────


@router.post("/signals/capture", status_code=status.HTTP_201_CREATED)
def capture_signal(body: CaptureSignalBody) -> dict[str, Any]:
    orch = default_orchestrator()
    signal = Signal(
        source=body.source,
        sector=body.sector,
        region=body.region,
        payload=body.payload,
        raw_text=body.raw_text,
    )
    opp = orch.capture_signal(signal)
    return {
        "signal": signal.model_dump(mode="json"),
        "opportunity": opp.model_dump(mode="json"),
    }


@router.get("/opportunities")
def list_opportunities(limit: int = 50) -> dict[str, Any]:
    orch = default_orchestrator()
    items = [o.model_dump(mode="json") for o in orch.opportunities[-limit:]]
    return {"items": items, "count": len(items)}


# ── Decisions / Executions ────────────────────────────────────────────


@router.post("/decisions", status_code=status.HTTP_201_CREATED)
def make_decision(body: DecideBody) -> dict[str, Any]:
    orch = default_orchestrator()
    try:
        decision = orch.decide(
            body.opportunity_id, body.verdict, body.rationale, body.next_action
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return decision.model_dump(mode="json")


@router.post("/executions", status_code=status.HTTP_201_CREATED)
def execute(body: ExecuteBody) -> dict[str, Any]:
    orch = default_orchestrator()
    try:
        exe = orch.execute(
            body.decision_id, body.agent_id, body.tool_id, body.artifact
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return exe.model_dump(mode="json")


@router.post("/decisions/{decision_id}/approve")
def approve(decision_id: str) -> dict[str, Any]:
    orch = default_orchestrator()
    try:
        d = orch.approve(decision_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return d.model_dump(mode="json")


@router.post("/decisions/{decision_id}/reject")
def reject(decision_id: str, reason: str = "no reason given") -> dict[str, Any]:
    orch = default_orchestrator()
    try:
        d = orch.reject(decision_id, reason)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return d.model_dump(mode="json")


# ── Trust ─────────────────────────────────────────────────────────────


@router.post("/trust/check")
def trust_check_endpoint(body: TrustCheckBody) -> dict[str, Any]:
    orch = default_orchestrator()
    result = orch.run_trust_check(
        TrustContext(
            target_id=body.target_id,
            target_kind=body.target_kind,
            text=body.text,
            payload=body.payload,
            action=body.action,
            verified_partners=body.verified_partners,
        )
    )
    return result.model_dump(mode="json")


@router.post("/trust/mcp/vet")
def vet_mcp_tool(body: MCPVetBody) -> dict[str, Any]:
    desc = MCPToolDescriptor(
        name=body.name,
        description=body.description,
        input_schema=body.input_schema,
        server=body.server,
        version=body.version,
    )
    return mcp_registry().allow(desc).to_dict()


@router.get("/trust/registry/snapshot")
def registry_snapshot() -> dict[str, Any]:
    orch = default_orchestrator()
    return {
        "agents": orch.agents.snapshot(),
        "tools": orch.tools.snapshot(),
        "mcp_tools": mcp_registry().snapshot(),
    }


@router.post("/sovereignty/evaluate")
def evaluate_sovereignty_endpoint(body: SovereigntyEvalBody) -> dict[str, Any]:
    result = evaluate_sov(body.action, body.agent_max_level)
    return {
        "allowed": result.allowed,
        "level": result.level.name,
        "requires_approval": result.requires_approval,
        "reason": result.reason,
        "approvers_needed": result.approvers_needed,
    }


# ── Outcomes / Assets ─────────────────────────────────────────────────


@router.post("/outcomes/log", status_code=status.HTTP_201_CREATED)
def log_outcome(body: OutcomeBody) -> dict[str, Any]:
    orch = default_orchestrator()
    outcome = Outcome(
        kind=body.kind,
        decision_id=body.decision_id,
        execution_id=body.execution_id,
        opportunity_id=body.opportunity_id,
        value_sar=body.value_sar,
        sector=body.sector,
        offer=body.offer,
        notes=body.notes,
    )
    out, asset = orch.log_outcome(outcome)
    return {
        "outcome": out.model_dump(mode="json"),
        "asset": asset.model_dump(mode="json"),
    }


@router.get("/assets")
def list_assets(limit: int = 50) -> dict[str, Any]:
    orch = default_orchestrator()
    items = [a.model_dump(mode="json") for a in orch.assets.all()[-limit:]]
    return {"items": items, "count": len(items)}


# ── Money engine endpoints ────────────────────────────────────────────


@router.post("/money/hunter")
def hunter(body: HunterBody) -> dict[str, Any]:
    return run_hunter(
        HunterRequest(
            sector=body.sector,
            region=body.region,
            icp=body.icp,
            offer=body.offer,
            price_sar=body.price_sar,
            message_style=body.message_style,
            leads=body.leads,
        )
    ).to_dict()


@router.post("/money/proposal")
def proposal(body: ProposalBody) -> dict[str, Any]:
    orch = default_orchestrator()
    try:
        opp = next(o for o in orch.opportunities if o.id == body.opportunity_id)
    except StopIteration as exc:
        raise HTTPException(status_code=404, detail="opportunity not found") from exc
    try:
        rendered = render_proposal(
            ProposalRequest(
                template=body.template,
                opportunity=opp,
                client_name=body.client_name,
                contact=body.contact,
                custom_price_sar=body.custom_price_sar,
                custom_scope=body.custom_scope,
                notes=body.notes,
            )
        )
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return rendered.to_dict()


@router.get("/money/proposal/templates")
def proposal_templates() -> dict[str, Any]:
    return {"templates": list_templates()}


@router.post("/money/followup")
def followup(body: FollowupBody) -> dict[str, Any]:
    orch = default_orchestrator()
    try:
        opp = next(o for o in orch.opportunities if o.id == body.opportunity_id)
    except StopIteration as exc:
        raise HTTPException(status_code=404, detail="opportunity not found") from exc
    plan = plan_followups(
        opp, client_name=body.client_name, offer=body.offer, channel=body.channel
    )
    return {
        "opportunity_id": plan.opportunity_id,
        "client_name": plan.client_name,
        "steps": [
            {
                "day_offset": s.day_offset,
                "scheduled_at": s.scheduled_at.isoformat(),
                "channel": s.channel,
                "draft": s.draft,
                "sovereignty_level": s.sovereignty_level.name,
                "requires_approval": s.requires_approval,
                "blocked_reason": s.blocked_reason,
            }
            for s in plan.steps
        ],
    }


@router.post("/money/price-band")
def price_band(body: PriceBandBody) -> dict[str, Any]:
    orch = default_orchestrator()
    try:
        opp = next(o for o in orch.opportunities if o.id == body.opportunity_id)
    except StopIteration as exc:
        raise HTTPException(status_code=404, detail="opportunity not found") from exc
    band = recommend_band(opp, body.base_price_sar)
    return {
        "low_sar": band.low_sar,
        "target_sar": band.target_sar,
        "high_sar": band.high_sar,
        "rationale": band.rationale,
        "requires_approval": band.requires_approval,
    }


@router.post("/money/cashflow")
def cashflow(body: CashflowBody) -> dict[str, Any]:
    return build_cashflow_brief(body.items, horizon_days=body.horizon_days).to_dict()


@router.post("/money/upsell")
def upsell(body: UpsellBody) -> dict[str, Any]:
    outcome = Outcome(
        kind=body.kind,
        offer=body.offer,
        sector=body.sector,
        value_sar=body.value_sar,
    )
    s = suggest_upsell(outcome)
    return {
        "current_offer": s.current_offer,
        "next_offers": s.next_offers,
        "rationale": s.rationale,
        "confidence": s.confidence,
    }


@router.get("/money/dashboard")
def money_dashboard(top_n: int = 5) -> dict[str, Any]:
    orch = default_orchestrator()
    return orch.money_dashboard(top_n=top_n).to_dict()


@router.get("/money/sources")
def money_sources() -> dict[str, Any]:
    return {"sources": [s.value for s in MoneyActionSource]}


# ── Sovereign Console ─────────────────────────────────────────────────


@router.get("/sovereign/brief")
def sovereign_brief(top_n: int = 5) -> dict[str, Any]:
    orch = default_orchestrator()
    return orch.sovereign_brief(top_n=top_n).model_dump(mode="json")


@router.get("/sovereign/console")
def sovereign_console(top_n: int = 5) -> dict[str, Any]:
    """Single payload for the founder console UI."""
    orch = default_orchestrator()
    brief = orch.sovereign_brief(top_n=top_n)
    dash = orch.money_dashboard(top_n=top_n)
    return {
        "brief": brief.model_dump(mode="json"),
        "money_dashboard": dash.to_dict(),
        "agents": orch.agents.snapshot(),
        "tools": orch.tools.snapshot(),
        "counts": {
            "signals": len(orch.signals),
            "opportunities": len(orch.opportunities),
            "decisions": len(orch.decisions),
            "executions": len(orch.executions),
            "outcomes": len(orch.outcomes),
            "assets": len(orch.assets.all()),
        },
    }
