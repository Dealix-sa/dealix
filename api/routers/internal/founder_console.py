"""Founder Console v4 — internal API for the CEO operating interface.

Reads live runtime from Private Ops CSVs and writes audit records for
every approval decision. External-impact actions remain gated by the
Trust plane; this router only records decisions and surfaces the
policy result.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.internal.runtime_reader import (
    append_csv,
    approvals_list,
    ceo_summary as build_ceo_summary,
    finance_summary,
    now_iso,
    sales_funnel_summary,
)

router = APIRouter(prefix="/api/v1/internal", tags=["internal-founder-console"])


class ApprovalDecision(BaseModel):
    decision: str
    reason: str | None = None
    actor: str = "sami"


AUDIT_HEADERS = [
    "approval_id",
    "type",
    "actor",
    "decision",
    "reason",
    "approval_class",
    "risk_level",
    "policy_result",
    "evidence",
    "source_endpoint",
    "timestamp",
    "external_action_allowed",
]


@router.get("/ceo/summary")
def ceo_summary():
    return build_ceo_summary()


@router.get("/sales/funnel")
def sales_funnel():
    return sales_funnel_summary()


@router.get("/approvals")
def approvals():
    return approvals_list()


def _write_decision(
    approval_id: str,
    payload: ApprovalDecision,
    decision: str,
    policy_result: str,
    external_action_allowed: bool,
):
    item = next((a for a in approvals_list() if a["id"] == approval_id), None)
    append_csv(
        "trust/approval_decisions.csv",
        {
            "approval_id": approval_id,
            "type": item["type"] if item else "",
            "actor": payload.actor,
            "decision": decision,
            "reason": payload.reason or "",
            "approval_class": item["approval_class"] if item else "",
            "risk_level": item["risk_level"] if item else "",
            "policy_result": policy_result,
            "evidence": item["evidence"] if item else "",
            "source_endpoint": f"/api/v1/internal/approvals/{approval_id}",
            "timestamp": now_iso(),
            "external_action_allowed": str(external_action_allowed),
        },
        AUDIT_HEADERS,
    )
    return {
        "approval_id": approval_id,
        "status": decision,
        "actor": payload.actor,
        "reason": payload.reason,
        "audit_written": True,
        "policy_result": policy_result,
        "external_action_allowed": external_action_allowed,
        "timestamp": now_iso(),
    }


@router.post("/approvals/{approval_id}/approve")
def approve_action(approval_id: str, payload: ApprovalDecision):
    if payload.decision.lower() != "approve":
        raise HTTPException(status_code=400, detail="Use approve decision only.")
    return _write_decision(
        approval_id=approval_id,
        payload=payload,
        decision="Approved",
        policy_result="ALLOW_AFTER_APPROVAL",
        external_action_allowed=True,
    )


@router.post("/approvals/{approval_id}/reject")
def reject_action(approval_id: str, payload: ApprovalDecision):
    return _write_decision(
        approval_id=approval_id,
        payload=payload,
        decision="Rejected",
        policy_result="DENY",
        external_action_allowed=False,
    )


@router.post("/approvals/{approval_id}/request-edit")
def request_edit(approval_id: str, payload: ApprovalDecision):
    return _write_decision(
        approval_id=approval_id,
        payload=payload,
        decision="Needs Edit",
        policy_result="NEEDS_EDIT",
        external_action_allowed=False,
    )


@router.get("/workers/health")
def workers_health():
    return []


@router.get("/trust/flags")
def trust_flags():
    return []


@router.get("/finance/summary")
def finance():
    return finance_summary()


@router.get("/distribution/summary")
def distribution_summary():
    return {
        "channels": 0,
        "active_sectors": 0,
        "experiments": 0,
        "double_down": None,
        "source": "private_ops_csv",
    }
