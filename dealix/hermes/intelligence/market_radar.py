"""Market Radar — every market signal must yield a campaign, report, offer, risk, lead list, or partner target."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.hermes.core.schemas import Signal


@dataclass
class MarketSignalOutput:
    source: str
    sector: str
    signal: str
    opportunity: str
    recommended_offer: str
    target_segments: list[str] = field(default_factory=list)
    confidence: float = 0.5
    produces: list[str] = field(default_factory=list)


class MarketRadar:
    def process(
        self,
        signal: Signal,
        *,
        sector: str,
        opportunity: str,
        recommended_offer: str,
        target_segments: list[str],
    ) -> MarketSignalOutput:
        produces: list[str] = []
        if "campaign" in opportunity.lower():
            produces.append("campaign")
        if "report" in opportunity.lower() or sector:
            produces.append("report")
        if recommended_offer:
            produces.append("offer")
        if target_segments:
            produces.append("lead_list")
        if not produces:
            produces = ["risk_warning"]
        return MarketSignalOutput(
            source=signal.source,
            sector=sector,
            signal=signal.title,
            opportunity=opportunity,
            recommended_offer=recommended_offer,
            target_segments=target_segments,
            confidence=signal.confidence,
            produces=produces,
        )
