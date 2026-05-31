"""FounderTimeLeverage: where the founder's time was saved or amplified."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FounderTimeLeverage:
    period: str
    tasks_delegated: int
    proposals_drafted: int
    decisions_summarized: int
    follow_ups_prepared: int
    hours_saved_estimate: float
    high_value_actions_identified: int


def compute(
    period: str,
    *,
    tasks_delegated: int = 0,
    proposals_drafted: int = 0,
    decisions_summarized: int = 0,
    follow_ups_prepared: int = 0,
    hours_saved_estimate: float = 0.0,
    high_value_actions_identified: int = 0,
) -> FounderTimeLeverage:
    """Compose a FounderTimeLeverage snapshot for a period."""
    return FounderTimeLeverage(
        period=period,
        tasks_delegated=int(tasks_delegated),
        proposals_drafted=int(proposals_drafted),
        decisions_summarized=int(decisions_summarized),
        follow_ups_prepared=int(follow_ups_prepared),
        hours_saved_estimate=float(hours_saved_estimate),
        high_value_actions_identified=int(high_value_actions_identified),
    )


def leverage_ratio(snapshot: FounderTimeLeverage, hours_invested: float) -> float:
    """Return hours_saved / hours_invested as a leverage ratio (0 when no investment)."""
    if hours_invested <= 0:
        return 0.0
    return round(snapshot.hours_saved_estimate / hours_invested, 4)
