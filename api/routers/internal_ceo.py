"""Founder Operating Layer — internal CEO summary endpoint.

Read-only endpoint that powers the `/ceo` page in the founder frontend.
Returns the top action, certification status, and the daily counters the
founder needs to operate Dealix as a company.

This router is intentionally minimal: the values are placeholders until
the CEO Summary Worker is connected. The shape is the source of truth —
the frontend depends on it.
"""
from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/internal/ceo", tags=["internal-ceo"])


@router.get("/summary")
def ceo_summary() -> dict:
    """Return the founder CEO summary payload.

    Stable contract — see ``docs/api/FOUNDER_INTERFACE_API_CONTRACT.md``.
    """
    return {
        "top_action": "Approve outreach batch",
        "status": "C3 Revenue Partial",
        "risk_flags": 0,
        "cash_collected_sar": 0,
        "approved_outreach": 0,
        "positive_replies": 0,
        "proposals_due": 0,
        "payment_followups_due": 0,
        "last_updated": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }
