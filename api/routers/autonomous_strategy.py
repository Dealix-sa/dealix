"""Autonomous Strategy router — strategic tier + cycle + ledger surface.

Endpoint contract (frozen — a parallel frontend binds to this):
  GET  /api/v1/strategy/autonomous/tier
  POST /api/v1/strategy/autonomous/run        (admin-key gated)
  GET  /api/v1/strategy/autonomous/latest
  GET  /api/v1/strategy/autonomous/decisions
  GET  /api/v1/strategy/autonomous/gates

Honors the non-negotiables: ``run`` never sends or charges and never
auto-executes an irreversible decision — irreversible moves are routed to
the founder approval queue as pending approvals.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/strategy/autonomous",
    tags=["strategy-autonomous"],
)


class _RunBody(BaseModel):
    on_date: str | None = Field(default=None, description="Cycle date (YYYY-MM-DD)")
    customer_id: str = Field(default="dealix_strategic", min_length=1)
    cadence: str = Field(default="weekly", description="weekly | monthly | gate")
    pipeline_summary: dict[str, int] | None = Field(
        default=None,
        description="Optional pipeline metrics; falls back to recorded ledgers.",
    )
    delegate_full_ops: bool = Field(
        default=True,
        description="Delegate reversible decisions to the Full Ops cycle.",
    )


@router.get("/tier")
async def tier() -> dict[str, Any]:
    """Return the strategic tier (CEO + board directors) with live status."""
    from auto_client_acquisition.strategy_autonomy.strategic_hierarchy import (
        seed_strategic_tier,
        strategic_tier_status,
    )

    seed_strategic_tier()
    return {**strategic_tier_status(), "governance_decision": "allow"}


@router.post("/run", dependencies=[Depends(require_admin_key)])
async def run(body: _RunBody) -> dict[str, Any]:
    """Run the strategic autonomy cycle and return the StrategicCycleReport.

    Never sends, never charges, never auto-executes an irreversible
    decision — irreversible moves become pending founder approvals.
    """
    from auto_client_acquisition.strategy_autonomy.strategic_cycle import (
        run_strategic_cycle,
    )
    from auto_client_acquisition.strategy_autonomy.strategic_hierarchy import (
        seed_strategic_tier,
    )

    seed_strategic_tier()
    report = run_strategic_cycle(
        on_date=body.on_date,
        customer_id=body.customer_id,
        cadence=body.cadence,
        pipeline_summary=body.pipeline_summary,
        delegate_full_ops=body.delegate_full_ops,
    )
    return {**report.to_dict(), "governance_decision": "allow_with_review"}


@router.get("/latest")
async def latest() -> dict[str, Any]:
    """Return the most recent StrategicCycleReport, or an empty-state payload."""
    from auto_client_acquisition.strategy_autonomy.strategic_cycle import (
        latest_strategic_report,
    )

    report = latest_strategic_report()
    if report is None:
        return {
            "empty": True,
            "title_en": "No strategic autonomy cycle has run yet",
            "title_ar": "لم تُشغّل أي دورة استقلالية استراتيجية بعد",
            "signal_snapshot": {},
            "gate_evaluations": [],
            "decisions": [],
            "approvals_pending": {"count": 0, "items": []},
            "delegated_cycles": [],
            "next_actions": [],
            "governance_decision": "allow",
        }
    return {**report, "empty": False, "governance_decision": "allow"}


@router.get("/decisions")
async def decisions(
    decision_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
) -> dict[str, Any]:
    """Return strategic decisions from the code-backed decision ledger."""
    from auto_client_acquisition.strategy_autonomy.decision_ledger import (
        query_decisions,
    )

    rows = query_decisions(
        decision_type=decision_type,
        status=status,
        limit=limit,
    )
    return {
        "decisions": [r.to_dict() for r in rows],
        "governance_decision": "allow",
    }


@router.get("/gates")
async def gates() -> dict[str, Any]:
    """Return the codified strategic gate catalog."""
    from auto_client_acquisition.strategy_autonomy.gate_catalog import list_gates

    return {
        "gates": [g.to_dict() for g in list_gates()],
        "governance_decision": "allow",
    }
