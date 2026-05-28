"""dealix-content executor — produces a bilingual content envelope."""

from __future__ import annotations

from typing import Any

from ..router import Route
from ._envelope import build_envelope


_CONTENT_CONSTRAINTS: list[str] = [
    "Bilingual AR + EN with parallel sections, not duplicated translation.",
    "Never invent customer names, metrics, or outcomes.",
    "No marketing fluff. No emojis. No model identifiers.",
    "Every customer-facing markdown ends with: 'Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة'.",
    "Never write code or tests.",
]


def content_executor(task: Any, route: Route) -> dict[str, Any]:
    return build_envelope(
        task=task,
        route=route,
        role="content",
        system_constraints=_CONTENT_CONSTRAINTS,
        deliverable=(
            "Markdown deliverable with parallel AR/EN sections, ending with the "
            "bilingual disclaimer. Include the target audience and intended channel."
        ),
    )
