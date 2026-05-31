"""Territory intelligence benchmarks and plan builder for Dealix Saudi B2B.

All data is static; no LLM or external API calls are made.
All generated plans carry a mandatory governance decision and must be
reviewed before acting on them.

Prefix: /api/v1/territory-intelligence
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/territory-intelligence",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: Saudi regions
# ---------------------------------------------------------------------------

_SAUDI_REGIONS: list[dict[str, Any]] = [
    {
        "region_id": "riyadh",
        "region_name_en": "Riyadh",
        "region_name_ar": "الرياض",
        "key_cities_en": ["Riyadh", "Diriyah", "Al Kharj"],
        "key_sectors_en": ["technology", "banking_finance", "government_services"],
        "gdp_contribution_pct": 45.0,
        "vision_2030_priority": True,
        "b2b_density": "high",
    },
    {
        "region_id": "western",
        "region_name_en": "Western Province (Jeddah)",
        "region_name_ar": "المنطقة الغربية (جدة)",
        "key_cities_en": ["Jeddah", "Yanbu"],
        "key_sectors_en": ["retail_ecommerce", "logistics", "food_beverage"],
        "gdp_contribution_pct": 25.0,
        "vision_2030_priority": True,
        "b2b_density": "high",
    },
    {
        "region_id": "eastern",
        "region_name_en": "Eastern Province",
        "region_name_ar": "المنطقة الشرقية",
        "key_cities_en": ["Dammam", "Al Khobar", "Dhahran"],
        "key_sectors_en": ["banking_finance", "logistics", "technology"],
        "gdp_contribution_pct": 20.0,
        "vision_2030_priority": True,
        "b2b_density": "medium",
    },
    {
        "region_id": "makkah_madinah",
        "region_name_en": "Makkah and Madinah",
        "region_name_ar": "مكة المكرمة والمدينة المنورة",
        "key_cities_en": ["Makkah", "Madinah", "Taif"],
        "key_sectors_en": ["healthcare", "retail_ecommerce", "food_beverage"],
        "gdp_contribution_pct": 7.0,
        "vision_2030_priority": True,
        "b2b_density": "medium",
    },
    {
        "region_id": "northern_southern",
        "region_name_en": "Northern and Southern Regions",
        "region_name_ar": "المناطق الشمالية والجنوبية",
        "key_cities_en": ["Tabuk", "Abha"],
        "key_sectors_en": ["logistics", "food_beverage", "retail_ecommerce"],
        "gdp_contribution_pct": 3.0,
        "vision_2030_priority": False,
        "b2b_density": "low",
    },
]

_VALID_REGIONS: set[str] = {r["region_id"] for r in _SAUDI_REGIONS}

# ---------------------------------------------------------------------------
# Static data: sector penetration
# ---------------------------------------------------------------------------

_SECTOR_PENETRATION_DATA: dict[str, dict[str, Any]] = {
    "retail_ecommerce": {
        "sector_name_en": "Retail and E-commerce",
        "sector_name_ar": "التجزئة والتجارة الإلكترونية",
        "estimated_tam_sar": 8_500_000_000,
        "current_penetration_pct": 3.2,
        "growth_rate_pct": 18.5,
        "priority": "tier_1",
    },
    "banking_finance": {
        "sector_name_en": "Banking and Finance",
        "sector_name_ar": "البنوك والتمويل",
        "estimated_tam_sar": 12_000_000_000,
        "current_penetration_pct": 2.1,
        "growth_rate_pct": 14.0,
        "priority": "tier_1",
    },
    "food_beverage": {
        "sector_name_en": "Food and Beverage",
        "sector_name_ar": "الأغذية والمشروبات",
        "estimated_tam_sar": 5_200_000_000,
        "current_penetration_pct": 4.5,
        "growth_rate_pct": 12.0,
        "priority": "tier_2",
    },
    "healthcare": {
        "sector_name_en": "Healthcare",
        "sector_name_ar": "الرعاية الصحية",
        "estimated_tam_sar": 7_300_000_000,
        "current_penetration_pct": 1.8,
        "growth_rate_pct": 16.5,
        "priority": "tier_1",
    },
    "logistics": {
        "sector_name_en": "Logistics",
        "sector_name_ar": "اللوجستيات",
        "estimated_tam_sar": 4_100_000_000,
        "current_penetration_pct": 5.0,
        "growth_rate_pct": 10.5,
        "priority": "tier_2",
    },
    "technology": {
        "sector_name_en": "Technology",
        "sector_name_ar": "التقنية",
        "estimated_tam_sar": 9_800_000_000,
        "current_penetration_pct": 6.7,
        "growth_rate_pct": 22.0,
        "priority": "tier_3",
    },
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class TerritoryPlanInput(BaseModel):
    region: str
    target_sector: str
    current_customers_in_region: int = Field(..., ge=0)
    target_new_logos_per_quarter: int = Field(..., ge=1)
    sales_headcount: int = Field(default=1, ge=1)


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _build_territory_plan(inp: TerritoryPlanInput) -> dict[str, Any]:
    """Compute a territory plan for a given Saudi region and sector.

    Returns a structured dict with pipeline targets, quota per rep,
    region metadata, and governance decision.
    """
    if inp.region not in _VALID_REGIONS:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid region '{inp.region}'. "
                f"Must be one of: {sorted(_VALID_REGIONS)}"
            ),
        )

    region_data = next(r for r in _SAUDI_REGIONS if r["region_id"] == inp.region)
    sector_data = _SECTOR_PENETRATION_DATA.get(inp.target_sector)

    pipeline_target_sar = inp.target_new_logos_per_quarter * 5000 * 3
    accounts_to_work = inp.target_new_logos_per_quarter * 5
    quota_per_rep_sar = pipeline_target_sar / inp.sales_headcount

    return {
        "region_name_en": region_data["region_name_en"],
        "region_name_ar": region_data["region_name_ar"],
        "vision_2030_priority": region_data["vision_2030_priority"],
        "pipeline_target_sar": pipeline_target_sar,
        "accounts_to_work": accounts_to_work,
        "quota_per_rep_sar": quota_per_rep_sar,
        "sector_tam_sar": sector_data["estimated_tam_sar"] if sector_data else None,
        "governance_decision": _GOV_APPROVAL,
        "disclaimer_en": (
            "All figures are estimates based on static benchmarks. "
            "Validate against live pipeline data before committing resources."
        ),
        "disclaimer_ar": (
            "جميع الأرقام تقديرية مبنية على معايير ثابتة. "
            "يُرجى التحقق من بيانات خط الأنابيب الحية قبل تخصيص الموارد."
        ),
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/regions", summary="All 5 Saudi regions with bilingual metadata")
def get_regions() -> dict[str, Any]:
    """Return all Saudi regions with bilingual names, key cities, and B2B density."""
    return {
        "regions": _SAUDI_REGIONS,
        "total_regions": len(_SAUDI_REGIONS),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/sector-penetration", summary="All 6 sector penetration profiles")
def get_sector_penetration() -> dict[str, Any]:
    """Return all sector penetration data with TAM, growth rates, and priority tiers."""
    return {
        "sectors": _SECTOR_PENETRATION_DATA,
        "total_sectors": len(_SECTOR_PENETRATION_DATA),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/build-plan", summary="Build a territory plan for a given region and sector")
def build_territory_plan(body: TerritoryPlanInput) -> dict[str, Any]:
    """Accept territory parameters and return a structured plan with pipeline targets.

    Governance decision: APPROVAL_FIRST.
    """
    return _build_territory_plan(body)
