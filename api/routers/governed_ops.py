"""Governed Ops HTTP surface (M3 + M4).

- GET  /api/v1/governed-ops/status                   — public health + gates
- POST /api/v1/governed-ops/governed-day/run         — run one governed day
- GET  /api/v1/governed-ops/governed-day/last        — last run in this process
- GET  /api/v1/governed-ops/governance-log           — recent governance events
- GET  /api/v1/governed-ops/governance-log/blocked   — blocked-actions audit log

Hard rules: the governed day only prepares / sweeps / snapshots — it never
sends anything externally. Admin-key gated for everything but /status.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from api.security.api_key import require_admin_key
from auto_client_acquisition.governance_os import governance_log
from auto_client_acquisition.orchestrator.governed_day import (
    get_last_governed_day_result,
    run_governed_day,
)

router = APIRouter(prefix="/api/v1/governed-ops", tags=["Governed Ops"])

_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_cold_outreach": True,
    "approval_required_for_external_actions": True,
    "governed_day_is_prepare_only": True,
}


@router.get("/status")
async def governed_ops_status() -> dict[str, Any]:
    return {"status": "ok", "surface": "governed_ops_m3_m4", "hard_gates": _HARD_GATES}


@router.post("/governed-day/run", dependencies=[Depends(require_admin_key)])
async def governed_day_run(dry_run: bool = Query(default=False)) -> dict[str, Any]:
    """Run one observable governed day. Prepare-only — no external sends."""
    result = run_governed_day(dry_run=dry_run)
    return result.to_dict()


@router.get("/governed-day/last", dependencies=[Depends(require_admin_key)])
async def governed_day_last() -> dict[str, Any]:
    result = get_last_governed_day_result()
    return result.to_dict() if result is not None else {"status": "not_run_yet"}


@router.get("/governance-log", dependencies=[Depends(require_admin_key)])
async def governance_log_recent(
    limit: int = Query(default=100, ge=1, le=1000),
) -> dict[str, Any]:
    events = governance_log.query_recent(limit=limit)
    return {"count": len(events), "events": events}


@router.get("/governance-log/blocked", dependencies=[Depends(require_admin_key)])
async def governance_log_blocked(
    limit: int = Query(default=100, ge=1, le=1000),
) -> dict[str, Any]:
    events = governance_log.query_blocked(limit=limit)
    return {"count": len(events), "events": events}
