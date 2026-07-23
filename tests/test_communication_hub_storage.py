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


def test_staging_and_production_reject_file_and_ephemeral_storage() -> None:
    for environment in ("staging", "production"):
        storage = get_communication_storage(
            environment=environment,
            backend="file",
            file_base_path="/tmp/communication-os",
        )

        assert storage.readiness() == {
            "status": "degraded",
            "backend": "unavailable",
            "durable": False,
            "write_ready": False,
            "reason": f"{environment}_requires_postgres",
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
    monkeypatch.setenv("ADMIN_API_KEYS", "test-admin")
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

    headers = {"X-Admin-API-Key": "test-admin"}
    readiness = client.get("/api/v1/ops/comms/readiness", headers=headers)
    assert readiness.status_code == 200
    assert readiness.json()["status"] == "degraded"
    assert readiness.json()["reason"] == "test_database_unavailable"

    response = client.post(
        "/api/v1/ops/comms/log-inbound",
        headers=headers,
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


def test_router_never_echoes_internal_exception_details(monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", "test-admin")
    sensitive_marker = "postgresql://user:secret@example.invalid/dealix"

    class ExplodingHub:
        def create_draft(self, **_: object) -> None:
            raise ValueError(sensitive_marker)

        def advance_sequence(self, *_: object) -> None:
            raise RuntimeError(sensitive_marker)

    monkeypatch.setattr(ops_communication, "_hub", ExplodingHub())
    app = FastAPI()
    app.include_router(ops_communication.router)
    client = TestClient(app, raise_server_exceptions=False)
    headers = {"X-Admin-API-Key": "test-admin"}

    draft = client.post(
        "/api/v1/ops/comms/draft",
        headers=headers,
        json={
            "contact_id": "contact-4",
            "company_name": "Example Company",
            "contact_name": "Example Contact",
            "channel": "email",
            "subject_en": "Draft",
            "subject_ar": "مسودة",
            "body_en": "Approval required.",
            "body_ar": "الموافقة مطلوبة.",
            "tags": [],
            "lang": "both",
        },
    )
    advance = client.post(
        "/api/v1/ops/comms/sequence/sequence-1/advance",
        headers=headers,
        json={"actor": "reviewer"},
    )

    for response in (draft, advance):
        assert response.status_code == 400
        assert response.json()["detail"]["code"] == "communication_operation_rejected"
        assert sensitive_marker not in response.text


def test_router_requires_admin_key_until_storage_is_tenant_scoped(
    monkeypatch,
) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", "test-admin")
    app = FastAPI()
    app.include_router(ops_communication.router)
    client = TestClient(app, raise_server_exceptions=False)

    missing = client.get("/api/v1/ops/comms/readiness")
    invalid = client.get(
        "/api/v1/ops/comms/readiness",
        headers={"X-Admin-API-Key": "wrong-admin"},
    )

    assert missing.status_code == 401
    assert invalid.status_code == 403
