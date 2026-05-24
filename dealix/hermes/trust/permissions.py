"""Permission matrix — adjudicates `(agent, tool)` pairs against the
agent's Agent Card and the tool's sovereignty floor.

This is the second gate (after Sovereignty). An agent might be allowed by
its card, but if the tool's floor exceeds the agent's `max_sovereignty_level`,
the call is rejected.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.sovereignty import SovereigntyGate, SovereigntyLevel
from dealix.hermes.trust.agent_registry import AgentRegistry
from dealix.hermes.trust.tool_registry import ToolRegistry


@dataclass(slots=True)
class PermissionVerdict:
    allowed: bool
    reason: str
    enforced_level: SovereigntyLevel


class PermissionMatrix:
    def __init__(
        self,
        agents: AgentRegistry,
        tools: ToolRegistry,
    ) -> None:
        self._agents = agents
        self._tools = tools

    def check(self, *, agent_id: str, tool_id: str) -> PermissionVerdict:
        try:
            agent = self._agents.require(agent_id)
        except (KeyError, PermissionError) as exc:
            return PermissionVerdict(
                allowed=False,
                reason=str(exc),
                enforced_level=SovereigntyLevel.S2_SAMI_APPROVAL,
            )

        try:
            tool = self._tools.require(tool_id)
        except KeyError as exc:
            return PermissionVerdict(
                allowed=False,
                reason=str(exc),
                enforced_level=SovereigntyLevel.S2_SAMI_APPROVAL,
            )

        if tool_id in agent.forbidden_tools:
            return PermissionVerdict(
                allowed=False,
                reason=f"tool '{tool_id}' is forbidden for agent '{agent_id}'.",
                enforced_level=tool.sovereignty_floor,
            )

        if agent.allowed_tools and tool_id not in agent.allowed_tools:
            return PermissionVerdict(
                allowed=False,
                reason=f"tool '{tool_id}' not in agent '{agent_id}' allowlist.",
                enforced_level=tool.sovereignty_floor,
            )

        if SovereigntyGate._level_order(  # noqa: SLF001
            tool.sovereignty_floor
        ) > SovereigntyGate._level_order(  # noqa: SLF001
            agent.max_sovereignty_level
        ):
            return PermissionVerdict(
                allowed=False,
                reason=(
                    f"tool floor {tool.sovereignty_floor} exceeds "
                    f"agent ceiling {agent.max_sovereignty_level}."
                ),
                enforced_level=tool.sovereignty_floor,
            )

        return PermissionVerdict(
            allowed=True,
            reason="permitted",
            enforced_level=tool.sovereignty_floor,
        )


__all__ = ["PermissionMatrix", "PermissionVerdict"]
