"""خادم الثقة — Permission ladder L0..L6 (spec §38).

Each agent has a permission_level. Each action has a minimum required
level. `evaluate(action_kind, agent_level, sovereignty_level)` returns
True iff the agent is allowed to execute the action given the active
sovereignty regime.

Pure data + pure functions — no I/O.
"""

from __future__ import annotations

from enum import StrEnum

from dealix.hermes.sovereignty import SovereigntyLevel


class PermissionLevel(StrEnum):
    L0_OBSERVE = "l0_observe"
    L1_DRAFT = "l1_draft"
    L2_INTERNAL_TASK = "l2_internal_task"
    L3_INTERNAL_UPDATE = "l3_internal_update"
    L4_EXTERNAL_WITH_APPROVAL = "l4_external_with_approval"
    L5_LOW_RISK_AUTONOMOUS = "l5_low_risk_autonomous"
    L6_NEVER_AUTONOMOUS = "l6_never_autonomous"

    @property
    def numeric(self) -> int:
        return {
            "l0_observe": 0,
            "l1_draft": 1,
            "l2_internal_task": 2,
            "l3_internal_update": 3,
            "l4_external_with_approval": 4,
            "l5_low_risk_autonomous": 5,
            "l6_never_autonomous": 6,
        }[self.value]

    def at_least(self, other: PermissionLevel) -> bool:
        return self.numeric >= other.numeric


class ActionKind(StrEnum):
    OBSERVE = "observe"
    DRAFT = "draft"
    INTERNAL_TASK = "internal_task"
    INTERNAL_UPDATE = "internal_update"
    EXTERNAL_LOW_RISK = "external_low_risk"
    EXTERNAL_HIGH_RISK = "external_high_risk"
    PUBLIC_COMMITMENT = "public_commitment"
    SOVEREIGN_DECISION = "sovereign_decision"


# Spec §38 — minimum agent level required per action kind.
PermissionMatrix: dict[ActionKind, PermissionLevel] = {
    ActionKind.OBSERVE: PermissionLevel.L0_OBSERVE,
    ActionKind.DRAFT: PermissionLevel.L1_DRAFT,
    ActionKind.INTERNAL_TASK: PermissionLevel.L2_INTERNAL_TASK,
    ActionKind.INTERNAL_UPDATE: PermissionLevel.L3_INTERNAL_UPDATE,
    ActionKind.EXTERNAL_LOW_RISK: PermissionLevel.L5_LOW_RISK_AUTONOMOUS,
    ActionKind.EXTERNAL_HIGH_RISK: PermissionLevel.L4_EXTERNAL_WITH_APPROVAL,
    ActionKind.PUBLIC_COMMITMENT: PermissionLevel.L6_NEVER_AUTONOMOUS,
    ActionKind.SOVEREIGN_DECISION: PermissionLevel.L6_NEVER_AUTONOMOUS,
}

# Action kinds that ALWAYS require human approval, regardless of agent
# permission level.
APPROVAL_REQUIRED_ACTIONS: frozenset[ActionKind] = frozenset(
    {
        ActionKind.EXTERNAL_HIGH_RISK,
        ActionKind.PUBLIC_COMMITMENT,
        ActionKind.SOVEREIGN_DECISION,
    }
)


def requires_approval(action_kind: ActionKind | str) -> bool:
    kind = ActionKind(action_kind) if isinstance(action_kind, str) else action_kind
    return kind in APPROVAL_REQUIRED_ACTIONS


def evaluate(
    action_kind: ActionKind | str,
    agent_level: PermissionLevel | str,
    sovereignty_level: SovereigntyLevel | str = SovereigntyLevel.S0_AUTONOMOUS,
) -> bool:
    """Allow / deny check.

    Rules:
      1. Look up the minimum PermissionLevel for the action.
      2. The agent must meet or exceed it.
      3. If the sovereignty level is S4_NEVER, always deny.
      4. If the action requires approval AND sovereignty is S0 (no human in
         the loop), deny — approval cannot be granted out of thin air.
    """
    kind = ActionKind(action_kind) if isinstance(action_kind, str) else action_kind
    level = PermissionLevel(agent_level) if isinstance(agent_level, str) else agent_level
    sov = (
        SovereigntyLevel(sovereignty_level)
        if isinstance(sovereignty_level, str)
        else sovereignty_level
    )

    if sov == SovereigntyLevel.S4_NEVER:
        return False

    minimum = PermissionMatrix[kind]
    if not level.at_least(minimum):
        return False

    if requires_approval(kind) and sov == SovereigntyLevel.S0_AUTONOMOUS:
        return False
    return True


__all__ = [
    "APPROVAL_REQUIRED_ACTIONS",
    "ActionKind",
    "PermissionLevel",
    "PermissionMatrix",
    "evaluate",
    "requires_approval",
]
