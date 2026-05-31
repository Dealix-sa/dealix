"""Tests for api/routers/pipeline_ops.py.

Covers all six endpoints: overview, deals, velocity, advance, forecast,
lost-analysis; plus the pure helper functions.
"""

from __future__ import annotations

import os
import sys
import types

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")
_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None  # type: ignore[attr-defined]
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.pipeline_ops import (  # noqa: E402
    PIPELINE_STAGES,
    _compute_forecast,
    _compute_weighted_value,
    _get_next_stage,
    _pipeline,
    _stage_counts,
    router,
)

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})

_GOV = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"


# ---------------------------------------------------------------------------
# TestOverviewEndpoint
# ---------------------------------------------------------------------------


class TestOverviewEndpoint:
    def test_overview_returns_200(self):
        r = client.get("/api/v1/pipeline/overview")
        assert r.status_code == 200

    def test_overview_governance_decision(self):
        body = client.get("/api/v1/pipeline/overview").json()
        assert body["governance_decision"] == _GOV

    def test_overview_has_total_deals(self):
        body = client.get("/api/v1/pipeline/overview").json()
        assert "total_deals" in body

    def test_overview_total_deals_positive(self):
        body = client.get("/api/v1/pipeline/overview").json()
        assert body["total_deals"] > 0

    def test_overview_has_total_pipeline_value(self):
        body = client.get("/api/v1/pipeline/overview").json()
        assert "total_pipeline_value_sar" in body

    def test_overview_total_pipeline_value_positive(self):
        body = client.get("/api/v1/pipeline/overview").json()
        assert body["total_pipeline_value_sar"] > 0

    def test_overview_has_weighted_pipeline_value(self):
        body = client.get("/api/v1/pipeline/overview").json()
        assert "weighted_pipeline_value_sar" in body

    def test_overview_weighted_le_total(self):
        body = client.get("/api/v1/pipeline/overview").json()
        assert body["weighted_pipeline_value_sar"] <= body["total_pipeline_value_sar"]

    def test_overview_has_stages_key(self):
        body = client.get("/api/v1/pipeline/overview").json()
        assert "stages" in body

    def test_overview_stages_contain_all_pipeline_stages(self):
        body = client.get("/api/v1/pipeline/overview").json()
        for stage in PIPELINE_STAGES:
            assert stage in body["stages"]

    def test_overview_each_stage_has_label(self):
        body = client.get("/api/v1/pipeline/overview").json()
        for stage_key, stage_data in body["stages"].items():
            assert "label" in stage_data

    def test_overview_currency_is_sar(self):
        body = client.get("/api/v1/pipeline/overview").json()
        assert body["currency"] == "SAR"


# ---------------------------------------------------------------------------
# TestDealsEndpoint
# ---------------------------------------------------------------------------


class TestDealsEndpoint:
    def test_deals_returns_200(self):
        r = client.get("/api/v1/pipeline/deals")
        assert r.status_code == 200

    def test_deals_governance_decision(self):
        body = client.get("/api/v1/pipeline/deals").json()
        assert body["governance_decision"] == _GOV

    def test_deals_has_deals_key(self):
        body = client.get("/api/v1/pipeline/deals").json()
        assert "deals" in body

    def test_deals_returns_12_deals(self):
        body = client.get("/api/v1/pipeline/deals").json()
        assert body["total"] == 12

    def test_deals_sorted_by_value_descending(self):
        body = client.get("/api/v1/pipeline/deals").json()
        values = [d["value_sar"] for d in body["deals"]]
        assert values == sorted(values, reverse=True)

    def test_deals_each_has_company_name_en(self):
        body = client.get("/api/v1/pipeline/deals").json()
        for d in body["deals"]:
            assert "company_name_en" in d

    def test_deals_each_has_company_name_ar(self):
        body = client.get("/api/v1/pipeline/deals").json()
        for d in body["deals"]:
            assert "company_name_ar" in d

    def test_deals_each_has_stage_label(self):
        body = client.get("/api/v1/pipeline/deals").json()
        for d in body["deals"]:
            assert "stage_label" in d

    def test_deals_each_has_weighted_value(self):
        body = client.get("/api/v1/pipeline/deals").json()
        for d in body["deals"]:
            assert "weighted_value_sar" in d

    def test_deals_filter_by_stage_returns_subset(self):
        body = client.get("/api/v1/pipeline/deals", params={"stage": "lead"}).json()
        for d in body["deals"]:
            assert d["stage"] == "lead"

    def test_deals_filter_by_stage_count_matches_total(self):
        body = client.get("/api/v1/pipeline/deals", params={"stage": "lead"}).json()
        assert body["total"] == len(body["deals"])

    def test_deals_invalid_stage_returns_400(self):
        r = client.get("/api/v1/pipeline/deals", params={"stage": "nonexistent_stage"})
        assert r.status_code == 400

    def test_deals_currency_is_sar(self):
        body = client.get("/api/v1/pipeline/deals").json()
        assert body["currency"] == "SAR"


# ---------------------------------------------------------------------------
# TestVelocityEndpoint
# ---------------------------------------------------------------------------


class TestVelocityEndpoint:
    def test_velocity_returns_200(self):
        r = client.get("/api/v1/pipeline/velocity")
        assert r.status_code == 200

    def test_velocity_governance_decision(self):
        body = client.get("/api/v1/pipeline/velocity").json()
        assert body["governance_decision"] == _GOV

    def test_velocity_has_stage_velocity_key(self):
        body = client.get("/api/v1/pipeline/velocity").json()
        assert "stage_velocity" in body

    def test_velocity_has_overall_win_rate(self):
        body = client.get("/api/v1/pipeline/velocity").json()
        assert "overall_win_rate" in body

    def test_velocity_win_rate_in_valid_range(self):
        body = client.get("/api/v1/pipeline/velocity").json()
        assert 0.0 <= body["overall_win_rate"] <= 1.0

    def test_velocity_has_bottleneck_stage(self):
        body = client.get("/api/v1/pipeline/velocity").json()
        assert "bottleneck_stage" in body

    def test_velocity_bottleneck_is_valid_stage(self):
        body = client.get("/api/v1/pipeline/velocity").json()
        stage = body["bottleneck_stage"]
        if stage is not None:
            assert stage in PIPELINE_STAGES

    def test_velocity_each_stage_has_avg_days(self):
        body = client.get("/api/v1/pipeline/velocity").json()
        for stage_key, stage_data in body["stage_velocity"].items():
            assert "avg_days" in stage_data

    def test_velocity_each_stage_has_deal_count(self):
        body = client.get("/api/v1/pipeline/velocity").json()
        for stage_key, stage_data in body["stage_velocity"].items():
            assert "deal_count" in stage_data

    def test_velocity_bottleneck_note_en_present(self):
        body = client.get("/api/v1/pipeline/velocity").json()
        assert "bottleneck_note_en" in body


# ---------------------------------------------------------------------------
# TestAdvanceEndpoint
# ---------------------------------------------------------------------------


class TestAdvanceEndpoint:
    def test_advance_returns_200(self):
        r = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-007", "new_stage": "qualified", "reason": "warm intro confirmed"},
        )
        assert r.status_code == 200

    def test_advance_governance_is_approval_first(self):
        # Use a fresh lead deal that hasn't been advanced yet
        body = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-008", "new_stage": "qualified", "reason": "test"},
        ).json()
        assert body["governance_decision"] == _GOV_APPROVAL

    def test_advance_returns_updated_deal(self):
        body = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-006", "new_stage": "diagnostic_sent", "reason": "qualified"},
        ).json()
        assert "deal" in body

    def test_advance_deal_stage_updated(self):
        # DL-004 starts at diagnostic_sent; advance to sprint_proposed
        body = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-004", "new_stage": "sprint_proposed", "reason": "diagnostic complete"},
        ).json()
        assert body["deal"]["stage"] == "sprint_proposed"

    def test_advance_has_approval_note_en(self):
        body = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-002", "new_stage": "sprint_active", "reason": "signed"},
        ).json()
        assert "approval_note_en" in body

    def test_advance_has_approval_note_ar(self):
        body = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-011", "new_stage": "sprint_proposed", "reason": "test"},
        ).json()
        assert "approval_note_ar" in body

    def test_advance_has_previous_stage(self):
        body = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-001", "new_stage": "diagnostic_sent", "reason": "test"},
        ).json()
        assert "previous_stage" in body

    def test_advance_invalid_deal_id_returns_404(self):
        r = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-NONEXISTENT", "new_stage": "qualified", "reason": "x"},
        )
        assert r.status_code == 404

    def test_advance_invalid_stage_returns_400(self):
        r = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-007", "new_stage": "not_a_stage", "reason": "x"},
        )
        assert r.status_code == 400

    def test_advance_missing_reason_returns_422(self):
        r = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-007", "new_stage": "qualified"},
        )
        assert r.status_code == 422

    def test_advance_to_closed_won_sets_probability_one(self):
        body = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-003", "new_stage": "closed_won", "reason": "sprint delivered"},
        ).json()
        assert body["deal"]["probability"] == 1.0

    def test_advance_to_closed_lost_sets_probability_zero(self):
        body = client.post(
            "/api/v1/pipeline/advance",
            json={"deal_id": "DL-005", "new_stage": "closed_lost", "reason": "no budget"},
        ).json()
        assert body["deal"]["probability"] == 0.0


# ---------------------------------------------------------------------------
# TestForecastEndpoint
# ---------------------------------------------------------------------------


class TestForecastEndpoint:
    def test_forecast_returns_200(self):
        r = client.get("/api/v1/pipeline/forecast")
        assert r.status_code == 200

    def test_forecast_governance_decision(self):
        body = client.get("/api/v1/pipeline/forecast").json()
        assert body["governance_decision"] == _GOV

    def test_forecast_has_forecast_key(self):
        body = client.get("/api/v1/pipeline/forecast").json()
        assert "forecast" in body

    def test_forecast_has_30_day(self):
        body = client.get("/api/v1/pipeline/forecast").json()
        assert "30_day_sar" in body["forecast"]

    def test_forecast_has_60_day(self):
        body = client.get("/api/v1/pipeline/forecast").json()
        assert "60_day_sar" in body["forecast"]

    def test_forecast_has_90_day(self):
        body = client.get("/api/v1/pipeline/forecast").json()
        assert "90_day_sar" in body["forecast"]

    def test_forecast_30_le_60_le_90(self):
        body = client.get("/api/v1/pipeline/forecast").json()
        f = body["forecast"]
        assert f["30_day_sar"] <= f["60_day_sar"] <= f["90_day_sar"]

    def test_forecast_has_disclaimer_en(self):
        body = client.get("/api/v1/pipeline/forecast").json()
        assert "disclaimer_en" in body

    def test_forecast_has_methodology_en(self):
        body = client.get("/api/v1/pipeline/forecast").json()
        assert "methodology_en" in body

    def test_forecast_currency_is_sar(self):
        body = client.get("/api/v1/pipeline/forecast").json()
        assert body["currency"] == "SAR"


# ---------------------------------------------------------------------------
# TestLostAnalysisEndpoint
# ---------------------------------------------------------------------------


class TestLostAnalysisEndpoint:
    def test_lost_analysis_returns_200(self):
        r = client.get("/api/v1/pipeline/lost-analysis")
        assert r.status_code == 200

    def test_lost_analysis_governance_decision(self):
        body = client.get("/api/v1/pipeline/lost-analysis").json()
        assert body["governance_decision"] == _GOV

    def test_lost_analysis_has_total_lost_deals(self):
        body = client.get("/api/v1/pipeline/lost-analysis").json()
        assert "total_lost_deals" in body

    def test_lost_analysis_has_reason_breakdown(self):
        body = client.get("/api/v1/pipeline/lost-analysis").json()
        assert "reason_breakdown" in body

    def test_lost_analysis_has_sector_patterns(self):
        body = client.get("/api/v1/pipeline/lost-analysis").json()
        assert "sector_patterns" in body

    def test_lost_analysis_each_reason_has_bilingual_label(self):
        body = client.get("/api/v1/pipeline/lost-analysis").json()
        for entry in body["reason_breakdown"]:
            assert "label" in entry
            assert "ar" in entry["label"]
            assert "en" in entry["label"]

    def test_lost_analysis_reason_pct_adds_to_100(self):
        body = client.get("/api/v1/pipeline/lost-analysis").json()
        reasons = body["reason_breakdown"]
        if reasons:
            total_pct = sum(r["pct"] for r in reasons)
            assert abs(total_pct - 100.0) < 1.0

    def test_lost_analysis_total_lost_value_positive(self):
        body = client.get("/api/v1/pipeline/lost-analysis").json()
        assert body["total_lost_value_sar"] > 0

    def test_lost_analysis_action_note_en_present(self):
        body = client.get("/api/v1/pipeline/lost-analysis").json()
        assert "action_note_en" in body

    def test_lost_analysis_currency_is_sar(self):
        body = client.get("/api/v1/pipeline/lost-analysis").json()
        assert body["currency"] == "SAR"


# ---------------------------------------------------------------------------
# Pure-function unit tests
# ---------------------------------------------------------------------------


class TestPureFunctions:
    def test_compute_weighted_value_empty(self):
        result = _compute_weighted_value([])
        assert result == 0.0

    def test_compute_weighted_value_single(self):
        deal = {"value_sar": 1000.0, "probability": 0.5}
        result = _compute_weighted_value([deal])
        assert result == 500.0

    def test_compute_forecast_30_le_90(self):
        f30 = _compute_forecast(30)
        f90 = _compute_forecast(90)
        assert f30 <= f90

    def test_compute_forecast_non_negative(self):
        result = _compute_forecast(90)
        assert result >= 0.0

    def test_stage_counts_has_all_stages(self):
        counts = _stage_counts()
        for stage in PIPELINE_STAGES:
            assert stage in counts

    def test_stage_counts_totals_to_pipeline_length(self):
        counts = _stage_counts()
        assert sum(counts.values()) == len(_pipeline)

    def test_get_next_stage_lead_to_qualified(self):
        assert _get_next_stage("lead") == "qualified"

    def test_get_next_stage_from_terminal_returns_none(self):
        assert _get_next_stage("closed_won") is None
        assert _get_next_stage("closed_lost") is None

    def test_pipeline_has_12_deals(self):
        assert len(_pipeline) == 12
