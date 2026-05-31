"""
Unit tests for api/routers/prospect_intelligence.py

Tests cover:
- 3 ICP profiles with bilingual names, trigger events, disqualifiers
- 5 trigger event categories with urgency levels
- _qualify_prospect: scoring, signals, gaps, qualification levels
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.prospect_intelligence import (
    _ICP_PROFILES,
    _TRIGGER_EVENT_CATEGORIES,
    _qualify_prospect,
    ICPQualificationInput,
    router,
)


class TestICPProfiles:
    def test_three_profiles(self):
        assert len(_ICP_PROFILES) == 3

    def test_expected_profiles(self):
        expected = {"saudi_sme_growth", "saudi_enterprise", "sama_regulated_fintech"}
        assert expected == set(_ICP_PROFILES.keys())

    def test_all_bilingual(self):
        for k, v in _ICP_PROFILES.items():
            assert v.get("profile_name_en"), f"{k} missing profile_name_en"
            assert v.get("profile_name_ar"), f"{k} missing profile_name_ar"

    def test_all_have_firmographic_criteria(self):
        for k, v in _ICP_PROFILES.items():
            assert v.get("firmographic_criteria"), f"{k} missing firmographic_criteria"

    def test_all_have_trigger_events(self):
        for k, v in _ICP_PROFILES.items():
            assert len(v.get("trigger_events_en", [])) >= 2, f"{k} needs ≥2 trigger events"

    def test_all_have_disqualifiers(self):
        for k, v in _ICP_PROFILES.items():
            assert len(v.get("disqualifiers_en", [])) >= 1, f"{k} needs ≥1 disqualifier"

    def test_all_have_best_entry_product(self):
        for k, v in _ICP_PROFILES.items():
            assert v.get("best_entry_product"), f"{k} missing best_entry_product"

    def test_all_have_avg_deal_size(self):
        for k, v in _ICP_PROFILES.items():
            assert v["avg_deal_size_sar"] > 0, f"{k} missing avg_deal_size_sar"

    def test_enterprise_higher_deal_size_than_sme(self):
        sme = _ICP_PROFILES["saudi_sme_growth"]["avg_deal_size_sar"]
        enterprise = _ICP_PROFILES["saudi_enterprise"]["avg_deal_size_sar"]
        assert enterprise > sme

    def test_enterprise_longer_sales_cycle(self):
        sme_days = _ICP_PROFILES["saudi_sme_growth"]["sales_cycle_days"]
        enterprise_days = _ICP_PROFILES["saudi_enterprise"]["sales_cycle_days"]
        assert enterprise_days > sme_days

    def test_sme_trigger_events_include_zatca(self):
        triggers = " ".join(_ICP_PROFILES["saudi_sme_growth"]["trigger_events_en"]).lower()
        assert "zatca" in triggers

    def test_fintech_entry_not_sprint(self):
        # FinTechs need more than a sprint — data_pack or higher
        entry = _ICP_PROFILES["sama_regulated_fintech"]["best_entry_product"]
        assert entry in ("data_pack", "managed_ops", "custom_ai")


class TestTriggerEventCategories:
    def test_five_categories(self):
        assert len(_TRIGGER_EVENT_CATEGORIES) == 5

    def test_all_bilingual(self):
        for e in _TRIGGER_EVENT_CATEGORIES:
            assert e.get("name_en"), f"{e['category']} missing name_en"
            assert e.get("name_ar"), f"{e['category']} missing name_ar"

    def test_compliance_is_critical(self):
        compliance = next(e for e in _TRIGGER_EVENT_CATEGORIES if e["category"] == "compliance_deadline")
        assert compliance["urgency"] == "critical"

    def test_leadership_change_is_high(self):
        leadership = next(e for e in _TRIGGER_EVENT_CATEGORIES if e["category"] == "leadership_change")
        assert leadership["urgency"] == "high"

    def test_all_have_examples(self):
        for e in _TRIGGER_EVENT_CATEGORIES:
            assert len(e.get("examples_en", [])) >= 2, f"{e['category']} needs ≥2 examples"

    def test_all_have_sales_implication(self):
        for e in _TRIGGER_EVENT_CATEGORIES:
            assert e.get("sales_implication_en"), f"{e['category']} missing sales_implication_en"

    def test_funding_event_present(self):
        categories = {e["category"] for e in _TRIGGER_EVENT_CATEGORIES}
        assert "funding_event" in categories


class TestQualifyProspect:
    def _strong_input(self, **overrides) -> ICPQualificationInput:
        data = dict(
            company_name="Almarai",
            sector="food_beverage",
            employee_count=200,
            annual_revenue_sar=20_000_000.0,
            has_zatca_phase2=True,
            has_identified_champion=True,
            has_budget_signal=True,
            has_trigger_event=True,
            nitaqat_band="low_green",
            months_since_last_funding=6,
        )
        data.update(overrides)
        return ICPQualificationInput(**data)

    def _weak_input(self, **overrides) -> ICPQualificationInput:
        data = dict(
            company_name="Tiny Co",
            sector="retail",
            employee_count=5,
            annual_revenue_sar=200_000.0,
            has_zatca_phase2=False,
            has_identified_champion=False,
            has_budget_signal=False,
            has_trigger_event=False,
            nitaqat_band="unknown",
            months_since_last_funding=999,
        )
        data.update(overrides)
        return ICPQualificationInput(**data)

    def test_strong_is_strong_icp(self):
        result = _qualify_prospect(self._strong_input())
        assert result["qualification_level_en"] == "Strong ICP"

    def test_weak_is_weak_icp(self):
        result = _qualify_prospect(self._weak_input())
        assert result["qualification_level_en"] == "Weak ICP"

    def test_strong_has_signals(self):
        result = _qualify_prospect(self._strong_input())
        assert len(result["signals"]) > 0

    def test_weak_has_gaps(self):
        result = _qualify_prospect(self._weak_input())
        assert len(result["gaps"]) > 0

    def test_no_champion_gap_mentioned(self):
        result = _qualify_prospect(self._strong_input(has_identified_champion=False))
        gap_text = " ".join(result["gaps"]).lower()
        assert "champion" in gap_text

    def test_no_budget_signal_gap_mentioned(self):
        result = _qualify_prospect(self._strong_input(has_budget_signal=False))
        gap_text = " ".join(result["gaps"]).lower()
        assert "budget" in gap_text

    def test_zatca_trigger_boosts_score(self):
        with_zatca = _qualify_prospect(self._strong_input(has_zatca_phase2=True))
        without_zatca = _qualify_prospect(self._strong_input(has_zatca_phase2=False))
        assert with_zatca["qualification_score"] > without_zatca["qualification_score"]

    def test_score_non_negative(self):
        result = _qualify_prospect(self._weak_input())
        assert result["qualification_score"] >= 0

    def test_governance_allow_with_review(self):
        result = _qualify_prospect(self._strong_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_company_name_in_result(self):
        result = _qualify_prospect(self._strong_input())
        assert result["company_name"] == "Almarai"

    def test_recommended_action_for_strong(self):
        result = _qualify_prospect(self._strong_input())
        assert "discovery" in result["recommended_action_en"].lower() or "book" in result["recommended_action_en"].lower()


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/prospect-intelligence"

    def test_router_tags(self):
        assert "Sales" in router.tags
