"""Draft-only action queue for Company OS."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .autonomy_levels import AutonomyLevel, classify_action, requires_human_approval


@dataclass(slots=True)
class ActionItem:
    id: str
    action_type: str
    summary: str
    target: str
    risk_level: str = "low"
    status: str = "draft"
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        level = classify_action(self.action_type)
        payload["autonomy_level"] = int(level)
        payload["autonomy_name"] = level.name
        payload["approval_required"] = requires_human_approval(self.action_type) or level >= AutonomyLevel.DRAFT
        return payload


def build_action_queue(opportunities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    for index, opp in enumerate(opportunities, start=1):
        queue.append(
            ActionItem(
                id=f"act-{index:03d}",
                action_type="draft_message",
                summary=f"Draft safe first-touch message for {opp['company_name']}",
                target=opp["id"],
                risk_level=opp.get("risk", "low"),
                evidence=opp.get("evidence", []),
            ).to_dict()
        )
    return queue
