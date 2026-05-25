"""
ToolGate — refuses any tool call where the requesting agent does not
hold the matching capability scope, or where the tool is not in the
platform tool registry.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.control_plane.request_context import RequestContext
from dealix.hermes.identity.agent_identity import AgentIdentity
from dealix.hermes.identity.capability_scope import CAPABILITY_REGISTRY


@dataclass(frozen=True)
class ToolDecision:
    allowed: bool
    reason: str


def evaluate(context: RequestContext, agent: AgentIdentity | None) -> ToolDecision:
    tool_id = context.tool_id
    capability = context.capability

    if capability not in CAPABILITY_REGISTRY:
        return ToolDecision(allowed=False, reason=f"Capability {capability!r} not in registry.")

    # System and Sami actors bypass the agent-specific tool gate
    if agent is None:
        return ToolDecision(allowed=True, reason="Non-agent actor, capability-only check.")

    if capability in agent.forbidden_capabilities:
        return ToolDecision(
            allowed=False,
            reason=f"Capability {capability!r} explicitly forbidden for agent {agent.agent_id!r}.",
        )

    if capability not in agent.capabilities:
        return ToolDecision(
            allowed=False,
            reason=f"Agent {agent.agent_id!r} does not hold capability {capability!r}.",
        )

    if tool_id and tool_id not in agent.allowed_tools:
        return ToolDecision(
            allowed=False,
            reason=f"Tool {tool_id!r} not in agent {agent.agent_id!r} allowlist.",
        )

    return ToolDecision(allowed=True, reason="Capability and tool both allowed.")
