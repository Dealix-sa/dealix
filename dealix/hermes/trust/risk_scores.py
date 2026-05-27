"""Risk Scoreboard.

Holds a running risk score in [0,1] per agent and per tool. Increments
on incidents / denials, decays on quiet days.
"""

from __future__ import annotations

from dataclasses import dataclass, field


def _clip(x: float) -> float:
    return max(0.0, min(1.0, x))


@dataclass
class RiskScoreboard:
    decay: float = 0.02            # per ``tick``
    _agent_scores: dict[str, float] = field(default_factory=dict)
    _tool_scores: dict[str, float] = field(default_factory=dict)

    def bump_agent(self, agent_id: str, delta: float) -> float:
        self._agent_scores[agent_id] = _clip(self._agent_scores.get(agent_id, 0.0) + delta)
        return self._agent_scores[agent_id]

    def bump_tool(self, tool_id: str, delta: float) -> float:
        self._tool_scores[tool_id] = _clip(self._tool_scores.get(tool_id, 0.0) + delta)
        return self._tool_scores[tool_id]

    def agent(self, agent_id: str) -> float:
        return self._agent_scores.get(agent_id, 0.0)

    def tool(self, tool_id: str) -> float:
        return self._tool_scores.get(tool_id, 0.0)

    def tick(self) -> None:
        for k in list(self._agent_scores.keys()):
            self._agent_scores[k] = _clip(self._agent_scores[k] - self.decay)
        for k in list(self._tool_scores.keys()):
            self._tool_scores[k] = _clip(self._tool_scores[k] - self.decay)

    def hot_agents(self, threshold: float = 0.6) -> list[str]:
        return sorted([k for k, v in self._agent_scores.items() if v >= threshold])

    def hot_tools(self, threshold: float = 0.6) -> list[str]:
        return sorted([k for k, v in self._tool_scores.items() if v >= threshold])


__all__ = ["RiskScoreboard"]
