"""
Unit tests for api/routers/pipeline_analytics.py

Tests cover:
- Saudi benchmarks: stages, conversion rates, velocity multipliers
- Stage playbooks: 5 stages, bilingual, exit criteria, risk signals
- _analyze_pipeline: win rate, health bands, Ramadan velocity
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.pipeline_analytics import (
    _SAUDI_BENCHMARKS,
    _STAGE_PLAYBOOKS,
    _analyze_pipeline,
    PipelineHealthInput,
    router,
)


class TestSaudiBenchmarks:
    def test_avg_deal_cycle_45_days(self):
        assert _SAUDI_BENCHMARKS["avg_deal_cycle_days"] == 45

    def test_five_stages_defined(self):
        assert len(_SAUDI_BENCHMARKS["typical_stages"]) == 5

    def test_stages_are_prospect_to_close(self):
        stages = _SAUDI_BENCHMARKS["typical_stages"]
        assert stages[0] == "Prospect"
        assert stages[-1] == "Close"

    def test_conversion_rates_present(self):
        rates = _SAUDI_BENCHMARKS["stage_conversion_rates_pct"]
        assert "Prospect_to_Qualify" in rates
        assert "Commit_to_Close" in rates

    def test_commit_to_close_highest_rate(self):
        rates = _SAUDI_BENCHMARKS["stage_conversion_rates_pct"]
        assert rates["Commit_to_Close"] >= rates["Prospect_to_Qualify"]

    def test_avg_deal_size_has_managed_ops(self):
        sizes = _SAUDI_BENCHMARKS["avg_deal_size_sar"]
        assert sizes["managed_ops"] == 3500

    def test_ramadan_velocity_multiplier_below_1(self):
        mult = _SAUDI_BENCHMARKS["velocity_multipliers"]["ramadan_period"]
        assert mult < 1.0

    def test_post_eid_velocity_multiplier_above_1(self):
        mult = _SAUDI_BENCHMARKS["velocity_multipliers"]["post_eid_period"]
        assert mult > 1.0


class TestStagePlaybooks:
    def test_five_stages(self):
        assert len(_STAGE_PLAYBOOKS) == 5

    def test_all_five_stage_names(self):
        assert set(_STAGE_PLAYBOOKS.keys()) == {"Prospect", "Qualify", "Validate", "Commit", "Close"}

    def test_all_stages_bilingual(self):
        for stage, data in _STAGE_PLAYBOOKS.items():
            assert data.get("stage_en"), f"{stage} missing stage_en"
            assert data.get("stage_ar"), f"{stage} missing stage_ar"

    def test_all_stages_have_exit_criteria(self):
        for stage, data in _STAGE_PLAYBOOKS.items():
            assert len(data.get("exit_criteria_en", [])) >= 2, f"{stage} needs ≥2 exit criteria"

    def test_all_stages_have_top_activities(self):
        for stage, data in _STAGE_PLAYBOOKS.items():
            assert len(data.get("top_activities_en", [])) >= 2, f"{stage} needs ≥2 activities"

    def test_all_stages_have_risk_signals(self):
        for stage, data in _STAGE_PLAYBOOKS.items():
            assert len(data.get("risk_signals_en", [])) >= 1, f"{stage} needs ≥1 risk signal"

    def test_all_stages_have_avg_days(self):
        for stage, data in _STAGE_PLAYBOOKS.items():
            assert data.get("avg_days_in_stage", 0) > 0, f"{stage} missing avg_days_in_stage"

    def test_close_fastest_stage(self):
        close_days = _STAGE_PLAYBOOKS["Close"]["avg_days_in_stage"]
        validate_days = _STAGE_PLAYBOOKS["Validate"]["avg_days_in_stage"]
        assert close_days < validate_days

    def test_commit_stage_mentions_procurement(self):
        activities = " ".join(_STAGE_PLAYBOOKS["Commit"]["top_activities_en"]).lower()
        assert "procurement" in activities or "legal" in activities or "contract" in activities


class TestAnalyzePipeline:
    def _healthy_input(self, **overrides) -> PipelineHealthInput:
        data = dict(
            total_pipeline_sar=100_000.0,
            deals_by_stage={"Prospect": 5, "Qualify": 3, "Validate": 2},
            avg_deal_age_days=30.0,
            won_deals_last_90d=8,
            lost_deals_last_90d=6,
            open_deals_total=10,
            is_ramadan_period=False,
        )
        data.update(overrides)
        return PipelineHealthInput(**data)

    def test_healthy_pipeline(self):
        result = _analyze_pipeline(self._healthy_input())
        assert result["pipeline_health"] == "Healthy"

    def test_win_rate_calculated(self):
        result = _analyze_pipeline(self._healthy_input(won_deals_last_90d=8, lost_deals_last_90d=6))
        # 8/(8+6) = 57.1%
        assert abs(result["win_rate_pct"] - 57.1) < 1.0

    def test_zero_closed_deals_win_rate_zero(self):
        result = _analyze_pipeline(self._healthy_input(won_deals_last_90d=0, lost_deals_last_90d=0))
        assert result["win_rate_pct"] == 0.0

    def test_ramadan_velocity_adjustment(self):
        normal = _analyze_pipeline(self._healthy_input(is_ramadan_period=False))
        ramadan = _analyze_pipeline(self._healthy_input(is_ramadan_period=True))
        assert ramadan["velocity_adjustment"] < normal["velocity_adjustment"]

    def test_ramadan_velocity_is_0_6(self):
        result = _analyze_pipeline(self._healthy_input(is_ramadan_period=True))
        assert result["velocity_adjustment"] == pytest.approx(0.6)

    def test_non_ramadan_velocity_is_1_0(self):
        result = _analyze_pipeline(self._healthy_input(is_ramadan_period=False))
        assert result["velocity_adjustment"] == pytest.approx(1.0)

    def test_coverage_ratio_positive(self):
        result = _analyze_pipeline(self._healthy_input(total_pipeline_sar=50_000))
        assert result["coverage_ratio"] > 0

    def test_low_win_rate_at_risk(self):
        result = _analyze_pipeline(self._healthy_input(
            won_deals_last_90d=2,
            lost_deals_last_90d=10,
            avg_deal_age_days=60.0,
        ))
        assert result["pipeline_health"] in ("At Risk", "Critical")

    def test_has_recommended_actions(self):
        result = _analyze_pipeline(self._healthy_input())
        assert len(result["recommended_actions"]) >= 2

    def test_has_bilingual_health(self):
        result = _analyze_pipeline(self._healthy_input())
        assert result.get("pipeline_health")
        assert result.get("pipeline_health_ar")

    def test_result_has_governance(self):
        result = _analyze_pipeline(self._healthy_input())
        assert result.get("governance_decision") == "ALLOW_WITH_REVIEW"

    def test_total_pipeline_sar_in_result(self):
        result = _analyze_pipeline(self._healthy_input(total_pipeline_sar=75_000))
        assert result["total_pipeline_sar"] == 75_000.0


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/pipeline-analytics"

    def test_router_tags(self):
        assert "Analytics" in router.tags
