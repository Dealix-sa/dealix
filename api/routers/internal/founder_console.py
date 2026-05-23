"""
Founder Console v3 — internal API.
واجهة المؤسس v3 — API داخلي.

Routes under /api/v1/internal/*. Read endpoints return summary state for
the founder UI; write endpoints (approve/reject/request-edit) record an
audit row and surface the Trust Plane policy result.

Per docs/trust/FOUNDER_CONSOLE_TRUST_GATE.md, external action is only
permitted when the policy result allows it; the UI must not bypass this
boundary.
"""

from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/internal", tags=["internal-founder-console"])


# ── Audit log location ─────────────────────────────────────────────
# Default to the private ops mount. Tests/dev can override via env.
_AUDIT_LOG_PATH = Path(
    os.environ.get(
        "DEALIX_APPROVAL_AUDIT_LOG",
        "/opt/dealix-ops-private/trust/approval_decisions.csv",
    )
)
_AUDIT_FIELDS = [
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


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _write_audit(row: dict[str, object]) -> bool:
    """Append a row to the approval audit log.

    Returns True on success, False if the log directory is not writable
    (which is the expected case in CI; the route still succeeds so the
    decision is not lost from the caller's perspective).
    """
    try:
        _AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        new_file = not _AUDIT_LOG_PATH.exists()
        with _AUDIT_LOG_PATH.open("a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=_AUDIT_FIELDS)
            if new_file:
                writer.writeheader()
            writer.writerow({field: row.get(field, "") for field in _AUDIT_FIELDS})
        return True
    except OSError:
        return False


# ── Schemas ────────────────────────────────────────────────────────
class ApprovalDecision(BaseModel):
    decision: Literal["approve", "reject", "needs_edit"] | None = None
    reason: str | None = None
    actor: str = "sami"
    approval_class: Literal["A0", "A1", "A2", "A3"] = "A2"
    risk_level: Literal["Low", "Medium", "High", "Critical"] = "Medium"
    evidence: str | None = None
    approval_type: str = Field(default="outreach", alias="type")

    model_config = {"populate_by_name": True}


# ── Read endpoints ─────────────────────────────────────────────────
@router.get("/ceo/summary")
def ceo_summary() -> dict[str, object]:
    return {
        "top_action": "Approve or build first outreach batch",
        "status": "C3 Revenue Partial",
        "risk_flags": 0,
        "cash_collected_sar": 0,
        "approved_outreach": 0,
        "positive_replies": 0,
        "proposals_due": 0,
        "payment_followups_due": 0,
        "last_updated": _now_iso(),
        "source": "api",
    }


@router.get("/sales/funnel")
def sales_funnel() -> dict[str, object]:
    return {
        "lead_intelligence": 0,
        "a_leads": 0,
        "pending_approval": 0,
        "approved_outreach": 0,
        "sent": 0,
        "replies": 0,
        "positive_replies": 0,
        "samples": 0,
        "proposals": 0,
        "payment_capture": 0,
        "source": "api",
    }


@router.get("/approvals")
def approvals() -> list[dict[str, object]]:
    return []


@router.get("/workers/health")
def workers_health() -> list[dict[str, object]]:
    return []


@router.get("/trust/flags")
def trust_flags() -> list[dict[str, object]]:
    return []


@router.get("/finance/summary")
def finance_summary() -> dict[str, object]:
    return {
        "cash_collected_sar": 0,
        "mrr_sar": 0,
        "pipeline_sar": 0,
        "weighted_pipeline_sar": 0,
        "payment_followups_due": 0,
        "source": "api",
    }


@router.get("/distribution/summary")
def distribution_summary() -> dict[str, object]:
    return {
        "channels": 0,
        "active_sectors": 0,
        "experiments": 0,
        "double_down": None,
        "source": "api",
    }


@router.get("/delivery/queue")
def delivery_queue() -> list[dict[str, object]]:
    return []


@router.get("/retention/queue")
def retention_queue() -> list[dict[str, object]]:
    return []


@router.get("/proof/library")
def proof_library() -> list[dict[str, object]]:
    return []


# ── Approval write endpoints (audit + policy) ──────────────────────
def _record_decision(
    *,
    approval_id: str,
    payload: ApprovalDecision,
    decision: str,
    policy_result: str,
    external_action_allowed: bool,
    source_endpoint: str,
) -> dict[str, object]:
    timestamp = _now_iso()
    audit_written = _write_audit(
        {
            "approval_id": approval_id,
            "type": payload.approval_type,
            "actor": payload.actor,
            "decision": decision,
            "reason": payload.reason or "",
            "approval_class": payload.approval_class,
            "risk_level": payload.risk_level,
            "policy_result": policy_result,
            "evidence": payload.evidence or "",
            "source_endpoint": source_endpoint,
            "timestamp": timestamp,
            "external_action_allowed": str(external_action_allowed).lower(),
        }
    )
    status_map = {
        "approve": "Approved",
        "reject": "Rejected",
        "needs_edit": "Needs Edit",
    }
    return {
        "approval_id": approval_id,
        "status": status_map[decision],
        "actor": payload.actor,
        "reason": payload.reason,
        "approval_class": payload.approval_class,
        "risk_level": payload.risk_level,
        "audit_written": audit_written,
        "policy_result": policy_result,
        "external_action_allowed": external_action_allowed,
        "timestamp": timestamp,
    }


@router.post("/approvals/{approval_id}/approve")
def approve_action(approval_id: str, payload: ApprovalDecision) -> dict[str, object]:
    if payload.decision is not None and payload.decision != "approve":
        raise HTTPException(status_code=400, detail="Use approve decision only.")
    # A3 cannot be auto-approved through this endpoint.
    if payload.approval_class == "A3":
        return _record_decision(
            approval_id=approval_id,
            payload=payload,
            decision="approve",
            policy_result="DENY_A3_REQUIRES_MANUAL_ESCALATION",
            external_action_allowed=False,
            source_endpoint=f"/api/v1/internal/approvals/{approval_id}/approve",
        )
    return _record_decision(
        approval_id=approval_id,
        payload=payload,
        decision="approve",
        policy_result="ALLOW_AFTER_APPROVAL",
        external_action_allowed=True,
        source_endpoint=f"/api/v1/internal/approvals/{approval_id}/approve",
    )


@router.post("/approvals/{approval_id}/reject")
def reject_action(approval_id: str, payload: ApprovalDecision) -> dict[str, object]:
    return _record_decision(
        approval_id=approval_id,
        payload=payload,
        decision="reject",
        policy_result="DENY",
        external_action_allowed=False,
        source_endpoint=f"/api/v1/internal/approvals/{approval_id}/reject",
    )


@router.post("/approvals/{approval_id}/request-edit")
def request_edit(approval_id: str, payload: ApprovalDecision) -> dict[str, object]:
    return _record_decision(
        approval_id=approval_id,
        payload=payload,
        decision="needs_edit",
        policy_result="NEEDS_EDIT",
        external_action_allowed=False,
        source_endpoint=f"/api/v1/internal/approvals/{approval_id}/request-edit",
    )
