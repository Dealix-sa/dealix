"""Tests for the Pipeline Intelligence Engine.

Covers opportunity scoring, pipeline analysis, revenue forecasting,
deal velocity, at-risk identification, and safety invariants.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.execution_contracts import OpportunityStage
from dealix.company_intelligence.pipeline_engine import (
    DealHealth,
    DealVelocity,
    ForecastConfidence,
    OpportunityScore,
    PipelineActionType,
    PipelineAnalysis,
    PipelineHealth,
    PipelineRecommendation,
    RevenueForecast,
    analyze_pipeline,
    assess_deal_velocity,
    forecast_revenue,
    identify_at_risk_deals,
    recommend_pipeline_actions,
    score_opportunity,
)

TENANT = "tenant_test_pipeline"
SOURCE = "test_source"


# -----------------------------------------------------------------------
# Opportunity scoring
# -----------------------------------------------------------------------


class TestOpportunityScoring:
    def test_basic_score(self):
        score = score_opportunity(
            tenant_id=TENANT,
            opportunity_id="opp_001",
            source_id=SOURCE,
        )
        assert isinstance(score, OpportunityScore)
        assert score.tenant_id == TENANT
        assert score.opportunity_id == "opp_001"
        assert 0.0 <= score.overall_score <= 1.0

    def test_deterministic_id(self):
        s1 = score_opportunity(
            tenant_id=TENANT, opportunity_id="opp_001", source_id=SOURCE,
        )
        s2 = score_opportunity(
            tenant_id=TENANT, opportunity_id="opp_001", source_id=SOURCE,
        )
        assert s1.score_id == s2.score_id
        assert s1.score_id.startswith("oppscore_")

    def test_high_scores_thriving(self):
        score = score_opportunity(
            tenant_id=TENANT,
            opportunity_id="opp_high",
            fit_score=0.9,
            engagement_score=0.9,
            timing_score=0.9,
            authority_score=0.9,
            source_id=SOURCE,
        )
        assert score.deal_health == DealHealth.THRIVING
        assert score.overall_score >= 0.7

    def test_stalled_deal(self):
        score = score_opportunity(
            tenant_id=TENANT,
            opportunity_id="opp_stalled",
            days_in_stage=45,
            source_id=SOURCE,
        )
        assert score.deal_health == DealHealth.STALLED
        assert "stalled" in score.score_reasons[0]

    def test_at_risk_deal(self):
        score = score_opportunity(
            tenant_id=TENANT,
            opportunity_id="opp_risk",
            days_in_stage=20,
            source_id=SOURCE,
        )
        assert score.deal_health == DealHealth.AT_RISK

    def test_lost_deal(self):
        score = score_opportunity(
            tenant_id=TENANT,
            opportunity_id="opp_lost",
            stage=OpportunityStage.LOST,
            source_id=SOURCE,
        )
        assert score.deal_health == DealHealth.LOST
        assert score.conversion_probability == 0.0

    def test_won_deal_full_probability(self):
        score = score_opportunity(
            tenant_id=TENANT,
            opportunity_id="opp_won",
            stage=OpportunityStage.WON,
            source_id=SOURCE,
        )
        assert score.conversion_probability == 1.0

    def test_stage_probability_increases(self):
        early = score_opportunity(
            tenant_id=TENANT,
            opportunity_id="opp_early",
            stage=OpportunityStage.RESEARCH,
            source_id=SOURCE,
        )
        late = score_opportunity(
            tenant_id=TENANT,
            opportunity_id="opp_late",
            stage=OpportunityStage.COMMERCIAL,
            source_id=SOURCE,
        )
        assert late.conversion_probability > early.conversion_probability


# -----------------------------------------------------------------------
# Pipeline analysis
# -----------------------------------------------------------------------


class TestPipelineAnalysis:
    def test_empty_pipeline(self):
        analysis = analyze_pipeline(
            tenant_id=TENANT, source_id=SOURCE,
        )
        assert analysis.pipeline_health == PipelineHealth.CRITICAL
        assert analysis.total_opportunities == 0
        assert "empty pipeline" in analysis.top_risks[0]

    def test_healthy_pipeline(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id=f"opp_{i}",
                fit_score=0.7,
                engagement_score=0.7,
                stage=OpportunityStage.CONVERSATION,
                source_id=SOURCE,
            )
            for i in range(5)
        ]
        analysis = analyze_pipeline(
            tenant_id=TENANT, scores=scores, source_id=SOURCE,
        )
        assert analysis.pipeline_health in (
            PipelineHealth.HEALTHY, PipelineHealth.EXCELLENT,
        )
        assert analysis.active_opportunities == 5

    def test_deterministic_id(self):
        a1 = analyze_pipeline(tenant_id=TENANT, source_id=SOURCE)
        a2 = analyze_pipeline(tenant_id=TENANT, source_id=SOURCE)
        assert a1.analysis_id == a2.analysis_id
        assert a1.analysis_id.startswith("pipeline_")

    def test_stage_distribution_captured(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_a",
                stage=OpportunityStage.RESEARCH,
                source_id=SOURCE,
            ),
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_b",
                stage=OpportunityStage.PILOT,
                source_id=SOURCE,
            ),
        ]
        analysis = analyze_pipeline(
            tenant_id=TENANT, scores=scores, source_id=SOURCE,
        )
        stage_dict = dict(analysis.stage_distribution)
        assert stage_dict.get("research") == 1
        assert stage_dict.get("pilot") == 1

    def test_stalled_pipeline_critical(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id=f"opp_{i}",
                days_in_stage=60,
                source_id=SOURCE,
            )
            for i in range(4)
        ]
        analysis = analyze_pipeline(
            tenant_id=TENANT, scores=scores, source_id=SOURCE,
        )
        assert analysis.pipeline_health == PipelineHealth.CRITICAL


# -----------------------------------------------------------------------
# Revenue forecasting
# -----------------------------------------------------------------------


class TestRevenueForecast:
    def test_basic_forecast(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_f1",
                stage=OpportunityStage.PILOT,
                source_id=SOURCE,
            ),
        ]
        forecast = forecast_revenue(
            tenant_id=TENANT,
            scores=scores,
            deal_values={"opp_f1": 50000.0},
            source_id=SOURCE,
        )
        assert isinstance(forecast, RevenueForecast)
        assert forecast.is_hypothesis is True
        assert forecast.recognized_revenue is False
        assert forecast.weighted_pipeline_value > 0

    def test_empty_pipeline_forecast(self):
        forecast = forecast_revenue(
            tenant_id=TENANT, source_id=SOURCE,
        )
        assert forecast.weighted_pipeline_value == 0.0
        assert forecast.confidence == ForecastConfidence.SPECULATIVE

    def test_deterministic_id(self):
        f1 = forecast_revenue(tenant_id=TENANT, source_id=SOURCE)
        f2 = forecast_revenue(tenant_id=TENANT, source_id=SOURCE)
        assert f1.forecast_id == f2.forecast_id
        assert f1.forecast_id.startswith("forecast_")

    def test_won_deals_committed(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_won",
                stage=OpportunityStage.WON,
                source_id=SOURCE,
            ),
        ]
        forecast = forecast_revenue(
            tenant_id=TENANT,
            scores=scores,
            deal_values={"opp_won": 100000.0},
            source_id=SOURCE,
        )
        assert forecast.committed_value == 100000.0

    def test_lost_deals_excluded(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_lost",
                stage=OpportunityStage.LOST,
                source_id=SOURCE,
            ),
        ]
        forecast = forecast_revenue(
            tenant_id=TENANT,
            scores=scores,
            deal_values={"opp_lost": 100000.0},
            source_id=SOURCE,
        )
        assert forecast.weighted_pipeline_value == 0.0


# -----------------------------------------------------------------------
# Deal velocity
# -----------------------------------------------------------------------


class TestDealVelocity:
    def test_basic_velocity(self):
        velocity = assess_deal_velocity(
            tenant_id=TENANT,
            opportunity_id="opp_v1",
            stage=OpportunityStage.CONVERSATION,
            days_in_stage=5,
            total_days=20,
            stages_completed=3,
            source_id=SOURCE,
        )
        assert isinstance(velocity, DealVelocity)
        assert velocity.avg_days_per_stage > 0
        assert velocity.stages_remaining > 0

    def test_deterministic_id(self):
        v1 = assess_deal_velocity(
            tenant_id=TENANT,
            opportunity_id="opp_v1",
            stage=OpportunityStage.PILOT,
            stages_completed=4,
            total_days=30,
            source_id=SOURCE,
        )
        v2 = assess_deal_velocity(
            tenant_id=TENANT,
            opportunity_id="opp_v1",
            stage=OpportunityStage.PILOT,
            stages_completed=4,
            total_days=30,
            source_id=SOURCE,
        )
        assert v1.velocity_id == v2.velocity_id

    def test_slowing_deal_negative_trend(self):
        velocity = assess_deal_velocity(
            tenant_id=TENANT,
            opportunity_id="opp_slow",
            stage=OpportunityStage.PILOT,
            days_in_stage=30,
            total_days=40,
            stages_completed=4,
            source_id=SOURCE,
        )
        assert velocity.velocity_trend < 0
        assert velocity.is_accelerating is False


# -----------------------------------------------------------------------
# At-risk identification
# -----------------------------------------------------------------------


class TestAtRiskDeals:
    def test_identifies_stalled(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_ok",
                source_id=SOURCE,
            ),
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_stalled",
                days_in_stage=40,
                source_id=SOURCE,
            ),
        ]
        at_risk = identify_at_risk_deals(scores)
        assert len(at_risk) == 1
        assert at_risk[0].opportunity_id == "opp_stalled"

    def test_excludes_won_and_lost(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_won_stale",
                stage=OpportunityStage.WON,
                days_in_stage=90,
                source_id=SOURCE,
            ),
        ]
        at_risk = identify_at_risk_deals(scores)
        assert len(at_risk) == 0

    def test_empty_returns_empty(self):
        assert identify_at_risk_deals([]) == []


# -----------------------------------------------------------------------
# Pipeline recommendations
# -----------------------------------------------------------------------


class TestPipelineRecommendations:
    def test_stalled_gets_reengage(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_stall_rec",
                days_in_stage=40,
                source_id=SOURCE,
            ),
        ]
        recs = recommend_pipeline_actions(scores=scores, source_id=SOURCE)
        assert len(recs) == 1
        assert recs[0].action_type == PipelineActionType.RE_ENGAGE

    def test_commercial_gets_close_now(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_close",
                stage=OpportunityStage.COMMERCIAL,
                source_id=SOURCE,
            ),
        ]
        recs = recommend_pipeline_actions(scores=scores, source_id=SOURCE)
        assert recs[0].action_type == PipelineActionType.CLOSE_NOW

    def test_excludes_won_and_lost(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_done",
                stage=OpportunityStage.WON,
                source_id=SOURCE,
            ),
        ]
        recs = recommend_pipeline_actions(scores=scores, source_id=SOURCE)
        assert len(recs) == 0

    def test_sorted_by_priority(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_low",
                stage=OpportunityStage.RESEARCH,
                source_id=SOURCE,
            ),
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_high",
                stage=OpportunityStage.COMMERCIAL,
                source_id=SOURCE,
            ),
        ]
        recs = recommend_pipeline_actions(scores=scores, source_id=SOURCE)
        assert recs[0].priority >= recs[-1].priority


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestPipelineEngineSafety:
    def test_analysis_never_allows_execution(self):
        with pytest.raises(ValueError, match="never authorize execution"):
            PipelineAnalysis(
                tenant_id=TENANT,
                analysis_id="pipeline_fake",
                execution_allowed=True,
                source_id=SOURCE,
            )

    def test_forecast_always_hypothesis(self):
        with pytest.raises(ValueError, match="hypotheses until evidenced"):
            RevenueForecast(
                tenant_id=TENANT,
                forecast_id="forecast_fake",
                forecast_period="q1",
                is_hypothesis=False,
                source_id=SOURCE,
            )

    def test_forecast_cannot_recognize_revenue(self):
        with pytest.raises(ValueError, match="revenue requires payment"):
            RevenueForecast(
                tenant_id=TENANT,
                forecast_id="forecast_fake",
                forecast_period="q1",
                recognized_revenue=True,
                source_id=SOURCE,
            )

    def test_recommendation_requires_approval(self):
        with pytest.raises(ValueError, match="require approval"):
            PipelineRecommendation(
                tenant_id=TENANT,
                recommendation_id="piperec_fake",
                opportunity_id="opp_fake",
                action_type=PipelineActionType.ACCELERATE,
                description="test",
                rationale="test",
                approval_required=False,
                execution_allowed=False,
                source_id=SOURCE,
            )

    def test_recommendation_never_allows_execution(self):
        with pytest.raises(ValueError, match="never authorize execution"):
            PipelineRecommendation(
                tenant_id=TENANT,
                recommendation_id="piperec_fake",
                opportunity_id="opp_fake",
                action_type=PipelineActionType.ACCELERATE,
                description="test",
                rationale="test",
                approval_required=True,
                execution_allowed=True,
                source_id=SOURCE,
            )
