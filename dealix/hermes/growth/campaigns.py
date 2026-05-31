"""Campaigns — every campaign must declare ICP × offer × channel."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CampaignStatus(StrEnum):
    draft = "draft"
    approved = "approved"
    live = "live"
    paused = "paused"
    killed = "killed"
    archived = "archived"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _cid() -> str:
    return f"cmp_{uuid.uuid4().hex[:16]}"


class Campaign(BaseModel):
    model_config = ConfigDict(extra="forbid")

    campaign_id: str = Field(default_factory=_cid)
    name: str
    target_icp: str
    offer_id: str
    channel: str
    message_angle: str = ""
    cta: str = ""
    status: CampaignStatus = CampaignStatus.draft
    approval_id: str | None = None
    created_at: str = Field(default_factory=_now)


@dataclass
class CampaignStore:
    _campaigns: dict[str, Campaign] = field(default_factory=dict)

    def create(self, campaign: Campaign) -> Campaign:
        if not campaign.offer_id:
            raise ValueError("campaign requires an offer_id (no campaign without offer)")
        self._campaigns[campaign.campaign_id] = campaign
        return campaign

    def approve(self, campaign_id: str, approval_id: str) -> Campaign:
        c = self._campaigns[campaign_id]
        updated = c.model_copy(update={"status": CampaignStatus.approved, "approval_id": approval_id})
        self._campaigns[campaign_id] = updated
        return updated

    def go_live(self, campaign_id: str) -> Campaign:
        c = self._campaigns[campaign_id]
        if c.status != CampaignStatus.approved:
            raise PermissionError("campaign cannot go live without approval")
        updated = c.model_copy(update={"status": CampaignStatus.live})
        self._campaigns[campaign_id] = updated
        return updated

    def get(self, campaign_id: str) -> Campaign:
        return self._campaigns[campaign_id]

    def list(self) -> list[Campaign]:
        return list(self._campaigns.values())
