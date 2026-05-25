from __future__ import annotations

"""Score current metrics against weekly target KPIs."""

from typing import Any

_DEFAULT_TARGETS: dict[str, float] = {
    "dms_sent": 25,
    "samples_sent": 3,
    "proposals_sent": 1,
    "payments_pursued": 1,
    "total_leads": 25,
    "cash_collected_sar": 5000,
}


def _as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def score_against_targets(
    metrics: dict[str, Any], targets: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Return {kpi: {actual, target, percent}} plus an overall percent."""
    targets = targets or _DEFAULT_TARGETS
    pipeline = metrics.get("pipeline", {})
    revenue = metrics.get("revenue", {})

    flat = {
        "dms_sent": revenue.get("dms_sent", 0),
        "samples_sent": revenue.get("samples_sent", 0),
        "proposals_sent": revenue.get("proposals_sent", 0),
        "payments_pursued": revenue.get("payments_pursued", 0),
        "total_leads": pipeline.get("total_leads", 0),
        "cash_collected_sar": revenue.get("cash_collected_sar", 0.0),
    }

    scores: dict[str, Any] = {}
    percents: list[float] = []
    for kpi, target in targets.items():
        target_f = _as_float(target)
        actual = _as_float(flat.get(kpi, 0))
        if target_f <= 0:
            pct = 100.0 if actual > 0 else 0.0
        else:
            pct = round(min(actual / target_f, 1.0) * 100, 1)
        scores[kpi] = {"actual": actual, "target": target_f, "percent": pct}
        percents.append(pct)

    overall = round(sum(percents) / len(percents), 1) if percents else 0.0
    scores["_overall_percent"] = overall
    return scores
