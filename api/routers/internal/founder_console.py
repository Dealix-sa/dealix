"""Founder Console v2 — internal API surface.

This router exposes the read endpoints and approval action endpoints that
the Founder Console UI calls. Every endpoint declares:

- input  : Pydantic model or path/query types
- output : a JSON-serialisable shape consumed by ``apps/web``
- source : the eventual source of truth (see
  ``docs/runtime/FOUNDER_CONSOLE_SOURCE_OF_TRUTH.md``)
- trust  : A1 (no approval) for reads, A2 (approval required) for writes
- audit  : every write returns ``audit_written: true`` and is intended to
  be persisted via the audit layer when wired to the runtime.

This v1 cut returns safe, empty/zero shapes so the Founder Console can
ship behind a CI gate without leaking pre-launch numbers. Source-of-truth
wiring happens in the next runtime PR.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/v1/internal", tags=["internal-founder-console"])


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class ApprovalDecision(BaseModel):
    """Body for approval decisions (approve / reject / request-edit)."""

    decision: str = Field(
        ...,
        description="One of: approve | reject | needs_edit | escalate | defer",
    )
    reason: Optional[str] = Field(
        default=None,
        description="Optional human-readable reason captured in the audit log.",
    )
    actor: str = Field(
        default="sami",
        description="Identity of the founder/operator making the call.",
    )


# ── /ceo/summary ─────────────────────────────────────────────────


@router.get("/ceo/summary")
def ceo_summary() -> dict:
    """CEO morning brief — one top action + headline counters."""
    return {
        "top_action": "Approve or build first outreach batch",
        "status": "C3 Revenue Partial",
        "risk_flags": 0,
        "cash_collected_sar": 0,
        "approved_outreach": 0,
        "positive_replies": 0,
        "proposals_due": 0,
        "payment_followups_due": 0,
        "last_updated": _utc_iso(),
        "source": "ceo_summary_worker",
        "trust_class": "A1",
    }


# ── /sales/funnel ────────────────────────────────────────────────


@router.get("/sales/funnel")
def sales_funnel() -> dict:
    """Funnel-stage counters for the Sales Cockpit."""
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
        "last_updated": _utc_iso(),
        "source": "revenue_runtime",
        "trust_class": "A1",
    }


# ── /approvals ───────────────────────────────────────────────────


@router.get("/approvals")
def approvals() -> list:
    """Pending approvals queue. Empty until queue is wired."""
    return []


@router.post("/approvals/{approval_id}/approve")
def approve_action(approval_id: str, payload: ApprovalDecision) -> dict:
    if payload.decision.lower() != "approve":
        raise HTTPException(
            status_code=400,
            detail="Use approve decision only.",
        )
    return {
        "approval_id": approval_id,
        "status": "Approved",
        "actor": payload.actor,
        "reason": payload.reason,
        "audit_written": True,
        "trust_class": "A2",
        "approved_at": _utc_iso(),
    }


@router.post("/approvals/{approval_id}/reject")
def reject_action(approval_id: str, payload: ApprovalDecision) -> dict:
    return {
        "approval_id": approval_id,
        "status": "Rejected",
        "actor": payload.actor,
        "reason": payload.reason,
        "audit_written": True,
        "trust_class": "A2",
        "rejected_at": _utc_iso(),
    }


@router.post("/approvals/{approval_id}/request-edit")
def request_edit(approval_id: str, payload: ApprovalDecision) -> dict:
    return {
        "approval_id": approval_id,
        "status": "Needs Edit",
        "actor": payload.actor,
        "reason": payload.reason,
        "audit_written": True,
        "trust_class": "A2",
        "updated_at": _utc_iso(),
    }


# ── /workers/health ──────────────────────────────────────────────


@router.get("/workers/health")
def workers_health() -> list:
    """Per-worker health snapshot. Empty until workers report in."""
    return []


# ── /trust/flags ─────────────────────────────────────────────────


@router.get("/trust/flags")
def trust_flags() -> list:
    """Open trust flags (policy violations, suppression, anomalies)."""
    return []


# ── /finance/summary ─────────────────────────────────────────────


@router.get("/finance/summary")
def finance_summary() -> dict:
    return {
        "cash_collected_sar": 0,
        "mrr_sar": 0,
        "pipeline_sar": 0,
        "weighted_pipeline_sar": 0,
        "payment_followups_due": 0,
        "last_updated": _utc_iso(),
        "source": "finance_runtime",
        "trust_class": "A1",
    }


# ── /distribution/summary ────────────────────────────────────────


@router.get("/distribution/summary")
def distribution_summary() -> dict:
    return {
        "channels": 0,
        "active_sectors": 0,
        "experiments": 0,
        "double_down": None,
        "last_updated": _utc_iso(),
        "source": "channel_sector_scorecards",
        "trust_class": "A1",
    }


# ── /delivery/queue ──────────────────────────────────────────────


@router.get("/delivery/queue")
def delivery_queue() -> list:
    return []


# ── /retention/queue ─────────────────────────────────────────────


@router.get("/retention/queue")
def retention_queue() -> list:
    return []


# ── /proof/library ───────────────────────────────────────────────


@router.get("/proof/library")
def proof_library() -> list:
    return []
