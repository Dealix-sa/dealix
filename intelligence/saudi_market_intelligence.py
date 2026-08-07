"""
Saudi Market Intelligence Engine

Analyzes Saudi B2B companies and market signals to produce:
- ICP fit scoring
- Sector momentum
- Competitor presence
- Entry recommendations

All analysis is based on public/synthetic data and PDPL-aware.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SectorSignal(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    UNKNOWN = "unknown"


@dataclass
class SaudiCompanyProfile:
    company_name: str
    sector: str
    city: str
    employees_estimate: int | None = None
    website: str | None = None
    signals: dict[str, Any] = field(default_factory=dict)


@dataclass
class ICPScore:
    company_name: str
    score: float  # 0.0 - 100.0
    reasons: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)


class SaudiMarketIntelligence:
    """Intelligence engine for Saudi B2B market analysis."""

    HIGH_GROWTH_SECTORS: set[str] = {
        "software", "fintech", "logistics", "healthcare_tech",
        "ecommerce_b2b", "renewable_energy", "construction_tech",
        "hr_tech", "proptech", "edtech", "ai_services",
    }

    TARGET_CITIES: set[str] = {
        "riyadh", "jeddah", "dammam", "khobar", "makkah", "madinah",
    }

    def __init__(self):
        self._profiles: list[SaudiCompanyProfile] = []
        self._analyses: list[dict[str, Any]] = []

    def add_profile(self, profile: SaudiCompanyProfile) -> None:
        self._profiles.append(profile)

    def score_icp(self, profile: SaudiCompanyProfile) -> ICPScore:
        """Score a company against the ideal Dealix customer profile."""
        score = 0.0
        reasons: list[str] = []
        risk_flags: list[str] = []

        sector = profile.sector.lower()
        if sector in self.HIGH_GROWTH_SECTORS:
            score += 35
            reasons.append(f"{profile.sector} is a high-growth Saudi B2B sector")
        else:
            risk_flags.append(f"{profile.sector} not in top target sectors")

        city = profile.city.lower()
        if city in self.TARGET_CITIES:
            score += 20
            reasons.append(f"Based in {profile.city}, a key commercial hub")
        else:
            risk_flags.append("Location outside primary target cities")

        employees = profile.employees_estimate
        if employees is not None:
            if 20 <= employees <= 200:
                score += 30
                reasons.append(f"Headcount {employees} fits sweet spot")
            elif employees < 20:
                score += 15
                risk_flags.append("Smaller team may have limited budget")
            else:
                score += 10
                risk_flags.append("Large enterprise; longer sales cycle")

        if profile.website:
            score += 10
            reasons.append("Has public web presence")
        else:
            risk_flags.append("No website detected")

        # Cap at 100
        score = min(score, 100.0)

        return ICPScore(
            company_name=profile.company_name,
            score=round(score, 1),
            reasons=reasons,
            risk_flags=risk_flags,
        )

    def sector_momentum(self, sector: str) -> SectorSignal:
        """Return a simple momentum signal for a sector."""
        sector = sector.lower()
        if sector in {"ai_services", "fintech", "construction_tech", "logistics"}:
            return SectorSignal.STRONG
        if sector in {"software", "healthcare_tech", "proptech", "hr_tech"}:
            return SectorSignal.MODERATE
        if sector in {"retail", "food_beverage", "traditional_services"}:
            return SectorSignal.WEAK
        return SectorSignal.UNKNOWN

    def recommend_entry(
        self,
        sector: str,
        city: str,
        budget_sar: float | None = None,
    ) -> dict[str, Any]:
        """Recommend a market-entry package for a sector/city."""
        momentum = self.sector_momentum(sector)
        city_tier = "tier_1" if city.lower() in self.TARGET_CITIES else "tier_2"

        package = "Revenue Diagnostic"
        if momentum == SectorSignal.STRONG and city_tier == "tier_1":
            package = "Pilot Service Pack"
        elif momentum == SectorSignal.MODERATE:
            package = "Lead Sprint"

        budget_note = None
        if budget_sar is not None and budget_sar < 3000:
            budget_note = "Consider starting with Revenue Diagnostic to prove value"

        recommendation = {
            "sector": sector,
            "city": city,
            "momentum": momentum.value,
            "city_tier": city_tier,
            "recommended_package": package,
            "budget_note": budget_note,
            "next_action": f"Build a sector-specific prospect pack for {sector} in {city}",
        }
        self._analyses.append(recommendation)
        return recommendation

    def batch_score(self) -> list[ICPScore]:
        """Score all loaded profiles."""
        return [self.score_icp(p) for p in self._profiles]
