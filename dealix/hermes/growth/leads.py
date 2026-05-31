"""Leads — every lead carries a campaign, ICP, fit score, pain hypothesis."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class LeadStatus(StrEnum):
    new = "new"
    qualified = "qualified"
    contacted = "contacted"
    replied = "replied"
    meeting_booked = "meeting_booked"
    proposed = "proposed"
    won = "won"
    lost = "lost"
    disqualified = "disqualified"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _lid() -> str:
    return f"lead_{uuid.uuid4().hex[:16]}"


class Lead(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lead_id: str = Field(default_factory=_lid)
    source: str
    campaign_id: str | None = None
    company_name: str
    contact_name: str | None = None
    icp: str
    fit_score: int = Field(default=0, ge=0, le=10)
    pain_hypothesis: str = ""
    status: LeadStatus = LeadStatus.new
    created_at: str = Field(default_factory=_now)


@dataclass
class LeadStore:
    _leads: dict[str, Lead] = field(default_factory=dict)

    def add(self, lead: Lead) -> Lead:
        self._leads[lead.lead_id] = lead
        return lead

    def transition(self, lead_id: str, status: LeadStatus) -> Lead:
        l = self._leads[lead_id]
        updated = l.model_copy(update={"status": status})
        self._leads[lead_id] = updated
        return updated

    def get(self, lead_id: str) -> Lead:
        return self._leads[lead_id]

    def for_campaign(self, campaign_id: str) -> list[Lead]:
        return [l for l in self._leads.values() if l.campaign_id == campaign_id]

    def list(self) -> list[Lead]:
        return list(self._leads.values())
