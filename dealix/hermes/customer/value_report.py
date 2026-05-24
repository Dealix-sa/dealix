"""Monthly Value Report — what the customer received this month.

This is the artifact we send to retainer customers so they see what they
paid for. The report is deterministic: counts come from the outcome log,
narrative comes from the customer's notes.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from dealix.hermes.core.outcomes import OutcomeLog
from dealix.hermes.core.schemas import OutcomeKind


@dataclass(slots=True)
class ValueReport:
    customer_id: str
    period_start: datetime
    period_end: datetime
    outcomes_count: int
    outcomes_paid: int
    outcomes_won: int
    outcomes_risk_blocked: int
    realised_value_sar: float
    next_actions: list[str]
    narrative: str


def build(
    *,
    customer_id: str,
    outcomes_for_customer: OutcomeLog,
    narrative: str,
    period_days: int = 30,
) -> ValueReport:
    now = datetime.now(UTC)
    start = now - timedelta(days=period_days)
    recent = [o for o in outcomes_for_customer.all() if o.recorded_at >= start]

    paid = sum(1 for o in recent if o.kind is OutcomeKind.PAID)
    won = sum(1 for o in recent if o.kind is OutcomeKind.WON)
    blocked = sum(1 for o in recent if o.kind is OutcomeKind.RISK_BLOCKED)
    realised = sum(o.realised_value_sar for o in recent if o.kind is OutcomeKind.PAID)
    next_actions = [o.next_action for o in recent if o.next_action]

    return ValueReport(
        customer_id=customer_id,
        period_start=start,
        period_end=now,
        outcomes_count=len(recent),
        outcomes_paid=paid,
        outcomes_won=won,
        outcomes_risk_blocked=blocked,
        realised_value_sar=round(realised, 2),
        next_actions=next_actions[:10],
        narrative=narrative,
    )


__all__ = ["ValueReport", "build"]
