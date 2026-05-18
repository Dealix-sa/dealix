"""Durable Postgres mirror for the in-memory ApprovalStore.

The in-memory ``ApprovalStore`` loses the founder's approval queue on every
worker restart (the worker filesystem is ephemeral). This module is the
durable side-car: it persists ``ApprovalRequest`` rows to the
``approval_records`` table and rehydrates the in-memory store on startup.

It does NOT change ``ApprovalStore``'s public method signatures or return
contracts — callers (the HTTP router, the cron) call ``persist`` / ``hydrate``
explicitly. All functions are best-effort: a missing/unreachable database is
logged and swallowed so the in-memory path keeps working in tests.

Doctrine: this is storage only. Persisting or rehydrating an approval never
sends anything.
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    get_default_approval_store,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from db.models import ApprovalRecord
from db.session import async_session_factory

log = logging.getLogger(__name__)

_MIRROR_FIELDS = (
    "approval_id", "object_type", "object_id", "action_type", "action_mode",
    "channel", "summary_ar", "summary_en", "risk_level", "proof_impact",
    "status", "reject_reason", "edit_history", "expires_at", "action_id",
    "lead_id", "customer_id", "due_date", "audit_ref", "proof_target",
    "created_at", "updated_at",
)


def _request_to_row(req: ApprovalRequest) -> dict[str, Any]:
    """Flatten an ApprovalRequest into an approval_records column dict."""
    data = req.model_dump(mode="python")
    return {field: data.get(field) for field in _MIRROR_FIELDS}


def _row_to_request(row: ApprovalRecord) -> ApprovalRequest:
    """Rebuild an ApprovalRequest from a durable approval_records row."""
    return ApprovalRequest.model_validate(
        {field: getattr(row, field) for field in _MIRROR_FIELDS}
    )


async def persist(req: ApprovalRequest) -> bool:
    """Upsert one ApprovalRequest into ``approval_records``.

    Returns True on success, False if the database is unreachable. Safe to
    call after every create / approve / reject / edit so the durable mirror
    stays in sync with the in-memory store.
    """
    row = _request_to_row(req)
    try:
        async with async_session_factory()() as session:
            stmt = pg_insert(ApprovalRecord).values(**row)
            update_cols = {
                k: stmt.excluded[k] for k in row if k != "approval_id"
            }
            stmt = stmt.on_conflict_do_update(
                index_elements=["approval_id"], set_=update_cols
            )
            await session.execute(stmt)
            await session.commit()
        return True
    except Exception as exc:  # noqa: BLE001
        log.warning("approval_durable_persist_failed err=%s", exc)
        return False


async def persist_many(reqs: list[ApprovalRequest]) -> int:
    """Persist a batch of ApprovalRequests. Returns the count persisted."""
    persisted = 0
    for req in reqs:
        if await persist(req):
            persisted += 1
    return persisted


async def load_all() -> list[ApprovalRequest]:
    """Read every durable approval row back as ApprovalRequest objects."""
    try:
        async with async_session_factory()() as session:
            rows = (await session.execute(select(ApprovalRecord))).scalars().all()
        return [_row_to_request(r) for r in rows]
    except Exception as exc:  # noqa: BLE001
        log.warning("approval_durable_load_failed err=%s", exc)
        return []


async def hydrate(store: ApprovalStore | None = None) -> int:
    """Rehydrate the in-memory store from the durable mirror on startup.

    Loads every persisted approval and injects it into the store's backing
    map without re-running create-time safety (the rows were already safe
    when first created). Returns the count of rehydrated approvals.
    """
    target = store or get_default_approval_store()
    requests = await load_all()
    if not requests:
        return 0
    with target._lock:  # noqa: SLF001 — durable side-car owns rehydration
        for req in requests:
            target._items[req.approval_id] = req  # noqa: SLF001
    log.info("approval_durable_hydrate count=%d", len(requests))
    return len(requests)
