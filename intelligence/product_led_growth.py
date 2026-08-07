"""
Product-Led Growth Flow

Self-service entry point for prospects to:
1. Score themselves
2. See recommended package
3. Book diagnostic
4. Get onboarding milestone preview

No external sends; purely consultative and opt-in.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from intelligence.pricing_engine import PricingEngine
from intelligence.saudi_market_intelligence import SaudiCompanyProfile, SaudiMarketIntelligence


@dataclass
class PLGRecommendation:
    company_name: str
    icp_score: float
    fit_summary: str
    recommended_package: str
    recommended_tier: str
    price_sar: float
    roi_estimate_percent: float
    next_steps: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "company_name": self.company_name,
            "icp_score": self.icp_score,
            "fit_summary": self.fit_summary,
            "recommended_package": self.recommended_package,
            "recommended_tier": self.recommended_tier,
            "price_sar": self.price_sar,
            "roi_estimate_percent": self.roi_estimate_percent,
            "next_steps": self.next_steps,
        }


class ProductLedGrowthFlow:
    """Self-service diagnostic and recommendation flow."""

    def __init__(self):
        self.market_intel = SaudiMarketIntelligence()
        self.pricing = PricingEngine()

    def run(
        self,
        company_name: str,
        sector: str,
        city: str,
        employees: int,
        website: str | None = None,
    ) -> PLGRecommendation:
        """Run the self-service flow and return a recommendation."""
        profile = SaudiCompanyProfile(
            company_name=company_name,
            sector=sector,
            city=city,
            employees_estimate=employees,
            website=website,
        )

        icp = self.market_intel.score_icp(profile)
        entry = self.market_intel.recommend_entry(sector, city)
        price = self.pricing.recommend(entry["recommended_package"], sector, employees)

        if icp.score >= 80:
            fit_summary = "Excellent fit for Dealix. We recommend starting with a paid pilot."
        elif icp.score >= 60:
            fit_summary = "Strong fit. A diagnostic or lead sprint will quickly prove value."
        elif icp.score >= 40:
            fit_summary = "Moderate fit. We recommend a low-risk diagnostic first."
        else:
            fit_summary = "Below ideal fit. Book a free consultation to explore fit."

        return PLGRecommendation(
            company_name=company_name,
            icp_score=icp.score,
            fit_summary=fit_summary,
            recommended_package=entry["recommended_package"],
            recommended_tier=price.tier.value,
            price_sar=price.adjusted_price_sar,
            roi_estimate_percent=price.roi_estimate_percent,
            next_steps=[
                "Book a 20-minute diagnostic call",
                "Receive a custom Saudi prospect pack",
                "Review proposal and SOW",
            ],
        )
