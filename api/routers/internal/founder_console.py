"""Founder Console internal API.

All endpoints are read-only or write to the audit log under the private
ops root. No endpoint sends anything to a third party. Every approval
write is policy-checked and audited.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from api.internal import (
    agent_registry_reader,
    policy_adapter,
    runtime_reader,
)
from api.internal.auth import is_production_token_set, require_internal_token

router = APIRouter(
    prefix="/api/v1/internal",
    tags=["internal-founder-console"],
    dependencies=[Depends(require_internal_token)],
)


class ApprovalDecisionBody(BaseModel):
    reason: str | None = None
    evidence: str | None = None
    risk_level: str | None = "low"


class AgentStateBody(BaseModel):
    reason: str | None = None


# ──────────────────────────── CEO / sales ────────────────────────────


@router.get("/ceo/summary")
def get_ceo_summary() -> dict[str, Any]:
    return runtime_reader.ceo_summary()


@router.get("/sales/funnel")
def get_sales_funnel() -> dict[str, Any]:
    return runtime_reader.sales_funnel()


# ──────────────────────────── approvals ─────────────────────────────


@router.get("/approvals")
def get_approvals() -> dict[str, Any]:
    return runtime_reader.approvals_list()


def _record_decision(
    *,
    approval_id: str,
    decision: str,
    actor: str,
    body: ApprovalDecisionBody,
    source_endpoint: str,
) -> dict[str, Any]:
    approvals = runtime_reader.approvals_list()["items"]
    match = next(
        (r for r in approvals if (r.get("approval_id") or "").strip() == approval_id),
        None,
    )

    approval_class = (match or {}).get("approval_class", "A2")
    action_type = (match or {}).get("type", "")
    evidence_present = bool(body.evidence or (match or {}).get("evidence"))
    risk_level = (body.risk_level or (match or {}).get("risk_level") or "low").lower()

    decision_state = "approved" if decision == "approved" else "pending"
    policy = policy_adapter.evaluate(
        approval_class=approval_class,
        action_type=action_type,
        risk_level=risk_level,
        evidence_present=evidence_present,
        recipient_suppressed=False,
        actor_type="founder",
        decision_state=decision_state,
    )

    external_action_allowed = (
        decision == "approved"
        and approval_class != "A3"
        and policy.external_action_allowed
    )

    row = {
        "approval_id": approval_id,
        "type": action_type,
        "actor": actor,
        "decision": decision,
        "reason": body.reason or "",
        "approval_class": approval_class,
        "risk_level": risk_level,
        "policy_result": policy.rule_id,
        "evidence": body.evidence or (match or {}).get("evidence", ""),
        "source_endpoint": source_endpoint,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "external_action_allowed": "true" if external_action_allowed else "false",
    }
    audit_path = runtime_reader.append_runtime("approval_decisions", row)
    return {
        "approval_id": approval_id,
        "decision": decision,
        "policy": policy.to_dict(),
        "external_action_allowed": external_action_allowed,
        "audit_path": str(audit_path),
        "recorded_at": row["timestamp"],
    }


@router.post("/approvals/{approval_id}/approve")
def approve(
    approval_id: str,
    body: ApprovalDecisionBody,
    ctx: dict[str, str] = Depends(require_internal_token),
) -> dict[str, Any]:
    return _record_decision(
        approval_id=approval_id,
        decision="approved",
        actor=ctx["actor"],
        body=body,
        source_endpoint="POST /approvals/{id}/approve",
    )


@router.post("/approvals/{approval_id}/reject")
def reject(
    approval_id: str,
    body: ApprovalDecisionBody,
    ctx: dict[str, str] = Depends(require_internal_token),
) -> dict[str, Any]:
    return _record_decision(
        approval_id=approval_id,
        decision="rejected",
        actor=ctx["actor"],
        body=body,
        source_endpoint="POST /approvals/{id}/reject",
    )


@router.post("/approvals/{approval_id}/request-edit")
def request_edit(
    approval_id: str,
    body: ApprovalDecisionBody,
    ctx: dict[str, str] = Depends(require_internal_token),
) -> dict[str, Any]:
    return _record_decision(
        approval_id=approval_id,
        decision="needs_edit",
        actor=ctx["actor"],
        body=body,
        source_endpoint="POST /approvals/{id}/request-edit",
    )


@router.post("/approvals/{approval_id}/escalate")
def escalate(
    approval_id: str,
    body: ApprovalDecisionBody,
    ctx: dict[str, str] = Depends(require_internal_token),
) -> dict[str, Any]:
    return _record_decision(
        approval_id=approval_id,
        decision="escalated",
        actor=ctx["actor"],
        body=body,
        source_endpoint="POST /approvals/{id}/escalate",
    )


# ──────────────────────────── workers / trust ───────────────────────


@router.get("/workers/health")
def get_workers_health() -> dict[str, Any]:
    return runtime_reader.workers_health()


@router.get("/trust/flags")
def get_trust_flags() -> dict[str, Any]:
    return runtime_reader.trust_flags()


# ──────────────────────────── finance / distribution ────────────────


@router.get("/finance/summary")
def get_finance_summary() -> dict[str, Any]:
    return runtime_reader.finance_summary()


@router.get("/distribution/summary")
def get_distribution_summary() -> dict[str, Any]:
    return runtime_reader.distribution_summary()


@router.get("/delivery/queue")
def get_delivery_queue() -> dict[str, Any]:
    return runtime_reader.delivery_queue()


@router.get("/retention/queue")
def get_retention_queue() -> dict[str, Any]:
    return runtime_reader.retention_queue()


@router.get("/proof/library")
def get_proof_library() -> dict[str, Any]:
    return runtime_reader.proof_library()


# ──────────────────────────── audit / eval ──────────────────────────


@router.get("/audit/events")
def get_audit_events() -> dict[str, Any]:
    return runtime_reader.audit_events()


@router.get("/evals/status")
def get_eval_status() -> dict[str, Any]:
    return runtime_reader.eval_status()


# ──────────────────────────── control plane ─────────────────────────


@router.get("/control/summary")
def get_control_summary() -> dict[str, Any]:
    policy = policy_adapter.summary()
    registry = agent_registry_reader.summary()
    evals = runtime_reader.eval_status()
    trust = runtime_reader.trust_flags()
    scorecard = _operating_scorecard_payload()
    return {
        "policies": policy,
        "agents": registry,
        "open_risks": trust["count"],
        "eval_gate": {
            "blocking_failures": evals["blocking_failures"],
            "suites": len(evals["suites"]),
        },
        "operating_scorecard": scorecard,
        "production_token_set": is_production_token_set(),
        "source": "mixed",
    }


@router.get("/control/policies")
def get_control_policies() -> dict[str, Any]:
    return policy_adapter.summary()


@router.get("/control/agents")
def get_control_agents() -> dict[str, Any]:
    return {"agents": agent_registry_reader.agents(), **agent_registry_reader.summary()}


@router.post("/control/agents/{agent_id}/disable")
def disable_agent(
    agent_id: str,
    body: AgentStateBody,
    ctx: dict[str, str] = Depends(require_internal_token),
) -> dict[str, Any]:
    try:
        state = agent_registry_reader.set_agent_enabled(agent_id, False, body.reason)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    runtime_reader.append_runtime(
        "approval_decisions",
        {
            "approval_id": f"agent:{agent_id}:disable",
            "type": "agent_state",
            "actor": ctx["actor"],
            "decision": "disabled",
            "reason": body.reason or "",
            "approval_class": "A1",
            "risk_level": "low",
            "policy_result": "control_plane",
            "evidence": "",
            "source_endpoint": "POST /control/agents/{id}/disable",
            "timestamp": state["changed_at"],
            "external_action_allowed": "false",
        },
    )
    return {"agent_id": agent_id, "state": state}


@router.post("/control/agents/{agent_id}/enable")
def enable_agent(
    agent_id: str,
    body: AgentStateBody,
    ctx: dict[str, str] = Depends(require_internal_token),
) -> dict[str, Any]:
    try:
        state = agent_registry_reader.set_agent_enabled(agent_id, True, body.reason)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    runtime_reader.append_runtime(
        "approval_decisions",
        {
            "approval_id": f"agent:{agent_id}:enable",
            "type": "agent_state",
            "actor": ctx["actor"],
            "decision": "enabled",
            "reason": body.reason or "",
            "approval_class": "A1",
            "risk_level": "low",
            "policy_result": "control_plane",
            "evidence": "",
            "source_endpoint": "POST /control/agents/{id}/enable",
            "timestamp": state["changed_at"],
            "external_action_allowed": "false",
        },
    )
    return {"agent_id": agent_id, "state": state}


@router.get("/control/scorecard")
def get_control_scorecard() -> dict[str, Any]:
    return _operating_scorecard_payload()


@router.get("/control/risks")
def get_control_risks() -> dict[str, Any]:
    flags = runtime_reader.trust_flags()
    open_flags = [r for r in flags["flags"] if (r.get("status") or "").strip() == "open"]
    return {"risks": open_flags, "count": len(open_flags), "source": flags["source"]}


# ──────────────────────────── product / security ────────────────────


@router.get("/product/productization")
def get_productization() -> dict[str, Any]:
    return runtime_reader.productization()


@router.get("/security/status")
def get_security_status() -> dict[str, Any]:
    payload = runtime_reader.security_status()
    payload["production_token_set"] = is_production_token_set()
    return payload


# ──────────────────────────── helpers ───────────────────────────────


def _operating_scorecard_payload() -> dict[str, Any]:
    funnel = runtime_reader.sales_funnel()
    finance = runtime_reader.finance_summary()
    trust = runtime_reader.trust_flags()
    workers = runtime_reader.workers_health()

    revenue_score = min(100, int(finance["cash_collected_sar"] / 1000) + funnel["positive_replies"] * 5)
    trust_score = max(0, 100 - trust["count"] * 10 - trust["a3_attempts"] * 20)
    failures = 0
    for row in workers["workers"]:
        try:
            failures += int(row.get("failures_24h") or 0)
        except ValueError:
            continue
    runtime_score = max(0, 100 - failures * 5)
    founder_leverage = min(100, funnel["approved_outreach"] * 2 + funnel["positive_replies"] * 5)
    product_score = 40 if funnel["proposals"] > 0 else 20

    bottleneck = "no_data"
    if funnel["pending_approval"] > 5:
        bottleneck = "founder_review_backlog"
    elif funnel["positive_replies"] == 0 and funnel["sent"] > 0:
        bottleneck = "messaging_or_targeting"
    elif funnel["payment_capture"] > 0:
        bottleneck = "payment_capture"

    next_action = "Review pending approvals." if funnel["pending_approval"] > 0 else \
        ("Follow up on positive replies." if funnel["positive_replies"] > 0 else \
         "Add more A leads to lead intelligence.")

    return {
        "revenue_score": revenue_score,
        "trust_score": trust_score,
        "runtime_score": runtime_score,
        "founder_leverage_score": founder_leverage,
        "productization_score": product_score,
        "top_bottleneck": bottleneck,
        "next_best_action": next_action,
        "source": funnel["source"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
