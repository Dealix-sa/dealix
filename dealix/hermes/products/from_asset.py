"""
Productization candidate detection.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AssetCandidate:
    asset_id: str
    is_candidate: bool
    rationale: list[str]


def is_productization_candidate(
    *,
    asset_id: str,
    times_used: int,
    influenced_revenue_sar: float,
    reusable: bool,
    low_risk: bool,
) -> AssetCandidate:
    rationale: list[str] = []
    if times_used < 3:
        rationale.append(f"only used {times_used} times (need >=3)")
    if influenced_revenue_sar <= 0:
        rationale.append("no influenced revenue")
    if not reusable:
        rationale.append("not flagged reusable")
    if not low_risk:
        rationale.append("not low risk")
    return AssetCandidate(
        asset_id=asset_id, is_candidate=not rationale, rationale=rationale
    )
