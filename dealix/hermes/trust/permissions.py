"""
Permission matrix — what an agent is allowed to do, expressed against the
sovereignty levels in ``dealix.hermes.sovereignty``.

Designed to be a simple lookup that the Orchestrator (and any future
agent runtime) consults before dispatching.
"""

from __future__ import annotations

from pydantic import BaseModel

from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.hermes.trust.registry import default_registry as default_agent_registry


class PermissionDecision(BaseModel):
    allowed: bool
    reason: str


def can_agent_run(agent_id: str, action_level: SovereigntyLevel) -> PermissionDecision:
    """Return whether ``agent_id`` may execute an action at ``action_level``."""
    agent = default_agent_registry().get(agent_id)
    if agent is None:
        return PermissionDecision(allowed=False, reason=f"Unknown agent: {agent_id}")
    if not agent.enabled:
        return PermissionDecision(allowed=False, reason=f"Agent disabled: {agent_id}")

    order = [
        SovereigntyLevel.S0_AUTO_SAFE,
        SovereigntyLevel.S1_INTERNAL,
        SovereigntyLevel.S2_SAMI_APPROVAL,
        SovereigntyLevel.S3_SOVEREIGN_MEMO,
        SovereigntyLevel.S4_SOVEREIGN_ONLY,
        SovereigntyLevel.S5_NEVER_AUTONOMOUS,
    ]
    requested_idx = order.index(action_level)
    max_idx = order.index(agent.max_sovereignty_level)

    if requested_idx <= max_idx:
        return PermissionDecision(allowed=True, reason="Within agent permission envelope.")
    return PermissionDecision(
        allowed=False,
        reason=(
            f"Action level {action_level.value} exceeds agent ceiling "
            f"{agent.max_sovereignty_level.value}; requires Sami."
        ),
    )
