"""
Permission Matrix — the canonical check that gates every action.

Permissions are decided by the combination of:
  - agent's max sovereignty level
  - tool's risk level + enabled flag
  - action's external_action flag and permission_level
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.schemas import PermissionLevel, SovereigntyLevel
from dealix.hermes.trust.agent_registry import get_agent_registry
from dealix.hermes.trust.tool_registry import get_tool_registry


_LEVEL_ORDER = {
    SovereigntyLevel.S0_AGENT_FREE.value: 0,
    SovereigntyLevel.S1_INTERNAL.value: 1,
    SovereigntyLevel.S2_SAMI_APPROVAL.value: 2,
    SovereigntyLevel.S3_SAMI_REVIEW.value: 3,
    SovereigntyLevel.S4_SOVEREIGN_ONLY.value: 4,
    SovereigntyLevel.S5_NEVER_AUTONOMOUS.value: 5,
}


@dataclass
class PermissionDecision:
    allowed: bool
    requires_approval: bool
    reason: str


class PermissionMatrix:
    def check(
        self,
        *,
        agent_id: str,
        tool_id: str,
        action_sovereignty: SovereigntyLevel | str,
        permission_level: PermissionLevel | str = PermissionLevel.L1_DRAFT,
        external_action: bool = False,
    ) -> PermissionDecision:
        agent = get_agent_registry().get(agent_id)
        tool = get_tool_registry().get(tool_id)

        if agent is None:
            return PermissionDecision(False, False, "agent_not_registered")
        if tool is None:
            return PermissionDecision(False, False, "tool_not_registered")
        if not get_agent_registry().can_use_tool(agent_id, tool_id):
            return PermissionDecision(False, False, "agent_forbidden_from_tool")

        action_sov = SovereigntyLevel(action_sovereignty).value
        agent_max = agent.max_sovereignty_level
        if action_sov == SovereigntyLevel.S5_NEVER_AUTONOMOUS.value:
            return PermissionDecision(False, False, "s5_never_autonomous")
        # Above the agent's max: the action can be planned, but it MUST be
        # routed through Sami's approval (it cannot run autonomously).
        sovereignty_escalated = _LEVEL_ORDER[action_sov] > _LEVEL_ORDER[agent_max]
        if not tool.enabled:
            return PermissionDecision(
                False,
                True,
                f"tool_disabled_requires_owner_enable:{tool.id}",
            )
        requires_approval = (
            sovereignty_escalated
            or tool.requires_approval
            or external_action
            or PermissionLevel(permission_level)
            in {PermissionLevel.L3_EXTERNAL_SEND, PermissionLevel.L4_COMMITMENT}
            or action_sov
            in {
                SovereigntyLevel.S2_SAMI_APPROVAL.value,
                SovereigntyLevel.S4_SOVEREIGN_ONLY.value,
            }
        )
        return PermissionDecision(True, requires_approval, "ok")


_default_matrix: PermissionMatrix | None = None


def get_permission_matrix() -> PermissionMatrix:
    global _default_matrix
    if _default_matrix is None:
        _default_matrix = PermissionMatrix()
    return _default_matrix
