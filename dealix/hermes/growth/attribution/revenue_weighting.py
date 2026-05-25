"""Normalize attribution weights to sum to 1.0 (or 0.0 if empty)."""

from __future__ import annotations


def normalize(weights: dict[str, float]) -> dict[str, float]:
    total = sum(weights.values())
    if total <= 0:
        return {k: 0.0 for k in weights}
    return {k: round(v / total, 4) for k, v in weights.items()}
