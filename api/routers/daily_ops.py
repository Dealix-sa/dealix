"""Daily ops router — morning targeting pipeline via HTTP.

Endpoints:
    GET  /api/v1/daily-ops/status          — today's run status
    GET  /api/v1/daily-ops/targets         — today's top targets with scores
    POST /api/v1/daily-ops/run             — trigger dry-run (no Gmail drafts)
    POST /api/v1/daily-ops/run-and-draft   — trigger with draft creation enabled
"""

from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/daily-ops", tags=["daily-ops"])
log = logging.getLogger(__name__)

_REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports" / "daily"


def _today_report_path() -> Path:
    return _REPORTS_DIR / f"{date.today().isoformat()}.json"


def _load_today_report() -> dict[str, Any] | None:
    path = _today_report_path()
    if not path.is_file():
        return None
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        log.warning("daily_ops: failed to load report path=%s err=%s", path, exc)
        return None


def _run_engine(dry_run: bool) -> dict[str, Any]:
    try:
        from dealix.daily_targeting.daily_engine import DailyTargetingEngine
        engine = DailyTargetingEngine(dry_run=dry_run)
        report = engine.run()
        return report.to_dict()
    except Exception as exc:
        log.error("daily_ops: engine run failed err=%s", exc)
        return {"error": str(exc), "governance_decision": "deny"}


@router.get("/status", dependencies=[Depends(require_admin_key)])
async def daily_ops_status() -> dict[str, Any]:
    """Return today's run status: whether it ran, at what time, how many drafts."""
    report = _load_today_report()
    if report is None:
        return {
            "governance_decision": "allow",
            "today": date.today().isoformat(),
            "ran": False,
            "note": "no_report_for_today_yet",
        }
    return {
        "governance_decision": "allow",
        "today": date.today().isoformat(),
        "ran": True,
        "run_at": report.get("run_at"),
        "dry_run": report.get("dry_run"),
        "top_targets_count": len(report.get("top_targets", [])),
        "drafts_created": report.get("drafts_created", 0),
        "tier_counts": report.get("tier_counts", {}),
    }


@router.get("/targets", dependencies=[Depends(require_admin_key)])
async def daily_ops_targets() -> dict[str, Any]:
    """Return today's top target accounts with ICP scores."""
    report = _load_today_report()
    if report is None:
        return {
            "governance_decision": "allow",
            "today": date.today().isoformat(),
            "note": "no_report_for_today_yet. POST /run to generate.",
            "targets": [],
        }
    return {
        "governance_decision": "allow",
        "today": date.today().isoformat(),
        "run_at": report.get("run_at"),
        "targets": report.get("top_targets", []),
        "tier_counts": report.get("tier_counts", {}),
    }


@router.post("/run", dependencies=[Depends(require_admin_key)])
async def daily_ops_run() -> dict[str, Any]:
    """Trigger the daily targeting engine in dry-run mode (no Gmail API calls)."""
    result = _run_engine(dry_run=True)
    result["governance_decision"] = result.get("governance_decision", "allow")
    return result


@router.post("/run-and-draft", dependencies=[Depends(require_admin_key)])
async def daily_ops_run_and_draft() -> dict[str, Any]:
    """Trigger the daily targeting engine and create real Gmail drafts."""
    result = _run_engine(dry_run=False)
    result["governance_decision"] = result.get("governance_decision", "allow")
    return result
