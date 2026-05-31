"""
Campaign Registry — كل حملة مرتبطة بـ offer_id واحد على الأقل، وكل حملة
لها channel وICP وميزانية ومخاطر.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import StrEnum


class CampaignStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    KILLED = "killed"
    DONE = "done"


@dataclass
class Campaign:
    campaign_id: str
    name: str
    offer_id: str  # MUST reference an Offer in the registry
    icp_id: str
    channels: list[str]
    budget_sar: int
    hypothesis: str
    target_metric: str
    target_value: float
    status: CampaignStatus = CampaignStatus.DRAFT
    trust_risks: list[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.offer_id:
            raise ValueError("campaign must reference an offer_id (no Campaign without Offer)")
        if not self.channels:
            raise ValueError("campaign must declare at least one channel")
        if self.budget_sar < 0:
            raise ValueError("budget_sar must be >= 0")


class CampaignRegistry:
    def __init__(self) -> None:
        self._campaigns: dict[str, Campaign] = {}
        self._lock = threading.Lock()

    def register(self, campaign: Campaign) -> Campaign:
        campaign.validate()
        with self._lock:
            if campaign.campaign_id in self._campaigns:
                raise ValueError(f"campaign `{campaign.campaign_id}` already registered")
            self._campaigns[campaign.campaign_id] = campaign
        return campaign

    def get(self, campaign_id: str) -> Campaign | None:
        with self._lock:
            return self._campaigns.get(campaign_id)

    def active(self) -> list[Campaign]:
        with self._lock:
            return [c for c in self._campaigns.values() if c.status == CampaignStatus.ACTIVE]


__all__ = ["Campaign", "CampaignRegistry", "CampaignStatus"]
