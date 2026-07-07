"""Internal content queue builder for Dealix."""

from __future__ import annotations

from typing import Any


def build_content_queue(plan: dict[str, Any]) -> list[dict[str, Any]]:
    strategy_names = [block.get("strategy", {}).get("name", "unknown") for block in plan.get("planned", [])]
    assets: list[dict[str, Any]] = []

    for name in strategy_names:
        assets.append(
            {
                "strategy": name,
                "type": "internal_content_idea",
                "title": f"Founder update draft for {name}",
                "status": "draft_only",
                "approval_required": True,
            }
        )

    return assets
