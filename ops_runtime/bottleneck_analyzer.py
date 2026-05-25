from __future__ import annotations

"""Identify the funnel stage with the worst conversion."""

from typing import Any

# Conversion is measured as next_stage_count / current_stage_count for the
# adjacent stage in this ordered list. Stages absent from the data are skipped.
_STAGE_ORDER: tuple[str, ...] = (
    "lead",
    "contacted",
    "qualified",
    "proposal",
    "negotiation",
    "closed_won",
)


def find_bottleneck(metrics: dict[str, Any]) -> dict[str, Any]:
    """Return {stage, conversion_rate, recommendation}.

    When data is too thin to compute, returns a stage of "" with a
    recommendation to collect more pipeline rows first.
    """
    by_stage = (metrics.get("pipeline", {}) or {}).get("by_stage", {}) or {}
    if not by_stage:
        return {
            "stage": "",
            "conversion_rate": 0.0,
            "recommendation": "Add leads to pipeline_tracker.csv to compute funnel.",
        }

    worst_stage = ""
    worst_rate = 1.0
    for i in range(len(_STAGE_ORDER) - 1):
        cur = _STAGE_ORDER[i]
        nxt = _STAGE_ORDER[i + 1]
        cur_count = by_stage.get(cur, 0)
        nxt_count = by_stage.get(nxt, 0)
        if cur_count <= 0:
            continue
        rate = nxt_count / cur_count
        if rate < worst_rate:
            worst_rate = rate
            worst_stage = cur

    if not worst_stage:
        return {
            "stage": "",
            "conversion_rate": 0.0,
            "recommendation": "Not enough adjacent-stage data to identify bottleneck.",
        }

    return {
        "stage": worst_stage,
        "conversion_rate": round(worst_rate, 3),
        "recommendation": (
            f"Focus this week on moving leads from '{worst_stage}' to the next stage."
        ),
    }
