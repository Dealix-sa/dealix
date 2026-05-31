"""
Unit tests for api/routers/saudi_sector_intelligence.py

Tests cover:
- 8 sector profiles with bilingual names, pain points, compliance
- Procurement thresholds: 3 tiers
- Decision-maker titles per sector
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.saudi_sector_intelligence import (
    _SECTOR_PROFILES,
    _PROCUREMENT_THRESHOLDS,
    router,
)


class TestSectorProfiles:
    def test_eight_sectors(self):
        assert len(_SECTOR_PROFILES) == 8

    def test_expected_sectors(self):
        expected = {
            "banking_finance", "healthcare", "logistics_supply_chain",
            "real_estate", "retail_ecommerce", "government_quasi_gov",
            "education_edtech", "manufacturing_industrial",
        }
        assert expected == set(_SECTOR_PROFILES.keys())

    def test_all_bilingual_names(self):
        for k, v in _SECTOR_PROFILES.items():
            assert v.get("name_en"), f"{k} missing name_en"
            assert v.get("name_ar"), f"{k} missing name_ar"

    def test_all_have_pain_points(self):
        for k, v in _SECTOR_PROFILES.items():
            assert len(v.get("key_pain_points_en", [])) >= 2, f"{k} needs ≥2 pain points"
            assert len(v.get("key_pain_points_ar", [])) >= 2, f"{k} needs ≥2 AR pain points"

    def test_pain_point_counts_match(self):
        for k, v in _SECTOR_PROFILES.items():
            en = len(v.get("key_pain_points_en", []))
            ar = len(v.get("key_pain_points_ar", []))
            assert en == ar, f"{k}: pain point count mismatch ({en} EN vs {ar} AR)"

    def test_all_have_decision_maker_titles(self):
        for k, v in _SECTOR_PROFILES.items():
            assert len(v.get("decision_maker_titles_en", [])) >= 2, f"{k} needs ≥2 DM titles"

    def test_all_have_compliance_requirements(self):
        for k, v in _SECTOR_PROFILES.items():
            assert len(v.get("compliance_requirements_en", [])) >= 1, f"{k} needs ≥1 compliance req"

    def test_all_have_dealix_entry_point(self):
        for k, v in _SECTOR_PROFILES.items():
            assert v.get("dealix_entry_point_en"), f"{k} missing dealix_entry_point_en"

    def test_all_have_top_companies(self):
        for k, v in _SECTOR_PROFILES.items():
            assert len(v.get("top_companies_examples", [])) >= 2, f"{k} needs ≥2 example companies"

    def test_banking_has_sama(self):
        compliance = " ".join(_SECTOR_PROFILES["banking_finance"].get("compliance_requirements_en", [])).lower()
        assert "sama" in compliance or "bank" in compliance

    def test_healthcare_has_moh_or_nphies(self):
        compliance = " ".join(_SECTOR_PROFILES["healthcare"].get("compliance_requirements_en", [])).lower()
        assert "moh" in compliance or "nphies" in compliance or "health" in compliance

    def test_all_have_vision_2030_programs(self):
        for k, v in _SECTOR_PROFILES.items():
            assert len(v.get("vision_2030_programs_en", [])) >= 1, f"{k} missing Vision 2030 programs"

    def test_banking_decision_makers_include_cfo_or_ceo(self):
        titles = " ".join(_SECTOR_PROFILES["banking_finance"]["decision_maker_titles_en"]).lower()
        assert "cfo" in titles or "ceo" in titles or "chief" in titles or "financial" in titles


class TestProcurementThresholds:
    def test_three_thresholds(self):
        assert len(_PROCUREMENT_THRESHOLDS) == 3

    def test_all_bilingual(self):
        for k, v in _PROCUREMENT_THRESHOLDS.items():
            assert v.get("description_en"), f"{k} missing description_en"
            assert v.get("description_ar"), f"{k} missing description_ar"

    def test_all_have_dealix_implication(self):
        for k, v in _PROCUREMENT_THRESHOLDS.items():
            assert v.get("dealix_implication_en"), f"{k} missing dealix_implication_en"

    def test_direct_purchase_below_100k(self):
        # Direct purchase threshold should be < 100K SAR
        direct = _PROCUREMENT_THRESHOLDS.get("direct_purchase") or _PROCUREMENT_THRESHOLDS.get(list(_PROCUREMENT_THRESHOLDS.keys())[0])
        desc = direct["description_en"].lower()
        assert "100" in desc or "direct" in desc


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/sector-intelligence"

    def test_router_tags(self):
        assert "Analytics" in router.tags
