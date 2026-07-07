"""Writers for Dealix internal action and approval queues."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def build_action_queue(plan: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for block in plan.get("planned", []):
        strategy = block.get("strategy", {}).get("name", "unknown")
        for action in block.get("safe_actions", []):
            items.append(
                {
                    "strategy": strategy,
                    "action": action.get("action"),
                    "status": "ready_internal",
                    "requires_founder_approval": False,
                }
            )
    return items


def build_approval_queue(plan: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for action in plan.get("approvals_required", []):
        items.append(
            {
                "strategy": action.get("strategy"),
                "action": action.get("action"),
                "status": "needs_founder_approval",
                "requires_founder_approval": True,
                "reason": action.get("decision", {}).get("reasons", []),
            }
        )
    return items
