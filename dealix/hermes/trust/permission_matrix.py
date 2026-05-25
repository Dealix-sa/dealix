"""Permission Matrix — agent × tool × workspace."""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.trust.agent_registry import AgentRegistry
from dealix.hermes.trust.tool_registry import ToolRegistry


@dataclass
class PermissionMatrix:
    agents: AgentRegistry
    tools: ToolRegistry
    _explicit_denies: set[tuple[str, str, str]] = field(default_factory=set)

    def deny(self, agent_id: str, tool_id: str, workspace_id: str) -> None:
        self._explicit_denies.add((agent_id, tool_id, workspace_id))

    def can_invoke(self, *, agent_id: str, tool_id: str, workspace_id: str) -> bool:
        if (agent_id, tool_id, workspace_id) in self._explicit_denies:
            return False
        if not self.agents.exists(agent_id) or not self.tools.exists(tool_id):
            return False
        agent = self.agents.get(agent_id)
        tool = self.tools.get(tool_id)
        if not agent.active or not tool.enabled:
            return False
        if tool_id in agent.forbidden_tools:
            return False
        if tool_id not in agent.allowed_tools:
            return False
        if tool.allowed_agents and agent_id not in tool.allowed_agents:
            return False
        return True
