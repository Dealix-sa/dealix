"""Security regression tests for Communication OS storage.

Validates path traversal prevention, input sanitization, and fail-closed behavior.
"""

from __future__ import annotations

import os
import pytest
from sqlalchemy import create_engine

from intelligence.comms_storage import (
    CONTACT_LOG_KEY,
    SEQUENCES_KEY,
    CommunicationStorageUnavailable,
    FileCommsStorage,
    PostgresCommsStorage,
    build_communication_storage,
    communication_state_metadata,
)
from intelligence.serverless_communication_hub import ServerlessCommunicationHub


class TestPathTraversalPrevention:
    """Ensure FileCommsStorage cannot escape its root directory."""

    def test_valid_keys_allowed(self, tmp_path):
        storage = FileCommsStorage(tmp_path)
        storage.write_list(CONTACT_LOG_KEY, [{"entry_id": "test"}])
        assert storage.read_list(CONTACT_LOG_KEY) == [{"entry_id": "test"}]

    def test_invalid_key_rejected(self, tmp_path):
        storage = FileCommsStorage(tmp_path)
        with pytest.raises(ValueError, match="Unsupported communication state key"):
            storage.write_list("../../../etc/passwd", [{"evil": True}])

    def test_path_traversal_in_key_blocked(self, tmp_path):
        """Even if key somehow passes validation, resolved path must stay in root."""
        storage = FileCommsStorage(tmp_path)
        # Direct _path call should validate and reject
        with pytest.raises((ValueError, CommunicationStorageUnavailable)):
            storage._path("../../../etc/passwd")

    def test_root_escape_via_resolved_path_blocked(self, tmp_path):
        """Symlink or .. in root itself should not allow escape."""
        root = tmp_path / "comms"
        root.mkdir()
        storage = FileCommsStorage(root)
        # Normal operation works
        storage.write_list(CONTACT_LOG_KEY, [{"entry_id": "safe"}])
        # But path must stay within root
        path = storage._path(CONTACT_LOG_KEY)
        assert path.resolve().is_relative_to(root.resolve())


class TestInputValidation:
    """Validate that malformed inputs fail safely."""

    def test_namespace_validation_rejects_empty(self):
        with pytest.raises(ValueError, match="namespace"):
            PostgresCommsStorage(
                create_engine("sqlite+pysqlite:///:memory:", future=True),
                namespace="",
            )

    def test_namespace_validation_rejects_special_chars(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
        # These should all fail validation (after strip where applicable)
        bad_cases = [
            "ns;drop table",      # semicolon injection
            "ns/../../../etc",    # path traversal in namespace
            "123start",           # must start with letter
            "a/b",                # slash not allowed
            "a.b",                # dot not allowed  
            "a space",            # space not allowed (strip won't help middle spaces)
        ]
        for bad in bad_cases:
            with pytest.raises(ValueError, match="namespace"):
                PostgresCommsStorage(engine, namespace=bad)

    def test_namespace_validation_accepts_safe(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
        for good in ["dealix", "test-ns", "test_ns", "a", "A123"]:
            storage = PostgresCommsStorage(engine, namespace=good)
            assert storage.namespace == good

    def test_non_dict_list_items_rejected_on_read(self, tmp_path):
        storage = FileCommsStorage(tmp_path)
        # Write valid data manually
        path = tmp_path / f"{CONTACT_LOG_KEY}.json"
        path.write_text('["not-a-dict"]', encoding="utf-8")
        with pytest.raises(CommunicationStorageUnavailable, match="non-dict"):
            storage.read_list(CONTACT_LOG_KEY)

    def test_non_dict_list_items_rejected_on_write(self, tmp_path):
        storage = FileCommsStorage(tmp_path)
        with pytest.raises(CommunicationStorageUnavailable, match="non-dict"):
            storage.write_list(CONTACT_LOG_KEY, ["not-a-dict"])

    def test_non_list_rejected_on_write(self, tmp_path):
        storage = FileCommsStorage(tmp_path)
        with pytest.raises(CommunicationStorageUnavailable, match="non-dict"):
            storage.write_list(CONTACT_LOG_KEY, {"not": "a-list"})


class TestFailClosed:
    """Ensure failures do not leak secrets or enable unsafe operations."""

    def test_readiness_does_not_leak_connection_string(self, tmp_path):
        storage = FileCommsStorage(tmp_path)
        result = storage.readiness()
        assert "connection" not in str(result).lower()
        assert "password" not in str(result).lower()
        assert "secret" not in str(result).lower()

    def test_file_storage_is_not_production_safe(self, tmp_path):
        storage = FileCommsStorage(tmp_path)
        result = storage.readiness()
        assert result["production_safe"] is False

    def test_production_rejects_file_backend(self, tmp_path):
        with pytest.raises(RuntimeError, match="durable PostgreSQL"):
            build_communication_storage(
                app_env="production",
                backend="file",
                file_root=tmp_path,
            )

    def test_staging_rejects_file_backend(self, tmp_path):
        with pytest.raises(RuntimeError, match="durable PostgreSQL"):
            build_communication_storage(
                app_env="staging",
                backend="file",
                file_root=tmp_path,
            )


class TestDatabaseAdapterSecurity:
    """Security tests for PostgreSQL/SQLite adapter."""

    def test_sqlite_namespace_isolation(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
        communication_state_metadata.create_all(engine)

        storage_a = PostgresCommsStorage(engine, namespace="tenant-a")
        storage_b = PostgresCommsStorage(engine, namespace="tenant-b")

        storage_a.write_list(CONTACT_LOG_KEY, [{"entry_id": "a"}])
        storage_b.write_list(CONTACT_LOG_KEY, [{"entry_id": "b"}])

        assert storage_a.read_list(CONTACT_LOG_KEY) == [{"entry_id": "a"}]
        assert storage_b.read_list(CONTACT_LOG_KEY) == [{"entry_id": "b"}]

    def test_database_url_does_not_appear_in_errors(self):
        """Connection failures must not echo the URL back."""
        with pytest.raises(CommunicationStorageUnavailable) as exc_info:
            PostgresCommsStorage.from_database_url(
                "postgresql://user:secret@localhost:5432/db",
                namespace="test",
            )
        error_str = str(exc_info.value)
        assert "secret" not in error_str.lower()
        assert "postgresql://" not in error_str.lower()

    def test_postgres_adapter_roundtrip_with_bad_data_rejected(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
        communication_state_metadata.create_all(engine)
        storage = PostgresCommsStorage(engine, namespace="test")

        with pytest.raises(CommunicationStorageUnavailable, match="non-dict"):
            storage.write_list(CONTACT_LOG_KEY, [{"valid": True}, "invalid"])
