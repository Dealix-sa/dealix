"""Unit tests for api/routers/territory_intelligence.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.territory_intelligence import (
    _SAUDI_REGIONS,
    _SECTOR_PENETRATION_DATA,
    _VALID_REGIONS,
    TerritoryPlanInput,
    _build_territory_plan,
    router,
)


def _make_input(**overrides) -> TerritoryPlanInput:
    data = dict(
        region="riyadh",
        target_sector="technology",
        current_customers_in_region=5,
        target_new_logos_per_quarter=4,
        sales_headcount=2,
    )
    data.update(overrides)
    return TerritoryPlanInput(**data)


# ---------------------------------------------------------------------------
# Static data: Saudi regions
# ---------------------------------------------------------------------------


class TestSaudiRegions:
    def test_has_five_regions(self):
        assert len(_SAUDI_REGIONS) == 5

    def test_all_have_region_id(self):
        for r in _SAUDI_REGIONS:
            assert r.get("region_id"), f"Region missing region_id: {r}"

    def test_all_have_region_name_en(self):
        for r in _SAUDI_REGIONS:
            assert r.get("region_name_en"), f"Region {r.get('region_id')} missing region_name_en"

    def test_all_have_region_name_ar(self):
        for r in _SAUDI_REGIONS:
            assert r.get("region_name_ar"), f"Region {r.get('region_id')} missing region_name_ar"

    def test_all_have_key_cities_en(self):
        for r in _SAUDI_REGIONS:
            assert isinstance(r.get("key_cities_en"), list)
            assert len(r["key_cities_en"]) >= 2, f"Region {r.get('region_id')} needs at least 2 cities"

    def test_all_have_key_sectors_en(self):
        for r in _SAUDI_REGIONS:
            assert isinstance(r.get("key_sectors_en"), list)
            assert len(r["key_sectors_en"]) == 3, f"Region {r.get('region_id')} must have 3 sectors"

    def test_all_have_gdp_contribution_pct(self):
        for r in _SAUDI_REGIONS:
            assert "gdp_contribution_pct" in r
            assert isinstance(r["gdp_contribution_pct"], float)

    def test_all_have_vision_2030_priority(self):
        for r in _SAUDI_REGIONS:
            assert "vision_2030_priority" in r
            assert isinstance(r["vision_2030_priority"], bool)

    def test_all_have_b2b_density(self):
        for r in _SAUDI_REGIONS:
            assert r.get("b2b_density") in {"high", "medium", "low"}, (
                f"Region {r.get('region_id')} has invalid b2b_density"
            )

    def test_riyadh_gdp_45(self):
        riyadh = next(r for r in _SAUDI_REGIONS if r["region_id"] == "riyadh")
        assert riyadh["gdp_contribution_pct"] == 45.0

    def test_riyadh_density_high(self):
        riyadh = next(r for r in _SAUDI_REGIONS if r["region_id"] == "riyadh")
        assert riyadh["b2b_density"] == "high"

    def test_riyadh_vision_true(self):
        riyadh = next(r for r in _SAUDI_REGIONS if r["region_id"] == "riyadh")
        assert riyadh["vision_2030_priority"] is True

    def test_western_gdp_25(self):
        western = next(r for r in _SAUDI_REGIONS if r["region_id"] == "western")
        assert western["gdp_contribution_pct"] == 25.0

    def test_western_density_high(self):
        western = next(r for r in _SAUDI_REGIONS if r["region_id"] == "western")
        assert western["b2b_density"] == "high"

    def test_eastern_gdp_20(self):
        eastern = next(r for r in _SAUDI_REGIONS if r["region_id"] == "eastern")
        assert eastern["gdp_contribution_pct"] == 20.0

    def test_northern_southern_vision_false(self):
        ns = next(r for r in _SAUDI_REGIONS if r["region_id"] == "northern_southern")
        assert ns["vision_2030_priority"] is False

    def test_northern_southern_density_low(self):
        ns = next(r for r in _SAUDI_REGIONS if r["region_id"] == "northern_southern")
        assert ns["b2b_density"] == "low"


# ---------------------------------------------------------------------------
# Static data: valid regions set
# ---------------------------------------------------------------------------


class TestValidRegions:
    def test_has_five_items(self):
        assert len(_VALID_REGIONS) == 5

    def test_contains_riyadh(self):
        assert "riyadh" in _VALID_REGIONS

    def test_contains_western(self):
        assert "western" in _VALID_REGIONS

    def test_contains_eastern(self):
        assert "eastern" in _VALID_REGIONS

    def test_contains_makkah_madinah(self):
        assert "makkah_madinah" in _VALID_REGIONS

    def test_contains_northern_southern(self):
        assert "northern_southern" in _VALID_REGIONS

    def test_matches_region_ids(self):
        region_ids = {r["region_id"] for r in _SAUDI_REGIONS}
        assert region_ids == _VALID_REGIONS


# ---------------------------------------------------------------------------
# Static data: sector penetration
# ---------------------------------------------------------------------------


class TestSectorPenetrationData:
    def test_has_six_sectors(self):
        assert len(_SECTOR_PENETRATION_DATA) == 6

    def test_contains_retail_ecommerce(self):
        assert "retail_ecommerce" in _SECTOR_PENETRATION_DATA

    def test_contains_banking_finance(self):
        assert "banking_finance" in _SECTOR_PENETRATION_DATA

    def test_contains_technology(self):
        assert "technology" in _SECTOR_PENETRATION_DATA

    def test_all_have_sector_name_en(self):
        for sid, data in _SECTOR_PENETRATION_DATA.items():
            assert data.get("sector_name_en"), f"Sector {sid} missing sector_name_en"

    def test_all_have_sector_name_ar(self):
        for sid, data in _SECTOR_PENETRATION_DATA.items():
            assert data.get("sector_name_ar"), f"Sector {sid} missing sector_name_ar"

    def test_all_have_estimated_tam_sar(self):
        for sid, data in _SECTOR_PENETRATION_DATA.items():
            assert "estimated_tam_sar" in data
            assert isinstance(data["estimated_tam_sar"], int)

    def test_all_have_priority(self):
        for sid, data in _SECTOR_PENETRATION_DATA.items():
            assert data.get("priority") in {"tier_1", "tier_2", "tier_3"}, (
                f"Sector {sid} has invalid priority"
            )


# ---------------------------------------------------------------------------
# _build_territory_plan
# ---------------------------------------------------------------------------


class TestBuildTerritoryPlan:
    def test_returns_dict(self):
        result = _build_territory_plan(_make_input())
        assert isinstance(result, dict)

    def test_has_pipeline_target_sar(self):
        result = _build_territory_plan(_make_input())
        assert "pipeline_target_sar" in result

    def test_has_accounts_to_work(self):
        result = _build_territory_plan(_make_input())
        assert "accounts_to_work" in result

    def test_has_quota_per_rep_sar(self):
        result = _build_territory_plan(_make_input())
        assert "quota_per_rep_sar" in result

    def test_pipeline_target_formula(self):
        inp = _make_input(target_new_logos_per_quarter=4, sales_headcount=1)
        result = _build_territory_plan(inp)
        assert result["pipeline_target_sar"] == 4 * 5000 * 3

    def test_pipeline_target_formula_varied(self):
        inp = _make_input(target_new_logos_per_quarter=10, sales_headcount=1)
        result = _build_territory_plan(inp)
        assert result["pipeline_target_sar"] == 10 * 5000 * 3

    def test_accounts_to_work_formula(self):
        inp = _make_input(target_new_logos_per_quarter=4)
        result = _build_territory_plan(inp)
        assert result["accounts_to_work"] == 4 * 5

    def test_quota_per_rep_formula(self):
        inp = _make_input(target_new_logos_per_quarter=4, sales_headcount=2)
        result = _build_territory_plan(inp)
        pipeline = 4 * 5000 * 3
        assert result["quota_per_rep_sar"] == pipeline / 2

    def test_quota_per_rep_single_rep(self):
        inp = _make_input(target_new_logos_per_quarter=4, sales_headcount=1)
        result = _build_territory_plan(inp)
        pipeline = result["pipeline_target_sar"]
        assert result["quota_per_rep_sar"] == pipeline

    def test_has_region_name_en(self):
        result = _build_territory_plan(_make_input(region="riyadh"))
        assert result.get("region_name_en")

    def test_has_region_name_ar(self):
        result = _build_territory_plan(_make_input(region="riyadh"))
        assert result.get("region_name_ar")

    def test_has_vision_2030_priority(self):
        result = _build_territory_plan(_make_input(region="riyadh"))
        assert result["vision_2030_priority"] is True

    def test_sector_tam_populated_for_known_sector(self):
        result = _build_territory_plan(_make_input(target_sector="technology"))
        assert result["sector_tam_sar"] is not None

    def test_sector_tam_none_for_unknown_sector(self):
        result = _build_territory_plan(_make_input(target_sector="unknown_sector"))
        assert result["sector_tam_sar"] is None

    def test_governance_decision_approval_first(self):
        result = _build_territory_plan(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_has_disclaimer_en(self):
        result = _build_territory_plan(_make_input())
        assert result.get("disclaimer_en")

    def test_has_disclaimer_ar(self):
        result = _build_territory_plan(_make_input())
        assert result.get("disclaimer_ar")

    def test_invalid_region_raises_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _build_territory_plan(_make_input(region="invalid_region"))
        assert exc_info.value.status_code == 422

    @pytest.mark.parametrize(
        "region",
        ["riyadh", "western", "eastern", "makkah_madinah", "northern_southern"],
    )
    def test_all_valid_regions_work(self, region):
        result = _build_territory_plan(_make_input(region=region))
        assert result["governance_decision"] == "APPROVAL_FIRST"


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/territory-intelligence"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
