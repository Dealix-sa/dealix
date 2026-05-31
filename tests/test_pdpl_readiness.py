"""Tests for the PDPL Readiness Assessment API.

Covers: scoring formula, data-map classification, penalties data integrity,
checklist structure, and API endpoints.
"""

from __future__ import annotations

import os
import sys
import types

import pytest

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")

# Defensive stub for api.security.api_key in case it is imported transitively
_security_stub = types.ModuleType("api.security.api_key")
_security_stub.require_api_key = lambda: None  # type: ignore[attr-defined]
sys.modules.setdefault("api.security.api_key", _security_stub)

from api.routers.pdpl_readiness import (
    CHECKLIST,
    PENALTIES,
    PDPLAssessBody,
    _classify_data_category,
    _score_assessment,
    router,
)
from fastapi import FastAPI
from fastapi.testclient import TestClient

_app = FastAPI()
_app.include_router(router)
client = TestClient(_app)


# ---------------------------------------------------------------------------
# TestPDPLScoring
# ---------------------------------------------------------------------------


class TestPDPLScoring:
    def _full_body(self) -> PDPLAssessBody:
        return PDPLAssessBody(
            has_privacy_policy=True,
            has_consent_mechanism=True,
            has_data_retention_policy=True,
            has_dsar_process=True,
            stores_data_saudi_servers=True,
            has_breach_response_plan=True,
            processes_sensitive_data=False,
            has_dpo_appointed=True,
            has_staff_training=True,
            has_vendor_agreements=True,
        )

    def _empty_body(self) -> PDPLAssessBody:
        return PDPLAssessBody()

    def test_full_compliance_score_is_100(self):
        result = _score_assessment(self._full_body())
        assert result["score"] == 100

    def test_zero_compliance_score_is_0(self):
        result = _score_assessment(self._empty_body())
        assert result["score"] == 0

    def test_full_compliance_tier_is_compliant(self):
        result = _score_assessment(self._full_body())
        assert result["tier"] == "compliant"

    def test_zero_compliance_tier_is_critical(self):
        result = _score_assessment(self._empty_body())
        assert result["tier"] == "critical"

    def test_consent_mechanism_is_critical_item(self):
        # Missing consent_mechanism should appear in critical_gaps
        body = PDPLAssessBody(
            has_privacy_policy=True,
            has_consent_mechanism=False,
            has_dsar_process=True,
        )
        result = _score_assessment(body)
        critical_fields = {g["field"] for g in result["critical_gaps"]}
        assert "has_consent_mechanism" in critical_fields

    def test_dsar_process_is_critical_item(self):
        body = PDPLAssessBody(
            has_consent_mechanism=True,
            has_dsar_process=False,
        )
        result = _score_assessment(body)
        critical_fields = {g["field"] for g in result["critical_gaps"]}
        assert "has_dsar_process" in critical_fields

    def test_partial_score_at_60_gives_partial_tier(self):
        # consent(20) + dsar(15) + privacy(15) + retention(10) = 60
        body = PDPLAssessBody(
            has_consent_mechanism=True,
            has_dsar_process=True,
            has_privacy_policy=True,
            has_data_retention_policy=True,
        )
        result = _score_assessment(body)
        assert result["score"] == 60
        assert result["tier"] == "partial"

    def test_score_above_80_is_compliant(self):
        body = PDPLAssessBody(
            has_privacy_policy=True,
            has_consent_mechanism=True,
            has_data_retention_policy=True,
            has_dsar_process=True,
            stores_data_saudi_servers=True,
            has_breach_response_plan=True,
            has_vendor_agreements=True,
        )
        result = _score_assessment(body)
        assert result["score"] >= 80
        assert result["tier"] == "compliant"

    def test_sensitive_data_flag_elevates_risk_from_low(self):
        body = self._full_body()
        body.processes_sensitive_data = True
        result = _score_assessment(body)
        # Full score is compliant (low risk) but sensitive_data_flag elevates it
        assert result["sensitive_data_flag"] is True
        assert result["risk_level"] in ("medium", "high", "critical")

    def test_no_sensitive_data_low_risk_when_compliant(self):
        body = self._full_body()
        body.processes_sensitive_data = False
        result = _score_assessment(body)
        assert result["risk_level"] == "low"

    def test_critical_gap_count_matches_critical_gaps_list(self):
        result = _score_assessment(self._empty_body())
        assert result["critical_gap_count"] == len(result["critical_gaps"])

    def test_gaps_do_not_include_answered_true_fields(self):
        body = PDPLAssessBody(has_consent_mechanism=True)
        result = _score_assessment(body)
        gap_fields = {g["field"] for g in result["gaps"]}
        assert "has_consent_mechanism" not in gap_fields

    def test_score_between_40_and_60_is_at_risk(self):
        # consent(20) + dsar(15) = 35 → below 40 (critical)
        # consent(20) + dsar(15) + retention(10) = 45 → at_risk
        body = PDPLAssessBody(
            has_consent_mechanism=True,
            has_dsar_process=True,
            has_data_retention_policy=True,
        )
        result = _score_assessment(body)
        assert 40 <= result["score"] < 60
        assert result["tier"] == "at_risk"

    def test_earned_weight_equals_sum_of_matched_items(self):
        body = PDPLAssessBody(has_privacy_policy=True)
        result = _score_assessment(body)
        privacy_weight = next(i["weight"] for i in CHECKLIST if i["field"] == "has_privacy_policy")
        assert result["earned_weight"] == privacy_weight


# ---------------------------------------------------------------------------
# TestDataMapEndpoint
# ---------------------------------------------------------------------------


class TestDataMapEndpoint:
    def test_email_classified_as_personal(self):
        result = _classify_data_category("email")
        assert result["pdpl_class"] == "personal"

    def test_health_classified_as_sensitive(self):
        result = _classify_data_category("health")
        assert result["pdpl_class"] == "sensitive"

    def test_financial_classified_as_sensitive(self):
        result = _classify_data_category("financial")
        assert result["pdpl_class"] == "sensitive"

    def test_phone_classified_as_personal(self):
        result = _classify_data_category("phone")
        assert result["pdpl_class"] == "personal"

    def test_location_risk_level_is_high(self):
        result = _classify_data_category("location")
        assert result["risk_level"] == "high"

    def test_health_risk_level_is_critical(self):
        result = _classify_data_category("health")
        assert result["risk_level"] == "critical"

    def test_national_id_risk_level_is_critical(self):
        result = _classify_data_category("national_id")
        assert result["risk_level"] == "critical"

    def test_unknown_category_returns_unknown_class(self):
        result = _classify_data_category("unknown_xyz")
        assert result["pdpl_class"] == "unknown"

    def test_category_field_preserved_in_output(self):
        result = _classify_data_category("email")
        assert result["category"] == "email"

    def test_required_controls_not_empty(self):
        result = _classify_data_category("health")
        assert len(result["required_controls"]) > 0

    def test_relevant_article_present(self):
        result = _classify_data_category("financial")
        assert "Art." in result["relevant_article"]

    def test_case_insensitive_lookup(self):
        result = _classify_data_category("Health")
        assert result["pdpl_class"] == "sensitive"


# ---------------------------------------------------------------------------
# TestPenalties
# ---------------------------------------------------------------------------


class TestPenalties:
    def test_all_penalties_present(self):
        assert len(PENALTIES) == 5

    def test_selling_data_penalty_sar_is_3m(self):
        pen = next(p for p in PENALTIES if "sell" in p["violation_en"].lower())
        assert pen["penalty_sar"] == 3_000_000

    def test_cross_border_penalty_is_5m(self):
        pen = next(p for p in PENALTIES if "cross-border" in p["violation_en"].lower())
        assert pen["max_sar"] == 5_000_000

    def test_sensitive_data_violation_is_5m(self):
        pen = next(p for p in PENALTIES if "sensitive" in p["violation_en"].lower())
        assert pen["max_sar"] == 5_000_000

    def test_max_penalty_sar_above_1m(self):
        max_pen = max(p["max_sar"] for p in PENALTIES)
        assert max_pen > 1_000_000

    def test_selling_data_is_criminal(self):
        pen = next(p for p in PENALTIES if "sell" in p["violation_en"].lower())
        assert pen["criminal"] is True

    def test_consent_violation_not_criminal(self):
        pen = next(p for p in PENALTIES if "consent" in p["violation_en"].lower())
        assert pen["criminal"] is False

    def test_all_penalties_have_pdpl_article(self):
        for pen in PENALTIES:
            assert "pdpl_article" in pen
            assert pen["pdpl_article"].startswith("Art.")

    def test_all_penalties_have_bilingual_fields(self):
        for pen in PENALTIES:
            assert "violation_ar" in pen
            assert "violation_en" in pen


# ---------------------------------------------------------------------------
# TestChecklistIntegrity
# ---------------------------------------------------------------------------


class TestChecklistIntegrity:
    def test_weights_sum_to_100(self):
        total = sum(item["weight"] for item in CHECKLIST)
        assert total == 100

    def test_bilingual_labels_present(self):
        for item in CHECKLIST:
            assert "title_ar" in item
            assert "title_en" in item
            assert len(item["title_ar"]) > 0
            assert len(item["title_en"]) > 0

    def test_critical_flag_is_bool(self):
        for item in CHECKLIST:
            assert isinstance(item["critical"], bool)

    def test_field_names_match_assessment_body(self):
        body_fields = PDPLAssessBody.model_fields.keys()
        for item in CHECKLIST:
            assert item["field"] in body_fields, f"Field {item['field']} not in PDPLAssessBody"

    def test_checklist_has_at_least_9_items(self):
        assert len(CHECKLIST) >= 9

    def test_critical_items_have_nonzero_weight(self):
        for item in CHECKLIST:
            if item["critical"]:
                assert item["weight"] > 0


# ---------------------------------------------------------------------------
# TestAPIAssess
# ---------------------------------------------------------------------------


class TestAPIAssess:
    def test_returns_200(self):
        r = client.post("/api/v1/pdpl-readiness/assess", json={})
        assert r.status_code == 200

    def test_governance_decision_present(self):
        data = client.post("/api/v1/pdpl-readiness/assess", json={}).json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_score_in_response(self):
        data = client.post("/api/v1/pdpl-readiness/assess", json={}).json()
        assert "readiness_score" in data
        assert 0 <= data["readiness_score"] <= 100

    def test_disclaimer_present(self):
        data = client.post("/api/v1/pdpl-readiness/assess", json={}).json()
        assert "disclaimer_ar" in data
        assert "disclaimer_en" in data

    def test_full_compliance_returns_100(self):
        full_body = {
            "has_privacy_policy": True,
            "has_consent_mechanism": True,
            "has_data_retention_policy": True,
            "has_dsar_process": True,
            "stores_data_saudi_servers": True,
            "has_breach_response_plan": True,
            "processes_sensitive_data": False,
            "has_dpo_appointed": True,
            "has_staff_training": True,
            "has_vendor_agreements": True,
        }
        data = client.post("/api/v1/pdpl-readiness/assess", json=full_body).json()
        assert data["readiness_score"] == 100

    def test_readiness_tier_has_id_and_ar(self):
        data = client.post("/api/v1/pdpl-readiness/assess", json={}).json()
        assert "readiness_tier" in data
        assert "id" in data["readiness_tier"]
        assert "ar" in data["readiness_tier"]

    def test_extra_fields_rejected(self):
        r = client.post("/api/v1/pdpl-readiness/assess", json={"unknown_field": True})
        assert r.status_code == 422

    def test_recommendation_bilingual(self):
        data = client.post("/api/v1/pdpl-readiness/assess", json={}).json()
        assert "recommendation" in data
        assert "ar" in data["recommendation"]
        assert "en" in data["recommendation"]


# ---------------------------------------------------------------------------
# TestAPIChecklist
# ---------------------------------------------------------------------------


class TestAPIChecklist:
    def test_returns_200(self):
        assert client.get("/api/v1/pdpl-readiness/checklist").status_code == 200

    def test_total_items_matches(self):
        data = client.get("/api/v1/pdpl-readiness/checklist").json()
        # total_items includes the scored items + sensitive_data risk flag item
        assert data["total_items"] == len(CHECKLIST) + 1

    def test_governance_decision_present(self):
        data = client.get("/api/v1/pdpl-readiness/checklist").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_weight_is_100(self):
        data = client.get("/api/v1/pdpl-readiness/checklist").json()
        assert data["total_weight"] == 100

    def test_critical_items_count_positive(self):
        data = client.get("/api/v1/pdpl-readiness/checklist").json()
        assert data["critical_items"] > 0

    def test_disclaimer_present(self):
        data = client.get("/api/v1/pdpl-readiness/checklist").json()
        assert "disclaimer_ar" in data


# ---------------------------------------------------------------------------
# TestAPIPenalties
# ---------------------------------------------------------------------------


class TestAPIPenalties:
    def test_returns_200(self):
        assert client.get("/api/v1/pdpl-readiness/penalties").status_code == 200

    def test_governance_decision_present(self):
        data = client.get("/api/v1/pdpl-readiness/penalties").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_max_single_penalty_sar_above_1m(self):
        data = client.get("/api/v1/pdpl-readiness/penalties").json()
        assert data["max_single_penalty_sar"] > 1_000_000

    def test_penalties_list_present(self):
        data = client.get("/api/v1/pdpl-readiness/penalties").json()
        assert len(data["penalties"]) > 0

    def test_disclaimer_present(self):
        data = client.get("/api/v1/pdpl-readiness/penalties").json()
        assert "disclaimer_ar" in data
        assert "disclaimer_en" in data

    def test_regulator_bilingual(self):
        data = client.get("/api/v1/pdpl-readiness/penalties").json()
        assert "regulator_ar" in data
        assert "regulator_en" in data


# ---------------------------------------------------------------------------
# TestAPIDataMap
# ---------------------------------------------------------------------------


class TestAPIDataMap:
    def test_returns_200(self):
        r = client.post("/api/v1/pdpl-readiness/data-map", json={"data_categories": []})
        assert r.status_code == 200

    def test_health_classified_as_sensitive(self):
        data = client.post(
            "/api/v1/pdpl-readiness/data-map",
            json={"data_categories": ["health"]},
        ).json()
        assert data["sensitive_count"] == 1
        assert data["classifications"][0]["pdpl_class"] == "sensitive"

    def test_email_classified_as_personal(self):
        data = client.post(
            "/api/v1/pdpl-readiness/data-map",
            json={"data_categories": ["email"]},
        ).json()
        assert data["personal_count"] == 1
        assert data["classifications"][0]["pdpl_class"] == "personal"

    def test_overall_risk_critical_when_sensitive_present(self):
        data = client.post(
            "/api/v1/pdpl-readiness/data-map",
            json={"data_categories": ["health", "email"]},
        ).json()
        assert data["overall_risk_level"] == "critical"

    def test_governance_decision_present(self):
        data = client.post(
            "/api/v1/pdpl-readiness/data-map",
            json={"data_categories": ["email"]},
        ).json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_categories_analyzed_count_correct(self):
        data = client.post(
            "/api/v1/pdpl-readiness/data-map",
            json={"data_categories": ["email", "phone", "health"]},
        ).json()
        assert data["categories_analyzed"] == 3

    def test_aggregated_controls_not_empty_for_sensitive(self):
        data = client.post(
            "/api/v1/pdpl-readiness/data-map",
            json={"data_categories": ["financial"]},
        ).json()
        assert len(data["aggregated_required_controls"]) > 0

    def test_disclaimer_present(self):
        data = client.post(
            "/api/v1/pdpl-readiness/data-map",
            json={"data_categories": ["email"]},
        ).json()
        assert "disclaimer_ar" in data

    def test_extra_fields_rejected(self):
        r = client.post(
            "/api/v1/pdpl-readiness/data-map",
            json={"data_categories": ["email"], "unknown": True},
        )
        assert r.status_code == 422
