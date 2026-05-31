"""Comprehensive tests for api/routers/growth_intelligence.py.

Covers all five endpoints, bilingual response fields, governance_decision,
and GrowthSimulationInput validation.
"""

from __future__ import annotations

import os
import sys
import types

# ---------------------------------------------------------------------------
# Stub out api.security.api_key before the router is imported so that the
# admin-key dependency is a no-op during tests.
# ---------------------------------------------------------------------------
os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")
_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None  # type: ignore[attr-defined]
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.growth_intelligence import router, GrowthSimulationInput  # noqa: E402

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_REQUIRED_GOV = "ALLOW_WITH_REVIEW"


def _get(path: str, **params):
    return client.get(path, params=params)


def _post(path: str, json: dict):
    return client.post(path, json=json)


# ---------------------------------------------------------------------------
# TestSignalsEndpoint
# ---------------------------------------------------------------------------


class TestSignalsEndpoint:
    def test_signals_returns_200(self):
        r = _get("/api/v1/growth-intelligence/signals")
        assert r.status_code == 200

    def test_signals_body_has_signals_key(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        assert "signals" in body

    def test_signals_list_is_non_empty(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        assert len(body["signals"]) > 0

    def test_signals_governance_decision_present(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        assert "governance_decision" in body

    def test_signals_governance_decision_value(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        assert body["governance_decision"] == _REQUIRED_GOV

    def test_signals_each_item_has_title_en(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        for sig in body["signals"]:
            assert "title_en" in sig, f"missing title_en in {sig}"

    def test_signals_each_item_has_title_ar(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        for sig in body["signals"]:
            assert "title_ar" in sig, f"missing title_ar in {sig}"

    def test_signals_each_item_has_signal_id(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        for sig in body["signals"]:
            assert "signal_id" in sig

    def test_signals_each_item_has_urgency(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        for sig in body["signals"]:
            assert sig.get("urgency") in {"HIGH", "MEDIUM", "LOW"}

    def test_signals_label_has_ar_key(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        assert "ar" in body["label"]

    def test_signals_label_has_en_key(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        assert "en" in body["label"]

    def test_signals_filter_by_urgency_high(self):
        body = _get("/api/v1/growth-intelligence/signals", urgency="HIGH").json()
        for sig in body["signals"]:
            assert sig["urgency"] == "HIGH"

    def test_signals_filter_by_urgency_medium(self):
        body = _get("/api/v1/growth-intelligence/signals", urgency="MEDIUM").json()
        for sig in body["signals"]:
            assert sig["urgency"] == "MEDIUM"

    def test_signals_filter_by_sector(self):
        body = _get(
            "/api/v1/growth-intelligence/signals", sector="healthcare"
        ).json()
        for sig in body["signals"]:
            assert "healthcare" in sig["sectors_affected"]

    def test_signals_total_matches_list_length(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        assert body["total"] == len(body["signals"])

    def test_signals_source_note_en_present(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        assert "source_note_en" in body

    def test_signals_source_note_en_mentions_not_scraping(self):
        body = _get("/api/v1/growth-intelligence/signals").json()
        note = body["source_note_en"].lower()
        assert "scraping" not in note or "not" in note


# ---------------------------------------------------------------------------
# TestMarketMapEndpoint
# ---------------------------------------------------------------------------


class TestMarketMapEndpoint:
    def test_market_map_returns_200(self):
        r = _get("/api/v1/growth-intelligence/market-map")
        assert r.status_code == 200

    def test_market_map_has_segments_key(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        assert "segments" in body

    def test_market_map_governance_decision_present(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        assert "governance_decision" in body

    def test_market_map_governance_decision_value(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        assert body["governance_decision"] == _REQUIRED_GOV

    def test_market_map_segments_non_empty(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        assert len(body["segments"]) > 0

    def test_market_map_each_segment_has_sector(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        for seg in body["segments"]:
            assert "sector" in seg

    def test_market_map_each_segment_has_sector_ar(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        for seg in body["segments"]:
            assert "sector_ar" in seg

    def test_market_map_each_segment_has_city_ar(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        for seg in body["segments"]:
            assert "city_ar" in seg

    def test_market_map_opportunity_scores_in_range(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        for seg in body["segments"]:
            score = seg["opportunity_score"]
            assert 0 <= score <= 100, f"score {score} out of range"

    def test_market_map_min_score_filter(self):
        body = _get("/api/v1/growth-intelligence/market-map", min_score=80).json()
        for seg in body["segments"]:
            assert seg["opportunity_score"] >= 80

    def test_market_map_min_score_out_of_range_returns_400(self):
        r = _get("/api/v1/growth-intelligence/market-map", min_score=101)
        assert r.status_code == 400

    def test_market_map_sorted_descending_by_score(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        scores = [s["opportunity_score"] for s in body["segments"]]
        assert scores == sorted(scores, reverse=True)

    def test_market_map_total_segments_matches_list(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        assert body["total_segments"] == len(body["segments"])

    def test_market_map_total_addressable_sar_positive(self):
        body = _get("/api/v1/growth-intelligence/market-map").json()
        assert body["total_addressable_sar"] > 0


# ---------------------------------------------------------------------------
# TestWeeklyFocusEndpoint
# ---------------------------------------------------------------------------


class TestWeeklyFocusEndpoint:
    def test_weekly_focus_returns_200(self):
        r = _get("/api/v1/growth-intelligence/weekly-focus")
        assert r.status_code == 200

    def test_weekly_focus_has_focus_areas(self):
        body = _get("/api/v1/growth-intelligence/weekly-focus").json()
        assert "focus_areas" in body

    def test_weekly_focus_focus_areas_non_empty(self):
        body = _get("/api/v1/growth-intelligence/weekly-focus").json()
        assert len(body["focus_areas"]) > 0

    def test_weekly_focus_governance_decision_present(self):
        body = _get("/api/v1/growth-intelligence/weekly-focus").json()
        assert "governance_decision" in body

    def test_weekly_focus_governance_decision_value(self):
        body = _get("/api/v1/growth-intelligence/weekly-focus").json()
        assert body["governance_decision"] == _REQUIRED_GOV

    def test_weekly_focus_each_item_has_focus_area_en(self):
        body = _get("/api/v1/growth-intelligence/weekly-focus").json()
        for item in body["focus_areas"]:
            assert "focus_area_en" in item

    def test_weekly_focus_each_item_has_focus_area_ar(self):
        body = _get("/api/v1/growth-intelligence/weekly-focus").json()
        for item in body["focus_areas"]:
            assert "focus_area_ar" in item

    def test_weekly_focus_each_item_has_priority(self):
        body = _get("/api/v1/growth-intelligence/weekly-focus").json()
        for item in body["focus_areas"]:
            assert "priority" in item

    def test_weekly_focus_governance_note_en_present(self):
        body = _get("/api/v1/growth-intelligence/weekly-focus").json()
        assert "governance_note_en" in body

    def test_weekly_focus_total_effort_positive(self):
        body = _get("/api/v1/growth-intelligence/weekly-focus").json()
        assert body["total_effort_hours"] > 0


# ---------------------------------------------------------------------------
# TestSimulateGrowthEndpoint
# ---------------------------------------------------------------------------


class TestSimulateGrowthEndpoint:
    _DEFAULT_BODY = {
        "current_mrr": 10000.0,
        "new_clients_per_month": 2,
        "avg_deal_sar": 3000.0,
        "churn_rate": 0.05,
    }

    def test_simulate_returns_200(self):
        r = _post("/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY)
        assert r.status_code == 200

    def test_simulate_returns_12_month_projection(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY
        ).json()
        assert len(body["projection"]) == 12

    def test_simulate_governance_decision_present(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY
        ).json()
        assert "governance_decision" in body

    def test_simulate_governance_decision_value(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY
        ).json()
        assert body["governance_decision"] == _REQUIRED_GOV

    def test_simulate_positive_inputs_month12_mrr_ge_month1(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth",
            {
                "current_mrr": 10000.0,
                "new_clients_per_month": 5,
                "avg_deal_sar": 3000.0,
                "churn_rate": 0.01,
            },
        ).json()
        proj = body["projection"]
        assert proj[11]["ending_mrr"] >= proj[0]["ending_mrr"]

    def test_simulate_zero_churn_mrr_grows_monotonically(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth",
            {
                "current_mrr": 5000.0,
                "new_clients_per_month": 2,
                "avg_deal_sar": 2000.0,
                "churn_rate": 0.0,
            },
        ).json()
        proj = body["projection"]
        for i in range(1, len(proj)):
            assert proj[i]["ending_mrr"] >= proj[i - 1]["ending_mrr"]

    def test_simulate_high_churn_may_reduce_mrr(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth",
            {
                "current_mrr": 100000.0,
                "new_clients_per_month": 1,
                "avg_deal_sar": 500.0,
                "churn_rate": 0.99,
            },
        ).json()
        proj = body["projection"]
        # With near-total churn, ending MRR in month 12 must be less than starting MRR
        assert proj[11]["ending_mrr"] < 100000.0

    def test_simulate_projection_has_month_field(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY
        ).json()
        for item in body["projection"]:
            assert "month" in item

    def test_simulate_projection_has_ending_mrr(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY
        ).json()
        for item in body["projection"]:
            assert "ending_mrr" in item

    def test_simulate_projection_has_arr(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY
        ).json()
        for item in body["projection"]:
            assert "arr" in item

    def test_simulate_summary_present(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY
        ).json()
        assert "summary" in body

    def test_simulate_summary_has_ending_mrr(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY
        ).json()
        assert "ending_mrr" in body["summary"]

    def test_simulate_invalid_churn_rate_above_1_returns_422(self):
        r = _post(
            "/api/v1/growth-intelligence/simulate-growth",
            {
                "current_mrr": 10000.0,
                "new_clients_per_month": 2,
                "avg_deal_sar": 3000.0,
                "churn_rate": 1.5,
            },
        )
        assert r.status_code == 422

    def test_simulate_note_en_present(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY
        ).json()
        assert "note_en" in body

    def test_simulate_month_numbers_are_sequential(self):
        body = _post(
            "/api/v1/growth-intelligence/simulate-growth", self._DEFAULT_BODY
        ).json()
        months = [item["month"] for item in body["projection"]]
        assert months == list(range(1, 13))


# ---------------------------------------------------------------------------
# TestBenchmarkEndpoint
# ---------------------------------------------------------------------------


class TestBenchmarkEndpoint:
    def test_benchmark_returns_200(self):
        r = _get("/api/v1/growth-intelligence/benchmark")
        assert r.status_code == 200

    def test_benchmark_governance_decision_present(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        assert "governance_decision" in body

    def test_benchmark_governance_decision_value(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        assert body["governance_decision"] == _REQUIRED_GOV

    def test_benchmark_has_benchmarks_key(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        assert "benchmarks" in body

    def test_benchmark_benchmarks_non_empty(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        assert len(body["benchmarks"]) > 0

    def test_benchmark_each_metric_has_dealix_value(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        for key, metric in body["benchmarks"].items():
            assert "dealix" in metric, f"missing dealix in {key}"

    def test_benchmark_each_metric_has_saudi_saas_median(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        for key, metric in body["benchmarks"].items():
            assert "saudi_saas_median" in metric, f"missing saudi_saas_median in {key}"

    def test_benchmark_each_metric_has_bilingual_label(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        for key, metric in body["benchmarks"].items():
            assert "label" in metric, f"missing label in {key}"
            assert "ar" in metric["label"], f"missing ar in label for {key}"
            assert "en" in metric["label"], f"missing en in label for {key}"

    def test_benchmark_summary_present(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        assert "summary" in body

    def test_benchmark_summary_has_above_median_count(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        assert "above_median_count" in body["summary"]

    def test_benchmark_source_note_en_present(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        assert "source_note_en" in body

    def test_benchmark_source_note_ar_present(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        assert "source_note_ar" in body

    def test_benchmark_summary_total_metrics_positive(self):
        body = _get("/api/v1/growth-intelligence/benchmark").json()
        assert body["summary"]["total_metrics"] > 0
