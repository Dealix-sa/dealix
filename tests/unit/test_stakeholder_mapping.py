"""Unit tests for api/routers/stakeholder_mapping.py"""
from __future__ import annotations

from api.routers.stakeholder_mapping import (
    _STAKEHOLDER_ARCHETYPES,
    _DECISION_MAKING_PATTERNS,
    _INFLUENCE_MAP_TEMPLATE,
    _VALID_ARCHETYPES,
    StakeholderAssessmentInput,
    _assess_stakeholder_map,
    router,
)


def _make_input(**overrides) -> StakeholderAssessmentInput:
    data = dict(
        prospect_company="Riyadh Investments Ltd.",
        identified_champion=False,
        economic_buyer_engaged=False,
        technical_evaluator_engaged=False,
        blockers_identified=0,
        decision_makers_count=2,
        deal_value_sar=150_000.0,
    )
    data.update(overrides)
    return StakeholderAssessmentInput(**data)


# ---------------------------------------------------------------------------
# Static data: _STAKEHOLDER_ARCHETYPES
# ---------------------------------------------------------------------------


class TestStakeholderArchetypes:
    def test_has_five_keys(self):
        assert len(_STAKEHOLDER_ARCHETYPES) == 5

    def test_contains_economic_buyer(self):
        assert "economic_buyer" in _STAKEHOLDER_ARCHETYPES

    def test_contains_champion(self):
        assert "champion" in _STAKEHOLDER_ARCHETYPES

    def test_contains_technical_evaluator(self):
        assert "technical_evaluator" in _STAKEHOLDER_ARCHETYPES

    def test_contains_end_user(self):
        assert "end_user" in _STAKEHOLDER_ARCHETYPES

    def test_contains_blocker(self):
        assert "blocker" in _STAKEHOLDER_ARCHETYPES

    def test_all_have_archetype_id(self):
        for key, arch in _STAKEHOLDER_ARCHETYPES.items():
            assert arch.get("archetype_id"), f"{key} missing archetype_id"

    def test_all_have_name_en(self):
        for key, arch in _STAKEHOLDER_ARCHETYPES.items():
            assert arch.get("name_en"), f"{key} missing name_en"

    def test_all_have_name_ar(self):
        for key, arch in _STAKEHOLDER_ARCHETYPES.items():
            assert arch.get("name_ar"), f"{key} missing name_ar"

    def test_all_have_motivation_en(self):
        for key, arch in _STAKEHOLDER_ARCHETYPES.items():
            assert arch.get("motivation_en"), f"{key} missing motivation_en"

    def test_all_have_motivation_ar(self):
        for key, arch in _STAKEHOLDER_ARCHETYPES.items():
            assert arch.get("motivation_ar"), f"{key} missing motivation_ar"

    def test_all_have_engagement_strategy_en(self):
        for key, arch in _STAKEHOLDER_ARCHETYPES.items():
            assert arch.get("engagement_strategy_en"), f"{key} missing engagement_strategy_en"

    def test_all_have_engagement_strategy_ar(self):
        for key, arch in _STAKEHOLDER_ARCHETYPES.items():
            assert arch.get("engagement_strategy_ar"), f"{key} missing engagement_strategy_ar"

    def test_archetype_id_matches_key(self):
        for key, arch in _STAKEHOLDER_ARCHETYPES.items():
            assert arch["archetype_id"] == key


# ---------------------------------------------------------------------------
# Static data: _DECISION_MAKING_PATTERNS
# ---------------------------------------------------------------------------


class TestDecisionMakingPatterns:
    def test_has_four_items(self):
        assert len(_DECISION_MAKING_PATTERNS) == 4

    def test_all_have_pattern_en(self):
        for i, p in enumerate(_DECISION_MAKING_PATTERNS):
            assert p.get("pattern_en"), f"pattern {i} missing pattern_en"

    def test_all_have_pattern_ar(self):
        for i, p in enumerate(_DECISION_MAKING_PATTERNS):
            assert p.get("pattern_ar"), f"pattern {i} missing pattern_ar"

    def test_all_have_implication_en(self):
        for i, p in enumerate(_DECISION_MAKING_PATTERNS):
            assert p.get("implication_en"), f"pattern {i} missing implication_en"


# ---------------------------------------------------------------------------
# Static data: _INFLUENCE_MAP_TEMPLATE
# ---------------------------------------------------------------------------


class TestInfluenceMapTemplate:
    def test_has_three_levels(self):
        assert len(_INFLUENCE_MAP_TEMPLATE) == 3

    def test_all_have_level_name_en(self):
        for i, level in enumerate(_INFLUENCE_MAP_TEMPLATE):
            assert level.get("level_name_en"), f"level {i} missing level_name_en"

    def test_all_have_level_name_ar(self):
        for i, level in enumerate(_INFLUENCE_MAP_TEMPLATE):
            assert level.get("level_name_ar"), f"level {i} missing level_name_ar"

    def test_all_have_typical_roles_en_list_of_three(self):
        for i, level in enumerate(_INFLUENCE_MAP_TEMPLATE):
            assert isinstance(level.get("typical_roles_en"), list), f"level {i} missing typical_roles_en"
            assert len(level["typical_roles_en"]) == 3, f"level {i} typical_roles_en length != 3"

    def test_all_have_dealix_value_prop_en(self):
        for i, level in enumerate(_INFLUENCE_MAP_TEMPLATE):
            assert level.get("dealix_value_prop_en"), f"level {i} missing dealix_value_prop_en"

    def test_contains_senior_leadership(self):
        names = [lv["level_name_en"] for lv in _INFLUENCE_MAP_TEMPLATE]
        assert "Senior Leadership" in names

    def test_contains_operational(self):
        names = [lv["level_name_en"] for lv in _INFLUENCE_MAP_TEMPLATE]
        assert "Operational" in names


# ---------------------------------------------------------------------------
# _assess_stakeholder_map
# ---------------------------------------------------------------------------


class TestAssessStakeholderMap:
    def test_returns_dict(self):
        result = _assess_stakeholder_map(_make_input())
        assert isinstance(result, dict)

    def test_has_coverage_score(self):
        result = _assess_stakeholder_map(_make_input())
        assert "coverage_score" in result

    def test_has_coverage_label(self):
        result = _assess_stakeholder_map(_make_input())
        assert "coverage_label" in result

    def test_has_missing_archetypes(self):
        result = _assess_stakeholder_map(_make_input())
        assert "missing_archetypes" in result

    def test_has_deal_risk_level(self):
        result = _assess_stakeholder_map(_make_input())
        assert "deal_risk_level" in result

    def test_has_recommended_next_contacts(self):
        result = _assess_stakeholder_map(_make_input())
        assert "recommended_next_contacts" in result

    def test_all_engaged_no_blockers_score_is_90(self):
        result = _assess_stakeholder_map(_make_input(
            identified_champion=True,
            economic_buyer_engaged=True,
            technical_evaluator_engaged=True,
            blockers_identified=0,
        ))
        assert result["coverage_score"] == 90

    def test_all_engaged_no_blockers_label_is_strong(self):
        result = _assess_stakeholder_map(_make_input(
            identified_champion=True,
            economic_buyer_engaged=True,
            technical_evaluator_engaged=True,
            blockers_identified=0,
        ))
        assert result["coverage_label"] == "strong"

    def test_nothing_engaged_score_is_zero(self):
        result = _assess_stakeholder_map(_make_input())
        assert result["coverage_score"] == 0

    def test_nothing_engaged_label_is_weak(self):
        result = _assess_stakeholder_map(_make_input())
        assert result["coverage_label"] == "weak"

    def test_blockers_reduce_score(self):
        no_blocker = _assess_stakeholder_map(_make_input(
            identified_champion=True, blockers_identified=0
        ))
        with_blocker = _assess_stakeholder_map(_make_input(
            identified_champion=True, blockers_identified=2
        ))
        assert with_blocker["coverage_score"] < no_blocker["coverage_score"]

    def test_coverage_score_never_below_zero(self):
        result = _assess_stakeholder_map(_make_input(blockers_identified=100))
        assert result["coverage_score"] >= 0

    def test_deal_risk_high_when_score_below_40(self):
        result = _assess_stakeholder_map(_make_input())
        assert result["deal_risk_level"] == "high"

    def test_deal_risk_medium_when_score_between_40_and_69(self):
        result = _assess_stakeholder_map(_make_input(
            identified_champion=True,
            economic_buyer_engaged=False,
            technical_evaluator_engaged=False,
            blockers_identified=0,
        ))
        assert result["coverage_score"] == 40
        assert result["deal_risk_level"] == "medium"

    def test_deal_risk_low_when_score_70_or_above(self):
        result = _assess_stakeholder_map(_make_input(
            identified_champion=True,
            economic_buyer_engaged=True,
            technical_evaluator_engaged=False,
            blockers_identified=0,
        ))
        assert result["coverage_score"] == 70
        assert result["deal_risk_level"] == "low"

    def test_missing_archetypes_includes_champion_when_not_identified(self):
        result = _assess_stakeholder_map(_make_input(identified_champion=False))
        assert "champion" in result["missing_archetypes"]

    def test_missing_archetypes_excludes_champion_when_identified(self):
        result = _assess_stakeholder_map(_make_input(identified_champion=True))
        assert "champion" not in result["missing_archetypes"]

    def test_missing_archetypes_includes_economic_buyer_when_not_engaged(self):
        result = _assess_stakeholder_map(_make_input(economic_buyer_engaged=False))
        assert "economic_buyer" in result["missing_archetypes"]

    def test_missing_archetypes_includes_technical_evaluator_when_not_engaged(self):
        result = _assess_stakeholder_map(_make_input(technical_evaluator_engaged=False))
        assert "technical_evaluator" in result["missing_archetypes"]

    def test_governance_decision_is_allow_with_review(self):
        result = _assess_stakeholder_map(_make_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_prospect_company_in_result(self):
        result = _assess_stakeholder_map(_make_input(prospect_company="Jeddah Steel Co."))
        assert result["prospect_company"] == "Jeddah Steel Co."

    def test_coverage_label_adequate_at_40(self):
        result = _assess_stakeholder_map(_make_input(
            identified_champion=True,
            economic_buyer_engaged=False,
            technical_evaluator_engaged=False,
            blockers_identified=0,
        ))
        assert result["coverage_label"] == "adequate"

    def test_recommended_next_contacts_matches_missing_archetypes(self):
        result = _assess_stakeholder_map(_make_input(
            identified_champion=False,
            economic_buyer_engaged=True,
            technical_evaluator_engaged=False,
        ))
        assert set(result["recommended_next_contacts"]) == set(result["missing_archetypes"])


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/stakeholder-mapping"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
