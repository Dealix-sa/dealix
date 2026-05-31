"""Tests for /api/v1/analytics — admin-gated read-only analytics endpoints.

Covers:
  - Demo data integrity (4 weeks, 5 posts, 6 sprints, 6 sectors, 6 funnel stages)
  - Feature adoption (200, governance, most_used, fastest_growing, trend shape)
  - Content performance (200, governance, disclaimer, best post identified)
  - Sprint performance (200, governance, rates computed, avg_nps in range)
  - Conversion funnel (200, governance, disclaimer, stages ordered, rates computed)
  - Sector breakdown (200, governance, 6 sectors, totals consistent)
  - Monthly report (200, governance, all list fields non-empty, key_metrics dict)
  - Helper function unit tests
"""

from __future__ import annotations

import os
import sys
import types

import pytest

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

# ---------------------------------------------------------------------------
# Stub the security module before any router import to avoid jose/crypto issues
# ---------------------------------------------------------------------------
_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.analytics_ops import (  # noqa: E402
    _CONTENT_POSTS,
    _FEATURE_NAMES,
    _FUNNEL_STAGES,
    _SECTORS,
    _SPRINTS,
    _WEEKLY_FEATURE_USAGE,
    _build_funnel_with_rates,
    _build_key_metrics,
    _build_usage_trend,
    _compute_fastest_growing_feature,
    _compute_most_used_feature,
    _compute_overall_conversion_pct,
    _compute_sprint_rates,
    _now_iso,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ===========================================================================
# 1. Demo data integrity
# ===========================================================================


class TestDemoDataIntegrity:
    def test_weekly_feature_usage_has_4_weeks(self):
        assert len(_WEEKLY_FEATURE_USAGE) == 4

    def test_weeks_are_labeled_w4_to_w1(self):
        labels = [w["week"] for w in _WEEKLY_FEATURE_USAGE]
        assert labels == ["W-4", "W-3", "W-2", "W-1"]

    def test_each_week_has_all_feature_keys(self):
        for week in _WEEKLY_FEATURE_USAGE:
            for feature in _FEATURE_NAMES:
                assert feature in week, f"Missing feature '{feature}' in {week['week']}"

    def test_all_weekly_values_are_positive_integers(self):
        for week in _WEEKLY_FEATURE_USAGE:
            for feature in _FEATURE_NAMES:
                val = week[feature]
                assert isinstance(val, int) and val > 0

    def test_content_posts_has_5_entries(self):
        assert len(_CONTENT_POSTS) == 5

    def test_each_post_has_post_id(self):
        for post in _CONTENT_POSTS:
            assert "post_id" in post and post["post_id"]

    def test_each_post_has_topic_ar(self):
        for post in _CONTENT_POSTS:
            assert "topic_ar" in post and post["topic_ar"]

    def test_each_post_has_topic_en(self):
        for post in _CONTENT_POSTS:
            assert "topic_en" in post and post["topic_en"]

    def test_each_post_has_published_date(self):
        for post in _CONTENT_POSTS:
            assert "published_date" in post and post["published_date"]

    def test_each_post_has_impressions_estimate(self):
        for post in _CONTENT_POSTS:
            assert "impressions_estimate" in post
            assert isinstance(post["impressions_estimate"], int)
            assert post["impressions_estimate"] > 0

    def test_each_post_has_engagements_estimate(self):
        for post in _CONTENT_POSTS:
            assert "engagements_estimate" in post
            assert post["engagements_estimate"] > 0

    def test_each_post_has_leads_generated_estimate(self):
        for post in _CONTENT_POSTS:
            assert "leads_generated_estimate" in post
            assert post["leads_generated_estimate"] >= 0

    def test_each_post_is_estimate_true(self):
        for post in _CONTENT_POSTS:
            assert post.get("is_estimate") is True

    def test_sprints_has_6_entries(self):
        assert len(_SPRINTS) == 6

    def test_each_sprint_has_sprint_id(self):
        for sprint in _SPRINTS:
            assert "sprint_id" in sprint and sprint["sprint_id"]

    def test_each_sprint_has_client_id(self):
        for sprint in _SPRINTS:
            assert "client_id" in sprint and sprint["client_id"]

    def test_each_sprint_duration_days_in_range(self):
        for sprint in _SPRINTS:
            assert 5 <= sprint["duration_days"] <= 9

    def test_each_sprint_has_dq_score_improvement(self):
        for sprint in _SPRINTS:
            assert "dq_score_improvement" in sprint
            assert isinstance(sprint["dq_score_improvement"], int)

    def test_each_sprint_has_zatca_compliance_achieved_bool(self):
        for sprint in _SPRINTS:
            assert isinstance(sprint["zatca_compliance_achieved"], bool)

    def test_each_sprint_has_on_time_bool(self):
        for sprint in _SPRINTS:
            assert isinstance(sprint["on_time"], bool)

    def test_each_sprint_nps_score_in_range(self):
        for sprint in _SPRINTS:
            assert 1 <= sprint["nps_score"] <= 10

    def test_each_sprint_has_month(self):
        for sprint in _SPRINTS:
            assert "month" in sprint and sprint["month"]

    def test_funnel_stages_count(self):
        assert len(_FUNNEL_STAGES) == 6

    def test_funnel_stages_ordered_descending(self):
        counts = [s["count"] for s in _FUNNEL_STAGES]
        assert counts == sorted(counts, reverse=True)

    def test_funnel_stages_have_stage_name_ar(self):
        for stage in _FUNNEL_STAGES:
            assert "stage_name_ar" in stage and stage["stage_name_ar"]

    def test_funnel_stages_have_stage_name_en(self):
        for stage in _FUNNEL_STAGES:
            assert "stage_name_en" in stage and stage["stage_name_en"]

    def test_sectors_has_6_entries(self):
        assert len(_SECTORS) == 6

    def test_sectors_have_sector_ar(self):
        for sector in _SECTORS:
            assert "sector_ar" in sector and sector["sector_ar"]

    def test_sectors_have_sector_en(self):
        for sector in _SECTORS:
            assert "sector_en" in sector and sector["sector_en"]

    def test_sectors_have_client_count(self):
        for sector in _SECTORS:
            assert "client_count" in sector
            assert sector["client_count"] > 0

    def test_sectors_have_mrr_sar_estimate(self):
        for sector in _SECTORS:
            assert "mrr_sar_estimate" in sector
            assert sector["mrr_sar_estimate"] > 0

    def test_sectors_have_avg_health_score(self):
        for sector in _SECTORS:
            assert "avg_health_score" in sector
            assert 0 <= sector["avg_health_score"] <= 100


# ===========================================================================
# 2. Feature adoption endpoint
# ===========================================================================


class TestFeatureAdoptionEndpoint:
    def test_returns_200(self):
        resp = client.get("/api/v1/analytics/feature-adoption")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_most_used_feature_present(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert "most_used_feature" in body
        assert body["most_used_feature"]

    def test_most_used_feature_is_valid_feature(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert body["most_used_feature"] in _FEATURE_NAMES

    def test_fastest_growing_feature_present(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert "fastest_growing_feature" in body
        assert body["fastest_growing_feature"]

    def test_fastest_growing_feature_is_valid_feature(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert body["fastest_growing_feature"] in _FEATURE_NAMES

    def test_usage_trend_present(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert "usage_trend" in body

    def test_usage_trend_has_4_entries(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert len(body["usage_trend"]) == 4

    def test_usage_trend_entries_have_week_key(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        for entry in body["usage_trend"]:
            assert "week" in entry

    def test_usage_trend_entries_have_total_active_users(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        for entry in body["usage_trend"]:
            assert "total_active_users" in entry
            assert entry["total_active_users"] > 0

    def test_data_has_4_weeks(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert body["weeks_count"] == 4

    def test_generated_at_present(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert "generated_at" in body

    def test_is_estimate_true(self):
        body = client.get("/api/v1/analytics/feature-adoption").json()
        assert body.get("is_estimate") is True


# ===========================================================================
# 3. Content performance endpoint
# ===========================================================================


class TestContentPerformanceEndpoint:
    def test_returns_200(self):
        resp = client.get("/api/v1/analytics/content-performance")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_posts_list_present(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "posts" in body
        assert isinstance(body["posts"], list)

    def test_posts_count_is_5(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert len(body["posts"]) == 5

    def test_disclaimer_present(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "disclaimer" in body

    def test_disclaimer_contains_arabic(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "تقديرية" in body["disclaimer"]

    def test_disclaimer_contains_english(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "estimates" in body["disclaimer"].lower()

    def test_total_impressions_estimate_present(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "total_impressions_estimate" in body
        assert body["total_impressions_estimate"] > 0

    def test_total_leads_estimate_present(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "total_leads_estimate" in body
        assert body["total_leads_estimate"] > 0

    def test_best_performing_post_topic_present(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "best_performing_post_topic" in body
        assert body["best_performing_post_topic"]

    def test_best_performing_post_topic_ar_present(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "best_performing_post_topic_ar" in body
        assert body["best_performing_post_topic_ar"]

    def test_best_post_id_present(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "best_performing_post_id" in body

    def test_total_impressions_equals_sum_of_posts(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        expected = sum(p["impressions_estimate"] for p in body["posts"])
        assert body["total_impressions_estimate"] == expected

    def test_generated_at_present(self):
        body = client.get("/api/v1/analytics/content-performance").json()
        assert "generated_at" in body


# ===========================================================================
# 4. Sprint performance endpoint
# ===========================================================================


class TestSprintPerformanceEndpoint:
    def test_returns_200(self):
        resp = client.get("/api/v1/analytics/sprint-performance")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_sprints_is_6(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert body["total_sprints"] == 6

    def test_on_time_rate_pct_present(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert "on_time_rate_pct" in body

    def test_on_time_rate_pct_in_valid_range(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert 0.0 <= body["on_time_rate_pct"] <= 100.0

    def test_avg_dq_improvement_present(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert "avg_dq_improvement" in body

    def test_avg_dq_improvement_positive(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert body["avg_dq_improvement"] > 0

    def test_avg_nps_present(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert "avg_nps" in body

    def test_avg_nps_in_valid_range(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert 1.0 <= body["avg_nps"] <= 10.0

    def test_zatca_compliance_rate_pct_present(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert "zatca_compliance_rate_pct" in body

    def test_zatca_compliance_rate_pct_in_valid_range(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert 0.0 <= body["zatca_compliance_rate_pct"] <= 100.0

    def test_sprints_list_present(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert "sprints" in body
        assert isinstance(body["sprints"], list)

    def test_sprints_list_has_6_entries(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert len(body["sprints"]) == 6

    def test_generated_at_present(self):
        body = client.get("/api/v1/analytics/sprint-performance").json()
        assert "generated_at" in body


# ===========================================================================
# 5. Conversion funnel endpoint
# ===========================================================================


class TestConversionFunnelEndpoint:
    def test_returns_200(self):
        resp = client.get("/api/v1/analytics/conversion-funnel")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_disclaimer_present(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert "disclaimer" in body

    def test_disclaimer_contains_arabic(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert "تقديرية" in body["disclaimer"]

    def test_disclaimer_contains_english(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert "estimates" in body["disclaimer"].lower()

    def test_stages_present(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert "stages" in body
        assert isinstance(body["stages"], list)

    def test_stages_count_is_6(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert len(body["stages"]) == 6

    def test_stages_have_stage_name_ar(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        for stage in body["stages"]:
            assert "stage_name_ar" in stage

    def test_stages_have_stage_name_en(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        for stage in body["stages"]:
            assert "stage_name_en" in stage

    def test_stages_have_conversion_rate_pct(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        for stage in body["stages"]:
            assert "conversion_rate_pct" in stage

    def test_first_stage_conversion_rate_is_100(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert body["stages"][0]["conversion_rate_pct"] == 100.0

    def test_stages_counts_are_descending(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        counts = [s["count"] for s in body["stages"]]
        assert counts == sorted(counts, reverse=True)

    def test_overall_conversion_pct_present(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert "overall_conversion_pct" in body

    def test_overall_conversion_pct_in_valid_range(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert 0.0 <= body["overall_conversion_pct"] <= 100.0

    def test_generated_at_present(self):
        body = client.get("/api/v1/analytics/conversion-funnel").json()
        assert "generated_at" in body


# ===========================================================================
# 6. Sector breakdown endpoint
# ===========================================================================


class TestSectorBreakdownEndpoint:
    def test_returns_200(self):
        resp = client.get("/api/v1/analytics/sector-breakdown")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_sectors_list_present(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        assert "sectors" in body
        assert isinstance(body["sectors"], list)

    def test_sectors_count_is_6(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        assert len(body["sectors"]) == 6

    def test_each_sector_has_sector_ar(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        for sector in body["sectors"]:
            assert "sector_ar" in sector and sector["sector_ar"]

    def test_each_sector_has_sector_en(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        for sector in body["sectors"]:
            assert "sector_en" in sector and sector["sector_en"]

    def test_each_sector_has_client_count(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        for sector in body["sectors"]:
            assert "client_count" in sector
            assert sector["client_count"] > 0

    def test_each_sector_has_mrr_sar_estimate(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        for sector in body["sectors"]:
            assert "mrr_sar_estimate" in sector

    def test_each_sector_has_avg_health_score(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        for sector in body["sectors"]:
            assert "avg_health_score" in sector

    def test_total_clients_present(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        assert "total_clients" in body

    def test_total_clients_equals_sum_of_sectors(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        expected = sum(s["client_count"] for s in body["sectors"])
        assert body["total_clients"] == expected

    def test_total_mrr_sar_estimate_present(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        assert "total_mrr_sar_estimate" in body
        assert body["total_mrr_sar_estimate"] > 0

    def test_total_mrr_equals_sum_of_sectors(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        expected = sum(s["mrr_sar_estimate"] for s in body["sectors"])
        assert body["total_mrr_sar_estimate"] == expected

    def test_generated_at_present(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        assert "generated_at" in body

    def test_sector_count_field(self):
        body = client.get("/api/v1/analytics/sector-breakdown").json()
        assert body["sector_count"] == 6


# ===========================================================================
# 7. Monthly report endpoint
# ===========================================================================


class TestMonthlyReportEndpoint:
    def test_returns_200(self):
        resp = client.get("/api/v1/analytics/monthly-report")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_report_month_present(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "report_month" in body
        assert body["report_month"]

    def test_executive_summary_ar_present_and_non_empty(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "executive_summary_ar" in body
        assert body["executive_summary_ar"].strip()

    def test_executive_summary_en_present_and_non_empty(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "executive_summary_en" in body
        assert body["executive_summary_en"].strip()

    def test_top_3_wins_ar_is_list_of_3(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "top_3_wins_ar" in body
        assert isinstance(body["top_3_wins_ar"], list)
        assert len(body["top_3_wins_ar"]) == 3

    def test_top_3_wins_en_is_list_of_3(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "top_3_wins_en" in body
        assert isinstance(body["top_3_wins_en"], list)
        assert len(body["top_3_wins_en"]) == 3

    def test_top_3_wins_ar_all_non_empty(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        for item in body["top_3_wins_ar"]:
            assert isinstance(item, str) and item.strip()

    def test_top_3_wins_en_all_non_empty(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        for item in body["top_3_wins_en"]:
            assert isinstance(item, str) and item.strip()

    def test_top_3_challenges_ar_is_list_of_3(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "top_3_challenges_ar" in body
        assert len(body["top_3_challenges_ar"]) == 3

    def test_top_3_challenges_en_is_list_of_3(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "top_3_challenges_en" in body
        assert len(body["top_3_challenges_en"]) == 3

    def test_top_3_challenges_ar_all_non_empty(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        for item in body["top_3_challenges_ar"]:
            assert isinstance(item, str) and item.strip()

    def test_top_3_challenges_en_all_non_empty(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        for item in body["top_3_challenges_en"]:
            assert isinstance(item, str) and item.strip()

    def test_key_metrics_present(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "key_metrics" in body
        assert isinstance(body["key_metrics"], dict)

    def test_key_metrics_has_8_entries(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert len(body["key_metrics"]) == 8

    def test_key_metrics_total_active_clients(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "total_active_clients" in body["key_metrics"]

    def test_key_metrics_mrr_sar_estimate(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "mrr_sar_estimate" in body["key_metrics"]

    def test_key_metrics_sprints_delivered(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "sprints_delivered" in body["key_metrics"]

    def test_key_metrics_avg_nps_score(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "avg_nps_score" in body["key_metrics"]

    def test_next_month_priorities_ar_is_list_of_3(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "next_month_priorities_ar" in body
        assert len(body["next_month_priorities_ar"]) == 3

    def test_next_month_priorities_en_is_list_of_3(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "next_month_priorities_en" in body
        assert len(body["next_month_priorities_en"]) == 3

    def test_next_month_priorities_ar_all_non_empty(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        for item in body["next_month_priorities_ar"]:
            assert isinstance(item, str) and item.strip()

    def test_next_month_priorities_en_all_non_empty(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        for item in body["next_month_priorities_en"]:
            assert isinstance(item, str) and item.strip()

    def test_generated_at_present(self):
        body = client.get("/api/v1/analytics/monthly-report").json()
        assert "generated_at" in body


# ===========================================================================
# 8. Helper — _now_iso
# ===========================================================================


class TestNowIso:
    def test_returns_string(self):
        result = _now_iso()
        assert isinstance(result, str)

    def test_contains_t_separator(self):
        result = _now_iso()
        assert "T" in result

    def test_contains_timezone_info(self):
        result = _now_iso()
        assert "+" in result or result.endswith("Z") or "+00:00" in result


# ===========================================================================
# 9. Helper — _compute_most_used_feature
# ===========================================================================


class TestComputeMostUsedFeature:
    def test_returns_feature_name_string(self):
        result = _compute_most_used_feature(_WEEKLY_FEATURE_USAGE)
        assert isinstance(result, str)

    def test_returns_valid_feature_name(self):
        result = _compute_most_used_feature(_WEEKLY_FEATURE_USAGE)
        assert result in _FEATURE_NAMES

    def test_returns_dashboard_for_demo_data(self):
        result = _compute_most_used_feature(_WEEKLY_FEATURE_USAGE)
        assert result == "dashboard"

    def test_returns_empty_string_for_empty_input(self):
        result = _compute_most_used_feature([])
        assert result == ""

    def test_ignores_week_key_in_totals(self):
        single = [{"week": "W-1", "dashboard": 5, "pipeline": 3, "health": 1,
                   "subscriptions": 1, "invoices": 1, "proof_packs": 1, "cockpit": 1}]
        result = _compute_most_used_feature(single)
        assert result == "dashboard"


# ===========================================================================
# 10. Helper — _compute_fastest_growing_feature
# ===========================================================================


class TestComputeFastestGrowingFeature:
    def test_returns_feature_name_string(self):
        result = _compute_fastest_growing_feature(_WEEKLY_FEATURE_USAGE)
        assert isinstance(result, str)

    def test_returns_valid_feature_name(self):
        result = _compute_fastest_growing_feature(_WEEKLY_FEATURE_USAGE)
        assert result in _FEATURE_NAMES

    def test_single_entry_returns_first_feature(self):
        single = [{"week": "W-1", "dashboard": 5, "pipeline": 3, "health": 1,
                   "subscriptions": 1, "invoices": 1, "proof_packs": 1, "cockpit": 1}]
        result = _compute_fastest_growing_feature(single)
        assert result in _FEATURE_NAMES

    def test_empty_input_returns_fallback(self):
        result = _compute_fastest_growing_feature([])
        assert result in _FEATURE_NAMES or result == ""


# ===========================================================================
# 11. Helper — _build_usage_trend
# ===========================================================================


class TestBuildUsageTrend:
    def test_returns_list(self):
        result = _build_usage_trend(_WEEKLY_FEATURE_USAGE)
        assert isinstance(result, list)

    def test_length_matches_input(self):
        result = _build_usage_trend(_WEEKLY_FEATURE_USAGE)
        assert len(result) == len(_WEEKLY_FEATURE_USAGE)

    def test_each_entry_has_week(self):
        for entry in _build_usage_trend(_WEEKLY_FEATURE_USAGE):
            assert "week" in entry

    def test_each_entry_has_total_active_users(self):
        for entry in _build_usage_trend(_WEEKLY_FEATURE_USAGE):
            assert "total_active_users" in entry

    def test_totals_are_positive(self):
        for entry in _build_usage_trend(_WEEKLY_FEATURE_USAGE):
            assert entry["total_active_users"] > 0

    def test_trend_is_increasing_for_demo_data(self):
        trend = _build_usage_trend(_WEEKLY_FEATURE_USAGE)
        totals = [e["total_active_users"] for e in trend]
        assert totals == sorted(totals)


# ===========================================================================
# 12. Helper — _compute_sprint_rates
# ===========================================================================


class TestComputeSprintRates:
    def test_returns_dict(self):
        result = _compute_sprint_rates(_SPRINTS)
        assert isinstance(result, dict)

    def test_total_sprints_correct(self):
        result = _compute_sprint_rates(_SPRINTS)
        assert result["total_sprints"] == 6

    def test_on_time_rate_pct_in_range(self):
        result = _compute_sprint_rates(_SPRINTS)
        assert 0.0 <= result["on_time_rate_pct"] <= 100.0

    def test_avg_dq_improvement_positive(self):
        result = _compute_sprint_rates(_SPRINTS)
        assert result["avg_dq_improvement"] > 0

    def test_avg_nps_in_range(self):
        result = _compute_sprint_rates(_SPRINTS)
        assert 1.0 <= result["avg_nps"] <= 10.0

    def test_zatca_compliance_rate_pct_in_range(self):
        result = _compute_sprint_rates(_SPRINTS)
        assert 0.0 <= result["zatca_compliance_rate_pct"] <= 100.0

    def test_empty_sprints_returns_zeros(self):
        result = _compute_sprint_rates([])
        assert result["total_sprints"] == 0
        assert result["on_time_rate_pct"] == 0.0
        assert result["avg_nps"] == 0.0

    def test_all_on_time_gives_100_pct(self):
        sprints = [
            {"on_time": True, "zatca_compliance_achieved": True, "dq_score_improvement": 10, "nps_score": 8}
            for _ in range(3)
        ]
        result = _compute_sprint_rates(sprints)
        assert result["on_time_rate_pct"] == 100.0


# ===========================================================================
# 13. Helper — _build_funnel_with_rates
# ===========================================================================


class TestBuildFunnelWithRates:
    def test_returns_list(self):
        result = _build_funnel_with_rates(_FUNNEL_STAGES)
        assert isinstance(result, list)

    def test_length_matches_input(self):
        result = _build_funnel_with_rates(_FUNNEL_STAGES)
        assert len(result) == len(_FUNNEL_STAGES)

    def test_first_stage_conversion_rate_is_100(self):
        result = _build_funnel_with_rates(_FUNNEL_STAGES)
        assert result[0]["conversion_rate_pct"] == 100.0

    def test_subsequent_rates_in_valid_range(self):
        result = _build_funnel_with_rates(_FUNNEL_STAGES)
        for entry in result[1:]:
            assert 0.0 <= entry["conversion_rate_pct"] <= 100.0

    def test_each_entry_preserves_original_fields(self):
        result = _build_funnel_with_rates(_FUNNEL_STAGES)
        for i, entry in enumerate(result):
            assert entry["count"] == _FUNNEL_STAGES[i]["count"]

    def test_empty_input_returns_empty_list(self):
        assert _build_funnel_with_rates([]) == []


# ===========================================================================
# 14. Helper — _compute_overall_conversion_pct
# ===========================================================================


class TestComputeOverallConversionPct:
    def test_returns_float(self):
        result = _compute_overall_conversion_pct(_FUNNEL_STAGES)
        assert isinstance(result, float)

    def test_in_valid_range(self):
        result = _compute_overall_conversion_pct(_FUNNEL_STAGES)
        assert 0.0 <= result <= 100.0

    def test_empty_input_returns_zero(self):
        assert _compute_overall_conversion_pct([]) == 0.0

    def test_zero_first_count_returns_zero(self):
        stages = [{"count": 0}, {"count": 5}]
        assert _compute_overall_conversion_pct(stages) == 0.0

    def test_100_pct_when_all_equal(self):
        stages = [{"count": 10}, {"count": 10}]
        assert _compute_overall_conversion_pct(stages) == 100.0


# ===========================================================================
# 15. Helper — _build_key_metrics
# ===========================================================================


class TestBuildKeyMetrics:
    def test_returns_dict(self):
        result = _build_key_metrics()
        assert isinstance(result, dict)

    def test_has_8_keys(self):
        result = _build_key_metrics()
        assert len(result) == 8

    def test_total_active_clients_matches_sector_sum(self):
        result = _build_key_metrics()
        expected = sum(s["client_count"] for s in _SECTORS)
        assert result["total_active_clients"] == expected

    def test_mrr_sar_estimate_matches_sector_sum(self):
        result = _build_key_metrics()
        expected = sum(s["mrr_sar_estimate"] for s in _SECTORS)
        assert result["mrr_sar_estimate"] == expected

    def test_sprints_delivered_matches_sprint_count(self):
        result = _build_key_metrics()
        assert result["sprints_delivered"] == len(_SPRINTS)

    def test_avg_nps_score_in_range(self):
        result = _build_key_metrics()
        assert 1.0 <= result["avg_nps_score"] <= 10.0

    def test_funnel_overall_conversion_in_range(self):
        result = _build_key_metrics()
        assert 0.0 <= result["funnel_overall_conversion_pct"] <= 100.0

    def test_content_impressions_estimate_positive(self):
        result = _build_key_metrics()
        assert result["content_impressions_estimate"] > 0
