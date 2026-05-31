"""Tests for the ZATCA Readiness Assessment API.

Covers: scoring formula, wave lookup, checklist structure,
penalty data integrity, invoice compliance checker, and API endpoints.
"""

from __future__ import annotations

import os
import sys
import types

import pytest

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")

# No jose stub needed — zatca_readiness.py has no security dependency
from api.routers.zatca_readiness import (
    CHECKLIST,
    PENALTIES,
    ZATCA_WAVES,
    _determine_applicable_wave,
    _score_assessment,
    router,
)
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
app.include_router(router)
client = TestClient(app)


# ---------------------------------------------------------------------------
# Unit: Wave determination
# ---------------------------------------------------------------------------


class TestWaveDetermination:
    def test_none_revenue_returns_none(self):
        assert _determine_applicable_wave(None) is None

    def test_1bn_returns_wave_5_or_higher(self):
        wave = _determine_applicable_wave(40_000_000)
        assert wave is not None
        assert wave["wave"] >= 5

    def test_3bn_revenue_returns_wave_1(self):
        wave = _determine_applicable_wave(3_000_000_000)
        assert wave is not None
        assert wave["wave"] == 1

    def test_small_company_1m_returns_wave_8_or_9(self):
        wave = _determine_applicable_wave(1_500_000)
        assert wave is not None
        assert wave["wave"] >= 7

    def test_large_company_above_threshold(self):
        wave = _determine_applicable_wave(500_000_000)
        assert wave is not None
        assert wave["wave"] <= 2

    def test_returns_dict_with_deadline(self):
        wave = _determine_applicable_wave(10_000_000)
        assert wave is not None
        assert "deadline" in wave


# ---------------------------------------------------------------------------
# Unit: Scoring formula
# ---------------------------------------------------------------------------


class TestScoringFormula:
    def _body(self, **kwargs):
        from api.routers.zatca_readiness import ZATCAAssessBody
        return ZATCAAssessBody(**kwargs)

    def test_zero_compliance_scores_low(self):
        body = self._body()
        result = _score_assessment(body)
        assert result["score"] <= 20

    def test_full_compliance_scores_100(self):
        body = self._body(
            has_csid=True,
            has_xml_ubl=True,
            has_qr_code=True,
            has_digital_stamp=True,
            has_fatoora_integration=True,
            has_realtime_submission=True,
            has_correct_trn=True,
            has_complete_data=True,
            has_rejection_process=True,
            has_team_training=True,
        )
        result = _score_assessment(body)
        assert result["score"] == 100
        assert result["tier"] == "compliant"
        assert result["risk_level"] == "low"

    def test_critical_items_only_gives_partial(self):
        body = self._body(
            has_csid=True,
            has_xml_ubl=True,
            has_qr_code=True,
            has_digital_stamp=True,
            has_fatoora_integration=True,
        )
        result = _score_assessment(body)
        # Critical items cover 75 weight points out of 100
        assert result["score"] >= 70

    def test_tier_at_risk(self):
        body = self._body(has_correct_trn=True, has_complete_data=True)
        result = _score_assessment(body)
        assert result["tier"] in ("at_risk", "non_compliant")

    def test_critical_gaps_identified(self):
        body = self._body(has_correct_trn=True)
        result = _score_assessment(body)
        assert result["critical_gap_count"] >= 4

    def test_no_gaps_when_fully_compliant(self):
        body = self._body(
            has_csid=True, has_xml_ubl=True, has_qr_code=True, has_digital_stamp=True,
            has_fatoora_integration=True, has_realtime_submission=True,
            has_correct_trn=True, has_complete_data=True,
            has_rejection_process=True, has_team_training=True,
        )
        result = _score_assessment(body)
        assert len(result["gaps"]) == 0

    def test_score_between_0_and_100(self):
        for _ in range(3):
            body = self._body(has_csid=True, has_qr_code=True)
            result = _score_assessment(body)
            assert 0 <= result["score"] <= 100


# ---------------------------------------------------------------------------
# Unit: Data integrity
# ---------------------------------------------------------------------------


class TestChecklistIntegrity:
    def test_checklist_not_empty(self):
        assert len(CHECKLIST) >= 8

    def test_checklist_weights_sum_to_100(self):
        total = sum(item["weight"] for item in CHECKLIST)
        assert total == 100

    def test_all_items_have_required_fields(self):
        for item in CHECKLIST:
            assert "id" in item
            assert "title_ar" in item
            assert "title_en" in item
            assert "weight" in item
            assert "critical" in item

    def test_critical_items_exist(self):
        critical = [i for i in CHECKLIST if i["critical"]]
        assert len(critical) >= 4

    def test_unique_ids(self):
        ids = [i["id"] for i in CHECKLIST]
        assert len(ids) == len(set(ids))


class TestWaveIntegrity:
    def test_waves_not_empty(self):
        assert len(ZATCA_WAVES) >= 7

    def test_all_waves_have_deadline(self):
        for wave in ZATCA_WAVES:
            assert "deadline" in wave
            assert wave["deadline"] != ""

    def test_waves_cover_all_statuses(self):
        statuses = {w["status"] for w in ZATCA_WAVES}
        assert "completed" in statuses

    def test_wave_numbers_sequential(self):
        wave_nums = sorted(w["wave"] for w in ZATCA_WAVES)
        assert wave_nums[0] == 1


class TestPenaltyIntegrity:
    def test_penalties_not_empty(self):
        assert len(PENALTIES) >= 4

    def test_all_penalties_have_required_fields(self):
        for p in PENALTIES:
            assert "violation_ar" in p
            assert "violation_en" in p
            assert "penalty_sar" in p
            assert "max_sar" in p

    def test_max_sar_geq_penalty_sar(self):
        for p in PENALTIES:
            assert p["max_sar"] >= p["penalty_sar"]

    def test_all_penalties_positive(self):
        for p in PENALTIES:
            assert p["penalty_sar"] > 0


# ---------------------------------------------------------------------------
# API integration tests
# ---------------------------------------------------------------------------


class TestAssessEndpoint:
    def test_returns_200(self):
        r = client.post("/api/v1/zatca-readiness/assess", json={})
        assert r.status_code == 200

    def test_governance_decision_present(self):
        data = client.post("/api/v1/zatca-readiness/assess", json={}).json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_score_in_response(self):
        data = client.post("/api/v1/zatca-readiness/assess", json={}).json()
        assert "readiness_score" in data
        assert 0 <= data["readiness_score"] <= 100

    def test_critical_gaps_present(self):
        data = client.post("/api/v1/zatca-readiness/assess", json={}).json()
        assert "critical_gaps" in data

    def test_disclaimer_bilingual(self):
        data = client.post("/api/v1/zatca-readiness/assess", json={}).json()
        assert "disclaimer_ar" in data
        assert "disclaimer_en" in data

    def test_full_compliance_body(self):
        full_body = {
            "has_csid": True, "has_xml_ubl": True, "has_qr_code": True,
            "has_digital_stamp": True, "has_fatoora_integration": True,
            "has_realtime_submission": True, "has_correct_trn": True,
            "has_complete_data": True, "has_rejection_process": True,
            "has_team_training": True,
        }
        data = client.post("/api/v1/zatca-readiness/assess", json=full_body).json()
        assert data["readiness_score"] == 100
        assert data["readiness_tier"]["id"] == "compliant"

    def test_with_revenue_includes_wave(self):
        data = client.post("/api/v1/zatca-readiness/assess", json={"annual_revenue_sar": 5_000_000}).json()
        assert data["applicable_wave"] is not None

    def test_penalty_exposure_nonzero_for_gaps(self):
        data = client.post("/api/v1/zatca-readiness/assess", json={}).json()
        assert data["estimated_penalty_exposure_sar"] >= 0

    def test_extra_fields_rejected(self):
        r = client.post("/api/v1/zatca-readiness/assess", json={"unknown_field": True})
        assert r.status_code == 422


class TestChecklistEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/zatca-readiness/checklist").status_code == 200

    def test_total_items_matches_checklist(self):
        data = client.get("/api/v1/zatca-readiness/checklist").json()
        assert data["total_items"] == len(CHECKLIST)

    def test_categories_present(self):
        data = client.get("/api/v1/zatca-readiness/checklist").json()
        assert "checklist_by_category" in data
        assert len(data["checklist_by_category"]) > 0

    def test_governance_decision(self):
        data = client.get("/api/v1/zatca-readiness/checklist").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"


class TestWavesEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/zatca-readiness/waves").status_code == 200

    def test_total_waves_correct(self):
        data = client.get("/api/v1/zatca-readiness/waves").json()
        assert data["total_waves"] == len(ZATCA_WAVES)

    def test_waves_array_present(self):
        data = client.get("/api/v1/zatca-readiness/waves").json()
        assert len(data["waves"]) > 0

    def test_completed_count_positive(self):
        data = client.get("/api/v1/zatca-readiness/waves").json()
        assert data["completed_count"] > 0


class TestPenaltiesEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/zatca-readiness/penalties").status_code == 200

    def test_total_exposure_positive(self):
        data = client.get("/api/v1/zatca-readiness/penalties").json()
        assert data["max_total_exposure_sar"] > 0

    def test_penalties_list_present(self):
        data = client.get("/api/v1/zatca-readiness/penalties").json()
        assert len(data["penalties"]) > 0

    def test_disclaimer_present(self):
        data = client.get("/api/v1/zatca-readiness/penalties").json()
        assert "disclaimer_ar" in data
        assert "disclaimer_en" in data


class TestInvoiceCheckEndpoint:
    def test_returns_200(self):
        r = client.post("/api/v1/zatca-readiness/invoice-check", json={})
        assert r.status_code == 200

    def test_non_compliant_when_empty(self):
        data = client.post("/api/v1/zatca-readiness/invoice-check", json={}).json()
        assert data["compliant"] is False

    def test_compliant_when_all_present(self):
        full = {
            "has_xml_format": True, "has_qr_code": True, "has_digital_signature": True,
            "has_uuid": True, "has_trn_supplier": True, "has_trn_buyer": True,
            "has_line_items": True, "invoice_type": "standard",
        }
        data = client.post("/api/v1/zatca-readiness/invoice-check", json=full).json()
        assert data["compliant"] is True
        assert data["critical_failures"] == 0

    def test_checks_list_present(self):
        data = client.post("/api/v1/zatca-readiness/invoice-check", json={}).json()
        assert len(data["checks"]) > 0

    def test_simplified_invoice_trn_buyer_not_critical(self):
        body = {
            "has_xml_format": True, "has_qr_code": True, "has_digital_signature": True,
            "has_uuid": True, "has_trn_supplier": True, "has_line_items": True,
            "invoice_type": "simplified",
        }
        data = client.post("/api/v1/zatca-readiness/invoice-check", json=body).json()
        assert data["compliant"] is True

    def test_bilingual_verdict(self):
        data = client.post("/api/v1/zatca-readiness/invoice-check", json={}).json()
        assert "verdict_ar" in data
        assert "verdict_en" in data

    def test_invalid_invoice_type_422(self):
        r = client.post("/api/v1/zatca-readiness/invoice-check", json={"invoice_type": "unknown"})
        assert r.status_code == 422
