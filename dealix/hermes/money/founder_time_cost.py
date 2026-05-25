"""
Founder time cost — make founder hours a first-class line item.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FounderTimeCost:
    score: float            # 0 (no founder time) → 100 (entirely founder-bound)
    band: str               # "low" | "medium" | "high" | "blocker"
    expand_recommendation: bool
    notes: list[str]


def score_founder_time_cost(
    *,
    founder_hours_required: float,
    decision_complexity: float,        # 0-1
    relationship_sensitivity: float,   # 0-1
    delegation_possible: float,        # 0-1, higher is better
    strategic_value: float,            # 0-1, higher is better
    builds_asset_or_retainer: bool,
) -> FounderTimeCost:
    if founder_hours_required < 0:
        raise ValueError("founder_hours_required must be >= 0")
    for name, value in [
        ("decision_complexity", decision_complexity),
        ("relationship_sensitivity", relationship_sensitivity),
        ("delegation_possible", delegation_possible),
        ("strategic_value", strategic_value),
    ]:
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be in [0,1], got {value}")

    raw = (
        min(founder_hours_required, 40) * 2
        + decision_complexity * 20
        + relationship_sensitivity * 15
        - delegation_possible * 25
        - strategic_value * 15
    )
    score = max(0.0, min(100.0, round(raw + 30, 2)))
    if score >= 80:
        band = "blocker"
    elif score >= 60:
        band = "high"
    elif score >= 35:
        band = "medium"
    else:
        band = "low"

    expand = band in ("low", "medium") and (
        builds_asset_or_retainer or strategic_value >= 0.7
    )
    notes: list[str] = []
    if not builds_asset_or_retainer and band in ("high", "blocker"):
        notes.append(
            "high founder time without producing an asset or retainer — reposition or kill"
        )
    if delegation_possible < 0.3 and band != "low":
        notes.append("low delegation_possible — invest in playbook + delivery automation")
    return FounderTimeCost(
        score=score,
        band=band,
        expand_recommendation=expand,
        notes=notes,
    )
