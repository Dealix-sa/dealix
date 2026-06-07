"""Dealix Now — daily founder operating pack (public read, draft-only).

All GET endpoints are public (no auth): they expose only public-sourced target
data and approval-first drafts — never PII, never sends. POST approve/reject
ONLY log a founder decision and return founder-operated send links; they never
send anything. Dealix never auto-sends.

The engine (``dealix.now``) is fully deterministic and offline: no LLM, no
network, no API keys.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse

from dealix.now import (
    build_now_pack,
    ledger,
    render_daily_brief_markdown,
)

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/now", tags=["now"])

# The 12 founder metrics (os/FOUNDER_OPERATING_MANUAL.md "أهم 12 رقم"). Values
# the engine can compute from the pack are filled; the rest are zero until the
# live pipeline produces them.
_FOUNDER_METRIC_NAMES: tuple[str, ...] = (
    "leads_researched",
    "fit_score_average",
    "drafts_created",
    "emails_approved",
    "reply_rate",
    "positive_reply_rate",
    "calls_booked",
    "proposal_rate",
    "close_rate",
    "delivery_cycle_time",
    "retainer_conversion",
    "expansion_revenue",
)


def _find_draft(pack: dict, draft_id: str) -> dict | None:
    for draft in pack.get("drafts", []):
        if draft.get("id") == draft_id:
            return draft
    return None


@router.get("/pack")
async def get_pack() -> dict[str, Any]:
    """Return the full DailyNowPack (deterministic, public-read)."""
    return build_now_pack()


@router.get("/leads")
async def get_leads() -> dict[str, Any]:
    """Return scored leads plus the metrics block."""
    pack = build_now_pack()
    return {"leads": pack["leads"], "metrics": pack["metrics"]}


@router.get("/drafts")
async def get_drafts() -> dict[str, Any]:
    """Return approval-first outreach drafts (high/medium tiers only)."""
    pack = build_now_pack()
    return {"drafts": pack["drafts"]}


@router.get("/daily-brief")
async def get_daily_brief(
    format: str = Query("markdown", pattern="^(markdown|json)$"),
) -> Any:
    """Return the Founder Daily Brief as markdown (text/plain) or JSON."""
    pack = build_now_pack()
    markdown = render_daily_brief_markdown(pack)
    if format == "json":
        return {"markdown": markdown, "pack": pack}
    return PlainTextResponse(markdown, media_type="text/plain; charset=utf-8")


@router.get("/metrics")
async def get_metrics() -> dict[str, Any]:
    """Return pack metrics plus the 12 founder metrics (zeros where unknown)."""
    pack = build_now_pack()
    metrics = pack["metrics"]
    founder_metrics: dict[str, float] = dict.fromkeys(_FOUNDER_METRIC_NAMES, 0)
    # Fill the metrics the engine can derive from today's pack.
    founder_metrics["leads_researched"] = metrics["leads_total"]
    founder_metrics["fit_score_average"] = metrics["avg_fit_score"]
    founder_metrics["drafts_created"] = metrics["drafts_ready"]
    return {"metrics": metrics, "founder_metrics": founder_metrics}


@router.post("/drafts/{draft_id}/approve")
async def approve_draft(draft_id: str) -> dict[str, Any]:
    """Log founder approval and return manual send links. NEVER sends."""
    pack = build_now_pack()
    draft = _find_draft(pack, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="draft_not_found")
    return ledger.approve(draft_id, draft)


@router.post("/drafts/{draft_id}/reject")
async def reject_draft(draft_id: str) -> dict[str, Any]:
    """Log founder rejection. Sends nothing."""
    pack = build_now_pack()
    draft = _find_draft(pack, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="draft_not_found")
    return ledger.reject(draft_id)


__all__ = ["router"]
