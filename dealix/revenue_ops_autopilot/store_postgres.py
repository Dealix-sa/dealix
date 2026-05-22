"""Postgres-backed war-room leads store (M-WR).

Before this, war-room leads lived in a JSON file
(``dealix/revenue_ops_autopilot/store.py``). The full
:class:`AutopilotJSONStore` continues to hold the other slices (evidence
events, tickets, invoices, diagnostics) until those need consolidation.
**This module is the leads slice only** — focused, low-risk, additive.

Mirrors the M1 :class:`PostgresApprovalStore` pattern at the public-API
level: callers swap backends via :func:`get_default_war_room_leads_store`
without behavioural change. The JSON store loses durability on every
deploy; Postgres survives.

Storage: one row per :class:`FunnelLeadRecord`. The full pydantic model
is persisted as a JSON ``payload`` column; scalars are mirrored out for
indexed querying. Backed by the ``war_room_leads`` table (migration 014).
"""
from __future__ import annotations

import logging
import threading
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    DateTime,
    Engine,
    String,
    create_engine,
    delete,
    func,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord


_LOG = logging.getLogger(__name__)


class WarRoomLeadsBase(DeclarativeBase):
    """Dedicated base so the table can bootstrap independently for tests."""


class WarRoomLeadORM(WarRoomLeadsBase):
    """Row storage for one :class:`FunnelLeadRecord`."""

    __tablename__ = "war_room_leads"

    lead_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    company: Mapped[str] = mapped_column(String(255), default="")
    industry: Mapped[str] = mapped_column(String(128), default="")
    stage: Mapped[str] = mapped_column(String(64), index=True, default="")
    war_room_status: Mapped[str] = mapped_column(String(64), index=True, default="")
    offer_id: Mapped[str] = mapped_column(String(64), default="")
    next_action_due: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, default=lambda: datetime.now(UTC)
    )
    payload: Mapped[dict] = mapped_column("payload", JSON, default=dict)


def _to_row(lead: FunnelLeadRecord) -> dict[str, Any]:
    """Project a :class:`FunnelLeadRecord` onto the row columns."""
    return {
        "lead_id": lead.id,
        "company": lead.company or "",
        "industry": lead.industry or "",
        "stage": str(lead.stage or ""),
        "war_room_status": str(lead.war_room_status or ""),
        "offer_id": lead.offer_id or "",
        "next_action_due": lead.next_action_due or None,
        "updated_at": datetime.now(UTC),
        "payload": lead.model_dump(mode="json"),
    }


def _from_row(row: WarRoomLeadORM) -> FunnelLeadRecord:
    """Rehydrate a :class:`FunnelLeadRecord` from row payload (full fidelity)."""
    return FunnelLeadRecord.model_validate(row.payload)


class PostgresWarRoomLeadsStore:
    """Restart-durable war-room leads store. Same surface as the JSON
    store's leads methods — drop-in replacement for the leads slice."""

    def __init__(
        self, *, database_url: str, engine: Engine | None = None, create_tables: bool = True
    ) -> None:
        self._engine = engine or create_engine(
            database_url, future=True, pool_pre_ping=True
        )
        self._sm = sessionmaker(self._engine, expire_on_commit=False)
        self._lock = threading.Lock()
        if create_tables:
            # Isolated table, no FK into the app schema — safe IF NOT EXISTS.
            WarRoomLeadsBase.metadata.create_all(self._engine)

    # ── public surface mirrors AutopilotJSONStore (leads slice) ──

    def list_leads(self, limit: int = 500) -> list[FunnelLeadRecord]:
        if limit <= 0:
            return []
        with self._sm() as s:
            rows = s.scalars(
                select(WarRoomLeadORM)
                .order_by(WarRoomLeadORM.created_at.desc())
                .limit(limit)
            ).all()
            return [_from_row(r) for r in rows]

    def get_lead(self, lead_id: str) -> FunnelLeadRecord | None:
        with self._sm() as s:
            row = s.get(WarRoomLeadORM, lead_id)
            return _from_row(row) if row is not None else None

    def upsert_lead(self, lead: FunnelLeadRecord) -> FunnelLeadRecord:
        """Idempotent upsert keyed by ``lead.id``."""
        with self._lock, self._sm() as s:
            row = s.get(WarRoomLeadORM, lead.id)
            data = _to_row(lead)
            if row is None:
                s.add(WarRoomLeadORM(**data))
            else:
                for key, value in data.items():
                    if key == "lead_id":
                        continue
                    setattr(row, key, value)
            s.commit()
        return lead

    def count_leads(self) -> int:
        with self._sm() as s:
            return int(s.scalar(select(func.count()).select_from(WarRoomLeadORM)) or 0)

    def clear(self) -> None:
        """Test helper — never call in production."""
        with self._sm() as s:
            s.execute(delete(WarRoomLeadORM))
            s.commit()


# ─── Process singleton + factory (mirrors M1 pattern) ──────────────

_DEFAULT: Any = None


def _war_room_backend() -> str:
    try:
        from core.config.settings import get_settings

        return (
            getattr(get_settings(), "war_room_store_backend", "json") or "json"
        ).lower().strip()
    except Exception:  # noqa: BLE001
        return "json"


def _war_room_sync_url() -> str | None:
    try:
        from core.config.settings import get_settings

        from auto_client_acquisition.persistence.db_sync_url import (
            sync_sqlalchemy_url,
        )

        url = getattr(get_settings(), "database_url", "") or ""
        return sync_sqlalchemy_url(url) if url else None
    except Exception:  # noqa: BLE001
        return None


def get_default_war_room_leads_store() -> Any:
    """Return the configured war-room leads store singleton.

    ``war_room_store_backend=postgres`` returns the restart-durable
    :class:`PostgresWarRoomLeadsStore`; any other value (or a missing
    ``DATABASE_URL``, or an unreachable engine) falls back to the existing
    JSON-backed :class:`AutopilotJSONStore`. Both expose ``list_leads``,
    ``get_lead``, ``upsert_lead`` with the same contract.
    """
    global _DEFAULT
    if _DEFAULT is not None:
        return _DEFAULT
    if _war_room_backend() == "postgres":
        url = _war_room_sync_url()
        if url:
            try:
                _DEFAULT = PostgresWarRoomLeadsStore(database_url=url, create_tables=True)
                return _DEFAULT
            except Exception as exc:  # noqa: BLE001
                _LOG.warning(
                    "war_room_store_postgres_unavailable:%s", type(exc).__name__
                )
    # JSON fallback — reuse the existing store
    from dealix.revenue_ops_autopilot.store import AutopilotJSONStore

    _DEFAULT = AutopilotJSONStore()
    return _DEFAULT


def reset_default_war_room_leads_store() -> None:
    """Test helper — drop the cached singleton so the next call re-evaluates."""
    global _DEFAULT
    _DEFAULT = None


__all__ = [
    "PostgresWarRoomLeadsStore",
    "WarRoomLeadORM",
    "WarRoomLeadsBase",
    "get_default_war_room_leads_store",
    "reset_default_war_room_leads_store",
]
