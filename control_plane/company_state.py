"""
Company state snapshot.

Aggregates the operating signals that the CEO brief, decision engine,
and risk engine consume. The snapshot is intentionally a plain
dataclass: easy to serialize, easy to test, easy to render in markdown.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable


@dataclass(slots=True)
class CompanyState:
    """A point-in-time read of the company.

    All counts are non-negative integers. All ratios are floats in [0, 1].
    Currency amounts are SAR (Saudi Riyal).
    """
    as_of: datetime
    stage: str = "0-founder-clarity"

    leads_this_week: int = 0
    qualified_leads: int = 0
    proposals_out: int = 0
    paid_sprints: int = 0

    cash_collected_30d: float = 0.0
    mrr: float = 0.0
    runway_months: float = 0.0

    pending_approvals: int = 0
    open_risks: list[str] = field(default_factory=list)

    company_health_score: int = 0  # 0..100

    @property
    def is_healthy(self) -> bool:
        return self.company_health_score >= 80


def snapshot(
    *,
    leads_this_week: int = 0,
    qualified_leads: int = 0,
    proposals_out: int = 0,
    paid_sprints: int = 0,
    cash_collected_30d: float = 0.0,
    mrr: float = 0.0,
    runway_months: float = 0.0,
    pending_approvals: int = 0,
    open_risks: Iterable[str] = (),
    company_health_score: int = 0,
    stage: str = "0-founder-clarity",
    as_of: datetime | None = None,
) -> CompanyState:
    """Build a CompanyState. Defaults make this safe to call empty."""
    return CompanyState(
        as_of=as_of or datetime.now(timezone.utc),
        stage=stage,
        leads_this_week=max(0, int(leads_this_week)),
        qualified_leads=max(0, int(qualified_leads)),
        proposals_out=max(0, int(proposals_out)),
        paid_sprints=max(0, int(paid_sprints)),
        cash_collected_30d=max(0.0, float(cash_collected_30d)),
        mrr=max(0.0, float(mrr)),
        runway_months=max(0.0, float(runway_months)),
        pending_approvals=max(0, int(pending_approvals)),
        open_risks=list(open_risks),
        company_health_score=max(0, min(100, int(company_health_score))),
    )
