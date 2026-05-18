"""Tests for the Postgres-backed DbApprovalStore + audit persistence.

The store is exercised against an in-memory SQLite database (sync engine
with a StaticPool so every session shares one connection). This mirrors
the existing DB-touching test pattern in tests/test_pg_event_store.py.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    DbApprovalStore,
    get_default_approval_store,
    reset_default_approval_store,
)
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)
from db.models import ApprovalRequestRecord, AuditLogRecord, Base


# ── Fixtures ──────────────────────────────────────────────────────


@pytest.fixture
def db_store() -> DbApprovalStore:
    """A DbApprovalStore wired to a fresh in-memory SQLite database."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)

    store = DbApprovalStore.__new__(DbApprovalStore)
    import threading

    store._lock = threading.Lock()
    store._database_url = "sqlite://"
    store._session_factory = factory
    return store


def _make_request(**overrides) -> ApprovalRequest:
    base: dict = {
        "object_type": "outreach_draft",
        "object_id": "obj_1",
        "action_type": "draft_email",
        "channel": "email",
        "summary_en": "Send a follow-up",
        "summary_ar": "إرسال متابعة",
        "risk_level": "low",
        "customer_id": "cust_1",
    }
    base.update(overrides)
    return ApprovalRequest(**base)


# ── create / get ──────────────────────────────────────────────────


def test_create_persists_and_get_roundtrips(db_store: DbApprovalStore) -> None:
    req = _make_request()
    db_store.create(req)

    fetched = db_store.get(req.approval_id)
    assert fetched is not None
    assert fetched.approval_id == req.approval_id
    assert fetched.summary_en == "Send a follow-up"
    assert fetched.customer_id == "cust_1"
    assert ApprovalStatus(fetched.status) == ApprovalStatus.PENDING


def test_get_missing_returns_none(db_store: DbApprovalStore) -> None:
    assert db_store.get("apr_does_not_exist") is None


def test_create_runs_safety_blocks_blocked_mode(db_store: DbApprovalStore) -> None:
    req = _make_request(action_mode="blocked")
    db_store.create(req)
    fetched = db_store.get(req.approval_id)
    assert fetched is not None
    assert ApprovalStatus(fetched.status) == ApprovalStatus.BLOCKED


# ── create_with_founder_rules ─────────────────────────────────────


def test_create_with_founder_rules_persists(db_store: DbApprovalStore) -> None:
    req = _make_request()
    db_store.create_with_founder_rules(req, confidence=1.0, content="hello")
    assert db_store.get(req.approval_id) is not None


# ── approve / reject / edit ───────────────────────────────────────


def test_approve_transitions_and_audits(db_store: DbApprovalStore) -> None:
    req = _make_request()
    db_store.create(req)

    approved = db_store.approve(req.approval_id, "founder")
    assert ApprovalStatus(approved.status) == ApprovalStatus.APPROVED
    assert approved.edit_history[-1]["action"] == "approve"

    # Audit row written.
    with db_store._session_factory() as session:
        rows = session.execute(select(AuditLogRecord)).scalars().all()
    assert any(
        r.action == "approval.approve" and r.entity_id == req.approval_id
        for r in rows
    )


def test_reject_records_reason(db_store: DbApprovalStore) -> None:
    req = _make_request()
    db_store.create(req)

    rejected = db_store.reject(req.approval_id, "founder", "off-policy")
    assert ApprovalStatus(rejected.status) == ApprovalStatus.REJECTED
    assert rejected.reject_reason == "off-policy"
    assert rejected.edit_history[-1]["reason"] == "off-policy"


def test_approve_blocked_raises(db_store: DbApprovalStore) -> None:
    req = _make_request(action_mode="blocked")
    db_store.create(req)
    with pytest.raises(ValueError):
        db_store.approve(req.approval_id, "founder")


def test_edit_applies_whitelisted_fields_only(db_store: DbApprovalStore) -> None:
    req = _make_request()
    db_store.create(req)

    edited = db_store.edit(
        req.approval_id,
        "founder",
        {"summary_en": "Revised copy", "status": "approved"},
    )
    # summary_en is whitelisted; status is not.
    assert edited.summary_en == "Revised copy"
    assert ApprovalStatus(edited.status) == ApprovalStatus.PENDING
    assert edited.edit_history[-1]["patch"] == {"summary_en": "Revised copy"}


def test_approve_missing_raises(db_store: DbApprovalStore) -> None:
    with pytest.raises(ValueError):
        db_store.approve("apr_missing", "founder")


# ── list_pending / list_history ───────────────────────────────────


def test_list_pending_returns_only_pending(db_store: DbApprovalStore) -> None:
    r1 = _make_request()
    r2 = _make_request()
    db_store.create(r1)
    db_store.create(r2)
    db_store.approve(r2.approval_id, "founder")

    pending = db_store.list_pending()
    assert [p.approval_id for p in pending] == [r1.approval_id]


def test_list_history_newest_first(db_store: DbApprovalStore) -> None:
    r1 = _make_request()
    r2 = _make_request()
    db_store.create(r1)
    db_store.create(r2)
    db_store.approve(r1.approval_id, "founder")

    history = db_store.list_history(limit=10)
    assert len(history) == 2
    # r1 was updated most recently (approved last).
    assert history[0].approval_id == r1.approval_id


# ── expire_overdue ────────────────────────────────────────────────


def test_expire_overdue_flips_past_due_pending(db_store: DbApprovalStore) -> None:
    overdue = _make_request(expires_at=datetime.now(UTC) - timedelta(hours=1))
    fresh = _make_request(expires_at=datetime.now(UTC) + timedelta(hours=1))
    db_store.create(overdue)
    db_store.create(fresh)

    count = db_store.expire_overdue()
    assert count == 1
    assert ApprovalStatus(db_store.get(overdue.approval_id).status) == ApprovalStatus.EXPIRED
    assert ApprovalStatus(db_store.get(fresh.approval_id).status) == ApprovalStatus.PENDING


# ── bulk_approve ──────────────────────────────────────────────────


def test_bulk_approve_by_ids(db_store: DbApprovalStore) -> None:
    r1 = _make_request()
    r2 = _make_request()
    db_store.create(r1)
    db_store.create(r2)

    result = db_store.bulk_approve(
        who="founder", approval_ids=[r1.approval_id, r2.approval_id]
    )
    assert set(result["approved"]) == {r1.approval_id, r2.approval_id}
    assert result["total"] == 2


def test_bulk_approve_by_proof_impact_prefix(db_store: DbApprovalStore) -> None:
    matched = _make_request(proof_impact="leadops:batch_7")
    other = _make_request(proof_impact="delivery:task_1")
    db_store.create(matched)
    db_store.create(other)

    result = db_store.bulk_approve(who="founder", proof_impact_prefix="leadops:")
    assert result["approved"] == [matched.approval_id]


def test_bulk_approve_requires_criterion(db_store: DbApprovalStore) -> None:
    result = db_store.bulk_approve(who="founder")
    assert result["total"] == 0
    assert "reason" in result


# ── clear ─────────────────────────────────────────────────────────


def test_clear_empties_the_table(db_store: DbApprovalStore) -> None:
    db_store.create(_make_request())
    db_store.clear()
    with db_store._session_factory() as session:
        rows = session.execute(select(ApprovalRequestRecord)).scalars().all()
    assert rows == []


# ── restart-safety ────────────────────────────────────────────────


def test_persists_across_new_store_instance(db_store: DbApprovalStore) -> None:
    """A new store bound to the same DB sees previously-created rows —
    this is the restart-survival guarantee."""
    req = _make_request()
    db_store.create(req)

    # Simulate a process restart: a brand new store instance, same DB.
    fresh = DbApprovalStore.__new__(DbApprovalStore)
    import threading

    fresh._lock = threading.Lock()
    fresh._database_url = "sqlite://"
    fresh._session_factory = db_store._session_factory

    assert fresh.get(req.approval_id) is not None


# ── get_default_approval_store factory ────────────────────────────


def test_factory_returns_memory_store_without_database_url(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    reset_default_approval_store()
    store = get_default_approval_store()
    assert isinstance(store, ApprovalStore)
    reset_default_approval_store()


def test_factory_returns_db_store_with_database_url(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    reset_default_approval_store()
    store = get_default_approval_store()
    assert isinstance(store, DbApprovalStore)
    reset_default_approval_store()
    monkeypatch.delenv("DATABASE_URL", raising=False)
