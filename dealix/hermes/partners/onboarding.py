"""Partner onboarding checklist."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class OnboardingChecklist(BaseModel):
    model_config = ConfigDict(extra="forbid")

    partner_id: str
    contract_signed: bool = False
    revenue_share_agreed: bool = False
    portal_access_provisioned: bool = False
    training_completed: bool = False
    first_deal_in_pipeline: bool = False
    items: list[str] = Field(default_factory=list)

    @property
    def progress(self) -> float:
        flags = [
            self.contract_signed,
            self.revenue_share_agreed,
            self.portal_access_provisioned,
            self.training_completed,
            self.first_deal_in_pipeline,
        ]
        return round(sum(1 for f in flags if f) / len(flags), 4)
