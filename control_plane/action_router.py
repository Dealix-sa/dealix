"""Action Router.

Every proposed action inside Dealix is routed to one of five paths:

    1. EXECUTE   -- low-risk internal action, run automatically
    2. DRAFT     -- AI prepares, founder reviews
    3. APPROVE   -- requires explicit founder approval before sending
    4. ESCALATE  -- high-risk or ambiguous; raise to CEO Decision Queue
    5. BLOCK     -- never allowed (A3 surface)

The full doctrine lives in ``docs/control_plane/ACTION_ROUTER.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ActionPath(str, Enum):
    EXECUTE = "execute"
    DRAFT = "draft"
    APPROVE = "approve"
    ESCALATE = "escalate"
    BLOCK = "block"


@dataclass(frozen=True)
class RoutedAction:
    name: str
    path: ActionPath
    reason: str


# Patterns are matched case-insensitively against the action name. First
# match wins, in the order BLOCK -> ESCALATE -> APPROVE -> DRAFT -> EXECUTE.
_BLOCK_PATTERNS: tuple[str, ...] = (
    "guaranteed revenue",
    "guarantee sales",
    "contract change",
    "sensitive data export",
    "refund approval",
)

_ESCALATE_PATTERNS: tuple[str, ...] = (
    "legal",
    "compliance claim",
    "sensitive data",
    "incident",
)

_APPROVE_PATTERNS: tuple[str, ...] = (
    "proposal sending",
    "send proposal",
    "client delivery",
    "pricing exception",
    "public case study",
)

_DRAFT_PATTERNS: tuple[str, ...] = (
    "outreach message",
    "proposal draft",
    "content post",
)

_EXECUTE_PATTERNS: tuple[str, ...] = (
    "update crm stage",
    "deduplicate leads",
    "calculate score",
)


class ActionRouter:
    """Pattern-based router. Real implementation can later swap in a
    policy engine; the interface stays the same."""

    def route(self, action_name: str) -> RoutedAction:
        needle = action_name.lower()

        for pattern in _BLOCK_PATTERNS:
            if pattern in needle:
                return RoutedAction(action_name, ActionPath.BLOCK, f"matches block: {pattern}")

        for pattern in _ESCALATE_PATTERNS:
            if pattern in needle:
                return RoutedAction(
                    action_name, ActionPath.ESCALATE, f"matches escalate: {pattern}"
                )

        for pattern in _APPROVE_PATTERNS:
            if pattern in needle:
                return RoutedAction(action_name, ActionPath.APPROVE, f"matches approve: {pattern}")

        for pattern in _DRAFT_PATTERNS:
            if pattern in needle:
                return RoutedAction(action_name, ActionPath.DRAFT, f"matches draft: {pattern}")

        for pattern in _EXECUTE_PATTERNS:
            if pattern in needle:
                return RoutedAction(action_name, ActionPath.EXECUTE, f"matches execute: {pattern}")

        # Unknown actions default to ESCALATE -- the safe default is to
        # ask the CEO rather than silently auto-run something untyped.
        return RoutedAction(action_name, ActionPath.ESCALATE, "unknown action; default escalate")
