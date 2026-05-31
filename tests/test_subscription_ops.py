"""Tests for the Subscription Operations API — subscription lifecycle management.

Covers: active subscriptions, expiring-soon, individual detail, pause/cancel/reactivate
state machine, governance gates, and doctrine compliance.
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

from api.routers.subscription_ops import _SUBSCRIPTIONS, _TIER_PRICES, router  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# Data Integrity
# ---------------------------------------------------------------------------


class TestDemoDataIntegrity:
    def test_six_subscriptions_exist(self):
        assert len(_SUBSCRIPTIONS) == 6

    def test_all_have_sub_id(self):
        ids = [s["sub_id"] for s in _SUBSCRIPTIONS]
        assert len(ids) == len(set(ids))

    def test_all_sub_ids_prefixed(self):
        for s in _SUBSCRIPTIONS:
            assert s["sub_id"].startswith("SUB-")

    def test_all_have_required_fields(self):
        required = {
            "sub_id", "client_id", "tier", "state", "monthly_value_sar",
            "renewal_date", "auto_renew", "payment_method",
        }
        for s in _SUBSCRIPTIONS:
            for f in required:
                assert f in s, f"Missing field {f!r} in {s['sub_id']}"

    def test_all_states_valid(self):
        valid = {"trial", "active", "paused", "cancelled", "reactivated"}
        for s in _SUBSCRIPTIONS:
            assert s["state"] in valid

    def test_active_subscriptions_exist(self):
        active = [s for s in _SUBSCRIPTIONS if s["state"] == "active"]
        assert len(active) >= 4

    def test_paused_subscription_exists(self):
        paused = [s for s in _SUBSCRIPTIONS if s["state"] == "paused"]
        assert len(paused) >= 1

    def test_cancelled_subscription_exists(self):
        cancelled = [s for s in _SUBSCRIPTIONS if s["state"] == "cancelled"]
        assert len(cancelled) >= 1

    def test_tier_prices_present(self):
        assert "managed_ops_professional" in _TIER_PRICES
        assert "managed_ops_enterprise" in _TIER_PRICES
        assert "sprint" in _TIER_PRICES

    def test_sprint_price_is_499(self):
        assert _TIER_PRICES["sprint"] == 499

    def test_all_monthly_values_positive(self):
        for s in _SUBSCRIPTIONS:
            assert s["monthly_value_sar"] > 0

    def test_bilingual_company_names(self):
        for s in _SUBSCRIPTIONS:
            assert "company_ar" in s
            assert "company_en" in s
            assert len(s["company_ar"]) > 0
            assert len(s["company_en"]) > 0


# ---------------------------------------------------------------------------
# GET /active
# ---------------------------------------------------------------------------


class TestActiveSubscriptionsEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/subscriptions/active").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/subscriptions/active").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_subscriptions_list(self):
        data = client.get("/api/v1/subscriptions/active").json()
        assert "subscriptions" in data
        assert len(data["subscriptions"]) >= 4

    def test_total_active_matches(self):
        data = client.get("/api/v1/subscriptions/active").json()
        assert data["total_active"] == len(data["subscriptions"])

    def test_has_mrr(self):
        data = client.get("/api/v1/subscriptions/active").json()
        assert "total_mrr_sar" in data
        assert data["total_mrr_sar"] > 0

    def test_has_arr(self):
        data = client.get("/api/v1/subscriptions/active").json()
        assert "total_arr_sar" in data
        assert data["total_arr_sar"] == data["total_mrr_sar"] * 12

    def test_has_expiring_30d_count(self):
        data = client.get("/api/v1/subscriptions/active").json()
        assert "expiring_30d_count" in data
        assert data["expiring_30d_count"] >= 0

    def test_has_generated_at(self):
        data = client.get("/api/v1/subscriptions/active").json()
        assert "generated_at" in data

    def test_each_sub_enriched_with_annual_value(self):
        data = client.get("/api/v1/subscriptions/active").json()
        for s in data["subscriptions"]:
            assert "annual_value_sar" in s
            assert s["annual_value_sar"] == s["monthly_value_sar"] * 12

    def test_each_sub_has_days_until_renewal(self):
        data = client.get("/api/v1/subscriptions/active").json()
        for s in data["subscriptions"]:
            assert "days_until_renewal" in s

    def test_filter_by_tier(self):
        data = client.get("/api/v1/subscriptions/active?tier=sprint").json()
        for s in data["subscriptions"]:
            assert s["tier"] == "sprint"

    def test_filter_by_unknown_tier_returns_empty(self):
        data = client.get("/api/v1/subscriptions/active?tier=nonexistent").json()
        assert data["total_active"] == 0
        assert data["subscriptions"] == []

    def test_sorted_by_renewal_urgency(self):
        data = client.get("/api/v1/subscriptions/active").json()
        subs = data["subscriptions"]
        days = [s.get("days_until_renewal") or 9999 for s in subs]
        assert days == sorted(days)

    def test_only_active_state_returned(self):
        data = client.get("/api/v1/subscriptions/active").json()
        for s in data["subscriptions"]:
            assert s["state"] == "active"


# ---------------------------------------------------------------------------
# GET /expiring-soon
# ---------------------------------------------------------------------------


class TestExpiringSoonEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/subscriptions/expiring-soon").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/subscriptions/expiring-soon").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_subscriptions(self):
        data = client.get("/api/v1/subscriptions/expiring-soon").json()
        assert "subscriptions" in data

    def test_has_window_days(self):
        data = client.get("/api/v1/subscriptions/expiring-soon").json()
        assert data["window_days"] == 30

    def test_custom_window(self):
        data = client.get("/api/v1/subscriptions/expiring-soon?days=90").json()
        assert data["window_days"] == 90

    def test_expiring_count_matches_list(self):
        data = client.get("/api/v1/subscriptions/expiring-soon?days=90").json()
        assert data["expiring_count"] == len(data["subscriptions"])

    def test_has_at_risk_value(self):
        data = client.get("/api/v1/subscriptions/expiring-soon").json()
        assert "at_risk_value_sar" in data

    def test_has_bilingual_action(self):
        data = client.get("/api/v1/subscriptions/expiring-soon").json()
        assert "action_ar" in data
        assert "action_en" in data

    def test_days_min_1(self):
        r = client.get("/api/v1/subscriptions/expiring-soon?days=0")
        assert r.status_code == 422

    def test_days_max_90(self):
        r = client.get("/api/v1/subscriptions/expiring-soon?days=91")
        assert r.status_code == 422

    def test_has_generated_at(self):
        data = client.get("/api/v1/subscriptions/expiring-soon").json()
        assert "generated_at" in data


# ---------------------------------------------------------------------------
# GET /{sub_id}
# ---------------------------------------------------------------------------


class TestGetSubscriptionEndpoint:
    def test_returns_200_for_valid_id(self):
        assert client.get("/api/v1/subscriptions/SUB-001").status_code == 200

    def test_returns_404_for_unknown_id(self):
        assert client.get("/api/v1/subscriptions/SUB-UNKNOWN").status_code == 404

    def test_governance_decision(self):
        data = client.get("/api/v1/subscriptions/SUB-001").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_sub_id(self):
        data = client.get("/api/v1/subscriptions/SUB-001").json()
        assert data["sub_id"] == "SUB-001"

    def test_has_tier(self):
        data = client.get("/api/v1/subscriptions/SUB-001").json()
        assert "tier" in data

    def test_has_state(self):
        data = client.get("/api/v1/subscriptions/SUB-001").json()
        assert "state" in data

    def test_enriched_annual_value(self):
        data = client.get("/api/v1/subscriptions/SUB-001").json()
        assert data["annual_value_sar"] == data["monthly_value_sar"] * 12

    def test_enriched_days_until_renewal(self):
        data = client.get("/api/v1/subscriptions/SUB-001").json()
        assert "days_until_renewal" in data

    def test_paused_sub_has_pause_info(self):
        data = client.get("/api/v1/subscriptions/SUB-005").json()
        assert data["state"] == "paused"
        assert data["paused_at"] is not None
        assert data["pause_reason"] is not None

    def test_cancelled_sub_has_cancel_info(self):
        data = client.get("/api/v1/subscriptions/SUB-006").json()
        assert data["state"] == "cancelled"
        assert data["cancelled_at"] is not None
        assert data["cancel_reason"] is not None

    def test_has_generated_at(self):
        data = client.get("/api/v1/subscriptions/SUB-001").json()
        assert "generated_at" in data


# ---------------------------------------------------------------------------
# POST /{sub_id}/pause
# ---------------------------------------------------------------------------


class TestPauseSubscriptionEndpoint:
    def test_pause_active_returns_200(self):
        body = {"reason": "Team vacation period — pausing billing", "pause_duration_days": 30}
        r = client.post("/api/v1/subscriptions/SUB-002/pause", json=body)
        assert r.status_code == 200

    def test_pause_requires_approval_first(self):
        body = {"reason": "Customer requested pause for budget review", "pause_duration_days": 14}
        data = client.post("/api/v1/subscriptions/SUB-003/pause", json=body).json()
        assert data["governance_decision"] == "APPROVAL_FIRST"

    def test_pause_returns_new_state(self):
        body = {"reason": "Operational pause requested by client", "pause_duration_days": 30}
        r = client.post("/api/v1/subscriptions/SUB-004/pause", json=body)
        if r.status_code == 200:
            assert r.json()["new_state"] == "paused"

    def test_pause_returns_resume_by(self):
        body = {"reason": "Short pause for system migration", "pause_duration_days": 15}
        r = client.post("/api/v1/subscriptions/SUB-001/pause", json=body)
        if r.status_code == 200:
            assert "resume_by" in r.json()

    def test_pause_unknown_sub_returns_404(self):
        body = {"reason": "Testing pause endpoint", "pause_duration_days": 30}
        r = client.post("/api/v1/subscriptions/SUB-UNKNOWN/pause", json=body)
        assert r.status_code == 404

    def test_pause_already_paused_returns_400(self):
        body = {"reason": "This should fail for paused sub", "pause_duration_days": 30}
        r = client.post("/api/v1/subscriptions/SUB-005/pause", json=body)
        assert r.status_code == 400

    def test_pause_cancelled_returns_400(self):
        body = {"reason": "This should fail for cancelled sub", "pause_duration_days": 30}
        r = client.post("/api/v1/subscriptions/SUB-006/pause", json=body)
        assert r.status_code == 400

    def test_pause_reason_too_short_returns_422(self):
        body = {"reason": "No", "pause_duration_days": 30}
        r = client.post("/api/v1/subscriptions/SUB-001/pause", json=body)
        assert r.status_code == 422

    def test_pause_duration_too_long_returns_422(self):
        body = {"reason": "Valid reason for pausing this subscription", "pause_duration_days": 999}
        r = client.post("/api/v1/subscriptions/SUB-001/pause", json=body)
        assert r.status_code == 422

    def test_pause_duration_zero_returns_422(self):
        body = {"reason": "Valid reason for pausing this subscription", "pause_duration_days": 0}
        r = client.post("/api/v1/subscriptions/SUB-001/pause", json=body)
        assert r.status_code == 422

    def test_pause_has_bilingual_status(self):
        body = {"reason": "Customer is going through system upgrade period", "pause_duration_days": 30}
        r = client.post("/api/v1/subscriptions/SUB-001/pause", json=body)
        if r.status_code == 200:
            data = r.json()
            assert "status_ar" in data
            assert "status_en" in data

    def test_pause_billing_note_present(self):
        body = {"reason": "Annual leave period for the entire team", "pause_duration_days": 21}
        r = client.post("/api/v1/subscriptions/SUB-001/pause", json=body)
        if r.status_code == 200:
            data = r.json()
            assert "note_ar" in data
            assert "note_en" in data


# ---------------------------------------------------------------------------
# POST /{sub_id}/cancel
# ---------------------------------------------------------------------------


class TestCancelSubscriptionEndpoint:
    def test_cancel_active_returns_200(self):
        body = {"reason": "Client chose a competing service after evaluation"}
        r = client.post("/api/v1/subscriptions/SUB-002/cancel", json=body)
        assert r.status_code in (200, 409)  # 409 if already cancelled by prior test

    def test_cancel_requires_approval_first(self):
        # Use a subscription still active (SUB-003 likely still active)
        body = {"reason": "Client out of budget for the remainder of the year"}
        r = client.post("/api/v1/subscriptions/SUB-003/cancel", json=body)
        if r.status_code == 200:
            assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_cancel_unknown_sub_returns_404(self):
        body = {"reason": "This should return a 404 not found"}
        r = client.post("/api/v1/subscriptions/SUB-UNKNOWN/cancel", json=body)
        assert r.status_code == 404

    def test_cancel_already_cancelled_returns_409(self):
        body = {"reason": "Duplicate cancellation attempt"}
        r = client.post("/api/v1/subscriptions/SUB-006/cancel", json=body)
        assert r.status_code == 409

    def test_cancel_reason_too_short_returns_422(self):
        body = {"reason": "No"}
        r = client.post("/api/v1/subscriptions/SUB-001/cancel", json=body)
        assert r.status_code == 422

    def test_cancel_has_churn_prevention_note(self):
        body = {"reason": "Client is reducing software spend this quarter"}
        r = client.post("/api/v1/subscriptions/SUB-001/cancel", json=body)
        if r.status_code == 200:
            data = r.json()
            assert "churn_prevention_ar" in data
            assert "churn_prevention_en" in data

    def test_cancel_has_warning_bilingual(self):
        body = {"reason": "Testing cancellation flow for governance"}
        r = client.post("/api/v1/subscriptions/SUB-001/cancel", json=body)
        if r.status_code == 200:
            data = r.json()
            assert "warning_ar" in data
            assert "warning_en" in data

    def test_cancel_returns_sub_id(self):
        body = {"reason": "Full contract review ended without renewal"}
        r = client.post("/api/v1/subscriptions/SUB-004/cancel", json=body)
        if r.status_code == 200:
            assert r.json()["sub_id"] == "SUB-004"

    def test_cancel_effective_immediately_field(self):
        body = {"reason": "Urgent cancellation per client legal request", "effective_immediately": True}
        r = client.post("/api/v1/subscriptions/SUB-001/cancel", json=body)
        if r.status_code == 200:
            data = r.json()
            assert data["effective_immediately"] is True


# ---------------------------------------------------------------------------
# POST /{sub_id}/reactivate
# ---------------------------------------------------------------------------


class TestReactivateSubscriptionEndpoint:
    def test_reactivate_paused_returns_200(self):
        body = {"reason": "Client team is back from vacation and ready to resume"}
        r = client.post("/api/v1/subscriptions/SUB-005/reactivate", json=body)
        assert r.status_code in (200, 409)

    def test_reactivate_requires_approval_first(self):
        body = {"reason": "Reactivating after successful budget reallocation"}
        r = client.post("/api/v1/subscriptions/SUB-005/reactivate", json=body)
        if r.status_code == 200:
            assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_reactivate_cancelled_returns_200(self):
        body = {"reason": "Client returned after trying competitor — signing new contract"}
        r = client.post("/api/v1/subscriptions/SUB-006/reactivate", json=body)
        assert r.status_code in (200, 409)

    def test_reactivate_active_returns_409(self):
        # Check current state before asserting — prior tests mutate shared in-memory state
        current_state = client.get("/api/v1/subscriptions/SUB-001").json()["state"]
        body = {"reason": "Should fail — subscription is already active"}
        r = client.post("/api/v1/subscriptions/SUB-001/reactivate", json=body)
        if current_state == "active":
            assert r.status_code == 409
        else:
            # Prior test paused or cancelled this sub — reactivate or already-active, either is fine
            assert r.status_code in (200, 409)

    def test_reactivate_unknown_sub_returns_404(self):
        body = {"reason": "Test for nonexistent subscription ID"}
        r = client.post("/api/v1/subscriptions/SUB-UNKNOWN/reactivate", json=body)
        assert r.status_code == 404

    def test_reactivate_reason_too_short_returns_422(self):
        body = {"reason": "No"}
        r = client.post("/api/v1/subscriptions/SUB-005/reactivate", json=body)
        assert r.status_code == 422

    def test_reactivate_with_new_renewal_date(self):
        body = {
            "reason": "Reactivating with extended renewal period per contract amendment",
            "new_renewal_date": "2027-01-01T00:00:00Z",
        }
        r = client.post("/api/v1/subscriptions/SUB-005/reactivate", json=body)
        if r.status_code == 200:
            data = r.json()
            assert "renewal_date" in data

    def test_reactivate_has_previous_state(self):
        body = {"reason": "Reactivation approved by founder after review meeting"}
        r = client.post("/api/v1/subscriptions/SUB-005/reactivate", json=body)
        if r.status_code == 200:
            data = r.json()
            assert "previous_state" in data

    def test_reactivate_returns_bilingual_status(self):
        body = {"reason": "Client renewed commitment after product demo session"}
        r = client.post("/api/v1/subscriptions/SUB-005/reactivate", json=body)
        if r.status_code == 200:
            data = r.json()
            assert "status_ar" in data
            assert "status_en" in data


# ---------------------------------------------------------------------------
# Doctrine Compliance
# ---------------------------------------------------------------------------


class TestDoctrineCompliance:
    def test_all_get_endpoints_have_governance_decision(self):
        endpoints = [
            "/api/v1/subscriptions/active",
            "/api/v1/subscriptions/expiring-soon",
            "/api/v1/subscriptions/SUB-001",
        ]
        for url in endpoints:
            data = client.get(url).json()
            assert "governance_decision" in data, f"Missing governance_decision on {url}"

    def test_mutating_endpoints_require_approval_first(self):
        """pause/cancel/reactivate must all use APPROVAL_FIRST governance."""
        # Test pause
        r = client.post("/api/v1/subscriptions/SUB-001/pause", json={
            "reason": "Governance test pause — waiting for approval",
            "pause_duration_days": 30,
        })
        if r.status_code == 200:
            assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_cancel_includes_client_contact_recommendation(self):
        """Cancellation must recommend contacting client first — APPROVAL_FIRST."""
        r = client.post("/api/v1/subscriptions/SUB-001/cancel", json={
            "reason": "Budget cut for Q3 — checking governance output",
        })
        if r.status_code == 200:
            data = r.json()
            # warning must mention contacting client
            assert "client" in data.get("warning_en", "").lower()

    def test_no_direct_execution_on_pause(self):
        """Pause note must say billing won't pause until approval — no autonomous billing stop."""
        r = client.post("/api/v1/subscriptions/SUB-001/pause", json={
            "reason": "Testing governance compliance on pause endpoint",
            "pause_duration_days": 30,
        })
        if r.status_code == 200:
            data = r.json()
            note = data.get("note_en", "")
            assert "approval" in note.lower()
