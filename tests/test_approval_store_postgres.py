"""Tests for the Postgres-backed ApprovalStore.

Uses SQLAlchemy + sqlite — the same code path Postgres runs, no live DB
required for CI. The headline test is restart-durability: the in-memory
store loses the pending queue on restart; this backend must not.
"""
from __future__ import annotations

import pytest

sa = pytest.importorskip("sqlalchemy")
try:
    _e = sa.create_engine("sqlite:///:memory:", future=True)
    _e.connect().close()
except Exception as exc:  # pragma: no cover — env-only
    pytest.skip(f"sqlite engine unavailable: {exc}", allow_module_level=True)

from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    ApprovalStatus,
    PostgresApprovalStore,
)


def _payload(**overrides: object) -> dict:
    base = {
        "object_type": "draft_message",
        "object_id": "msg_001",
        "action_type": "draft_email",
        "action_mode": "approval_required",
        "channel": "email",
        "summary_ar": "مسودة بريد للعميل",
        "summary_en": "Draft email to customer",
        "risk_level": "low",
        "proof_impact": "leadops: records 1 outreach event",
    }
    base.update(overrides)
    return base


@pytest.fixture()
def store() -> PostgresApprovalStore:
    engine = sa.create_engine("sqlite:///:memory:", future=True)
    return PostgresApprovalStore(engine=engine)


def test_create_then_list_pending(store: PostgresApprovalStore) -> None:
    req = ApprovalRequest.model_validate(_payload())
    store.create(req)
    pending = store.list_pending()
    assert len(pending) == 1
    assert pending[0].approval_id == req.approval_id
    assert ApprovalStatus(pending[0].status) == ApprovalStatus.PENDING


def test_approve_flips_status(store: PostgresApprovalStore) -> None:
    req = store.create(ApprovalRequest.model_validate(_payload()))
    store.approve(req.approval_id, who="founder")
    got = store.get(req.approval_id)
    assert got is not None
    assert ApprovalStatus(got.status) == ApprovalStatus.APPROVED
    assert got.edit_history[-1]["action"] == "approve"
    assert store.list_pending() == []


def test_reject_records_reason(store: PostgresApprovalStore) -> None:
    req = store.create(ApprovalRequest.model_validate(_payload()))
    store.reject(req.approval_id, who="founder", reason="off-tone")
    got = store.get(req.approval_id)
    assert got is not None
    assert ApprovalStatus(got.status) == ApprovalStatus.REJECTED
    assert got.reject_reason == "off-tone"


def test_edit_applies_safe_fields_only(store: PostgresApprovalStore) -> None:
    req = store.create(ApprovalRequest.model_validate(_payload()))
    store.edit(req.approval_id, who="founder", patch={"summary_en": "Revised", "status": "approved"})
    got = store.get(req.approval_id)
    assert got is not None
    assert got.summary_en == "Revised"
    # status is NOT in the edit allow-list — stays pending
    assert ApprovalStatus(got.status) == ApprovalStatus.PENDING


def test_bulk_approve_by_prefix(store: PostgresApprovalStore) -> None:
    store.create(ApprovalRequest.model_validate(_payload(object_id="a")))
    store.create(ApprovalRequest.model_validate(_payload(object_id="b")))
    store.create(ApprovalRequest.model_validate(_payload(object_id="c", proof_impact="other: x")))
    result = store.bulk_approve(who="founder", proof_impact_prefix="leadops:")
    assert len(result["approved"]) == 2
    assert len(store.list_pending()) == 1


def test_missing_approval_raises(store: PostgresApprovalStore) -> None:
    with pytest.raises(ValueError):
        store.approve("apr_does_not_exist", who="founder")
    assert store.get("apr_does_not_exist") is None


def test_survives_restart(tmp_path) -> None:
    """The headline guarantee: a new store instance on the same DB still
    sees the pending queue. The in-memory store cannot do this."""
    db_url = f"sqlite:///{tmp_path / 'approvals.db'}"

    store_a = PostgresApprovalStore(database_url=db_url)
    req = store_a.create(ApprovalRequest.model_validate(_payload()))
    store_a.approve(
        store_a.create(ApprovalRequest.model_validate(_payload(object_id="m2"))).approval_id,
        who="founder",
    )

    # Simulate a process restart: brand-new store, same database file.
    store_b = PostgresApprovalStore(database_url=db_url, create_tables=False)
    pending = store_b.list_pending()
    assert len(pending) == 1
    assert pending[0].approval_id == req.approval_id
    assert len(store_b.list_history(limit=50)) == 2
