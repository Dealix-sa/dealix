"""Tender Radar — converts public tenders into structured opportunities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TenderOpportunity:
    title: str
    buyer: str
    estimated_value_sar: float
    deadline: str
    fit_score: int
    next_action: str


class TenderRadar:
    def score(
        self,
        *,
        title: str,
        buyer: str,
        estimated_value_sar: float,
        deadline: str,
        sector_fit: int,
        capability_fit: int,
        risk: int,
    ) -> TenderOpportunity:
        fit = max(1, min(sector_fit + capability_fit - risk, 5))
        action = "Prepare bid summary for Sami approval" if fit >= 3 else "Skip"
        return TenderOpportunity(title, buyer, estimated_value_sar, deadline, fit, action)
