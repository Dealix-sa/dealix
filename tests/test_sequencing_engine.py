"""Tests for the persistent follow-up sequencing engine (M7)."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

sa = pytest.importorskip("sqlalchemy")
import sqlalchemy.orm  # noqa: E402,F401  (used as sa.orm.Session)

from auto_client_acquisition.sales_os.sequencing_engine import (  # noqa: E402
    due_tasks,
    mark_task,
    materialize_tasks,
    plan_cadence,
)


# ── Pure cadence planner ──────────────────────────────────────────


def test_plan_cadence_offsets() -> None:
    start = datetime(2026, 5, 1, tzinfo=UTC)
    tasks = plan_cadence(start=start, channel="email")
    assert [t.attempt for t in tasks] == [1, 2, 3, 4]
    assert (tasks[0].scheduled_for - start).days == 0
    assert (tasks[1].scheduled_for - start).days == 3
    assert (tasks[2].scheduled_for - start).days == 7
    assert (tasks[3].scheduled_for - start).days == 14
    assert all(t.channel == "email" for t in tasks)


def test_plan_cadence_extra_touches_reuse_final_interval() -> None:
    start = datetime(2026, 5, 1, tzinfo=UTC)
    tasks = plan_cadence(start=start, touches=6)
    assert len(tasks) == 6
    # touches 5 and 6 reuse the 14-day interval
    assert (tasks[4].scheduled_for - start).days == 14
    assert (tasks[5].scheduled_for - start).days == 14


# ── Persistence helpers (sqlite) ──────────────────────────────────


@pytest.fixture()
def session():
    from db.models import Base

    engine = sa.create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    with sa.orm.Session(engine, future=True) as s:
        yield s


def test_materialize_and_query_due_tasks(session) -> None:
    past = datetime.now(UTC) - timedelta(days=30)
    ids = materialize_tasks(session, lead_id="lead_x", start=past)
    session.commit()
    assert len(ids) == 4

    # all four are overdue (cadence started 30 days ago)
    due = due_tasks(session, now=datetime.now(UTC))
    assert len(due) == 4
    assert due[0].scheduled_for <= due[-1].scheduled_for  # oldest first


def test_due_excludes_future_and_non_scheduled(session) -> None:
    future = datetime.now(UTC) + timedelta(days=10)
    materialize_tasks(session, lead_id="lead_y", start=future)
    session.commit()
    assert due_tasks(session, now=datetime.now(UTC)) == []


def test_mark_task_moves_status(session) -> None:
    ids = materialize_tasks(
        session, lead_id="lead_z", start=datetime.now(UTC) - timedelta(days=20)
    )
    session.commit()
    mark_task(session, ids[0], status="queued", draft_approval_id="apr_77")
    session.commit()

    from db.models import FollowUpTask

    task = session.get(FollowUpTask, ids[0])
    assert task.status == "queued"
    assert task.draft_approval_id == "apr_77"
    # a queued task is no longer "due"
    assert ids[0] not in {t.id for t in due_tasks(session, now=datetime.now(UTC))}


def test_mark_missing_task_raises(session) -> None:
    with pytest.raises(ValueError):
        mark_task(session, "fut_nope", status="done")
