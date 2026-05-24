"""Enablement Plan — what the buyer must do in the 30 days after a workshop."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EnablementMilestone:
    week: int
    goal: str
    artifact: str


class EnablementPlan:
    def build(self, title: str) -> list[EnablementMilestone]:
        return [
            EnablementMilestone(1, f"Apply {title} concept #1", "Signed policy"),
            EnablementMilestone(2, "Run two governed agent tasks", "Approval log"),
            EnablementMilestone(3, "Publish an internal value report", "Value report v1"),
            EnablementMilestone(4, "Decide on the upsell", "Upsell decision note"),
        ]
