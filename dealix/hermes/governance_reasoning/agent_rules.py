"""Per-agent capability scope."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AgentCapabilities:
    agent_id: str
    capabilities: frozenset[str]
    max_autonomy_level: int = 1


@dataclass(frozen=True)
class AgentRuleResult:
    allowed: bool
    reason: str = ""


_AGENTS: dict[str, AgentCapabilities] = {}


def register_agent(agent: AgentCapabilities) -> None:
    """Register or replace an agent's capability declaration."""
    _AGENTS[agent.agent_id] = agent


def get_agent(agent_id: str) -> AgentCapabilities | None:
    """Return the AgentCapabilities for agent_id, or None if absent."""
    return _AGENTS.get(agent_id)


def evaluate(agent_id: str, action: str, required_autonomy: int = 1) -> AgentRuleResult:
    """Return whether the agent is permitted to take action at the requested autonomy level."""
    agent = _AGENTS.get(agent_id)
    if agent is None:
        return AgentRuleResult(allowed=False, reason=f"agent {agent_id} not registered")
    if action not in agent.capabilities:
        return AgentRuleResult(allowed=False, reason=f"agent {agent_id} lacks capability {action}")
    if required_autonomy > agent.max_autonomy_level:
        return AgentRuleResult(
            allowed=False,
            reason=f"agent {agent_id} autonomy {agent.max_autonomy_level} < required {required_autonomy}",
        )
    return AgentRuleResult(allowed=True)


def clear() -> None:
    """Clear the agent registry (test helper)."""
    _AGENTS.clear()
