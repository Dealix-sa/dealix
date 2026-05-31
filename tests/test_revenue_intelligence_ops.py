"""Tests for revenue_intelligence_ops API router.

Covers: demo data integrity, MRR breakdown, leakage analysis, growth forecast,
cohort analysis, revenue alert creation, NRR analysis, governance decision
presence, helper functions, validation errors, and bilingual labels.
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

from api.routers.revenue_intelligence_ops import (  # noqa: E402
    _ALERTS,
    _COHORTS,
    _FORECAST_DISCLAIMER,
    _LEAKAGE_SIGNALS,
    _MRR_HISTORY,
    _TOTAL_LEAKAGE_SAR,
    _VALID_ALERT_TYPES,
    _VALID_URGENCY,
    _compute_growth_forecast,
    _compute_nrr,
    _now_iso,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clear_alerts():
    """Clear the in-memory alert store after each test."""
    yield
    _ALERTS.clear()


# ===========================================================================
# Unit tests — _now_iso
# ===========================================================================


class TestNowIso:
    def test_returns_string(self):
        assert isinstance(_now_iso(), str)

    def test_contains_t_separator(self):
        assert "T" in _now_iso()

    def test_ends_with_utc_offset(self):
        result = _now_iso()
        assert "+00:00" in result or result.endswith("Z")

    def test_is_non_empty(self):
        assert len(_now_iso()) > 0


# ===========================================================================
# Unit tests — demo data integrity
# ===========================================================================


class TestDemoDataIntegrity:
    def test_mrr_history_has_6_months(self):
        assert len(_MRR_HISTORY) == 6

    def test_mrr_history_months_are_correct(self):
        months = [m["month"] for m in _MRR_HISTORY]
        assert months[0] == "Jan 2026"
        assert months[-1] == "Jun 2026"

    def test_mrr_history_each_entry_has_total_mrr(self):
        for entry in _MRR_HISTORY:
            assert "total_mrr" in entry
            assert entry["total_mrr"] > 0

    def test_mrr_history_each_entry_has_new_mrr(self):
        for entry in _MRR_HISTORY:
            assert "new_mrr" in entry

    def test_mrr_history_each_entry_has_expansion_mrr(self):
        for entry in _MRR_HISTORY:
            assert "expansion_mrr" in entry

    def test_mrr_history_each_entry_has_churned_mrr(self):
        for entry in _MRR_HISTORY:
            assert "churned_mrr" in entry

    def test_mrr_history_each_entry_has_contracted_mrr(self):
        for entry in _MRR_HISTORY:
            assert "contracted_mrr" in entry

    def test_mrr_history_each_entry_has_arabic_month(self):
        for entry in _MRR_HISTORY:
            assert "month_ar" in entry
            assert len(entry["month_ar"]) > 0

    def test_jan_mrr_is_35000(self):
        assert _MRR_HISTORY[0]["total_mrr"] == 35_000

    def test_jun_mrr_is_68000(self):
        assert _MRR_HISTORY[-1]["total_mrr"] == 68_000

    def test_mrr_history_is_monotonically_increasing(self):
        mrrs = [m["total_mrr"] for m in _MRR_HISTORY]
        for i in range(1, len(mrrs)):
            assert mrrs[i] > mrrs[i - 1]

    def test_leakage_signals_count_is_5(self):
        assert len(_LEAKAGE_SIGNALS) == 5

    def test_leakage_signals_have_ids(self):
        for signal in _LEAKAGE_SIGNALS:
            assert "id" in signal
            assert signal["id"].startswith("LEAK-")

    def test_leakage_signals_have_amounts(self):
        for signal in _LEAKAGE_SIGNALS:
            assert "estimated_amount_sar" in signal
            assert signal["estimated_amount_sar"] > 0

    def test_leakage_signals_have_arabic_descriptions(self):
        for signal in _LEAKAGE_SIGNALS:
            assert "description_ar" in signal
            assert len(signal["description_ar"]) > 0

    def test_leakage_signals_have_english_descriptions(self):
        for signal in _LEAKAGE_SIGNALS:
            assert "description_en" in signal

    def test_leakage_signals_have_action_ar(self):
        for signal in _LEAKAGE_SIGNALS:
            assert "action_ar" in signal

    def test_leakage_signals_have_action_en(self):
        for signal in _LEAKAGE_SIGNALS:
            assert "action_en" in signal

    def test_total_leakage_equals_sum_of_signals(self):
        expected = sum(s["estimated_amount_sar"] for s in _LEAKAGE_SIGNALS)
        assert _TOTAL_LEAKAGE_SAR == expected

    def test_total_leakage_is_19999(self):
        assert _TOTAL_LEAKAGE_SAR == 19_999

    def test_cohorts_count_is_6(self):
        assert len(_COHORTS) == 6

    def test_cohorts_have_cohort_month(self):
        for cohort in _COHORTS:
            assert "cohort_month" in cohort

    def test_cohorts_have_initial_clients(self):
        for cohort in _COHORTS:
            assert "initial_clients" in cohort
            assert cohort["initial_clients"] > 0

    def test_cohorts_have_avg_ltv_estimate(self):
        for cohort in _COHORTS:
            assert "avg_ltv_sar_estimate" in cohort
            assert cohort["avg_ltv_sar_estimate"] > 0

    def test_forecast_disclaimer_is_bilingual(self):
        assert "/" in _FORECAST_DISCLAIMER
        assert "estimates" in _FORECAST_DISCLAIMER
        assert "ضمانات" in _FORECAST_DISCLAIMER

    def test_valid_alert_types_count(self):
        assert len(_VALID_ALERT_TYPES) == 5

    def test_valid_urgency_levels(self):
        assert _VALID_URGENCY == {"high", "medium", "low"}


# ===========================================================================
# Unit tests — _compute_nrr
# ===========================================================================


class TestComputeNrr:
    def test_returns_dict(self):
        result = _compute_nrr(_MRR_HISTORY)
        assert isinstance(result, dict)

    def test_nrr_pct_present(self):
        result = _compute_nrr(_MRR_HISTORY)
        assert "nrr_pct" in result

    def test_grr_pct_present(self):
        result = _compute_nrr(_MRR_HISTORY)
        assert "gross_revenue_retention_pct" in result

    def test_expansion_pct_present(self):
        result = _compute_nrr(_MRR_HISTORY)
        assert "expansion_revenue_pct" in result

    def test_churn_rate_pct_present(self):
        result = _compute_nrr(_MRR_HISTORY)
        assert "churn_rate_pct" in result

    def test_nrr_is_float(self):
        result = _compute_nrr(_MRR_HISTORY)
        assert isinstance(result["nrr_pct"], float)

    def test_nrr_positive_for_demo_data(self):
        result = _compute_nrr(_MRR_HISTORY)
        assert result["nrr_pct"] > 0

    def test_interpretation_ar_present(self):
        result = _compute_nrr(_MRR_HISTORY)
        assert "interpretation_ar" in result

    def test_interpretation_en_present(self):
        result = _compute_nrr(_MRR_HISTORY)
        assert "interpretation_en" in result

    def test_empty_history_returns_zeros(self):
        result = _compute_nrr([])
        assert result["nrr_pct"] == 0.0

    def test_single_month_returns_zeros(self):
        result = _compute_nrr([_MRR_HISTORY[0]])
        assert result["nrr_pct"] == 0.0

    def test_zero_starting_mrr_returns_zeros(self):
        history = [{"total_mrr": 0, "expansion_mrr": 0, "churned_mrr": 0, "contracted_mrr": 0}]
        result = _compute_nrr(history)
        assert result["nrr_pct"] == 0.0

    def test_nrr_computed_from_demo_data(self):
        # NRR is computed from Jan base; total churn across 5 months exceeds expansion,
        # reflecting the cost of growth — the value is deterministic and positive.
        result = _compute_nrr(_MRR_HISTORY)
        assert result["nrr_pct"] > 0.0
        assert result["nrr_pct"] < 200.0


# ===========================================================================
# Unit tests — _compute_growth_forecast
# ===========================================================================


class TestComputeGrowthForecast:
    def test_returns_dict(self):
        result = _compute_growth_forecast(_MRR_HISTORY)
        assert isinstance(result, dict)

    def test_forecast_has_3_months(self):
        result = _compute_growth_forecast(_MRR_HISTORY)
        assert len(result["forecast"]) == 3

    def test_trailing_rate_is_float(self):
        result = _compute_growth_forecast(_MRR_HISTORY)
        assert isinstance(result["trailing_3m_growth_rate_pct"], float)

    def test_forecast_months_in_future(self):
        result = _compute_growth_forecast(_MRR_HISTORY)
        months = [f["month"] for f in result["forecast"]]
        assert "Jul 2026" in months

    def test_forecast_has_base_mrr(self):
        result = _compute_growth_forecast(_MRR_HISTORY)
        for entry in result["forecast"]:
            assert "base_mrr" in entry

    def test_forecast_has_optimistic_mrr(self):
        result = _compute_growth_forecast(_MRR_HISTORY)
        for entry in result["forecast"]:
            assert "optimistic_mrr" in entry

    def test_forecast_has_pessimistic_mrr(self):
        result = _compute_growth_forecast(_MRR_HISTORY)
        for entry in result["forecast"]:
            assert "pessimistic_mrr" in entry

    def test_optimistic_above_base(self):
        result = _compute_growth_forecast(_MRR_HISTORY)
        for entry in result["forecast"]:
            assert entry["optimistic_mrr"] >= entry["base_mrr"]

    def test_pessimistic_below_base(self):
        result = _compute_growth_forecast(_MRR_HISTORY)
        for entry in result["forecast"]:
            assert entry["pessimistic_mrr"] <= entry["base_mrr"]

    def test_empty_history_returns_empty_forecast(self):
        result = _compute_growth_forecast([])
        assert result["forecast"] == []

    def test_forecast_has_arabic_month_label(self):
        result = _compute_growth_forecast(_MRR_HISTORY)
        for entry in result["forecast"]:
            assert "month_ar" in entry


# ===========================================================================
# API tests — GET /mrr-breakdown
# ===========================================================================


class TestMrrBreakdown:
    def test_returns_200(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert response.status_code == 200

    def test_has_governance_decision(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert "governance_decision" in response.json()

    def test_governance_is_allow_with_review(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert response.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_total_mrr(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert "total_mrr" in response.json()

    def test_total_mrr_is_68000(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert response.json()["total_mrr"] == 68_000

    def test_arr_run_rate_is_mrr_times_12(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        data = response.json()
        assert data["arr_run_rate"] == data["total_mrr"] * 12

    def test_arr_is_816000(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert response.json()["arr_run_rate"] == 816_000

    def test_has_new_mrr(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert "new_mrr" in response.json()

    def test_has_expansion_mrr(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert "expansion_mrr" in response.json()

    def test_has_churned_mrr(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert "churned_mrr" in response.json()

    def test_has_contracted_mrr(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert "contracted_mrr" in response.json()

    def test_has_net_new_mrr(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert "net_new_mrr" in response.json()

    def test_has_history(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert "history" in response.json()

    def test_history_has_6_entries(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert len(response.json()["history"]) == 6

    def test_has_currency_sar(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert response.json().get("currency") == "SAR"

    def test_has_generated_at(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        assert "generated_at" in response.json()

    def test_has_bilingual_labels(self):
        response = client.get("/api/v1/revenue-intelligence/ops/mrr-breakdown")
        data = response.json()
        assert "label_ar" in data
        assert "label_en" in data


# ===========================================================================
# API tests — GET /leakage-analysis
# ===========================================================================


class TestLeakageAnalysis:
    def test_returns_200(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert response.status_code == 200

    def test_has_governance_decision(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert "governance_decision" in response.json()

    def test_governance_is_allow_with_review(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert response.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_total_leakage_estimate(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert "total_leakage_estimate_sar" in response.json()

    def test_total_leakage_is_positive(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert response.json()["total_leakage_estimate_sar"] > 0

    def test_total_leakage_is_19999(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert response.json()["total_leakage_estimate_sar"] == 19_999

    def test_has_signals(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert "signals" in response.json()

    def test_signals_count_is_5(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert len(response.json()["signals"]) == 5

    def test_has_priority_action_ar(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert "priority_action_ar" in response.json()

    def test_has_priority_action_en(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert "priority_action_en" in response.json()

    def test_each_signal_has_estimated_amount(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        for signal in response.json()["signals"]:
            assert "estimated_amount_sar" in signal
            assert signal["estimated_amount_sar"] > 0

    def test_has_generated_at(self):
        response = client.get("/api/v1/revenue-intelligence/ops/leakage-analysis")
        assert "generated_at" in response.json()


# ===========================================================================
# API tests — GET /growth-forecast
# ===========================================================================


class TestGrowthForecast:
    def test_returns_200(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        assert response.status_code == 200

    def test_has_governance_decision(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        assert "governance_decision" in response.json()

    def test_governance_is_allow_with_review(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        assert response.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_trailing_growth_rate(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        assert "trailing_3m_growth_rate_pct" in response.json()

    def test_has_forecast_list(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        assert "forecast" in response.json()

    def test_forecast_has_3_months(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        assert len(response.json()["forecast"]) == 3

    def test_each_forecast_has_optimistic(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        for entry in response.json()["forecast"]:
            assert "optimistic_mrr" in entry

    def test_each_forecast_has_base(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        for entry in response.json()["forecast"]:
            assert "base_mrr" in entry

    def test_each_forecast_has_pessimistic(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        for entry in response.json()["forecast"]:
            assert "pessimistic_mrr" in entry

    def test_has_disclaimer(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        assert "disclaimer" in response.json()

    def test_disclaimer_is_bilingual(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        disclaimer = response.json()["disclaimer"]
        assert "estimates" in disclaimer
        assert "ضمانات" in disclaimer

    def test_has_generated_at(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        assert "generated_at" in response.json()

    def test_has_currency(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        assert response.json()["currency"] == "SAR"

    def test_each_forecast_has_arabic_month(self):
        response = client.get("/api/v1/revenue-intelligence/ops/growth-forecast")
        for entry in response.json()["forecast"]:
            assert "month_ar" in entry


# ===========================================================================
# API tests — GET /cohort-analysis
# ===========================================================================


class TestCohortAnalysis:
    def test_returns_200(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        assert response.status_code == 200

    def test_has_governance_decision(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        assert "governance_decision" in response.json()

    def test_governance_is_allow_with_review(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        assert response.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_cohorts(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        assert "cohorts" in response.json()

    def test_cohorts_count_is_6(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        assert len(response.json()["cohorts"]) == 6

    def test_each_cohort_has_cohort_month(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        for cohort in response.json()["cohorts"]:
            assert "cohort_month" in cohort

    def test_each_cohort_has_initial_clients(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        for cohort in response.json()["cohorts"]:
            assert "initial_clients" in cohort
            assert cohort["initial_clients"] > 0

    def test_each_cohort_has_retained_at_3m(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        for cohort in response.json()["cohorts"]:
            assert "retained_at_3m" in cohort

    def test_each_cohort_has_retained_at_6m(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        for cohort in response.json()["cohorts"]:
            assert "retained_at_6m" in cohort

    def test_each_cohort_has_avg_ltv_estimate(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        for cohort in response.json()["cohorts"]:
            assert "avg_ltv_sar_estimate" in cohort

    def test_has_generated_at(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        assert "generated_at" in response.json()

    def test_has_bilingual_labels(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        data = response.json()
        assert "label_ar" in data
        assert "label_en" in data

    def test_has_note_for_null_values(self):
        response = client.get("/api/v1/revenue-intelligence/ops/cohort-analysis")
        data = response.json()
        assert "note_ar" in data
        assert "note_en" in data


# ===========================================================================
# API tests — POST /revenue-alert
# ===========================================================================


class TestRevenueAlert:
    def _valid_body(self) -> dict:
        return {
            "alert_type": "mrr_drop",
            "description": "MRR dropped by 15% compared to last month",
            "estimated_impact_sar": 5000.0,
            "urgency": "high",
        }

    def test_returns_200_for_valid_body(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert response.status_code == 200

    def test_has_governance_decision(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert "governance_decision" in response.json()

    def test_governance_is_approval_first(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert response.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_has_alert_id(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert "alert_id" in response.json()

    def test_alert_id_starts_with_ralert(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert response.json()["alert_id"].startswith("RALERT-")

    def test_has_message_ar(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert "message_ar" in response.json()

    def test_has_message_en(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert "message_en" in response.json()

    def test_has_type_label_ar(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert "alert_type_label_ar" in response.json()

    def test_has_type_label_en(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert "alert_type_label_en" in response.json()

    def test_status_is_pending_approval(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert response.json()["status"] == "alert_logged_pending_approval"

    def test_all_valid_alert_types_accepted(self):
        for alert_type in _VALID_ALERT_TYPES:
            body = self._valid_body()
            body["alert_type"] = alert_type
            response = client.post(
                "/api/v1/revenue-intelligence/ops/revenue-alert",
                json=body,
            )
            assert response.status_code == 200, f"Failed for alert_type={alert_type}"

    def test_all_valid_urgency_levels_accepted(self):
        for urgency in _VALID_URGENCY:
            body = self._valid_body()
            body["urgency"] = urgency
            response = client.post(
                "/api/v1/revenue-intelligence/ops/revenue-alert",
                json=body,
            )
            assert response.status_code == 200, f"Failed for urgency={urgency}"

    def test_invalid_alert_type_returns_422(self):
        body = self._valid_body()
        body["alert_type"] = "not_a_valid_type"
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=body,
        )
        assert response.status_code == 422

    def test_invalid_urgency_returns_422(self):
        body = self._valid_body()
        body["urgency"] = "critical"
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=body,
        )
        assert response.status_code == 422

    def test_short_description_returns_422(self):
        body = self._valid_body()
        body["description"] = "short"
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=body,
        )
        assert response.status_code == 422

    def test_negative_impact_returns_422(self):
        body = self._valid_body()
        body["estimated_impact_sar"] = -100.0
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=body,
        )
        assert response.status_code == 422

    def test_zero_impact_is_accepted(self):
        body = self._valid_body()
        body["estimated_impact_sar"] = 0.0
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=body,
        )
        assert response.status_code == 200

    def test_has_generated_at(self):
        response = client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert "generated_at" in response.json()

    def test_alert_is_stored(self):
        assert len(_ALERTS) == 0
        client.post(
            "/api/v1/revenue-intelligence/ops/revenue-alert",
            json=self._valid_body(),
        )
        assert len(_ALERTS) == 1


# ===========================================================================
# API tests — GET /nrr-analysis
# ===========================================================================


class TestNrrAnalysis:
    def test_returns_200(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert response.status_code == 200

    def test_has_governance_decision(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert "governance_decision" in response.json()

    def test_governance_is_allow_with_review(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert response.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_nrr_pct(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert "nrr_pct" in response.json()

    def test_nrr_pct_is_numeric(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert isinstance(response.json()["nrr_pct"], (int, float))

    def test_has_gross_revenue_retention_pct(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert "gross_revenue_retention_pct" in response.json()

    def test_has_expansion_revenue_pct(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert "expansion_revenue_pct" in response.json()

    def test_has_churn_rate_pct(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert "churn_rate_pct" in response.json()

    def test_has_interpretation_ar(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert "interpretation_ar" in response.json()
        assert len(response.json()["interpretation_ar"]) > 0

    def test_has_interpretation_en(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert "interpretation_en" in response.json()
        assert len(response.json()["interpretation_en"]) > 0

    def test_has_target_nrr(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert "target_nrr_pct" in response.json()
        assert response.json()["target_nrr_pct"] == 110.0

    def test_has_generated_at(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        assert "generated_at" in response.json()

    def test_has_bilingual_labels(self):
        response = client.get("/api/v1/revenue-intelligence/ops/nrr-analysis")
        data = response.json()
        assert "label_ar" in data
        assert "label_en" in data
