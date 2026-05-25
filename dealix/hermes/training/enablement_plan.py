"""Customer enablement plan."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EnablementStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: str
    title: str
    owner: str
    due_at: str | None = None
    completed: bool = False


class EnablementPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_id: str
    customer_id: str
    steps: list[EnablementStep] = Field(default_factory=list)

    @property
    def progress(self) -> float:
        if not self.steps:
            return 0.0
        done = sum(1 for s in self.steps if s.completed)
        return round(done / len(self.steps), 4)
