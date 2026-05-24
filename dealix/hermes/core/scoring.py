"""Shared scoring helpers used across stages."""

from __future__ import annotations


def clip01(x: float) -> float:
    return max(0.0, min(1.0, x))


def weighted_score(weights: dict[str, float], values: dict[str, float]) -> float:
    """Compute Σ wᵢ vᵢ where weights sum to 1.0 (the caller guarantees it).

    Both arguments are dicts keyed by component name; the result is clipped
    to [0, 1].
    """
    s = 0.0
    for k, w in weights.items():
        s += w * clip01(values.get(k, 0.0))
    return clip01(s)


def revenue_priority(
    *,
    expected_value_sar: float,
    days_to_close: float,
    delivery_capacity: float,
) -> float:
    """Higher = bid now. Big deals far out lose to small deals this week.

    days_to_close ∈ [0, ∞), delivery_capacity ∈ [0, 1].
    """
    if expected_value_sar <= 0 or delivery_capacity <= 0:
        return 0.0
    discount = 1.0 / (1.0 + max(0.0, days_to_close) / 14.0)
    return expected_value_sar * discount * clip01(delivery_capacity)


__all__ = ["clip01", "weighted_score", "revenue_priority"]
