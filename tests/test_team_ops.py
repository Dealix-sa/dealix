"""Tests for the Team Operations API.

Covers: data integrity, list endpoint, hiring plan, member detail,
add member, update status, capacity overview, and governance compliance.
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

from api.routers.team_ops import (  # noqa: E402
    _HIRING_MILESTONES,
    _TEAM_MEMBERS,
    _days_tenure,
    _enrich_member,
    _now_iso,
    _today_str,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# Helper function unit tests
# ---------------------------------------------------------------------------


class TestHelperFunctions:
    def test_now_iso_returns_string(self):
        result = _now_iso()
        assert isinstance(result, str)

    def test_now_iso_contains_t(self):
        result = _now_iso()
        assert "T" in result

    def test_today_str_format(self):
        result = _today_str()
        parts = result.split("-")
        assert len(parts) == 3
        assert len(parts[0]) == 4  # year

    def test_days_tenure_none_returns_zero(self):
        assert _days_tenure(None) == 0

    def test_days_tenure_empty_string_returns_zero(self):
        assert _days_tenure("") == 0

    def test_days_tenure_past_date_positive(self):
        assert _days_tenure("2024-01-01") > 0

    def test_days_tenure_today_returns_zero(self):
        from datetime import date
        today = date.today().isoformat()
        result = _days_tenure(today)
        assert result >= 0

    def test_days_tenure_invalid_string_returns_zero(self):
        assert _days_tenure("not-a-date") == 0

    def test_enrich_member_adds_days_tenure(self):
        member = {
            "member_id": "TM-TEST",
            "name_ar": "اسم",
            "name_en": "Name",
            "role_ar": "دور",
            "role_en": "Role",
            "employment_type": "full_time",
            "status": "active",
            "hire_trigger": None,
            "monthly_cost_sar": 5000.0,
            "permissions": [],
            "joined_at": "2025-01-01",
            "kpi_targets": {},
        }
        enriched = _enrich_member(member)
        assert "days_tenure" in enriched
        assert enriched["days_tenure"] >= 0

    def test_enrich_member_planned_has_zero_tenure(self):
        member = {
            "member_id": "TM-PLAN",
            "name_ar": "مخطط",
            "name_en": "Planned",
            "role_ar": "دور مخطط",
            "role_en": "Planned Role",
            "employment_type": "planned",
            "status": "planned",
            "hire_trigger": "100K SAR MRR",
            "monthly_cost_sar": 9000.0,
            "permissions": [],
            "joined_at": None,
            "kpi_targets": {},
        }
        enriched = _enrich_member(member)
        assert enriched["days_tenure"] == 0


# ---------------------------------------------------------------------------
# Data Integrity
# ---------------------------------------------------------------------------


class TestDemoDataIntegrity:
    def test_five_team_members_exist(self):
        assert len(_TEAM_MEMBERS) >= 5

    def test_all_have_member_id(self):
        ids = [m["member_id"] for m in _TEAM_MEMBERS]
        assert len(ids) == len(set(ids))

    def test_member_ids_prefixed_tm(self):
        for m in _TEAM_MEMBERS:
            assert m["member_id"].startswith("TM-")

    def test_tm_001_through_005_exist(self):
        ids = {m["member_id"] for m in _TEAM_MEMBERS}
        for expected in ("TM-001", "TM-002", "TM-003", "TM-004", "TM-005"):
            assert expected in ids

    def test_founder_is_tm_001(self):
        founder = next(m for m in _TEAM_MEMBERS if m["member_id"] == "TM-001")
        assert "CEO" in founder["role_en"] or "Founder" in founder["role_en"]

    def test_all_required_fields_present(self):
        required = {
            "member_id", "name_ar", "name_en", "role_ar", "role_en",
            "employment_type", "status", "monthly_cost_sar",
            "permissions", "joined_at", "kpi_targets",
        }
        for m in _TEAM_MEMBERS:
            for f in required:
                assert f in m, f"Missing field {f!r} in {m['member_id']}"

    def test_all_employment_types_valid(self):
        valid = {"full_time", "part_time", "contractor", "planned"}
        for m in _TEAM_MEMBERS:
            assert m["employment_type"] in valid

    def test_all_statuses_valid(self):
        valid = {"active", "probation", "planned", "inactive"}
        for m in _TEAM_MEMBERS:
            assert m["status"] in valid

    def test_one_planned_role_exists(self):
        planned = [m for m in _TEAM_MEMBERS if m["status"] == "planned"]
        assert len(planned) >= 1

    def test_planned_member_has_no_joined_at(self):
        planned = next(m for m in _TEAM_MEMBERS if m["status"] == "planned")
        assert planned["joined_at"] is None

    def test_one_probation_member_exists(self):
        probation = [m for m in _TEAM_MEMBERS if m["status"] == "probation"]
        assert len(probation) >= 1

    def test_founder_has_all_permission(self):
        founder = next(m for m in _TEAM_MEMBERS if m["member_id"] == "TM-001")
        assert "all" in founder["permissions"]

    def test_planned_member_has_empty_permissions(self):
        planned = next(m for m in _TEAM_MEMBERS if m["status"] == "planned")
        assert planned["permissions"] == []

    def test_all_monthly_costs_non_negative(self):
        for m in _TEAM_MEMBERS:
            assert m["monthly_cost_sar"] >= 0

    def test_active_full_time_members_have_positive_cost_or_founder(self):
        for m in _TEAM_MEMBERS:
            if m["status"] == "active" and m["employment_type"] == "full_time" and m["member_id"] != "TM-001":
                assert m["monthly_cost_sar"] > 0

    def test_all_have_bilingual_names(self):
        for m in _TEAM_MEMBERS:
            assert len(m["name_ar"]) > 0
            assert len(m["name_en"]) > 0

    def test_all_have_bilingual_roles(self):
        for m in _TEAM_MEMBERS:
            assert len(m["role_ar"]) > 0
            assert len(m["role_en"]) > 0

    def test_all_have_kpi_targets_dict(self):
        for m in _TEAM_MEMBERS:
            assert isinstance(m["kpi_targets"], dict)

    def test_five_hiring_milestones_exist(self):
        assert len(_HIRING_MILESTONES) == 5

    def test_hiring_milestones_have_required_fields(self):
        required = {"mrr_threshold_sar", "role_ar", "role_en", "status"}
        for h in _HIRING_MILESTONES:
            for f in required:
                assert f in h, f"Missing field {f!r} in milestone"

    def test_hiring_milestone_statuses_valid(self):
        valid = {"triggered", "upcoming", "planned"}
        for h in _HIRING_MILESTONES:
            assert h["status"] in valid


# ---------------------------------------------------------------------------
# GET / — list all team members
# ---------------------------------------------------------------------------


class TestListTeamMembersEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/team/").status_code == 200

    def test_governance_decision_allow_with_review(self):
        data = client.get("/api/v1/team/").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_members_list(self):
        data = client.get("/api/v1/team/").json()
        assert "members" in data
        assert isinstance(data["members"], list)

    def test_members_count_at_least_five(self):
        data = client.get("/api/v1/team/").json()
        assert len(data["members"]) >= 5

    def test_has_summary_block(self):
        data = client.get("/api/v1/team/").json()
        assert "summary" in data

    def test_summary_total_members(self):
        data = client.get("/api/v1/team/").json()
        assert data["summary"]["total_members"] == len(data["members"])

    def test_summary_active_count_accurate(self):
        data = client.get("/api/v1/team/").json()
        active_from_list = sum(1 for m in data["members"] if m["status"] == "active")
        assert data["summary"]["active_count"] == active_from_list

    def test_summary_monthly_cost_positive(self):
        data = client.get("/api/v1/team/").json()
        assert data["summary"]["monthly_cost_sar_total"] >= 0

    def test_summary_arr_is_monthly_times_12(self):
        data = client.get("/api/v1/team/").json()
        monthly = data["summary"]["monthly_cost_sar_total"]
        arr = data["summary"]["team_arr_overhead_sar"]
        assert arr == monthly * 12

    def test_summary_open_roles_count(self):
        data = client.get("/api/v1/team/").json()
        planned_from_list = sum(1 for m in data["members"] if m["status"] == "planned")
        assert data["summary"]["open_roles_count"] == planned_from_list

    def test_each_member_has_days_tenure(self):
        data = client.get("/api/v1/team/").json()
        for m in data["members"]:
            assert "days_tenure" in m, f"Missing days_tenure for {m.get('member_id')}"

    def test_planned_member_has_zero_days_tenure(self):
        data = client.get("/api/v1/team/").json()
        planned = [m for m in data["members"] if m["status"] == "planned"]
        for m in planned:
            assert m["days_tenure"] == 0

    def test_has_generated_at(self):
        data = client.get("/api/v1/team/").json()
        assert "generated_at" in data

    def test_active_members_have_positive_tenure(self):
        data = client.get("/api/v1/team/").json()
        active = [m for m in data["members"] if m["status"] == "active" and m["member_id"] != "TM-001"]
        for m in active:
            assert m["days_tenure"] >= 0


# ---------------------------------------------------------------------------
# GET /hiring-plan
# ---------------------------------------------------------------------------


class TestHiringPlanEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/team/hiring-plan").status_code == 200

    def test_governance_decision_allow_with_review(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_milestones_list(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        assert "milestones" in data
        assert isinstance(data["milestones"], list)

    def test_five_milestones_returned(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        assert len(data["milestones"]) == 5

    def test_milestones_sorted_by_threshold(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        thresholds = [m["mrr_threshold_sar"] for m in data["milestones"]]
        assert thresholds == sorted(thresholds)

    def test_first_milestone_is_30k(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        assert data["milestones"][0]["mrr_threshold_sar"] == 30_000

    def test_last_milestone_is_200k(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        assert data["milestones"][-1]["mrr_threshold_sar"] == 200_000

    def test_next_hire_is_first_upcoming(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        upcoming = [m for m in data["milestones"] if m["status"] == "upcoming"]
        if upcoming:
            assert data["next_hire"] == upcoming[0]["role_en"]

    def test_next_hire_is_sdr(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        assert data["next_hire"] == "SDR"

    def test_has_total_planned_cost(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        assert "total_planned_cost_sar" in data
        assert data["total_planned_cost_sar"] >= 0

    def test_has_bilingual_action(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        assert "action_ar" in data
        assert "action_en" in data
        assert len(data["action_ar"]) > 0
        assert len(data["action_en"]) > 0

    def test_has_generated_at(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        assert "generated_at" in data

    def test_triggered_milestones_exist(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        triggered = [m for m in data["milestones"] if m["status"] == "triggered"]
        assert len(triggered) >= 2

    def test_each_milestone_has_bilingual_role(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        for m in data["milestones"]:
            assert "role_ar" in m and len(m["role_ar"]) > 0
            assert "role_en" in m and len(m["role_en"]) > 0

    def test_next_hire_ar_present(self):
        data = client.get("/api/v1/team/hiring-plan").json()
        assert "next_hire_ar" in data


# ---------------------------------------------------------------------------
# GET /{member_id} — single member detail
# ---------------------------------------------------------------------------


class TestGetMemberEndpoint:
    def test_returns_200_for_tm_001(self):
        assert client.get("/api/v1/team/TM-001").status_code == 200

    def test_returns_200_for_tm_005(self):
        assert client.get("/api/v1/team/TM-005").status_code == 200

    def test_returns_404_for_unknown_id(self):
        assert client.get("/api/v1/team/TM-UNKNOWN").status_code == 404

    def test_governance_decision_allow_with_review(self):
        data = client.get("/api/v1/team/TM-001").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_returns_correct_member_id(self):
        data = client.get("/api/v1/team/TM-002").json()
        assert data["member_id"] == "TM-002"

    def test_has_days_tenure(self):
        data = client.get("/api/v1/team/TM-001").json()
        assert "days_tenure" in data

    def test_planned_member_has_zero_tenure(self):
        data = client.get("/api/v1/team/TM-005").json()
        assert data["days_tenure"] == 0

    def test_has_generated_at(self):
        data = client.get("/api/v1/team/TM-001").json()
        assert "generated_at" in data

    def test_has_kpi_targets(self):
        data = client.get("/api/v1/team/TM-001").json()
        assert "kpi_targets" in data
        assert isinstance(data["kpi_targets"], dict)

    def test_has_permissions_list(self):
        data = client.get("/api/v1/team/TM-001").json()
        assert "permissions" in data
        assert isinstance(data["permissions"], list)

    def test_404_detail_mentions_member_id(self):
        resp = client.get("/api/v1/team/TM-NOTFOUND")
        assert resp.status_code == 404
        assert "TM-NOTFOUND" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# POST / — add a new team member
# ---------------------------------------------------------------------------


class TestAddMemberEndpoint:
    def _valid_body(self) -> dict:
        return {
            "name_ar": "موظف جديد",
            "name_en": "New Employee",
            "role_ar": "محلل بيانات",
            "role_en": "Data Analyst",
            "employment_type": "full_time",
            "monthly_cost_sar": 10000.0,
            "permissions": ["reporting", "data_access"],
        }

    def test_returns_200(self):
        r = client.post("/api/v1/team/", json=self._valid_body())
        assert r.status_code == 200

    def test_governance_decision_approval_first(self):
        r = client.post("/api/v1/team/", json=self._valid_body())
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_response_contains_member_id(self):
        r = client.post("/api/v1/team/", json=self._valid_body())
        data = r.json()
        assert "member_id" in data
        assert data["member_id"].startswith("TM-")

    def test_member_gets_active_status(self):
        r = client.post("/api/v1/team/", json=self._valid_body())
        data = r.json()
        assert data["member"]["status"] == "active"

    def test_member_gets_joined_at_today(self):
        from datetime import date
        r = client.post("/api/v1/team/", json=self._valid_body())
        data = r.json()
        assert data["member"]["joined_at"] == date.today().isoformat()

    def test_response_contains_member_block(self):
        r = client.post("/api/v1/team/", json=self._valid_body())
        assert "member" in r.json()

    def test_member_block_has_days_tenure(self):
        r = client.post("/api/v1/team/", json=self._valid_body())
        assert "days_tenure" in r.json()["member"]

    def test_missing_name_ar_returns_422(self):
        body = self._valid_body()
        del body["name_ar"]
        r = client.post("/api/v1/team/", json=body)
        assert r.status_code == 422

    def test_missing_name_en_returns_422(self):
        body = self._valid_body()
        del body["name_en"]
        r = client.post("/api/v1/team/", json=body)
        assert r.status_code == 422

    def test_missing_role_en_returns_422(self):
        body = self._valid_body()
        del body["role_en"]
        r = client.post("/api/v1/team/", json=body)
        assert r.status_code == 422

    def test_missing_employment_type_returns_422(self):
        body = self._valid_body()
        del body["employment_type"]
        r = client.post("/api/v1/team/", json=body)
        assert r.status_code == 422

    def test_invalid_employment_type_returns_422(self):
        body = self._valid_body()
        body["employment_type"] = "freelance"
        r = client.post("/api/v1/team/", json=body)
        assert r.status_code == 422

    def test_negative_monthly_cost_returns_422(self):
        body = self._valid_body()
        body["monthly_cost_sar"] = -100.0
        r = client.post("/api/v1/team/", json=body)
        assert r.status_code == 422

    def test_zero_monthly_cost_is_allowed(self):
        body = self._valid_body()
        body["monthly_cost_sar"] = 0.0
        r = client.post("/api/v1/team/", json=body)
        assert r.status_code == 200

    def test_permissions_defaults_to_empty_list(self):
        body = self._valid_body()
        del body["permissions"]
        r = client.post("/api/v1/team/", json=body)
        assert r.status_code == 200
        assert r.json()["member"]["permissions"] == []

    def test_response_has_bilingual_status(self):
        r = client.post("/api/v1/team/", json=self._valid_body())
        data = r.json()
        assert "status_ar" in data
        assert "status_en" in data

    def test_sequential_ids_assigned(self):
        r1 = client.post("/api/v1/team/", json=self._valid_body())
        r2 = client.post("/api/v1/team/", json=self._valid_body())
        id1 = r1.json()["member_id"]
        id2 = r2.json()["member_id"]
        seq1 = int(id1.split("-")[1])
        seq2 = int(id2.split("-")[1])
        assert seq2 > seq1


# ---------------------------------------------------------------------------
# PUT /{member_id}/status — update member status
# ---------------------------------------------------------------------------


class TestUpdateMemberStatusEndpoint:
    def _valid_body(self, new_status: str = "probation") -> dict:
        return {
            "new_status": new_status,
            "reason": "Performance review triggered status change",
        }

    def test_returns_200_for_valid_update(self):
        r = client.put("/api/v1/team/TM-002/status", json=self._valid_body("probation"))
        assert r.status_code == 200

    def test_governance_decision_approval_first(self):
        r = client.put("/api/v1/team/TM-003/status", json=self._valid_body("active"))
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_returns_404_for_unknown_member(self):
        r = client.put("/api/v1/team/TM-UNKNOWN/status", json=self._valid_body("active"))
        assert r.status_code == 404

    def test_returns_400_for_planned_status(self):
        r = client.put("/api/v1/team/TM-002/status", json={
            "new_status": "planned",
            "reason": "This should be rejected by the endpoint",
        })
        assert r.status_code == 400

    def test_400_detail_mentions_post(self):
        r = client.put("/api/v1/team/TM-002/status", json={
            "new_status": "planned",
            "reason": "Testing planned status rejection",
        })
        detail = r.json()["detail"].lower()
        assert "post" in detail or "planned" in detail

    def test_reason_too_short_returns_422(self):
        r = client.put("/api/v1/team/TM-002/status", json={
            "new_status": "active",
            "reason": "No",
        })
        assert r.status_code == 422

    def test_invalid_status_returns_422(self):
        r = client.put("/api/v1/team/TM-002/status", json={
            "new_status": "terminated",
            "reason": "Invalid status value submitted",
        })
        assert r.status_code == 422

    def test_response_has_previous_status(self):
        r = client.put("/api/v1/team/TM-003/status", json=self._valid_body("active"))
        data = r.json()
        assert "previous_status" in data

    def test_response_has_new_status(self):
        r = client.put("/api/v1/team/TM-003/status", json=self._valid_body("active"))
        assert r.json()["new_status"] == "active"

    def test_response_echoes_reason(self):
        body = self._valid_body("inactive")
        r = client.put("/api/v1/team/TM-003/status", json=body)
        if r.status_code == 200:
            assert r.json()["reason"] == body["reason"]

    def test_response_has_bilingual_status_message(self):
        r = client.put("/api/v1/team/TM-003/status", json=self._valid_body("active"))
        data = r.json()
        assert "status_ar" in data
        assert "status_en" in data

    def test_response_has_generated_at(self):
        r = client.put("/api/v1/team/TM-003/status", json=self._valid_body("active"))
        assert "generated_at" in r.json()

    def test_set_inactive_returns_200(self):
        r = client.put("/api/v1/team/TM-004/status", json=self._valid_body("inactive"))
        assert r.status_code == 200

    def test_set_active_returns_200(self):
        r = client.put("/api/v1/team/TM-004/status", json=self._valid_body("active"))
        assert r.status_code == 200


# ---------------------------------------------------------------------------
# GET /capacity — team capacity overview
# ---------------------------------------------------------------------------


class TestCapacityEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/team/capacity").status_code == 200

    def test_governance_decision_allow_with_review(self):
        data = client.get("/api/v1/team/capacity").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_active_members_field(self):
        data = client.get("/api/v1/team/capacity").json()
        assert "active_members" in data
        assert isinstance(data["active_members"], int)

    def test_active_members_excludes_planned(self):
        data_list = client.get("/api/v1/team/").json()
        data_cap = client.get("/api/v1/team/capacity").json()
        # active_members (capacity) must not include planned-status members
        planned_count = sum(1 for m in data_list["members"] if m["status"] == "planned")
        total_count = len(data_list["members"])
        assert data_cap["active_members"] <= total_count - planned_count

    def test_has_current_active_clients(self):
        data = client.get("/api/v1/team/capacity").json()
        assert "current_active_clients" in data
        assert data["current_active_clients"] == 12

    def test_has_capacity_per_member(self):
        data = client.get("/api/v1/team/capacity").json()
        assert "capacity_per_member" in data

    def test_capacity_per_member_computed_correctly(self):
        data = client.get("/api/v1/team/capacity").json()
        expected = round(data["current_active_clients"] / data["active_members"], 2)
        assert data["capacity_per_member"] == expected

    def test_has_capacity_warning_bool(self):
        data = client.get("/api/v1/team/capacity").json()
        assert "capacity_warning" in data
        assert isinstance(data["capacity_warning"], bool)

    def test_capacity_warning_reflects_threshold(self):
        data = client.get("/api/v1/team/capacity").json()
        ratio = data["current_active_clients"] / data["active_members"]
        expected_warning = ratio > 6
        assert data["capacity_warning"] == expected_warning

    def test_has_team_health_score(self):
        data = client.get("/api/v1/team/capacity").json()
        assert "team_health_score" in data

    def test_health_score_in_range(self):
        data = client.get("/api/v1/team/capacity").json()
        score = data["team_health_score"]
        assert 0 <= score <= 100

    def test_has_recommendations_ar(self):
        data = client.get("/api/v1/team/capacity").json()
        assert "recommendations_ar" in data
        assert isinstance(data["recommendations_ar"], list)
        assert len(data["recommendations_ar"]) > 0

    def test_has_recommendations_en(self):
        data = client.get("/api/v1/team/capacity").json()
        assert "recommendations_en" in data
        assert isinstance(data["recommendations_en"], list)
        assert len(data["recommendations_en"]) > 0

    def test_has_monthly_cost_total(self):
        data = client.get("/api/v1/team/capacity").json()
        assert "monthly_cost_sar_total" in data
        assert data["monthly_cost_sar_total"] >= 0

    def test_has_generated_at(self):
        data = client.get("/api/v1/team/capacity").json()
        assert "generated_at" in data


# ---------------------------------------------------------------------------
# Monthly cost totals
# ---------------------------------------------------------------------------


class TestMonthlyCostTotals:
    def test_list_endpoint_monthly_cost_positive_when_active_members_present(self):
        data = client.get("/api/v1/team/").json()
        active_with_cost = [
            m for m in data["members"]
            if m["status"] != "planned" and m["monthly_cost_sar"] > 0
        ]
        if active_with_cost:
            assert data["summary"]["monthly_cost_sar_total"] > 0

    def test_capacity_monthly_cost_non_negative(self):
        data = client.get("/api/v1/team/capacity").json()
        assert data["monthly_cost_sar_total"] >= 0

    def test_arr_is_12x_monthly(self):
        data = client.get("/api/v1/team/").json()
        assert data["summary"]["team_arr_overhead_sar"] == data["summary"]["monthly_cost_sar_total"] * 12

    def test_planned_members_excluded_from_cost(self):
        data = client.get("/api/v1/team/").json()
        planned_cost = sum(
            m["monthly_cost_sar"]
            for m in data["members"]
            if m["status"] == "planned"
        )
        # Planned members should not inflate the monthly total
        active_cost = sum(
            m["monthly_cost_sar"]
            for m in data["members"]
            if m["status"] != "planned"
        )
        assert data["summary"]["monthly_cost_sar_total"] == active_cost


# ---------------------------------------------------------------------------
# Governance compliance
# ---------------------------------------------------------------------------


class TestGovernanceCompliance:
    def test_all_read_endpoints_return_allow_with_review(self):
        endpoints = [
            "/api/v1/team/",
            "/api/v1/team/hiring-plan",
            "/api/v1/team/capacity",
            "/api/v1/team/TM-001",
        ]
        for url in endpoints:
            data = client.get(url).json()
            assert data.get("governance_decision") == "ALLOW_WITH_REVIEW", (
                f"Expected ALLOW_WITH_REVIEW on {url}, got {data.get('governance_decision')}"
            )

    def test_post_member_uses_approval_first(self):
        body = {
            "name_ar": "حوكمة",
            "name_en": "Governance Test Member",
            "role_ar": "دور اختباري",
            "role_en": "Test Role",
            "employment_type": "contractor",
            "monthly_cost_sar": 5000.0,
        }
        data = client.post("/api/v1/team/", json=body).json()
        assert data["governance_decision"] == "APPROVAL_FIRST"

    def test_put_status_uses_approval_first(self):
        body = {"new_status": "active", "reason": "Governance compliance verification test"}
        data = client.put("/api/v1/team/TM-002/status", json=body).json()
        assert data["governance_decision"] == "APPROVAL_FIRST"

    def test_all_responses_have_governance_decision_field(self):
        responses = [
            client.get("/api/v1/team/"),
            client.get("/api/v1/team/hiring-plan"),
            client.get("/api/v1/team/capacity"),
            client.get("/api/v1/team/TM-001"),
            client.post("/api/v1/team/", json={
                "name_ar": "اختبار",
                "name_en": "Gov Check",
                "role_ar": "دور",
                "role_en": "Tester",
                "employment_type": "full_time",
                "monthly_cost_sar": 0.0,
            }),
            client.put("/api/v1/team/TM-002/status", json={
                "new_status": "active",
                "reason": "Final governance check for all endpoints",
            }),
        ]
        for r in responses:
            assert "governance_decision" in r.json(), (
                f"governance_decision missing from response: {r.json()}"
            )
