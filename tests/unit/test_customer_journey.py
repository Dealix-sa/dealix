"""Unit tests for api/routers/customer_journey.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.customer_journey import (
    _JOURNEY_STAGES,
    _TOUCHPOINT_LIBRARY,
    _JOURNEY_HEALTH_INDICATORS,
    _VALID_JOURNEY_STAGES,
    JourneyMappingInput,
    _map_customer_journey,
    router,
)


def _make_input(**overrides) -> JourneyMappingInput:
    data = dict(
        client_name="Noura Al-Ghamdi",
        current_stage="consideration",
        days_in_current_stage=7,
        has_completed_onboarding=False,
        first_value_delivered=False,
        nps_score=7.0,
    )
    data.update(overrides)
    return JourneyMappingInput(**data)


# ---------------------------------------------------------------------------
# Static data: _JOURNEY_STAGES
# ---------------------------------------------------------------------------


class TestJourneyStages:
    def test_has_six_stages(self):
        assert len(_JOURNEY_STAGES) == 6

    def test_ordered_1_to_6(self):
        orders = [s["order"] for s in _JOURNEY_STAGES]
        assert orders == [1, 2, 3, 4, 5, 6]

    def test_all_have_stage_id(self):
        for s in _JOURNEY_STAGES:
            assert s.get("stage_id"), f"Stage order {s.get('order')} missing stage_id"

    def test_all_have_stage_name_en(self):
        for s in _JOURNEY_STAGES:
            assert s.get("stage_name_en"), f"{s.get('stage_id')} missing stage_name_en"

    def test_all_have_stage_name_ar(self):
        for s in _JOURNEY_STAGES:
            assert s.get("stage_name_ar"), f"{s.get('stage_id')} missing stage_name_ar"

    def test_all_have_avg_duration_days(self):
        for s in _JOURNEY_STAGES:
            assert isinstance(s.get("avg_duration_days"), int), (
                f"{s.get('stage_id')} missing avg_duration_days int"
            )

    def test_all_have_key_experience_en(self):
        for s in _JOURNEY_STAGES:
            assert s.get("key_experience_en"), f"{s.get('stage_id')} missing key_experience_en"

    def test_all_have_key_experience_ar(self):
        for s in _JOURNEY_STAGES:
            assert s.get("key_experience_ar"), f"{s.get('stage_id')} missing key_experience_ar"

    def test_all_have_success_metrics_en_list(self):
        for s in _JOURNEY_STAGES:
            metrics = s.get("success_metrics_en", [])
            assert isinstance(metrics, list), f"{s.get('stage_id')} success_metrics_en must be list"
            assert len(metrics) == 2, f"{s.get('stage_id')} must have exactly 2 success_metrics_en"

    def test_all_have_dropout_risks_en_list(self):
        for s in _JOURNEY_STAGES:
            risks = s.get("dropout_risks_en", [])
            assert isinstance(risks, list), f"{s.get('stage_id')} dropout_risks_en must be list"
            assert len(risks) == 2, f"{s.get('stage_id')} must have exactly 2 dropout_risks_en"

    def test_awareness_order_is_1(self):
        s = next(x for x in _JOURNEY_STAGES if x["stage_id"] == "awareness")
        assert s["order"] == 1

    def test_expansion_order_is_6(self):
        s = next(x for x in _JOURNEY_STAGES if x["stage_id"] == "expansion")
        assert s["order"] == 6

    def test_expansion_avg_duration_days_is_0(self):
        s = next(x for x in _JOURNEY_STAGES if x["stage_id"] == "expansion")
        assert s["avg_duration_days"] == 0


# ---------------------------------------------------------------------------
# Static data: _TOUCHPOINT_LIBRARY
# ---------------------------------------------------------------------------


class TestTouchpointLibrary:
    def test_has_eight_touchpoints(self):
        assert len(_TOUCHPOINT_LIBRARY) == 8

    def test_all_have_touchpoint_en(self):
        for t in _TOUCHPOINT_LIBRARY:
            assert t.get("touchpoint_en"), "Touchpoint missing touchpoint_en"

    def test_all_have_touchpoint_ar(self):
        for t in _TOUCHPOINT_LIBRARY:
            assert t.get("touchpoint_ar"), "Touchpoint missing touchpoint_ar"

    def test_all_have_stage_id(self):
        for t in _TOUCHPOINT_LIBRARY:
            assert t.get("stage_id"), "Touchpoint missing stage_id"

    def test_all_stage_ids_are_valid(self):
        for t in _TOUCHPOINT_LIBRARY:
            assert t["stage_id"] in _VALID_JOURNEY_STAGES, (
                f"Touchpoint has unknown stage_id: {t['stage_id']}"
            )

    def test_all_have_channel(self):
        for t in _TOUCHPOINT_LIBRARY:
            assert t.get("channel"), "Touchpoint missing channel"

    def test_all_have_impact(self):
        valid_impacts = {"high", "medium", "low"}
        for t in _TOUCHPOINT_LIBRARY:
            assert t.get("impact") in valid_impacts, f"Touchpoint has invalid impact: {t.get('impact')}"


# ---------------------------------------------------------------------------
# Static data: _JOURNEY_HEALTH_INDICATORS
# ---------------------------------------------------------------------------


class TestJourneyHealthIndicators:
    def test_has_five_indicators(self):
        assert len(_JOURNEY_HEALTH_INDICATORS) == 5

    def test_all_have_indicator_en(self):
        for i in _JOURNEY_HEALTH_INDICATORS:
            assert i.get("indicator_en"), "Indicator missing indicator_en"

    def test_all_have_indicator_ar(self):
        for i in _JOURNEY_HEALTH_INDICATORS:
            assert i.get("indicator_ar"), "Indicator missing indicator_ar"

    def test_all_have_measurement_en(self):
        for i in _JOURNEY_HEALTH_INDICATORS:
            assert i.get("measurement_en"), "Indicator missing measurement_en"


# ---------------------------------------------------------------------------
# _map_customer_journey
# ---------------------------------------------------------------------------


class TestMapCustomerJourney:
    def test_returns_dict(self):
        result = _map_customer_journey(_make_input())
        assert isinstance(result, dict)

    def test_has_client_name(self):
        result = _map_customer_journey(_make_input(client_name="Sara"))
        assert result["client_name"] == "Sara"

    def test_has_current_stage(self):
        result = _map_customer_journey(_make_input(current_stage="purchase"))
        assert result["current_stage"] == "purchase"

    def test_has_stage_health(self):
        result = _map_customer_journey(_make_input())
        assert "stage_health" in result

    def test_has_next_stage(self):
        result = _map_customer_journey(_make_input())
        assert "next_stage" in result

    def test_has_journey_completion_pct(self):
        result = _map_customer_journey(_make_input())
        assert "journey_completion_pct" in result

    def test_has_priority_touchpoints(self):
        result = _map_customer_journey(_make_input())
        assert "priority_touchpoints" in result

    def test_on_track_when_days_within_avg(self):
        # consideration avg = 14; 7 days <= 14 → on_track
        result = _map_customer_journey(_make_input(current_stage="consideration", days_in_current_stage=7))
        assert result["stage_health"] == "on_track"

    def test_slow_when_days_exceed_avg(self):
        # consideration avg = 14; 20 > 14 but <= 28 → slow
        result = _map_customer_journey(_make_input(current_stage="consideration", days_in_current_stage=20))
        assert result["stage_health"] == "slow"

    def test_at_risk_when_days_exceed_double_avg(self):
        # consideration avg = 14; 30 > 28 → at_risk
        result = _map_customer_journey(_make_input(current_stage="consideration", days_in_current_stage=30))
        assert result["stage_health"] == "at_risk"

    def test_expansion_always_on_track(self):
        # expansion avg = 0 → always on_track regardless of days
        result = _map_customer_journey(_make_input(current_stage="expansion", days_in_current_stage=999))
        assert result["stage_health"] == "on_track"

    def test_awareness_stage1_completion_pct_is_0(self):
        result = _map_customer_journey(_make_input(current_stage="awareness", days_in_current_stage=1))
        assert result["journey_completion_pct"] == pytest.approx(0.0)

    def test_expansion_stage6_completion_pct_is_100(self):
        result = _map_customer_journey(_make_input(current_stage="expansion", days_in_current_stage=0))
        assert result["journey_completion_pct"] == pytest.approx(100.0)

    def test_consideration_stage2_completion_pct(self):
        # order 2: (2-1)/5 * 100 = 20%
        result = _map_customer_journey(_make_input(current_stage="consideration", days_in_current_stage=1))
        assert result["journey_completion_pct"] == pytest.approx(20.0)

    def test_value_realization_stage5_completion_pct(self):
        # order 5: (5-1)/5 * 100 = 80%
        result = _map_customer_journey(_make_input(current_stage="value_realization", days_in_current_stage=1))
        assert result["journey_completion_pct"] == pytest.approx(80.0)

    def test_next_stage_from_awareness_is_consideration(self):
        result = _map_customer_journey(_make_input(current_stage="awareness", days_in_current_stage=1))
        assert result["next_stage"] == "consideration"

    def test_next_stage_from_expansion_is_none(self):
        result = _map_customer_journey(_make_input(current_stage="expansion", days_in_current_stage=0))
        assert result["next_stage"] is None

    def test_priority_touchpoints_max_three(self):
        result = _map_customer_journey(_make_input())
        assert len(result["priority_touchpoints"]) <= 3

    def test_priority_touchpoints_match_current_stage(self):
        result = _map_customer_journey(_make_input(current_stage="consideration"))
        for tp in result["priority_touchpoints"]:
            assert tp["stage_id"] == "consideration"

    def test_governance_decision_is_allow_with_review(self):
        result = _map_customer_journey(_make_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_invalid_current_stage_raises_http_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _map_customer_journey(_make_input(current_stage="invalid_stage"))
        assert exc_info.value.status_code == 422

    def test_all_six_valid_stages_work(self):
        for stage in _VALID_JOURNEY_STAGES:
            result = _map_customer_journey(_make_input(current_stage=stage, days_in_current_stage=0))
            assert result["current_stage"] == stage

    def test_priority_touchpoints_sorted_high_first(self):
        result = _map_customer_journey(_make_input(current_stage="awareness", days_in_current_stage=1))
        impacts = [tp["impact"] for tp in result["priority_touchpoints"]]
        order_map = {"high": 0, "medium": 1, "low": 2}
        ordered = sorted(impacts, key=lambda x: order_map[x])
        assert impacts == ordered


# ---------------------------------------------------------------------------
# _VALID_JOURNEY_STAGES
# ---------------------------------------------------------------------------


class TestValidJourneyStages:
    def test_has_six_values(self):
        assert len(_VALID_JOURNEY_STAGES) == 6

    def test_contains_awareness(self):
        assert "awareness" in _VALID_JOURNEY_STAGES

    def test_contains_consideration(self):
        assert "consideration" in _VALID_JOURNEY_STAGES

    def test_contains_purchase(self):
        assert "purchase" in _VALID_JOURNEY_STAGES

    def test_contains_onboarding(self):
        assert "onboarding" in _VALID_JOURNEY_STAGES

    def test_contains_value_realization(self):
        assert "value_realization" in _VALID_JOURNEY_STAGES

    def test_contains_expansion(self):
        assert "expansion" in _VALID_JOURNEY_STAGES


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/customer-journey"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
