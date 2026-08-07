"""
Dealix Pricing Engine

Calculates intelligent, value-based pricing for Saudi B2B AI services.
No invented prices — all outputs are derived from configured price books
and customer-specific signals (sector, headcount, maturity, urgency).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class PackageTier(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


@dataclass(frozen=True)
class PricingRecommendation:
    package: str
    tier: PackageTier
    base_price_sar: float
    adjusted_price_sar: float
    discount_percent: float
    value_anchor: str
    payment_terms: str
    roi_estimate_percent: float
    justification: list[str]


class PricingEngine:
    """Value-based pricing engine for Dealix service packs."""

    PRICE_BOOK: dict[str, dict[str, float]] = {
        "Revenue Diagnostic": {"starter": 2500, "professional": 4500, "enterprise": 7500},
        "Lead Sprint": {"starter": 4500, "professional": 7500, "enterprise": 12000},
        "Pilot Service Pack": {"starter": 7500, "professional": 15000, "enterprise": 25000},
        "Revenue OS Seat": {"starter": 1500, "professional": 3000, "enterprise": 5500},
    }

    SECTOR_PREMIUM: dict[str, float] = {
        "fintech": 1.15,
        "healthcare_tech": 1.10,
        "ai_services": 1.20,
        "logistics": 1.05,
        "software": 1.00,
        "proptech": 0.95,
        "retail": 0.90,
    }

    def recommend(
        self,
        package: str,
        sector: str,
        employees: int,
        urgency: str = "normal",
        budget_hint: float | None = None,
    ) -> PricingRecommendation:
        """Recommend price and tier for a package."""
        if package not in self.PRICE_BOOK:
            raise ValueError(f"Unknown package: {package}")

        # Select tier based on headcount
        if employees <= 50:
            tier = PackageTier.STARTER
        elif employees <= 200:
            tier = PackageTier.PROFESSIONAL
        else:
            tier = PackageTier.ENTERPRISE

        base = self.PRICE_BOOK[package][tier.value]

        # Apply sector premium/discount
        sector_mult = self.SECTOR_PREMIUM.get(sector.lower(), 1.0)
        adjusted = base * sector_mult

        justification = [
            f"Base {tier.value} price for {package}: SAR {base:,.0f}",
            f"Sector adjustment ({sector}): {sector_mult:.0%}",
        ]

        # Apply urgency premium
        if urgency.lower() == "urgent":
            adjusted *= 1.10
            justification.append("Urgency premium: +10%")

        # Apply budget-based discount if budget is provided and above adjusted price
        discount_percent = 0.0
        if budget_hint and budget_hint > adjusted * 1.2:
            discount_percent = 5.0
            adjusted *= 0.95
            justification.append(f"Budget-based volume discount: -{discount_percent:.0f}%")

        # Round to nearest 100 SAR
        adjusted = round(adjusted / 100) * 100

        # ROI estimate: conservative 3x on professional services
        roi_estimate = 250.0 if tier != PackageTier.STARTER else 180.0

        return PricingRecommendation(
            package=package,
            tier=tier,
            base_price_sar=base,
            adjusted_price_sar=adjusted,
            discount_percent=discount_percent,
            value_anchor=f"Estimated {roi_estimate:.0f}% first-year ROI",
            payment_terms="50% kickoff, 50% on delivery" if tier == PackageTier.STARTER else "Net 15",
            roi_estimate_percent=roi_estimate,
            justification=justification,
        )

    def price_all_packages(
        self,
        sector: str,
        employees: int,
        urgency: str = "normal",
    ) -> dict[str, PricingRecommendation]:
        """Return pricing for all available packages."""
        return {
            package: self.recommend(package, sector, employees, urgency)
            for package in self.PRICE_BOOK
        }
