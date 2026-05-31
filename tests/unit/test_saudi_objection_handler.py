"""
Unit tests for api/routers/saudi_objection_handler.py

Tests cover:
- Objection database: structure, categories, bilingual fields
- Key objections present: price, timing, authority, trust, technical
- Category grouping correct
- Known objection IDs findable
- Red flags present on relevant objections
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.saudi_objection_handler import (
    _OBJECTIONS,
    _OBJECTIONS_BY_ID,
    _OBJECTIONS_BY_CATEGORY,
    _CATEGORIES,
    router,
)


class TestObjectionData:
    def test_at_least_seven_objections(self):
        assert len(_OBJECTIONS) >= 7

    def test_five_categories_covered(self):
        assert "price" in _CATEGORIES
        assert "timing" in _CATEGORIES
        assert "authority" in _CATEGORIES
        assert "trust" in _CATEGORIES
        assert "technical" in _CATEGORIES

    def test_all_have_bilingual_objections(self):
        for obj in _OBJECTIONS:
            assert obj.get("objection_en"), f"{obj['id']} missing objection_en"
            assert obj.get("objection_ar"), f"{obj['id']} missing objection_ar"

    def test_all_have_recommended_responses(self):
        for obj in _OBJECTIONS:
            assert obj.get("recommended_response_en"), f"{obj['id']} missing response_en"
            assert obj.get("recommended_response_ar"), f"{obj['id']} missing response_ar"

    def test_all_have_saudi_context(self):
        for obj in _OBJECTIONS:
            assert obj.get("saudi_context_en"), f"{obj['id']} missing saudi_context_en"

    def test_all_have_follow_up_action(self):
        for obj in _OBJECTIONS:
            assert obj.get("follow_up_action"), f"{obj['id']} missing follow_up_action"

    def test_all_have_category(self):
        valid_cats = {"price", "timing", "authority", "trust", "technical"}
        for obj in _OBJECTIONS:
            assert obj.get("category") in valid_cats, f"{obj['id']} invalid category"

    def test_all_have_frequency(self):
        valid_freqs = {"very_high", "high", "medium", "low", "seasonal"}
        for obj in _OBJECTIONS:
            assert obj.get("frequency") in valid_freqs, f"{obj['id']} invalid frequency"


class TestKnownObjections:
    def test_price_too_expensive_present(self):
        assert "price_too_expensive" in _OBJECTIONS_BY_ID

    def test_timing_ramadan_present(self):
        assert "timing_busy_ramadan" in _OBJECTIONS_BY_ID

    def test_authority_not_decision_maker_present(self):
        assert "authority_not_decision_maker" in _OBJECTIONS_BY_ID

    def test_trust_new_vendor_present(self):
        assert "trust_new_vendor" in _OBJECTIONS_BY_ID

    def test_tech_data_security_present(self):
        assert "tech_data_security" in _OBJECTIONS_BY_ID

    def test_price_too_expensive_mentions_roi(self):
        obj = _OBJECTIONS_BY_ID["price_too_expensive"]
        response = obj["recommended_response_en"].lower()
        assert "roi" in response or "payback" in response or "pay back" in response

    def test_ramadan_objection_seasonal_frequency(self):
        obj = _OBJECTIONS_BY_ID["timing_busy_ramadan"]
        assert obj["frequency"] == "seasonal"

    def test_ramadan_response_does_not_push_decision(self):
        obj = _OBJECTIONS_BY_ID["timing_busy_ramadan"]
        # Should not use pressure tactics in Ramadan
        response = obj["recommended_response_en"].lower()
        assert "limited time" not in response
        assert "urgent" not in response

    def test_trust_response_mentions_poc(self):
        obj = _OBJECTIONS_BY_ID["trust_new_vendor"]
        response = obj["recommended_response_en"].lower()
        assert "pilot" in response or "poc" in response or "sprint" in response

    def test_data_security_mentions_pdpl(self):
        obj = _OBJECTIONS_BY_ID["tech_data_security"]
        context = obj["saudi_context_en"].lower()
        assert "pdpl" in context

    def test_authority_mentions_multi_threading(self):
        obj = _OBJECTIONS_BY_ID["authority_not_decision_maker"]
        assert obj["response_strategy"] == "multi_threading"


class TestCategoryGrouping:
    def test_price_category_has_multiple_objections(self):
        assert len(_OBJECTIONS_BY_CATEGORY.get("price", [])) >= 2

    def test_timing_category_includes_ramadan(self):
        timing_ids = [o["id"] for o in _OBJECTIONS_BY_CATEGORY.get("timing", [])]
        assert "timing_busy_ramadan" in timing_ids

    def test_all_objections_in_some_category(self):
        all_in_categories = sum(len(v) for v in _OBJECTIONS_BY_CATEGORY.values())
        assert all_in_categories == len(_OBJECTIONS)


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/objection-handler"

    def test_router_tags(self):
        assert "Sales" in router.tags
