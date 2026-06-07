"""Delivery API — start and advance the stateful 7-day Revenue Intelligence
Sprint, with the Day-5 founder-approval pause.

Additive surface (does NOT touch the existing stateless /api/v1/sprint/* demo
routes). Admin-gated with the same X-Admin-API-Key dependency as sprint_runner.
No external send ever happens here — the executor only advances internal state.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from api.routers.sprint_runner import _require_admin
from auto_client_acquisition.delivery_factory import sprint_executor

router = APIRouter(prefix="/api/v1/delivery", tags=["delivery"])


@router.post("/sprint/start")
async def start_sprint(
    body: dict[str, Any],
    _admin: str = Depends(_require_admin),
) -> dict[str, Any]:
    """Begin a sprint. Requires engagement_id + customer_id; other fields optional."""
    engagement_id = str(body.get("engagement_id") or "").strip()
    customer_id = str(body.get("customer_id") or "").strip()
    if not engagement_id or not customer_id:
        raise HTTPException(status_code=422, detail="engagement_id and customer_id are required")

    from dealix.commercial.sprint_orchestrator import SprintContext

    ctx = SprintContext(
        engagement_id=engagement_id,
        customer_id=customer_id,
        customer_name=str(body.get("customer_name") or ""),
        customer_name_ar=str(body.get("customer_name_ar") or ""),
        sector=str(body.get("sector") or ""),
        city=str(body.get("city") or ""),
        sources=list(body.get("sources") or []),
        rows=list(body.get("rows") or []),
        pain_summary=str(body.get("pain_summary") or ""),
        pain_summary_ar=str(body.get("pain_summary_ar") or ""),
        founder_approved=False,
    )
    return sprint_executor.start_sprint(ctx)


@router.post("/sprint/{engagement_id}/advance")
async def advance_sprint(
    engagement_id: str,
    _admin: str = Depends(_require_admin),
) -> dict[str, Any]:
    """Run the next sprint day. Pauses automatically at the Day-5 gate."""
    state = sprint_executor.advance(engagement_id)
    if state is None:
        raise HTTPException(status_code=404, detail="sprint_not_found")
    return state


@router.get("/sprint/{engagement_id}")
async def get_sprint(
    engagement_id: str,
    _admin: str = Depends(_require_admin),
) -> dict[str, Any]:
    """Current sprint state (day results, status, awaiting_approval)."""
    state = sprint_executor.get(engagement_id)
    if state is None:
        raise HTTPException(status_code=404, detail="sprint_not_found")
    return state


@router.post("/sprint/{engagement_id}/approve-day5")
async def approve_day5(
    engagement_id: str,
    body: dict[str, Any] | None = None,
    _admin: str = Depends(_require_admin),
) -> dict[str, Any]:
    """Founder approves the Day-5 governance gate; the sprint resumes on advance."""
    who = str((body or {}).get("who") or "founder").strip() or "founder"
    state = sprint_executor.approve_day5(engagement_id, who)
    if state is None:
        raise HTTPException(status_code=404, detail="sprint_not_found")
    return state
