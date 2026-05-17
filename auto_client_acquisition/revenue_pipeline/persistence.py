"""Postgres persistence for the Revenue Pipeline.

The in-memory :class:`RevenuePipeline` is the working set; this module
makes the pipeline durable across process restarts. The store hydrates
from this table on startup and the HTTP router writes through on every
mutation.

Every function degrades gracefully: if the database is unreachable the
calls log a warning and return without raising, so a missing DB never
takes the API down — the in-memory pipeline keeps serving.
"""
from __future__ import annotations

from sqlalchemy import select

from auto_client_acquisition.revenue_pipeline.lead import Lead
from core.logging import get_logger
from db.models import PipelineLeadRecord
from db.session import async_session_factory

log = get_logger(__name__)


def _to_row(lead: Lead) -> dict:
    """Project a Lead onto the pipeline_leads column set."""
    return {
        "id": lead.id,
        "slot_id": lead.slot_id,
        "sector": lead.sector,
        "region": lead.region,
        "relationship_strength": lead.relationship_strength,
        "consent_status": lead.consent_status,
        "stage": str(lead.stage),
        "last_touch_at": lead.last_touch_at,
        "expected_amount_sar": lead.expected_amount_sar,
        "actual_amount_sar": lead.actual_amount_sar,
        "commitment_evidence": lead.commitment_evidence or "",
        "payment_evidence": lead.payment_evidence or "",
        "notes_placeholder": lead.notes_placeholder or "",
        "payload": lead.model_dump(mode="json"),
        "created_at": lead.created_at,
    }


async def upsert(lead: Lead) -> bool:
    """Write-through a single lead. Returns False on DB failure."""
    return await upsert_many([lead])


async def upsert_many(leads: list[Lead]) -> bool:
    """Write-through a batch of leads. Returns False on DB failure."""
    if not leads:
        return True
    try:
        async with async_session_factory()() as session:
            for lead in leads:
                row = _to_row(lead)
                existing = await session.get(PipelineLeadRecord, lead.id)
                if existing is None:
                    session.add(PipelineLeadRecord(**row))
                else:
                    for key, value in row.items():
                        if key not in ("id", "created_at"):
                            setattr(existing, key, value)
            await session.commit()
        return True
    except Exception as exc:
        log.warning("pipeline_persist_failed", error=str(exc), count=len(leads))
        return False


async def load_all() -> list[Lead]:
    """Load every persisted lead. Returns [] on DB failure."""
    try:
        async with async_session_factory()() as session:
            result = await session.execute(select(PipelineLeadRecord.payload))
            payloads = list(result.scalars().all())
    except Exception as exc:
        log.warning("pipeline_hydrate_query_failed", error=str(exc))
        return []

    leads: list[Lead] = []
    for payload in payloads:
        try:
            leads.append(Lead.model_validate(payload))
        except Exception as exc:  # skip a corrupt row, keep the rest
            log.warning("pipeline_hydrate_row_skipped", error=str(exc))
    return leads


async def ping() -> bool:
    """Return True if the durable store is reachable."""
    try:
        async with async_session_factory()() as session:
            await session.execute(select(PipelineLeadRecord.id).limit(1))
        return True
    except Exception as exc:
        log.warning("pipeline_ping_failed", error=str(exc))
        return False


async def hydrate_into(pipeline) -> int:
    """Populate ``pipeline`` from the durable table. Returns rows loaded."""
    leads = await load_all()
    loaded = pipeline.bulk_load(leads)
    log.info("revenue_pipeline_hydrated", loaded=loaded)
    return loaded
