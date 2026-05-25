"""Case-study drafting — output only. Sami publishes."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CaseStudyDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str
    headline: str
    challenge: str
    solution: str
    outcome: str
    metrics: list[str] = Field(default_factory=list)
    approval_id: str | None = None
