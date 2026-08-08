"""Tests for the Learning Intelligence Engine.

Covers win/loss analysis, pattern extraction, strategy recommendations,
learning velocity, and safety invariants.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.learning_engine import (
    InsightCategory,
    LearningVelocity,
    PatternInsight,
    PatternStrength,
    StrategyAdjustmentType,
    StrategyRecommendation,
    WinLossAnalysis,
    analyze_win_loss,
    compute_learning_velocity,
    extract_patterns,
    generate_insights,
)

TENANT = "tenant_test_learning"
SOURCE = "test_source"


# -----------------------------------------------------------------------
# Win/loss analysis
# -----------------------------------------------------------------------


class TestWinLossAnalysis:
    def test_basic_analysis(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT,
            period="2026-Q3",
            win_outcomes=("outcome_w1", "outcome_w2"),
            loss_outcomes=("outcome_l1",),
            source_id=SOURCE,
        )
        assert isinstance(analysis, WinLossAnalysis)
        assert analysis.wins == 2
        assert analysis.losses == 1
        assert analysis.total_outcomes == 3
        assert analysis.win_rate == pytest.approx(0.6667, abs=0.01)

    def test_deterministic_id(self):
        a1 = analyze_win_loss(
            tenant_id=TENANT, period="2026-Q3",
            win_outcomes=("w1",), source_id=SOURCE,
        )
        a2 = analyze_win_loss(
            tenant_id=TENANT, period="2026-Q3",
            win_outcomes=("w1",), source_id=SOURCE,
        )
        assert a1.analysis_id == a2.analysis_id
        assert a1.analysis_id.startswith("winloss_")

    def test_empty_outcomes(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT, period="2026-Q3", source_id=SOURCE,
        )
        assert analysis.total_outcomes == 0
        assert analysis.win_rate == 0.0

    def test_factors_and_objections_captured(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT,
            period="2026-Q3",
            win_outcomes=("w1",),
            win_factors=("strong fit", "good timing"),
            loss_factors=("price too high",),
            objections=("budget constraints", "not now"),
            source_id=SOURCE,
        )
        assert "strong fit" in analysis.common_win_factors
        assert "price too high" in analysis.common_loss_factors
        assert "budget constraints" in analysis.top_objections

    def test_always_hypothesis(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT, period="2026-Q3", source_id=SOURCE,
        )
        assert analysis.is_hypothesis is True


# -----------------------------------------------------------------------
# Pattern extraction
# -----------------------------------------------------------------------


class TestPatternExtraction:
    def test_high_win_rate_pattern(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT,
            period="2026-Q3",
            win_outcomes=tuple(f"w{i}" for i in range(8)),
            loss_outcomes=("l1", "l2"),
            source_id=SOURCE,
        )
        patterns = extract_patterns(
            tenant_id=TENANT, analysis=analysis, source_id=SOURCE,
        )
        targeting_patterns = [
            p for p in patterns if p.category == InsightCategory.TARGETING
        ]
        assert len(targeting_patterns) >= 1
        assert "high win rate" in targeting_patterns[0].pattern_description

    def test_low_win_rate_pattern(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT,
            period="2026-Q3",
            win_outcomes=("w1",),
            loss_outcomes=tuple(f"l{i}" for i in range(5)),
            source_id=SOURCE,
        )
        patterns = extract_patterns(
            tenant_id=TENANT, analysis=analysis, source_id=SOURCE,
        )
        targeting_patterns = [
            p for p in patterns if p.category == InsightCategory.TARGETING
        ]
        assert len(targeting_patterns) >= 1
        assert "low win rate" in targeting_patterns[0].pattern_description

    def test_loss_factors_become_patterns(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT,
            period="2026-Q3",
            loss_outcomes=("l1",),
            loss_factors=("competitor pricing",),
            source_id=SOURCE,
        )
        patterns = extract_patterns(
            tenant_id=TENANT, analysis=analysis, source_id=SOURCE,
        )
        objection_patterns = [
            p for p in patterns if p.category == InsightCategory.OBJECTION
        ]
        assert len(objection_patterns) >= 1

    def test_long_cycle_pattern(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT,
            period="2026-Q3",
            win_outcomes=("w1",),
            avg_cycle_days=60.0,
            source_id=SOURCE,
        )
        patterns = extract_patterns(
            tenant_id=TENANT, analysis=analysis, source_id=SOURCE,
        )
        process_patterns = [
            p for p in patterns if p.category == InsightCategory.PROCESS
        ]
        assert len(process_patterns) >= 1
        assert "long sales cycle" in process_patterns[0].pattern_description

    def test_patterns_are_hypotheses(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT, period="2026-Q3",
            win_outcomes=tuple(f"w{i}" for i in range(10)),
            source_id=SOURCE,
        )
        patterns = extract_patterns(
            tenant_id=TENANT, analysis=analysis, source_id=SOURCE,
        )
        for pattern in patterns:
            assert pattern.is_hypothesis is True


# -----------------------------------------------------------------------
# Strategy recommendations
# -----------------------------------------------------------------------


class TestStrategyRecommendations:
    def test_generates_from_patterns(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT,
            period="2026-Q3",
            win_outcomes=tuple(f"w{i}" for i in range(10)),
            loss_outcomes=("l1",),
            loss_factors=("pricing",),
            objections=("budget",),
            source_id=SOURCE,
        )
        patterns = extract_patterns(
            tenant_id=TENANT, analysis=analysis, source_id=SOURCE,
        )
        recs = generate_insights(patterns=patterns, source_id=SOURCE)
        assert len(recs) >= 1
        for rec in recs:
            assert isinstance(rec, StrategyRecommendation)
            assert rec.approval_required is True
            assert rec.applied is False

    def test_sorted_by_priority(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT,
            period="2026-Q3",
            win_outcomes=tuple(f"w{i}" for i in range(10)),
            loss_factors=("pricing", "timing"),
            objections=("budget",),
            source_id=SOURCE,
        )
        patterns = extract_patterns(
            tenant_id=TENANT, analysis=analysis, source_id=SOURCE,
        )
        recs = generate_insights(patterns=patterns, source_id=SOURCE)
        if len(recs) >= 2:
            assert recs[0].priority >= recs[-1].priority

    def test_targeting_maps_to_refine_icp(self):
        analysis = analyze_win_loss(
            tenant_id=TENANT,
            period="2026-Q3",
            win_outcomes=tuple(f"w{i}" for i in range(10)),
            source_id=SOURCE,
        )
        patterns = extract_patterns(
            tenant_id=TENANT, analysis=analysis, source_id=SOURCE,
        )
        recs = generate_insights(patterns=patterns, source_id=SOURCE)
        targeting_recs = [
            r for r in recs
            if r.adjustment_type == StrategyAdjustmentType.REFINE_ICP
        ]
        assert len(targeting_recs) >= 1

    def test_empty_patterns_no_recommendations(self):
        recs = generate_insights(patterns=[], source_id=SOURCE)
        assert recs == []


# -----------------------------------------------------------------------
# Learning velocity
# -----------------------------------------------------------------------


class TestLearningVelocity:
    def test_improving_velocity(self):
        velocity = compute_learning_velocity(
            tenant_id=TENANT,
            period="2026-Q3",
            patterns_discovered=5,
            recommendations_generated=3,
            previous_win_rate=0.3,
            current_win_rate=0.5,
            source_id=SOURCE,
        )
        assert isinstance(velocity, LearningVelocity)
        assert velocity.is_improving is True
        assert velocity.win_rate_trend > 0

    def test_declining_velocity(self):
        velocity = compute_learning_velocity(
            tenant_id=TENANT,
            period="2026-Q3",
            previous_win_rate=0.5,
            current_win_rate=0.3,
            previous_cycle_days=30,
            current_cycle_days=45,
            source_id=SOURCE,
        )
        assert velocity.is_improving is False
        assert velocity.win_rate_trend < 0

    def test_deterministic_id(self):
        v1 = compute_learning_velocity(
            tenant_id=TENANT, period="2026-Q3",
            patterns_discovered=3, source_id=SOURCE,
        )
        v2 = compute_learning_velocity(
            tenant_id=TENANT, period="2026-Q3",
            patterns_discovered=3, source_id=SOURCE,
        )
        assert v1.velocity_id == v2.velocity_id
        assert v1.velocity_id.startswith("learnvel_")


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestLearningEngineSafety:
    def test_pattern_must_be_hypothesis(self):
        with pytest.raises(ValueError, match="hypotheses until validated"):
            PatternInsight(
                tenant_id=TENANT,
                pattern_id="pattern_fake",
                category=InsightCategory.TARGETING,
                pattern_description="test",
                strength=PatternStrength.STRONG,
                is_hypothesis=False,
                source_id=SOURCE,
            )

    def test_recommendation_requires_approval(self):
        with pytest.raises(ValueError, match="require approval"):
            StrategyRecommendation(
                tenant_id=TENANT,
                recommendation_id="rec_fake",
                adjustment_type=StrategyAdjustmentType.REFINE_ICP,
                description="test",
                rationale="test",
                expected_impact="test",
                approval_required=False,
                applied=False,
                source_id=SOURCE,
            )

    def test_recommendation_cannot_be_pre_applied(self):
        with pytest.raises(ValueError, match="cannot be pre-applied"):
            StrategyRecommendation(
                tenant_id=TENANT,
                recommendation_id="rec_fake",
                adjustment_type=StrategyAdjustmentType.REFINE_ICP,
                description="test",
                rationale="test",
                expected_impact="test",
                approval_required=True,
                applied=True,
                source_id=SOURCE,
            )
