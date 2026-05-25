"""Attribution — revenue ↔ campaign / lead / offer."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class AttributionType(StrEnum):
    first_touch = "first_touch"
    last_touch = "last_touch"
    multi_touch = "multi_touch"
    partner = "partner"
    direct = "direct"


class AttributionLink(BaseModel):
    model_config = ConfigDict(extra="forbid")

    revenue_id: str
    campaign_id: str | None = None
    lead_id: str | None = None
    offer_id: str | None = None
    partner_id: str | None = None
    channel: str | None = None
    attribution_type: AttributionType = AttributionType.last_touch
    amount_sar: float = 0.0


@dataclass
class RevenueAttribution:
    _links: list[AttributionLink] = field(default_factory=list)

    def link(self, link: AttributionLink) -> AttributionLink:
        self._links.append(link)
        return link

    def for_revenue(self, revenue_id: str) -> list[AttributionLink]:
        return [l for l in self._links if l.revenue_id == revenue_id]

    def for_campaign(self, campaign_id: str) -> list[AttributionLink]:
        return [l for l in self._links if l.campaign_id == campaign_id]

    def coverage_ratio(self, all_revenue_ids: list[str]) -> float:
        if not all_revenue_ids:
            return 0.0
        attributed = {l.revenue_id for l in self._links}
        return round(len(attributed & set(all_revenue_ids)) / len(all_revenue_ids), 4)
