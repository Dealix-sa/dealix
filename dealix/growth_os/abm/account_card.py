"""AccountCard pydantic model — the core ABM record."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Stakeholder(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: str = Field(..., min_length=1)
    influence: Literal["champion", "decision_maker", "blocker", "user"]
    notes: str = ""


class AccountCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    account_id: str = Field(..., min_length=1)
    account_label: str = Field(..., min_length=1, description="Generic label like 'Agency X'")
    icp_key: str
    stage: str
    pain_hypothesis: str = ""
    stakeholders: list[Stakeholder] = Field(default_factory=list)
    personalized_offer: str = ""
    proof_assets_attached: list[str] = Field(default_factory=list)
    next_action: str = ""
    deal_room_url: str = ""
    outcome: Literal["open", "won", "lost", "deferred"] = "open"
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)


__all__ = ["AccountCard", "Stakeholder"]
