"""
Agent + tool registry.

Single source of truth for what agents and tools exist in the Kernel,
who owns them, and what sovereignty level they can operate at.
"""

from __future__ import annotations

from pydantic import BaseModel

from dealix.hermes.sovereignty import SovereigntyLevel


class AgentRecord(BaseModel):
    agent_id: str
    owner: str
    description: str
    max_sovereignty_level: SovereigntyLevel = SovereigntyLevel.S1_INTERNAL
    enabled: bool = True


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, AgentRecord] = {}

    def register(self, agent: AgentRecord) -> None:
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> AgentRecord | None:
        return self._agents.get(agent_id)

    def list_all(self) -> list[AgentRecord]:
        return list(self._agents.values())


_default_registry = AgentRegistry()

# Seed core agents — all internal-only by default.
for _agent in (
    AgentRecord(
        agent_id="founder_brief",
        owner="sami",
        description="Daily sovereign brief: cash, risk, top opportunities.",
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
    ),
    AgentRecord(
        agent_id="opportunity_mapper",
        owner="sami",
        description="Maps signals to opportunities and scores them.",
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
    ),
    AgentRecord(
        agent_id="trust_checker",
        owner="sami",
        description="Runs guardrails on every external-bound draft.",
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
    ),
    AgentRecord(
        agent_id="asset_builder",
        owner="sami",
        description="Promotes outcomes to reusable assets.",
        max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
    ),
):
    _default_registry.register(_agent)


def default_registry() -> AgentRegistry:
    return _default_registry
