"""
Hermes Universal Kernel — HTTP surface.

Exposes the sovereign pipeline (Signal → Asset) and the trust registries
under ``/api/v1/hermes``. Every external-facing route returns drafts only —
no live external send happens here, by design.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query

from dealix.hermes.core.assets import get_asset_store
from dealix.hermes.core.decisions import get_decision_store
from dealix.hermes.core.executions import get_execution_store
from dealix.hermes.core.opportunities import get_opportunity_store
from dealix.hermes.core.outcomes import get_outcome_store
from dealix.hermes.core.scale import review as review_scale
from dealix.hermes.core.schemas import (
    AssetType,
    OpportunityType,
    OutcomeStatus,
    PermissionLevel,
    RiskLevel,
    SignalType,
    SovereigntyLevel,
)
from dealix.hermes.core.signals import get_signal_store
from dealix.hermes.customer.health_score import CustomerHealthScorer
from dealix.hermes.customer.value_report import ValueReportBuilder
from dealix.hermes.intelligence.market_radar import MarketRadar
from dealix.hermes.intelligence.report_builder import ReportBuilder
from dealix.hermes.money.cash_scout import CashScout
from dealix.hermes.money.cashflow import CashflowBrief
from dealix.hermes.money.dashboard import MoneyDashboard
from dealix.hermes.money.pricing import PricingIntelligence
from dealix.hermes.money.proposal_factory import ProposalFactory
from dealix.hermes.orchestrator import get_orchestrator
from dealix.hermes.partners.fit_score import PartnerFitScorer
from dealix.hermes.products.offer_builder import OfferBuilder, OfferBuildError
from dealix.hermes.products.offer_library import default_offers
from dealix.hermes.sovereignty import (
    S4_SOVEREIGN_ACTIONS,
    S5_NEVER_AUTONOMOUS_ACTIONS,
    classify_action,
    get_sovereign_layer,
)
from dealix.hermes.trust.agent_registry import (
    AgentRegistryError,
    get_agent_registry,
)
from dealix.hermes.trust.approvals import get_approval_center
from dealix.hermes.trust.audit import get_audit_log
from dealix.hermes.trust.evidence import EvidencePackBuilder
from dealix.hermes.trust.incident_response import get_incident_log
from dealix.hermes.trust.mcp_security import MCPReviewer
from dealix.hermes.trust.tool_registry import (
    ToolRegistryError,
    get_tool_registry,
)
from dealix.hermes.ventures.kill_scale import VentureKillScale
from dealix.hermes.ventures.vertical_launcher import VerticalLauncher


router = APIRouter(prefix="/api/v1/hermes", tags=["hermes"])


# ── Status ─────────────────────────────────────────────────────────


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "kernel": "Hermes Universal Kernel",
        "owner": "Sami",
        "sovereignty_levels": [lvl.value for lvl in SovereigntyLevel],
        "s4_sovereign_actions": sorted(S4_SOVEREIGN_ACTIONS),
        "s5_never_autonomous_actions": sorted(S5_NEVER_AUTONOMOUS_ACTIONS),
        "kill_switch_engaged": get_sovereign_layer().kill_switch_engaged,
        "principles": [
            "Every signal → opportunity → outcome → asset.",
            "No external send without approval.",
            "Sovereignty belongs only to Sami.",
        ],
    }


# ── Signals ────────────────────────────────────────────────────────


@router.post("/signals")
async def ingest_signal(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    try:
        sig = get_orchestrator().ingest_signal(
            source=payload["source"],
            signal_type=SignalType(payload["signal_type"]),
            title=payload["title"],
            content=payload.get("content", ""),
            confidence=payload.get("confidence", 0.5),
            raw_payload=payload.get("raw_payload"),
        )
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return sig.model_dump(mode="json")


@router.get("/signals")
async def list_signals(only_unprocessed: bool = False) -> dict[str, Any]:
    items = get_signal_store().list(only_unprocessed=only_unprocessed)
    return {"count": len(items), "items": [s.model_dump(mode="json") for s in items]}


# ── Opportunities ──────────────────────────────────────────────────


@router.post("/opportunities/from-signal/{signal_id}")
async def evaluate_opportunity(signal_id: str, payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    signal = get_signal_store().get(signal_id)
    if signal is None:
        raise HTTPException(status_code=404, detail="signal_not_found")
    opp = get_orchestrator().evaluate_opportunity(
        signal,
        opportunity_type=payload.get("opportunity_type"),
        estimated_value_sar=payload.get("estimated_value_sar", 0.0),
        cash_speed=payload.get("cash_speed", 3),
        strategic=payload.get("strategic", 3),
        repeatability=payload.get("repeatability", 3),
        data_moat=payload.get("data_moat", 3),
        difficulty=payload.get("difficulty", 3),
        risk=payload.get("risk", 2),
        recommended_action=payload.get("recommended_action", ""),
    )
    return opp.model_dump(mode="json")


@router.get("/opportunities")
async def list_opportunities(
    status: str | None = None,
    min_score: float | None = None,
) -> dict[str, Any]:
    items = get_opportunity_store().list(status=status, min_score=min_score)
    return {"count": len(items), "items": [o.model_dump(mode="json") for o in items]}


# ── Decisions ──────────────────────────────────────────────────────


@router.post("/decisions/from-opportunity/{opportunity_id}")
async def propose_decision(opportunity_id: str, payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    opp = get_opportunity_store().get(opportunity_id)
    if opp is None:
        raise HTTPException(status_code=404, detail="opportunity_not_found")
    dec = get_orchestrator().make_decision(
        opp,
        decision_type=payload.get("decision_type", "execute"),
        recommendation=payload.get("recommendation", "Proceed"),
        risk_level=RiskLevel(payload.get("risk_level", "low")),
        options=payload.get("options"),
    )
    return dec.model_dump(mode="json")


@router.post("/decisions/{decision_id}/approve")
async def approve_decision(decision_id: str, approver: str = "Sami") -> dict[str, Any]:
    dec = get_decision_store().approve(decision_id, approver=approver)
    if dec is None:
        raise HTTPException(status_code=404, detail="decision_not_found")
    return dec.model_dump(mode="json")


@router.post("/decisions/{decision_id}/reject")
async def reject_decision(decision_id: str, reason: str = Body(..., embed=True)) -> dict[str, Any]:
    dec = get_decision_store().reject(decision_id, reason)
    if dec is None:
        raise HTTPException(status_code=404, detail="decision_not_found")
    return dec.model_dump(mode="json")


# ── Executions ─────────────────────────────────────────────────────


@router.post("/executions/plan/{decision_id}")
async def plan_execution(decision_id: str, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    dec = get_decision_store().get(decision_id)
    if dec is None:
        raise HTTPException(status_code=404, detail="decision_not_found")
    result = get_orchestrator().plan_execution(
        dec,
        agent_id=payload["agent_id"],
        tool_id=payload["tool_id"],
        action_type=payload["action_type"],
        permission_level=PermissionLevel(payload.get("permission_level", "L1_DRAFT")),
        external_action=payload.get("external_action", False),
        expected_result=payload.get("expected_result", ""),
        payload=payload.get("payload"),
    )
    return result.as_dict()


@router.get("/executions")
async def list_executions(status: str | None = None) -> dict[str, Any]:
    items = get_execution_store().list(status=status)
    return {"count": len(items), "items": [e.model_dump(mode="json") for e in items]}


# ── Outcomes ───────────────────────────────────────────────────────


@router.post("/outcomes/{execution_id}")
async def record_outcome(execution_id: str, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    exe = get_execution_store().get(execution_id)
    if exe is None:
        raise HTTPException(status_code=404, detail="execution_not_found")
    out = get_orchestrator().record_outcome(
        exe,
        status=OutcomeStatus(payload["status"]),
        actual_result=payload.get("actual_result", ""),
        revenue_sar=payload.get("revenue_sar", 0.0),
        learning=payload.get("learning", ""),
    )
    return out.model_dump(mode="json")


@router.get("/outcomes")
async def list_outcomes(status: str | None = None) -> dict[str, Any]:
    items = get_outcome_store().list(status=status)
    return {"count": len(items), "items": [o.model_dump(mode="json") for o in items]}


# ── Assets ─────────────────────────────────────────────────────────


@router.post("/assets/from-outcome/{outcome_id}")
async def register_asset(outcome_id: str, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    out = get_outcome_store().get(outcome_id)
    if out is None:
        raise HTTPException(status_code=404, detail="outcome_not_found")
    asset = get_orchestrator().register_asset(
        out,
        asset_type=AssetType(payload["asset_type"]),
        title=payload["title"],
        description=payload.get("description", ""),
        commercializable=payload.get("commercializable", False),
    )
    return asset.model_dump(mode="json")


@router.get("/assets")
async def list_assets(asset_type: str | None = None, commercializable_only: bool = False) -> dict[str, Any]:
    items = get_asset_store().list(asset_type=asset_type, commercializable_only=commercializable_only)
    return {"count": len(items), "items": [a.model_dump(mode="json") for a in items]}


# ── Pipeline shortcut ──────────────────────────────────────────────


@router.post("/pipeline/run")
async def run_pipeline(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    result = get_orchestrator().run_pipeline(
        source=payload["source"],
        signal_type=SignalType(payload["signal_type"]),
        title=payload["title"],
        content=payload.get("content", ""),
        agent_id=payload.get("agent_id", "revenue_hunter"),
        tool_id=payload.get("tool_id", "draft_message"),
        action_type=payload.get("action_type", "draft_outreach"),
        estimated_value_sar=payload.get("estimated_value_sar", 5_000.0),
    )
    return result.as_dict()


# ── Trust Registry ─────────────────────────────────────────────────


@router.get("/trust/agents")
async def list_agents() -> dict[str, Any]:
    items = get_agent_registry().list()
    return {"count": len(items), "items": [a.model_dump(mode="json") for a in items]}


@router.post("/trust/agents")
async def register_agent(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    try:
        agent = get_agent_registry().register(
            id=payload["id"],
            name=payload["name"],
            mission=payload["mission"],
            domain=payload["domain"],
            owner=payload.get("owner", ""),
            max_sovereignty_level=SovereigntyLevel(
                payload.get("max_sovereignty_level", SovereigntyLevel.S1_INTERNAL.value)
            ),
            allowed_tools=payload.get("allowed_tools", []),
            forbidden_tools=payload.get("forbidden_tools", []),
            kpis=payload.get("kpis", []),
        )
    except AgentRegistryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return agent.model_dump(mode="json")


@router.get("/trust/tools")
async def list_tools() -> dict[str, Any]:
    items = get_tool_registry().list()
    return {"count": len(items), "items": [t.model_dump(mode="json") for t in items]}


@router.post("/trust/tools")
async def register_tool(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    try:
        tool = get_tool_registry().register(
            id=payload["id"],
            name=payload["name"],
            tool_type=payload["tool_type"],
            owner=payload.get("owner", ""),
            risk_level=RiskLevel(payload.get("risk_level", "low")),
            requires_approval=payload.get("requires_approval", True),
            enabled=payload.get("enabled", False),
            data_scope=payload.get("data_scope", "tenant_only"),
            allowed_agents=payload.get("allowed_agents", []),
        )
    except ToolRegistryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return tool.model_dump(mode="json")


@router.get("/trust/approvals")
async def list_approvals(pending_only: bool = True) -> dict[str, Any]:
    center = get_approval_center()
    items = center.pending() if pending_only else center.history()
    return {"count": len(items), "items": [r.model_dump(mode="json") for r in items]}


@router.post("/trust/approvals/{approval_id}/approve")
async def approve(approval_id: str, approver: str = "Sami") -> dict[str, Any]:
    req = get_approval_center().approve(approval_id, approver=approver)
    if req is None:
        raise HTTPException(status_code=400, detail="approval_not_actionable")
    return req.model_dump(mode="json")


@router.post("/trust/approvals/{approval_id}/reject")
async def reject(approval_id: str, reason: str = Body(..., embed=True)) -> dict[str, Any]:
    req = get_approval_center().reject(approval_id, reason)
    if req is None:
        raise HTTPException(status_code=404, detail="approval_not_found")
    return req.model_dump(mode="json")


@router.get("/trust/audit")
async def audit(limit: int = Query(default=200, ge=1, le=1000)) -> dict[str, Any]:
    items = get_audit_log().list(limit=limit)
    return {"count": len(items), "items": [e.model_dump(mode="json") for e in items]}


@router.post("/trust/mcp/review")
async def mcp_review(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    result = MCPReviewer().review(
        server_name=payload.get("server_name", ""),
        owner=payload.get("owner", ""),
        data_scope=payload.get("data_scope", ""),
        tools=payload.get("tools", []),
        s4_approved=payload.get("s4_approved", False),
    )
    return {"approved": result.approved, "reasons": result.reasons}


@router.post("/trust/incidents")
async def report_incident(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    inc = get_incident_log().report(
        title=payload["title"],
        severity=RiskLevel(payload.get("severity", "medium")),
        description=payload.get("description", ""),
        metadata=payload.get("metadata"),
    )
    return inc.model_dump(mode="json")


@router.get("/trust/incidents")
async def list_incidents(open_only: bool = True) -> dict[str, Any]:
    items = get_incident_log().list(open_only=open_only)
    return {"count": len(items), "items": [i.model_dump(mode="json") for i in items]}


# ── Sovereignty ────────────────────────────────────────────────────


@router.get("/sovereignty/classify")
async def classify(action_type: str) -> dict[str, Any]:
    sov = classify_action(action_type)
    return {"action_type": action_type, "sovereignty_level": sov.value}


@router.post("/sovereignty/kill-switch/engage")
async def engage_kill(reason: str = "manual") -> dict[str, Any]:
    get_sovereign_layer().engage_kill_switch(reason)
    return {"kill_switch_engaged": True}


@router.post("/sovereignty/kill-switch/disengage")
async def disengage_kill(reason: str = "manual") -> dict[str, Any]:
    get_sovereign_layer().disengage_kill_switch(reason)
    return {"kill_switch_engaged": False}


# ── Money ──────────────────────────────────────────────────────────


@router.get("/money/dashboard")
async def money_dashboard() -> dict[str, Any]:
    return MoneyDashboard().snapshot().as_dict()


@router.get("/money/cash-scout")
async def cash_scout(top: int = 5) -> dict[str, Any]:
    return {"items": CashScout().fastest_paths(top=top)}


@router.get("/money/cashflow")
async def cashflow() -> dict[str, Any]:
    return CashflowBrief().summary().__dict__


@router.post("/money/pricing")
async def pricing(opportunity_id: str = Body(..., embed=True)) -> dict[str, Any]:
    opp = get_opportunity_store().get(opportunity_id)
    if opp is None:
        raise HTTPException(status_code=404, detail="opportunity_not_found")
    return PricingIntelligence().recommend(opp).__dict__


@router.post("/money/proposal")
async def proposal(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    opp = get_opportunity_store().get(payload["opportunity_id"])
    if opp is None:
        raise HTTPException(status_code=404, detail="opportunity_not_found")
    offer = payload.get("offer") or next(iter(default_offers()), {})
    return ProposalFactory().draft(opp, offer=offer)


# ── Products ───────────────────────────────────────────────────────


@router.get("/products/offers")
async def offers() -> dict[str, Any]:
    items = default_offers()
    return {"count": len(items), "items": items}


@router.post("/products/offers")
async def build_offer(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    try:
        card = OfferBuilder().build(
            offer=payload["offer"],
            buyer=payload["buyer"],
            pain=payload["pain"],
            promise=payload["promise"],
            deliverables=payload["deliverables"],
            price_range_sar=payload["price_range_sar"],
            outcome_metric=payload["outcome_metric"],
            delivery_time=payload.get("delivery_time", ""),
            upsell=payload.get("upsell", ""),
        )
    except (KeyError, OfferBuildError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return card.as_dict()


# ── Partners ───────────────────────────────────────────────────────


@router.post("/partners/fit-score")
async def partner_fit(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    fit = PartnerFitScorer().score(
        partner_name=payload["partner_name"],
        partner_type=payload["partner_type"],
        client_base_score=payload.get("client_base_score", 3),
        sales_capability=payload.get("sales_capability", 3),
        delivery_capability=payload.get("delivery_capability", 3),
        trust_level=payload.get("trust_level", 3),
        sector_fit=payload.get("sector_fit", 3),
        risk_level=payload.get("risk_level", 2),
    )
    return fit.__dict__


# ── Intelligence ───────────────────────────────────────────────────


@router.post("/intelligence/market")
async def market_signal(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    sig = get_orchestrator().ingest_signal(
        source=payload["source"],
        signal_type=SignalType.MARKET,
        title=payload["title"],
        content=payload.get("content", ""),
    )
    out = MarketRadar().process(
        sig,
        sector=payload.get("sector", ""),
        opportunity=payload.get("opportunity", ""),
        recommended_offer=payload.get("recommended_offer", ""),
        target_segments=payload.get("target_segments", []),
    )
    return {
        "signal": sig.model_dump(mode="json"),
        "market_output": out.__dict__,
    }


@router.post("/intelligence/report")
async def market_report(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return ReportBuilder().build(
        title=payload["title"],
        sector=payload.get("sector", ""),
        signals=payload.get("signals", []),
    )


# ── Customer ───────────────────────────────────────────────────────


@router.post("/customer/health")
async def customer_health(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    health = CustomerHealthScorer().score(
        customer_id=payload["customer_id"],
        usage_score=payload.get("usage_score", 3),
        outcome_score=payload.get("outcome_score", 3),
        communication_score=payload.get("communication_score", 3),
        value_score=payload.get("value_score", 3),
    )
    return health.__dict__


@router.post("/customer/value-report")
async def customer_value_report(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return ValueReportBuilder().build(
        customer_id=payload["customer_id"],
        opportunities_count=payload.get("opportunities_count", 0),
        messages_drafted=payload.get("messages_drafted", 0),
        proposals_count=payload.get("proposals_count", 0),
        outcomes_count=payload.get("outcomes_count", 0),
        value_summary=payload.get("value_summary", ""),
        next_plan=payload.get("next_plan", ""),
        recommendation=payload.get("recommendation", ""),
        upsell=payload.get("upsell", ""),
    )


# ── Ventures ───────────────────────────────────────────────────────


@router.post("/ventures/plan")
async def venture_plan(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    test = VerticalLauncher().plan(
        vertical=payload["vertical"],
        buyer=payload["buyer"],
        pain=payload["pain"],
        offer=payload["offer"],
        price=payload.get("price", "TBD"),
        first_50_targets=payload.get("first_50_targets", []),
    )
    return test.__dict__


@router.post("/ventures/evaluate")
async def venture_evaluate(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    test = VerticalLauncher().plan(
        vertical=payload["vertical"],
        buyer=payload.get("buyer", ""),
        pain=payload.get("pain", ""),
        offer=payload.get("offer", ""),
        price=payload.get("price", "TBD"),
    )
    verdict = VentureKillScale().evaluate(
        test,
        replies=payload.get("replies", 0),
        paid_customers=payload.get("paid_customers", 0),
        outreach_count=payload.get("outreach_count", 0),
    )
    return verdict.__dict__


# ── Scale / Kill ───────────────────────────────────────────────────


@router.get("/scale-kill/{opportunity_id}")
async def scale_kill(opportunity_id: str) -> dict[str, Any]:
    opp = get_opportunity_store().get(opportunity_id)
    if opp is None:
        raise HTTPException(status_code=404, detail="opportunity_not_found")
    verdict = review_scale(opp)
    return verdict.__dict__


# ── Evidence packs ─────────────────────────────────────────────────


@router.get("/evidence/{opportunity_id}")
async def evidence_pack(opportunity_id: str) -> dict[str, Any]:
    opp = get_opportunity_store().get(opportunity_id)
    if opp is None:
        raise HTTPException(status_code=404, detail="opportunity_not_found")
    signal = get_signal_store().get(opp.signal_id)
    decisions = [d for d in get_decision_store().list() if d.opportunity_id == opp.id]
    decision = decisions[0] if decisions else None
    execution = None
    outcome = None
    asset = None
    if decision is not None:
        execs = [e for e in get_execution_store().list() if e.decision_id == decision.id]
        execution = execs[0] if execs else None
        if execution is not None:
            outcome = get_outcome_store().for_execution(execution.id)
            if outcome is not None and outcome.asset_id:
                asset = get_asset_store().get(outcome.asset_id)
    pack = EvidencePackBuilder.build(
        title=f"Evidence pack — {opp.title}",
        signal=signal,
        opportunity=opp,
        decision=decision,
        execution=execution,
        outcome=outcome,
        asset=asset,
    )
    return pack.as_dict()
