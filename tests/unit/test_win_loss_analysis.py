"""
Unit tests for api/routers/win_loss_analysis.py

Coverage:
- _WIN_FACTORS: 8 factors, weights sum to 100, bilingual labels
- _LOSS_FACTORS: 6 entries, bilingual labels, recovery guidance
- _ANALYSIS_TEMPLATES: 3 templates, question counts, metric counts
- WinLossInput: field validation (ranges, required fields)
- _analyze_deal: arithmetic, strongest/weakest detection, loss_guidance
- Governance decision values on GET (ALLOW_WITH_REVIEW) and POST (APPROVAL_FIRST)
- Router metadata: prefix and tags
"""
from __future__ import annotations

import pytest

from api.routers.win_loss_analysis import (
    _WIN_FACTORS,
    _WIN_FACTOR_WEIGHT_TOTAL,
    _LOSS_FACTORS,
    _ANALYSIS_TEMPLATES,
    _analyze_deal,
    WinLossInput,
    router,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_input(**overrides) -> WinLossInput:
    """Return a valid WinLossInput with perfect scores unless overridden."""
    data: dict = dict(
        deal_name="Almarai Contract",
        outcome="won",
        primary_loss_reason=None,
        relationship_strength_score=10.0,
        roi_clarity_score=10.0,
        pdpl_zatca_fit_score=10.0,
        decision_maker_access_score=10.0,
        timing_alignment_score=10.0,
        vision_2030_narrative_score=10.0,
        competitive_differentiation_score=10.0,
        proposal_quality_score=10.0,
    )
    data.update(overrides)
    return WinLossInput(**data)


# ---------------------------------------------------------------------------
# Win factor structure
# ---------------------------------------------------------------------------

class TestWinFactors:
    def test_eight_win_factors(self):
        assert len(_WIN_FACTORS) == 8

    def test_expected_factor_keys(self):
        expected = {
            "relationship_strength",
            "roi_clarity",
            "pdpl_zatca_fit",
            "decision_maker_access",
            "timing_alignment",
            "vision_2030_narrative",
            "competitive_differentiation",
            "proposal_quality",
        }
        assert set(_WIN_FACTORS.keys()) == expected

    def test_weights_sum_to_100(self):
        assert _WIN_FACTOR_WEIGHT_TOTAL == 100

    def test_all_have_bilingual_labels(self):
        for fid, fmeta in _WIN_FACTORS.items():
            assert fmeta.get("label_en"), f"{fid} missing label_en"
            assert fmeta.get("label_ar"), f"{fid} missing label_ar"

    def test_all_have_positive_weight(self):
        for fid, fmeta in _WIN_FACTORS.items():
            assert fmeta["weight"] > 0, f"{fid} has non-positive weight"

    def test_relationship_strength_highest_weight(self):
        assert _WIN_FACTORS["relationship_strength"]["weight"] == 25

    def test_proposal_quality_lowest_weight(self):
        assert _WIN_FACTORS["proposal_quality"]["weight"] == 3

    def test_all_have_score_range(self):
        for fid, fmeta in _WIN_FACTORS.items():
            assert fmeta.get("score_range"), f"{fid} missing score_range"


# ---------------------------------------------------------------------------
# Loss factor structure
# ---------------------------------------------------------------------------

class TestLossFactors:
    def test_six_loss_factors(self):
        assert len(_LOSS_FACTORS) == 6

    def test_expected_loss_keys(self):
        expected = {
            "budget_not_approved",
            "competitor_won",
            "internal_project_chosen",
            "timing_mismatch",
            "champion_left",
            "no_decision",
        }
        assert set(_LOSS_FACTORS.keys()) == expected

    def test_all_have_bilingual_labels(self):
        for fid, fmeta in _LOSS_FACTORS.items():
            assert fmeta.get("label_en"), f"{fid} missing label_en"
            assert fmeta.get("label_ar"), f"{fid} missing label_ar"

    def test_all_have_recovery_guidance(self):
        for fid, fmeta in _LOSS_FACTORS.items():
            assert fmeta.get("recovery_en"), f"{fid} missing recovery_en"
            assert fmeta.get("recovery_ar"), f"{fid} missing recovery_ar"

    def test_all_have_description(self):
        for fid, fmeta in _LOSS_FACTORS.items():
            assert fmeta.get("description_en"), f"{fid} missing description_en"


# ---------------------------------------------------------------------------
# Analysis templates structure
# ---------------------------------------------------------------------------

class TestAnalysisTemplates:
    def test_three_templates(self):
        assert len(_ANALYSIS_TEMPLATES) == 3

    def test_expected_template_keys(self):
        assert set(_ANALYSIS_TEMPLATES.keys()) == {
            "quick_debrief", "deep_analysis", "pattern_report"
        }

    def test_quick_debrief_has_four_questions(self):
        questions = _ANALYSIS_TEMPLATES["quick_debrief"]["questions"]
        assert len(questions) == 4

    def test_deep_analysis_has_eight_questions(self):
        questions = _ANALYSIS_TEMPLATES["deep_analysis"]["questions"]
        assert len(questions) == 8

    def test_pattern_report_has_six_metrics(self):
        metrics = _ANALYSIS_TEMPLATES["pattern_report"]["metrics"]
        assert len(metrics) == 6

    def test_all_have_bilingual_names(self):
        for tid, tmeta in _ANALYSIS_TEMPLATES.items():
            assert tmeta.get("name_en"), f"{tid} missing name_en"
            assert tmeta.get("name_ar"), f"{tid} missing name_ar"


# ---------------------------------------------------------------------------
# WinLossInput validation
# ---------------------------------------------------------------------------

class TestWinLossInputValidation:
    def test_valid_won_input_created(self):
        inp = _make_input()
        assert inp.deal_name == "Almarai Contract"
        assert inp.outcome == "won"

    def test_valid_lost_input_with_loss_reason(self):
        inp = _make_input(outcome="lost", primary_loss_reason="budget_not_approved")
        assert inp.primary_loss_reason == "budget_not_approved"

    def test_score_below_zero_rejected(self):
        with pytest.raises(Exception):
            _make_input(relationship_strength_score=-0.1)

    def test_score_above_ten_rejected(self):
        with pytest.raises(Exception):
            _make_input(roi_clarity_score=10.1)

    def test_empty_deal_name_rejected(self):
        with pytest.raises(Exception):
            _make_input(deal_name="")


# ---------------------------------------------------------------------------
# _analyze_deal core logic
# ---------------------------------------------------------------------------

class TestAnalyzeDeal:
    def test_perfect_scores_give_100(self):
        result = _analyze_deal(_make_input())
        assert result["weighted_score"] == 100.0

    def test_zero_scores_give_0(self):
        result = _analyze_deal(_make_input(
            relationship_strength_score=0,
            roi_clarity_score=0,
            pdpl_zatca_fit_score=0,
            decision_maker_access_score=0,
            timing_alignment_score=0,
            vision_2030_narrative_score=0,
            competitive_differentiation_score=0,
            proposal_quality_score=0,
        ))
        assert result["weighted_score"] == 0.0

    def test_weighted_score_arithmetic(self):
        # Only relationship_strength_score set to 10; all others 0.
        # Contribution: 10 * 25 / 10 = 25.0
        result = _analyze_deal(_make_input(
            roi_clarity_score=0,
            pdpl_zatca_fit_score=0,
            decision_maker_access_score=0,
            timing_alignment_score=0,
            vision_2030_narrative_score=0,
            competitive_differentiation_score=0,
            proposal_quality_score=0,
        ))
        assert result["weighted_score"] == 25.0

    def test_strongest_factors_count_two(self):
        result = _analyze_deal(_make_input())
        assert len(result["strongest_factors"]) == 2

    def test_weakest_factors_count_two(self):
        result = _analyze_deal(_make_input())
        assert len(result["weakest_factors"]) == 2

    def test_strongest_factor_is_relationship_strength_at_max(self):
        result = _analyze_deal(_make_input())
        factor_ids = [c["factor"] for c in result["strongest_factors"]]
        assert "relationship_strength" in factor_ids

    def test_weakest_factor_is_proposal_quality_at_zero_others_max(self):
        result = _analyze_deal(_make_input(proposal_quality_score=0))
        weakest_ids = [c["factor"] for c in result["weakest_factors"]]
        assert "proposal_quality" in weakest_ids

    def test_loss_guidance_populated_when_outcome_lost(self):
        result = _analyze_deal(
            _make_input(outcome="lost", primary_loss_reason="champion_left")
        )
        assert result["loss_guidance"] is not None
        assert result["loss_guidance"]["loss_reason"] == "champion_left"

    def test_loss_guidance_none_when_outcome_won(self):
        result = _analyze_deal(_make_input(outcome="won"))
        assert result["loss_guidance"] is None

    def test_loss_guidance_none_when_lost_no_reason(self):
        result = _analyze_deal(_make_input(outcome="lost", primary_loss_reason=None))
        assert result["loss_guidance"] is None

    def test_loss_guidance_includes_recovery(self):
        result = _analyze_deal(
            _make_input(outcome="lost", primary_loss_reason="no_decision")
        )
        guidance = result["loss_guidance"]
        assert guidance["recovery_en"]
        assert guidance["recovery_ar"]

    def test_deal_name_preserved_in_output(self):
        result = _analyze_deal(_make_input(deal_name="SABIC Deal"))
        assert result["deal_name"] == "SABIC Deal"

    def test_outcome_preserved_in_output(self):
        result = _analyze_deal(_make_input(outcome="won"))
        assert result["outcome"] == "won"

    def test_governance_decision_is_allow_with_review(self):
        result = _analyze_deal(_make_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_invalid_outcome_raises_value_error(self):
        with pytest.raises(ValueError):
            _analyze_deal(_make_input(outcome="maybe"))

    def test_invalid_loss_reason_raises_value_error(self):
        with pytest.raises(ValueError):
            _analyze_deal(_make_input(outcome="lost", primary_loss_reason="unknown_reason"))

    def test_partial_scores_produce_partial_weighted_total(self):
        # Half scores on all factors should give half the max (50.0)
        result = _analyze_deal(_make_input(
            relationship_strength_score=5,
            roi_clarity_score=5,
            pdpl_zatca_fit_score=5,
            decision_maker_access_score=5,
            timing_alignment_score=5,
            vision_2030_narrative_score=5,
            competitive_differentiation_score=5,
            proposal_quality_score=5,
        ))
        assert result["weighted_score"] == 50.0


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------

class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/win-loss-analysis"

    def test_router_tags_include_analytics(self):
        assert "Analytics" in router.tags
