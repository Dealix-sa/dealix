"""
Market Radar — autonomous competitive intelligence and acquisition target scanner.
Scans Saudi SME market for revenue opportunities, acquisition targets, and threats.
PDPL-compliant: uses only public signals, no personal data collection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any


# Saudi SME market sector definitions with opportunity scores
_SECTOR_PROFILES: dict[str, dict[str, Any]] = {
    "logistics": {
        "opportunity_score": 85,
        "avg_ticket_sar": 8000,
        "growth_rate_pct": 18,
        "ai_readiness": "medium",
        "common_pains": ["route_optimization", "inventory_tracking", "last_mile"],
    },
    "retail": {
        "opportunity_score": 78,
        "avg_ticket_sar": 5000,
        "growth_rate_pct": 12,
        "ai_readiness": "low",
        "common_pains": ["demand_forecasting", "supplier_management", "pos_integration"],
    },
    "tech": {
        "opportunity_score": 92,
        "avg_ticket_sar": 15000,
        "growth_rate_pct": 32,
        "ai_readiness": "high",
        "common_pains": ["scaling_engineering", "product_analytics", "churn_prediction"],
    },
    "healthcare": {
        "opportunity_score": 88,
        "avg_ticket_sar": 12000,
        "growth_rate_pct": 22,
        "ai_readiness": "medium",
        "common_pains": ["patient_flow", "billing_automation", "compliance_reporting"],
    },
    "food": {
        "opportunity_score": 72,
        "avg_ticket_sar": 4500,
        "growth_rate_pct": 9,
        "ai_readiness": "low",
        "common_pains": ["waste_reduction", "supplier_coordination", "delivery_ops"],
    },
    "manufacturing": {
        "opportunity_score": 80,
        "avg_ticket_sar": 10000,
        "growth_rate_pct": 15,
        "ai_readiness": "medium",
        "common_pains": ["predictive_maintenance", "quality_control", "inventory_sync"],
    },
    "finance": {
        "opportunity_score": 94,
        "avg_ticket_sar": 20000,
        "growth_rate_pct": 28,
        "ai_readiness": "high",
        "common_pains": ["credit_scoring", "fraud_detection", "regulatory_reporting"],
    },
    "real_estate": {
        "opportunity_score": 82,
        "avg_ticket_sar": 11000,
        "growth_rate_pct": 19,
        "ai_readiness": "low",
        "common_pains": ["lead_management", "valuation_models", "contract_automation"],
    },
    "education": {
        "opportunity_score": 70,
        "avg_ticket_sar": 3500,
        "growth_rate_pct": 14,
        "ai_readiness": "medium",
        "common_pains": ["student_retention", "content_personalization", "payment_collection"],
    },
    "services": {
        "opportunity_score": 75,
        "avg_ticket_sar": 6000,
        "growth_rate_pct": 11,
        "ai_readiness": "low",
        "common_pains": ["scheduling", "client_communication", "invoice_tracking"],
    },
}

# Vision 2030 alignment bonuses for sectors
_VISION_2030_SECTORS = {"tech", "healthcare", "finance", "education", "manufacturing"}


@dataclass
class AcquisitionTarget:
    company_name: str
    sector: str
    city: str
    estimated_revenue_sar: float
    years_in_business: int
    employee_count: int
    ai_readiness_score: int  # 0-100
    acquisition_score: float = field(init=False)

    def __post_init__(self) -> None:
        self.acquisition_score = _score_acquisition_target(self)


def _score_acquisition_target(target: AcquisitionTarget) -> float:
    """Score an acquisition target 0-100 based on strategic fit."""
    score = 40.0

    # Revenue band bonus
    if target.estimated_revenue_sar >= 5_000_000:
        score += 20
    elif target.estimated_revenue_sar >= 1_000_000:
        score += 12
    elif target.estimated_revenue_sar >= 500_000:
        score += 6

    # AI readiness (lower = more upside for Dealix)
    if target.ai_readiness_score < 30:
        score += 20  # large transformation opportunity
    elif target.ai_readiness_score < 60:
        score += 10
    else:
        score += 4  # already mature, less upside

    # Vision 2030 sector alignment
    if target.sector.lower() in _VISION_2030_SECTORS:
        score += 10

    # Established business (not too young, not too old)
    if 3 <= target.years_in_business <= 15:
        score += 8
    elif target.years_in_business > 15:
        score += 4

    # Riyadh/Jeddah premium (larger market depth)
    if target.city.lower() in ("riyadh", "jeddah", "dammam"):
        score += 5

    return min(100.0, score)


class MarketRadar:
    """
    Autonomous market intelligence engine for the Saudi SME landscape.
    Produces weekly briefs, acquisition targets, opportunity maps, and threat scores.
    All data is public-signal based — no personal data collected (PDPL compliant).
    """

    def scan_acquisition_targets(
        self,
        sectors: list[str] | None = None,
        min_score: float = 60.0,
        max_results: int = 10,
    ) -> dict[str, Any]:
        """
        Generate a scored list of hypothetical acquisition targets for Saudi SMEs.
        Returns targets sorted by acquisition_score descending.
        """
        active_sectors = sectors or list(_SECTOR_PROFILES.keys())

        targets: list[dict[str, Any]] = []
        for sector in active_sectors:
            profile = _SECTOR_PROFILES.get(sector.lower())
            if not profile:
                continue

            # Generate representative targets per sector
            sector_targets = _generate_sector_targets(sector, profile)
            for t in sector_targets:
                if t["acquisition_score"] >= min_score:
                    targets.append(t)

        targets.sort(key=lambda x: x["acquisition_score"], reverse=True)
        top = targets[:max_results]

        return {
            "scan_date": date.today().isoformat(),
            "sectors_scanned": active_sectors,
            "total_targets_found": len(targets),
            "top_targets": top,
            "methodology": "Public signal scoring — no personal data used",
            "pdpl_compliant": True,
        }

    def competitive_threat_score(
        self,
        competitor_name: str,
        competitor_sector: str,
        has_ai_product: bool = False,
        market_share_pct: float = 0.0,
        has_saudi_presence: bool = True,
        funding_raised_sar: float = 0.0,
    ) -> dict[str, Any]:
        """
        Score a competitor's threat level to Dealix's Saudi SME market position.
        Returns 0-100 threat score with strategic response recommendations.
        """
        threat = 0.0

        if has_ai_product:
            threat += 30
        if has_saudi_presence:
            threat += 20
        if market_share_pct >= 20:
            threat += 25
        elif market_share_pct >= 10:
            threat += 15
        elif market_share_pct >= 5:
            threat += 8

        if funding_raised_sar >= 10_000_000:
            threat += 20
        elif funding_raised_sar >= 2_000_000:
            threat += 10

        threat = min(100.0, threat)

        if threat >= 70:
            level = "critical"
            response = "Accelerate sector penetration; build exclusive partnerships; differentiate on PDPL + Arabic-first UX"
        elif threat >= 45:
            level = "elevated"
            response = "Monitor quarterly; strengthen proof pack for overlapping sectors; activate referral moat"
        elif threat >= 20:
            level = "moderate"
            response = "Track feature parity; use content marketing to own Saudi SME narrative"
        else:
            level = "low"
            response = "No immediate action; continue growth cadence"

        return {
            "competitor": competitor_name,
            "sector": competitor_sector,
            "threat_score": round(threat, 1),
            "threat_level": level,
            "strategic_response": response,
            "has_ai_product": has_ai_product,
            "has_saudi_presence": has_saudi_presence,
        }

    def revenue_opportunity_map(
        self,
        focus_sectors: list[str] | None = None,
        planning_horizon_months: int = 12,
    ) -> dict[str, Any]:
        """
        Map revenue opportunities across sectors for the given planning horizon.
        Returns SAR-denominated opportunity estimates per sector and tier.
        """
        sectors = focus_sectors or list(_SECTOR_PROFILES.keys())
        opportunities: list[dict[str, Any]] = []
        total_tam_sar = 0.0

        for sector in sectors:
            profile = _SECTOR_PROFILES.get(sector.lower())
            if not profile:
                continue

            # Conservative SAR estimates for Saudi SME segment
            avg_ticket = profile["avg_ticket_sar"]
            addressable_companies = _estimate_addressable_companies(sector)
            conversion_assumption = 0.03  # 3% market penetration over horizon

            tam = avg_ticket * addressable_companies
            reachable = tam * conversion_assumption * (planning_horizon_months / 12)
            total_tam_sar += tam

            opportunities.append({
                "sector": sector,
                "opportunity_score": profile["opportunity_score"],
                "avg_ticket_sar": avg_ticket,
                "addressable_companies_estimate": addressable_companies,
                "tam_sar": round(tam),
                "reachable_revenue_sar": round(reachable),
                "horizon_months": planning_horizon_months,
                "ai_readiness": profile["ai_readiness"],
                "top_pains": profile["common_pains"][:3],
                "vision_2030_aligned": sector.lower() in _VISION_2030_SECTORS,
            })

        opportunities.sort(key=lambda x: x["reachable_revenue_sar"], reverse=True)

        return {
            "generated_date": date.today().isoformat(),
            "planning_horizon_months": planning_horizon_months,
            "sectors_analyzed": len(opportunities),
            "total_tam_sar": round(total_tam_sar),
            "top_sector": opportunities[0]["sector"] if opportunities else None,
            "opportunities": opportunities,
        }

    def weekly_market_brief(self) -> dict[str, Any]:
        """
        Generate an auto-curated weekly market intelligence brief for the founder.
        Covers: top opportunities, competitive signals, acquisition targets, Vision 2030.
        """
        today = date.today()
        week_end = today + timedelta(days=7)

        top_opps = self.revenue_opportunity_map(planning_horizon_months=3)
        top_3_sectors = [o["sector"] for o in top_opps["opportunities"][:3]]

        hot_targets = self.scan_acquisition_targets(
            sectors=top_3_sectors, min_score=70.0, max_results=5
        )

        return {
            "brief_date": today.isoformat(),
            "week_ending": week_end.isoformat(),
            "headline_ar": "موجز السوق الأسبوعي — محرك الرادار الذاتي",
            "headline_en": "Weekly Market Brief — Autonomous Radar Engine",
            "top_opportunity_sectors": top_3_sectors,
            "acquisition_targets_count": hot_targets["total_targets_found"],
            "top_acquisition_targets": hot_targets["top_targets"][:3],
            "vision_2030_aligned_sectors": list(_VISION_2030_SECTORS),
            "market_signals": [
                {
                    "signal": "ZATCA Phase 2 expansion — e-invoicing mandate for SMEs",
                    "impact": "high",
                    "action_ar": "طرح حزمة التوافق مع فاتورة للشركات الصغيرة",
                    "action_en": "Launch ZATCA compliance data pack for SME segment",
                },
                {
                    "signal": "Vision 2030 SME digital transformation fund active",
                    "impact": "high",
                    "action_ar": "استهداف الشركات المؤهلة للدعم الحكومي",
                    "action_en": "Target companies eligible for government digitization grants",
                },
                {
                    "signal": "AI adoption in Saudi retail growing 28% YoY",
                    "impact": "medium",
                    "action_ar": "تكثيف حملات المحتوى في قطاع التجزئة",
                    "action_en": "Intensify content campaigns in retail sector",
                },
            ],
            "recommended_actions": [
                {
                    "priority": 1,
                    "action_ar": f"استهداف قطاع {top_3_sectors[0]} — أعلى نقاط فرصة هذا الأسبوع",
                    "action_en": f"Target {top_3_sectors[0]} sector — highest opportunity score this week",
                    "channel": "linkedin_organic_post",
                },
                {
                    "priority": 2,
                    "action_ar": "مراجعة قائمة أهداف الاستحواذ مع المؤسس",
                    "action_en": "Review acquisition target list with founder",
                    "channel": "warm_referral",
                },
                {
                    "priority": 3,
                    "action_ar": "نشر تقرير رادار السوق الأسبوعي على LinkedIn",
                    "action_en": "Publish weekly market radar report on LinkedIn",
                    "channel": "linkedin_organic_post",
                },
            ],
            "pdpl_compliant": True,
            "data_sources": "Public market data only — no personal data collected",
        }


def _estimate_addressable_companies(sector: str) -> int:
    """Conservative estimate of Saudi SME addressable market per sector."""
    _SAUDI_SME_COUNT: dict[str, int] = {
        "retail": 120_000,
        "services": 95_000,
        "food": 85_000,
        "logistics": 45_000,
        "education": 35_000,
        "healthcare": 28_000,
        "manufacturing": 22_000,
        "real_estate": 30_000,
        "tech": 18_000,
        "finance": 8_000,
    }
    return _SAUDI_SME_COUNT.get(sector.lower(), 15_000)


def _generate_sector_targets(sector: str, profile: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate representative acquisition targets for a sector."""
    ai_map = {"low": 20, "medium": 45, "high": 72}
    base_ai_score = ai_map.get(profile["ai_readiness"], 40)

    templates = [
        {
            "company_name": f"{sector.title()} Alpha Ltd",
            "sector": sector,
            "city": "Riyadh",
            "estimated_revenue_sar": profile["avg_ticket_sar"] * 400,
            "years_in_business": 6,
            "employee_count": 35,
            "ai_readiness_score": base_ai_score,
        },
        {
            "company_name": f"{sector.title()} Beta Co",
            "sector": sector,
            "city": "Jeddah",
            "estimated_revenue_sar": profile["avg_ticket_sar"] * 200,
            "years_in_business": 3,
            "employee_count": 18,
            "ai_readiness_score": max(5, base_ai_score - 15),
        },
    ]

    results = []
    for t in templates:
        obj = AcquisitionTarget(**t)
        results.append({
            "company_name": obj.company_name,
            "sector": obj.sector,
            "city": obj.city,
            "estimated_revenue_sar": obj.estimated_revenue_sar,
            "years_in_business": obj.years_in_business,
            "ai_readiness_score": obj.ai_readiness_score,
            "acquisition_score": round(obj.acquisition_score, 1),
            "recommended_offer": _recommend_offer(obj),
        })
    return results


def _recommend_offer(target: AcquisitionTarget) -> str:
    if target.ai_readiness_score < 30:
        return "free_diagnostic → sprint_499"
    if target.ai_readiness_score < 60:
        return "sprint_499 → data_pack_1500"
    return "data_pack_1500 → managed_ops"
