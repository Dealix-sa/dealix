"""dealix-delivery executor — produces a sprint-step envelope."""

from __future__ import annotations

from typing import Any

from ..router import Route
from ._envelope import build_envelope


_DELIVERY_CONSTRAINTS: list[str] = [
    "Follow the 7-day Revenue Intelligence Sprint: Source Passport → DQ score → Account scoring → Draft pack → Governance review → Proof Pack assembly → Capital asset registration → Retainer eligibility check.",
    "Source Passport validation is mandatory on Day 1; no AI runs against unsourced data.",
    "Value-ledger discipline: estimated/observed/verified/client_confirmed tiers, evidence required for verified+.",
    "Minimum 1 Capital Asset per engagement (taxonomy: scoring_rule, draft_template, governance_rule, proof_example, sector_insight, productization_signal, qa_rubric, arabic_style_pattern).",
    "Never send external messages.",
]


def delivery_executor(task: Any, route: Route) -> dict[str, Any]:
    return build_envelope(
        task=task,
        route=route,
        role="delivery",
        system_constraints=_DELIVERY_CONSTRAINTS,
        deliverable=(
            "Day-N artefact: which sprint step, the inputs consumed, the output produced, "
            "the ledger entries written, and the next step's prerequisites."
        ),
    )
