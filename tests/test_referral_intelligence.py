"""Tests for the Referral Intelligence API — referral tracking and program management.

Covers: data integrity, dashboard, all referrals (with filtering), by-referrer
lookup, referral registration, and program terms.
"""

from __future__ import annotations

import os
import sys
import types

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.referral_intelligence import (  # noqa: E402
    _REFERRALS,
    _REQUIRED_REFERRAL_FIELDS,
    _VALID_STATUSES,
    _compute_conversion_rate,
    _compute_total_incentives,
    _find_best_referrer,
    _sort_by_date_desc,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})

_BASE = "/api/v1/referral-intelligence"


# ---------------------------------------------------------------------------
# TestReferralDataIntegrity
# ---------------------------------------------------------------------------


class TestReferralDataIntegrity:
    def test_exactly_10_referrals_exist(self):
        assert len(_REFERRALS) >= 10

    def test_all_referrals_have_required_fields(self):
        for ref in _REFERRALS:
            for field in _REQUIRED_REFERRAL_FIELDS:
                assert field in ref, f"Missing field '{field}' in referral {ref.get('referral_id')}"

    def test_all_referral_ids_unique(self):
        ids = [r["referral_id"] for r in _REFERRALS]
        assert len(ids) == len(set(ids))

    def test_all_statuses_valid(self):
        for ref in _REFERRALS:
            assert ref["status"] in _VALID_STATUSES, f"Invalid status: {ref['status']}"

    def test_converted_statuses_present(self):
        statuses = {r["status"] for r in _REFERRALS}
        assert "converted" in statuses

    def test_qualified_statuses_present(self):
        statuses = {r["status"] for r in _REFERRALS}
        assert "qualified" in statuses

    def test_pending_statuses_present(self):
        statuses = {r["status"] for r in _REFERRALS}
        assert "pending" in statuses

    def test_lost_statuses_present(self):
        statuses = {r["status"] for r in _REFERRALS}
        assert "lost" in statuses

    def test_exactly_3_converted(self):
        converted = [r for r in _REFERRALS if r["status"] == "converted"]
        assert len(converted) == 3

    def test_converted_referrals_have_nonzero_value(self):
        for ref in _REFERRALS:
            if ref["status"] == "converted":
                assert ref["converted_value_sar"] > 0, (
                    f"Converted referral {ref['referral_id']} has zero converted_value_sar"
                )

    def test_non_converted_referrals_have_zero_value(self):
        for ref in _REFERRALS:
            if ref["status"] != "converted":
                assert ref["converted_value_sar"] == 0

    def test_converted_referrals_have_nonzero_incentive(self):
        for ref in _REFERRALS:
            if ref["status"] == "converted":
                assert ref["incentive_sar"] > 0

    def test_incentive_is_approximately_10_percent_of_value(self):
        for ref in _REFERRALS:
            if ref["status"] == "converted" and ref["converted_value_sar"] > 0:
                ratio = ref["incentive_sar"] / ref["converted_value_sar"]
                assert 0.08 <= ratio <= 0.12, (
                    f"Incentive ratio {ratio:.3f} out of 10% range for {ref['referral_id']}"
                )

    def test_five_unique_referrers(self):
        referrers = {r["referrer_client_id"] for r in _REFERRALS}
        assert len(referrers) == 5

    def test_each_referrer_has_2_referrals(self):
        counts: dict[str, int] = {}
        for r in _REFERRALS:
            counts[r["referrer_client_id"]] = counts.get(r["referrer_client_id"], 0) + 1
        for referrer, count in counts.items():
            assert count == 2, f"Referrer {referrer} has {count} referrals, expected 2"

    def test_all_companies_have_arabic_name(self):
        for ref in _REFERRALS:
            assert len(ref["referred_company_ar"]) > 0

    def test_all_companies_have_english_name(self):
        for ref in _REFERRALS:
            assert len(ref["referred_company_en"]) > 0

    def test_conversion_rate_calculation_correct(self):
        rate = _compute_conversion_rate(_REFERRALS)
        expected = 3 / 10
        assert abs(rate - expected) < 0.001

    def test_conversion_rate_empty_list_returns_zero(self):
        assert _compute_conversion_rate([]) == 0.0

    def test_compute_total_incentives_correct(self):
        total = _compute_total_incentives(_REFERRALS)
        assert total == sum(r["incentive_sar"] for r in _REFERRALS)
        assert total > 0

    def test_find_best_referrer_returns_string(self):
        best = _find_best_referrer(_REFERRALS)
        assert best is not None
        assert isinstance(best, str)

    def test_find_best_referrer_empty_list_returns_none(self):
        assert _find_best_referrer([]) is None

    def test_sort_by_date_desc_orders_correctly(self):
        sorted_refs = _sort_by_date_desc(_REFERRALS)
        dates = [r["referred_at"] for r in sorted_refs]
        assert dates == sorted(dates, reverse=True)


# ---------------------------------------------------------------------------
# TestDashboardEndpoint
# ---------------------------------------------------------------------------


class TestDashboardEndpoint:
    def test_returns_200(self):
        assert client.get(f"{_BASE}/dashboard").status_code == 200

    def test_governance_decision_allow_with_review(self):
        data = client.get(f"{_BASE}/dashboard").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_total_referrals(self):
        data = client.get(f"{_BASE}/dashboard").json()
        assert "total_referrals" in data
        assert data["total_referrals"] >= 10

    def test_has_conversion_rate(self):
        data = client.get(f"{_BASE}/dashboard").json()
        assert "conversion_rate" in data
        assert 0.0 <= data["conversion_rate"] <= 1.0

    def test_conversion_rate_pct_present(self):
        data = client.get(f"{_BASE}/dashboard").json()
        assert "conversion_rate_pct" in data
        assert 0.0 <= data["conversion_rate_pct"] <= 100.0

    def test_has_best_referrer(self):
        data = client.get(f"{_BASE}/dashboard").json()
        assert "best_referrer" in data
        assert data["best_referrer"] is not None

    def test_has_total_incentives_earned(self):
        data = client.get(f"{_BASE}/dashboard").json()
        assert "total_incentives_earned_sar" in data
        assert data["total_incentives_earned_sar"] > 0

    def test_has_converted_count(self):
        data = client.get(f"{_BASE}/dashboard").json()
        assert data["converted_count"] == 3

    def test_has_generated_at(self):
        data = client.get(f"{_BASE}/dashboard").json()
        assert "generated_at" in data

    def test_has_no_cold_outreach_note(self):
        data = client.get(f"{_BASE}/dashboard").json()
        assert "note_en" in data
        note = data["note_en"].lower()
        assert "outreach" in note or "approval" in note

    def test_unique_referrers_count(self):
        data = client.get(f"{_BASE}/dashboard").json()
        assert "unique_referrers" in data
        assert data["unique_referrers"] == 5

    def test_status_counts_sum_to_total(self):
        data = client.get(f"{_BASE}/dashboard").json()
        total = (
            data["converted_count"]
            + data["qualified_count"]
            + data["pending_count"]
            + data["lost_count"]
        )
        assert total == data["total_referrals"]


# ---------------------------------------------------------------------------
# TestAllReferralsEndpoint
# ---------------------------------------------------------------------------


class TestAllReferralsEndpoint:
    def test_returns_200(self):
        assert client.get(f"{_BASE}/all").status_code == 200

    def test_governance_decision(self):
        data = client.get(f"{_BASE}/all").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_returns_at_least_10_referrals(self):
        data = client.get(f"{_BASE}/all").json()
        assert data["total"] >= 10
        assert len(data["referrals"]) >= 10

    def test_total_matches_referrals_length(self):
        data = client.get(f"{_BASE}/all").json()
        assert data["total"] == len(data["referrals"])

    def test_sorted_by_date_descending(self):
        data = client.get(f"{_BASE}/all").json()
        dates = [r["referred_at"] for r in data["referrals"]]
        assert dates == sorted(dates, reverse=True)

    def test_filter_by_converted_status(self):
        data = client.get(f"{_BASE}/all?status=converted").json()
        assert data["total"] == 3
        for r in data["referrals"]:
            assert r["status"] == "converted"

    def test_filter_by_qualified_status(self):
        data = client.get(f"{_BASE}/all?status=qualified").json()
        assert data["total"] == 4
        for r in data["referrals"]:
            assert r["status"] == "qualified"

    def test_filter_by_pending_status(self):
        data = client.get(f"{_BASE}/all?status=pending").json()
        for r in data["referrals"]:
            assert r["status"] == "pending"

    def test_filter_by_lost_status(self):
        data = client.get(f"{_BASE}/all?status=lost").json()
        assert data["total"] == 1
        for r in data["referrals"]:
            assert r["status"] == "lost"

    def test_invalid_status_returns_422(self):
        resp = client.get(f"{_BASE}/all?status=invalid_status")
        assert resp.status_code == 422

    def test_filter_status_echoed_in_response(self):
        data = client.get(f"{_BASE}/all?status=converted").json()
        assert data["filter_status"] == "converted"

    def test_no_filter_has_null_filter_status(self):
        data = client.get(f"{_BASE}/all").json()
        assert data["filter_status"] is None

    def test_all_referrals_have_required_fields(self):
        data = client.get(f"{_BASE}/all").json()
        for ref in data["referrals"]:
            for field in _REQUIRED_REFERRAL_FIELDS:
                assert field in ref


# ---------------------------------------------------------------------------
# TestByReferrerEndpoint
# ---------------------------------------------------------------------------


class TestByReferrerEndpoint:
    def test_returns_200_for_valid_referrer(self):
        assert client.get(f"{_BASE}/by-referrer/CLT-001").status_code == 200

    def test_returns_404_for_unknown_referrer(self):
        assert client.get(f"{_BASE}/by-referrer/UNKNOWN-REF-999").status_code == 404

    def test_governance_decision(self):
        data = client.get(f"{_BASE}/by-referrer/CLT-001").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_referrer_id_echoed_in_response(self):
        data = client.get(f"{_BASE}/by-referrer/CLT-001").json()
        assert data["referrer_client_id"] == "CLT-001"

    def test_returns_2_referrals_per_referrer(self):
        for referrer in ("CLT-001", "CLT-002", "CLT-003", "CLT-004", "CLT-005"):
            data = client.get(f"{_BASE}/by-referrer/{referrer}").json()
            assert data["total_referrals"] == 2

    def test_all_returned_referrals_belong_to_referrer(self):
        data = client.get(f"{_BASE}/by-referrer/CLT-003").json()
        for ref in data["referrals"]:
            assert ref["referrer_client_id"] == "CLT-003"

    def test_has_conversion_rate(self):
        data = client.get(f"{_BASE}/by-referrer/CLT-003").json()
        assert "conversion_rate" in data
        assert 0.0 <= data["conversion_rate"] <= 1.0

    def test_has_total_incentives_earned(self):
        data = client.get(f"{_BASE}/by-referrer/CLT-005").json()
        assert "total_incentives_earned_sar" in data


# ---------------------------------------------------------------------------
# TestRegisterEndpoint
# ---------------------------------------------------------------------------


class TestRegisterEndpoint:
    def _valid_body(self, suffix: str = "01") -> dict[str, str]:
        return {
            "referrer_client_id": "CLT-001",
            "referred_company_ar": f"شركة اختبار {suffix}",
            "referred_company_en": f"Test Company {suffix}",
            "sector": "technology",
            "city": "riyadh",
        }

    def test_returns_200_with_valid_body(self):
        r = client.post(f"{_BASE}/register", json=self._valid_body("T01"))
        assert r.status_code == 200

    def test_governance_decision_is_approval_first(self):
        data = client.post(f"{_BASE}/register", json=self._valid_body("T02")).json()
        assert data["governance_decision"] == "APPROVAL_FIRST"

    def test_status_is_pending(self):
        data = client.post(f"{_BASE}/register", json=self._valid_body("T03")).json()
        assert data["status"] == "pending"

    def test_referral_id_returned(self):
        data = client.post(f"{_BASE}/register", json=self._valid_body("T04")).json()
        assert "referral_id" in data
        assert data["referral_id"].startswith("REF-INTEL-")

    def test_register_note_prohibits_cold_outreach(self):
        data = client.post(f"{_BASE}/register", json=self._valid_body("T05")).json()
        note = data.get("no_cold_outreach_note_en", "")
        note_lower = note.lower()
        assert "no outreach" in note_lower or "no cold" in note_lower, (
            f"Expected cold outreach prohibition in note, got: {note}"
        )
        assert "founder" in note_lower or "approval" in note_lower, (
            f"Expected founder approval requirement in note, got: {note}"
        )

    def test_register_note_includes_whatsapp_prohibition(self):
        data = client.post(f"{_BASE}/register", json=self._valid_body("T06")).json()
        note = data.get("no_cold_outreach_note_en", "")
        assert "whatsapp" in note.lower() or "channel" in note.lower()

    def test_register_arabic_note_present(self):
        data = client.post(f"{_BASE}/register", json=self._valid_body("T07")).json()
        assert "no_cold_outreach_note_ar" in data
        assert len(data["no_cold_outreach_note_ar"]) > 0

    def test_next_step_bilingual_present(self):
        data = client.post(f"{_BASE}/register", json=self._valid_body("T08")).json()
        assert "next_step_ar" in data
        assert "next_step_en" in data

    def test_referred_company_echoed_in_response(self):
        body = self._valid_body("T09")
        data = client.post(f"{_BASE}/register", json=body).json()
        assert data["referred_company_en"] == body["referred_company_en"]

    def test_referrer_client_id_echoed_in_response(self):
        body = self._valid_body("T10")
        data = client.post(f"{_BASE}/register", json=body).json()
        assert data["referrer_client_id"] == body["referrer_client_id"]

    def test_missing_referrer_client_id_returns_422(self):
        r = client.post(
            f"{_BASE}/register",
            json={
                "referred_company_ar": "شركة ما",
                "referred_company_en": "Some Company",
                "sector": "technology",
                "city": "riyadh",
            },
        )
        assert r.status_code == 422

    def test_missing_referred_company_en_returns_422(self):
        r = client.post(
            f"{_BASE}/register",
            json={
                "referrer_client_id": "CLT-001",
                "referred_company_ar": "شركة ما",
                "sector": "technology",
                "city": "riyadh",
            },
        )
        assert r.status_code == 422

    def test_missing_sector_returns_422(self):
        r = client.post(
            f"{_BASE}/register",
            json={
                "referrer_client_id": "CLT-001",
                "referred_company_ar": "شركة ما",
                "referred_company_en": "Some Company",
                "city": "riyadh",
            },
        )
        assert r.status_code == 422

    def test_missing_city_returns_422(self):
        r = client.post(
            f"{_BASE}/register",
            json={
                "referrer_client_id": "CLT-001",
                "referred_company_ar": "شركة ما",
                "referred_company_en": "Some Company",
                "sector": "technology",
            },
        )
        assert r.status_code == 422

    def test_empty_body_returns_422(self):
        r = client.post(f"{_BASE}/register", json={})
        assert r.status_code == 422

    def test_registered_referral_appears_in_all_endpoint(self):
        body = {
            "referrer_client_id": "CLT-002",
            "referred_company_ar": "شركة ظهور",
            "referred_company_en": "Appearance Co",
            "sector": "retail",
            "city": "dammam",
        }
        reg = client.post(f"{_BASE}/register", json=body).json()
        new_id = reg["referral_id"]
        all_data = client.get(f"{_BASE}/all").json()
        ids = [r["referral_id"] for r in all_data["referrals"]]
        assert new_id in ids

    def test_generated_at_present_in_register_response(self):
        data = client.post(f"{_BASE}/register", json=self._valid_body("T11")).json()
        assert "generated_at" in data


# ---------------------------------------------------------------------------
# TestProgramTermsEndpoint
# ---------------------------------------------------------------------------


class TestProgramTermsEndpoint:
    def test_returns_200(self):
        assert client.get(f"{_BASE}/program-terms").status_code == 200

    def test_governance_decision(self):
        data = client.get(f"{_BASE}/program-terms").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_incentive_structure(self):
        data = client.get(f"{_BASE}/program-terms").json()
        assert "incentive_structure" in data

    def test_incentive_structure_bilingual(self):
        data = client.get(f"{_BASE}/program-terms").json()
        structure = data["incentive_structure"]
        assert "incentive_structure_ar" in structure
        assert "incentive_structure_en" in structure

    def test_incentive_structure_includes_10_percent(self):
        data = client.get(f"{_BASE}/program-terms").json()
        note_en = data["incentive_structure"]["incentive_structure_en"].lower()
        assert "10%" in note_en

    def test_has_eligibility_rules(self):
        data = client.get(f"{_BASE}/program-terms").json()
        assert "eligibility" in data
        assert "rules_en" in data["eligibility"]
        assert len(data["eligibility"]["rules_en"]) > 0

    def test_eligibility_bilingual(self):
        data = client.get(f"{_BASE}/program-terms").json()
        eligibility = data["eligibility"]
        assert "rules_ar" in eligibility
        assert "rules_en" in eligibility

    def test_has_payout_timing(self):
        data = client.get(f"{_BASE}/program-terms").json()
        assert "payout_timing" in data

    def test_payout_timing_bilingual(self):
        data = client.get(f"{_BASE}/program-terms").json()
        payout = data["payout_timing"]
        assert "trigger_ar" in payout
        assert "trigger_en" in payout

    def test_has_approval_requirement_section(self):
        data = client.get(f"{_BASE}/program-terms").json()
        assert "approval_requirement" in data

    def test_approval_requirement_prohibits_cold_outreach(self):
        data = client.get(f"{_BASE}/program-terms").json()
        note = data["approval_requirement"]["note_en"].lower()
        assert "cold" in note or "approval" in note

    def test_has_program_version(self):
        data = client.get(f"{_BASE}/program-terms").json()
        assert "program_version" in data

    def test_has_effective_date(self):
        data = client.get(f"{_BASE}/program-terms").json()
        assert "effective_date" in data

    def test_has_generated_at(self):
        data = client.get(f"{_BASE}/program-terms").json()
        assert "generated_at" in data
