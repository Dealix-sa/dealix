"""Customer onboarding."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CustomerOnboarding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str
    kickoff_done: bool = False
    integrations_provisioned: bool = False
    first_outcome_logged: bool = False
    value_report_scheduled: bool = False
    items: list[str] = Field(default_factory=list)

    @property
    def progress(self) -> float:
        flags = [
            self.kickoff_done,
            self.integrations_provisioned,
            self.first_outcome_logged,
            self.value_report_scheduled,
        ]
        return round(sum(1 for f in flags if f) / len(flags), 4)
