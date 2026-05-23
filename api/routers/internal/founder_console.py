"""Founder Console + Control Plane internal API.

All endpoints are mounted under ``/api/v1/internal``. Token-gated via
``api.internal.auth.require_internal_token``. Read-mostly; the small
number of POST endpoints write to the audit log in the private ops
runtime and never produce external side effects.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Path

from api.internal import runtime_reader as rr
from api.internal.auth import require_internal_token
from api.internal.policy_adapter import evaluate_action

router = APIRouter(
    prefix="/api/v1/internal",
    tags=["internal-founder-console"],
    dependencies=[Depends(require_internal_token)],
)


# ── CEO / Sales / Approvals ───────────────────────────────────────


@router.get("/ceo/summary")
def ceo_summary() -> dict[str, Any]:
    return rr.ceo_summary()


@router.get("/sales/funnel")
def sales_funnel() -> dict[str, Any]:
    return rr.sales_funnel_summary()


@router.get("/approvals")
def approvals() -> dict[str, Any]:
    return rr.approvals_list()


_APPROVAL_FIELDS = [
    "id",
    "decision",
    "decided_at",
    "reason",
    "approved_by",
    "evidence",
    "class",
]


def _record_decision(approval_id: str, decision: str, reason: str | None) -> dict[str, Any]:
    row = {
        "id": approval_id,
        "decision": decision,
        "decided_at": rr.now_iso(),
        "reason": reason or "",
        "approved_by": "founder",
        "evidence": "",
        "class": "A2",
    }
    ok = rr.append_csv("trust/approval_decisions.csv", _APPROVAL_FIELDS, row)
    return {"recorded": ok, "decision": row}


@router.post("/approvals/{approval_id}/approve")
def approve(approval_id: str = Path(...), payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    verdict = evaluate_action(
        {"class": payload.get("class", "A2"), "approved_by": "founder", "evidence": payload.get("evidence")}
    )
    if not verdict["allowed"]:
        raise HTTPException(status_code=400, detail={"verdict": verdict})
    return _record_decision(approval_id, "approve", payload.get("reason"))


@router.post("/approvals/{approval_id}/reject")
def reject(approval_id: str = Path(...), payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    return _record_decision(approval_id, "reject", payload.get("reason"))


@router.post("/approvals/{approval_id}/request-edit")
def request_edit(approval_id: str = Path(...), payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    return _record_decision(approval_id, "request_edit", payload.get("reason"))


@router.post("/approvals/{approval_id}/escalate")
def escalate(approval_id: str = Path(...), payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    return _record_decision(approval_id, "escalate", payload.get("reason"))


# ── Workers ───────────────────────────────────────────────────────


@router.get("/workers/health")
def workers_health() -> dict[str, Any]:
    return rr.worker_health()


@router.post("/workers/{worker_id}/retry")
def workers_retry(worker_id: str = Path(...), payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    rr.append_csv(
        "runtime/worker_state.csv",
        ["worker", "last_run", "status", "failures_24h", "next_run", "notes"],
        {
            "worker": worker_id,
            "last_run": rr.now_iso(),
            "status": "retry_requested",
            "failures_24h": "0",
            "next_run": "",
            "notes": payload.get("reason", "manual retry"),
        },
    )
    return {"worker_id": worker_id, "queued": True}


# ── Trust / Finance / Distribution / Delivery / Retention / Proof ─


@router.get("/trust/flags")
def trust_flags() -> dict[str, Any]:
    return rr.trust_flags()


@router.get("/finance/summary")
def finance_summary() -> dict[str, Any]:
    return rr.finance_summary()


@router.get("/distribution/summary")
def distribution_summary() -> dict[str, Any]:
    return rr.distribution_summary()


@router.get("/delivery/queue")
def delivery_queue() -> dict[str, Any]:
    return rr.delivery_queue()


@router.get("/retention/queue")
def retention_queue() -> dict[str, Any]:
    return rr.retention_queue()


@router.get("/proof/library")
def proof_library() -> dict[str, Any]:
    return rr.proof_library()


@router.get("/audit/events")
def audit_events() -> dict[str, Any]:
    return rr.audit_events()


# ── Control plane ─────────────────────────────────────────────────


@router.get("/control/summary")
def control_summary() -> dict[str, Any]:
    return rr.control_summary()


@router.get("/control/policies")
def control_policies() -> dict[str, Any]:
    return rr.policies_summary()


@router.get("/control/agents")
def control_agents() -> dict[str, Any]:
    return rr.agent_registry()


_AGENT_TOGGLE_FIELDS = ["agent_id", "decision", "decided_at", "reason"]


@router.post("/control/agents/{agent_id}/disable")
def agents_disable(agent_id: str = Path(...), payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    rr.append_csv(
        "trust/agent_toggles.csv",
        _AGENT_TOGGLE_FIELDS,
        {"agent_id": agent_id, "decision": "disable", "decided_at": rr.now_iso(), "reason": payload.get("reason", "")},
    )
    return {"agent_id": agent_id, "state": "disabled"}


@router.post("/control/agents/{agent_id}/enable")
def agents_enable(agent_id: str = Path(...), payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    rr.append_csv(
        "trust/agent_toggles.csv",
        _AGENT_TOGGLE_FIELDS,
        {"agent_id": agent_id, "decision": "enable", "decided_at": rr.now_iso(), "reason": payload.get("reason", "")},
    )
    return {"agent_id": agent_id, "state": "enabled"}


@router.get("/control/scorecard")
def control_scorecard() -> dict[str, Any]:
    return rr.operating_scorecard()


@router.get("/control/risks")
def control_risks() -> dict[str, Any]:
    flags = rr.trust_flags().get("flags", [])
    open_flags = [f for f in flags if (f.get("status") or "open") != "resolved"]
    return {"open_count": len(open_flags), "items": open_flags, "source": "private_ops"}


# ── Evals / Productization / Security ─────────────────────────────


@router.get("/evals/status")
def evals_status() -> dict[str, Any]:
    return rr.eval_status()


@router.get("/product/productization")
def productization() -> dict[str, Any]:
    return rr.productization()


@router.get("/security/status")
def security_status() -> dict[str, Any]:
    return rr.security_status()
