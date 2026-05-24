"""Agent + tool registries.

The orchestrator consults these registries on every step:
  * `AgentRegistry` knows which agents exist, their mission, their max
    sovereignty level, and which tools they may use.
  * `ToolRegistry` knows risk level, owner, and audit requirements for
    every tool — MCP tools delegate the cryptographic checks to
    `mcp_security.MCPRegistry`.

Both registries are in-process, deterministic, and JSON-exportable so
they fit naturally inside the Sovereign Console and the test suite.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.hermes.trust.mcp_security import MCPRiskLevel


@dataclass
class AgentCard:
    id: str
    name: str
    mission: str
    domain: str
    owner: str
    max_sovereignty_level: SovereigntyLevel
    allowed_tools: list[str] = field(default_factory=list)
    forbidden_tools: list[str] = field(default_factory=list)
    kpis: list[str] = field(default_factory=list)

    def can_use(self, tool_id: str) -> bool:
        if tool_id in self.forbidden_tools:
            return False
        if not self.allowed_tools:
            return False
        return tool_id in self.allowed_tools

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "mission": self.mission,
            "domain": self.domain,
            "owner": self.owner,
            "max_sovereignty_level": self.max_sovereignty_level.name,
            "allowed_tools": list(self.allowed_tools),
            "forbidden_tools": list(self.forbidden_tools),
            "kpis": list(self.kpis),
        }


@dataclass
class ToolCard:
    id: str
    description: str
    risk_level: MCPRiskLevel
    owner: str
    requires_approval: bool = False
    allowed_agents: list[str] = field(default_factory=list)
    data_scope: str = "tenant_only"
    audit_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "risk_level": self.risk_level.value,
            "owner": self.owner,
            "requires_approval": self.requires_approval,
            "allowed_agents": list(self.allowed_agents),
            "data_scope": self.data_scope,
            "audit_required": self.audit_required,
        }


class AgentRegistry:
    def __init__(self) -> None:
        self._by_id: dict[str, AgentCard] = {}

    def register(self, card: AgentCard) -> AgentCard:
        self._by_id[card.id] = card
        return card

    def get(self, agent_id: str) -> AgentCard | None:
        return self._by_id.get(agent_id)

    def all(self) -> list[AgentCard]:
        return list(self._by_id.values())

    def snapshot(self) -> list[dict[str, Any]]:
        return [c.to_dict() for c in self._by_id.values()]


class ToolRegistry:
    def __init__(self) -> None:
        self._by_id: dict[str, ToolCard] = {}

    def register(self, card: ToolCard) -> ToolCard:
        self._by_id[card.id] = card
        return card

    def get(self, tool_id: str) -> ToolCard | None:
        return self._by_id.get(tool_id)

    def can_agent_call(self, agent: AgentCard, tool_id: str) -> tuple[bool, str]:
        tool = self.get(tool_id)
        if tool is None:
            return False, f"tool {tool_id!r} not registered"
        if not agent.can_use(tool_id):
            return False, f"agent {agent.id!r} not authorised for {tool_id!r}"
        if tool.allowed_agents and agent.id not in tool.allowed_agents:
            return False, f"tool {tool_id!r} restricts agents"
        if tool.risk_level == MCPRiskLevel.BLOCKED:
            return False, f"tool {tool_id!r} is blocked"
        return True, "ok"

    def all(self) -> list[ToolCard]:
        return list(self._by_id.values())

    def snapshot(self) -> list[dict[str, Any]]:
        return [c.to_dict() for c in self._by_id.values()]


def build_default_registries() -> tuple[AgentRegistry, ToolRegistry]:
    """Seed the registries with Hermes' canonical agents and tools.

    Keep this list small and explicit — anything else has to be added
    by the founder, never autodiscovered.
    """
    agents = AgentRegistry()
    tools = ToolRegistry()

    tools.register(
        ToolCard(
            id="read_leads",
            description="Read leads from the internal lead inbox.",
            risk_level=MCPRiskLevel.LOW,
            owner="Sami",
            data_scope="tenant_only",
        )
    )
    tools.register(
        ToolCard(
            id="score_opportunity",
            description="Compute opportunity score from a signal.",
            risk_level=MCPRiskLevel.LOW,
            owner="Sami",
        )
    )
    tools.register(
        ToolCard(
            id="draft_message",
            description="Draft an outbound message — never sends.",
            risk_level=MCPRiskLevel.LOW,
            owner="Sami",
        )
    )
    tools.register(
        ToolCard(
            id="draft_proposal",
            description="Draft an external proposal from a template.",
            risk_level=MCPRiskLevel.MEDIUM,
            owner="Sami",
            requires_approval=True,
        )
    )
    tools.register(
        ToolCard(
            id="send_external",
            description="Send an external message — requires approval.",
            risk_level=MCPRiskLevel.HIGH,
            owner="Sami",
            requires_approval=True,
        )
    )
    tools.register(
        ToolCard(
            id="sign_contract",
            description="Sign a binding contract.",
            risk_level=MCPRiskLevel.BLOCKED,
            owner="Sami",
            requires_approval=True,
        )
    )

    agents.register(
        AgentCard(
            id="revenue_hunter",
            name="Hermes Revenue Hunter",
            mission="Find monetizable opportunities and draft outreach.",
            domain="money",
            owner="Sami",
            max_sovereignty_level=SovereigntyLevel.L2_INTERNAL_TASK,
            allowed_tools=["read_leads", "score_opportunity", "draft_message"],
            forbidden_tools=["send_external", "sign_contract"],
            kpis=["qualified_opportunities", "messages_drafted", "meetings_booked"],
        )
    )
    agents.register(
        AgentCard(
            id="proposal_factory",
            name="Hermes Proposal Factory",
            mission="Turn an opportunity into a ready-to-send proposal draft.",
            domain="money",
            owner="Sami",
            max_sovereignty_level=SovereigntyLevel.L2_INTERNAL_TASK,
            allowed_tools=["read_leads", "draft_proposal"],
            forbidden_tools=["send_external", "sign_contract"],
            kpis=["proposals_drafted", "proposals_accepted"],
        )
    )
    agents.register(
        AgentCard(
            id="followup_commander",
            name="Hermes Follow-up Commander",
            mission="Plan and draft follow-ups; never sends without approval.",
            domain="money",
            owner="Sami",
            max_sovereignty_level=SovereigntyLevel.L2_INTERNAL_TASK,
            allowed_tools=["read_leads", "draft_message"],
            forbidden_tools=["send_external", "sign_contract"],
            kpis=["followups_drafted", "replies_received"],
        )
    )

    return agents, tools


_default_agents, _default_tools = build_default_registries()


def default_agent_registry() -> AgentRegistry:
    return _default_agents


def default_tool_registry() -> ToolRegistry:
    return _default_tools
