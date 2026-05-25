"""Partner-led co-marketing tracking."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class PartnerCampaign(BaseModel):
    model_config = ConfigDict(extra="forbid")

    partner_id: str
    campaign_id: str
    revenue_share_pct: float = Field(default=0.0, ge=0.0, le=1.0)
    attributed_revenue_sar: float = 0.0


@dataclass
class PartnerMarketingLedger:
    _entries: dict[tuple[str, str], PartnerCampaign] = field(default_factory=dict)

    def upsert(self, entry: PartnerCampaign) -> PartnerCampaign:
        self._entries[(entry.partner_id, entry.campaign_id)] = entry
        return entry

    def for_partner(self, partner_id: str) -> list[PartnerCampaign]:
        return [v for k, v in self._entries.items() if k[0] == partner_id]
