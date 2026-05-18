"""Tests for Postgres-backed audit event persistence.

Covers persist_audit_event (DB path) and record_audit_event (DB path +
JSONL fallback). Uses an in-memory async SQLite database, mirroring the
DB-touching test pattern in tests/test_pg_event_store.py.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    list_events,
    persist_audit_event,
    record_audit_event,
)
from db.models import AuditLogRecord, Base

pytest_plugins = ("pytest_asyncio",)


@pytest_asyncio.fixture
async def async_session_factory():
    """Async SQLite session factory with the audit_logs table created."""
    engine = create_async_engine("sqlite+aiosqlite://", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    yield factory
    await engine.dispose()


async def test_persist_audit_event_writes_row(async_session_factory) -> None:
    async with async_session_factory() as session:
        audit_id = await persist_audit_event(
            session,
            tenant_id="cust_1",
            action="approval.approve",
            entity_type="approval_request",
            entity_id="apr_abc",
            user_id="founder",
            diff={"reason": "ok"},
        )
        await session.commit()
        assert audit_id.startswith("audit_")

    async with async_session_factory() as session:
        rows = (await session.execute(select(AuditLogRecord))).scalars().all()
    assert len(rows) == 1
    assert rows[0].action == "approval.approve"
    assert rows[0].entity_id == "apr_abc"
    assert rows[0].tenant_id == "cust_1"
    assert rows[0].diff == {"reason": "ok"}


async def test_persist_audit_event_defaults_tenant_to_system(
    async_session_factory,
) -> None:
    async with async_session_factory() as session:
        await persist_audit_event(
            session,
            tenant_id="",
            action="approval.edit",
            entity_type="approval_request",
            entity_id="apr_xyz",
        )
        await session.commit()
    async with async_session_factory() as session:
        rows = (await session.execute(select(AuditLogRecord))).scalars().all()
    assert rows[0].tenant_id == "system"


async def test_record_audit_event_db_path(async_session_factory) -> None:
    async with async_session_factory() as session:
        audit_id = await record_audit_event(
            session,
            tenant_id="cust_2",
            action="approval.reject",
            entity_type="approval_request",
            entity_id="apr_r1",
        )
        await session.commit()
        assert audit_id is not None

    async with async_session_factory() as session:
        rows = (await session.execute(select(AuditLogRecord))).scalars().all()
    assert len(rows) == 1
    assert rows[0].action == "approval.reject"


async def test_record_audit_event_jsonl_fallback(tmp_path, monkeypatch) -> None:
    """With no DB session, record_audit_event falls back to the JSONL sink."""
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))

    audit_id = await record_audit_event(
        None,
        tenant_id="cust_3",
        action="approval.approve",
        entity_type="approval_request",
        entity_id="apr_f1",
        summary="founder approved draft",
    )
    assert audit_id is None  # JSONL path returns no row id.

    events = list_events(customer_id="cust_3")
    assert len(events) == 1
    assert events[0].kind == AuditEventKind.APPROVAL.value
    assert events[0].policy_checked == "approval.approve"
