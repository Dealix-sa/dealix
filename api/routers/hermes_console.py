"""Hermes — Sovereign Console API.

Surfaces the single-pane-of-glass view that Sami opens every morning:
fastest cash action, top opportunity, pending approvals, scale/kill
verdicts, trust + audit state.

All endpoints are admin-gated: Hermes decisions are sovereign artifacts.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from dealix.hermes import ValueOutput
from dealix.hermes.console import render_console
from dealix.hermes.core.opportunities import OpportunityGraph
from dealix.hermes.core.schemas import OpportunityKind, SignalSource
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.sovereignty import Action, SovereigntyLevel

router = APIRouter(prefix="/hermes", tags=["hermes"])


@lru_cache(maxsize=1)
def _orchestrator() -> HermesOrchestrator:
    """Process-wide singleton orchestrator.

    Hermes state is in-memory by design today (Phase 1). Phase 2 swaps the
    backing stores in the orchestrator for durable backends without
    changing this surface.
    """
    return HermesOrchestrator()


def get_orchestrator() -> HermesOrchestrator:
    return _orchestrator()


# ───────────────────────────── Console ─────────────────────────────


@router.get("/console", dependencies=[Depends(require_admin_key)])
def console_snapshot(
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    """Sovereign Console snapshot — Sami's morning view."""
    return render_console(orch)


# ──────────────────────────── Signals ─────────────────────────────


class SignalIn(BaseModel):
    source: SignalSource
    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1, max_length=2000)
    captured_by: str
    tags: list[str] = Field(default_factory=list)
    raw_payload: dict[str, Any] = Field(default_factory=dict)


@router.post("/signals", dependencies=[Depends(require_admin_key)])
def capture_signal(
    body: SignalIn,
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    s = orch.intake.capture(
        source=body.source,
        title=body.title,
        summary=body.summary,
        captured_by=body.captured_by,
        raw_payload=body.raw_payload,
        tags=body.tags,
    )
    return {"signal_id": s.signal_id, "captured_at": s.captured_at.isoformat()}


@router.get("/signals", dependencies=[Depends(require_admin_key)])
def list_signals(
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    return {
        "count": len(orch.intake),
        "items": [s.model_dump() for s in orch.intake.all()],
    }


# ────────────────────────── Opportunities ─────────────────────────


class OpportunityIn(BaseModel):
    source_signal_ids: list[str] = Field(min_length=1)
    kind: OpportunityKind
    title: str
    buyer_segment: str
    estimated_value_sar: float = Field(ge=0)
    close_probability: float = Field(ge=0.0, le=1.0)
    fit_score: float = Field(ge=0.0, le=1.0)
    urgency_score: float = Field(ge=0.0, le=1.0)
    risk_score: float = Field(ge=0.0, le=1.0)
    proposed_value_outputs: list[ValueOutput] = Field(min_length=1)
    notes: str = ""


@router.post("/opportunities", dependencies=[Depends(require_admin_key)])
def register_opportunity(
    body: OpportunityIn,
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    signals = [orch.intake.get(sid) for sid in body.source_signal_ids]
    if any(s is None for s in signals):
        raise HTTPException(status_code=404, detail="one or more signals not found")
    opp = orch.opportunities.register(
        source_signals=[s for s in signals if s is not None],
        kind=body.kind,
        title=body.title,
        buyer_segment=body.buyer_segment,
        estimated_value_sar=body.estimated_value_sar,
        close_probability=body.close_probability,
        fit_score=body.fit_score,
        urgency_score=body.urgency_score,
        risk_score=body.risk_score,
        proposed_value_outputs=body.proposed_value_outputs,
        notes=body.notes,
    )
    return opp.model_dump()


@router.get("/opportunities/top", dependencies=[Depends(require_admin_key)])
def top_opportunities(
    n: int = 10,
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    return {"items": [o.model_dump() for o in orch.opportunities.top(n=n)]}


# ───────────────────────────── Money ──────────────────────────────


@router.get("/money/dashboard", dependencies=[Depends(require_admin_key)])
def money_dashboard(
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    from dealix.hermes.money.dashboard import render

    d = render(scout=orch.cash_scout, outcomes=orch.outcomes, open_proposals=0)
    return {
        "pipeline_value_sar": d.pipeline_value_sar,
        "cash_collected_sar": d.cash_collected_sar,
        "pipeline_to_paid_ratio": d.pipeline_to_paid_ratio,
        "open_proposals": d.open_proposals,
        "fastest_cash": [
            {
                "opportunity_id": a.opportunity_id,
                "title": a.title,
                "kind": a.kind.value,
                "expected_value_sar": round(a.expected_value_sar, 2),
                "priority": round(a.priority, 2),
                "days_to_close": round(a.days_to_close, 1),
                "next_action": a.next_action,
            }
            for a in d.fastest_cash
        ],
    }


# ───────────────────────────── Offers ─────────────────────────────


@router.get("/offers", dependencies=[Depends(require_admin_key)])
def list_offers(
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    return {"items": [o.model_dump() for o in orch.offers.active()]}


# ─────────────────────────── Sovereignty ──────────────────────────


class ProposeActionIn(BaseModel):
    action_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    proposed_by: str
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.S0_AUTONOMOUS
    risk_level: float = Field(ge=0.0, le=1.0, default=0.0)
    expected_value_sar: float = 0.0
    expected_outcome: str = ""


@router.post("/sovereignty/propose", dependencies=[Depends(require_admin_key)])
def propose_action(
    body: ProposeActionIn,
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    action = Action(
        action_type=body.action_type,
        payload=body.payload,
        proposed_by=body.proposed_by,
        sovereignty_level=body.sovereignty_level,
        risk_level=body.risk_level,
        expected_value_sar=body.expected_value_sar,
        expected_outcome=body.expected_outcome,
    )
    decision, req = orch.propose(action)
    return {
        "action_id": action.action_id,
        "verdict": decision.verdict.value,
        "enforced_level": decision.enforced_level.value,
        "reason": decision.reason,
        "approval_required": decision.approval_required,
        "memo_required": decision.memo_required,
        "approval_request_id": req.request_id if req else None,
    }


class ApprovalDecisionIn(BaseModel):
    granted: bool
    approver: str
    note: str = ""


@router.post(
    "/sovereignty/approvals/{request_id}/decide",
    dependencies=[Depends(require_admin_key)],
)
def decide_approval(
    request_id: str,
    body: ApprovalDecisionIn,
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    try:
        req = orch.decide_approval(
            request_id, granted=body.granted, approver=body.approver, note=body.note
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="approval request not found")
    return {
        "request_id": req.request_id,
        "status": req.status.value,
        "approver": req.approver,
        "decided_at": req.decided_at.isoformat() if req.decided_at else None,
    }


@router.get(
    "/sovereignty/approvals/pending",
    dependencies=[Depends(require_admin_key)],
)
def list_pending_approvals(
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    return {
        "items": [
            {
                "request_id": r.request_id,
                "action_id": r.action.action_id,
                "action_type": r.action.action_type,
                "enforced_level": r.decision.enforced_level.value,
                "reason": r.decision.reason,
                "created_at": r.created_at.isoformat(),
                "expires_at": r.expires_at.isoformat(),
            }
            for r in orch.approvals.pending()
        ]
    }


# ─────────────────────────────── Trust ────────────────────────────


@router.get("/trust/agents", dependencies=[Depends(require_admin_key)])
def list_agents(
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    return {"items": [c.model_dump() for c in orch.agents.all()]}


@router.get("/trust/tools", dependencies=[Depends(require_admin_key)])
def list_tools(
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    return {"items": [t.model_dump() for t in orch.tools.all()]}


class PermissionCheckIn(BaseModel):
    agent_id: str
    tool_id: str


@router.post("/trust/permissions/check", dependencies=[Depends(require_admin_key)])
def check_permission(
    body: PermissionCheckIn,
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    v = orch.permissions.check(agent_id=body.agent_id, tool_id=body.tool_id)
    return {
        "allowed": v.allowed,
        "reason": v.reason,
        "enforced_level": v.enforced_level.value,
    }


@router.get("/trust/audit", dependencies=[Depends(require_admin_key)])
def audit_tail(
    limit: int = 50,
    orch: HermesOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    entries = orch.audit.all()[-limit:]
    return {
        "chain_valid": orch.audit.verify_chain(),
        "count": len(entries),
        "items": [
            {
                "entry_id": e.entry_id,
                "event_type": e.event_type,
                "actor": e.actor,
                "payload": e.payload,
                "recorded_at": e.recorded_at.isoformat(),
                "prev_hash": e.prev_hash,
                "entry_hash": e.entry_hash,
            }
            for e in entries
        ],
    }


# ────────────────────────────── MCP risk ──────────────────────────


@router.post("/trust/mcp/score", dependencies=[Depends(require_admin_key)])
def mcp_risk_score(
    metadata: dict[str, Any] = Body(...),
) -> dict[str, Any]:
    from dealix.hermes.trust.mcp_security import metadata_hash, score_metadata

    findings = score_metadata(metadata)
    return {
        "findings": [f.__dict__ for f in findings],
        "metadata_hash": metadata_hash(metadata),
        "blocked": any(f.severity == "block" for f in findings),
    }


__all__ = ["router", "get_orchestrator"]
