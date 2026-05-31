"""Tests for the retainer_ops API router.

Covers: listing active retainers, at-risk detection, renewal calendar,
MRR breakdown, full retainer detail, renewal processing, tier upgrades,
pause logic, proof update queuing, and governance decision presence.
"""

from __future__ import annotations

import os
import sys
import types
import unittest.mock as mock

import pytest

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

# ---------------------------------------------------------------------------
# Prevent the jose/cryptography pyo3 panic by stubbing the security module
# BEFORE anything that imports api.security is loaded.
# ---------------------------------------------------------------------------
_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None  # no-op dependency
sys.modules.setdefault("api.security.api_key", _mock_security)

# Also stub api.security itself if not yet loaded
if "api.security" not in sys.modules:
    _api_security = types.ModuleType("api.security")
    sys.modules["api.security"] = _api_security

from api.routers.retainer_ops import (  # noqa: E402
    TIER_PRICE,
    _RETAINERS,
    _days_until,
    _health_tier,
    _retainer_or_404,
    _status_label,
    _upgrade_path,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# Unit tests — pure helpers
# ---------------------------------------------------------------------------


class TestTierPricing:
    def test_essential_price(self):
        assert TIER_PRICE["essential"] == 2_999

    def test_professional_price(self):
        assert TIER_PRICE["professional"] == 3_999

    def test_enterprise_price(self):
        assert TIER_PRICE["enterprise"] == 4_999

    def test_all_tiers_present(self):
        assert set(TIER_PRICE.keys()) == {"essential", "professional", "enterprise"}


class TestHealthTier:
    def test_healthy_at_75(self):
        result = _health_tier(75)
        assert result["tier"] == "healthy"
        assert result["color"] == "green"

    def test_healthy_at_100(self):
        result = _health_tier(100)
        assert result["tier"] == "healthy"

    def test_moderate_at_60(self):
        result = _health_tier(60)
        assert result["tier"] == "moderate"
        assert result["color"] == "amber"

    def test_at_risk_at_40(self):
        result = _health_tier(40)
        assert result["tier"] == "at_risk"
        assert result["color"] == "orange"

    def test_critical_at_30(self):
        result = _health_tier(30)
        assert result["tier"] == "critical"
        assert result["color"] == "red"

    def test_boundary_55(self):
        result = _health_tier(55)
        assert result["tier"] == "moderate"

    def test_boundary_35(self):
        result = _health_tier(35)
        assert result["tier"] == "at_risk"


class TestStatusLabel:
    def test_active_bilingual(self):
        label = _status_label("active")
        assert label["ar"] == "نشط"
        assert label["en"] == "Active"

    def test_at_risk_bilingual(self):
        label = _status_label("at_risk")
        assert "خطر" in label["ar"]
        assert "Risk" in label["en"]

    def test_paused_bilingual(self):
        label = _status_label("paused")
        assert label["en"] == "Paused"

    def test_unknown_status_passthrough(self):
        label = _status_label("unknown_status")
        assert label["ar"] == "unknown_status"
        assert label["en"] == "unknown_status"


class TestUpgradePath:
    def test_essential_to_professional(self):
        path = _upgrade_path("essential")
        assert path is not None
        assert path["next_tier"] == "professional"
        assert path["delta_sar"] == 1_000

    def test_professional_to_enterprise(self):
        path = _upgrade_path("professional")
        assert path is not None
        assert path["next_tier"] == "enterprise"
        assert path["delta_sar"] == 1_000

    def test_enterprise_no_upgrade(self):
        path = _upgrade_path("enterprise")
        assert path is None

    def test_essential_upgrade_price(self):
        path = _upgrade_path("essential")
        assert path["current_sar"] == 2_999
        assert path["next_sar"] == 3_999


class TestDaysUntil:
    def test_future_date_positive(self):
        from datetime import date, timedelta
        future = (date.today() + timedelta(days=15)).isoformat()
        days = _days_until(future)
        assert days == 15

    def test_past_date_negative(self):
        from datetime import date, timedelta
        past = (date.today() - timedelta(days=5)).isoformat()
        days = _days_until(past)
        assert days == -5

    def test_invalid_date_returns_zero(self):
        days = _days_until("not-a-date")
        assert days == 0


class TestRetainerOrNotFound:
    def test_valid_id_found(self):
        r = _retainer_or_404("RTN-001")
        assert r["client_id"] == "RTN-001"

    def test_case_insensitive(self):
        r = _retainer_or_404("rtn-001")
        assert r["client_id"] == "RTN-001"

    def test_not_found_raises_404(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            _retainer_or_404("RTN-999")
        assert exc_info.value.status_code == 404

    def test_404_detail_bilingual(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            _retainer_or_404("RTN-999")
        detail = exc_info.value.detail
        assert "ar" in detail
        assert "en" in detail


# ---------------------------------------------------------------------------
# API integration tests
# ---------------------------------------------------------------------------


class TestListActiveRetainers:
    def test_returns_200(self):
        r = client.get("/api/v1/retainer/active")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/retainer/active")
        data = r.json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_summary_keys(self):
        data = client.get("/api/v1/retainer/active").json()
        summary = data["summary"]
        assert "total_active" in summary
        assert "monthly_mrr_sar" in summary
        assert "annual_arr_sar" in summary

    def test_retainers_list_non_empty(self):
        data = client.get("/api/v1/retainer/active").json()
        assert len(data["retainers"]) > 0

    def test_retainer_has_required_fields(self):
        data = client.get("/api/v1/retainer/active").json()
        r = data["retainers"][0]
        assert "client_id" in r
        assert "company" in r
        assert "health" in r
        assert "tier" in r
        assert "next_renewal" in r

    def test_arr_is_mrr_times_12(self):
        data = client.get("/api/v1/retainer/active").json()
        summary = data["summary"]
        assert summary["annual_arr_sar"] == summary["monthly_mrr_sar"] * 12

    def test_no_churned_in_active(self):
        data = client.get("/api/v1/retainer/active").json()
        for r in data["retainers"]:
            assert r["status"]["id"] != "churned"


class TestAtRiskRetainers:
    def test_returns_200(self):
        r = client.get("/api/v1/retainer/at-risk")
        assert r.status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/retainer/at-risk").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_at_risk_have_low_health(self):
        data = client.get("/api/v1/retainer/at-risk").json()
        for intervention in data["interventions"]:
            assert intervention["health_score"] < 60

    def test_interventions_have_recommended_action(self):
        data = client.get("/api/v1/retainer/at-risk").json()
        for intervention in data["interventions"]:
            assert "recommended_action_ar" in intervention
            assert "recommended_action_en" in intervention

    def test_revenue_at_risk_positive(self):
        data = client.get("/api/v1/retainer/at-risk").json()
        assert data["revenue_at_risk_sar"] >= 0

    def test_urgency_field_valid_values(self):
        data = client.get("/api/v1/retainer/at-risk").json()
        valid_urgencies = {"critical", "high", "medium"}
        for intervention in data["interventions"]:
            assert intervention["urgency"] in valid_urgencies


class TestRenewalCalendar:
    def test_returns_200(self):
        r = client.get("/api/v1/retainer/renewal-calendar")
        assert r.status_code == 200

    def test_default_days_ahead_30(self):
        data = client.get("/api/v1/retainer/renewal-calendar").json()
        assert data["days_ahead"] == 30

    def test_custom_days_ahead(self):
        data = client.get("/api/v1/retainer/renewal-calendar?days_ahead=60").json()
        assert data["days_ahead"] == 60

    def test_renewals_structure(self):
        data = client.get("/api/v1/retainer/renewal-calendar").json()
        for r in data.get("renewals", []):
            assert "client_id" in r
            assert "renewal_date" in r
            assert "days_until" in r
            assert "renewal_risk" in r

    def test_governance_decision(self):
        data = client.get("/api/v1/retainer/renewal-calendar").json()
        assert "governance_decision" in data


class TestMRRBreakdown:
    def test_returns_200(self):
        r = client.get("/api/v1/retainer/mrr-breakdown")
        assert r.status_code == 200

    def test_has_total_mrr(self):
        data = client.get("/api/v1/retainer/mrr-breakdown").json()
        assert data["total_mrr_sar"] > 0

    def test_arr_is_mrr_times_12(self):
        data = client.get("/api/v1/retainer/mrr-breakdown").json()
        assert data["total_arr_sar"] == data["total_mrr_sar"] * 12

    def test_by_tier_present(self):
        data = client.get("/api/v1/retainer/mrr-breakdown").json()
        assert "by_tier" in data
        assert len(data["by_tier"]) > 0

    def test_by_sector_present(self):
        data = client.get("/api/v1/retainer/mrr-breakdown").json()
        assert "by_sector" in data

    def test_target_progress_pct_reasonable(self):
        data = client.get("/api/v1/retainer/mrr-breakdown").json()
        pct = data["target_progress_pct"]
        assert 0 <= pct <= 200


class TestGetRetainer:
    def test_valid_client_200(self):
        r = client.get("/api/v1/retainer/RTN-001")
        assert r.status_code == 200

    def test_invalid_client_404(self):
        r = client.get("/api/v1/retainer/RTN-999")
        assert r.status_code == 404

    def test_response_structure(self):
        data = client.get("/api/v1/retainer/RTN-001").json()
        required = ["client_id", "company", "tier", "status", "health", "months_active", "arr_sar"]
        for field in required:
            assert field in data, f"Missing: {field}"

    def test_governance_decision(self):
        data = client.get("/api/v1/retainer/RTN-001").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_arr_equals_tier_price_times_12(self):
        data = client.get("/api/v1/retainer/RTN-001").json()
        tier_id = data["tier"]["id"]
        expected_arr = TIER_PRICE[tier_id] * 12
        assert data["arr_sar"] == expected_arr

    def test_bilingual_company_name(self):
        data = client.get("/api/v1/retainer/RTN-001").json()
        assert "ar" in data["company"]
        assert "en" in data["company"]


class TestRenewal:
    def test_pending_payment_when_not_confirmed(self):
        r = client.post("/api/v1/retainer/RTN-002/renew", json={"payment_confirmed": False})
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "pending_payment"

    def test_renewal_success_when_confirmed(self):
        r = client.post("/api/v1/retainer/RTN-002/renew", json={"payment_confirmed": True})
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "renewed"

    def test_renewal_updates_months_active(self):
        # Get starting months_active
        before = client.get("/api/v1/retainer/RTN-007").json()["months_active"]
        client.post("/api/v1/retainer/RTN-007/renew", json={"payment_confirmed": True})
        after = client.get("/api/v1/retainer/RTN-007").json()["months_active"]
        assert after == before + 1

    def test_renewal_404_for_unknown_client(self):
        r = client.post("/api/v1/retainer/RTN-999/renew", json={"payment_confirmed": True})
        assert r.status_code == 404


class TestUpgrade:
    def test_valid_upgrade_essential_to_professional(self):
        r = client.post("/api/v1/retainer/RTN-002/upgrade", json={"target_tier": "professional"})
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "upgrade_queued_for_approval"

    def test_upgrade_requires_approval_first(self):
        r = client.post("/api/v1/retainer/RTN-002/upgrade", json={"target_tier": "enterprise"})
        data = r.json()
        assert data["governance_decision"] == "APPROVAL_FIRST"

    def test_downgrade_returns_400(self):
        r = client.post("/api/v1/retainer/RTN-008/upgrade", json={"target_tier": "essential"})
        assert r.status_code == 400

    def test_same_tier_returns_400(self):
        r = client.post("/api/v1/retainer/RTN-008/upgrade", json={"target_tier": "enterprise"})
        assert r.status_code == 400


class TestPauseRetainer:
    def test_pause_active_retainer(self):
        r = client.post("/api/v1/retainer/RTN-004/pause", json={"reason": "Client going on vacation"})
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "paused"

    def test_pause_returns_expected_resume(self):
        r = client.post("/api/v1/retainer/RTN-006/pause", json={
            "reason": "Seasonal closure",
            "resume_date": "2026-07-01",
        })
        assert r.status_code == 200
        data = r.json()
        assert data["expected_resume"] == "2026-07-01"

    def test_pause_404_for_unknown(self):
        r = client.post("/api/v1/retainer/RTN-999/pause", json={"reason": "test pause reason"})
        assert r.status_code == 404


class TestProofUpdate:
    def test_queues_with_default_sections(self):
        r = client.post("/api/v1/retainer/RTN-001/proof-update", json={})
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "proof_update_queued"
        assert len(data["sections_to_update"]) == 4

    def test_requires_approval_first(self):
        data = client.post("/api/v1/retainer/RTN-001/proof-update", json={}).json()
        assert data["governance_decision"] == "APPROVAL_FIRST"

    def test_custom_sections_respected(self):
        r = client.post("/api/v1/retainer/RTN-001/proof-update", json={
            "sections": ["data_audit", "roi_projection"]
        })
        data = r.json()
        assert data["sections_to_update"] == ["data_audit", "roi_projection"]

    def test_estimated_hours_scales_with_sections(self):
        r = client.post("/api/v1/retainer/RTN-001/proof-update", json={
            "sections": ["data_audit"]
        })
        data = r.json()
        assert data["estimated_hours"] == 1.5


class TestDataIntegrity:
    def test_all_demo_retainers_have_valid_tiers(self):
        for client_id, r in _RETAINERS.items():
            assert r["tier"] in TIER_PRICE, f"Invalid tier for {client_id}"

    def test_all_demo_retainers_have_required_fields(self):
        required = ["client_id", "company_name_ar", "company_name_en", "sector", "city",
                    "tier", "status", "health_score", "next_renewal", "months_active"]
        for client_id, r in _RETAINERS.items():
            for field in required:
                assert field in r, f"Missing {field} in {client_id}"

    def test_health_scores_in_valid_range(self):
        for client_id, r in _RETAINERS.items():
            assert 0 <= r["health_score"] <= 100, f"Invalid health score for {client_id}"

    def test_at_least_one_at_risk_client(self):
        at_risk = [r for r in _RETAINERS.values() if r["health_score"] < 55]
        assert len(at_risk) >= 1

    def test_at_least_one_healthy_client(self):
        healthy = [r for r in _RETAINERS.values() if r["health_score"] >= 75]
        assert len(healthy) >= 1
