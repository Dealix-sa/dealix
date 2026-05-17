"""Postgres persistence for the Approval Command Center queue.

The in-memory :class:`ApprovalStore` is the working set; this module
makes the queue durable across process restarts. The store hydrates
from this table on startup and the HTTP router writes through on every
mutation.

Every function degrades gracefully: if the database is unreachable the
calls log a warning and return without raising, so a missing DB never
takes the API down — the in-memory store keeps serving.
"""
from __future__ import annotations

from sqlalchemy import select

from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from core.logging import get_logger
from db.models import ApprovalTicketRecord
from db.session import async_session_factory

log = get_logger(__name__)


def _to_row(req: ApprovalRequest) -> dict:
    """Project an ApprovalRequest onto the approval_tickets column set."""
    return {
        "approval_id": req.approval_id,
        "object_type": req.object_type or "",
        "object_id": req.object_id or "",
        "action_type": req.action_type or "",
        "action_mode": req.action_mode or "approval_required",
        "status": str(req.status),
        "risk_level": req.risk_level or "low",
        "channel": req.channel,
        "proof_impact": req.proof_impact or "",
        "customer_id": req.customer_id,
        "lead_id": req.lead_id,
        "payload": req.model_dump(mode="json"),
        "created_at": req.created_at,
        "updated_at": req.updated_at,
    }


async def upsert(req: ApprovalRequest) -> bool:
    """Write-through a single approval. Returns False on DB failure."""
    return await upsert_many([req])


async def upsert_many(reqs: list[ApprovalRequest]) -> bool:
    """Write-through a batch of approvals. Returns False on DB failure."""
    if not reqs:
        return True
    try:
        async with async_session_factory()() as session:
            for req in reqs:
                row = _to_row(req)
                existing = await session.get(ApprovalTicketRecord, req.approval_id)
                if existing is None:
                    session.add(ApprovalTicketRecord(**row))
                else:
                    for key, value in row.items():
                        if key not in ("approval_id", "created_at"):
                            setattr(existing, key, value)
            await session.commit()
        return True
    except Exception as exc:
        log.warning("approval_persist_failed", error=str(exc), count=len(reqs))
        return False


async def load_all() -> list[ApprovalRequest]:
    """Load every persisted approval. Returns [] on DB failure."""
    try:
        async with async_session_factory()() as session:
            result = await session.execute(select(ApprovalTicketRecord.payload))
            payloads = list(result.scalars().all())
    except Exception as exc:
        log.warning("approval_hydrate_query_failed", error=str(exc))
        return []

    requests: list[ApprovalRequest] = []
    for payload in payloads:
        try:
            requests.append(ApprovalRequest.model_validate(payload))
        except Exception as exc:
            log.warning("approval_hydrate_row_skipped", error=str(exc))
    return requests


async def hydrate_into(store) -> int:
    """Populate ``store`` from the durable table. Returns rows loaded."""
    requests = await load_all()
    loaded = store.bulk_load(requests)
    log.info("approval_store_hydrated", loaded=loaded)
    return loaded
