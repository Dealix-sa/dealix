"""Tests for the Onboarding Operations API — 12-step client onboarding workflow.

Covers: checklist structure, active onboardings, step advancement,
start onboarding, and performance metrics.
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

from api.routers.onboarding_ops import ONBOARDING_CHECKLIST, router  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


class TestChecklistEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/onboarding/checklist").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/onboarding/checklist").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_12_steps(self):
        data = client.get("/api/v1/onboarding/checklist").json()
        assert data["total_steps"] == 12
        assert len(data["checklist"]) == 12

    def test_has_categories(self):
        data = client.get("/api/v1/onboarding/checklist").json()
        assert "checklist_by_category" in data
        assert len(data["checklist_by_category"]) > 0

    def test_each_step_has_bilingual_names(self):
        data = client.get("/api/v1/onboarding/checklist").json()
        for step in data["checklist"]:
            assert "name_ar" in step
            assert "name_en" in step

    def test_critical_steps_present(self):
        data = client.get("/api/v1/onboarding/checklist").json()
        assert data["critical_steps"] > 0

    def test_approval_first_steps_listed(self):
        data = client.get("/api/v1/onboarding/checklist").json()
        assert "approval_first_steps" in data
        assert len(data["approval_first_steps"]) > 0

    def test_estimated_hours_positive(self):
        data = client.get("/api/v1/onboarding/checklist").json()
        assert data["estimated_total_hours"] > 0

    def test_has_governance_note(self):
        data = client.get("/api/v1/onboarding/checklist").json()
        assert "note_ar" in data
        assert "note_en" in data


class TestChecklistDataIntegrity:
    def test_12_steps_in_module(self):
        assert len(ONBOARDING_CHECKLIST) == 12

    def test_steps_sequential(self):
        steps = [s["step"] for s in ONBOARDING_CHECKLIST]
        assert steps == list(range(1, 13))

    def test_all_have_step_ids(self):
        ids = [s["step_id"] for s in ONBOARDING_CHECKLIST]
        assert len(ids) == len(set(ids))

    def test_all_governance_gates_valid(self):
        valid_gates = {"ALLOW_WITH_REVIEW", "APPROVAL_FIRST"}
        for step in ONBOARDING_CHECKLIST:
            assert step["governance_gate"] in valid_gates

    def test_at_least_3_approval_first_steps(self):
        approval_steps = [s for s in ONBOARDING_CHECKLIST if s["governance_gate"] == "APPROVAL_FIRST"]
        assert len(approval_steps) >= 3

    def test_all_owners_valid(self):
        valid_owners = {"founder", "client"}
        for step in ONBOARDING_CHECKLIST:
            assert step["owner"] in valid_owners

    def test_client_owned_steps_exist(self):
        client_steps = [s for s in ONBOARDING_CHECKLIST if s["owner"] == "client"]
        assert len(client_steps) >= 2


class TestActiveOnboardingsEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/onboarding/active").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/onboarding/active").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_clients_list(self):
        data = client.get("/api/v1/onboarding/active").json()
        assert "clients" in data
        assert len(data["clients"]) >= 2

    def test_total_count_matches(self):
        data = client.get("/api/v1/onboarding/active").json()
        assert data["total_onboarding"] == len(data["clients"])

    def test_each_client_has_completion_pct(self):
        data = client.get("/api/v1/onboarding/active").json()
        for c in data["clients"]:
            assert "completion_pct" in c
            assert 0 <= c["completion_pct"] <= 100

    def test_blocked_count_matches(self):
        data = client.get("/api/v1/onboarding/active").json()
        blocked = [c for c in data["clients"] if c["blocked"]]
        assert data["blocked_count"] == len(blocked)

    def test_has_alert_ar_and_en(self):
        data = client.get("/api/v1/onboarding/active").json()
        assert "alert_ar" in data
        assert "alert_en" in data


class TestOnboardingDetailEndpoint:
    def test_returns_200_for_valid_id(self):
        assert client.get("/api/v1/onboarding/ONB-001").status_code == 200

    def test_returns_404_for_unknown_id(self):
        assert client.get("/api/v1/onboarding/UNKNOWN-999").status_code == 404

    def test_governance_decision(self):
        data = client.get("/api/v1/onboarding/ONB-001").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_completion_pct(self):
        data = client.get("/api/v1/onboarding/ONB-001").json()
        assert "completion_pct" in data
        assert 0 <= data["completion_pct"] <= 100

    def test_has_current_step_data(self):
        data = client.get("/api/v1/onboarding/ONB-001").json()
        assert "current_step_data" in data

    def test_has_next_action_bilingual(self):
        data = client.get("/api/v1/onboarding/ONB-001").json()
        assert "next_action_ar" in data
        assert "next_action_en" in data

    def test_has_estimated_hours_remaining(self):
        data = client.get("/api/v1/onboarding/ONB-001").json()
        assert "estimated_hours_remaining" in data
        assert data["estimated_hours_remaining"] >= 0


class TestStartOnboardingEndpoint:
    def test_start_new_client_returns_200(self):
        body = {
            "client_id": "ONB-NEW-001",
            "company_name_ar": "شركة اختبار جديدة",
            "company_name_en": "New Test Company",
            "sector": "technology",
            "city": "riyadh",
            "tier": "sprint",
            "contract_value_sar": 499,
        }
        r = client.post("/api/v1/onboarding/start", json=body)
        assert r.status_code == 200

    def test_start_uses_approval_first(self):
        body = {
            "client_id": "ONB-NEW-002",
            "company_name_ar": "شركة أخرى",
            "company_name_en": "Another Company",
            "sector": "logistics",
            "city": "jeddah",
            "tier": "sprint",
            "contract_value_sar": 499,
        }
        data = client.post("/api/v1/onboarding/start", json=body).json()
        assert data["governance_decision"] == "APPROVAL_FIRST"

    def test_duplicate_client_returns_409(self):
        body = {
            "client_id": "ONB-NEW-001",  # already created above
            "company_name_ar": "شركة مكررة",
            "company_name_en": "Duplicate Co",
            "sector": "technology",
            "city": "riyadh",
            "tier": "sprint",
            "contract_value_sar": 499,
        }
        r = client.post("/api/v1/onboarding/start", json=body)
        assert r.status_code == 409

    def test_missing_required_fields_returns_422(self):
        r = client.post("/api/v1/onboarding/start", json={})
        assert r.status_code == 422


class TestAdvanceStepEndpoint:
    def test_advance_valid_step_returns_200(self):
        body = {"step_id": "OB-001"}
        r = client.post("/api/v1/onboarding/ONB-002/step", json=body)
        assert r.status_code in (200, 409)  # 409 if already completed

    def test_unknown_client_returns_404(self):
        body = {"step_id": "OB-001"}
        r = client.post("/api/v1/onboarding/UNKNOWN-999/step", json=body)
        assert r.status_code == 404

    def test_unknown_step_returns_404(self):
        body = {"step_id": "OB-INVALID"}
        r = client.post("/api/v1/onboarding/ONB-001/step", json=body)
        assert r.status_code == 404

    def test_completed_step_returns_completion_pct(self):
        body = {"step_id": "OB-001"}
        r = client.post("/api/v1/onboarding/ONB-003/step", json=body)
        if r.status_code == 200:
            data = r.json()
            assert "completion_pct" in data
            assert 0 <= data["completion_pct"] <= 100


class TestMetricsEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/onboarding/metrics").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/onboarding/metrics").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_avg_days_to_sprint_start(self):
        data = client.get("/api/v1/onboarding/metrics").json()
        assert "avg_days_to_sprint_start" in data
        assert data["avg_days_to_sprint_start"] > 0

    def test_has_completion_rate(self):
        data = client.get("/api/v1/onboarding/metrics").json()
        assert "completion_rate_pct" in data
        assert 0 <= data["completion_rate_pct"] <= 100

    def test_has_bottleneck_note(self):
        data = client.get("/api/v1/onboarding/metrics").json()
        assert "note_ar" in data
        assert "note_en" in data

    def test_has_step_timings(self):
        data = client.get("/api/v1/onboarding/metrics").json()
        assert "step_timings" in data
        assert len(data["step_timings"]) > 0
