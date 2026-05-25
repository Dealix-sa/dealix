"""Attribution analysis — group revenue by various dimensions."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.revenue_proof.proof_rules import is_real_revenue
from dealix.growth_os.revenue_proof.revenue_record import RevenueRecord

Dimension = Literal["channel", "offer", "campaign", "asset", "agent", "partner"]


class AttributionBreakdown(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimension: str
    only_real_revenue: bool = True
    totals: dict[str, float] = Field(default_factory=dict)
    counts: dict[str, int] = Field(default_factory=dict)


_DIM_FIELDS: dict[Dimension, tuple[str, str]] = {
    "channel": ("attributed_channels", ""),
    "offer": ("", "offer_key"),
    "campaign": ("attributed_campaigns", ""),
    "asset": ("attributed_assets", ""),
    "agent": ("attributed_agents", ""),
    "partner": ("attributed_partners", ""),
}


def _values_for(record: RevenueRecord, dim: Dimension) -> list[str]:
    list_field, scalar_field = _DIM_FIELDS[dim]
    if scalar_field:
        v = getattr(record, scalar_field)
        return [v] if v else []
    return [v for v in getattr(record, list_field) if v]


def group_revenue_by(
    records: Iterable[RevenueRecord],
    dimension: Dimension,
    *,
    only_real_revenue: bool = True,
) -> AttributionBreakdown:
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}
    for r in records:
        if only_real_revenue and not is_real_revenue(r):
            continue
        keys = _values_for(r, dimension)
        if not keys:
            continue
        share = r.amount_usd / len(keys)
        for k in keys:
            totals[k] = round(totals.get(k, 0.0) + share, 4)
            counts[k] = counts.get(k, 0) + 1
    return AttributionBreakdown(
        dimension=dimension,
        only_real_revenue=only_real_revenue,
        totals=totals,
        counts=counts,
    )


def group_revenue_by_channel(
    records: Iterable[RevenueRecord], *, only_real_revenue: bool = True
) -> AttributionBreakdown:
    return group_revenue_by(records, "channel", only_real_revenue=only_real_revenue)


def group_revenue_by_offer(
    records: Iterable[RevenueRecord], *, only_real_revenue: bool = True
) -> AttributionBreakdown:
    return group_revenue_by(records, "offer", only_real_revenue=only_real_revenue)


def group_revenue_by_campaign(
    records: Iterable[RevenueRecord], *, only_real_revenue: bool = True
) -> AttributionBreakdown:
    return group_revenue_by(records, "campaign", only_real_revenue=only_real_revenue)


def group_revenue_by_asset(
    records: Iterable[RevenueRecord], *, only_real_revenue: bool = True
) -> AttributionBreakdown:
    return group_revenue_by(records, "asset", only_real_revenue=only_real_revenue)


def group_revenue_by_agent(
    records: Iterable[RevenueRecord], *, only_real_revenue: bool = True
) -> AttributionBreakdown:
    return group_revenue_by(records, "agent", only_real_revenue=only_real_revenue)


def group_revenue_by_partner(
    records: Iterable[RevenueRecord], *, only_real_revenue: bool = True
) -> AttributionBreakdown:
    return group_revenue_by(records, "partner", only_real_revenue=only_real_revenue)


__all__ = [
    "AttributionBreakdown",
    "Dimension",
    "group_revenue_by",
    "group_revenue_by_agent",
    "group_revenue_by_asset",
    "group_revenue_by_campaign",
    "group_revenue_by_channel",
    "group_revenue_by_offer",
    "group_revenue_by_partner",
]
