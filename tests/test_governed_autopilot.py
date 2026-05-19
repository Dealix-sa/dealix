"""Tests for the Governed Autopilot daily motion (G1a + G1b).

Covers the new public functions:
  - core/tasks/worker.py cron jobs (lead-prep, targeting, follow-ups,
    founder brief, expire-sweep)
  - auto_client_acquisition/automation/daily_runner.py
  - auto_client_acquisition/approval_center/execution_hook.py
  - auto_client_acquisition/approval_center/durable_mirror.py

Doctrine: every test asserts that prospect outreach is NEVER auto-sent —
the execution hook only enqueues a send job for draft_email + channel=email,
and blocked channels (whatsapp/linkedin/phone) never auto-execute.
"""

from __future__ import annotations

import asyncio

import pytest

from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    ApprovalStatus,
)
from auto_client_acquisition.approval_center.execution_hook import (
    dispatch_approved,
    is_auto_executable,
)
from auto_client_acquisition.automation.daily_runner import followup_template
from core.tasks.worker import WorkerSettings


# ─── Cron registration (G1a) ─────────────────────────────────────


def test_worker_registers_five_new_cron_jobs() -> None:
    """daily_pipeline_refresh + 5 Governed Autopilot crons + the
    own-brand publish cron = 7 daily-motion crons, plus the 6 strategic
    automation crons (1 daily metrics snapshot + 5 weekly) = 13 total."""
    assert len(WorkerSettings.cron_jobs) == 13


def test_run_outreach_batch_is_a_registered_worker_function() -> None:
    """The execution hook enqueues run_outreach_batch — it must be a job fn."""
    names = {fn.__name__ for fn in WorkerSettings.functions}
    assert "run_outreach_batch" in names


# ─── followup_template (daily_runner) ────────────────────────────


def test_followup_template_has_opt_out_for_each_step() -> None:
    for step in (2, 5, 10):
        body = followup_template(step)
        assert body
        assert "STOP" in body


def test_followup_template_unknown_step_is_empty() -> None:
    assert followup_template(99) == ""


# ─── Execution hook doctrine (G1b) ───────────────────────────────


def _approved(action_type: str, channel: str | None) -> ApprovalRequest:
    return ApprovalRequest(
        object_type="draft_message",
        object_id="batch_abc",
        action_type=action_type,
        channel=channel,
        status=ApprovalStatus.APPROVED,
    )


def test_is_auto_executable_only_for_approved_draft_email_on_email() -> None:
    assert is_auto_executable(_approved("draft_email", "email")) is True


def test_is_auto_executable_false_for_pending() -> None:
    req = ApprovalRequest(
        object_type="draft_message",
        object_id="b1",
        action_type="draft_email",
        channel="email",
    )
    assert ApprovalStatus(req.status) == ApprovalStatus.PENDING
    assert is_auto_executable(req) is False


@pytest.mark.parametrize("channel", ["whatsapp", "linkedin", "phone"])
def test_is_auto_executable_false_for_blocked_channels(channel: str) -> None:
    """Doctrine: blocked channels never auto-execute, even when approved."""
    assert is_auto_executable(_approved("draft_email", channel)) is False


def test_is_auto_executable_false_for_non_email_action_type() -> None:
    assert is_auto_executable(_approved("call_script", "phone")) is False


def test_dispatch_enqueues_email_draft_and_blocks_whatsapp() -> None:
    """A mixed batch: email draft is enqueued, whatsapp draft is blocked."""
    reqs = [
        _approved("draft_email", "email"),
        _approved("draft_email", "whatsapp"),
    ]
    result = asyncio.run(dispatch_approved(reqs, redis_pool=None))
    assert result["enqueued_count"] == 1
    assert result["blocked_count"] == 1
    assert result["dry_run"] is True
    assert result["blocked_from_execution"][0]["channel"] == "whatsapp"


def test_dispatch_enqueues_job_when_pool_present() -> None:
    """With a fake pool, the email draft enqueues exactly one job."""

    class _FakePool:
        def __init__(self) -> None:
            self.jobs: list[tuple[str, dict]] = []

        async def enqueue_job(self, name: str, **kwargs: object) -> None:
            self.jobs.append((name, kwargs))

    pool = _FakePool()
    result = asyncio.run(
        dispatch_approved([_approved("draft_email", "email")], redis_pool=pool)
    )
    assert result["enqueued_count"] == 1
    assert len(pool.jobs) == 1
    assert pool.jobs[0][0] == "run_outreach_batch"


def test_dispatch_never_enqueues_blocked_channel_even_with_pool() -> None:
    """Doctrine: blocked channels emit zero jobs regardless of pool."""

    class _FakePool:
        def __init__(self) -> None:
            self.jobs: list[str] = []

        async def enqueue_job(self, name: str, **kwargs: object) -> None:
            self.jobs.append(name)

    pool = _FakePool()
    for channel in ("whatsapp", "linkedin", "phone"):
        pool.jobs.clear()
        result = asyncio.run(
            dispatch_approved([_approved("draft_email", channel)], redis_pool=pool)
        )
        assert pool.jobs == []
        assert result["enqueued_count"] == 0
        assert result["blocked_count"] == 1


def test_dispatch_skips_unapproved_requests() -> None:
    pending = ApprovalRequest(
        object_type="draft_message",
        object_id="b2",
        action_type="draft_email",
        channel="email",
    )
    result = asyncio.run(dispatch_approved([pending], redis_pool=None))
    assert result["enqueued_count"] == 0
    assert pending.approval_id in result["skipped"]


# ─── Durable mirror round-trip (G1b) ─────────────────────────────


def test_durable_mirror_request_row_roundtrip() -> None:
    """_request_to_row + _row_to_request preserve the ApprovalRequest."""
    from auto_client_acquisition.approval_center.durable_mirror import (
        _request_to_row,
        _row_to_request,
    )
    from db.models import ApprovalRecord

    req = _approved("draft_email", "email")
    row = _request_to_row(req)
    record = ApprovalRecord(**row)
    assert record.approval_id == req.approval_id
    assert record.action_type == "draft_email"
    assert record.channel == "email"
    assert record.status == ApprovalStatus.APPROVED.value

    rebuilt = _row_to_request(record)
    assert rebuilt.approval_id == req.approval_id
    assert rebuilt.action_type == "draft_email"
    assert ApprovalStatus(rebuilt.status) == ApprovalStatus.APPROVED


# ─── daily_runner core functions ─────────────────────────────────


def test_expire_stale_approvals_returns_count() -> None:
    """expire_stale_approvals is a pure in-memory sweep — always ok."""
    from auto_client_acquisition.automation.daily_runner import (
        expire_stale_approvals,
    )

    result = expire_stale_approvals()
    assert result["status"] == "ok"
    assert isinstance(result["expired_count"], int)


def test_run_lead_prep_core_handles_missing_db_gracefully() -> None:
    """Without a Postgres backend the core function degrades, never raises."""
    from auto_client_acquisition.automation.daily_runner import run_lead_prep_core

    result = asyncio.run(run_lead_prep_core())
    assert result["status"] in {"ok", "skipped_db_unreachable"}


def test_run_followups_core_handles_missing_db_gracefully() -> None:
    from auto_client_acquisition.automation.daily_runner import run_followups_core

    result = asyncio.run(run_followups_core())
    assert result["status"] in {"ok", "skipped_db_unreachable", "commit_failed"}


def test_run_daily_targeting_core_handles_missing_db_gracefully() -> None:
    from auto_client_acquisition.automation.daily_runner import (
        run_daily_targeting_core,
    )

    result = asyncio.run(run_daily_targeting_core(daily_target_count=50))
    # Either a full DailyTargetingResult dict or a graceful DB-skip dict.
    assert "status" in result or "selected_count" in result
