"""Per-agent performance summary."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentPerformance:
    agent_id: str
    executions: int
    outcomes_logged: int
    assets_created: int
    avg_score: float

    @property
    def outcome_coverage(self) -> float:
        return round(self.outcomes_logged / self.executions, 4) if self.executions else 0.0
