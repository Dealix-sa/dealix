"""Revenue + KPI computation. Recognized revenue counts a deal only when it has a
real `payment_received` event — never on drafts or sends."""

from __future__ import annotations

from datetime import date

from . import pipeline
from .schemas import Deal, DealStage, KPIs, REVENUE_EVENT, STAGE_PROBABILITY


def recognized_revenue(deals: list[Deal]) -> int:
    return sum(d.value_sar for d in deals if d.has_event(REVENUE_EVENT))


def weighted_pipeline(deals: list[Deal]) -> float:
    total = 0.0
    for d in deals:
        if d.stage in {DealStage.LOST}:
            continue
        if d.has_event(REVENUE_EVENT):
            continue  # already recognized; not "pipeline"
        total += d.value_sar * STAGE_PROBABILITY.get(d.stage, 0.0)
    return total


def open_pipeline(deals: list[Deal]) -> int:
    return sum(
        d.value_sar
        for d in deals
        if d.stage not in {DealStage.LOST} and not d.has_event(REVENUE_EVENT)
    )


def compute_kpis(deals: list[Deal], today: date) -> KPIs:
    total = len(deals)
    won = sum(1 for d in deals if pipeline.is_won(d.stage))
    lost = sum(1 for d in deals if d.stage == DealStage.LOST)
    stalled = sum(1 for d in deals if pipeline.is_stalled(d, today))
    active = sum(1 for d in deals if pipeline.is_active(d.stage))
    decided = won + lost
    win_rate = (won / decided) if decided else 0.0
    return KPIs(
        total_deals=total,
        active_deals=active,
        won_deals=won,
        lost_deals=lost,
        stalled_deals=stalled,
        recognized_revenue_sar=recognized_revenue(deals),
        weighted_pipeline_sar=weighted_pipeline(deals),
        open_pipeline_sar=open_pipeline(deals),
        win_rate=win_rate,
    )
