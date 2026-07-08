"""Builds the action queue and the human approval queue from classified actions."""

from __future__ import annotations

from .schemas import Action, ApprovalItem


def split_queues(actions: list[Action]) -> tuple[list[Action], list[ApprovalItem]]:
    """Return (executed/internal actions, approval items) from classified actions.

    Any action whose status requires human review becomes an ApprovalItem. Blocked
    live actions are also surfaced as approval items so the founder sees them, but
    they are clearly marked as blocked.
    """

    approvals: list[ApprovalItem] = []
    for action in actions:
        if action.status in {"queued_for_approval", "blocked"}:
            reason = (
                "Blocked live action — do not auto-run; manual decision only"
                if action.status == "blocked"
                else "External-facing draft — founder must review before any send"
            )
            approvals.append(
                ApprovalItem(
                    strategy=action.strategy,
                    title=action.title,
                    action_type=action.action_type,
                    reason=reason,
                    draft=action.detail,
                )
            )
    return actions, approvals
