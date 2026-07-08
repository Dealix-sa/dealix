"""Approval queue builder for founder-first Dealix runs."""

from __future__ import annotations

from typing import Any


APPROVAL_DECISIONS = ["approve", "edit", "reject", "explain_more"]


def build_approval_items(action_queue: list[dict[str, Any]]) -> list[dict[str, Any]]:
    approvals: list[dict[str, Any]] = []
    for action in action_queue:
        approvals.append(
            {
                "approval_id": f"approval-{action['id']}",
                "action_id": action["id"],
                "summary": action["summary"],
                "target": action["target"],
                "risk_level": action.get("risk_level", "low"),
                "status": "pending_founder_review",
                "allowed_decisions": APPROVAL_DECISIONS,
                "external_action_enabled": False,
                "note": "Draft-only. Founder must approve/edit/reject before any external action.",
            }
        )
    return approvals
