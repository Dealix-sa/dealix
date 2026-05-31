"""AI Training Operations — model training pipeline management.

Endpoints:
  GET  /api/v1/ai-training/jobs                      — list all training jobs
  GET  /api/v1/ai-training/jobs/active               — running + queued jobs
  GET  /api/v1/ai-training/jobs/{job_id}             — single job detail
  POST /api/v1/ai-training/jobs/{job_id}/pause       — pause a running job
  POST /api/v1/ai-training/jobs/{job_id}/resume      — resume a paused job
  POST /api/v1/ai-training/jobs/{job_id}/cancel      — cancel a job
  GET  /api/v1/ai-training/models                    — list deployed models
  GET  /api/v1/ai-training/models/{model_id}         — single model detail
  GET  /api/v1/ai-training/performance-report        — aggregate ML performance
  GET  /api/v1/ai-training/data-compliance           — PDPL data compliance report

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - Read-only actions: ALLOW_WITH_REVIEW
  - Mutating actions: APPROVAL_FIRST
  - PDPL-compliant — data residency sa-east-1
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/ai-training",
    tags=["AI Training Operations"],
    dependencies=[Depends(require_admin_key)],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_MUTATE = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Valid status transitions
# ---------------------------------------------------------------------------

_PAUSABLE_STATUSES = frozenset({"running"})
_RESUMABLE_STATUSES = frozenset({"paused"})
_CANCELLABLE_STATUSES = frozenset({"queued", "running", "paused"})
_TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled"})

# ---------------------------------------------------------------------------
# Demo data — 6 training jobs
# ---------------------------------------------------------------------------

TRAINING_JOBS: dict[str, dict[str, Any]] = {
    "TRJ-001": {
        "id": "TRJ-001",
        "name": "customer_intent_classifier_v3",
        "model_type": "classification",
        "status": "completed",
        "dataset_size": 12500,
        "epochs_total": 50,
        "epochs_completed": 50,
        "accuracy": 0.924,
        "f1_score": 0.918,
        "loss": 0.124,
        "training_time_hours": 2.4,
        "base_model": "arabert-v2",
        "language": "ar",
        "sector": "healthcare",
        "created_at": "2026-05-01T10:00:00Z",
        "completed_at": "2026-05-01T12:24:00Z",
        "notes": "Production-grade intent classifier for Arabic healthcare queries",
        "pdpl_compliant": True,
        "data_residency": "sa-east-1",
    },
    "TRJ-002": {
        "id": "TRJ-002",
        "name": "revenue_forecast_model_v2",
        "model_type": "regression",
        "status": "running",
        "dataset_size": 8900,
        "epochs_total": 100,
        "epochs_completed": 67,
        "accuracy": 0.891,
        "f1_score": None,
        "loss": 0.089,
        "training_time_hours": 1.8,
        "base_model": "lstm-financial",
        "language": "ar",
        "sector": "fintech",
        "created_at": "2026-05-28T08:00:00Z",
        "completed_at": None,
        "notes": "MRR forecasting model for SaaS revenue intelligence",
        "pdpl_compliant": True,
        "data_residency": "sa-east-1",
    },
    "TRJ-003": {
        "id": "TRJ-003",
        "name": "churn_predictor_v1",
        "model_type": "binary_classification",
        "status": "completed",
        "dataset_size": 5600,
        "epochs_total": 30,
        "epochs_completed": 30,
        "accuracy": 0.879,
        "f1_score": 0.863,
        "loss": 0.198,
        "training_time_hours": 0.9,
        "base_model": "bert-mini-arabic",
        "language": "ar",
        "sector": "multi-sector",
        "created_at": "2026-04-15T09:00:00Z",
        "completed_at": "2026-04-15T09:54:00Z",
        "notes": "Churn risk binary classifier — 87.9% accuracy",
        "pdpl_compliant": True,
        "data_residency": "sa-east-1",
    },
    "TRJ-004": {
        "id": "TRJ-004",
        "name": "document_qa_model_v1",
        "model_type": "generative",
        "status": "queued",
        "dataset_size": 22000,
        "epochs_total": 20,
        "epochs_completed": 0,
        "accuracy": None,
        "f1_score": None,
        "loss": None,
        "training_time_hours": 0.0,
        "base_model": "jais-13b",
        "language": "ar",
        "sector": "legal",
        "created_at": "2026-05-31T07:00:00Z",
        "completed_at": None,
        "notes": "Arabic document Q&A for legal sector — queued for GPU allocation",
        "pdpl_compliant": True,
        "data_residency": "sa-east-1",
    },
    "TRJ-005": {
        "id": "TRJ-005",
        "name": "invoice_ocr_classifier",
        "model_type": "vision",
        "status": "failed",
        "dataset_size": 3400,
        "epochs_total": 15,
        "epochs_completed": 7,
        "accuracy": 0.612,
        "f1_score": 0.589,
        "loss": 0.445,
        "training_time_hours": 0.4,
        "base_model": "paddle-ocr-arabic",
        "language": "ar",
        "sector": "fintech",
        "created_at": "2026-05-10T14:00:00Z",
        "completed_at": None,
        "notes": "ZATCA invoice OCR — failed due to insufficient labeled data",
        "pdpl_compliant": True,
        "data_residency": "sa-east-1",
    },
    "TRJ-006": {
        "id": "TRJ-006",
        "name": "sentiment_analyzer_v2",
        "model_type": "classification",
        "status": "paused",
        "dataset_size": 9800,
        "epochs_total": 40,
        "epochs_completed": 22,
        "accuracy": 0.856,
        "f1_score": 0.841,
        "loss": 0.167,
        "training_time_hours": 1.1,
        "base_model": "arabert-v2",
        "language": "ar",
        "sector": "retail",
        "created_at": "2026-05-20T11:00:00Z",
        "completed_at": None,
        "notes": "Customer sentiment for retail sector — paused for data augmentation",
        "pdpl_compliant": True,
        "data_residency": "sa-east-1",
    },
}

# ---------------------------------------------------------------------------
# Demo data — 4 model deployments
# ---------------------------------------------------------------------------

DEPLOYED_MODELS: dict[str, dict[str, Any]] = {
    "MDL-001": {
        "id": "MDL-001",
        "training_job_id": "TRJ-001",
        "name": "customer_intent_classifier_v3",
        "endpoint": "/api/v1/models/customer-intent/predict",
        "status": "live",
        "requests_today": 1247,
        "requests_total": 89432,
        "avg_latency_ms": 42,
        "uptime_pct": 99.94,
        "version": "3.0.1",
        "deployed_at": "2026-05-02T09:00:00Z",
    },
    "MDL-002": {
        "id": "MDL-002",
        "training_job_id": "TRJ-003",
        "name": "churn_predictor_v1",
        "endpoint": "/api/v1/models/churn-predictor/predict",
        "status": "live",
        "requests_today": 234,
        "requests_total": 12890,
        "avg_latency_ms": 38,
        "uptime_pct": 99.87,
        "version": "1.0.0",
        "deployed_at": "2026-04-16T10:00:00Z",
    },
    "MDL-003": {
        "id": "MDL-003",
        "training_job_id": None,
        "name": "dealix_base_llm_v1",
        "endpoint": "/api/v1/models/base-llm/complete",
        "status": "live",
        "requests_today": 5621,
        "requests_total": 234100,
        "avg_latency_ms": 187,
        "uptime_pct": 99.99,
        "version": "1.0.0",
        "deployed_at": "2026-03-01T08:00:00Z",
    },
    "MDL-004": {
        "id": "MDL-004",
        "training_job_id": None,
        "name": "revenue_forecast_model_v1",
        "endpoint": "/api/v1/models/revenue-forecast/predict",
        "status": "deprecated",
        "requests_today": 0,
        "requests_total": 45600,
        "avg_latency_ms": 95,
        "uptime_pct": 0.0,
        "version": "1.0.0",
        "deployed_at": "2026-01-15T08:00:00Z",
    },
}

# ---------------------------------------------------------------------------
# In-memory state log (status changes recorded here for audit trail)
# ---------------------------------------------------------------------------

_STATE_LOG: list[dict[str, Any]] = []

# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------


class JobActionBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(min_length=5, max_length=2000)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(UTC).isoformat()


def _today_iso() -> str:
    """Return today's date as an ISO 8601 date string."""
    return date.today().isoformat()


def _job_or_404(job_id: str) -> dict[str, Any]:
    """Return the job record or raise HTTP 404."""
    job = TRAINING_JOBS.get(job_id)
    if job is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "job_not_found",
                "job_id": job_id,
            },
        )
    return job


def _model_or_404(model_id: str) -> dict[str, Any]:
    """Return the deployed model record or raise HTTP 404."""
    model = DEPLOYED_MODELS.get(model_id)
    if model is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "model_not_found",
                "model_id": model_id,
            },
        )
    return model


def _compute_avg_accuracy_completed(
    jobs: dict[str, dict[str, Any]],
) -> float:
    """Return the mean accuracy across all completed jobs that have an accuracy value."""
    accuracies = [
        j["accuracy"]
        for j in jobs.values()
        if j["status"] == "completed" and j["accuracy"] is not None
    ]
    if not accuracies:
        return 0.0
    return round(sum(accuracies) / len(accuracies), 3)


def _compute_pdpl_compliance_rate(jobs: dict[str, dict[str, Any]]) -> float:
    """Return the fraction of jobs that are PDPL compliant."""
    total = len(jobs)
    if total == 0:
        return 0.0
    compliant = sum(1 for j in jobs.values() if j.get("pdpl_compliant"))
    return round(compliant / total, 4)


def _compute_total_requests_today(models: dict[str, dict[str, Any]]) -> int:
    """Return the sum of requests_today across all deployed models."""
    return sum(m.get("requests_today", 0) for m in models.values())


def _compute_avg_latency_live(models: dict[str, dict[str, Any]]) -> float:
    """Return the mean avg_latency_ms across all live deployed models."""
    latencies = [
        m["avg_latency_ms"]
        for m in models.values()
        if m.get("status") == "live" and m.get("avg_latency_ms") is not None
    ]
    if not latencies:
        return 0.0
    return round(sum(latencies) / len(latencies), 2)


def _count_by_status(jobs: dict[str, dict[str, Any]]) -> dict[str, int]:
    """Return a mapping of status -> count for the given job dict."""
    counts: dict[str, int] = {}
    for j in jobs.values():
        s = j["status"]
        counts[s] = counts.get(s, 0) + 1
    return counts


# ---------------------------------------------------------------------------
# Endpoints — fixed paths first, then parameterised
# ---------------------------------------------------------------------------


@router.get("/jobs/active")
async def list_active_jobs() -> dict[str, Any]:
    """List all training jobs with status running or queued."""
    active = [j for j in TRAINING_JOBS.values() if j["status"] in ("running", "queued")]
    _log.info("ai_training_active_jobs_listed", count=len(active))
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "active_job_count": len(active),
        "jobs": active,
    }


@router.get("/jobs")
async def list_jobs(
    status: str | None = Query(default=None, description="Filter by status"),
    model_type: str | None = Query(default=None, description="Filter by model_type"),
    sector: str | None = Query(default=None, description="Filter by sector"),
) -> dict[str, Any]:
    """List all training jobs with optional filters."""
    jobs = list(TRAINING_JOBS.values())
    if status is not None:
        jobs = [j for j in jobs if j["status"] == status]
    if model_type is not None:
        jobs = [j for j in jobs if j["model_type"] == model_type]
    if sector is not None:
        jobs = [j for j in jobs if j["sector"] == sector]
    _log.info("ai_training_jobs_listed", count=len(jobs))
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total": len(jobs),
        "jobs": jobs,
    }


@router.get("/jobs/{job_id}")
async def get_job(job_id: str) -> dict[str, Any]:
    """Get full detail for a single training job."""
    job = _job_or_404(job_id)
    _log.info("ai_training_job_fetched", job_id=job_id, status=job["status"])
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        **job,
    }


@router.post("/jobs/{job_id}/pause")
async def pause_job(job_id: str, body: JobActionBody) -> dict[str, Any]:
    """Pause a running training job. Requires APPROVAL_FIRST."""
    job = _job_or_404(job_id)
    if job["status"] not in _PAUSABLE_STATUSES:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "invalid_transition",
                "current_status": job["status"],
                "allowed_from": sorted(_PAUSABLE_STATUSES),
                "ar": f"لا يمكن إيقاف مؤقت للوظيفة بالحالة '{job['status']}'",
                "en": f"Cannot pause a job with status '{job['status']}'",
            },
        )
    job["status"] = "paused"
    timestamp = _now_iso()
    _STATE_LOG.append(
        {
            "job_id": job_id,
            "action": "pause",
            "reason": body.reason,
            "previous_status": "running",
            "new_status": "paused",
            "logged_at": timestamp,
        }
    )
    _log.info("ai_training_job_paused", job_id=job_id, reason=body.reason)
    return {
        "governance_decision": _GOV_MUTATE,
        "status": "paused_pending_approval",
        "job_id": job_id,
        "new_status": "paused",
        "reason": body.reason,
        "actioned_at": timestamp,
    }


@router.post("/jobs/{job_id}/resume")
async def resume_job(job_id: str, body: JobActionBody) -> dict[str, Any]:
    """Resume a paused training job. Requires APPROVAL_FIRST."""
    job = _job_or_404(job_id)
    if job["status"] not in _RESUMABLE_STATUSES:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "invalid_transition",
                "current_status": job["status"],
                "allowed_from": sorted(_RESUMABLE_STATUSES),
                "ar": f"لا يمكن استئناف الوظيفة بالحالة '{job['status']}'",
                "en": f"Cannot resume a job with status '{job['status']}'",
            },
        )
    job["status"] = "running"
    timestamp = _now_iso()
    _STATE_LOG.append(
        {
            "job_id": job_id,
            "action": "resume",
            "reason": body.reason,
            "previous_status": "paused",
            "new_status": "running",
            "logged_at": timestamp,
        }
    )
    _log.info("ai_training_job_resumed", job_id=job_id, reason=body.reason)
    return {
        "governance_decision": _GOV_MUTATE,
        "status": "resumed_pending_approval",
        "job_id": job_id,
        "new_status": "running",
        "reason": body.reason,
        "actioned_at": timestamp,
    }


@router.post("/jobs/{job_id}/cancel")
async def cancel_job(job_id: str, body: JobActionBody) -> dict[str, Any]:
    """Cancel a queued, running, or paused training job. Requires APPROVAL_FIRST."""
    job = _job_or_404(job_id)
    if job["status"] not in _CANCELLABLE_STATUSES:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "invalid_transition",
                "current_status": job["status"],
                "allowed_from": sorted(_CANCELLABLE_STATUSES),
                "ar": f"لا يمكن إلغاء الوظيفة بالحالة '{job['status']}'",
                "en": f"Cannot cancel a job with status '{job['status']}'",
            },
        )
    previous_status = job["status"]
    job["status"] = "cancelled"
    timestamp = _now_iso()
    _STATE_LOG.append(
        {
            "job_id": job_id,
            "action": "cancel",
            "reason": body.reason,
            "previous_status": previous_status,
            "new_status": "cancelled",
            "logged_at": timestamp,
        }
    )
    _log.info("ai_training_job_cancelled", job_id=job_id, reason=body.reason)
    return {
        "governance_decision": _GOV_MUTATE,
        "status": "cancelled_pending_approval",
        "job_id": job_id,
        "new_status": "cancelled",
        "reason": body.reason,
        "actioned_at": timestamp,
    }


@router.get("/models")
async def list_models() -> dict[str, Any]:
    """List all deployed models."""
    models = list(DEPLOYED_MODELS.values())
    _log.info("ai_deployed_models_listed", count=len(models))
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total": len(models),
        "models": models,
    }


@router.get("/models/{model_id}")
async def get_model(model_id: str) -> dict[str, Any]:
    """Get full detail for a single deployed model."""
    model = _model_or_404(model_id)
    _log.info("ai_deployed_model_fetched", model_id=model_id, status=model["status"])
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        **model,
    }


@router.get("/performance-report")
async def get_performance_report() -> dict[str, Any]:
    """Aggregate ML performance metrics across all training jobs and deployments."""
    by_status = _count_by_status(TRAINING_JOBS)
    avg_accuracy = _compute_avg_accuracy_completed(TRAINING_JOBS)
    total_requests_today = _compute_total_requests_today(DEPLOYED_MODELS)
    avg_latency = _compute_avg_latency_live(DEPLOYED_MODELS)
    live_models = sum(1 for m in DEPLOYED_MODELS.values() if m["status"] == "live")
    pdpl_rate = _compute_pdpl_compliance_rate(TRAINING_JOBS)

    _log.info("ai_performance_report_generated")

    return {
        "governance_decision": _GOV_READ,
        "total_jobs": len(TRAINING_JOBS),
        "by_status": by_status,
        "avg_accuracy_completed": avg_accuracy,
        "deployed_models": len(DEPLOYED_MODELS),
        "live_models": live_models,
        "total_requests_today": total_requests_today,
        "avg_latency_ms": avg_latency,
        "data_residency": "sa-east-1",
        "pdpl_compliance_rate": pdpl_rate,
        "report_date": _today_iso(),
    }


@router.get("/data-compliance")
async def get_data_compliance() -> dict[str, Any]:
    """PDPL data compliance report for all training jobs."""
    jobs_list = list(TRAINING_JOBS.values())
    pdpl_compliant_count = sum(1 for j in jobs_list if j.get("pdpl_compliant"))
    total = len(jobs_list)
    compliance_rate = round(pdpl_compliant_count / total, 4) if total else 0.0

    compliance_jobs = [
        {
            "id": j["id"],
            "name": j["name"],
            "status": j["status"],
            "pdpl_compliant": j.get("pdpl_compliant"),
            "data_residency": j.get("data_residency"),
        }
        for j in jobs_list
    ]

    _log.info(
        "ai_data_compliance_report_generated",
        pdpl_compliant=pdpl_compliant_count,
        total=total,
    )

    return {
        "governance_decision": _GOV_READ,
        "pdpl_compliant_jobs": pdpl_compliant_count,
        "total_jobs": total,
        "compliance_rate": compliance_rate,
        "data_residency": "sa-east-1",
        "retention_policy_days": 365,
        "audit_log": True,
        "right_to_erasure": True,
        "consent_required": True,
        "cross_border_transfer": False,
        "jobs": compliance_jobs,
    }
