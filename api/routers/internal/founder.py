"""Internal Founder Console API (v1, read-only).

Backs the Next.js Founder Console at ``apps/web/``. All endpoints are
gated by ``require_super_admin`` and return placeholder JSON whose shape
matches the TypeScript types in ``apps/web/lib/dealix-runtime.ts``.

Phase 2 of ``docs/runtime/FOUNDER_CONSOLE_RUNTIME_BINDING_PLAN.md`` wires
real data sources without changing response shapes. Action endpoints
(POST/PATCH) arrive in Phase 3 and route through the existing
``dealix/trust/ApprovalCenter`` and ``PolicyEvaluator``.
"""

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends

from api.security import require_super_admin

router = APIRouter(
    prefix="/api/v1/internal/founder",
    tags=["internal-founder"],
    dependencies=[Depends(require_super_admin)],
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.get("/ceo/summary")
async def ceo_summary() -> dict[str, Any]:
    """CEO command center summary — top action, status, risk, revenue."""
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
    }


@router.get("/sales/funnel")
async def sales_funnel() -> dict[str, int]:
    """Sales funnel counts from intelligence through payment capture."""
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
    }


@router.get("/approvals")
async def approvals() -> list[dict[str, Any]]:
    """Approval queue — A1/A2/A3 items awaiting founder review.

    Phase 3 replaces this placeholder with live items from
    ``dealix.trust.ApprovalCenter``.
    """
    return []


@router.get("/workers/health")
async def workers_health() -> list[dict[str, Any]]:
    """Runtime worker registry — status, last run, backlog, failures."""
    return []


@router.get("/trust/flags")
async def trust_flags() -> list[dict[str, Any]]:
    """Active trust flags — suppression, overclaim, breach, AI eval, incident."""
    return []


@router.get("/finance/summary")
async def finance_summary() -> dict[str, int]:
    """Cash, MRR, pipeline, weighted pipeline, payment follow-ups."""
    return {
        "cash_collected_sar": 0,
        "mrr_sar": 0,
        "pipeline_sar": 0,
        "weighted_pipeline_sar": 0,
        "payment_followups_due": 0,
    }


@router.get("/distribution/summary")
async def distribution_summary() -> dict[str, Any]:
    """Channel, sector, experiment counters + double-down decision."""
    return {
        "channels": 0,
        "active_sectors": 0,
        "experiments": 0,
        "double_down": None,
    }
