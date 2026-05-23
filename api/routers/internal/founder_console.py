"""Founder Console internal API.

Mounted under ``/api/v1/internal/...`` by ``api/main.py``. Every endpoint
in this router is read-by-default, write-on-approval. No endpoint
performs external sending; the most "active" thing they do is append
an approval-decision row to the audit log.

The endpoints are intentionally thin: they delegate to
``api.internal.runtime_reader`` for IO and ``api.internal.policy_adapter``
for guard checks. That keeps the router easy to audit and easy to test.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException

from api.internal import policy_adapter
from api.internal.auth import auth_mode, require_internal_token
from api.internal.runtime_reader import (
    approvals_list,
    audit_events,
    ceo_summary,
    control_summary,
    delivery_queue,
    distribution_summary,
    eval_status,
    finance_summary,
    operating_scorecard,
    policies_summary,
    productization,
    proof_library,
    record_approval_decision,
    record_incident,
    retention_queue,
    sales_funnel_summary,
    security_status,
    sovereign_readiness,
    trust_flags,
    worker_health,
)
from api.internal.runtime_reader import agent_registry as _agent_registry

router = APIRouter(
    prefix="/api/v1/internal",
    tags=["Internal — Founder Console"],
    dependencies=[Depends(require_internal_token)],
)


# ── read endpoints ─────────────────────────────────────────────────────────

@router.get("/ceo/summary")
def get_ceo_summary() -> dict[str, Any]:
    return ceo_summary()


@router.get("/sales/funnel")
def get_sales_funnel() -> dict[str, Any]:
    return sales_funnel_summary()


@router.get("/approvals")
def get_approvals() -> dict[str, Any]:
    return approvals_list()


@router.get("/workers/health")
def get_worker_health() -> dict[str, Any]:
    return worker_health()


@router.get("/trust/flags")
def get_trust_flags() -> dict[str, Any]:
    return trust_flags()


@router.get("/finance/summary")
def get_finance_summary() -> dict[str, Any]:
    return finance_summary()


@router.get("/distribution/summary")
def get_distribution_summary() -> dict[str, Any]:
    return distribution_summary()


@router.get("/delivery/queue")
def get_delivery_queue() -> dict[str, Any]:
    return delivery_queue()


@router.get("/retention/queue")
def get_retention_queue() -> dict[str, Any]:
    return retention_queue()


@router.get("/proof/library")
def get_proof_library() -> dict[str, Any]:
    return proof_library()


@router.get("/audit/events")
def get_audit_events(limit: int = 200) -> dict[str, Any]:
    return audit_events(limit=limit)


@router.get("/control/summary")
def get_control_summary() -> dict[str, Any]:
    return {**control_summary(), "auth_mode": auth_mode()}


@router.get("/control/policies")
def get_control_policies() -> dict[str, Any]:
    return policies_summary()


@router.get("/control/agents")
def get_control_agents() -> dict[str, Any]:
    return _agent_registry()


@router.get("/control/scorecard")
def get_control_scorecard() -> dict[str, Any]:
    return operating_scorecard()


@router.get("/control/risks")
def get_control_risks() -> dict[str, Any]:
    flags = trust_flags()
    return {
        "source": flags.get("source", "fallback"),
        "open_risks": [f for f in flags.get("flags", []) if f.get("status") == "open"],
        "generated_at": flags.get("generated_at"),
    }


@router.get("/evals/status")
def get_evals_status() -> dict[str, Any]:
    return eval_status()


@router.get("/product/productization")
def get_productization() -> dict[str, Any]:
    return productization()


@router.get("/security/status")
def get_security_status() -> dict[str, Any]:
    return {**security_status(), "auth_mode": auth_mode()}


@router.get("/sovereign/readiness")
def get_sovereign_readiness() -> dict[str, Any]:
    return sovereign_readiness()


# ── write endpoints (audit-logged, never external) ─────────────────────────

def _record_decision(approval_id: str, decision: str, reason: str | None) -> dict[str, Any]:
    if not approval_id:
        raise HTTPException(status_code=400, detail="approval_id required")
    policy = policy_adapter.evaluate(
        "send_outreach" if decision == "approve" else "approve_internal",
        external_impact=(decision == "approve"),
    )
    out = record_approval_decision(
        approval_id=approval_id,
        decision=decision,
        reason=reason,
        decided_by="founder",
        policy_class=policy.approval_class,
    )
    return {**out, "policy": policy.as_dict()}


@router.post("/approvals/{approval_id}/approve")
def post_approve(approval_id: str, body: dict[str, Any] | None = Body(default=None)) -> dict[str, Any]:
    return _record_decision(approval_id, "approve", (body or {}).get("reason"))


@router.post("/approvals/{approval_id}/reject")
def post_reject(approval_id: str, body: dict[str, Any] | None = Body(default=None)) -> dict[str, Any]:
    return _record_decision(approval_id, "reject", (body or {}).get("reason"))


@router.post("/approvals/{approval_id}/request-edit")
def post_request_edit(approval_id: str, body: dict[str, Any] | None = Body(default=None)) -> dict[str, Any]:
    return _record_decision(approval_id, "request_edit", (body or {}).get("reason"))


@router.post("/approvals/{approval_id}/escalate")
def post_escalate(approval_id: str, body: dict[str, Any] | None = Body(default=None)) -> dict[str, Any]:
    reason = (body or {}).get("reason") or "founder escalation"
    record_incident(kind="escalation", target=f"approval:{approval_id}", reason=reason)
    return _record_decision(approval_id, "escalate", reason)


@router.post("/workers/{worker_id}/retry")
def post_retry_worker(worker_id: str, body: dict[str, Any] | None = Body(default=None)) -> dict[str, Any]:
    reason = (body or {}).get("reason") or "manual retry"
    record_incident(kind="worker_retry", target=worker_id, reason=reason)
    return {"ok": True, "worker_id": worker_id, "queued_at": "<scheduler>", "reason": reason}


@router.post("/control/agents/{agent_id}/disable")
def post_disable_agent(agent_id: str, body: dict[str, Any] | None = Body(default=None)) -> dict[str, Any]:
    reason = (body or {}).get("reason") or "founder disabled"
    record_incident(kind="agent_disable", target=agent_id, reason=reason)
    return {"ok": True, "agent_id": agent_id, "status": "disabled", "reason": reason}


@router.post("/control/agents/{agent_id}/enable")
def post_enable_agent(agent_id: str, body: dict[str, Any] | None = Body(default=None)) -> dict[str, Any]:
    reason = (body or {}).get("reason") or "founder enabled"
    record_incident(kind="agent_enable", target=agent_id, reason=reason)
    return {"ok": True, "agent_id": agent_id, "status": "enabled", "reason": reason}
