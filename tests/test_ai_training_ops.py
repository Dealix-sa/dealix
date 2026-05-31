"""Tests for /api/v1/ai-training — AI training pipeline management endpoints.

Covers:
  - Demo data integrity (6 training jobs, 4 deployed models)
  - GET /jobs (list, filter by status/model_type/sector)
  - GET /jobs/active (running + queued)
  - GET /jobs/{job_id} (detail, 404)
  - POST /jobs/{job_id}/pause (success, 409 conflicts, 404)
  - POST /jobs/{job_id}/resume (success, 409 conflicts, 404)
  - POST /jobs/{job_id}/cancel (success from all cancellable statuses, 409, 404)
  - GET /models (list)
  - GET /models/{model_id} (detail, 404)
  - GET /performance-report (aggregate metrics)
  - GET /data-compliance (PDPL compliance report)
  - governance_decision field present on all responses
  - Helper function unit tests
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

from api.routers.ai_training_ops import (  # noqa: E402
    DEPLOYED_MODELS,
    TRAINING_JOBS,
    _CANCELLABLE_STATUSES,
    _PAUSABLE_STATUSES,
    _RESUMABLE_STATUSES,
    _STATE_LOG,
    _TERMINAL_STATUSES,
    _compute_avg_accuracy_completed,
    _compute_avg_latency_live,
    _compute_pdpl_compliance_rate,
    _compute_total_requests_today,
    _count_by_status,
    _now_iso,
    _today_iso,
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
def _reset_job_statuses():
    """Restore original job statuses and clear state log after each test."""
    original_statuses = {jid: j["status"] for jid, j in TRAINING_JOBS.items()}
    yield
    for jid, status in original_statuses.items():
        TRAINING_JOBS[jid]["status"] = status
    _STATE_LOG.clear()


# ===========================================================================
# 1. Demo data integrity
# ===========================================================================


class TestDemoDataIntegrity:
    def test_training_jobs_has_6_entries(self):
        assert len(TRAINING_JOBS) == 6

    def test_job_ids_are_trj_001_to_006(self):
        expected = {"TRJ-001", "TRJ-002", "TRJ-003", "TRJ-004", "TRJ-005", "TRJ-006"}
        assert set(TRAINING_JOBS.keys()) == expected

    def test_each_job_has_required_fields(self):
        required = {
            "id", "name", "model_type", "status", "dataset_size", "epochs_total",
            "epochs_completed", "training_time_hours", "base_model", "language",
            "sector", "created_at", "pdpl_compliant", "data_residency",
        }
        for jid, job in TRAINING_JOBS.items():
            for field in required:
                assert field in job, f"Job {jid} missing field '{field}'"

    def test_all_jobs_are_pdpl_compliant(self):
        for jid, job in TRAINING_JOBS.items():
            assert job["pdpl_compliant"] is True, f"Job {jid} not PDPL compliant"

    def test_all_jobs_use_sa_east_1_residency(self):
        for jid, job in TRAINING_JOBS.items():
            assert job["data_residency"] == "sa-east-1", f"Job {jid} wrong residency"

    def test_all_jobs_use_arabic_language(self):
        for jid, job in TRAINING_JOBS.items():
            assert job["language"] == "ar", f"Job {jid} wrong language"

    def test_trj001_is_completed(self):
        assert TRAINING_JOBS["TRJ-001"]["status"] == "completed"

    def test_trj002_is_running(self):
        assert TRAINING_JOBS["TRJ-002"]["status"] == "running"

    def test_trj003_is_completed(self):
        assert TRAINING_JOBS["TRJ-003"]["status"] == "completed"

    def test_trj004_is_queued(self):
        assert TRAINING_JOBS["TRJ-004"]["status"] == "queued"

    def test_trj005_is_failed(self):
        assert TRAINING_JOBS["TRJ-005"]["status"] == "failed"

    def test_trj006_is_paused(self):
        assert TRAINING_JOBS["TRJ-006"]["status"] == "paused"

    def test_deployed_models_has_4_entries(self):
        assert len(DEPLOYED_MODELS) == 4

    def test_model_ids_are_mdl_001_to_004(self):
        expected = {"MDL-001", "MDL-002", "MDL-003", "MDL-004"}
        assert set(DEPLOYED_MODELS.keys()) == expected

    def test_three_live_models(self):
        live = [m for m in DEPLOYED_MODELS.values() if m["status"] == "live"]
        assert len(live) == 3

    def test_one_deprecated_model(self):
        deprecated = [m for m in DEPLOYED_MODELS.values() if m["status"] == "deprecated"]
        assert len(deprecated) == 1

    def test_each_model_has_required_fields(self):
        required = {
            "id", "name", "endpoint", "status", "requests_today",
            "requests_total", "avg_latency_ms", "uptime_pct", "version", "deployed_at",
        }
        for mid, model in DEPLOYED_MODELS.items():
            for field in required:
                assert field in model, f"Model {mid} missing field '{field}'"

    def test_mdl004_is_deprecated(self):
        assert DEPLOYED_MODELS["MDL-004"]["status"] == "deprecated"


# ===========================================================================
# 2. Helper function unit tests
# ===========================================================================


class TestNowIso:
    def test_returns_string(self):
        assert isinstance(_now_iso(), str)

    def test_contains_t_separator(self):
        assert "T" in _now_iso()

    def test_ends_with_utc_offset(self):
        result = _now_iso()
        assert "+00:00" in result or result.endswith("Z")


class TestTodayIso:
    def test_returns_string(self):
        assert isinstance(_today_iso(), str)

    def test_format_is_date(self):
        result = _today_iso()
        parts = result.split("-")
        assert len(parts) == 3
        assert len(parts[0]) == 4  # year

    def test_no_time_component(self):
        result = _today_iso()
        assert "T" not in result


class TestComputeAvgAccuracyCompleted:
    def test_returns_float(self):
        result = _compute_avg_accuracy_completed(TRAINING_JOBS)
        assert isinstance(result, float)

    def test_value_in_range(self):
        result = _compute_avg_accuracy_completed(TRAINING_JOBS)
        assert 0.0 <= result <= 1.0

    def test_empty_jobs_returns_zero(self):
        assert _compute_avg_accuracy_completed({}) == 0.0

    def test_only_completed_jobs_counted(self):
        jobs = {
            "A": {"status": "completed", "accuracy": 0.9},
            "B": {"status": "running", "accuracy": 0.5},
        }
        result = _compute_avg_accuracy_completed(jobs)
        assert result == 0.9

    def test_none_accuracy_excluded(self):
        jobs = {
            "A": {"status": "completed", "accuracy": 0.8},
            "B": {"status": "completed", "accuracy": None},
        }
        result = _compute_avg_accuracy_completed(jobs)
        assert result == 0.8

    def test_result_matches_manual_calc(self):
        # TRJ-001 accuracy=0.924, TRJ-003 accuracy=0.879
        result = _compute_avg_accuracy_completed(TRAINING_JOBS)
        expected = round((0.924 + 0.879) / 2, 3)
        assert result == expected


class TestComputePdplComplianceRate:
    def test_returns_float(self):
        result = _compute_pdpl_compliance_rate(TRAINING_JOBS)
        assert isinstance(result, float)

    def test_all_compliant_returns_one(self):
        jobs = {
            "A": {"pdpl_compliant": True},
            "B": {"pdpl_compliant": True},
        }
        assert _compute_pdpl_compliance_rate(jobs) == 1.0

    def test_none_compliant_returns_zero(self):
        jobs = {
            "A": {"pdpl_compliant": False},
            "B": {"pdpl_compliant": False},
        }
        assert _compute_pdpl_compliance_rate(jobs) == 0.0

    def test_empty_returns_zero(self):
        assert _compute_pdpl_compliance_rate({}) == 0.0

    def test_demo_data_is_fully_compliant(self):
        assert _compute_pdpl_compliance_rate(TRAINING_JOBS) == 1.0


class TestComputeTotalRequestsToday:
    def test_returns_int(self):
        result = _compute_total_requests_today(DEPLOYED_MODELS)
        assert isinstance(result, int)

    def test_is_sum_of_all_models(self):
        expected = sum(m["requests_today"] for m in DEPLOYED_MODELS.values())
        assert _compute_total_requests_today(DEPLOYED_MODELS) == expected

    def test_empty_returns_zero(self):
        assert _compute_total_requests_today({}) == 0


class TestComputeAvgLatencyLive:
    def test_returns_float(self):
        result = _compute_avg_latency_live(DEPLOYED_MODELS)
        assert isinstance(result, float)

    def test_only_live_models_counted(self):
        models = {
            "A": {"status": "live", "avg_latency_ms": 100},
            "B": {"status": "deprecated", "avg_latency_ms": 200},
        }
        result = _compute_avg_latency_live(models)
        assert result == 100.0

    def test_empty_returns_zero(self):
        assert _compute_avg_latency_live({}) == 0.0

    def test_result_positive(self):
        assert _compute_avg_latency_live(DEPLOYED_MODELS) > 0.0


class TestCountByStatus:
    def test_returns_dict(self):
        result = _count_by_status(TRAINING_JOBS)
        assert isinstance(result, dict)

    def test_all_statuses_counted(self):
        result = _count_by_status(TRAINING_JOBS)
        assert result.get("completed", 0) == 2
        assert result.get("running", 0) == 1
        assert result.get("queued", 0) == 1
        assert result.get("failed", 0) == 1
        assert result.get("paused", 0) == 1

    def test_totals_sum_to_job_count(self):
        result = _count_by_status(TRAINING_JOBS)
        assert sum(result.values()) == len(TRAINING_JOBS)

    def test_empty_returns_empty_dict(self):
        assert _count_by_status({}) == {}


# ===========================================================================
# 3. GET /jobs — list all training jobs
# ===========================================================================


class TestJobList:
    def test_status_200(self):
        r = client.get("/api/v1/ai-training/jobs")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/ai-training/jobs")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_is_6(self):
        r = client.get("/api/v1/ai-training/jobs")
        assert r.json()["total"] == 6

    def test_jobs_list_has_6_items(self):
        r = client.get("/api/v1/ai-training/jobs")
        assert len(r.json()["jobs"]) == 6

    def test_generated_at_present(self):
        r = client.get("/api/v1/ai-training/jobs")
        assert "generated_at" in r.json()

    def test_filter_by_status_completed(self):
        r = client.get("/api/v1/ai-training/jobs?status=completed")
        data = r.json()
        assert data["total"] == 2
        for job in data["jobs"]:
            assert job["status"] == "completed"

    def test_filter_by_status_running(self):
        r = client.get("/api/v1/ai-training/jobs?status=running")
        data = r.json()
        assert data["total"] == 1
        assert data["jobs"][0]["status"] == "running"

    def test_filter_by_status_queued(self):
        r = client.get("/api/v1/ai-training/jobs?status=queued")
        data = r.json()
        assert data["total"] == 1
        assert data["jobs"][0]["status"] == "queued"

    def test_filter_by_status_failed(self):
        r = client.get("/api/v1/ai-training/jobs?status=failed")
        data = r.json()
        assert data["total"] == 1
        assert data["jobs"][0]["status"] == "failed"

    def test_filter_by_status_paused(self):
        r = client.get("/api/v1/ai-training/jobs?status=paused")
        data = r.json()
        assert data["total"] == 1
        assert data["jobs"][0]["status"] == "paused"

    def test_filter_by_model_type_classification(self):
        r = client.get("/api/v1/ai-training/jobs?model_type=classification")
        data = r.json()
        assert data["total"] == 2
        for job in data["jobs"]:
            assert job["model_type"] == "classification"

    def test_filter_by_model_type_regression(self):
        r = client.get("/api/v1/ai-training/jobs?model_type=regression")
        data = r.json()
        assert data["total"] == 1

    def test_filter_by_model_type_vision(self):
        r = client.get("/api/v1/ai-training/jobs?model_type=vision")
        data = r.json()
        assert data["total"] == 1
        assert data["jobs"][0]["id"] == "TRJ-005"

    def test_filter_by_sector_fintech(self):
        r = client.get("/api/v1/ai-training/jobs?sector=fintech")
        data = r.json()
        assert data["total"] == 2
        for job in data["jobs"]:
            assert job["sector"] == "fintech"

    def test_filter_by_sector_healthcare(self):
        r = client.get("/api/v1/ai-training/jobs?sector=healthcare")
        data = r.json()
        assert data["total"] == 1

    def test_filter_nonexistent_status_returns_empty(self):
        r = client.get("/api/v1/ai-training/jobs?status=nonexistent")
        data = r.json()
        assert data["total"] == 0
        assert data["jobs"] == []

    def test_each_job_has_pdpl_compliant_field(self):
        r = client.get("/api/v1/ai-training/jobs")
        for job in r.json()["jobs"]:
            assert "pdpl_compliant" in job

    def test_each_job_has_data_residency(self):
        r = client.get("/api/v1/ai-training/jobs")
        for job in r.json()["jobs"]:
            assert job["data_residency"] == "sa-east-1"


# ===========================================================================
# 4. GET /jobs/active — running + queued jobs
# ===========================================================================


class TestActiveJobs:
    def test_status_200(self):
        r = client.get("/api/v1/ai-training/jobs/active")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/ai-training/jobs/active")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_active_job_count_is_2(self):
        r = client.get("/api/v1/ai-training/jobs/active")
        data = r.json()
        assert data["active_job_count"] == 2

    def test_jobs_list_has_2_items(self):
        r = client.get("/api/v1/ai-training/jobs/active")
        data = r.json()
        assert len(data["jobs"]) == 2

    def test_all_active_jobs_are_running_or_queued(self):
        r = client.get("/api/v1/ai-training/jobs/active")
        for job in r.json()["jobs"]:
            assert job["status"] in ("running", "queued")

    def test_no_completed_jobs_in_active(self):
        r = client.get("/api/v1/ai-training/jobs/active")
        statuses = [j["status"] for j in r.json()["jobs"]]
        assert "completed" not in statuses

    def test_no_failed_jobs_in_active(self):
        r = client.get("/api/v1/ai-training/jobs/active")
        statuses = [j["status"] for j in r.json()["jobs"]]
        assert "failed" not in statuses

    def test_no_paused_jobs_in_active(self):
        r = client.get("/api/v1/ai-training/jobs/active")
        statuses = [j["status"] for j in r.json()["jobs"]]
        assert "paused" not in statuses

    def test_generated_at_present(self):
        r = client.get("/api/v1/ai-training/jobs/active")
        assert "generated_at" in r.json()


# ===========================================================================
# 5. GET /jobs/{job_id} — single job detail
# ===========================================================================


class TestJobDetail:
    def test_status_200_for_existing_job(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-001")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-001")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_id_matches_requested_job(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-001")
        assert r.json()["id"] == "TRJ-001"

    def test_trj001_name(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-001")
        assert r.json()["name"] == "customer_intent_classifier_v3"

    def test_trj001_accuracy(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-001")
        assert r.json()["accuracy"] == 0.924

    def test_trj002_status_running(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-002")
        assert r.json()["status"] == "running"

    def test_trj004_epochs_completed_zero(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-004")
        assert r.json()["epochs_completed"] == 0

    def test_trj005_status_failed(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-005")
        assert r.json()["status"] == "failed"

    def test_404_for_unknown_job(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-999")
        assert r.status_code == 404

    def test_404_error_has_job_id(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-999")
        assert "TRJ-999" in str(r.json())

    def test_generated_at_present(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-001")
        assert "generated_at" in r.json()

    def test_pdpl_compliant_true(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-001")
        assert r.json()["pdpl_compliant"] is True

    def test_data_residency_sa_east_1(self):
        r = client.get("/api/v1/ai-training/jobs/TRJ-001")
        assert r.json()["data_residency"] == "sa-east-1"


# ===========================================================================
# 6. POST /jobs/{job_id}/pause
# ===========================================================================


class TestJobPause:
    def test_pause_running_job_returns_200(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "Maintenance window required"},
        )
        assert r.status_code == 200

    def test_pause_returns_approval_first(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "Maintenance window required"},
        )
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_pause_returns_paused_new_status(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "Maintenance window required"},
        )
        assert r.json()["new_status"] == "paused"

    def test_pause_updates_job_status(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "Maintenance window required"},
        )
        assert TRAINING_JOBS["TRJ-002"]["status"] == "paused"

    def test_pause_returns_job_id(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "Maintenance window required"},
        )
        assert r.json()["job_id"] == "TRJ-002"

    def test_pause_returns_reason(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "Maintenance window required"},
        )
        assert r.json()["reason"] == "Maintenance window required"

    def test_pause_returns_actioned_at(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "Maintenance window required"},
        )
        assert "actioned_at" in r.json()

    def test_pause_logs_state_change(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "Maintenance window required"},
        )
        assert len(_STATE_LOG) == 1
        assert _STATE_LOG[0]["action"] == "pause"

    def test_pause_completed_job_returns_409(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-001/pause",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 409

    def test_pause_paused_job_returns_409(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-006/pause",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 409

    def test_pause_failed_job_returns_409(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-005/pause",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 409

    def test_pause_queued_job_returns_409(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-004/pause",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 409

    def test_pause_nonexistent_job_returns_404(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-999/pause",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 404

    def test_pause_409_includes_current_status(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-001/pause",
            json={"reason": "Test reason here"},
        )
        detail = r.json()["detail"]
        assert detail["current_status"] == "completed"

    def test_pause_missing_reason_returns_422(self):
        r = client.post("/api/v1/ai-training/jobs/TRJ-002/pause", json={})
        assert r.status_code == 422

    def test_pause_short_reason_returns_422(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "Hi"},
        )
        assert r.status_code == 422


# ===========================================================================
# 7. POST /jobs/{job_id}/resume
# ===========================================================================


class TestJobResume:
    def test_resume_paused_job_returns_200(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-006/resume",
            json={"reason": "Data augmentation completed successfully"},
        )
        assert r.status_code == 200

    def test_resume_returns_approval_first(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-006/resume",
            json={"reason": "Data augmentation completed successfully"},
        )
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_resume_returns_running_new_status(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-006/resume",
            json={"reason": "Data augmentation completed successfully"},
        )
        assert r.json()["new_status"] == "running"

    def test_resume_updates_job_status(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-006/resume",
            json={"reason": "Data augmentation completed successfully"},
        )
        assert TRAINING_JOBS["TRJ-006"]["status"] == "running"

    def test_resume_returns_job_id(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-006/resume",
            json={"reason": "Data augmentation completed successfully"},
        )
        assert r.json()["job_id"] == "TRJ-006"

    def test_resume_returns_actioned_at(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-006/resume",
            json={"reason": "Data augmentation completed successfully"},
        )
        assert "actioned_at" in r.json()

    def test_resume_logs_state_change(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-006/resume",
            json={"reason": "Data augmentation completed successfully"},
        )
        assert len(_STATE_LOG) == 1
        assert _STATE_LOG[0]["action"] == "resume"

    def test_resume_running_job_returns_409(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-002/resume",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 409

    def test_resume_completed_job_returns_409(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-001/resume",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 409

    def test_resume_failed_job_returns_409(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-005/resume",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 409

    def test_resume_queued_job_returns_409(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-004/resume",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 409

    def test_resume_nonexistent_job_returns_404(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-999/resume",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 404

    def test_resume_409_includes_current_status(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-002/resume",
            json={"reason": "Test reason here"},
        )
        detail = r.json()["detail"]
        assert detail["current_status"] == "running"

    def test_resume_missing_reason_returns_422(self):
        r = client.post("/api/v1/ai-training/jobs/TRJ-006/resume", json={})
        assert r.status_code == 422


# ===========================================================================
# 8. POST /jobs/{job_id}/cancel
# ===========================================================================


class TestJobCancel:
    def test_cancel_queued_job_returns_200(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-004/cancel",
            json={"reason": "Budget constraints — deferring to next quarter"},
        )
        assert r.status_code == 200

    def test_cancel_running_job_returns_200(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-002/cancel",
            json={"reason": "Budget constraints — deferring to next quarter"},
        )
        assert r.status_code == 200

    def test_cancel_paused_job_returns_200(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-006/cancel",
            json={"reason": "Budget constraints — deferring to next quarter"},
        )
        assert r.status_code == 200

    def test_cancel_returns_approval_first(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-004/cancel",
            json={"reason": "Budget constraints — deferring to next quarter"},
        )
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_cancel_returns_cancelled_new_status(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-004/cancel",
            json={"reason": "Budget constraints — deferring to next quarter"},
        )
        assert r.json()["new_status"] == "cancelled"

    def test_cancel_updates_job_status(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-004/cancel",
            json={"reason": "Budget constraints — deferring to next quarter"},
        )
        assert TRAINING_JOBS["TRJ-004"]["status"] == "cancelled"

    def test_cancel_returns_job_id(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-004/cancel",
            json={"reason": "Budget constraints — deferring to next quarter"},
        )
        assert r.json()["job_id"] == "TRJ-004"

    def test_cancel_returns_actioned_at(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-004/cancel",
            json={"reason": "Budget constraints — deferring to next quarter"},
        )
        assert "actioned_at" in r.json()

    def test_cancel_logs_state_change(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-004/cancel",
            json={"reason": "Budget constraints — deferring to next quarter"},
        )
        assert any(entry["action"] == "cancel" for entry in _STATE_LOG)

    def test_cancel_completed_job_returns_409(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-001/cancel",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 409

    def test_cancel_failed_job_returns_409(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-005/cancel",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 409

    def test_cancel_nonexistent_job_returns_404(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-999/cancel",
            json={"reason": "Test reason here"},
        )
        assert r.status_code == 404

    def test_cancel_409_includes_current_status(self):
        r = client.post(
            "/api/v1/ai-training/jobs/TRJ-001/cancel",
            json={"reason": "Test reason here"},
        )
        detail = r.json()["detail"]
        assert detail["current_status"] == "completed"

    def test_cancel_missing_reason_returns_422(self):
        r = client.post("/api/v1/ai-training/jobs/TRJ-004/cancel", json={})
        assert r.status_code == 422


# ===========================================================================
# 9. GET /models — list deployed models
# ===========================================================================


class TestModelList:
    def test_status_200(self):
        r = client.get("/api/v1/ai-training/models")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/ai-training/models")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_is_4(self):
        r = client.get("/api/v1/ai-training/models")
        assert r.json()["total"] == 4

    def test_models_list_has_4_items(self):
        r = client.get("/api/v1/ai-training/models")
        assert len(r.json()["models"]) == 4

    def test_generated_at_present(self):
        r = client.get("/api/v1/ai-training/models")
        assert "generated_at" in r.json()

    def test_each_model_has_id(self):
        r = client.get("/api/v1/ai-training/models")
        for model in r.json()["models"]:
            assert "id" in model

    def test_each_model_has_status(self):
        r = client.get("/api/v1/ai-training/models")
        for model in r.json()["models"]:
            assert "status" in model

    def test_each_model_has_endpoint(self):
        r = client.get("/api/v1/ai-training/models")
        for model in r.json()["models"]:
            assert "endpoint" in model

    def test_three_models_are_live(self):
        r = client.get("/api/v1/ai-training/models")
        live = [m for m in r.json()["models"] if m["status"] == "live"]
        assert len(live) == 3

    def test_one_model_is_deprecated(self):
        r = client.get("/api/v1/ai-training/models")
        deprecated = [m for m in r.json()["models"] if m["status"] == "deprecated"]
        assert len(deprecated) == 1


# ===========================================================================
# 10. GET /models/{model_id} — single model detail
# ===========================================================================


class TestModelDetail:
    def test_status_200_for_existing_model(self):
        r = client.get("/api/v1/ai-training/models/MDL-001")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/ai-training/models/MDL-001")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_id_matches_requested_model(self):
        r = client.get("/api/v1/ai-training/models/MDL-001")
        assert r.json()["id"] == "MDL-001"

    def test_mdl001_name(self):
        r = client.get("/api/v1/ai-training/models/MDL-001")
        assert r.json()["name"] == "customer_intent_classifier_v3"

    def test_mdl001_status_live(self):
        r = client.get("/api/v1/ai-training/models/MDL-001")
        assert r.json()["status"] == "live"

    def test_mdl004_status_deprecated(self):
        r = client.get("/api/v1/ai-training/models/MDL-004")
        assert r.json()["status"] == "deprecated"

    def test_mdl001_uptime(self):
        r = client.get("/api/v1/ai-training/models/MDL-001")
        assert r.json()["uptime_pct"] == 99.94

    def test_404_for_unknown_model(self):
        r = client.get("/api/v1/ai-training/models/MDL-999")
        assert r.status_code == 404

    def test_404_error_has_model_id(self):
        r = client.get("/api/v1/ai-training/models/MDL-999")
        assert "MDL-999" in str(r.json())

    def test_generated_at_present(self):
        r = client.get("/api/v1/ai-training/models/MDL-001")
        assert "generated_at" in r.json()

    def test_mdl003_training_job_id_is_none(self):
        r = client.get("/api/v1/ai-training/models/MDL-003")
        assert r.json()["training_job_id"] is None

    def test_mdl001_training_job_id_is_trj001(self):
        r = client.get("/api/v1/ai-training/models/MDL-001")
        assert r.json()["training_job_id"] == "TRJ-001"


# ===========================================================================
# 11. GET /performance-report
# ===========================================================================


class TestPerformanceReport:
    def test_status_200(self):
        r = client.get("/api/v1/ai-training/performance-report")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/ai-training/performance-report")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_jobs_is_6(self):
        r = client.get("/api/v1/ai-training/performance-report")
        assert r.json()["total_jobs"] == 6

    def test_deployed_models_is_4(self):
        r = client.get("/api/v1/ai-training/performance-report")
        assert r.json()["deployed_models"] == 4

    def test_live_models_is_3(self):
        r = client.get("/api/v1/ai-training/performance-report")
        assert r.json()["live_models"] == 3

    def test_by_status_has_all_statuses(self):
        r = client.get("/api/v1/ai-training/performance-report")
        by_status = r.json()["by_status"]
        assert by_status.get("completed") == 2
        assert by_status.get("running") == 1
        assert by_status.get("queued") == 1
        assert by_status.get("failed") == 1
        assert by_status.get("paused") == 1

    def test_avg_accuracy_completed_is_correct(self):
        r = client.get("/api/v1/ai-training/performance-report")
        expected = round((0.924 + 0.879) / 2, 3)
        assert r.json()["avg_accuracy_completed"] == expected

    def test_data_residency_sa_east_1(self):
        r = client.get("/api/v1/ai-training/performance-report")
        assert r.json()["data_residency"] == "sa-east-1"

    def test_pdpl_compliance_rate_is_1(self):
        r = client.get("/api/v1/ai-training/performance-report")
        assert r.json()["pdpl_compliance_rate"] == 1.0

    def test_total_requests_today_is_correct(self):
        r = client.get("/api/v1/ai-training/performance-report")
        expected = sum(m["requests_today"] for m in DEPLOYED_MODELS.values())
        assert r.json()["total_requests_today"] == expected

    def test_avg_latency_ms_is_positive(self):
        r = client.get("/api/v1/ai-training/performance-report")
        assert r.json()["avg_latency_ms"] > 0

    def test_report_date_present(self):
        r = client.get("/api/v1/ai-training/performance-report")
        assert "report_date" in r.json()
        assert r.json()["report_date"]

    def test_report_date_is_date_string(self):
        r = client.get("/api/v1/ai-training/performance-report")
        report_date = r.json()["report_date"]
        parts = report_date.split("-")
        assert len(parts) == 3


# ===========================================================================
# 12. GET /data-compliance
# ===========================================================================


class TestDataCompliance:
    def test_status_200(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_pdpl_compliant_jobs_is_6(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.json()["pdpl_compliant_jobs"] == 6

    def test_total_jobs_is_6(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.json()["total_jobs"] == 6

    def test_compliance_rate_is_1(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.json()["compliance_rate"] == 1.0

    def test_data_residency_sa_east_1(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.json()["data_residency"] == "sa-east-1"

    def test_retention_policy_365(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.json()["retention_policy_days"] == 365

    def test_audit_log_is_true(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.json()["audit_log"] is True

    def test_right_to_erasure_is_true(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.json()["right_to_erasure"] is True

    def test_consent_required_is_true(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.json()["consent_required"] is True

    def test_cross_border_transfer_is_false(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert r.json()["cross_border_transfer"] is False

    def test_jobs_list_has_6_items(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        assert len(r.json()["jobs"]) == 6

    def test_each_job_has_pdpl_compliant(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        for job in r.json()["jobs"]:
            assert "pdpl_compliant" in job

    def test_each_job_has_data_residency(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        for job in r.json()["jobs"]:
            assert job["data_residency"] == "sa-east-1"

    def test_each_job_has_id(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        for job in r.json()["jobs"]:
            assert "id" in job

    def test_each_job_has_status(self):
        r = client.get("/api/v1/ai-training/data-compliance")
        for job in r.json()["jobs"]:
            assert "status" in job


# ===========================================================================
# 13. Constant / set membership tests
# ===========================================================================


class TestStatusSets:
    def test_pausable_contains_running(self):
        assert "running" in _PAUSABLE_STATUSES

    def test_resumable_contains_paused(self):
        assert "paused" in _RESUMABLE_STATUSES

    def test_cancellable_contains_queued_running_paused(self):
        assert "queued" in _CANCELLABLE_STATUSES
        assert "running" in _CANCELLABLE_STATUSES
        assert "paused" in _CANCELLABLE_STATUSES

    def test_terminal_contains_completed_failed(self):
        assert "completed" in _TERMINAL_STATUSES
        assert "failed" in _TERMINAL_STATUSES

    def test_cancellable_and_terminal_are_disjoint(self):
        assert _CANCELLABLE_STATUSES.isdisjoint(_TERMINAL_STATUSES)

    def test_pausable_and_terminal_are_disjoint(self):
        assert _PAUSABLE_STATUSES.isdisjoint(_TERMINAL_STATUSES)

    def test_resumable_and_terminal_are_disjoint(self):
        assert _RESUMABLE_STATUSES.isdisjoint(_TERMINAL_STATUSES)


# ===========================================================================
# 14. State log audit trail
# ===========================================================================


class TestStateLog:
    def test_state_log_records_pause(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "GPU reallocation needed now"},
        )
        assert any(e["action"] == "pause" and e["job_id"] == "TRJ-002" for e in _STATE_LOG)

    def test_state_log_records_resume(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-006/resume",
            json={"reason": "Data augmentation completed now"},
        )
        assert any(e["action"] == "resume" and e["job_id"] == "TRJ-006" for e in _STATE_LOG)

    def test_state_log_records_cancel(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-004/cancel",
            json={"reason": "Budget constraint confirmed now"},
        )
        assert any(e["action"] == "cancel" and e["job_id"] == "TRJ-004" for e in _STATE_LOG)

    def test_state_log_entry_has_reason(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "GPU reallocation needed today"},
        )
        assert _STATE_LOG[0]["reason"] == "GPU reallocation needed today"

    def test_state_log_entry_has_logged_at(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-002/pause",
            json={"reason": "GPU reallocation needed today"},
        )
        assert "logged_at" in _STATE_LOG[0]

    def test_failed_action_does_not_pollute_state_log(self):
        client.post(
            "/api/v1/ai-training/jobs/TRJ-001/pause",
            json={"reason": "Test reason here for long"},
        )
        assert len(_STATE_LOG) == 0
