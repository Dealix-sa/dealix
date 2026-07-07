"""Learning-note builder for daily strategy execution."""

from __future__ import annotations

from typing import Any


def build_learning_notes(plan: dict[str, Any], proof_log: dict[str, Any]) -> dict[str, Any]:
    return {
        "date": plan.get("date"),
        "what_to_repeat": ["Use proof-backed artifacts", "Keep external work approval-first"],
        "what_to_watch": ["critical technical blockers", "draft quality", "approval queue size"],
        "tomorrow_focus": [
            block.get("strategy", {}).get("name", "unknown") for block in plan.get("planned", [])[:3]
        ],
        "metrics": {
            "strategies_count": proof_log.get("strategies_count", 0),
            "internal_actions_count": proof_log.get("internal_actions_count", 0),
            "approval_items_count": proof_log.get("approval_items_count", 0),
        },
    }
