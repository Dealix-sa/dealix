"""Full Ops Sales System API — /api/v1/full-ops-os.

Founder-facing surface over the FullOpsOrchestrator: start runs, advance
stages, inspect the trace and audit trail, and list the approvals a run
has queued. Every response carries a ``governance_decision`` field.

Distinct from the legacy ``/api/v1/full-ops`` daily-command-center router.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.agent_os import get_agent
from auto_client_acquisition.full_ops_os.agents import FULL_OPS_AGENT_SPECS
from auto_client_acquisition.full_ops_os.orchestrator import FullOpsOrchestrator
from core.logging import get_logger

router = APIRouter(prefix="/api/v1/full-ops-os", tags=["full-ops-os"])
log = get_logger(__name__)

_ORCHESTRATOR: FullOpsOrchestrator | None = None


def get_orchestrator() -> FullOpsOrchestrator:
    """Return the process-scoped orchestrator singleton."""
    global _ORCHESTRATOR
    if _ORCHESTRATOR is None:
        _ORCHESTRATOR = FullOpsOrchestrator()
    return _ORCHESTRATOR


def _run_view(orch: FullOpsOrchestrator, run_id: str) -> dict[str, Any]:
    run = orch.repo.get_run(tenant_id=orch.tenant_id, run_id=run_id)
    return {
        "run_id": run.run_id,
        "workflow_id": run.workflow_id,
        "customer_id": run.customer_id,
        "state": run.state,
        "current_step": run.current_step,
    }


@router.get("/status")
async def status() -> dict[str, Any]:
    """Module status."""
    return {
        "module": "full_ops_os",
        "stages": 12,
        "agents": len(FULL_OPS_AGENT_SPECS),
        "automation": "up_to_approval_gate",
        "governance_decision": "ok",
    }


@router.get("/agents")
async def agents() -> dict[str, Any]:
    """The runtime agent pyramid and its registration state."""
    rows: list[dict[str, Any]] = []
    for spec in FULL_OPS_AGENT_SPECS:
        card = get_agent(spec.agent_id)
        rows.append({
            "agent_id": spec.agent_id,
            "name": spec.name,
            "tier": spec.tier,
            "autonomy_level": int(spec.autonomy_level),
            "registered": card is not None,
            "status": card.status if card is not None else "unregistered",
        })
    return {
        "count": len(rows),
        "agents": rows,
        "governance_decision": "ok",
    }


@router.post("/runs")
async def create_run(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Start a Full Ops workflow run for a lead."""
    customer_id = str(payload.get("customer_id", "")).strip()
    if not customer_id:
        raise HTTPException(status_code=400, detail="customer_id is required")
    lead = payload.get("lead") or {}
    if not isinstance(lead, dict):
        raise HTTPException(status_code=400, detail="lead must be an object")
    orch = get_orchestrator()
    run = orch.start_run(
        customer_id=customer_id,
        lead=lead,
        correlation_id=payload.get("correlation_id"),
    )
    log.info("full_ops_run_created", run_id=run.run_id, customer_id=customer_id)
    return {
        "run": _run_view(orch, run.run_id),
        "governance_decision": "run_started_within_doctrine",
    }


@router.post("/runs/{run_id}/advance")
async def advance_run(run_id: str) -> dict[str, Any]:
    """Run the next stage of a workflow run."""
    orch = get_orchestrator()
    try:
        result = orch.advance(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found") from None
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {
        "result": result.to_dict(),
        "run": _run_view(orch, run_id),
        "governance_decision": (
            "auto_executed" if result.auto_executed else "approval_required"
        ),
    }


@router.post("/runs/{run_id}/run-all")
async def run_all(run_id: str) -> dict[str, Any]:
    """Run every remaining stage of a workflow run."""
    orch = get_orchestrator()
    try:
        results = orch.run_all(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found") from None
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    gated = sum(1 for r in results if not r.auto_executed)
    return {
        "results": [r.to_dict() for r in results],
        "run": _run_view(orch, run_id),
        "stages_run": len(results),
        "stages_gated": gated,
        "governance_decision": f"completed_with_{gated}_approval_gated_stages",
    }


@router.get("/runs/{run_id}")
async def get_run(run_id: str) -> dict[str, Any]:
    """Inspect a run: state, control-event trace, audit summary."""
    orch = get_orchestrator()
    try:
        view = _run_view(orch, run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found") from None
    trace = [
        {
            "event_type": ev.event_type,
            "decision": ev.decision,
            "occurred_at": ev.occurred_at.isoformat(),
        }
        for ev in orch.trace(run_id)
    ]
    audit = orch.audit_trail(run_id)
    return {
        "run": view,
        "trace": trace,
        "audit_entries": len(audit),
        "governance_decision": "ok",
    }


@router.get("/runs/{run_id}/approvals")
async def run_approvals(run_id: str) -> dict[str, Any]:
    """List the control-plane approval tickets a run has queued."""
    orch = get_orchestrator()
    try:
        orch.repo.get_run(tenant_id=orch.tenant_id, run_id=run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found") from None
    tickets = [
        {
            "ticket_id": t.ticket_id,
            "action_type": t.action_type,
            "state": t.state,
            "description": t.description,
        }
        for t in orch.repo.list_oversight_queue(tenant_id=orch.tenant_id)
        if t.run_id == run_id
    ]
    return {
        "run_id": run_id,
        "pending_approvals": tickets,
        "count": len(tickets),
        "governance_decision": "ok",
    }
