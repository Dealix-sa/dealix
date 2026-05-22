"""
Autonomous Daily Scheduler — manage scheduled tasks and serve founder daily brief.

  POST   /api/v1/scheduler/tasks
  GET    /api/v1/scheduler/tasks
  POST   /api/v1/scheduler/tasks/{task_id}/run
  GET    /api/v1/scheduler/tasks/{task_id}/history
  DELETE /api/v1/scheduler/tasks/{task_id}
  GET    /api/v1/scheduler/daily-brief
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auto_client_acquisition.governance_os.runtime_decision import decide

router = APIRouter(prefix="/api/v1/scheduler", tags=["scheduler"])
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# In-memory stores
# ---------------------------------------------------------------------------

_tasks: dict[str, dict[str, Any]] = {}
_runs: dict[str, list[dict[str, Any]]] = {}  # task_id -> list of TaskRun dicts

_MAX_HISTORY = 20


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ScheduledTask(BaseModel):
    task_id: str = ""
    name: str
    task_type: str  # "daily" | "weekly" | "monthly"
    next_run_at: str
    last_run_at: str | None = None
    status: str = "active"
    payload: dict[str, Any] = {}


class ScheduledTaskCreate(BaseModel):
    name: str
    task_type: str
    next_run_at: str
    payload: dict[str, Any] = {}


class TaskRun(BaseModel):
    run_id: str
    task_id: str
    started_at: str
    completed_at: str
    result_summary: str
    success: bool


# ---------------------------------------------------------------------------
# Pure-function helpers
# ---------------------------------------------------------------------------


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _simulate_run(task: dict[str, Any]) -> dict[str, Any]:
    """Simulate task execution and return a TaskRun dict."""
    started = _utcnow_iso()
    run: dict[str, Any] = {
        "run_id": _new_id("run"),
        "task_id": task["task_id"],
        "started_at": started,
        "completed_at": _utcnow_iso(),
        "result_summary": f"Task '{task['name']}' completed successfully (simulated).",
        "success": True,
    }
    return run


def _seed_default_tasks() -> None:
    """Pre-seed 5 default scheduled tasks."""
    defaults = [
        {
            "name": "Daily Lead Prep",
            "task_type": "daily",
            "next_run_at": "2026-05-23T07:00:00+03:00",
            "payload": {"description": "Prepare daily lead pipeline and prioritise outreach queue."},
        },
        {
            "name": "Weekly Scorecard",
            "task_type": "weekly",
            "next_run_at": "2026-05-24T08:00:00+03:00",
            "payload": {"description": "Generate weekly commercial scorecard for founder review."},
        },
        {
            "name": "Monthly Revenue Report",
            "task_type": "monthly",
            "next_run_at": "2026-06-01T09:00:00+03:00",
            "payload": {"description": "Compile monthly revenue, MRR and churn report."},
        },
        {
            "name": "M&A Radar Scan",
            "task_type": "weekly",
            "next_run_at": "2026-05-27T10:00:00+03:00",
            "payload": {"description": "Scan M&A targets in active sectors and update proposal pipeline."},
        },
        {
            "name": "Customer Health Check",
            "task_type": "daily",
            "next_run_at": "2026-05-23T18:00:00+03:00",
            "payload": {"description": "Evaluate customer health scores and flag at-risk accounts."},
        },
    ]
    for spec in defaults:
        task_id = _new_id("task")
        _tasks[task_id] = {
            "task_id": task_id,
            "name": spec["name"],
            "task_type": spec["task_type"],
            "next_run_at": spec["next_run_at"],
            "last_run_at": None,
            "status": "active",
            "payload": spec["payload"],
            "created_at": _utcnow_iso(),
        }
        _runs[task_id] = []


# Seed on module load so the router is pre-populated at startup.
_seed_default_tasks()


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/tasks")
async def create_task(body: ScheduledTaskCreate) -> dict[str, Any]:
    """Create a new scheduled task."""
    gov = decide(action_type="scheduler_create_task", context={"task_type": body.task_type})
    task_id = _new_id("task")
    task: dict[str, Any] = {
        "task_id": task_id,
        "name": body.name,
        "task_type": body.task_type,
        "next_run_at": body.next_run_at,
        "last_run_at": None,
        "status": "active",
        "payload": body.payload,
        "created_at": _utcnow_iso(),
    }
    _tasks[task_id] = task
    _runs[task_id] = []
    log.info("scheduler_task_created task_id=%s name=%s", task_id, body.name)
    return {"governance_decision": gov.decision, "task": task}


@router.get("/tasks")
async def list_tasks() -> dict[str, Any]:
    """List all scheduled tasks with their next_run times."""
    gov = decide(action_type="scheduler_list_tasks", context={})
    active = [t for t in _tasks.values() if t.get("status") != "cancelled"]
    return {
        "governance_decision": gov.decision,
        "count": len(active),
        "tasks": active,
    }


@router.post("/tasks/{task_id}/run")
async def run_task(task_id: str) -> dict[str, Any]:
    """Manually trigger a task and return a TaskRun record."""
    gov = decide(action_type="scheduler_run_task", context={"task_id": task_id})
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task_not_found")
    if task.get("status") == "cancelled":
        raise HTTPException(status_code=409, detail="task_is_cancelled")

    run = _simulate_run(task)
    task["last_run_at"] = run["completed_at"]

    history = _runs.setdefault(task_id, [])
    history.append(run)
    # Keep only the last _MAX_HISTORY runs
    if len(history) > _MAX_HISTORY:
        _runs[task_id] = history[-_MAX_HISTORY:]

    log.info("scheduler_task_run task_id=%s run_id=%s", task_id, run["run_id"])
    return {"governance_decision": gov.decision, "run": run}


@router.get("/tasks/{task_id}/history")
async def task_history(task_id: str) -> dict[str, Any]:
    """Return the last 20 runs for a task."""
    gov = decide(action_type="scheduler_task_history", context={})
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="task_not_found")
    runs = _runs.get(task_id, [])
    return {
        "governance_decision": gov.decision,
        "task_id": task_id,
        "count": len(runs),
        "runs": runs[-_MAX_HISTORY:],
    }


@router.delete("/tasks/{task_id}")
async def cancel_task(task_id: str) -> dict[str, Any]:
    """Cancel (soft-delete) a scheduled task."""
    gov = decide(action_type="scheduler_cancel_task", context={})
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task_not_found")
    task["status"] = "cancelled"
    task["cancelled_at"] = _utcnow_iso()
    log.info("scheduler_task_cancelled task_id=%s", task_id)
    return {"governance_decision": gov.decision, "task_id": task_id, "status": "cancelled"}


@router.get("/daily-brief")
async def daily_brief() -> dict[str, Any]:
    """Return today's auto-generated founder brief."""
    gov = decide(action_type="scheduler_daily_brief", context={})
    today = datetime.now(timezone.utc).date().isoformat()

    active_tasks = [t for t in _tasks.values() if t.get("status") == "active"]
    completed_today = [
        t for t in active_tasks
        if t.get("last_run_at") and t["last_run_at"].startswith(today)
    ]
    pending = [t for t in active_tasks if t not in completed_today]

    priority_actions = [
        f"Review and trigger: {t['name']} (next run: {t['next_run_at']})"
        for t in sorted(pending, key=lambda x: x.get("next_run_at", ""))[:3]
    ]

    return {
        "governance_decision": gov.decision,
        "date": today,
        "pending_tasks": len(pending),
        "completed_today": len(completed_today),
        "revenue_targets": {
            "note": "Connect to value_os for live revenue targets.",
            "monthly_target_sar": 0,
            "achieved_sar": 0,
        },
        "priority_actions": priority_actions,
        "active_task_names": [t["name"] for t in active_tasks],
    }
