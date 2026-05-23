"""
Autonomy policy.

A central rule-set defining which agents can take which actions without
human-in-the-loop. Read by the action router before any agent execution.
"""
from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_AUTO_ACTIONS: frozenset[str] = frozenset({
    "read_public_repo",
    "compute_score",
    "render_internal_brief",
    "add_to_suppression_list",
    "write_internal_audit_record",
    "generate_internal_draft",
    "run_verify_script",
})


_BLOCKED_ACTIONS: frozenset[str] = frozenset({
    "send_external_message",
    "publish_to_landing_page",
    "issue_refund",
    "remove_from_suppression_list",
    "publish_public_claim",
    "delete_audit_record",
    "modify_doctrine",
})


@dataclass(frozen=True, slots=True)
class AutonomyDecision:
    action: str
    allowed: bool
    reason: str


def evaluate(action: str) -> AutonomyDecision:
    if action in _BLOCKED_ACTIONS:
        return AutonomyDecision(action, False, "Action is blocked by autonomy policy.")
    if action in _ALLOWED_AUTO_ACTIONS:
        return AutonomyDecision(action, True, "Action is auto-allowed by autonomy policy.")
    return AutonomyDecision(action, False, "Action requires explicit approval.")
