"""Tests for the Autonomous Daily Scheduler API."""

from __future__ import annotations

import pytest

from api.routers.autonomous_scheduler import (
    ScheduledTaskCreate,
    _simulate_run,
    _tasks,
    _runs,
    _new_id,
    _utcnow_iso,
    _seed_default_tasks,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _make_task_create(
    name: str = "Test Task",
    task_type: str = "daily",
    next_run_at: str = "2026-06-01T07:00:00+03:00",
    payload: dict | None = None,
) -> ScheduledTaskCreate:
    return ScheduledTaskCreate(
        name=name,
        task_type=task_type,
        next_run_at=next_run_at,
        payload=payload or {},
    )


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------


def test_task_id_has_correct_prefix() -> None:
    tid = _new_id("task")
    assert tid.startswith("task_")
    assert len(tid) > 8


def test_run_id_has_correct_prefix() -> None:
    rid = _new_id("run")
    assert rid.startswith("run_")


def test_utcnow_iso_is_string() -> None:
    ts = _utcnow_iso()
    assert isinstance(ts, str)
    assert "T" in ts


def test_default_tasks_seeded() -> None:
    """Scheduler is pre-seeded with default tasks on module load."""
    assert len(_tasks) >= 5


def test_default_tasks_have_required_fields() -> None:
    for task in _tasks.values():
        assert "task_id" in task
        assert "name" in task
        assert "task_type" in task
        assert "next_run_at" in task
        assert "status" in task


def test_simulate_run_returns_success() -> None:
    # Use the first default task
    task = next(iter(_tasks.values()))
    run = _simulate_run(task)
    assert run["success"] is True
    assert run["task_id"] == task["task_id"]
    assert run["run_id"].startswith("run_")
    assert "completed_at" in run
    assert "result_summary" in run


def test_simulate_run_summary_contains_task_name() -> None:
    task = next(iter(_tasks.values()))
    run = _simulate_run(task)
    assert task["name"] in run["result_summary"]


def test_task_types_valid_in_defaults() -> None:
    valid_types = {"daily", "weekly", "monthly"}
    for task in _tasks.values():
        assert task["task_type"] in valid_types


def test_task_create_model_validates() -> None:
    create = _make_task_create(name="SEO Audit", task_type="weekly")
    assert create.name == "SEO Audit"
    assert create.task_type == "weekly"


def test_multiple_task_ids_are_unique() -> None:
    ids = [_new_id("task") for _ in range(50)]
    assert len(set(ids)) == 50


def test_daily_brief_task_present() -> None:
    """The 'Daily Lead Prep' task must be seeded by default."""
    names = [t["name"] for t in _tasks.values()]
    assert "Daily Lead Prep" in names


def test_weekly_scorecard_task_present() -> None:
    names = [t["name"] for t in _tasks.values()]
    assert "Weekly Scorecard" in names
