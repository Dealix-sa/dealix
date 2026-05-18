"""Postgres-backed implementation of the proof ledger.

Mirrors :class:`auto_client_acquisition.proof_ledger.file_backend.FileProofLedger`
byte-for-byte at the public-API level so callers can swap backends without
behavioural change. Storage uses SQLAlchemy 2.0 (works with sqlite for tests
and Postgres in production — no driver-specific code in this module).

Hard contract (must match the file backend):
  * PII redaction happens **before** insert. Raw summary fields are stored
    only as the caller supplied them (we do not store an unredacted form
    that did not exist on the input event); the redacted variants are
    always written.
  * Customer handle anonymization on read is the export layer's job
    (``evidence_export.py``), NOT this storage layer.
  * Public methods: ``record``, ``list_events``, ``record_unit``, ``list_units``.
"""
from __future__ import annotations

import threading
from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    Engine,
    Integer,
    String,
    Text,
    create_engine,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from auto_client_acquisition.proof_ledger.schemas import (
    ProofEvent,
    RevenueWorkUnit,
)


class ProofLedgerBase(DeclarativeBase):
    """Dedicated declarative base for proof-ledger ORM tables.

    Kept separate from ``db.models.Base`` so the proof ledger can be
    bootstrapped against an in-memory SQLite engine in tests without
    pulling the entire app schema along for the ride.
    """


# Pydantic-only fields that have no native column in the migration-004
# ``proof_events`` schema. They are round-tripped losslessly inside the
# ``payload`` JSONB under this reserved key so callers that rely on the
# rich ProofEvent schema see no behavioural change across backends.
_AUX_PAYLOAD_KEY = "_proof_ledger_aux"
_AUX_FIELDS: tuple[str, ...] = (
    "summary_ar",
    "summary_en",
    "evidence_source",
    "confidence",
    "consent_for_publication",
    "redacted_summary_ar",
    "redacted_summary_en",
    "approval_status",
    "risk_level",
)


class ProofEventORM(ProofLedgerBase):
    """SQLAlchemy mapping for the ``proof_events`` table (migration 004).

    Column definitions match ``db/migrations/versions/20260513_004_proof_events.py``
    exactly so the ORM never writes a column production has not migrated.
    Rich :class:`ProofEvent` fields without a native column are persisted
    inside ``payload`` (see ``_AUX_FIELDS``).
    """

    __tablename__ = "proof_events"

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False, default="default")
    customer_handle: Mapped[str] = mapped_column(
        String(80), nullable=False, default="Saudi B2B customer"
    )
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    service_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    level: Mapped[str] = mapped_column(String(4), nullable=False, default="L1")
    claim: Mapped[str] = mapped_column(Text, nullable=False, default="")
    payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    evidence_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    evidence_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    customer_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    publish_consent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    consent_signature: Mapped[str | None] = mapped_column(String(256), nullable=True)
    approved_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), nullable=False, default=lambda: datetime.now(UTC)
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(), nullable=True)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    __table_args__ = (
        CheckConstraint(
            "level IN ('L1', 'L2', 'L3', 'L4', 'L5')",
            name="ck_proof_events_level",
        ),
    )


class RevenueWorkUnitORM(ProofLedgerBase):
    """SQLAlchemy mapping for the ``proof_revenue_work_units`` table.

    Matches ``db/migrations/versions/20260518_013_proof_revenue_work_units.py``.
    """

    __tablename__ = "proof_revenue_work_units"

    unit_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False, default="default")
    unit_type: Mapped[str] = mapped_column(String(64), nullable=False)
    customer_handle: Mapped[str] = mapped_column(
        String(80), nullable=False, default="Saudi B2B customer"
    )
    service_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    proof_event_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), nullable=False, default=lambda: datetime.now(UTC)
    )
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


def _orm_to_event(row: ProofEventORM) -> ProofEvent:
    payload = dict(row.payload or {})
    aux = payload.pop(_AUX_PAYLOAD_KEY, {}) or {}
    data: dict = {
        "id": row.event_id,
        "event_type": row.event_type,
        "tenant_id": row.tenant_id,
        "customer_handle": row.customer_handle,
        "service_id": row.service_id,
        "level": row.level,
        "claim": row.claim or "",
        "payload": payload,
        "evidence_url": row.evidence_url,
        "evidence_hash": row.evidence_hash,
        "customer_visible": row.customer_visible,
        "publish_consent": row.publish_consent,
        "consent_signature": row.consent_signature,
        "approved_by": row.approved_by,
        "approved_at": row.approved_at,
        "created_at": row.created_at,
        "deleted_at": row.deleted_at,
        "schema_version": row.schema_version,
    }
    for field in _AUX_FIELDS:
        if field in aux:
            data[field] = aux[field]
    return ProofEvent.model_validate(data)


def _orm_to_unit(row: RevenueWorkUnitORM) -> RevenueWorkUnit:
    return RevenueWorkUnit.model_validate({
        "id": row.unit_id,
        "unit_type": row.unit_type,
        "customer_handle": row.customer_handle,
        "service_id": row.service_id,
        "quantity": row.quantity,
        "description": row.description or "",
        "proof_event_id": row.proof_event_id,
        "created_at": row.created_at,
    })


class PostgresProofLedger:
    """SQLAlchemy-backed proof ledger.

    Same public surface as :class:`FileProofLedger`. Engine is supplied by
    the caller — the factory wires Postgres in production; tests pass a
    sqlite in-memory engine.
    """

    def __init__(
        self,
        *,
        engine: Engine | None = None,
        database_url: str | None = None,
        create_tables: bool = True,
    ) -> None:
        if engine is None:
            url = database_url or "sqlite:///:memory:"
            engine = create_engine(url, future=True)
        self._engine: Engine = engine
        self._sessionmaker = sessionmaker(self._engine, expire_on_commit=False, future=True)
        self._lock = threading.Lock()
        if create_tables:
            ProofLedgerBase.metadata.create_all(self._engine)

    # ─── ProofEvents ────────────────────────────────────────────

    def record(self, event: ProofEvent) -> ProofEvent:
        """Persist one event with redaction. Returns the stored event.

        Mirrors :meth:`FileProofLedger.record`: redacted summaries are
        computed at write time and persisted alongside the raw fields.
        """
        ar_redacted = redact_text(event.summary_ar) if event.summary_ar else ""
        en_redacted = redact_text(event.summary_en) if event.summary_en else ""

        stored = event.model_copy(update={
            "redacted_summary_ar": ar_redacted,
            "redacted_summary_en": en_redacted,
        })

        # The migration-004 ``claim`` column is NOT NULL — fall back to the
        # redacted English/Arabic summary so a real claim text is always set.
        claim = stored.claim or stored.redacted_summary_en or stored.redacted_summary_ar or ""

        payload = dict(stored.payload or {})
        payload[_AUX_PAYLOAD_KEY] = {
            "summary_ar": stored.summary_ar or "",
            "summary_en": stored.summary_en or "",
            "evidence_source": stored.evidence_source or "",
            "confidence": stored.confidence,
            "consent_for_publication": stored.consent_for_publication,
            "redacted_summary_ar": stored.redacted_summary_ar or "",
            "redacted_summary_en": stored.redacted_summary_en or "",
            "approval_status": stored.approval_status,
            "risk_level": stored.risk_level,
        }

        row = ProofEventORM(
            event_id=stored.id,
            tenant_id=stored.tenant_id,
            customer_handle=stored.customer_handle,
            event_type=str(stored.event_type),
            service_id=stored.service_id,
            level=stored.level,
            claim=claim,
            payload=payload,
            evidence_url=stored.evidence_url,
            evidence_hash=stored.evidence_hash,
            customer_visible=stored.customer_visible,
            publish_consent=stored.publish_consent or stored.consent_for_publication,
            consent_signature=stored.consent_signature,
            approved_by=stored.approved_by,
            approved_at=stored.approved_at,
            created_at=stored.created_at,
            deleted_at=stored.deleted_at,
            schema_version=stored.schema_version,
        )

        with self._lock, self._sessionmaker() as session:
            session.add(row)
            session.commit()
        return stored

    def list_events(
        self,
        *,
        customer_handle: str | None = None,
        event_type: str | None = None,
        limit: int = 100,
    ) -> list[ProofEvent]:
        """Return recent events, newest first, with optional filters."""
        stmt = select(ProofEventORM).order_by(ProofEventORM.created_at.desc())
        if customer_handle is not None:
            stmt = stmt.where(ProofEventORM.customer_handle == customer_handle)
        if event_type is not None:
            stmt = stmt.where(ProofEventORM.event_type == event_type)
        stmt = stmt.limit(limit)
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
        return [_orm_to_event(r) for r in rows]

    # ─── RevenueWorkUnits ───────────────────────────────────────

    def record_unit(self, unit: RevenueWorkUnit) -> RevenueWorkUnit:
        row = RevenueWorkUnitORM(
            unit_id=unit.id,
            unit_type=str(unit.unit_type),
            customer_handle=unit.customer_handle,
            service_id=unit.service_id,
            quantity=unit.quantity,
            description=unit.description or "",
            proof_event_id=unit.proof_event_id,
            created_at=unit.created_at,
        )
        with self._lock, self._sessionmaker() as session:
            session.add(row)
            session.commit()
        return unit

    def list_units(
        self,
        *,
        customer_handle: str | None = None,
        unit_type: str | None = None,
        limit: int = 100,
    ) -> list[RevenueWorkUnit]:
        stmt = select(RevenueWorkUnitORM).order_by(RevenueWorkUnitORM.created_at.desc())
        if customer_handle is not None:
            stmt = stmt.where(RevenueWorkUnitORM.customer_handle == customer_handle)
        if unit_type is not None:
            stmt = stmt.where(RevenueWorkUnitORM.unit_type == unit_type)
        stmt = stmt.limit(limit)
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
        return [_orm_to_unit(r) for r in rows]

    # ─── Test helpers ───────────────────────────────────────────

    def clear(self) -> None:
        """Test-only: drop and recreate the ledger tables."""
        with self._lock:
            ProofLedgerBase.metadata.drop_all(self._engine)
            ProofLedgerBase.metadata.create_all(self._engine)


__all__: list[str] = [
    "PostgresProofLedger",
    "ProofEventORM",
    "RevenueWorkUnitORM",
    "ProofLedgerBase",
]
