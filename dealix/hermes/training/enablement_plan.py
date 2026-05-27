"""Per-customer enablement plan."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EnablementPlan:
    customer_id: str
    workshops: list[str] = field(default_factory=list)
    milestones: list[str] = field(default_factory=list)
    completed_milestones: list[str] = field(default_factory=list)

    def add_milestone(self, m: str) -> None:
        self.milestones.append(m)

    def complete(self, m: str) -> None:
        if m not in self.milestones:
            raise KeyError(f"Unknown milestone: {m}")
        if m not in self.completed_milestones:
            self.completed_milestones.append(m)

    @property
    def progress(self) -> float:
        if not self.milestones:
            return 0.0
        return len(self.completed_milestones) / len(self.milestones)


__all__ = ["EnablementPlan"]
