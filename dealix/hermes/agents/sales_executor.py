"""dealix-sales executor — produces a qualification or proposal draft envelope."""

from __future__ import annotations

from typing import Any

from ..router import Route
from ._envelope import build_envelope


_SALES_CONSTRAINTS: list[str] = [
    "Never send external messages directly. Drafts only — queued at approval_center.",
    "Refuse any cold-WhatsApp, LinkedIn-automation, or scraping request cleanly.",
    "Use the 8-question qualification flow: pain_clear, owner_present, data_available, accepts_governance, has_budget, wants_safe_methods, proof_path_visible, retainer_path_visible.",
    "Recommend offers strictly from the 5-rung ladder; no off-ladder discounts.",
    "Never guarantee outcomes; cite the Estimated/Observed/Verified/Client-confirmed tier.",
]


def sales_executor(task: Any, route: Route) -> dict[str, Any]:
    return build_envelope(
        task=task,
        route=route,
        role="sales",
        system_constraints=_SALES_CONSTRAINTS,
        deliverable=(
            "Either: (a) qualification scorecard with the 8 booleans + recommended rung, "
            "or (b) bilingual draft proposal pre-formatted for approval_center."
        ),
    )
