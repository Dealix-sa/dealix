"""Per-customer value report — doctrine: no paid customer without one."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ValueReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str
    period: str  # e.g. "2026-Q2"
    activities: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    outcomes: list[str] = Field(default_factory=list)
    estimated_value_sar: float = 0.0
    risks_reduced: list[str] = Field(default_factory=list)
    assets_created: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    upsell_recommendation: str = ""
    approval_id: str | None = None

    @property
    def is_complete(self) -> bool:
        return bool(self.activities and self.outputs and self.outcomes and self.next_actions)
