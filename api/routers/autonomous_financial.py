"""Autonomous financial router — financial cycle + board memo surface.

Endpoint contract (frozen — a parallel frontend binds to this):
  GET  /api/v1/financial/autonomous/latest
  POST /api/v1/financial/autonomous/run                (admin-key gated)
  GET  /api/v1/financial/autonomous/board-memo/{month}
  POST /api/v1/financial/autonomous/board-memo/run     (admin-key gated)
  GET  /api/v1/financial/autonomous/thresholds

Honors the non-negotiables: ``run`` never sends, never charges, never
refunds. Every high-stakes financial signal is queued as a pending
approval for the founder.
"""
from __future__ import annotations

import re
from typing import Any

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key

_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")

router = APIRouter(
    prefix="/api/v1/financial/autonomous",
    tags=["financial-autonomous"],
)


class _RunBody(BaseModel):
    period_end: str | None = Field(
        default=None, description="Period end date (YYYY-MM-DD)"
    )
    cadence: str = Field(default="weekly", description="weekly | monthly")
    customer_id: str = Field(default="dealix_financial", min_length=1)


@router.get("/latest")
async def latest() -> dict[str, Any]:
    """Return the most recent :class:`FinancialCycleReport`, or empty state."""
    from auto_client_acquisition.financial_autonomy.financial_cycle import (
        latest_financial_report,
    )

    report = latest_financial_report()
    if report is None:
        return {
            "empty": True,
            "title_en": "No financial autonomy cycle has run yet",
            "title_ar": "لم تُشغّل أي دورة استقلالية مالية بعد",
            "metrics": {},
            "anomalies": [],
            "threshold_violations": [],
            "approvals_pending": {"count": 0, "items": []},
            "hard_gates": [],
            "warnings": [],
            "governance_decision": "allow",
        }
    return {**report, "empty": False, "governance_decision": "allow"}


@router.post("/run", dependencies=[Depends(require_admin_key)])
async def run(body: _RunBody) -> dict[str, Any]:
    """Run the weekly autonomous financial cycle.

    Never sends, never charges, never refunds. Every high-stakes signal
    becomes a pending founder approval.
    """
    from auto_client_acquisition.financial_autonomy.financial_cycle import (
        run_financial_cycle,
    )

    report = run_financial_cycle(
        period_end=body.period_end,
        cadence=body.cadence,
        customer_id=body.customer_id,
    )
    return {**report.to_dict(), "governance_decision": "allow_with_review"}


@router.get("/board-memo/{month}")
async def board_memo(month: str) -> dict[str, Any]:
    """Return the persisted board memo for ``month`` (``YYYY-MM``), or empty state."""
    from auto_client_acquisition.financial_autonomy.board_memo_cycle import (
        latest_board_memo,
    )

    if not _MONTH_RE.match(month or ""):
        return {
            "empty": True,
            "month": month,
            "error": "month_must_be_yyyy_mm",
            "governance_decision": "block",
        }
    try:
        report = latest_board_memo(month)
    except ValueError:
        return {
            "empty": True,
            "month": month,
            "error": "month_must_be_yyyy_mm",
            "governance_decision": "block",
        }
    if report is None:
        return {
            "empty": True,
            "month": month,
            "title_en": f"No board memo for {month}",
            "title_ar": f"لا توجد مذكّرة مجلس لشهر {month}",
            "sections": {},
            "governance_decision": "allow",
        }
    return {**report, "empty": False, "governance_decision": "allow"}


@router.post("/board-memo/run", dependencies=[Depends(require_admin_key)])
async def board_memo_run(
    month: str = Query(..., pattern=r"^\d{4}-\d{2}$"),
) -> dict[str, Any]:
    """Run the monthly board-memo cycle for ``month`` (``YYYY-MM``).

    The memo is never shared automatically — the response carries a
    pending approval id for the founder.
    """
    from auto_client_acquisition.financial_autonomy.board_memo_cycle import (
        run_board_memo_cycle,
    )

    report = run_board_memo_cycle(month=month)
    return {**report.to_dict(), "governance_decision": "allow_with_review"}


@router.get("/thresholds")
async def thresholds() -> dict[str, Any]:
    """Return the codified financial threshold catalog (read-only)."""
    from auto_client_acquisition.financial_autonomy.threshold_rules import (
        FINANCIAL_THRESHOLDS,
    )

    return {
        "thresholds": [rule.to_dict() for rule in FINANCIAL_THRESHOLDS],
        "governance_decision": "allow",
    }
