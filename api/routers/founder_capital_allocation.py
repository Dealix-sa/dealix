# This router NEVER triggers external sends. Local JSONL/CSV only.
"""Capital allocation router — quarterly buckets and ROI matrix.

GET /api/v1/founder/capital-allocation/quarterly
GET /api/v1/founder/capital-allocation/roi-matrix

All endpoints admin-key gated. PRIVATE_OPS off → returns enabled:false.
This layer records intent only; money movement flows through
docs/revenue/INVOICE_FLOW.md + Moyasar verifier.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key
from dealix.private_ops import is_enabled, missing_private_ops_note, resolve_csv

router = APIRouter(
    prefix="/api/v1/founder/capital-allocation",
    tags=["founder", "capital-allocation"],
)


def _current_quarter() -> str:
    now = datetime.now(UTC)
    q = (now.month - 1) // 3 + 1
    return f"{now.year}Q{q}"


def _read_allocations() -> list[dict[str, str]]:
    p = resolve_csv("ceo/capital_allocations.csv")
    if p is None or not p.exists():
        return []
    with p.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


@router.get("/quarterly", dependencies=[Depends(require_admin_key)])
async def quarterly(quarter: str | None = None) -> dict[str, Any]:
    enabled = is_enabled()
    q = quarter or _current_quarter()
    rows = _read_allocations() if enabled else []
    subset = [r for r in rows if r.get("quarter") == q]
    buckets: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"allocated_sar": 0, "actual_sar": 0, "roi_estimate": 0.0, "count": 0}
    )
    for r in subset:
        bucket = r.get("bucket", "(unspecified)")
        try:
            buckets[bucket]["allocated_sar"] += int(float(r.get("allocated_sar") or 0))
            buckets[bucket]["actual_sar"] += int(float(r.get("actual_sar") or 0))
            buckets[bucket]["roi_estimate"] += float(r.get("roi_estimate") or 0)
            buckets[bucket]["count"] += 1
        except (TypeError, ValueError):
            continue
    for bucket, vals in buckets.items():
        if vals["count"]:
            vals["roi_estimate"] = round(vals["roi_estimate"] / vals["count"], 2)
    return {
        "private_ops_enabled": enabled,
        "private_ops_note": None if enabled else missing_private_ops_note("en"),
        "quarter": q,
        "buckets": [{"bucket": k, **v} for k, v in buckets.items()],
        "total_allocated_sar": sum(b["allocated_sar"] for b in buckets.values()),
        "total_actual_sar": sum(b["actual_sar"] for b in buckets.values()),
        "is_estimate": True,
        "governance_decision": "allow",
    }


@router.get("/roi-matrix", dependencies=[Depends(require_admin_key)])
async def roi_matrix() -> dict[str, Any]:
    enabled = is_enabled()
    rows = _read_allocations() if enabled else []
    scored: list[dict[str, Any]] = []
    for r in rows:
        try:
            score = float(r.get("roi_estimate") or 0)
        except (TypeError, ValueError):
            score = 0
        verdict = "approve" if score >= 20 else "test" if score >= 15 else "decline"
        scored.append({
            "quarter": r.get("quarter"),
            "bucket": r.get("bucket"),
            "owner": r.get("owner"),
            "roi_score": score,
            "verdict": verdict,
        })
    scored.sort(key=lambda d: d["roi_score"], reverse=True)
    return {
        "private_ops_enabled": enabled,
        "private_ops_note": None if enabled else missing_private_ops_note("en"),
        "count": len(scored),
        "items": scored,
        "is_estimate": True,
    }
