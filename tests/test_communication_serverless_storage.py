"""Regression tests for Issue #934 Communication OS storage."""

from __future__ import annotations

import importlib

import pytest
from sqlalchemy import create_engine

from intelligence.comms_storage import (
    CONTACT_LOG_KEY,
    SEQUENCES_KEY,
    FileCommsStorage,
    PostgresCommsStorage,
    build_communication_storage,
    communication_state_metadata,
)
from intelligence.serverless_communication_hub import ServerlessCommunicationHub


def test_file_adapter_has_no_constructor_side_effect(tmp_path):
    root = tmp_path / "not-created-yet"
    storage = FileCommsStorage(root)
    hub = ServerlessCommunicationHub(storage=storage)

    assert not root.exists()
    assert hub.readiness()["backend"] == "file"
    assert not root.exists()


def test_file_adapter_roundtrip(tmp_path):
    storage = FileCommsStorage(tmp_path / "comms")
    rows = [{"entry_id": "inbound-1", "status": "sent_externally"}]

    storage.write_list(CONTACT_LOG_KEY, rows)

    assert storage.read_list(CONTACT_LOG_KEY) == rows
    assert storage.read_list(SEQUENCES_KEY) == []


def test_serverless_hub_uses_injected_storage(tmp_path):
    storage = FileCommsStorage(tmp_path / "comms")
    hub = ServerlessCommunicationHub(storage=storage)

    entry = hub.log_inbound(
        contact_id="contact-1",
        company_name="Example Co",
        contact_name="Example Contact",
        channel="email",
        body_en="Inbound message",
        body_ar="رسالة واردة",
    )

    history = hub.get_contact_history("contact-1", "both")
    assert entry.direction == "inbound"
    assert history["count"] == 1


def test_production_rejects_file_or_tmp_storage(tmp_path):
    with pytest.raises(RuntimeError, match="durable PostgreSQL"):
        build_communication_storage(
            app_env="production",
            backend="file",
            file_root=tmp_path,
        )

    with pytest.raises(RuntimeError, match="durable PostgreSQL"):
        build_communication_storage(
            app_env="staging",
            backend="file",
            file_root="/tmp/dealix-comms",
        )


def test_database_adapter_roundtrip_with_test_engine():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    communication_state_metadata.create_all(engine)
    storage = PostgresCommsStorage(engine, namespace="test")

    contact_rows = [{"entry_id": "entry-1"}]
    sequence_rows = [{"sequence_id": "seq-1"}]
    storage.write_list(CONTACT_LOG_KEY, contact_rows)
    storage.write_list(SEQUENCES_KEY, sequence_rows)

    assert storage.read_list(CONTACT_LOG_KEY) == contact_rows
    assert storage.read_list(SEQUENCES_KEY) == sequence_rows
    assert storage.readiness() == {
        "ready": True,
        "backend": "postgres",
        "durable": True,
        "production_safe": True,
    }


def test_router_import_is_lazy_and_does_not_create_hub():
    import api.routers.ops_communication as module

    module = importlib.reload(module)

    assert module._hub is None
    paths = {route.path for route in module.router.routes}
    assert "/api/v1/ops/comms/readiness" in paths
    assert "/api/v1/ops/comms/stats" in paths
