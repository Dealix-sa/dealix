"""Agent Registry — no agent runs without a card."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.sovereignty.levels import SovereigntyLevel


class AgentCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str
    owner: str = "Sami"
    domain: str  # e.g. "money", "growth", "trust"
    mission: str
    max_sovereignty_level: SovereigntyLevel = SovereigntyLevel.S1_INTERNAL
    allowed_tools: list[str] = Field(default_factory=list)
    forbidden_tools: list[str] = Field(default_factory=list)
    kpis: list[str] = Field(default_factory=list)
    active: bool = True


@dataclass
class AgentRegistry:
    _cards: dict[str, AgentCard] = field(default_factory=dict)

    def register(self, card: AgentCard) -> AgentCard:
        self._cards[card.agent_id] = card
        return card

    def deactivate(self, agent_id: str) -> AgentCard:
        c = self._cards[agent_id]
        updated = c.model_copy(update={"active": False})
        self._cards[agent_id] = updated
        return updated

    def get(self, agent_id: str) -> AgentCard:
        return self._cards[agent_id]

    def exists(self, agent_id: str) -> bool:
        return agent_id in self._cards

    def list(self) -> list[AgentCard]:
        return list(self._cards.values())

    def is_tool_allowed(self, agent_id: str, tool_id: str) -> bool:
        card = self._cards.get(agent_id)
        if card is None or not card.active:
            return False
        if tool_id in card.forbidden_tools:
            return False
        return tool_id in card.allowed_tools
