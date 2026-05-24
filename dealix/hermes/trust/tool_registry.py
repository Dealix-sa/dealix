"""Tool Registry. Mirrors AgentRegistry but for callable side-effects.

A Tool Card (section 127) declares its owner, type, risk level, whether
approval is required, and the per-call data scope. The Tool Gateway
refuses to invoke an unregistered tool.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ToolCard:
    tool_id: str
    name: str
    tool_type: str     # "github" | "email" | "crm" | "mcp" | ...
    owner: str         # human owner — never a bare service account
    risk_level: str = "medium"        # low|medium|high
    enabled: bool = True
    requires_approval: bool = False
    allowed_agents: list[str] = field(default_factory=list)
    data_scope: str = ""              # short, machine-checkable string
    audit_required: bool = True

    def is_high_risk(self) -> bool:
        return self.risk_level == "high"


class ToolRegistry:
    def __init__(self) -> None:
        self._by_id: dict[str, ToolCard] = {}

    def register(self, card: ToolCard) -> ToolCard:
        if not card.owner:
            raise ValueError(f"Tool {card.tool_id} must declare an owner (no-orphan rule).")
        if card.is_high_risk() and not card.requires_approval:
            raise ValueError(f"High-risk tool {card.tool_id} must set requires_approval=True.")
        self._by_id[card.tool_id] = card
        return card

    def get(self, tool_id: str) -> ToolCard:
        if tool_id not in self._by_id:
            raise KeyError(f"Unregistered tool: {tool_id}")
        return self._by_id[tool_id]

    def disable(self, tool_id: str) -> None:
        self._by_id[tool_id].enabled = False

    def enable(self, tool_id: str) -> None:
        self._by_id[tool_id].enabled = True

    def all(self) -> list[ToolCard]:
        return list(self._by_id.values())

    def high_risk(self) -> list[ToolCard]:
        return [t for t in self._by_id.values() if t.is_high_risk()]


__all__ = ["ToolCard", "ToolRegistry"]
