# This router NEVER triggers external sends. Local JSONL/CSV only.
"""Founder leverage router — Make/Manage/Move bucket mix and time-audit history.

GET /api/v1/founder/leverage/dashboard
GET /api/v1/founder/leverage/time-audit/recent

All endpoints admin-key gated. PRIVATE_OPS off → returns enabled:false +
empty totals.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key
from dealix.private_ops import is_enabled, missing_private_ops_note, resolve_csv

router = APIRouter(prefix="/api/v1/founder/leverage", tags=["founder", "leverage"])


def _read_audit() -> list[dict[str, str]]:
    p = resolve_csv("ceo/leverage_time_audit.csv")
    if p is None or not p.exists():
        return []
    with p.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _ratio(rows: list[dict[str, str]], window: int) -> dict[str, Any]:
    recent = rows[-window:]
    totals = {"make": 0, "manage": 0, "move": 0}
    for r in recent:
        for bucket in totals:
            try:
                totals[bucket] += int(float(r.get(f"{bucket}_hours") or 0))
            except (TypeError, ValueError):
                continue
    total = sum(totals.values()) or 1
    return {
        "window_weeks": window,
        "totals": totals,
        "ratio": {k: round(v / total, 3) for k, v in totals.items()},
        "rows_used": len(recent),
    }


@router.get("/dashboard", dependencies=[Depends(require_admin_key)])
async def dashboard() -> dict[str, Any]:
    enabled = is_enabled()
    rows = _read_audit() if enabled else []
    summary = _ratio(rows, window=4)
    bottlenecks_csv = Path(__file__).resolve().parents[2] / "docs/metrics/bottlenecks_recent.csv"
    bottlenecks: list[str] = []
    if bottlenecks_csv.exists():
        try:
            with bottlenecks_csv.open("r", encoding="utf-8", newline="") as fh:
                reader = csv.DictReader(fh)
                bottlenecks = [
                    r.get("title", r.get("id", "(unnamed)"))
                    for r in list(reader)[:3]
                ]
        except OSError:
            bottlenecks = []
    return {
        "private_ops_enabled": enabled,
        "private_ops_note": None if enabled else missing_private_ops_note("en"),
        "summary": summary,
        "bottlenecks_top3": bottlenecks,
        "is_estimate": True,
        "governance_decision": "allow",
    }


@router.get("/time-audit/recent", dependencies=[Depends(require_admin_key)])
async def recent(window: int = 4) -> dict[str, Any]:
    enabled = is_enabled()
    rows = _read_audit() if enabled else []
    recent_rows = rows[-window:] if rows else []
    return {
        "private_ops_enabled": enabled,
        "private_ops_note": None if enabled else missing_private_ops_note("en"),
        "window": window,
        "rows": recent_rows,
    }
