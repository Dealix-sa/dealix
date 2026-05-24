"""Permission Matrix.

Joins agents and tools. A call is allowed only if:

  * Agent is registered + enabled.
  * Tool is registered + enabled.
  * Tool's ``allowed_agents`` list contains the agent (or is empty AND
    agent's ``allowed_tools`` list contains the tool).
  * The tool isn't in the agent's ``forbidden_tools``.

Returns a structured verdict so the gateway can log + audit it.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.trust.agent_registry import AgentRegistry
from dealix.hermes.trust.tool_registry import ToolRegistry


@dataclass(frozen=True)
class PermissionVerdict:
    allowed: bool
    reason: str
    requires_approval: bool = False


class PermissionMatrix:
    def __init__(self, agents: AgentRegistry, tools: ToolRegistry) -> None:
        self._agents = agents
        self._tools = tools

    def check(self, *, agent_id: str, tool_id: str) -> PermissionVerdict:
        try:
            agent = self._agents.get(agent_id)
        except KeyError:
            return PermissionVerdict(False, f"Agent '{agent_id}' is not registered.")
        try:
            tool = self._tools.get(tool_id)
        except KeyError:
            return PermissionVerdict(False, f"Tool '{tool_id}' is not registered.")

        if not agent.enabled:
            return PermissionVerdict(False, f"Agent '{agent_id}' is disabled.")
        if not tool.enabled:
            return PermissionVerdict(False, f"Tool '{tool_id}' is disabled.")
        if tool_id in agent.forbidden_tools:
            return PermissionVerdict(False, f"Tool '{tool_id}' is in agent's forbidden_tools.")

        agent_allows = (not agent.allowed_tools) or tool_id in agent.allowed_tools
        tool_allows = (not tool.allowed_agents) or agent_id in tool.allowed_agents
        if not (agent_allows and tool_allows):
            return PermissionVerdict(False, "Permission matrix denies this agent×tool pair.")

        return PermissionVerdict(True, "Permission granted.", requires_approval=tool.requires_approval)


__all__ = ["PermissionMatrix", "PermissionVerdict"]
