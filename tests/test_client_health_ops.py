"""Tests for the client_health_ops API router.

Covers: data integrity, portfolio endpoint, at-risk endpoint, single client
detail, update-score, intervention, benchmarks, health computation accuracy,
and governance decision presence on every endpoint.
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

from api.routers.client_health_ops import (  # noqa: E402
    DIMENSIONS,
    VALID_INTERVENTION_TYPES,
    _BENCHMARKS,
    _CLIENTS,
    _client_or_404,
    _compute_health,
    _now_iso,
    _recommended_action,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# Helper: reset _CLIENTS scores between tests that mutate state
# ---------------------------------------------------------------------------

import copy  # noqa: E402

_CLIENTS_BACKUP = copy.deepcopy(_CLIENTS)


@pytest.fixture(autouse=True)
def _restore_clients():
    """Restore client data after each test that may have mutated scores."""
    yield
    for k, v in _CLIENTS_BACKUP.items():
        _CLIENTS[k]["health_scores"] = copy.deepcopy(v["health_scores"])
        _CLIENTS[k]["last_updated"] = v["last_updated"]
        _CLIENTS[k]["pending_intervention"] = v["pending_intervention"]


# ===========================================================================
# Unit tests — pure helpers
# ===========================================================================


class TestNowIso:
    def test_returns_string(self):
        result = _now_iso()
        assert isinstance(result, str)

    def test_contains_t_separator(self):
        result = _now_iso()
        assert "T" in result

    def test_ends_with_utc_offset(self):
        result = _now_iso()
        # UTC datetimes from datetime.now(UTC) end with +00:00
        assert "+00:00" in result or "Z" in result or result.endswith("+00:00")


class TestComputeHealth:
    def test_healthy_band_at_80(self):
        scores = {d: 80.0 for d in DIMENSIONS}
        score, band = _compute_health(scores)
        assert score == 80.0
        assert band == "healthy"

    def test_healthy_band_above_80(self):
        scores = {d: 95.0 for d in DIMENSIONS}
        _, band = _compute_health(scores)
        assert band == "healthy"

    def test_at_risk_band_at_60(self):
        scores = {d: 60.0 for d in DIMENSIONS}
        score, band = _compute_health(scores)
        assert score == 60.0
        assert band == "at_risk"

    def test_at_risk_band_at_79(self):
        # Score of 79 for all dims → weighted sum = 79 → at_risk
        scores = {d: 79.0 for d in DIMENSIONS}
        score, band = _compute_health(scores)
        assert score == 79.0
        assert band == "at_risk"

    def test_critical_band_below_60(self):
        scores = {d: 59.0 for d in DIMENSIONS}
        _, band = _compute_health(scores)
        assert band == "critical"

    def test_critical_band_at_zero(self):
        scores = {d: 0.0 for d in DIMENSIONS}
        score, band = _compute_health(scores)
        assert score == 0.0
        assert band == "critical"

    def test_weights_sum_to_one(self):
        total_weight = sum(DIMENSIONS.values())
        assert abs(total_weight - 1.0) < 1e-9

    def test_weighted_sum_not_uniform(self):
        # data_readiness and delivery_quality each have 0.20 weight
        # recurring_revenue has 0.10 — verify unevenness matters
        scores = {d: 0.0 for d in DIMENSIONS}
        scores["data_readiness"] = 100.0
        score, _ = _compute_health(scores)
        assert abs(score - 20.0) < 0.01

    def test_returns_tuple_of_two(self):
        scores = {d: 50.0 for d in DIMENSIONS}
        result = _compute_health(scores)
        assert len(result) == 2

    def test_score_is_float(self):
        scores = {d: 70.0 for d in DIMENSIONS}
        score, _ = _compute_health(scores)
        assert isinstance(score, float)

    def test_missing_dimension_treated_as_zero(self):
        scores = {}
        score, band = _compute_health(scores)
        assert score == 0.0
        assert band == "critical"


class TestDimensions:
    def test_all_six_dimensions_present(self):
        expected = {
            "data_readiness",
            "onboarding_ops",
            "delivery_quality",
            "zatca_compliance",
            "client_retention",
            "recurring_revenue",
        }
        assert set(DIMENSIONS.keys()) == expected

    def test_data_readiness_weight(self):
        assert DIMENSIONS["data_readiness"] == 0.20

    def test_onboarding_ops_weight(self):
        assert DIMENSIONS["onboarding_ops"] == 0.15

    def test_delivery_quality_weight(self):
        assert DIMENSIONS["delivery_quality"] == 0.20

    def test_zatca_compliance_weight(self):
        assert DIMENSIONS["zatca_compliance"] == 0.15

    def test_client_retention_weight(self):
        assert DIMENSIONS["client_retention"] == 0.20

    def test_recurring_revenue_weight(self):
        assert DIMENSIONS["recurring_revenue"] == 0.10


class TestRecommendedAction:
    def test_critical_below_40_returns_urgent(self):
        action_ar, action_en = _recommended_action("critical", 35.0)
        assert "24" in action_en
        assert "24" in action_ar

    def test_critical_above_40_returns_proactive(self):
        action_ar, action_en = _recommended_action("critical", 55.0)
        assert "48" in action_en
        assert "48" in action_ar

    def test_at_risk_returns_followup(self):
        action_ar, action_en = _recommended_action("at_risk", 65.0)
        assert len(action_en) > 0
        assert len(action_ar) > 0

    def test_returns_tuple(self):
        result = _recommended_action("at_risk", 70.0)
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestClientOrNotFound:
    def test_valid_id_returns_record(self):
        record = _client_or_404("CLT-001")
        assert record["client_id"] == "CLT-001"

    def test_case_insensitive(self):
        record = _client_or_404("clt-001")
        assert record["client_id"] == "CLT-001"

    def test_unknown_id_raises_404(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            _client_or_404("CLT-999")
        assert exc_info.value.status_code == 404

    def test_404_detail_bilingual(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            _client_or_404("CLT-999")
        detail = exc_info.value.detail
        assert "ar" in detail
        assert "en" in detail


# ===========================================================================
# Data integrity tests
# ===========================================================================


class TestDataIntegrity:
    def test_exactly_eight_clients(self):
        assert len(_CLIENTS) == 8

    def test_client_ids_clt_001_to_008(self):
        expected_ids = {f"CLT-{i:03d}" for i in range(1, 9)}
        assert set(_CLIENTS.keys()) == expected_ids

    def test_every_client_has_six_dimension_scores(self):
        for cid, record in _CLIENTS.items():
            assert set(record["health_scores"].keys()) == set(DIMENSIONS.keys()), (
                f"Client {cid} missing dimensions"
            )

    def test_all_scores_in_range_0_to_100(self):
        for cid, record in _CLIENTS.items():
            for dim, score in record["health_scores"].items():
                assert 0.0 <= score <= 100.0, (
                    f"Client {cid} dimension {dim} score {score} out of range"
                )

    def test_every_client_has_required_fields(self):
        required = {
            "client_id", "company_ar", "company_en", "sector", "tier",
            "health_scores", "last_updated",
        }
        for cid, record in _CLIENTS.items():
            assert required.issubset(record.keys()), f"Client {cid} missing fields"

    def test_at_least_two_healthy_clients(self):
        healthy = [
            cid for cid, r in _CLIENTS.items()
            if _compute_health(r["health_scores"])[1] == "healthy"
        ]
        assert len(healthy) >= 2

    def test_at_least_three_at_risk_clients(self):
        at_risk = [
            cid for cid, r in _CLIENTS.items()
            if _compute_health(r["health_scores"])[1] == "at_risk"
        ]
        assert len(at_risk) >= 3

    def test_at_least_two_critical_clients(self):
        critical = [
            cid for cid, r in _CLIENTS.items()
            if _compute_health(r["health_scores"])[1] == "critical"
        ]
        assert len(critical) >= 2

    def test_at_least_one_pending_intervention(self):
        pending = [cid for cid, r in _CLIENTS.items() if r.get("pending_intervention")]
        assert len(pending) >= 1

    def test_all_sectors_are_strings(self):
        for cid, record in _CLIENTS.items():
            assert isinstance(record["sector"], str)
            assert len(record["sector"]) > 0

    def test_all_tiers_valid(self):
        valid_tiers = {"essential", "professional", "enterprise"}
        for cid, record in _CLIENTS.items():
            assert record["tier"] in valid_tiers, (
                f"Client {cid} has invalid tier: {record['tier']}"
            )

    def test_all_company_ar_non_empty(self):
        for cid, record in _CLIENTS.items():
            assert isinstance(record["company_ar"], str)
            assert len(record["company_ar"]) > 0

    def test_all_company_en_non_empty(self):
        for cid, record in _CLIENTS.items():
            assert isinstance(record["company_en"], str)
            assert len(record["company_en"]) > 0

    def test_valid_intervention_types_count(self):
        assert len(VALID_INTERVENTION_TYPES) == 5

    def test_valid_intervention_type_names(self):
        expected = {
            "proof_pack_delivery",
            "executive_checkin",
            "technical_review",
            "contract_review",
            "escalation",
        }
        assert VALID_INTERVENTION_TYPES == expected


# ===========================================================================
# Portfolio endpoint tests
# ===========================================================================


class TestPortfolioEndpoint:
    def test_returns_200(self):
        r = client.get("/api/v1/client-health/portfolio")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/client-health/portfolio")
        assert "governance_decision" in r.json()

    def test_governance_decision_value(self):
        r = client.get("/api/v1/client-health/portfolio")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_portfolio_summary_present(self):
        r = client.get("/api/v1/client-health/portfolio")
        assert "portfolio_summary" in r.json()

    def test_total_clients_is_eight(self):
        r = client.get("/api/v1/client-health/portfolio")
        assert r.json()["portfolio_summary"]["total_clients"] == 8

    def test_clients_list_present(self):
        r = client.get("/api/v1/client-health/portfolio")
        assert "clients" in r.json()
        assert len(r.json()["clients"]) == 8

    def test_sorted_by_health_ascending(self):
        r = client.get("/api/v1/client-health/portfolio")
        scores = [c["health_score"] for c in r.json()["clients"]]
        assert scores == sorted(scores)

    def test_avg_health_score_present(self):
        r = client.get("/api/v1/client-health/portfolio")
        summary = r.json()["portfolio_summary"]
        assert "avg_health_score" in summary
        assert isinstance(summary["avg_health_score"], float)

    def test_critical_count_accurate(self):
        r = client.get("/api/v1/client-health/portfolio")
        summary = r.json()["portfolio_summary"]
        clients_list = r.json()["clients"]
        expected_critical = sum(1 for c in clients_list if c["health_band"] == "critical")
        assert summary["critical_count"] == expected_critical

    def test_at_risk_count_accurate(self):
        r = client.get("/api/v1/client-health/portfolio")
        summary = r.json()["portfolio_summary"]
        clients_list = r.json()["clients"]
        expected_at_risk = sum(1 for c in clients_list if c["health_band"] == "at_risk")
        assert summary["at_risk_count"] == expected_at_risk

    def test_healthy_count_accurate(self):
        r = client.get("/api/v1/client-health/portfolio")
        summary = r.json()["portfolio_summary"]
        clients_list = r.json()["clients"]
        expected_healthy = sum(1 for c in clients_list if c["health_band"] == "healthy")
        assert summary["healthy_count"] == expected_healthy

    def test_health_band_distribution_present(self):
        r = client.get("/api/v1/client-health/portfolio")
        summary = r.json()["portfolio_summary"]
        dist = summary["health_band_distribution"]
        assert "critical" in dist
        assert "at_risk" in dist
        assert "healthy" in dist

    def test_health_band_counts_consistent(self):
        r = client.get("/api/v1/client-health/portfolio")
        summary = r.json()["portfolio_summary"]
        dist = summary["health_band_distribution"]
        assert dist["critical"] == summary["critical_count"]
        assert dist["at_risk"] == summary["at_risk_count"]
        assert dist["healthy"] == summary["healthy_count"]

    def test_each_client_has_health_score(self):
        r = client.get("/api/v1/client-health/portfolio")
        for c in r.json()["clients"]:
            assert "health_score" in c
            assert isinstance(c["health_score"], float)

    def test_each_client_has_health_band(self):
        r = client.get("/api/v1/client-health/portfolio")
        for c in r.json()["clients"]:
            assert "health_band" in c
            assert c["health_band"] in ("healthy", "at_risk", "critical")

    def test_generated_at_present(self):
        r = client.get("/api/v1/client-health/portfolio")
        assert "generated_at" in r.json()


# ===========================================================================
# At-risk endpoint tests
# ===========================================================================


class TestAtRiskEndpoint:
    def test_returns_200(self):
        r = client.get("/api/v1/client-health/at-risk")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/client-health/at-risk")
        assert "governance_decision" in r.json()

    def test_governance_decision_value(self):
        r = client.get("/api/v1/client-health/at-risk")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_only_at_risk_and_critical_returned(self):
        r = client.get("/api/v1/client-health/at-risk")
        for c in r.json()["clients"]:
            assert c["health_band"] in ("at_risk", "critical"), (
                f"Client {c['client_id']} has band {c['health_band']}, should be at_risk or critical"
            )

    def test_no_healthy_clients_in_response(self):
        r = client.get("/api/v1/client-health/at-risk")
        bands = [c["health_band"] for c in r.json()["clients"]]
        assert "healthy" not in bands

    def test_recommended_action_ar_present(self):
        r = client.get("/api/v1/client-health/at-risk")
        for c in r.json()["clients"]:
            assert "recommended_action_ar" in c
            assert len(c["recommended_action_ar"]) > 0

    def test_recommended_action_en_present(self):
        r = client.get("/api/v1/client-health/at-risk")
        for c in r.json()["clients"]:
            assert "recommended_action_en" in c
            assert len(c["recommended_action_en"]) > 0

    def test_sorted_by_health_ascending(self):
        r = client.get("/api/v1/client-health/at-risk")
        scores = [c["health_score"] for c in r.json()["clients"]]
        assert scores == sorted(scores)

    def test_total_at_risk_count_present(self):
        r = client.get("/api/v1/client-health/at-risk")
        assert "total_at_risk" in r.json()

    def test_total_at_risk_matches_list_length(self):
        r = client.get("/api/v1/client-health/at-risk")
        data = r.json()
        assert data["total_at_risk"] == len(data["clients"])

    def test_generated_at_present(self):
        r = client.get("/api/v1/client-health/at-risk")
        assert "generated_at" in r.json()


# ===========================================================================
# Single client detail endpoint tests
# ===========================================================================


class TestClientDetailEndpoint:
    def test_returns_200_for_clt001(self):
        r = client.get("/api/v1/client-health/CLT-001")
        assert r.status_code == 200

    def test_returns_404_for_unknown(self):
        r = client.get("/api/v1/client-health/CLT-999")
        assert r.status_code == 404

    def test_governance_decision_present(self):
        r = client.get("/api/v1/client-health/CLT-001")
        assert "governance_decision" in r.json()

    def test_governance_decision_value(self):
        r = client.get("/api/v1/client-health/CLT-001")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_all_required_fields_present(self):
        r = client.get("/api/v1/client-health/CLT-001")
        data = r.json()
        required = {
            "client_id", "company_ar", "company_en", "sector", "tier",
            "health_score", "health_band", "dimension_scores",
            "dimension_detail", "last_updated", "governance_decision",
        }
        assert required.issubset(data.keys())

    def test_correct_client_id_returned(self):
        r = client.get("/api/v1/client-health/CLT-002")
        assert r.json()["client_id"] == "CLT-002"

    def test_dimension_detail_has_six_entries(self):
        r = client.get("/api/v1/client-health/CLT-001")
        assert len(r.json()["dimension_detail"]) == 6

    def test_dimension_detail_has_required_keys(self):
        r = client.get("/api/v1/client-health/CLT-001")
        for entry in r.json()["dimension_detail"]:
            assert "dimension" in entry
            assert "score" in entry
            assert "weight" in entry
            assert "weighted_contribution" in entry

    def test_health_band_is_valid(self):
        r = client.get("/api/v1/client-health/CLT-001")
        assert r.json()["health_band"] in ("healthy", "at_risk", "critical")

    def test_health_score_consistent_with_band(self):
        r = client.get("/api/v1/client-health/CLT-001")
        data = r.json()
        score = data["health_score"]
        band = data["health_band"]
        if score >= 80:
            assert band == "healthy"
        elif score >= 60:
            assert band == "at_risk"
        else:
            assert band == "critical"

    def test_clt001_is_healthy(self):
        r = client.get("/api/v1/client-health/CLT-001")
        assert r.json()["health_band"] == "healthy"

    def test_clt007_is_critical(self):
        r = client.get("/api/v1/client-health/CLT-007")
        assert r.json()["health_band"] == "critical"

    def test_case_insensitive_lookup(self):
        r = client.get("/api/v1/client-health/clt-001")
        assert r.status_code == 200
        assert r.json()["client_id"] == "CLT-001"

    def test_generated_at_present(self):
        r = client.get("/api/v1/client-health/CLT-001")
        assert "generated_at" in r.json()


# ===========================================================================
# Update score endpoint tests
# ===========================================================================


class TestUpdateScoreEndpoint:
    def test_returns_200_on_valid_update(self):
        payload = {"updates": {"data_readiness": 75.0}, "reason": "Monthly review complete"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert r.status_code == 200

    def test_governance_decision_approval_first(self):
        payload = {"updates": {"data_readiness": 75.0}, "reason": "Monthly review complete"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_new_health_score_present(self):
        payload = {"updates": {"delivery_quality": 80.0}, "reason": "Score corrected"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert "new_health_score" in r.json()

    def test_new_health_band_present(self):
        payload = {"updates": {"delivery_quality": 80.0}, "reason": "Score corrected"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert "new_health_band" in r.json()

    def test_invalid_dimension_returns_422(self):
        payload = {"updates": {"nonexistent_dimension": 80.0}, "reason": "Test invalid"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert r.status_code == 422

    def test_score_above_100_returns_422(self):
        payload = {"updates": {"data_readiness": 101.0}, "reason": "Test range"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert r.status_code == 422

    def test_score_below_0_returns_422(self):
        payload = {"updates": {"data_readiness": -1.0}, "reason": "Test range"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert r.status_code == 422

    def test_unknown_client_returns_404(self):
        payload = {"updates": {"data_readiness": 80.0}, "reason": "Test not found"}
        r = client.post("/api/v1/client-health/CLT-999/update-score", json=payload)
        assert r.status_code == 404

    def test_short_reason_returns_422(self):
        payload = {"updates": {"data_readiness": 80.0}, "reason": "ab"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert r.status_code == 422

    def test_previous_and_new_scores_differ_after_update(self):
        payload = {"updates": {"data_readiness": 5.0}, "reason": "Forced degradation for test"}
        r = client.post("/api/v1/client-health/CLT-001/update-score", json=payload)
        data = r.json()
        assert data["previous_health_score"] != data["new_health_score"]

    def test_dimensions_updated_list_present(self):
        payload = {"updates": {"onboarding_ops": 70.0}, "reason": "Onboarding progress noted"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert "dimensions_updated" in r.json()
        assert "onboarding_ops" in r.json()["dimensions_updated"]

    def test_reason_echoed_in_response(self):
        payload = {"updates": {"onboarding_ops": 70.0}, "reason": "Quarterly review done"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert r.json()["reason"] == "Quarterly review done"

    def test_multiple_dimension_updates_accepted(self):
        payload = {
            "updates": {"data_readiness": 80.0, "client_retention": 75.0},
            "reason": "Mid-cycle review completed",
        }
        r = client.post("/api/v1/client-health/CLT-004/update-score", json=payload)
        assert r.status_code == 200

    def test_message_ar_present(self):
        payload = {"updates": {"data_readiness": 70.0}, "reason": "Regular update"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert "message_ar" in r.json()

    def test_message_en_present(self):
        payload = {"updates": {"data_readiness": 70.0}, "reason": "Regular update"}
        r = client.post("/api/v1/client-health/CLT-003/update-score", json=payload)
        assert "message_en" in r.json()


# ===========================================================================
# Intervention endpoint tests
# ===========================================================================


class TestInterventionEndpoint:
    _VALID_BODY = {
        "intervention_type": "executive_checkin",
        "notes": "Executive reviewed the account and aligned on next steps",
        "next_action_date": "2026-06-15",
    }

    def test_returns_200_on_valid_intervention(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert r.status_code == 200

    def test_governance_decision_approval_first(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_intervention_id_present(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        data = r.json()
        assert "intervention_id" in data
        assert data["intervention_id"].startswith("INT-")

    def test_client_id_echoed(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert r.json()["client_id"] == "CLT-005"

    def test_intervention_type_echoed(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert r.json()["intervention_type"] == "executive_checkin"

    def test_bilingual_labels_present(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        data = r.json()
        assert "intervention_type_label_ar" in data
        assert "intervention_type_label_en" in data

    def test_confirmation_ar_present(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert "confirmation_ar" in r.json()
        assert len(r.json()["confirmation_ar"]) > 0

    def test_confirmation_en_present(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert "confirmation_en" in r.json()
        assert len(r.json()["confirmation_en"]) > 0

    def test_invalid_intervention_type_returns_422(self):
        body = {**self._VALID_BODY, "intervention_type": "send_marketing_blast"}
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=body)
        assert r.status_code == 422

    def test_short_notes_returns_422(self):
        body = {**self._VALID_BODY, "notes": "Too short"}
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=body)
        assert r.status_code == 422

    def test_unknown_client_returns_404(self):
        r = client.post("/api/v1/client-health/CLT-999/intervention", json=self._VALID_BODY)
        assert r.status_code == 404

    def test_each_valid_intervention_type_accepted(self):
        for itype in VALID_INTERVENTION_TYPES:
            body = {
                "intervention_type": itype,
                "notes": f"Testing intervention type {itype} with adequate notes length",
                "next_action_date": "2026-06-20",
            }
            r = client.post("/api/v1/client-health/CLT-006/intervention", json=body)
            assert r.status_code == 200, f"Type {itype} returned {r.status_code}"

    def test_next_action_date_present_in_response(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert r.json()["next_action_date"] == "2026-06-15"

    def test_health_score_at_intervention_present(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert "health_score_at_intervention" in r.json()

    def test_health_band_at_intervention_present(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert "health_band_at_intervention" in r.json()

    def test_message_ar_present(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert "message_ar" in r.json()

    def test_message_en_present(self):
        r = client.post("/api/v1/client-health/CLT-005/intervention", json=self._VALID_BODY)
        assert "message_en" in r.json()


# ===========================================================================
# Benchmarks endpoint tests
# ===========================================================================


class TestBenchmarksEndpoint:
    def test_returns_200(self):
        r = client.get("/api/v1/client-health/benchmarks")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/client-health/benchmarks")
        assert "governance_decision" in r.json()

    def test_governance_decision_value(self):
        r = client.get("/api/v1/client-health/benchmarks")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_benchmarks_list_present(self):
        r = client.get("/api/v1/client-health/benchmarks")
        assert "benchmarks" in r.json()
        assert isinstance(r.json()["benchmarks"], list)

    def test_multiple_sectors_in_benchmarks(self):
        r = client.get("/api/v1/client-health/benchmarks")
        assert len(r.json()["benchmarks"]) >= 3

    def test_each_benchmark_has_sector(self):
        r = client.get("/api/v1/client-health/benchmarks")
        for b in r.json()["benchmarks"]:
            assert "sector" in b
            assert len(b["sector"]) > 0

    def test_each_benchmark_has_sector_ar(self):
        r = client.get("/api/v1/client-health/benchmarks")
        for b in r.json()["benchmarks"]:
            assert "sector_ar" in b

    def test_each_benchmark_has_avg_health_score(self):
        r = client.get("/api/v1/client-health/benchmarks")
        for b in r.json()["benchmarks"]:
            assert "benchmark_avg_health_score" in b

    def test_each_benchmark_has_dimension_benchmarks(self):
        r = client.get("/api/v1/client-health/benchmarks")
        for b in r.json()["benchmarks"]:
            assert "dimension_benchmarks" in b
            assert len(b["dimension_benchmarks"]) == 6

    def test_portfolio_comparison_present(self):
        r = client.get("/api/v1/client-health/benchmarks")
        for b in r.json()["benchmarks"]:
            assert "dealix_portfolio_avg" in b
            assert "vs_benchmark" in b

    def test_note_ar_present(self):
        r = client.get("/api/v1/client-health/benchmarks")
        assert "note_ar" in r.json()

    def test_note_en_present(self):
        r = client.get("/api/v1/client-health/benchmarks")
        assert "note_en" in r.json()

    def test_generated_at_present(self):
        r = client.get("/api/v1/client-health/benchmarks")
        assert "generated_at" in r.json()

    def test_technology_sector_benchmark_present(self):
        r = client.get("/api/v1/client-health/benchmarks")
        sectors = [b["sector"] for b in r.json()["benchmarks"]]
        assert "technology" in sectors


# ===========================================================================
# Health computation accuracy tests
# ===========================================================================


class TestHealthComputationAccuracy:
    def test_all_100_gives_score_100(self):
        scores = {d: 100.0 for d in DIMENSIONS}
        score, band = _compute_health(scores)
        assert score == 100.0
        assert band == "healthy"

    def test_all_80_gives_healthy(self):
        scores = {d: 80.0 for d in DIMENSIONS}
        _, band = _compute_health(scores)
        assert band == "healthy"

    def test_all_60_gives_at_risk(self):
        scores = {d: 60.0 for d in DIMENSIONS}
        _, band = _compute_health(scores)
        assert band == "at_risk"

    def test_all_59_gives_critical(self):
        scores = {d: 59.0 for d in DIMENSIONS}
        _, band = _compute_health(scores)
        assert band == "critical"

    def test_clt001_healthy(self):
        _, band = _compute_health(_CLIENTS["CLT-001"]["health_scores"])
        assert band == "healthy"

    def test_clt002_healthy(self):
        _, band = _compute_health(_CLIENTS["CLT-002"]["health_scores"])
        assert band == "healthy"

    def test_clt006_critical(self):
        _, band = _compute_health(_CLIENTS["CLT-006"]["health_scores"])
        assert band == "critical"

    def test_clt007_critical(self):
        _, band = _compute_health(_CLIENTS["CLT-007"]["health_scores"])
        assert band == "critical"

    def test_score_respects_weights(self):
        # Only set recurring_revenue (weight 0.10) to 100, rest zero
        scores = {d: 0.0 for d in DIMENSIONS}
        scores["recurring_revenue"] = 100.0
        score, _ = _compute_health(scores)
        assert abs(score - 10.0) < 0.01

    def test_client_retention_weight_contribution(self):
        # Only set client_retention (weight 0.20) to 100, rest zero
        scores = {d: 0.0 for d in DIMENSIONS}
        scores["client_retention"] = 100.0
        score, _ = _compute_health(scores)
        assert abs(score - 20.0) < 0.01
