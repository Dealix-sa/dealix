"""ROI Calculator — monetized pain quantification for Saudi B2B prospects.

Deterministic ROI modeling from prospect profile data.
No LLM required — based on Saudi B2B market benchmarks.
Hard rule: all projections labelled as estimates; no guaranteed outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class ServiceTier(StrEnum):
    DIAGNOSTIC = "diagnostic"       # 499 SAR
    SPRINT = "sprint"               # 1,500 SAR
    DATA_PACK = "data_pack"         # 1,500 SAR
    MANAGED_OPS = "managed_ops"     # 2,999-4,999 SAR/month
    CUSTOM_AI = "custom_ai"         # 5,000-25,000 SAR


# Saudi B2B market benchmarks (conservative estimates)
_SAUDI_BENCHMARKS: dict[str, float | int] = {
    "avg_hourly_cost_sar": 75,           # Average Saudi white-collar employee cost/hr
    "avg_lead_value_sar": 2500,          # Average B2B deal in SAR (SMB)
    "typical_follow_up_leak_rate": 0.35, # 35% of leads typically lost without follow-up
    "proof_churn_risk_rate": 0.05,       # 5% monthly churn risk without proof packs
    "weeks_per_month": 4.3,
}

# Recovery rate and time savings per service tier
_SERVICE_MULTIPLIERS: dict[ServiceTier, dict[str, float]] = {
    ServiceTier.DIAGNOSTIC: {
        "leak_recovery_rate": 0.05,
        "time_savings_hrs_monthly": 4.0,
    },
    ServiceTier.SPRINT: {
        "leak_recovery_rate": 0.20,
        "time_savings_hrs_monthly": 12.0,
    },
    ServiceTier.DATA_PACK: {
        "leak_recovery_rate": 0.25,
        "time_savings_hrs_monthly": 15.0,
    },
    ServiceTier.MANAGED_OPS: {
        "leak_recovery_rate": 0.50,
        "time_savings_hrs_monthly": 40.0,
    },
    ServiceTier.CUSTOM_AI: {
        "leak_recovery_rate": 0.70,
        "time_savings_hrs_monthly": 80.0,
    },
}

# Investment cost per tier (midpoint for MANAGED_OPS range)
_SERVICE_COSTS_SAR: dict[ServiceTier, int] = {
    ServiceTier.DIAGNOSTIC: 499,
    ServiceTier.SPRINT: 1500,
    ServiceTier.DATA_PACK: 1500,
    ServiceTier.MANAGED_OPS: 3999,
    ServiceTier.CUSTOM_AI: 15000,
}


@dataclass(frozen=True, slots=True)
class ProspectProfile:
    """Prospect data points for ROI modelling."""

    monthly_leads: int                  # Number of leads per month
    current_close_rate_pct: float       # Current close rate (0-100)
    avg_deal_sar: int                   # Average deal value in SAR
    wasted_follow_up_hrs_weekly: int    # Hours wasted on manual follow-up
    team_size: int                      # Number of people in revenue team
    monthly_revenue_sar: int            # Current monthly revenue


@dataclass(frozen=True, slots=True)
class PainMonetization:
    """Quantified pain in SAR terms (estimates only)."""

    monthly_lead_leak_sar: int          # Revenue estimate lost from leads falling through
    monthly_time_waste_sar: int         # Cost estimate of manual follow-up hours
    monthly_proof_gap_cost_sar: int     # Churn risk cost without proof
    total_monthly_pain_sar: int
    annual_pain_sar: int


@dataclass(frozen=True, slots=True)
class ROIProjection:
    """ROI projection for a service tier (estimates only)."""

    service_tier: str
    investment_sar: int
    monthly_recovered_sar: int
    annual_recovered_sar: int
    roi_multiple: float
    payback_weeks: int
    efficiency_gain_hrs_monthly: int
    close_rate_improvement_pct: float
    narrative_ar: str
    narrative_en: str


def monetize_pain(profile: ProspectProfile) -> PainMonetization:
    """Quantify prospect pain in SAR terms using Saudi B2B benchmarks.

    Uses benchmarks where prospect data is incomplete.
    All values are estimates, not guaranteed outcomes.
    """
    benchmarks = _SAUDI_BENCHMARKS
    leak_rate = float(benchmarks["typical_follow_up_leak_rate"])
    avg_deal = profile.avg_deal_sar or int(benchmarks["avg_lead_value_sar"])

    monthly_lead_leak = int(profile.monthly_leads * leak_rate * avg_deal)

    hourly = int(benchmarks["avg_hourly_cost_sar"])
    weeks_per_month = float(benchmarks["weeks_per_month"])
    monthly_time_waste = int(profile.wasted_follow_up_hrs_weekly * weeks_per_month * hourly)

    churn_risk = float(benchmarks["proof_churn_risk_rate"])
    monthly_proof_gap = int(profile.monthly_revenue_sar * churn_risk)

    total = monthly_lead_leak + monthly_time_waste + monthly_proof_gap

    return PainMonetization(
        monthly_lead_leak_sar=monthly_lead_leak,
        monthly_time_waste_sar=monthly_time_waste,
        monthly_proof_gap_cost_sar=monthly_proof_gap,
        total_monthly_pain_sar=total,
        annual_pain_sar=total * 12,
    )


def calculate_roi(
    profile: ProspectProfile,
    tier: ServiceTier = ServiceTier.SPRINT,
) -> ROIProjection:
    """Calculate ROI projection for a service tier.

    All projections are estimates based on Saudi B2B benchmarks.
    """
    pain = monetize_pain(profile)
    multipliers = _SERVICE_MULTIPLIERS[tier]
    cost = _SERVICE_COSTS_SAR[tier]

    recovery_rate = multipliers["leak_recovery_rate"]
    monthly_recovered = int(pain.total_monthly_pain_sar * recovery_rate)
    annual_recovered = monthly_recovered * 12

    roi_multiple = round(annual_recovered / max(cost, 1), 1)

    weeks_per_month = float(_SAUDI_BENCHMARKS["weeks_per_month"])
    if monthly_recovered > 0:
        payback_weeks = max(1, int((cost / monthly_recovered) * weeks_per_month))
    else:
        payback_weeks = 52

    time_savings = int(multipliers["time_savings_hrs_monthly"])
    close_rate_improvement = round(min(20.0, recovery_rate * 30), 1)

    narrative_ar = (
        f"استثمار {cost:,} ر.س يُتيح تعافياً تقديرياً بـ {monthly_recovered:,} ر.س شهرياً "
        f"(عائد تقديري {roi_multiple}x خلال السنة الأولى، فترة استرداد {payback_weeks} أسبوع)."
    )
    narrative_en = (
        f"Investment of SAR {cost:,} enables estimated recovery of SAR {monthly_recovered:,}/month "
        f"(estimated {roi_multiple}x return in year one, {payback_weeks}-week payback)."
    )

    return ROIProjection(
        service_tier=tier.value,
        investment_sar=cost,
        monthly_recovered_sar=monthly_recovered,
        annual_recovered_sar=annual_recovered,
        roi_multiple=roi_multiple,
        payback_weeks=payback_weeks,
        efficiency_gain_hrs_monthly=time_savings,
        close_rate_improvement_pct=close_rate_improvement,
        narrative_ar=narrative_ar,
        narrative_en=narrative_en,
    )


def recommend_tier(profile: ProspectProfile) -> ServiceTier:
    """Recommend the appropriate service tier based on prospect profile."""
    if profile.monthly_revenue_sar >= 200_000 or profile.team_size >= 20:
        return ServiceTier.MANAGED_OPS
    if profile.monthly_revenue_sar >= 50_000 or profile.team_size >= 5:
        return ServiceTier.SPRINT
    return ServiceTier.DIAGNOSTIC


def build_roi_summary(profile: ProspectProfile) -> dict[str, Any]:
    """Build a full ROI summary across all tiers for a prospect."""
    pain = monetize_pain(profile)
    recommended = recommend_tier(profile)

    tiers: dict[str, Any] = {}
    for tier in ServiceTier:
        proj = calculate_roi(profile, tier)
        tiers[tier.value] = {
            "investment_sar": proj.investment_sar,
            "monthly_recovered_sar": proj.monthly_recovered_sar,
            "roi_multiple": proj.roi_multiple,
            "payback_weeks": proj.payback_weeks,
            "narrative_ar": proj.narrative_ar,
            "narrative_en": proj.narrative_en,
        }

    return {
        "pain_monetization": {
            "monthly_lead_leak_sar": pain.monthly_lead_leak_sar,
            "monthly_time_waste_sar": pain.monthly_time_waste_sar,
            "monthly_proof_gap_cost_sar": pain.monthly_proof_gap_cost_sar,
            "total_monthly_pain_sar": pain.total_monthly_pain_sar,
            "annual_pain_sar": pain.annual_pain_sar,
        },
        "recommended_tier": recommended.value,
        "tiers": tiers,
    }


__all__ = [
    "PainMonetization",
    "ProspectProfile",
    "ROIProjection",
    "ServiceTier",
    "build_roi_summary",
    "calculate_roi",
    "monetize_pain",
    "recommend_tier",
]
