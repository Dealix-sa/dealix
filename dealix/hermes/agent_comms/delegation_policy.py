"""Delegation policy: an agent cannot delegate what it cannot do itself."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Agent:
    agent_id: str
    capabilities: frozenset[str]


@dataclass(frozen=True)
class DelegationResult:
    allowed: bool
    reason: str = ""


def can_delegate(agent: Agent, action: str) -> bool:
    """Return True only when action is within the agent's declared capabilities."""
    return action in agent.capabilities


def delegate(agent: Agent, delegate_agent: Agent, action: str) -> DelegationResult:
    """Reject delegation if the delegating agent lacks the capability for action."""
    if not can_delegate(agent, action):
        return DelegationResult(allowed=False, reason=f"{agent.agent_id} lacks capability {action}")
    if not can_delegate(delegate_agent, action):
        return DelegationResult(allowed=False, reason=f"{delegate_agent.agent_id} lacks capability {action}")
    return DelegationResult(allowed=True)
