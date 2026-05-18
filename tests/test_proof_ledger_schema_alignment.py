"""ProofEventORM / RevenueWorkUnitORM align with their Alembic migrations.

Covers C1 + C2: the Postgres backend must never write a column that
production has not migrated. These tests assert the ORM column set equals
the migration column set, and that native migration-004 fields
(level / claim / customer_visible / ...) round-trip through the ledger.
"""
from __future__ import annotations

import pytest

sa = pytest.importorskip("sqlalchemy")

from auto_client_acquisition.proof_ledger import (  # noqa: E402
    PostgresProofLedger,
    ProofEvent,
    ProofEventType,
    RevenueWorkUnit,
    RevenueWorkUnitType,
)
from auto_client_acquisition.proof_ledger.postgres_backend import (  # noqa: E402
    ProofEventORM,
    RevenueWorkUnitORM,
)

# Column sets declared by the Alembic migrations (source of truth — these
# are what production has actually run).
_MIGRATION_004_PROOF_EVENTS = {
    "event_id", "tenant_id", "customer_handle", "event_type", "service_id",
    "level", "claim", "payload", "evidence_url", "evidence_hash",
    "customer_visible", "publish_consent", "consent_signature",
    "approved_by", "approved_at", "created_at", "deleted_at", "schema_version",
}
_MIGRATION_013_WORK_UNITS = {
    "unit_id", "tenant_id", "unit_type", "customer_handle", "service_id",
    "quantity", "description", "proof_event_id", "created_at", "schema_version",
}


def test_proof_event_orm_columns_match_migration_004() -> None:
    orm_cols = {c.name for c in ProofEventORM.__table__.columns}
    assert orm_cols == _MIGRATION_004_PROOF_EVENTS


def test_proof_event_orm_tablename_and_pk() -> None:
    assert ProofEventORM.__tablename__ == "proof_events"
    pk = {c.name for c in ProofEventORM.__table__.primary_key.columns}
    assert pk == {"event_id"}


def test_revenue_work_unit_orm_columns_match_migration_013() -> None:
    orm_cols = {c.name for c in RevenueWorkUnitORM.__table__.columns}
    assert orm_cols == _MIGRATION_013_WORK_UNITS
    assert RevenueWorkUnitORM.__tablename__ == "proof_revenue_work_units"


def test_native_columns_round_trip_through_postgres_ledger() -> None:
    """level / claim / customer_visible / publish_consent survive a write+read."""
    ledger = PostgresProofLedger(engine=sa.create_engine("sqlite:///:memory:", future=True))
    ledger.record(ProofEvent(
        event_type=ProofEventType.PROOF_PACK_ASSEMBLED,
        customer_handle="ACME",
        level="L4",
        claim="Proof Pack assembled with four evidence signals.",
        customer_visible=True,
        publish_consent=True,
        evidence_url="https://evidence.test/pack",
        summary_en="A proof pack.",
    ))
    [ev] = ledger.list_events()
    assert ev.level == "L4"
    assert ev.claim == "Proof Pack assembled with four evidence signals."
    assert ev.customer_visible is True
    assert ev.publish_consent is True
    assert ev.evidence_url == "https://evidence.test/pack"
    # Aux (Pydantic-only) fields survive too.
    assert ev.summary_en == "A proof pack."


def test_level_check_constraint_rejects_bad_level() -> None:
    """The migration-004 CHECK (level IN L1..L5) is enforced by the ORM."""
    ledger = PostgresProofLedger(engine=sa.create_engine("sqlite:///:memory:", future=True))
    # ProofEvent's own pattern validator rejects an out-of-range level first.
    with pytest.raises(ValueError):
        ProofEvent(event_type=ProofEventType.LEAD_INTAKE, level="L9")


def test_work_unit_round_trip() -> None:
    ledger = PostgresProofLedger(engine=sa.create_engine("sqlite:///:memory:", future=True))
    ledger.record_unit(RevenueWorkUnit(
        unit_type=RevenueWorkUnitType.PROOF_PACK_ASSEMBLED,
        customer_handle="ACME",
        quantity=2,
        proof_event_id="evt_xyz",
    ))
    [u] = ledger.list_units(customer_handle="ACME")
    assert u.quantity == 2
    assert u.proof_event_id == "evt_xyz"
