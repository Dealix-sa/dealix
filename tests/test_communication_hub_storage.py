"""Communication OS durable-storage and serverless-safety regression tests."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from api.routers import ops_communication
from intelligence.communication_hub import CommunicationHub
from intelligence.communication_storage import (
    CommunicationStorageUnavailable,
    FileCommunicationStorage,
    PostgresCommunicationStorage,
    UnavailableCommunicationStorage,
    get_communication_storage,
)


def _sequence_steps() -> list[dict[str, object]]:
    return [
        {
            "channel": "email",
            "delay_days": 0,
            "subject_en": "Draft",
            "subject_ar": "مسودة",
            "body_en": "Approval required.",
            "body_ar": "الموافقة مطلوبة.",
        }
    ]


def test_file_adapter_is_lazy_and_round_trips(tmp_path: Path) -> None:
    base_path = tmp_path / "comms"
    storage = FileCommunicationStorage(base_path)
    hub = CommunicationHub(storage)

    assert not base_path.exists()
    assert hub.storage_readiness()["status"] == "ready"
    assert not base_path.exists()

    entry = hub.log_inbound(
        contact_id="contact-1",
        company_name="Example Company",
        contact_name="Example Contact",
        channel="email",
        body_en="Inbound",
        body_ar="وارد",
    )
    sequence = hub.create_sequence(
        name="Approval-first follow-up",
        contact_id="contact-1",
        company_name="Example Company",
        steps=_sequence_steps(),
    )

    assert base_path.exists()
    assert hub.get_contact_history("contact-1")["count"] == 1
    assert hub.get_sequence(sequence.sequence_id) is not None
    assert entry.direction == "inbound"


def test_postgres_adapter_persists_across_hub_instances() -> None:
    engine = create_engine("sqlite:///:memory:", future=True)
    storage = PostgresCommunicationStorage(engine=engine, create_tables=True)
    first_hub = CommunicationHub(storage)

    first_hub.log_inbound(
        contact_id="contact-2",
        company_name="Example Company",
        contact_name="Example Contact",
        channel="meeting",
        body_en="Meeting note",
        body_ar="ملاحظة اجتماع",
    )
    sequence = first_hub.create_sequence(
        name="Durable sequence",
        contact_id="contact-2",
        company_name="Example Company",
        steps=_sequence_steps(),
    )

    second_hub = CommunicationHub(
        PostgresCommunicationStorage(engine=engine, create_tables=False)
    )
    assert second_hub.get_contact_history("contact-2")["count"] == 1
    assert second_hub.get_sequence(sequence.sequence_id) is not None
    assert second_hub.storage_readiness() == {
        "status": "ready",
        "backend": "postgres",
        "durable": True,
        "write_ready": True,
        "reason": "postgres_available",
    }


def test_production_rejects_file_and_ephemeral_storage() -> None:
    storage = get_communication_storage(
        environment="production",
        backend="file",
        file_base_path="/tmp/communication-os",
    )

    assert storage.readiness() == {
        "status": "degraded",
        "backend": "unavailable",
        "durable": False,
        "write_ready": False,
        "reason": "production_requires_postgres",
    }


def test_missing_migration_degrades_and_mutations_fail_closed() -> None:
    engine = create_engine("sqlite:///:memory:", future=True)
    storage = PostgresCommunicationStorage(engine=engine, create_tables=False)

    assert storage.readiness()["status"] == "degraded"
    try:
        storage.mutate("contact_log", lambda rows: rows.append({}))
    except CommunicationStorageUnavailable:
        pass
    else:
        raise AssertionError("mutation must fail closed when the table is unavailable")


def test_router_stays_registered_and_returns_safe_degraded_signal(monkeypatch) -> None:
    unavailable = UnavailableCommunicationStorage("test_database_unavailable")
    monkeypatch.setattr(
        ops_communication,
        "_hub",
        CommunicationHub(unavailable),
    )
    app = FastAPI()
    app.include_router(ops_communication.router)
    client = TestClient(app, raise_server_exceptions=False)

    route_paths = {route.path for route in app.routes}
    assert "/api/v1/ops/comms/readiness" in route_paths
    assert "/api/v1/ops/comms/log-inbound" in route_paths

    readiness = client.get("/api/v1/ops/comms/readiness")
    assert readiness.status_code == 200
    assert readiness.json()["status"] == "degraded"
    assert readiness.json()["reason"] == "test_database_unavailable"

    response = client.post(
        "/api/v1/ops/comms/log-inbound",
        json={
            "contact_id": "contact-3",
            "company_name": "Example Company",
            "contact_name": "Example Contact",
            "channel": "email",
            "body_en": "Inbound",
            "body_ar": "وارد",
            "tags": [],
        },
    )
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "communication_storage_unavailable"
