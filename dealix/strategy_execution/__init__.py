"""Dealix Strategy Execution OS — internal, draft-only autonomous growth layer.

This package plans and *internally* executes Dealix growth strategies. It never
sends external messages, never publishes, never charges, and never changes
production. Any action that would touch the outside world is routed to an
approval queue for a human (founder) to review and act on manually.

Autonomy levels:
    0  observe only
    1  analyze and prioritize
    2  draft and recommend
    3  internal execution (reports, files, queues, proof logs)   <- daily default
    4  repo execution (branches, PR drafts, tests, internal patches)
    5  external execution (sending, publishing, payments, prod)  <- BLOCKED

Level 5 is blocked by default and is intentionally not implemented.
"""

from __future__ import annotations

from .schemas import (
    MAX_ENABLED_AUTONOMY_LEVEL,
    Action,
    ApprovalItem,
    AutonomyLevel,
    ProofEvent,
    Strategy,
)

__all__ = [
    "MAX_ENABLED_AUTONOMY_LEVEL",
    "Action",
    "ApprovalItem",
    "AutonomyLevel",
    "ProofEvent",
    "Strategy",
]
