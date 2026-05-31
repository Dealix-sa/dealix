"""
Unit tests for api/routers/competitive_positioning.py

Tests cover:
- 5 competitor categories with bilingual names, win conditions
- 4 battle cards
- PositioningBriefRequest validation
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.competitive_positioning import (
    _COMPETITOR_CATEGORIES,
    _BATTLE_CARDS,
    PositioningBriefRequest,
    router,
)


class TestCompetitorCategories:
    def test_five_categories(self):
        assert len(_COMPETITOR_CATEGORIES) == 5

    def test_expected_category_keys(self):
        expected = {"generic_crm", "big_4_consulting", "local_it_integrators", "in_house_team", "do_nothing"}
        assert expected == set(_COMPETITOR_CATEGORIES.keys())

    def test_all_bilingual_names(self):
        for k, v in _COMPETITOR_CATEGORIES.items():
            assert v.get("name_en"), f"{k} missing name_en"
            assert v.get("name_ar"), f"{k} missing name_ar"

    def test_all_have_dealix_advantage(self):
        for k, v in _COMPETITOR_CATEGORIES.items():
            assert v.get("dealix_advantage_en"), f"{k} missing dealix_advantage_en"
            assert v.get("dealix_advantage_ar"), f"{k} missing dealix_advantage_ar"

    def test_all_have_win_conditions(self):
        for k, v in _COMPETITOR_CATEGORIES.items():
            assert len(v.get("win_conditions", [])) >= 2, f"{k} needs ≥2 win conditions"

    def test_generic_crm_mentions_arabic_or_saudi(self):
        adv = _COMPETITOR_CATEGORIES["generic_crm"]["dealix_advantage_en"].lower()
        assert "arabic" in adv or "saudi" in adv or "zatca" in adv

    def test_do_nothing_mentions_cost_of_inaction(self):
        adv = _COMPETITOR_CATEGORIES["do_nothing"]["dealix_advantage_en"].lower()
        assert "cost" in adv or "inaction" in adv or "month" in adv or "miss" in adv

    def test_big_4_advantage_mentions_speed(self):
        adv = _COMPETITOR_CATEGORIES["big_4_consulting"]["dealix_advantage_en"].lower()
        assert "day" in adv or "week" in adv or "7" in adv or "speed" in adv or "sprint" in adv

    def test_all_have_objection_response(self):
        for k, v in _COMPETITOR_CATEGORIES.items():
            assert v.get("objection_response_en"), f"{k} missing objection_response_en"


class TestBattleCards:
    def test_four_battle_cards(self):
        assert len(_BATTLE_CARDS) == 4

    def test_all_bilingual(self):
        for card in _BATTLE_CARDS:
            assert card.get("scenario") or card.get("scenario_en"), f"Missing scenario: {card}"
            assert card.get("dealix_response_en"), "Missing dealix_response_en"

    def test_salesforce_card_present(self):
        texts = [str(c).lower() for c in _BATTLE_CARDS]
        assert any("salesforce" in t or "crm" in t for t in texts)

    def test_budget_card_present(self):
        texts = [str(c).lower() for c in _BATTLE_CARDS]
        assert any("budget" in t or "499" in t or "sprint" in t for t in texts)

    def test_all_have_trap_to_avoid(self):
        for card in _BATTLE_CARDS:
            assert card.get("trap_to_avoid_en"), "Missing trap_to_avoid_en"


class TestPositioningBriefRequest:
    def test_valid_request_created(self):
        req = PositioningBriefRequest(
            competitor_category="generic_crm",
            client_name="Almarai",
            client_pain_points=["Manual reporting"],
            deal_size_sar=15000.0,
        )
        assert req.client_name == "Almarai"

    def test_missing_client_name_rejected(self):
        with pytest.raises(Exception):
            PositioningBriefRequest(
                competitor_category="generic_crm",
                client_pain_points=["pain"],
                deal_size_sar=5000.0,
            )


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/competitive-positioning"

    def test_router_tags(self):
        assert "Sales" in router.tags
