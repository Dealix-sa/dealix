"""
Unit tests for api/routers/lead_scoring.py

Tests cover:
- 8 scoring criteria with weights summing to 100
- 5 grade bands (A+, A, B, C, D) with SLA hours
- _score_lead: total score, grade, strengths, gaps, next steps
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.lead_scoring import (
    _SCORING_CRITERIA,
    _GRADE_BANDS,
    _score_lead,
    LeadScoringInput,
    router,
)


class TestScoringCriteria:
    def test_eight_criteria(self):
        assert len(_SCORING_CRITERIA) == 8

    def test_weights_sum_to_100(self):
        total = sum(v["weight"] for v in _SCORING_CRITERIA.values())
        assert total == 100

    def test_all_bilingual(self):
        for k, v in _SCORING_CRITERIA.items():
            assert v.get("description_en"), f"{k} missing description_en"
            assert v.get("description_ar"), f"{k} missing description_ar"

    def test_sector_fit_weight_20(self):
        assert _SCORING_CRITERIA["sector_fit"]["weight"] == 20

    def test_company_size_fit_weight_15(self):
        assert _SCORING_CRITERIA["company_size_fit"]["weight"] == 15

    def test_vision_2030_weight_7(self):
        assert _SCORING_CRITERIA["vision_2030_alignment"]["weight"] == 7

    def test_all_have_positive_weights(self):
        for k, v in _SCORING_CRITERIA.items():
            assert v["weight"] > 0, f"{k} has zero or negative weight"


class TestGradeBands:
    def test_five_bands(self):
        assert len(_GRADE_BANDS) == 5

    def test_grades_present(self):
        grades = {b["grade"] for b in _GRADE_BANDS}
        assert "A+" in grades
        assert "A" in grades
        assert "D" in grades

    def test_all_bilingual(self):
        for b in _GRADE_BANDS:
            assert b.get("label_en"), f"{b['grade']} missing label_en"
            assert b.get("label_ar"), f"{b['grade']} missing label_ar"

    def test_all_have_sla_hours(self):
        for b in _GRADE_BANDS:
            assert b.get("sla_hours"), f"{b['grade']} missing sla_hours"

    def test_a_plus_fastest_sla(self):
        a_plus = next(b for b in _GRADE_BANDS if b["grade"] == "A+")
        d_band = next(b for b in _GRADE_BANDS if b["grade"] == "D")
        assert a_plus["sla_hours"] < d_band["sla_hours"]

    def test_all_have_recommended_action(self):
        for b in _GRADE_BANDS:
            assert b.get("recommended_action_en"), f"{b['grade']} missing recommended_action_en"
            assert b.get("recommended_action_ar"), f"{b['grade']} missing recommended_action_ar"


class TestScoreLead:
    def _perfect_input(self, **overrides) -> LeadScoringInput:
        data = dict(
            prospect_name="Ahmed Al-Rashid",
            prospect_company="Almarai",
            sector="ai_software",
            company_size_employees=200,
            sector_fit_score=20.0,
            company_size_fit_score=15.0,
            pain_clarity_score=15.0,
            budget_signal_score=15.0,
            champion_quality_score=10.0,
            timing_signal_score=10.0,
            competitor_dissatisfaction_score=8.0,
            vision_2030_alignment_score=7.0,
        )
        data.update(overrides)
        return LeadScoringInput(**data)

    def _weak_input(self, **overrides) -> LeadScoringInput:
        data = dict(
            prospect_name="Unknown",
            prospect_company="Small Co",
            sector="unknown",
            company_size_employees=5,
            sector_fit_score=2.0,
            company_size_fit_score=2.0,
            pain_clarity_score=2.0,
            budget_signal_score=2.0,
            champion_quality_score=1.0,
            timing_signal_score=1.0,
            competitor_dissatisfaction_score=1.0,
            vision_2030_alignment_score=0.0,
        )
        data.update(overrides)
        return LeadScoringInput(**data)

    def test_perfect_score_100(self):
        result = _score_lead(self._perfect_input())
        assert result["total_score"] == 100.0

    def test_perfect_grade_a_plus(self):
        result = _score_lead(self._perfect_input())
        assert result["grade"] == "A+"

    def test_weak_grade_is_low(self):
        result = _score_lead(self._weak_input())
        assert result["grade"] in ("C", "D")

    def test_has_sla_hours(self):
        result = _score_lead(self._perfect_input())
        assert result["sla_hours"] > 0

    def test_has_next_steps(self):
        result = _score_lead(self._perfect_input())
        assert len(result["next_steps_en"]) >= 2

    def test_top_strengths_populated_for_high_score(self):
        result = _score_lead(self._perfect_input())
        assert len(result["top_strengths"]) > 0

    def test_gaps_populated_for_weak_input(self):
        result = _score_lead(self._weak_input())
        assert len(result["gaps"]) > 0

    def test_partial_scores_sum_correctly(self):
        result = _score_lead(self._perfect_input(
            sector_fit_score=10.0,
            company_size_fit_score=5.0,
            pain_clarity_score=5.0,
            budget_signal_score=5.0,
            champion_quality_score=5.0,
            timing_signal_score=5.0,
            competitor_dissatisfaction_score=4.0,
            vision_2030_alignment_score=3.5,
        ))
        assert result["total_score"] == pytest.approx(42.5)

    def test_scores_out_of_range_rejected(self):
        with pytest.raises(Exception):
            LeadScoringInput(
                prospect_name="Test",
                prospect_company="Test Co",
                sector="ai",
                company_size_employees=100,
                sector_fit_score=25.0,  # max is 20
                company_size_fit_score=15.0,
                pain_clarity_score=15.0,
                budget_signal_score=15.0,
                champion_quality_score=10.0,
                timing_signal_score=10.0,
                competitor_dissatisfaction_score=8.0,
                vision_2030_alignment_score=7.0,
            )

    def test_result_has_grade_and_label(self):
        result = _score_lead(self._perfect_input())
        assert "grade" in result
        assert "label_en" in result

    @pytest.mark.parametrize("score,expected_grade", [
        (90.0, "A+"),
        (75.0, "A"),
        (60.0, "B"),
        (45.0, "C"),
        (20.0, "D"),
    ])
    def test_grade_thresholds(self, score, expected_grade):
        # Build input that sums to approx score by scaling all fields proportionally
        scale = score / 100.0
        inp = self._perfect_input(
            sector_fit_score=round(20.0 * scale, 1),
            company_size_fit_score=round(15.0 * scale, 1),
            pain_clarity_score=round(15.0 * scale, 1),
            budget_signal_score=round(15.0 * scale, 1),
            champion_quality_score=round(10.0 * scale, 1),
            timing_signal_score=round(10.0 * scale, 1),
            competitor_dissatisfaction_score=round(8.0 * scale, 1),
            vision_2030_alignment_score=round(7.0 * scale, 1),
        )
        result = _score_lead(inp)
        # Grade should match expected (within rounding tolerance)
        assert result["grade"] == expected_grade


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/lead-scoring"

    def test_router_tags(self):
        assert "Sales" in router.tags
