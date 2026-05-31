"""
Unit tests for api/routers/deal_scoring.py

Tests cover:
- Factor definitions: 9 factors, correct weights, bilingual labels
- _score_deal: arithmetic, stage mapping, weak factor detection
- Action recommendations for zero scores
- Max possible score = sum of all weights
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.deal_scoring import (
    _FACTORS,
    _score_deal,
    DealScoreInput,
    router,
)


_MAX_SCORE = sum(f["weight"] for f in _FACTORS.values())


class TestFactorDefinitions:
    def test_nine_factors(self):
        assert len(_FACTORS) == 9

    def test_meddpicc_factors_present(self):
        expected = {
            "metrics", "economic_buyer", "decision_criteria",
            "decision_process", "paper_process", "identified_pain",
            "champion", "competition", "saudi_cultural_fit"
        }
        assert expected == set(_FACTORS.keys())

    def test_all_have_bilingual_labels(self):
        for fid, f in _FACTORS.items():
            assert f.get("label_ar"), f"{fid} missing label_ar"
            assert f.get("label_en"), f"{fid} missing label_en"

    def test_all_have_weights(self):
        for fid, f in _FACTORS.items():
            assert f.get("weight", 0) > 0, f"{fid} has zero weight"

    def test_economic_buyer_highest_weight(self):
        # EB and champion share highest weight (16 each)
        eb_weight = _FACTORS["economic_buyer"]["weight"]
        for fid, f in _FACTORS.items():
            assert f["weight"] <= eb_weight or fid == "champion"

    def test_all_have_levels(self):
        for fid, f in _FACTORS.items():
            assert f.get("levels"), f"{fid} missing levels"
            assert len(f["levels"]) >= 3

    def test_saudi_cultural_fit_factor_present(self):
        assert "saudi_cultural_fit" in _FACTORS


class TestDealScoring:
    def _make_input(self, **overrides) -> DealScoreInput:
        data = dict(
            deal_name="ACME IT Automation",
            sector="information_technology",
            deal_size_sar=500_000,
            metrics_score=12,
            economic_buyer_score=16,
            decision_criteria_score=10,
            decision_process_score=10,
            paper_process_score=8,
            identified_pain_score=14,
            champion_score=16,
            competition_score=8,
            saudi_cultural_fit_score=6,
        )
        data.update(overrides)
        return DealScoreInput(**data)

    def test_perfect_score_is_100_pct(self):
        result = _score_deal(self._make_input())
        assert result["score_pct"] == 100.0

    def test_perfect_score_stage_is_close(self):
        result = _score_deal(self._make_input())
        assert result["recommended_stage"] == "Close"

    def test_zero_score_stage_is_prospect(self):
        result = _score_deal(self._make_input(
            metrics_score=0,
            economic_buyer_score=0,
            decision_criteria_score=0,
            decision_process_score=0,
            paper_process_score=0,
            identified_pain_score=0,
            champion_score=0,
            competition_score=0,
            saudi_cultural_fit_score=0,
        ))
        assert result["recommended_stage"] == "Prospect"
        assert result["score_pct"] == 0.0

    def test_arithmetic_correct(self):
        result = _score_deal(self._make_input(
            metrics_score=0,
            economic_buyer_score=0,
        ))
        expected_raw = _MAX_SCORE - 12 - 16
        assert result["total_score"] == expected_raw

    def test_max_possible_correct(self):
        result = _score_deal(self._make_input())
        assert result["max_possible"] == _MAX_SCORE

    def test_three_weakest_factors_identified(self):
        result = _score_deal(self._make_input())
        # Perfect score — all factors at max, weakest by pct
        assert len(result["weakest_factors"]) == 3

    def test_low_economic_buyer_generates_action(self):
        result = _score_deal(self._make_input(economic_buyer_score=0))
        actions = " ".join(result["recommended_actions_en"]).lower()
        assert "economic buyer" in actions or "eb" in actions or "buyer" in actions

    def test_low_champion_generates_action(self):
        result = _score_deal(self._make_input(champion_score=0))
        actions = " ".join(result["recommended_actions_en"]).lower()
        assert "champion" in actions

    def test_low_pain_generates_zatca_action(self):
        result = _score_deal(self._make_input(identified_pain_score=0))
        actions = " ".join(result["recommended_actions_en"]).lower()
        assert "zatca" in actions or "compelling" in actions or "event" in actions

    def test_stage_validate_range(self):
        # Score ~50% → validate
        result = _score_deal(self._make_input(
            metrics_score=6,
            economic_buyer_score=8,
            decision_criteria_score=5,
            decision_process_score=5,
            paper_process_score=4,
            identified_pain_score=7,
            champion_score=8,
            competition_score=4,
            saudi_cultural_fit_score=3,
        ))
        assert result["recommended_stage"] in ("Validate", "Qualify", "Commit")

    def test_deal_name_in_result(self):
        result = _score_deal(self._make_input(deal_name="Test Deal"))
        assert result["deal_name"] == "Test Deal"

    def test_factor_details_nine_entries(self):
        result = _score_deal(self._make_input())
        assert len(result["factor_details"]) == 9

    def test_factor_pct_100_at_max(self):
        result = _score_deal(self._make_input())
        for fd in result["factor_details"]:
            assert fd["pct"] == 100


class TestInputValidation:
    def test_metrics_score_out_of_range(self):
        with pytest.raises(Exception):
            DealScoreInput(
                deal_name="Test", sector="it", deal_size_sar=100_000,
                metrics_score=13,  # > 12
                economic_buyer_score=0, decision_criteria_score=0,
                decision_process_score=0, paper_process_score=0,
                identified_pain_score=0, champion_score=0,
                competition_score=0, saudi_cultural_fit_score=0,
            )


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/deal-scoring"

    def test_router_tags(self):
        assert "Analytics" in router.tags
