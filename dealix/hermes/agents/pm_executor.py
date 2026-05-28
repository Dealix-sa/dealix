"""dealix-pm executor — produces a status + next-actions envelope."""

from __future__ import annotations

from typing import Any

from ..router import Route
from ._envelope import build_envelope


_PM_CONSTRAINTS: list[str] = [
    "Honor all 11 non-negotiables (no scraping, cold WhatsApp, LinkedIn automation, fake claims, PII in logs, source-less answers, unapproved external action, untracked agents).",
    "Read the 90-day plan at /root/.claude/plans/wiggly-cooking-sketch.md before deciding next actions.",
    "Never invent revenue or customer outcomes.",
    "Surface high-severity friction events as escalations, never silently dismiss.",
    "Delegate parallelizable work to engineer/content/sales/delivery sub-agents.",
]


def pm_executor(task: Any, route: Route) -> dict[str, Any]:
    return build_envelope(
        task=task,
        route=route,
        role="pm",
        system_constraints=_PM_CONSTRAINTS,
        deliverable=(
            "5-line status: phase + commit delta + top-3 friction + next 1-3 actions + blockers. "
            "Then a TodoWrite-style action list for parallelizable work."
        ),
    )
