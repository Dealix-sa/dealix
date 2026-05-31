"""Per-campaign revenue quality scoring."""

from __future__ import annotations


def score_campaign_quality(
    *,
    revenue_sar: float,
    cost_sar: float,
    retainer_potential: float,
    moat_score: float,
) -> float:
    if cost_sar <= 0:
        return 0.0
    margin_ratio = max(0.0, (revenue_sar - cost_sar) / max(revenue_sar, 1.0))
    score = (
        0.4 * margin_ratio
        + 0.3 * min(max(retainer_potential, 0.0), 1.0)
        + 0.3 * min(max(moat_score, 0.0), 1.0)
    )
    return round(score, 4)
