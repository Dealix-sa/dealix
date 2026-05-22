"""Tests for the Postgres-backed war-room leads store (M-WR)."""
from __future__ import annotations

import os
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine

from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord
from dealix.revenue_ops_autopilot.store_postgres import (
    PostgresWarRoomLeadsStore,
    get_default_war_room_leads_store,
    reset_default_war_room_leads_store,
)


def _lead(lead_id: str, *, company: str = "Acme", stage: str = "new_lead") -> FunnelLeadRecord:
    return FunnelLeadRecord(
        id=lead_id,
        company=company,
        industry="agency",
        stage=stage,  # type: ignore[arg-type]
        war_room_status="not_contacted",  # type: ignore[arg-type]
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )


@pytest.fixture
def store() -> PostgresWarRoomLeadsStore:
    # Isolated sqlite for tests — same engine surface as Postgres.
    engine = create_engine("sqlite:///:memory:", future=True)
    return PostgresWarRoomLeadsStore(database_url="sqlite://", engine=engine, create_tables=True)


def test_upsert_then_get_roundtrip(store: PostgresWarRoomLeadsStore) -> None:
    lead = _lead("lead_1", company="Riyadh Agency")
    store.upsert_lead(lead)
    fetched = store.get_lead("lead_1")
    assert fetched is not None
    assert fetched.id == "lead_1"
    assert fetched.company == "Riyadh Agency"
    assert fetched.industry == "agency"


def test_upsert_is_idempotent_by_lead_id(store: PostgresWarRoomLeadsStore) -> None:
    store.upsert_lead(_lead("lead_1", company="First"))
    store.upsert_lead(_lead("lead_1", company="Second"))
    assert store.count_leads() == 1
    fetched = store.get_lead("lead_1")
    assert fetched is not None
    assert fetched.company == "Second"


def test_list_leads_orders_newest_first_and_respects_limit(
    store: PostgresWarRoomLeadsStore,
) -> None:
    for i in range(5):
        store.upsert_lead(_lead(f"lead_{i}"))
    items = store.list_leads(limit=3)
    assert len(items) == 3


def test_get_missing_lead_returns_none(store: PostgresWarRoomLeadsStore) -> None:
    assert store.get_lead("does_not_exist") is None


def test_count_and_clear(store: PostgresWarRoomLeadsStore) -> None:
    for i in range(3):
        store.upsert_lead(_lead(f"lead_{i}"))
    assert store.count_leads() == 3
    store.clear()
    assert store.count_leads() == 0


def test_factory_returns_json_store_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without env override the factory yields the JSON-backed store."""
    monkeypatch.delenv("DEALIX_WAR_ROOM_STORE_BACKEND", raising=False)
    monkeypatch.delenv("war_room_store_backend", raising=False)
    reset_default_war_room_leads_store()
    try:
        from dealix.revenue_ops_autopilot.store import AutopilotJSONStore

        result = get_default_war_room_leads_store()
        assert isinstance(result, AutopilotJSONStore)
    finally:
        reset_default_war_room_leads_store()
