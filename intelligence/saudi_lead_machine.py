"""
Saudi Lead Machine v2

Enriches raw company signals into scored, actionable Saudi B2B leads.
Combines public data patterns, sector intelligence, and ICP scoring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from intelligence.saudi_market_intelligence import SaudiCompanyProfile, SaudiMarketIntelligence


@dataclass
class EnrichedLead:
    company_name: str
    sector: str
    city: str
    employees_estimate: int | None
    website: str | None
    icp_score: float
    momentum: str
    recommended_package: str
    enrichment_signals: dict[str, Any] = field(default_factory=dict)
    data_quality: str = "medium"  # low | medium | high


class SaudiLeadMachine:
    """Enrichment and scoring engine for Saudi B2B leads."""

    def __init__(self):
        self.market_intel = SaudiMarketIntelligence()

    def enrich(
        self,
        company_name: str,
        sector: str,
        city: str,
        employees_estimate: int | None = None,
        website: str | None = None,
        signals: dict[str, Any] | None = None,
    ) -> EnrichedLead:
        """Enrich a raw lead with intelligence signals."""
        signals = signals or {}
        profile = SaudiCompanyProfile(
            company_name=company_name,
            sector=sector,
            city=city,
            employees_estimate=employees_estimate,
            website=website,
        )

        icp = self.market_intel.score_icp(profile)
        entry = self.market_intel.recommend_entry(sector, city)

        # Data quality scoring
        quality_score = 0
        if employees_estimate:
            quality_score += 1
        if website:
            quality_score += 1
        if signals:
            quality_score += 1
        data_quality = ["low", "medium", "high"][min(quality_score, 2)]

        enrichment_signals = {
            "has_website": bool(website),
            "has_headcount": bool(employees_estimate),
            "has_external_signals": bool(signals),
            "sector_momentum": entry["momentum"],
            "city_tier": entry["city_tier"],
        }
        enrichment_signals.update(signals)

        return EnrichedLead(
            company_name=company_name,
            sector=sector,
            city=city,
            employees_estimate=employees_estimate,
            website=website,
            icp_score=icp.score,
            momentum=entry["momentum"],
            recommended_package=entry["recommended_package"],
            enrichment_signals=enrichment_signals,
            data_quality=data_quality,
        )

    def enrich_batch(self, raw_leads: list[dict[str, Any]]) -> list[EnrichedLead]:
        """Enrich a batch of raw leads."""
        return [
            self.enrich(
                company_name=lead["company_name"],
                sector=lead["sector"],
                city=lead["city"],
                employees_estimate=lead.get("employees_estimate"),
                website=lead.get("website"),
                signals=lead.get("signals"),
            )
            for lead in raw_leads
        ]

    def export_priority_list(self, enriched: list[EnrichedLead], top_n: int = 20) -> list[dict[str, Any]]:
        """Return top-N priority leads ready for sales action."""
        sorted_leads = sorted(enriched, key=lambda x: x.icp_score, reverse=True)
        return [
            {
                "company_name": lead.company_name,
                "icp_score": lead.icp_score,
                "recommended_package": lead.recommended_package,
                "data_quality": lead.data_quality,
                "city": lead.city,
                "sector": lead.sector,
            }
            for lead in sorted_leads[:top_n]
        ]
