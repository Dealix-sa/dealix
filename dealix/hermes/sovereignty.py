"""Sovereignty levels — the founder is the only commercial authority.

Every action, decision, agent and tool carries a SovereigntyLevel that
declares who is allowed to perform it. Levels are deliberately ordered
so callers can do `level >= SovereigntyLevel.S2_SAMI_APPROVAL` to know
when human approval is required.

L0 — observe
L1 — draft internally
L2 — internal task (no external surface)
L3 — internal update (write to ledgers)
L4 — external action that requires approval
L5 — low-risk autonomous (only after explicit policy)
L6 — never autonomous (sovereign-only)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Final


class SovereigntyLevel(IntEnum):
    """Ordered authority levels. Higher = more restricted."""

    L0_OBSERVE = 0
    L1_DRAFT = 1
    L2_INTERNAL_TASK = 2
    L3_INTERNAL_UPDATE = 3
    L4_EXTERNAL_APPROVAL = 4
    L5_LOW_RISK_AUTONOMOUS = 5
    L6_SOVEREIGN_ONLY = 6


# Friendly aliases used in payloads and docs.
S0_OBSERVE: Final = SovereigntyLevel.L0_OBSERVE
S1_INTERNAL: Final = SovereigntyLevel.L2_INTERNAL_TASK
S2_SAMI_APPROVAL: Final = SovereigntyLevel.L4_EXTERNAL_APPROVAL
S3_SOVEREIGN_MEMO: Final = SovereigntyLevel.L6_SOVEREIGN_ONLY


# Actions that may never be executed autonomously, regardless of agent.
SOVEREIGN_ONLY_ACTIONS: Final[frozenset[str]] = frozenset(
    {
        "sign_contract",
        "issue_invoice_external",
        "send_external_proposal",
        "claim_partnership",
        "publish_public_statement",
        "transfer_funds",
        "make_public_pricing_change",
        "commit_legal_obligation",
        "acquire_company",
        "release_to_press",
    }
)


@dataclass(frozen=True)
class SovereigntyDecision:
    """Result of evaluating an action against the sovereignty gate."""

    allowed: bool
    level: SovereigntyLevel
    requires_approval: bool
    reason: str
    approvers_needed: int = 0

    @property
    def is_blocked(self) -> bool:
        return not self.allowed


def required_level_for(action: str) -> SovereigntyLevel:
    """Map an action name to its minimum sovereignty level."""
    if action in SOVEREIGN_ONLY_ACTIONS:
        return SovereigntyLevel.L6_SOVEREIGN_ONLY
    if action.startswith("send_external") or action.startswith("publish_"):
        return SovereigntyLevel.L4_EXTERNAL_APPROVAL
    if action.startswith("update_") or action.startswith("write_"):
        return SovereigntyLevel.L3_INTERNAL_UPDATE
    if action.startswith("draft_") or action.startswith("propose_"):
        return SovereigntyLevel.L1_DRAFT
    if action.startswith("read_") or action.startswith("score_"):
        return SovereigntyLevel.L0_OBSERVE
    # Unknown actions default to requiring approval — safe by default.
    return SovereigntyLevel.L4_EXTERNAL_APPROVAL


def evaluate(
    action: str,
    agent_max_level: SovereigntyLevel = SovereigntyLevel.L2_INTERNAL_TASK,
) -> SovereigntyDecision:
    """Check if an agent with `agent_max_level` may run `action`."""
    required = required_level_for(action)

    if required >= SovereigntyLevel.L6_SOVEREIGN_ONLY:
        return SovereigntyDecision(
            allowed=False,
            level=required,
            requires_approval=True,
            reason=f"Action '{action}' is sovereign-only and never autonomous.",
            approvers_needed=1,
        )

    if required >= SovereigntyLevel.L4_EXTERNAL_APPROVAL:
        return SovereigntyDecision(
            allowed=False,
            level=required,
            requires_approval=True,
            reason=f"Action '{action}' requires founder approval.",
            approvers_needed=1,
        )

    if required > agent_max_level:
        return SovereigntyDecision(
            allowed=False,
            level=required,
            requires_approval=True,
            reason=(
                f"Agent max level {agent_max_level.name} below required "
                f"{required.name} for action '{action}'."
            ),
            approvers_needed=1,
        )

    return SovereigntyDecision(
        allowed=True,
        level=required,
        requires_approval=False,
        reason="within agent authority",
    )
