"""Agent Registry. Every agent must register before it can act.

An Agent Card (section 126) declares its mission, max sovereignty level,
allowed / forbidden tools, expected inputs / outputs, KPIs, and risk
level. The kernel refuses to dispatch work to an unregistered agent.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.sovereignty.levels import SovereigntyLevel


@dataclass
class AgentCard:
    agent_id: str
    name: str
    owner: str
    domain: str
    mission: str
    max_sovereignty_level: SovereigntyLevel
    allowed_tools: list[str] = field(default_factory=list)
    forbidden_tools: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    kpis: list[str] = field(default_factory=list)
    risk_level: str = "medium"   # low|medium|high
    enabled: bool = True

    def can_use(self, tool_id: str) -> bool:
        if tool_id in self.forbidden_tools:
            return False
        return tool_id in self.allowed_tools


class AgentRegistry:
    def __init__(self) -> None:
        self._by_id: dict[str, AgentCard] = {}

    def register(self, card: AgentCard) -> AgentCard:
        if not card.kpis:
            raise ValueError(f"Agent {card.agent_id} must declare at least one KPI (no-orphan rule).")
        if card.max_sovereignty_level >= SovereigntyLevel.S4_SOVEREIGN_ONLY:
            raise ValueError(
                f"Agent {card.agent_id} cannot have max sovereignty level above S3 — S4/S5 are sovereign-only."
            )
        self._by_id[card.agent_id] = card
        return card

    def get(self, agent_id: str) -> AgentCard:
        if agent_id not in self._by_id:
            raise KeyError(f"Unregistered agent: {agent_id}")
        return self._by_id[agent_id]

    def disable(self, agent_id: str) -> None:
        self._by_id[agent_id].enabled = False

    def enable(self, agent_id: str) -> None:
        self._by_id[agent_id].enabled = True

    def all(self) -> list[AgentCard]:
        return list(self._by_id.values())

    def by_domain(self, domain: str) -> list[AgentCard]:
        return [a for a in self._by_id.values() if a.domain == domain]


__all__ = ["AgentCard", "AgentRegistry"]
