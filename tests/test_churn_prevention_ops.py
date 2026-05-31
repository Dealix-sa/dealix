"""Tests for the churn_prevention_ops API router.

Covers: data integrity, dashboard, at-risk, signals analysis, client detail,
log-intervention, send-proof-pack, risk score computation, governance decision
presence, doctrine compliance (WhatsApp blocked), and helper functions.
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

from api.routers.churn_prevention_ops import (  # noqa: E402
    VALID_DELIVERY_CHANNELS,
    VALID_INTERVENTION_TYPES,
    VALID_OUTCOMES,
    _CLIENTS,
    _INTERVENTIONS,
    _client_or_404,
    _compute_risk_score,
    _enrich_client,
    _intervention_label,
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
def _clear_interventions():
    """Clear the in-memory intervention log after each test."""
    yield
    _INTERVENTIONS.clear()


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


# ===========================================================================
# Unit tests — _compute_risk_score
# ===========================================================================


class TestComputeRiskScore:
    def test_returns_tuple_of_two(self):
        result = _compute_risk_score(_CLIENTS["ARC-001"])
        assert len(result) == 2

    def test_score_is_float(self):
        score, _ = _compute_risk_score(_CLIENTS["ARC-001"])
        assert isinstance(score, float)

    def test_band_is_string(self):
        _, band = _compute_risk_score(_CLIENTS["ARC-001"])
        assert isinstance(band, str)

    def test_score_in_0_to_100_range(self):
        for record in _CLIENTS.values():
            score, _ = _compute_risk_score(record)
            assert 0.0 <= score <= 100.0, f"Score {score} out of range for {record['client_id']}"

    def test_band_is_valid_value(self):
        valid_bands = {"critical", "high", "medium", "low"}
        for record in _CLIENTS.values():
            _, band = _compute_risk_score(record)
            assert band in valid_bands

    def test_critical_band_at_70(self):
        # Construct a client that yields exactly 70 or above
        c = {"health_score": 0, "days_since_last_checkin": 90, "consecutive_missed_checkins": 5,
             "nps_score": 1, "contract_days_remaining": 0}
        score, band = _compute_risk_score(c)
        assert band == "critical"
        assert score >= 70.0

    def test_low_band_for_healthy_client(self):
        c = {"health_score": 100, "days_since_last_checkin": 0, "consecutive_missed_checkins": 0,
             "nps_score": 10, "contract_days_remaining": 180}
        score, band = _compute_risk_score(c)
        assert band == "low"
        assert score < 30.0

    def test_high_health_lowers_risk(self):
        low_health = {"health_score": 10, "days_since_last_checkin": 0,
                      "consecutive_missed_checkins": 0, "nps_score": 10, "contract_days_remaining": 180}
        high_health = {"health_score": 90, "days_since_last_checkin": 0,
                       "consecutive_missed_checkins": 0, "nps_score": 10, "contract_days_remaining": 180}
        score_low, _ = _compute_risk_score(low_health)
        score_high, _ = _compute_risk_score(high_health)
        assert score_low > score_high

    def test_more_missed_checkins_raises_risk(self):
        few = {"health_score": 50, "days_since_last_checkin": 10, "consecutive_missed_checkins": 0,
               "nps_score": 5, "contract_days_remaining": 90}
        many = {"health_score": 50, "days_since_last_checkin": 10, "consecutive_missed_checkins": 5,
                "nps_score": 5, "contract_days_remaining": 90}
        score_few, _ = _compute_risk_score(few)
        score_many, _ = _compute_risk_score(many)
        assert score_many > score_few

    def test_low_nps_raises_risk(self):
        high_nps = {"health_score": 50, "days_since_last_checkin": 10, "consecutive_missed_checkins": 1,
                    "nps_score": 10, "contract_days_remaining": 90}
        low_nps = {"health_score": 50, "days_since_last_checkin": 10, "consecutive_missed_checkins": 1,
                   "nps_score": 1, "contract_days_remaining": 90}
        score_high, _ = _compute_risk_score(high_nps)
        score_low, _ = _compute_risk_score(low_nps)
        assert score_low > score_high

    def test_expiring_contract_raises_risk(self):
        long_contract = {"health_score": 50, "days_since_last_checkin": 10,
                         "consecutive_missed_checkins": 1, "nps_score": 5,
                         "contract_days_remaining": 180}
        short_contract = {"health_score": 50, "days_since_last_checkin": 10,
                          "consecutive_missed_checkins": 1, "nps_score": 5,
                          "contract_days_remaining": 5}
        score_long, _ = _compute_risk_score(long_contract)
        score_short, _ = _compute_risk_score(short_contract)
        assert score_short > score_long

    def test_arc001_is_critical(self):
        _, band = _compute_risk_score(_CLIENTS["ARC-001"])
        assert band == "critical"

    def test_arc002_is_critical(self):
        _, band = _compute_risk_score(_CLIENTS["ARC-002"])
        assert band == "critical"

    def test_arc003_is_high(self):
        _, band = _compute_risk_score(_CLIENTS["ARC-003"])
        assert band == "high"

    def test_arc004_is_high(self):
        _, band = _compute_risk_score(_CLIENTS["ARC-004"])
        assert band == "high"

    def test_arc005_is_medium(self):
        _, band = _compute_risk_score(_CLIENTS["ARC-005"])
        assert band == "medium"

    def test_arc006_is_medium(self):
        _, band = _compute_risk_score(_CLIENTS["ARC-006"])
        assert band == "medium"

    def test_arc007_is_low(self):
        _, band = _compute_risk_score(_CLIENTS["ARC-007"])
        assert band == "low"


# ===========================================================================
# Unit tests — _intervention_label
# ===========================================================================


class TestInterventionLabel:
    def test_returns_tuple_of_two_strings(self):
        result = _intervention_label("executive_checkin")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(s, str) for s in result)

    def test_executive_checkin_ar_non_empty(self):
        ar, _ = _intervention_label("executive_checkin")
        assert len(ar) > 0

    def test_executive_checkin_en_non_empty(self):
        _, en = _intervention_label("executive_checkin")
        assert len(en) > 0

    def test_all_valid_types_have_labels(self):
        for itype in VALID_INTERVENTION_TYPES:
            ar, en = _intervention_label(itype)
            assert len(ar) > 0 and len(en) > 0

    def test_unknown_type_returns_fallback(self):
        ar, en = _intervention_label("unknown_type")
        assert ar == "unknown_type"
        assert en == "unknown_type"


# ===========================================================================
# Unit tests — _client_or_404
# ===========================================================================


class TestClientOr404:
    def test_valid_id_returns_record(self):
        record = _client_or_404("ARC-001")
        assert record["client_id"] == "ARC-001"

    def test_case_insensitive(self):
        record = _client_or_404("arc-001")
        assert record["client_id"] == "ARC-001"

    def test_unknown_id_raises_404(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            _client_or_404("ARC-999")
        assert exc_info.value.status_code == 404

    def test_404_detail_has_ar_and_en(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            _client_or_404("ARC-999")
        detail = exc_info.value.detail
        assert "ar" in detail
        assert "en" in detail


# ===========================================================================
# Unit tests — _enrich_client
# ===========================================================================


class TestEnrichClient:
    def test_adds_risk_score(self):
        enriched = _enrich_client(_CLIENTS["ARC-001"])
        assert "risk_score" in enriched

    def test_adds_risk_band(self):
        enriched = _enrich_client(_CLIENTS["ARC-001"])
        assert "risk_band" in enriched

    def test_preserves_existing_fields(self):
        enriched = _enrich_client(_CLIENTS["ARC-001"])
        assert enriched["client_id"] == "ARC-001"

    def test_risk_score_consistent_with_compute(self):
        expected_score, expected_band = _compute_risk_score(_CLIENTS["ARC-001"])
        enriched = _enrich_client(_CLIENTS["ARC-001"])
        assert enriched["risk_score"] == expected_score
        assert enriched["risk_band"] == expected_band


# ===========================================================================
# Data integrity tests
# ===========================================================================


class TestDataIntegrity:
    def test_exactly_seven_clients(self):
        assert len(_CLIENTS) == 7

    def test_client_ids_arc_001_to_007(self):
        expected = {f"ARC-{i:03d}" for i in range(1, 8)}
        assert set(_CLIENTS.keys()) == expected

    def test_two_critical_clients(self):
        critical = [cid for cid, r in _CLIENTS.items()
                    if _compute_risk_score(r)[1] == "critical"]
        assert len(critical) == 2

    def test_two_high_clients(self):
        high = [cid for cid, r in _CLIENTS.items()
                if _compute_risk_score(r)[1] == "high"]
        assert len(high) == 2

    def test_two_medium_clients(self):
        medium = [cid for cid, r in _CLIENTS.items()
                  if _compute_risk_score(r)[1] == "medium"]
        assert len(medium) == 2

    def test_one_low_client(self):
        low = [cid for cid, r in _CLIENTS.items()
               if _compute_risk_score(r)[1] == "low"]
        assert len(low) == 1

    def test_every_client_has_required_fields(self):
        required = {
            "client_id", "company_ar", "company_en", "tier",
            "health_score", "days_since_last_checkin", "consecutive_missed_checkins",
            "nps_score", "contract_days_remaining", "monthly_value_sar",
            "churn_signals", "last_contact_ar", "last_contact_en",
        }
        for cid, record in _CLIENTS.items():
            assert required.issubset(record.keys()), f"Client {cid} missing fields"

    def test_all_tiers_valid(self):
        valid_tiers = {"essential", "professional", "enterprise"}
        for cid, record in _CLIENTS.items():
            assert record["tier"] in valid_tiers

    def test_all_health_scores_in_range(self):
        for cid, record in _CLIENTS.items():
            assert 0 <= record["health_score"] <= 100

    def test_all_nps_scores_in_range(self):
        for cid, record in _CLIENTS.items():
            assert 1 <= record["nps_score"] <= 10

    def test_all_churn_signals_non_empty_for_at_risk(self):
        for cid, record in _CLIENTS.items():
            _, band = _compute_risk_score(record)
            if band in ("critical", "high"):
                assert len(record["churn_signals"]) > 0, f"{cid} has no churn signals"

    def test_all_company_ar_non_empty(self):
        for cid, record in _CLIENTS.items():
            assert len(record["company_ar"]) > 0

    def test_all_company_en_non_empty(self):
        for cid, record in _CLIENTS.items():
            assert len(record["company_en"]) > 0

    def test_all_monthly_values_positive(self):
        for cid, record in _CLIENTS.items():
            assert record["monthly_value_sar"] > 0

    def test_all_contract_days_non_negative(self):
        for cid, record in _CLIENTS.items():
            assert record["contract_days_remaining"] >= 0

    def test_churn_signals_is_list(self):
        for cid, record in _CLIENTS.items():
            assert isinstance(record["churn_signals"], list)

    def test_valid_intervention_types_set(self):
        expected = {"executive_checkin", "proof_pack_delivery", "contract_review",
                    "discount_offer", "feature_demo", "escalation"}
        assert VALID_INTERVENTION_TYPES == expected

    def test_valid_outcomes_set(self):
        assert VALID_OUTCOMES == {"positive", "neutral", "negative"}

    def test_valid_delivery_channels_set(self):
        assert VALID_DELIVERY_CHANNELS == {"email", "in_person"}

    def test_whatsapp_not_in_valid_channels(self):
        assert "whatsapp" not in VALID_DELIVERY_CHANNELS


# ===========================================================================
# Dashboard endpoint tests
# ===========================================================================


class TestDashboard:
    def test_200_status(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert response.status_code == 200

    def test_governance_decision_present(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert "governance_decision" in response.json()

    def test_governance_decision_allow_with_review(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert response.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_monitored_is_seven(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert response.json()["total_monitored"] == 7

    def test_critical_count_is_two(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert response.json()["critical_count"] == 2

    def test_high_count_is_two(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert response.json()["high_count"] == 2

    def test_medium_count_is_two(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert response.json()["medium_count"] == 2

    def test_low_count_is_one(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert response.json()["low_count"] == 1

    def test_at_risk_mrr_is_sum_of_critical_and_high(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        data = response.json()
        expected = sum(
            r["monthly_value_sar"] for r in _CLIENTS.values()
            if _compute_risk_score(r)[1] in ("critical", "high")
        )
        assert data["total_at_risk_mrr_sar"] == expected

    def test_avg_risk_score_is_float(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert isinstance(response.json()["avg_risk_score"], float)

    def test_clients_list_has_seven_items(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert len(response.json()["clients"]) == 7

    def test_clients_sorted_by_risk_descending(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        scores = [c["risk_score"] for c in response.json()["clients"]]
        assert scores == sorted(scores, reverse=True)

    def test_each_client_has_risk_score(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        for c in response.json()["clients"]:
            assert "risk_score" in c

    def test_each_client_has_risk_band(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        for c in response.json()["clients"]:
            assert "risk_band" in c

    def test_action_ar_present(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert "action_ar" in response.json()
        assert len(response.json()["action_ar"]) > 0

    def test_action_en_present(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert "action_en" in response.json()
        assert len(response.json()["action_en"]) > 0

    def test_generated_at_present(self):
        response = client.get("/api/v1/churn-prevention/dashboard")
        assert "generated_at" in response.json()


# ===========================================================================
# At-risk endpoint tests
# ===========================================================================


class TestAtRisk:
    def test_200_status(self):
        response = client.get("/api/v1/churn-prevention/at-risk")
        assert response.status_code == 200

    def test_governance_decision_present(self):
        response = client.get("/api/v1/churn-prevention/at-risk")
        assert "governance_decision" in response.json()

    def test_governance_decision_allow_with_review(self):
        response = client.get("/api/v1/churn-prevention/at-risk")
        assert response.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_returns_only_critical_and_high(self):
        response = client.get("/api/v1/churn-prevention/at-risk")
        data = response.json()
        for c in data["clients"]:
            assert c["risk_band"] in ("critical", "high")

    def test_total_at_risk_is_four(self):
        response = client.get("/api/v1/churn-prevention/at-risk")
        assert response.json()["total_at_risk"] == 4

    def test_each_client_has_recommended_intervention_ar(self):
        response = client.get("/api/v1/churn-prevention/at-risk")
        for c in response.json()["clients"]:
            assert "recommended_intervention_ar" in c
            assert len(c["recommended_intervention_ar"]) > 0

    def test_each_client_has_recommended_intervention_en(self):
        response = client.get("/api/v1/churn-prevention/at-risk")
        for c in response.json()["clients"]:
            assert "recommended_intervention_en" in c
            assert len(c["recommended_intervention_en"]) > 0

    def test_critical_gets_executive_checkin_recommendation(self):
        response = client.get("/api/v1/churn-prevention/at-risk")
        for c in response.json()["clients"]:
            if c["risk_band"] == "critical":
                assert "executive" in c["recommended_intervention_en"].lower() or \
                       "24" in c["recommended_intervention_en"]

    def test_high_gets_proof_pack_recommendation(self):
        response = client.get("/api/v1/churn-prevention/at-risk")
        for c in response.json()["clients"]:
            if c["risk_band"] == "high":
                assert "proof" in c["recommended_intervention_en"].lower() or \
                       "48" in c["recommended_intervention_en"]

    def test_filter_by_critical_returns_only_critical(self):
        response = client.get("/api/v1/churn-prevention/at-risk?risk_band=critical")
        data = response.json()
        for c in data["clients"]:
            assert c["risk_band"] == "critical"

    def test_filter_by_high_returns_only_high(self):
        response = client.get("/api/v1/churn-prevention/at-risk?risk_band=high")
        data = response.json()
        for c in data["clients"]:
            assert c["risk_band"] == "high"

    def test_filter_by_critical_count_is_two(self):
        response = client.get("/api/v1/churn-prevention/at-risk?risk_band=critical")
        assert response.json()["total_at_risk"] == 2

    def test_filter_by_high_count_is_two(self):
        response = client.get("/api/v1/churn-prevention/at-risk?risk_band=high")
        assert response.json()["total_at_risk"] == 2


# ===========================================================================
# Client detail endpoint tests
# ===========================================================================


class TestClientDetail:
    def test_200_for_valid_client(self):
        response = client.get("/api/v1/churn-prevention/ARC-001")
        assert response.status_code == 200

    def test_404_for_unknown_client(self):
        response = client.get("/api/v1/churn-prevention/ARC-999")
        assert response.status_code == 404

    def test_governance_decision_present(self):
        response = client.get("/api/v1/churn-prevention/ARC-001")
        assert "governance_decision" in response.json()

    def test_governance_decision_allow_with_review(self):
        response = client.get("/api/v1/churn-prevention/ARC-001")
        assert response.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_risk_score_computed(self):
        response = client.get("/api/v1/churn-prevention/ARC-001")
        data = response.json()
        assert "risk_score" in data
        assert isinstance(data["risk_score"], float)

    def test_risk_band_computed(self):
        response = client.get("/api/v1/churn-prevention/ARC-001")
        data = response.json()
        assert "risk_band" in data
        assert data["risk_band"] in ("critical", "high", "medium", "low")

    def test_arc001_risk_band_is_critical(self):
        response = client.get("/api/v1/churn-prevention/ARC-001")
        assert response.json()["risk_band"] == "critical"

    def test_arc007_risk_band_is_low(self):
        response = client.get("/api/v1/churn-prevention/ARC-007")
        assert response.json()["risk_band"] == "low"

    def test_intervention_history_present_and_list(self):
        response = client.get("/api/v1/churn-prevention/ARC-001")
        data = response.json()
        assert "intervention_history" in data
        assert isinstance(data["intervention_history"], list)

    def test_recommended_actions_is_list_of_three(self):
        response = client.get("/api/v1/churn-prevention/ARC-001")
        actions = response.json()["recommended_actions"]
        assert isinstance(actions, list)
        assert len(actions) == 3

    def test_recommended_actions_have_ar_and_en(self):
        response = client.get("/api/v1/churn-prevention/ARC-001")
        for action in response.json()["recommended_actions"]:
            assert "ar" in action
            assert "en" in action

    def test_all_core_fields_present(self):
        response = client.get("/api/v1/churn-prevention/ARC-001")
        data = response.json()
        for field in ("client_id", "company_ar", "company_en", "tier",
                      "health_score", "days_since_last_checkin",
                      "consecutive_missed_checkins", "nps_score",
                      "contract_days_remaining", "monthly_value_sar",
                      "churn_signals", "last_contact_ar", "last_contact_en"):
            assert field in data, f"Missing field: {field}"

    def test_case_insensitive_client_id(self):
        response = client.get("/api/v1/churn-prevention/arc-001")
        assert response.status_code == 200
        assert response.json()["client_id"] == "ARC-001"


# ===========================================================================
# Log intervention endpoint tests
# ===========================================================================


class TestLogIntervention:
    _valid_body = {
        "intervention_type": "executive_checkin",
        "notes": "Called the client to discuss renewal and address concerns.",
        "outcome": "positive",
        "next_review_days": 14,
    }

    def test_200_for_valid_request(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=self._valid_body,
        )
        assert response.status_code == 200

    def test_governance_decision_is_approval_first(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=self._valid_body,
        )
        assert response.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_response_has_intervention_id(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=self._valid_body,
        )
        data = response.json()
        assert "intervention_id" in data
        assert data["intervention_id"].startswith("CPO-")

    def test_response_has_timestamp(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=self._valid_body,
        )
        assert "generated_at" in response.json()

    def test_response_has_risk_guidance_ar(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=self._valid_body,
        )
        data = response.json()
        assert "updated_risk_guidance_ar" in data
        assert len(data["updated_risk_guidance_ar"]) > 0

    def test_response_has_risk_guidance_en(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=self._valid_body,
        )
        data = response.json()
        assert "updated_risk_guidance_en" in data
        assert len(data["updated_risk_guidance_en"]) > 0

    def test_negative_outcome_guidance_mentions_escalation(self):
        body = {**self._valid_body, "outcome": "negative"}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=body,
        )
        guidance = response.json()["updated_risk_guidance_en"].lower()
        assert "escalat" in guidance or "negative" in guidance

    def test_404_for_unknown_client(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-999/log-intervention",
            json=self._valid_body,
        )
        assert response.status_code == 404

    def test_422_for_invalid_intervention_type(self):
        body = {**self._valid_body, "intervention_type": "cold_call"}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=body,
        )
        assert response.status_code == 422

    def test_422_for_invalid_outcome(self):
        body = {**self._valid_body, "outcome": "excellent"}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=body,
        )
        assert response.status_code == 422

    def test_422_for_notes_too_short(self):
        body = {**self._valid_body, "notes": "Short"}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=body,
        )
        assert response.status_code == 422

    def test_422_for_next_review_days_zero(self):
        body = {**self._valid_body, "next_review_days": 0}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=body,
        )
        assert response.status_code == 422

    def test_422_for_next_review_days_over_90(self):
        body = {**self._valid_body, "next_review_days": 91}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=body,
        )
        assert response.status_code == 422

    def test_all_valid_intervention_types_accepted(self):
        for itype in VALID_INTERVENTION_TYPES:
            body = {**self._valid_body, "intervention_type": itype}
            response = client.post(
                "/api/v1/churn-prevention/ARC-001/log-intervention",
                json=body,
            )
            assert response.status_code == 200, f"Type {itype} unexpectedly rejected"

    def test_all_valid_outcomes_accepted(self):
        for outcome in VALID_OUTCOMES:
            body = {**self._valid_body, "outcome": outcome}
            response = client.post(
                "/api/v1/churn-prevention/ARC-001/log-intervention",
                json=body,
            )
            assert response.status_code == 200, f"Outcome {outcome} unexpectedly rejected"

    def test_intervention_appears_in_history(self):
        client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=self._valid_body,
        )
        detail = client.get("/api/v1/churn-prevention/ARC-001")
        history = detail.json()["intervention_history"]
        assert len(history) == 1
        assert history[0]["intervention_type"] == "executive_checkin"

    def test_response_has_intervention_type_label_ar(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=self._valid_body,
        )
        assert "intervention_type_label_ar" in response.json()

    def test_response_has_intervention_type_label_en(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/log-intervention",
            json=self._valid_body,
        )
        assert "intervention_type_label_en" in response.json()


# ===========================================================================
# Send proof pack endpoint tests
# ===========================================================================


class TestSendProofPack:
    _valid_body = {
        "notes": "Sending updated Proof Pack to at-risk client.",
        "delivery_channel": "email",
    }

    def test_200_for_valid_email_channel(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=self._valid_body,
        )
        assert response.status_code == 200

    def test_200_for_in_person_channel(self):
        body = {**self._valid_body, "delivery_channel": "in_person"}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=body,
        )
        assert response.status_code == 200

    def test_governance_decision_is_approval_first(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=self._valid_body,
        )
        assert response.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_response_has_delivery_id(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=self._valid_body,
        )
        data = response.json()
        assert "delivery_id" in data
        assert data["delivery_id"].startswith("PPD-")

    def test_404_for_unknown_client(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-999/send-proof-pack",
            json=self._valid_body,
        )
        assert response.status_code == 404

    def test_whatsapp_returns_400(self):
        body = {**self._valid_body, "delivery_channel": "whatsapp"}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=body,
        )
        assert response.status_code == 400

    def test_whatsapp_400_contains_doctrine_note(self):
        body = {**self._valid_body, "delivery_channel": "whatsapp"}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=body,
        )
        detail = response.json()["detail"]
        assert "doctrine_note" in detail
        assert detail["doctrine_note"] == "no_cold_whatsapp"

    def test_whatsapp_400_mentions_unsolicited_outreach(self):
        body = {**self._valid_body, "delivery_channel": "whatsapp"}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=body,
        )
        detail = response.json()["detail"]
        # Both ar and en messages should address the doctrine
        assert "whatsapp" in detail["en"].lower() or "unsolicited" in detail["en"].lower()

    def test_invalid_channel_returns_422(self):
        body = {**self._valid_body, "delivery_channel": "sms"}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=body,
        )
        assert response.status_code == 422

    def test_notes_too_short_returns_422(self):
        body = {**self._valid_body, "notes": "Hi"}
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=body,
        )
        assert response.status_code == 422

    def test_response_has_risk_score_and_band(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=self._valid_body,
        )
        data = response.json()
        assert "risk_score" in data
        assert "risk_band" in data

    def test_response_has_message_ar_and_en(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json=self._valid_body,
        )
        data = response.json()
        assert "message_ar" in data
        assert "message_en" in data


# ===========================================================================
# Signals analysis endpoint tests
# ===========================================================================


class TestSignalsAnalysis:
    def test_200_status(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert response.status_code == 200

    def test_governance_decision_present(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert "governance_decision" in response.json()

    def test_governance_decision_allow_with_review(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert response.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_signal_frequency_is_dict(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert isinstance(response.json()["signal_frequency"], dict)

    def test_signal_frequency_populated(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        freq = response.json()["signal_frequency"]
        assert len(freq) > 0

    def test_signal_frequency_values_are_positive_ints(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        for count in response.json()["signal_frequency"].values():
            assert isinstance(count, int)
            assert count > 0

    def test_most_common_signal_is_string(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert isinstance(response.json()["most_common_signal"], str)

    def test_at_risk_by_tier_is_dict(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert isinstance(response.json()["at_risk_by_tier"], dict)

    def test_at_risk_by_tier_populated(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        tier_data = response.json()["at_risk_by_tier"]
        assert len(tier_data) > 0
        total = sum(tier_data.values())
        assert total == 4  # 2 critical + 2 high

    def test_recommendations_ar_is_list(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert isinstance(response.json()["recommendations_ar"], list)

    def test_recommendations_en_is_list(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert isinstance(response.json()["recommendations_en"], list)

    def test_recommendations_ar_non_empty(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert len(response.json()["recommendations_ar"]) > 0

    def test_recommendations_en_non_empty(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert len(response.json()["recommendations_en"]) > 0

    def test_generated_at_present(self):
        response = client.get("/api/v1/churn-prevention/signals-analysis")
        assert "generated_at" in response.json()


# ===========================================================================
# Doctrine tests — WhatsApp explicitly blocked
# ===========================================================================


class TestDoctrineWhatsAppBlocked:
    def test_whatsapp_blocked_in_send_proof_pack(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json={"notes": "Testing whatsapp block", "delivery_channel": "whatsapp"},
        )
        assert response.status_code == 400

    def test_whatsapp_block_includes_doctrine_note_field(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json={"notes": "Testing whatsapp block", "delivery_channel": "whatsapp"},
        )
        detail = response.json()["detail"]
        assert "doctrine_note" in detail

    def test_whatsapp_not_listed_as_allowed_channel(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json={"notes": "Testing whatsapp block", "delivery_channel": "whatsapp"},
        )
        detail = response.json()["detail"]
        if "allowed_channels" in detail:
            assert "whatsapp" not in detail["allowed_channels"]

    def test_whatsapp_not_in_valid_delivery_channels_constant(self):
        assert "whatsapp" not in VALID_DELIVERY_CHANNELS

    def test_email_allowed_channel_works(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json={"notes": "Valid delivery via email.", "delivery_channel": "email"},
        )
        assert response.status_code == 200

    def test_in_person_allowed_channel_works(self):
        response = client.post(
            "/api/v1/churn-prevention/ARC-001/send-proof-pack",
            json={"notes": "Valid delivery in person.", "delivery_channel": "in_person"},
        )
        assert response.status_code == 200
