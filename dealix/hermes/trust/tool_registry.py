"""Tool Registry — every tool declares risk, scope, owner, audit needs."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ToolRisk(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class ToolCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool_id: str
    owner: str = "Sami"
    description: str = ""
    risk_level: ToolRisk = ToolRisk.medium
    enabled: bool = False
    requires_approval: bool = True
    allowed_agents: list[str] = Field(default_factory=list)
    data_scope: str = "internal_only"
    audit_required: bool = True
    pdpl_relevant: bool = False


@dataclass
class ToolRegistry:
    _cards: dict[str, ToolCard] = field(default_factory=dict)

    def register(self, card: ToolCard) -> ToolCard:
        self._cards[card.tool_id] = card
        return card

    def enable(self, tool_id: str) -> ToolCard:
        c = self._cards[tool_id]
        updated = c.model_copy(update={"enabled": True})
        self._cards[tool_id] = updated
        return updated

    def disable(self, tool_id: str) -> ToolCard:
        c = self._cards[tool_id]
        updated = c.model_copy(update={"enabled": False})
        self._cards[tool_id] = updated
        return updated

    def get(self, tool_id: str) -> ToolCard:
        return self._cards[tool_id]

    def exists(self, tool_id: str) -> bool:
        return tool_id in self._cards

    def list(self) -> list[ToolCard]:
        return list(self._cards.values())
