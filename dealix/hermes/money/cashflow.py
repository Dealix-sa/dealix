"""
Cashflow summary over recorded outcomes.

Intentionally simple: aggregate revenue from the in-memory outcome store
so the dashboard and brief have a single source of truth.
"""

from __future__ import annotations

from pydantic import BaseModel

from dealix.hermes.core.outcomes import default_store as default_outcome_store


class CashflowSnapshot(BaseModel):
    total_revenue_sar: float
    wins_count: int
    pending_drafts: int
    time_saved_minutes: int


def snapshot() -> CashflowSnapshot:
    store = default_outcome_store()
    return CashflowSnapshot(
        total_revenue_sar=store.total_revenue_sar(),
        wins_count=len(store.wins()),
        pending_drafts=0,
        time_saved_minutes=store.total_time_saved_minutes(),
    )
