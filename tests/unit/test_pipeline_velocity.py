"""Unit tests for api/routers/pipeline_velocity.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.pipeline_velocity import (
    _PIPELINE_HEALTH_SIGNALS,
    _STAGE_VELOCITY_BENCHMARKS,
    _VALID_STAGES,
    DealVelocityInput,
    _analyze_velocity,
    router,
)


def _make_input(**overrides) -> DealVelocityInput:
    data = dict(
        deal_name="Aramco Deal",
        stage="discovery",
        days_in_stage=3,
        deal_value_sar=50000.0,
        has_champion=True,
        last_activity_days_ago=1,
    )
    data.update(overrides)
    return DealVelocityInput(**data)


# ---------------------------------------------------------------------------
# Static data: stage velocity benchmarks
# ---------------------------------------------------------------------------


class TestStageBenchmarks:
    def test_has_six_stages(self):
        assert len(_STAGE_VELOCITY_BENCHMARKS) == 6

    def test_all_have_stage_id(self):
        for s in _STAGE_VELOCITY_BENCHMARKS:
            assert s.get("stage_id"), f"Stage missing stage_id: {s}"

    def test_all_have_stage_name_en(self):
        for s in _STAGE_VELOCITY_BENCHMARKS:
            assert s.get("stage_name_en"), f"Stage {s.get('stage_id')} missing stage_name_en"

    def test_all_have_stage_name_ar(self):
        for s in _STAGE_VELOCITY_BENCHMARKS:
            assert s.get("stage_name_ar"), f"Stage {s.get('stage_id')} missing stage_name_ar"

    def test_all_have_benchmark_days(self):
        for s in _STAGE_VELOCITY_BENCHMARKS:
            assert "benchmark_days" in s, f"Stage {s.get('stage_id')} missing benchmark_days"
            assert isinstance(s["benchmark_days"], int)

    def test_all_have_stall_threshold_days(self):
        for s in _STAGE_VELOCITY_BENCHMARKS:
            assert "stall_threshold_days" in s
            assert s["stall_threshold_days"] > s["benchmark_days"]

    def test_all_have_exit_criteria_en(self):
        for s in _STAGE_VELOCITY_BENCHMARKS:
            assert s.get("exit_criteria_en")

    def test_all_have_exit_criteria_ar(self):
        for s in _STAGE_VELOCITY_BENCHMARKS:
            assert s.get("exit_criteria_ar")

    def test_discovery_benchmark_days(self):
        stage = next(s for s in _STAGE_VELOCITY_BENCHMARKS if s["stage_id"] == "discovery")
        assert stage["benchmark_days"] == 7
        assert stage["stall_threshold_days"] == 14

    def test_qualification_benchmark_days(self):
        stage = next(s for s in _STAGE_VELOCITY_BENCHMARKS if s["stage_id"] == "qualification")
        assert stage["benchmark_days"] == 5
        assert stage["stall_threshold_days"] == 10

    def test_negotiation_benchmark_days(self):
        stage = next(s for s in _STAGE_VELOCITY_BENCHMARKS if s["stage_id"] == "negotiation")
        assert stage["benchmark_days"] == 14
        assert stage["stall_threshold_days"] == 28


# ---------------------------------------------------------------------------
# Static data: valid stages set
# ---------------------------------------------------------------------------


class TestValidStages:
    def test_has_six_items(self):
        assert len(_VALID_STAGES) == 6

    def test_contains_all_expected_stages(self):
        expected = {"discovery", "qualification", "demo", "proposal", "negotiation", "closed"}
        assert expected == _VALID_STAGES

    def test_matches_benchmark_stage_ids(self):
        benchmark_ids = {s["stage_id"] for s in _STAGE_VELOCITY_BENCHMARKS}
        assert benchmark_ids == _VALID_STAGES


# ---------------------------------------------------------------------------
# Static data: pipeline health signals
# ---------------------------------------------------------------------------


class TestPipelineHealthSignals:
    def test_has_five_signals(self):
        assert len(_PIPELINE_HEALTH_SIGNALS) == 5

    def test_all_have_signal_en(self):
        for sig in _PIPELINE_HEALTH_SIGNALS:
            assert sig.get("signal_en"), "Signal missing signal_en"

    def test_all_have_signal_ar(self):
        for sig in _PIPELINE_HEALTH_SIGNALS:
            assert sig.get("signal_ar"), "Signal missing signal_ar"

    def test_all_have_action_en(self):
        for sig in _PIPELINE_HEALTH_SIGNALS:
            assert sig.get("action_en"), "Signal missing action_en"

    def test_all_have_action_ar(self):
        for sig in _PIPELINE_HEALTH_SIGNALS:
            assert sig.get("action_ar"), "Signal missing action_ar"


# ---------------------------------------------------------------------------
# _analyze_velocity
# ---------------------------------------------------------------------------


class TestAnalyzeVelocity:
    def test_returns_dict(self):
        result = _analyze_velocity(_make_input())
        assert isinstance(result, dict)

    def test_has_velocity_status(self):
        result = _analyze_velocity(_make_input())
        assert "velocity_status" in result

    def test_has_urgency_score(self):
        result = _analyze_velocity(_make_input())
        assert "urgency_score" in result

    def test_has_days_over_benchmark(self):
        result = _analyze_velocity(_make_input())
        assert "days_over_benchmark" in result

    def test_has_recommended_action_en(self):
        result = _analyze_velocity(_make_input())
        assert result.get("recommended_action_en")

    def test_has_recommended_action_ar(self):
        result = _analyze_velocity(_make_input())
        assert result.get("recommended_action_ar")

    def test_has_deal_name(self):
        result = _analyze_velocity(_make_input(deal_name="SABIC Contract"))
        assert result["deal_name"] == "SABIC Contract"

    def test_on_track_case(self):
        # discovery benchmark=7; 3 days in stage => on_track
        result = _analyze_velocity(_make_input(stage="discovery", days_in_stage=3))
        assert result["velocity_status"] == "on_track"

    def test_on_track_days_over_benchmark_zero(self):
        result = _analyze_velocity(_make_input(stage="discovery", days_in_stage=3))
        assert result["days_over_benchmark"] == 0

    def test_stalled_case(self):
        # discovery stall_threshold=14; 30 days => stalled
        result = _analyze_velocity(_make_input(stage="discovery", days_in_stage=30))
        assert result["velocity_status"] == "stalled"

    def test_stalled_recommended_action_escalate(self):
        result = _analyze_velocity(_make_input(stage="discovery", days_in_stage=30))
        assert "Escalate" in result["recommended_action_en"]

    def test_slow_case(self):
        # discovery: benchmark=7, stall=14; 10 days => slow
        result = _analyze_velocity(_make_input(stage="discovery", days_in_stage=10))
        assert result["velocity_status"] == "slow"

    def test_slow_recommended_action_accelerate(self):
        result = _analyze_velocity(_make_input(stage="discovery", days_in_stage=10))
        assert "Accelerate" in result["recommended_action_en"]

    def test_on_track_recommended_action_maintain(self):
        result = _analyze_velocity(_make_input(stage="discovery", days_in_stage=3))
        assert "Maintain" in result["recommended_action_en"]

    def test_urgency_score_in_range_0_100(self):
        result = _analyze_velocity(_make_input())
        assert 0 <= result["urgency_score"] <= 100

    def test_no_champion_increases_urgency(self):
        with_champion = _analyze_velocity(
            _make_input(has_champion=True, last_activity_days_ago=1)
        )
        without_champion = _analyze_velocity(
            _make_input(has_champion=False, last_activity_days_ago=1)
        )
        assert without_champion["urgency_score"] > with_champion["urgency_score"]

    def test_late_last_activity_increases_urgency(self):
        recent = _analyze_velocity(_make_input(last_activity_days_ago=1, has_champion=True))
        late = _analyze_velocity(_make_input(last_activity_days_ago=14, has_champion=True))
        assert late["urgency_score"] > recent["urgency_score"]

    def test_urgency_score_capped_at_100(self):
        # Worst case: stalled + no champion + very late activity
        result = _analyze_velocity(
            _make_input(stage="discovery", days_in_stage=100, has_champion=False, last_activity_days_ago=30)
        )
        assert result["urgency_score"] <= 100

    def test_days_over_benchmark_correct(self):
        # discovery benchmark=7; 10 days => 3 over
        result = _analyze_velocity(_make_input(stage="discovery", days_in_stage=10))
        assert result["days_over_benchmark"] == 3

    def test_invalid_stage_raises_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _analyze_velocity(_make_input(stage="invalid_stage"))
        assert exc_info.value.status_code == 422

    def test_governance_decision_allow_with_review(self):
        result = _analyze_velocity(_make_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    @pytest.mark.parametrize("stage", ["discovery", "qualification", "demo", "proposal", "negotiation", "closed"])
    def test_all_valid_stages_work(self, stage):
        result = _analyze_velocity(_make_input(stage=stage))
        assert result["velocity_status"] in {"on_track", "slow", "stalled"}

    def test_qualification_stage(self):
        # benchmark=5, stall=10; 3 days => on_track
        result = _analyze_velocity(_make_input(stage="qualification", days_in_stage=3))
        assert result["velocity_status"] == "on_track"

    def test_closed_stage_stalled(self):
        # benchmark=3, stall=7; 10 days => stalled
        result = _analyze_velocity(_make_input(stage="closed", days_in_stage=10))
        assert result["velocity_status"] == "stalled"


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/pipeline-velocity"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
