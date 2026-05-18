"""Autonomous Full Ops router — hierarchy + cycle surface.

Endpoint contract (frozen — a parallel frontend binds to this):
  GET  /api/v1/full-ops/autonomous/hierarchy
  POST /api/v1/full-ops/autonomous/run       (admin-key gated)
  GET  /api/v1/full-ops/autonomous/latest

Honors the non-negotiables: ``run`` never sends or charges; it produces
draft-only outputs and pending approvals for the founder.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key

router = APIRouter(
    prefix="/api/v1/full-ops/autonomous",
    tags=["full-ops-autonomous"],
)


class _RunBody(BaseModel):
    leads: list[dict[str, Any]] | None = Field(
        default=None,
        description="Optional lead list; falls back to the lead inbox.",
    )
    on_date: str | None = Field(default=None, description="Cycle date (YYYY-MM-DD)")
    customer_id: str = Field(default="dealix_full_ops", min_length=1)


@router.get("/hierarchy")
async def hierarchy() -> dict[str, Any]:
    """Return the agent pyramid annotated with live registry status."""
    from auto_client_acquisition.full_ops.agent_hierarchy import (
        hierarchy_status,
        seed_hierarchy,
    )

    seed_hierarchy()
    tree = hierarchy_status()
    return {**tree, "governance_decision": "allow"}


@router.post("/run", dependencies=[Depends(require_admin_key)])
async def run(body: _RunBody) -> dict[str, Any]:
    """Run the autonomous Full Ops cycle and return the CycleReport.

    Deterministic-to-the-gate: never sends, never charges. Every external
    action becomes a pending approval for the founder.
    """
    from auto_client_acquisition.full_ops.agent_hierarchy import seed_hierarchy
    from auto_client_acquisition.full_ops.autonomous_cycle import run_cycle

    seed_hierarchy()
    report = run_cycle(
        leads=body.leads,
        on_date=body.on_date,
        customer_id=body.customer_id,
    )
    return {**report.to_dict(), "governance_decision": "allow_with_review"}


@router.get("/latest")
async def latest() -> dict[str, Any]:
    """Return the most recent CycleReport, or an empty-state payload."""
    from auto_client_acquisition.full_ops.autonomous_cycle import latest_report

    report = latest_report()
    if report is None:
        return {
            "empty": True,
            "title_en": "No Full Ops cycle has run yet",
            "title_ar": "لم تُشغّل أي دورة Full Ops بعد",
            "stages": {},
            "approvals_pending": {"count": 0, "items": []},
            "work_items": {"count": 0, "by_priority": {}, "top": []},
            "next_actions": [],
            "governance_decision": "allow",
        }
    return {**report, "empty": False, "governance_decision": "allow"}
