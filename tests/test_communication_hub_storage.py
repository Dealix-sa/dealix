from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from api.routers import ops_communication
from dealix.communication_hub import CommunicationHub
from dealix.communication_storage import (
    CommunicationStorageUnavailable,
    FileCommunicationStorage,
    PostgresCommunicationStorage,
    UnavailableCommunicationStorage,
    build_communication_storage,
)


def test_file_storage_is_explicitly_local_only(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("COMMUNICATION_HUB_STORAGE_BACKEND", "file")
    monkeypatch.setenv("COMMUNICATION_HUB_DATA_DIR", str(tmp_path))

    storage = build_communication_storage()

    assert isinstance(storage, FileCommunicationStorage)
    assert storage.readiness()["status"] == "ready"


def test_production_rejects_file_storage(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("COMMUNICATION_HUB_STORAGE_BACKEND", "file")
    monkeypatch.setenv("COMMUNICATION_HUB_DATA_DIR", str(tmp_path))

    with pytest.raises(CommunicationStorageUnavailable):
        build_communication_storage()


def test_postgres_storage_round_trip_and_readiness() -> None:
    engine = create_engine("sqlite:///:memory:", future=True)
    storage = PostgresCommunicationStorage(engine=engine, create_tables=True)

    assert storage.readiness()["status"] == "ready"
    assert storage.load("contact_log") == []

    storage.mutate(
        "contact_log",
        lambda rows: rows.append(
            {
                "contact_id": "contact-1",
                "company_name": "Example Company",
                "contact_name": "Example Contact",
                "channel": "email",
                "body_en": "Hello",
                "body_ar": "مرحبًا",
                "direction": "inbound",
                "status": "received",
                "tags": [],
            }
        ),
    )

    records = storage.load("contact_log")
    assert len(records) == 1
    assert records[0]["contact_id"] == "contact-1"


def test_postgres_storage_redacts_json_snapshot() -> None:
    engine = create_engine("sqlite:///:memory:", future=True)
    storage = PostgresCommunicationStorage(engine=engine, create_tables=True)

    payload = {
        "token": "secret-value",
        "nested": {"api_key": "key-value", "safe": "ok"},
    }
    storage.mutate("contact_log", lambda rows: rows.append(payload))

    stored = storage.load("contact_log")[0]
    assert stored["token"] == "[REDACTED]"
    assert stored["nested"]["api_key"] == "[REDACTED]"
    assert stored["nested"]["safe"] == "ok"


def test_postgres_storage_rejects_unknown_collection() -> None:
    engine = create_engine("sqlite:///:memory:", future=True)
    storage = PostgresCommunicationStorage(engine=engine, create_tables=True)

    with pytest.raises(ValueError, match="unsupported collection"):
        storage.load("unknown")


def test_file_storage_preserves_legacy_shape(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("COMMUNICATION_HUB_STORAGE_BACKEND", "file")
    monkeypatch.setenv("COMMUNICATION_HUB_DATA_DIR", str(tmp_path))
    legacy = tmp_path / "contact_log.json"
    legacy.write_text(json.dumps([{"contact_id": "legacy"}]), encoding="utf-8")

    storage = build_communication_storage()

    assert storage.load("contact_log") == [{"contact_id": "legacy"}]


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

    # Newer FastAPI versions retain internal router metadata entries alongside
    # concrete routes. Only route objects are expected to expose ``path``.
    route_paths = {
        route.path for route in app.routes if getattr(route, "path", None) is not None
    }
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
