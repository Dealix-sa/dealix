"""Tests for /api/v1/client-portal — client portal operations.

Covers:
  - Demo data integrity (5 accounts, 5 deliverables)
  - GET /accounts (list, filters)
  - GET /accounts/{client_id} (single account, 404)
  - GET /accounts/{client_id}/deliverables (deliverables, 404 on missing client)
  - GET /summary (portfolio summary, field correctness)
  - POST /accounts/{client_id}/request-review (action endpoint, governance)
  - GET /upgrade-paths (recommendations, health threshold, tier logic)
  - Helper function unit tests (_filter_accounts, _compute_by_tier,
    _compute_portfolio_summary, _next_tier, _build_upgrade_paths, _now_iso,
    _client_or_404)
"""

from __future__ import annotations

import os
import sys
import types

import pytest

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

# ---------------------------------------------------------------------------
# Stub the security module only if the real one can't be imported.
# Using setdefault unconditionally contaminates the whole pytest session
# in CI (where jose/cryptography work) and breaks auth tests in other files.
# ---------------------------------------------------------------------------
if "api.security.api_key" not in sys.modules:
    try:
        import importlib
        importlib.import_module("api.security.api_key")
    except BaseException:
        _mock_security = types.ModuleType("api.security.api_key")
        _mock_security.require_admin_key = lambda: None
        sys.modules["api.security.api_key"] = _mock_security
        if "api.security" not in sys.modules:
            sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.client_portal_ops import (  # noqa: E402
    CLIENT_PORTALS,
    DELIVERABLES,
    _TIER_MRR,
    _TIER_ORDER,
    _UPGRADE_REASON,
    _build_upgrade_paths,
    _client_or_404,
    _compute_by_tier,
    _compute_portfolio_summary,
    _filter_accounts,
    _next_tier,
    _now_iso,
    router,
)
from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})

# ---------------------------------------------------------------------------
# Convenience: all accounts as a list
# ---------------------------------------------------------------------------
_ALL_ACCOUNTS = list(CLIENT_PORTALS.values())


# ===========================================================================
# 1. Demo data integrity
# ===========================================================================


class TestDemoDataIntegrity:
    def test_client_portals_has_5_entries(self) -> None:
        assert len(CLIENT_PORTALS) == 5

    def test_client_portal_ids_are_cp_001_to_cp_005(self) -> None:
        assert set(CLIENT_PORTALS.keys()) == {
            "CP-001", "CP-002", "CP-003", "CP-004", "CP-005"
        }

    def test_every_account_has_client_id(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert "client_id" in acc and acc["client_id"]

    def test_every_account_has_company_name(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert "company_name" in acc and acc["company_name"]

    def test_every_account_has_company_name_en(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert "company_name_en" in acc and acc["company_name_en"]

    def test_every_account_has_contact_name(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert "contact_name" in acc and acc["contact_name"]

    def test_every_account_has_contact_email(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert "contact_email" in acc
            assert "@" in acc["contact_email"]

    def test_every_account_has_valid_tier(self) -> None:
        valid_tiers = set(_TIER_ORDER)
        for acc in CLIENT_PORTALS.values():
            assert acc["tier"] in valid_tiers

    def test_every_account_has_mrr_sar(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert "mrr_sar" in acc
            assert isinstance(acc["mrr_sar"], float)
            assert acc["mrr_sar"] > 0

    def test_every_account_health_score_in_range(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert 0 <= acc["health_score"] <= 100

    def test_every_account_sprints_completed_non_negative(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert acc["sprints_completed"] >= 0

    def test_every_account_sprints_remaining_non_negative(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert acc["sprints_remaining"] >= 0

    def test_every_account_active_deliverables_is_list(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert isinstance(acc["active_deliverables"], list)

    def test_every_account_has_next_review_date(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert "next_review_date" in acc and acc["next_review_date"]

    def test_every_account_satisfaction_score_in_range(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert 0.0 <= acc["satisfaction_score"] <= 5.0

    def test_every_account_nps_in_range(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert 0 <= acc["nps"] <= 10

    def test_every_account_has_last_login(self) -> None:
        for acc in CLIENT_PORTALS.values():
            assert "last_login" in acc and acc["last_login"]

    def test_deliverables_has_5_entries(self) -> None:
        assert len(DELIVERABLES) == 5

    def test_deliverable_ids_are_dlv_001_to_005(self) -> None:
        assert set(DELIVERABLES.keys()) == {
            "DLV-001", "DLV-002", "DLV-003", "DLV-004", "DLV-005"
        }

    def test_every_deliverable_has_id(self) -> None:
        for dlv in DELIVERABLES.values():
            assert "id" in dlv and dlv["id"]

    def test_every_deliverable_has_client_id(self) -> None:
        for dlv in DELIVERABLES.values():
            assert "client_id" in dlv and dlv["client_id"]

    def test_every_deliverable_has_name(self) -> None:
        for dlv in DELIVERABLES.values():
            assert "name" in dlv and dlv["name"]

    def test_every_deliverable_has_valid_status(self) -> None:
        valid = {"delivered", "in_progress", "planned"}
        for dlv in DELIVERABLES.values():
            assert dlv["status"] in valid

    def test_every_deliverable_has_due_date(self) -> None:
        for dlv in DELIVERABLES.values():
            assert "due_date" in dlv and dlv["due_date"]

    def test_delivered_deliverables_have_quality_score(self) -> None:
        for dlv in DELIVERABLES.values():
            if dlv["status"] == "delivered":
                assert dlv["quality_score"] is not None
                assert 0 <= dlv["quality_score"] <= 100

    def test_non_delivered_deliverables_have_null_quality_score(self) -> None:
        for dlv in DELIVERABLES.values():
            if dlv["status"] != "delivered":
                assert dlv["quality_score"] is None

    def test_cp001_deliverables_are_dlv_001_to_003(self) -> None:
        cp001_dlvs = [d for d in DELIVERABLES.values() if d["client_id"] == "CP-001"]
        assert len(cp001_dlvs) == 3

    def test_cp003_deliverables_are_dlv_004_and_005(self) -> None:
        cp003_dlvs = [d for d in DELIVERABLES.values() if d["client_id"] == "CP-003"]
        assert len(cp003_dlvs) == 2

    def test_tier_mrr_has_4_tiers(self) -> None:
        assert len(_TIER_MRR) == 4

    def test_tier_order_has_4_entries(self) -> None:
        assert len(_TIER_ORDER) == 4

    def test_tier_order_starts_with_sprint(self) -> None:
        assert _TIER_ORDER[0] == "sprint"

    def test_tier_order_ends_with_custom_ai(self) -> None:
        assert _TIER_ORDER[-1] == "custom_ai"


# ===========================================================================
# 2. GET /accounts — list accounts
# ===========================================================================


class TestListAccounts:
    def test_returns_200(self) -> None:
        resp = client.get("/api/v1/client-portal/accounts")
        assert resp.status_code == 200

    def test_governance_decision_present(self) -> None:
        body = client.get("/api/v1/client-portal/accounts").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self) -> None:
        body = client.get("/api/v1/client-portal/accounts").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_accounts_key_present(self) -> None:
        body = client.get("/api/v1/client-portal/accounts").json()
        assert "accounts" in body

    def test_accounts_is_list(self) -> None:
        body = client.get("/api/v1/client-portal/accounts").json()
        assert isinstance(body["accounts"], list)

    def test_returns_all_5_accounts_unfiltered(self) -> None:
        body = client.get("/api/v1/client-portal/accounts").json()
        assert body["total"] == 5
        assert len(body["accounts"]) == 5

    def test_total_field_matches_accounts_length(self) -> None:
        body = client.get("/api/v1/client-portal/accounts").json()
        assert body["total"] == len(body["accounts"])

    def test_generated_at_present(self) -> None:
        body = client.get("/api/v1/client-portal/accounts").json()
        assert "generated_at" in body

    def test_filter_by_tier_sprint(self) -> None:
        body = client.get("/api/v1/client-portal/accounts?tier=sprint").json()
        assert body["total"] == 1
        assert body["accounts"][0]["tier"] == "sprint"

    def test_filter_by_tier_data_pack(self) -> None:
        body = client.get("/api/v1/client-portal/accounts?tier=data_pack").json()
        assert body["total"] == 1
        assert body["accounts"][0]["tier"] == "data_pack"

    def test_filter_by_tier_managed_ops_returns_two(self) -> None:
        body = client.get("/api/v1/client-portal/accounts?tier=managed_ops").json()
        assert body["total"] == 2

    def test_filter_by_tier_custom_ai_returns_one(self) -> None:
        body = client.get("/api/v1/client-portal/accounts?tier=custom_ai").json()
        assert body["total"] == 1

    def test_filter_by_tier_nonexistent_returns_empty(self) -> None:
        body = client.get("/api/v1/client-portal/accounts?tier=enterprise").json()
        assert body["total"] == 0
        assert body["accounts"] == []

    def test_filter_by_min_health_80_returns_high_health(self) -> None:
        body = client.get("/api/v1/client-portal/accounts?min_health=80").json()
        for acc in body["accounts"]:
            assert acc["health_score"] >= 80

    def test_filter_by_min_health_90_returns_only_cp003(self) -> None:
        body = client.get("/api/v1/client-portal/accounts?min_health=90").json()
        assert body["total"] == 1
        assert body["accounts"][0]["client_id"] == "CP-003"

    def test_filter_by_min_health_100_returns_empty(self) -> None:
        body = client.get("/api/v1/client-portal/accounts?min_health=100").json()
        assert body["total"] == 0

    def test_filter_by_min_health_0_returns_all(self) -> None:
        body = client.get("/api/v1/client-portal/accounts?min_health=0").json()
        assert body["total"] == 5

    def test_combined_filter_tier_and_min_health(self) -> None:
        body = client.get(
            "/api/v1/client-portal/accounts?tier=managed_ops&min_health=85"
        ).json()
        # CP-001 managed_ops health_score=87, CP-005 managed_ops health_score=81
        assert body["total"] == 1
        assert body["accounts"][0]["client_id"] == "CP-001"

    def test_every_returned_account_has_client_id(self) -> None:
        body = client.get("/api/v1/client-portal/accounts").json()
        for acc in body["accounts"]:
            assert "client_id" in acc

    def test_every_returned_account_has_tier(self) -> None:
        body = client.get("/api/v1/client-portal/accounts").json()
        for acc in body["accounts"]:
            assert "tier" in acc

    def test_every_returned_account_has_health_score(self) -> None:
        body = client.get("/api/v1/client-portal/accounts").json()
        for acc in body["accounts"]:
            assert "health_score" in acc


# ===========================================================================
# 3. GET /accounts/{client_id} — single account
# ===========================================================================


class TestGetAccount:
    def test_cp001_returns_200(self) -> None:
        resp = client.get("/api/v1/client-portal/accounts/CP-001")
        assert resp.status_code == 200

    def test_governance_decision_present(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_client_id_matches(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert body["client_id"] == "CP-001"

    def test_company_name_is_arabic_string(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert body["company_name"] == "مجموعة الصحة الوطنية"

    def test_company_name_en_is_national_health_group(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert body["company_name_en"] == "National Health Group"

    def test_tier_is_managed_ops_for_cp001(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert body["tier"] == "managed_ops"

    def test_health_score_correct_for_cp001(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert body["health_score"] == 87

    def test_nps_correct_for_cp001(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert body["nps"] == 9

    def test_active_deliverables_is_list(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert isinstance(body["active_deliverables"], list)

    def test_active_deliverables_count_for_cp001(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert len(body["active_deliverables"]) == 3

    def test_cp003_tier_is_custom_ai(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-003").json()
        assert body["tier"] == "custom_ai"

    def test_cp004_health_score_is_58(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-004").json()
        assert body["health_score"] == 58

    def test_cp005_sprints_remaining_is_7(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-005").json()
        assert body["sprints_remaining"] == 7

    def test_unknown_client_returns_404(self) -> None:
        resp = client.get("/api/v1/client-portal/accounts/CP-999")
        assert resp.status_code == 404

    def test_unknown_client_404_detail_has_en_key(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-999").json()
        assert "en" in body["detail"]

    def test_unknown_client_404_detail_has_ar_key(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-999").json()
        assert "ar" in body["detail"]

    def test_generated_at_present(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001").json()
        assert "generated_at" in body


# ===========================================================================
# 4. GET /accounts/{client_id}/deliverables
# ===========================================================================


class TestGetClientDeliverables:
    def test_cp001_returns_200(self) -> None:
        resp = client.get("/api/v1/client-portal/accounts/CP-001/deliverables")
        assert resp.status_code == 200

    def test_governance_decision_present(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_cp001_has_3_deliverables(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        assert body["total"] == 3
        assert len(body["deliverables"]) == 3

    def test_cp003_has_2_deliverables(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-003/deliverables").json()
        assert body["total"] == 2

    def test_cp002_has_0_deliverables(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-002/deliverables").json()
        assert body["total"] == 0
        assert body["deliverables"] == []

    def test_client_id_in_response(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        assert body["client_id"] == "CP-001"

    def test_delivered_count_is_1_for_cp001(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        assert body["delivered_count"] == 1

    def test_in_progress_count_is_1_for_cp001(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        assert body["in_progress_count"] == 1

    def test_planned_count_is_1_for_cp001(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        assert body["planned_count"] == 1

    def test_all_deliverables_belong_to_client(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        for dlv in body["deliverables"]:
            assert dlv["client_id"] == "CP-001"

    def test_every_deliverable_has_id(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        for dlv in body["deliverables"]:
            assert "id" in dlv

    def test_every_deliverable_has_status(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        for dlv in body["deliverables"]:
            assert "status" in dlv

    def test_every_deliverable_has_due_date(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        for dlv in body["deliverables"]:
            assert "due_date" in dlv

    def test_missing_client_returns_404(self) -> None:
        resp = client.get("/api/v1/client-portal/accounts/CP-999/deliverables")
        assert resp.status_code == 404

    def test_generated_at_present(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-001/deliverables").json()
        assert "generated_at" in body

    def test_cp003_deliverables_all_delivered(self) -> None:
        body = client.get("/api/v1/client-portal/accounts/CP-003/deliverables").json()
        for dlv in body["deliverables"]:
            assert dlv["status"] == "delivered"


# ===========================================================================
# 5. GET /summary
# ===========================================================================


class TestGetPortfolioSummary:
    def test_returns_200(self) -> None:
        resp = client.get("/api/v1/client-portal/summary")
        assert resp.status_code == 200

    def test_governance_decision_present(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_clients_is_5(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert body["total_clients"] == 5

    def test_by_tier_present(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert "by_tier" in body
        assert isinstance(body["by_tier"], dict)

    def test_by_tier_sprint_is_1(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert body["by_tier"]["sprint"] == 1

    def test_by_tier_data_pack_is_1(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert body["by_tier"]["data_pack"] == 1

    def test_by_tier_managed_ops_is_2(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert body["by_tier"]["managed_ops"] == 2

    def test_by_tier_custom_ai_is_1(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert body["by_tier"]["custom_ai"] == 1

    def test_avg_health_score_present(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert "avg_health_score" in body

    def test_avg_health_score_in_valid_range(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert 0.0 <= body["avg_health_score"] <= 100.0

    def test_total_mrr_sar_present(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert "total_mrr_sar" in body
        assert body["total_mrr_sar"] > 0

    def test_total_mrr_sar_equals_sum_of_all_mrr(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        expected = sum(a["mrr_sar"] for a in CLIENT_PORTALS.values())
        assert abs(body["total_mrr_sar"] - expected) < 0.01

    def test_avg_satisfaction_present(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert "avg_satisfaction" in body

    def test_avg_satisfaction_in_valid_range(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert 0.0 <= body["avg_satisfaction"] <= 5.0

    def test_avg_nps_present(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert "avg_nps" in body

    def test_avg_nps_in_valid_range(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert 0.0 <= body["avg_nps"] <= 10.0

    def test_active_deliverables_count_present(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert "active_deliverables_count" in body

    def test_active_deliverables_count_correct(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        expected = sum(
            len(a["active_deliverables"]) for a in CLIENT_PORTALS.values()
        )
        assert body["active_deliverables_count"] == expected

    def test_high_health_clients_present(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert "high_health_clients" in body

    def test_high_health_clients_count_correct(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        expected = sum(
            1 for a in CLIENT_PORTALS.values() if a["health_score"] >= 80
        )
        assert body["high_health_clients"] == expected

    def test_at_risk_clients_present(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        assert "at_risk_clients" in body

    def test_at_risk_clients_count_correct(self) -> None:
        body = client.get("/api/v1/client-portal/summary").json()
        expected = sum(
            1 for a in CLIENT_PORTALS.values() if a["health_score"] < 65
        )
        assert body["at_risk_clients"] == expected


# ===========================================================================
# 6. POST /accounts/{client_id}/request-review
# ===========================================================================


class TestRequestReview:
    _valid_body = {
        "requested_date": "2026-07-01",
        "topics": ["sprint performance", "upcoming renewals"],
    }

    def test_returns_200(self) -> None:
        resp = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        )
        assert resp.status_code == 200

    def test_governance_decision_present(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        ).json()
        assert "governance_decision" in body

    def test_governance_decision_is_approval_first(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        ).json()
        assert body["governance_decision"] == "APPROVAL_FIRST"

    def test_status_is_pending_approval(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        ).json()
        assert "pending_approval" in body["status"]

    def test_client_id_echoed(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        ).json()
        assert body["client_id"] == "CP-001"

    def test_requested_date_echoed(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        ).json()
        assert body["requested_date"] == "2026-07-01"

    def test_topics_echoed(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        ).json()
        assert body["topics"] == self._valid_body["topics"]

    def test_company_name_en_present(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        ).json()
        assert "company_name" in body
        assert body["company_name"]

    def test_message_ar_present_and_non_empty(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        ).json()
        assert "message_ar" in body
        assert body["message_ar"].strip()

    def test_message_en_present_and_non_empty(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        ).json()
        assert "message_en" in body
        assert body["message_en"].strip()

    def test_generated_at_present(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json=self._valid_body,
        ).json()
        assert "generated_at" in body

    def test_missing_client_returns_404(self) -> None:
        resp = client.post(
            "/api/v1/client-portal/accounts/CP-999/request-review",
            json=self._valid_body,
        )
        assert resp.status_code == 404

    def test_missing_requested_date_returns_422(self) -> None:
        resp = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json={"topics": ["sprint review"]},
        )
        assert resp.status_code == 422

    def test_missing_topics_returns_422(self) -> None:
        resp = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json={"requested_date": "2026-07-01"},
        )
        assert resp.status_code == 422

    def test_extra_fields_returns_422(self) -> None:
        resp = client.post(
            "/api/v1/client-portal/accounts/CP-001/request-review",
            json={**self._valid_body, "extra_field": "not_allowed"},
        )
        assert resp.status_code == 422

    def test_works_for_cp003(self) -> None:
        resp = client.post(
            "/api/v1/client-portal/accounts/CP-003/request-review",
            json={"requested_date": "2026-07-10", "topics": ["custom NLP roadmap"]},
        )
        assert resp.status_code == 200

    def test_multiple_topics_accepted(self) -> None:
        body = client.post(
            "/api/v1/client-portal/accounts/CP-002/request-review",
            json={
                "requested_date": "2026-07-15",
                "topics": ["data quality", "renewal options", "expansion"],
            },
        ).json()
        assert len(body["topics"]) == 3


# ===========================================================================
# 7. GET /upgrade-paths
# ===========================================================================


class TestGetUpgradePaths:
    def test_returns_200(self) -> None:
        resp = client.get("/api/v1/client-portal/upgrade-paths")
        assert resp.status_code == 200

    def test_governance_decision_present(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        assert "governance_decision" in body

    def test_governance_decision_is_allow_with_review(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        assert body["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_upgrade_paths_key_present(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        assert "upgrade_paths" in body
        assert isinstance(body["upgrade_paths"], list)

    def test_disclaimer_present(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        assert "disclaimer" in body
        assert body["disclaimer"].strip()

    def test_disclaimer_contains_no_guarantee_language(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        disclaimer = body["disclaimer"].lower()
        assert "not" in disclaimer or "indicative" in disclaimer

    def test_cp003_custom_ai_not_in_upgrade_paths(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        ids = [p["client_id"] for p in body["upgrade_paths"]]
        assert "CP-003" not in ids

    def test_cp004_health_58_not_in_upgrade_paths(self) -> None:
        # CP-004 health_score=58 < 70 threshold
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        ids = [p["client_id"] for p in body["upgrade_paths"]]
        assert "CP-004" not in ids

    def test_cp001_in_upgrade_paths(self) -> None:
        # CP-001 managed_ops, health_score=87 >= 70
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        ids = [p["client_id"] for p in body["upgrade_paths"]]
        assert "CP-001" in ids

    def test_cp001_recommended_tier_is_custom_ai(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        cp001_path = next(
            p for p in body["upgrade_paths"] if p["client_id"] == "CP-001"
        )
        assert cp001_path["recommended_tier"] == "custom_ai"

    def test_cp002_data_pack_health_73_in_upgrade_paths(self) -> None:
        # CP-002 data_pack, health_score=73 >= 70
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        ids = [p["client_id"] for p in body["upgrade_paths"]]
        assert "CP-002" in ids

    def test_cp002_recommended_tier_is_managed_ops(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        cp002_path = next(
            p for p in body["upgrade_paths"] if p["client_id"] == "CP-002"
        )
        assert cp002_path["recommended_tier"] == "managed_ops"

    def test_cp005_managed_ops_health_81_in_upgrade_paths(self) -> None:
        # CP-005 managed_ops, health_score=81 >= 70
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        ids = [p["client_id"] for p in body["upgrade_paths"]]
        assert "CP-005" in ids

    def test_every_path_has_required_fields(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        required = {
            "client_id", "company_name", "current_tier", "recommended_tier",
            "current_mrr_sar", "recommended_mrr_sar", "revenue_uplift_sar", "reason",
        }
        for path in body["upgrade_paths"]:
            for field in required:
                assert field in path, f"Missing field '{field}' in path {path}"

    def test_revenue_uplift_is_positive_for_all_paths(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        for path in body["upgrade_paths"]:
            assert path["revenue_uplift_sar"] > 0

    def test_revenue_uplift_equals_recommended_minus_current(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        for path in body["upgrade_paths"]:
            expected = round(path["recommended_mrr_sar"] - path["current_mrr_sar"], 2)
            assert abs(path["revenue_uplift_sar"] - expected) < 0.01

    def test_reason_is_non_empty_string_for_all_paths(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        for path in body["upgrade_paths"]:
            assert isinstance(path["reason"], str) and path["reason"].strip()

    def test_generated_at_present(self) -> None:
        body = client.get("/api/v1/client-portal/upgrade-paths").json()
        assert "generated_at" in body


# ===========================================================================
# 8. Helper — _now_iso
# ===========================================================================


class TestNowIso:
    def test_returns_string(self) -> None:
        result = _now_iso()
        assert isinstance(result, str)

    def test_contains_t_separator(self) -> None:
        result = _now_iso()
        assert "T" in result

    def test_contains_timezone_info(self) -> None:
        result = _now_iso()
        assert "+" in result or result.endswith("Z") or "+00:00" in result

    def test_length_is_reasonable(self) -> None:
        result = _now_iso()
        assert len(result) >= 19


# ===========================================================================
# 9. Helper — _client_or_404
# ===========================================================================


class TestClientOr404:
    def test_returns_dict_for_known_id(self) -> None:
        record = _client_or_404("CP-001")
        assert isinstance(record, dict)

    def test_returned_record_has_correct_client_id(self) -> None:
        record = _client_or_404("CP-001")
        assert record["client_id"] == "CP-001"

    def test_returns_cp003_record(self) -> None:
        record = _client_or_404("CP-003")
        assert record["tier"] == "custom_ai"

    def test_raises_http_exception_for_unknown_id(self) -> None:
        with pytest.raises(HTTPException) as exc_info:
            _client_or_404("CP-999")
        assert exc_info.value.status_code == 404

    def test_exception_detail_has_en_key(self) -> None:
        with pytest.raises(HTTPException) as exc_info:
            _client_or_404("DOES-NOT-EXIST")
        assert "en" in exc_info.value.detail

    def test_exception_detail_has_ar_key(self) -> None:
        with pytest.raises(HTTPException) as exc_info:
            _client_or_404("DOES-NOT-EXIST")
        assert "ar" in exc_info.value.detail


# ===========================================================================
# 10. Helper — _filter_accounts
# ===========================================================================


class TestFilterAccounts:
    def test_no_filters_returns_all(self) -> None:
        result = _filter_accounts(_ALL_ACCOUNTS, tier=None, min_health=None)
        assert len(result) == 5

    def test_tier_filter_sprint(self) -> None:
        result = _filter_accounts(_ALL_ACCOUNTS, tier="sprint", min_health=None)
        assert all(a["tier"] == "sprint" for a in result)
        assert len(result) == 1

    def test_tier_filter_managed_ops(self) -> None:
        result = _filter_accounts(_ALL_ACCOUNTS, tier="managed_ops", min_health=None)
        assert len(result) == 2

    def test_tier_filter_custom_ai(self) -> None:
        result = _filter_accounts(_ALL_ACCOUNTS, tier="custom_ai", min_health=None)
        assert len(result) == 1
        assert result[0]["client_id"] == "CP-003"

    def test_tier_filter_nonexistent_returns_empty(self) -> None:
        result = _filter_accounts(_ALL_ACCOUNTS, tier="enterprise", min_health=None)
        assert result == []

    def test_min_health_80_filters_correctly(self) -> None:
        result = _filter_accounts(_ALL_ACCOUNTS, tier=None, min_health=80)
        assert all(a["health_score"] >= 80 for a in result)

    def test_min_health_0_returns_all(self) -> None:
        result = _filter_accounts(_ALL_ACCOUNTS, tier=None, min_health=0)
        assert len(result) == 5

    def test_min_health_100_returns_empty(self) -> None:
        result = _filter_accounts(_ALL_ACCOUNTS, tier=None, min_health=100)
        assert result == []

    def test_combined_tier_and_min_health(self) -> None:
        result = _filter_accounts(_ALL_ACCOUNTS, tier="managed_ops", min_health=85)
        assert len(result) == 1
        assert result[0]["client_id"] == "CP-001"

    def test_empty_input_returns_empty(self) -> None:
        result = _filter_accounts([], tier="sprint", min_health=80)
        assert result == []


# ===========================================================================
# 11. Helper — _compute_by_tier
# ===========================================================================


class TestComputeByTier:
    def test_returns_dict(self) -> None:
        result = _compute_by_tier(_ALL_ACCOUNTS)
        assert isinstance(result, dict)

    def test_sprint_count_is_1(self) -> None:
        result = _compute_by_tier(_ALL_ACCOUNTS)
        assert result["sprint"] == 1

    def test_data_pack_count_is_1(self) -> None:
        result = _compute_by_tier(_ALL_ACCOUNTS)
        assert result["data_pack"] == 1

    def test_managed_ops_count_is_2(self) -> None:
        result = _compute_by_tier(_ALL_ACCOUNTS)
        assert result["managed_ops"] == 2

    def test_custom_ai_count_is_1(self) -> None:
        result = _compute_by_tier(_ALL_ACCOUNTS)
        assert result["custom_ai"] == 1

    def test_sum_of_counts_equals_total_accounts(self) -> None:
        result = _compute_by_tier(_ALL_ACCOUNTS)
        assert sum(result.values()) == len(_ALL_ACCOUNTS)

    def test_empty_input_returns_empty_dict(self) -> None:
        result = _compute_by_tier([])
        assert result == {}


# ===========================================================================
# 12. Helper — _compute_portfolio_summary
# ===========================================================================


class TestComputePortfolioSummary:
    def test_returns_dict(self) -> None:
        result = _compute_portfolio_summary(_ALL_ACCOUNTS)
        assert isinstance(result, dict)

    def test_total_clients_is_5(self) -> None:
        result = _compute_portfolio_summary(_ALL_ACCOUNTS)
        assert result["total_clients"] == 5

    def test_avg_health_score_in_range(self) -> None:
        result = _compute_portfolio_summary(_ALL_ACCOUNTS)
        assert 0.0 <= result["avg_health_score"] <= 100.0

    def test_total_mrr_sar_positive(self) -> None:
        result = _compute_portfolio_summary(_ALL_ACCOUNTS)
        assert result["total_mrr_sar"] > 0

    def test_avg_satisfaction_in_range(self) -> None:
        result = _compute_portfolio_summary(_ALL_ACCOUNTS)
        assert 0.0 <= result["avg_satisfaction"] <= 5.0

    def test_avg_nps_in_range(self) -> None:
        result = _compute_portfolio_summary(_ALL_ACCOUNTS)
        assert 0.0 <= result["avg_nps"] <= 10.0

    def test_active_deliverables_count_correct(self) -> None:
        result = _compute_portfolio_summary(_ALL_ACCOUNTS)
        expected = sum(len(a["active_deliverables"]) for a in _ALL_ACCOUNTS)
        assert result["active_deliverables_count"] == expected

    def test_high_health_clients_count_correct(self) -> None:
        result = _compute_portfolio_summary(_ALL_ACCOUNTS)
        expected = sum(1 for a in _ALL_ACCOUNTS if a["health_score"] >= 80)
        assert result["high_health_clients"] == expected

    def test_at_risk_clients_count_correct(self) -> None:
        result = _compute_portfolio_summary(_ALL_ACCOUNTS)
        expected = sum(1 for a in _ALL_ACCOUNTS if a["health_score"] < 65)
        assert result["at_risk_clients"] == expected

    def test_empty_accounts_returns_zero_values(self) -> None:
        result = _compute_portfolio_summary([])
        assert result["total_clients"] == 0
        assert result["avg_health_score"] == 0.0
        assert result["total_mrr_sar"] == 0.0
        assert result["by_tier"] == {}

    def test_single_account_summary(self) -> None:
        single = [CLIENT_PORTALS["CP-003"]]
        result = _compute_portfolio_summary(single)
        assert result["total_clients"] == 1
        assert result["avg_health_score"] == 92.0


# ===========================================================================
# 13. Helper — _next_tier
# ===========================================================================


class TestNextTier:
    def test_sprint_next_is_data_pack(self) -> None:
        assert _next_tier("sprint") == "data_pack"

    def test_data_pack_next_is_managed_ops(self) -> None:
        assert _next_tier("data_pack") == "managed_ops"

    def test_managed_ops_next_is_custom_ai(self) -> None:
        assert _next_tier("managed_ops") == "custom_ai"

    def test_custom_ai_next_is_none(self) -> None:
        assert _next_tier("custom_ai") is None

    def test_unknown_tier_returns_none(self) -> None:
        assert _next_tier("enterprise") is None


# ===========================================================================
# 14. Helper — _build_upgrade_paths
# ===========================================================================


class TestBuildUpgradePaths:
    def test_returns_list(self) -> None:
        result = _build_upgrade_paths(_ALL_ACCOUNTS)
        assert isinstance(result, list)

    def test_cp003_excluded_custom_ai(self) -> None:
        result = _build_upgrade_paths(_ALL_ACCOUNTS)
        ids = [p["client_id"] for p in result]
        assert "CP-003" not in ids

    def test_cp004_excluded_low_health(self) -> None:
        # CP-004 health_score=58 < 70
        result = _build_upgrade_paths(_ALL_ACCOUNTS)
        ids = [p["client_id"] for p in result]
        assert "CP-004" not in ids

    def test_cp001_included(self) -> None:
        result = _build_upgrade_paths(_ALL_ACCOUNTS)
        ids = [p["client_id"] for p in result]
        assert "CP-001" in ids

    def test_cp002_included(self) -> None:
        result = _build_upgrade_paths(_ALL_ACCOUNTS)
        ids = [p["client_id"] for p in result]
        assert "CP-002" in ids

    def test_cp005_included(self) -> None:
        result = _build_upgrade_paths(_ALL_ACCOUNTS)
        ids = [p["client_id"] for p in result]
        assert "CP-005" in ids

    def test_each_path_has_revenue_uplift(self) -> None:
        result = _build_upgrade_paths(_ALL_ACCOUNTS)
        for path in result:
            assert "revenue_uplift_sar" in path

    def test_revenue_uplift_always_positive(self) -> None:
        result = _build_upgrade_paths(_ALL_ACCOUNTS)
        for path in result:
            assert path["revenue_uplift_sar"] > 0

    def test_empty_accounts_returns_empty_list(self) -> None:
        assert _build_upgrade_paths([]) == []

    def test_sprint_to_data_pack_reason(self) -> None:
        # CP-001 would need a sprint-tier account with health>=70 to test this
        test_accounts = [
            {
                "client_id": "TEST-001",
                "company_name_en": "Test Co",
                "tier": "sprint",
                "health_score": 75,
                "mrr_sar": 499.0,
            }
        ]
        result = _build_upgrade_paths(test_accounts)
        assert len(result) == 1
        assert result[0]["reason"] == "Ready for structured data ops"

    def test_data_pack_to_managed_ops_reason(self) -> None:
        test_accounts = [
            {
                "client_id": "TEST-002",
                "company_name_en": "Test Co 2",
                "tier": "data_pack",
                "health_score": 80,
                "mrr_sar": 1500.0,
            }
        ]
        result = _build_upgrade_paths(test_accounts)
        assert len(result) == 1
        assert result[0]["reason"] == "Strong data foundation — upgrade to managed AI"

    def test_managed_ops_to_custom_ai_reason(self) -> None:
        test_accounts = [
            {
                "client_id": "TEST-003",
                "company_name_en": "Test Co 3",
                "tier": "managed_ops",
                "health_score": 85,
                "mrr_sar": 2999.0,
            }
        ]
        result = _build_upgrade_paths(test_accounts)
        assert len(result) == 1
        assert result[0]["reason"] == "Complex workflows warrant custom AI build"

    def test_health_exactly_70_is_included(self) -> None:
        test_accounts = [
            {
                "client_id": "TEST-004",
                "company_name_en": "Threshold Co",
                "tier": "data_pack",
                "health_score": 70,
                "mrr_sar": 1500.0,
            }
        ]
        result = _build_upgrade_paths(test_accounts)
        assert len(result) == 1

    def test_health_69_is_excluded(self) -> None:
        test_accounts = [
            {
                "client_id": "TEST-005",
                "company_name_en": "Below Threshold Co",
                "tier": "data_pack",
                "health_score": 69,
                "mrr_sar": 1500.0,
            }
        ]
        result = _build_upgrade_paths(test_accounts)
        assert result == []
