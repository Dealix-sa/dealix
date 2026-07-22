"""Storage adapters for the approval-first Communication OS.

Production must use durable PostgreSQL storage. Local development and tests may
use an explicit file adapter. No adapter sends messages externally.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    MetaData,
    String,
    Table,
    and_,
    create_engine,
    insert,
    select,
    update,
)
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url
from core.config.settings import get_settings
from core.utils import utcnow

CONTACT_LOG_KEY = "contact_log"
SEQUENCES_KEY = "sequences"
_ALLOWED_KEYS = frozenset({CONTACT_LOG_KEY, SEQUENCES_KEY})

# Security: restrict namespace to safe characters only
_NAMESPACE_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]{0,62}$")


class CommunicationStorageUnavailable(RuntimeError):
    """Raised when durable communication state cannot be read or written."""


@runtime_checkable
class CommunicationStorage(Protocol):
    """Minimal persistence contract used by :class:`CommunicationHub`."""

    backend_name: str
    durable: bool

    def read_list(self, key: str) -> list[dict[str, Any]]:
        """Read one list-valued state document."""

    def write_list(self, key: str, data: list[dict[str, Any]]) -> None:
        """Atomically replace one list-valued state document."""

    def readiness(self) -> dict[str, Any]:
        """Return a secret-free readiness result."""


def _validated_key(key: str) -> str:
    if key not in _ALLOWED_KEYS:
        raise ValueError(f"Unsupported communication state key: {key}")
    return key


def _safe_namespace(namespace: str) -> str:
    """Validate namespace to prevent injection and path traversal."""
    ns = namespace.strip()
    if not ns or not _NAMESPACE_PATTERN.match(ns):
        raise ValueError(
            "Communication storage namespace must start with a letter, "
            "contain only alphanumeric characters, hyphens, and underscores, "
            "and be between 1 and 63 characters long."
        )
    return ns


class FileCommsStorage:
    """Explicit local/test adapter backed by JSON files.

    The directory is created only on the first write. Constructing this adapter
    has no filesystem side effects, which keeps imports safe on serverless
    read-only filesystems.
    """

    backend_name = "file"
    durable = False

    def __init__(self, root: Path | str = Path("data/comms")) -> None:
        self.root = Path(root).resolve()

    def _path(self, key: str) -> Path:
        """Resolve storage path, preventing path traversal outside root."""
        validated = _validated_key(key)
        target = (self.root / f"{validated}.json").resolve()
        # Security: ensure resolved path is within root directory
        try:
            target.relative_to(self.root)
        except ValueError as exc:
            raise CommunicationStorageUnavailable(
                "Communication storage path is outside the allowed root directory"
            ) from exc
        return target

    def read_list(self, key: str) -> list[dict[str, Any]]:
        path = self._path(key)
        if not path.exists():
            return []
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CommunicationStorageUnavailable(
                "Communication file storage is unavailable"
            ) from exc
        if not isinstance(raw, list):
            raise CommunicationStorageUnavailable(
                "Communication file storage contains invalid state"
            )
        # Validate list items are dicts (defense against deserialization issues)
        if not all(isinstance(item, dict) for item in raw):
            raise CommunicationStorageUnavailable(
                "Communication file storage contains non-dict entries"
            )
        return raw

    def write_list(self, key: str, data: list[dict[str, Any]]) -> None:
        path = self._path(key)
        # Validate data before writing
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise CommunicationStorageUnavailable(
                "Cannot write non-dict entries to communication storage"
            )
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = path.with_suffix(path.suffix + ".tmp")
            tmp_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            tmp_path.replace(path)
        except OSError as exc:
            raise CommunicationStorageUnavailable(
                "Communication file storage is unavailable"
            ) from exc

    def readiness(self) -> dict[str, Any]:
        return {
            "ready": True,
            "backend": self.backend_name,
            "durable": self.durable,
            "production_safe": False,
        }


communication_state_metadata = MetaData()
communication_state_table = Table(
    "communication_state",
    communication_state_metadata,
    Column("namespace", String(64), primary_key=True),
    Column("state_key", String(64), primary_key=True),
    Column("payload", JSON, nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)


class PostgresCommsStorage:
    """Durable production adapter backed by the ``communication_state`` table."""

    backend_name = "postgres"
    durable = True

    def __init__(self, engine: Engine, *, namespace: str = "dealix") -> None:
        self.namespace = _safe_namespace(namespace)
        self._engine = engine

    @classmethod
    def from_database_url(
        cls,
        database_url: str,
        *,
        namespace: str = "dealix",
    ) -> "PostgresCommsStorage":
        sync_url = sync_sqlalchemy_url(database_url)
        if not sync_url:
            raise CommunicationStorageUnavailable(
                "Communication database configuration is unavailable"
            )
        try:
            engine = create_engine(sync_url, future=True, pool_pre_ping=True)
        except (ImportError, ModuleNotFoundError, SQLAlchemyError) as exc:
            raise CommunicationStorageUnavailable(
                "Communication database configuration is unavailable"
            ) from exc
        return cls(engine, namespace=namespace)

    def _predicate(self, key: str):
        return and_(
            communication_state_table.c.namespace == self.namespace,
            communication_state_table.c.state_key == _validated_key(key),
        )

    def read_list(self, key: str) -> list[dict[str, Any]]:
        try:
            with self._engine.connect() as connection:
                payload = connection.execute(
                    select(communication_state_table.c.payload).where(
                        self._predicate(key)
                    )
                ).scalar_one_or_none()
        except SQLAlchemyError as exc:
            raise CommunicationStorageUnavailable(
                "Durable communication storage is unavailable"
            ) from exc
        if payload is None:
            return []
        if not isinstance(payload, list):
            raise CommunicationStorageUnavailable(
                "Durable communication storage contains invalid state"
            )
        # Validate list items are dicts
        if not all(isinstance(item, dict) for item in payload):
            raise CommunicationStorageUnavailable(
                "Durable communication storage contains non-dict entries"
            )
        return payload

    def write_list(self, key: str, data: list[dict[str, Any]]) -> None:
        # Validate data before writing
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise CommunicationStorageUnavailable(
                "Cannot write non-dict entries to communication storage"
            )
        now = utcnow()
        try:
            with self._engine.begin() as connection:
                exists = connection.execute(
                    select(communication_state_table.c.state_key).where(
                        self._predicate(key)
                    )
                ).scalar_one_or_none()
                if exists is None:
                    connection.execute(
                        insert(communication_state_table).values(
                            namespace=self.namespace,
                            state_key=_validated_key(key),
                            payload=data,
                            updated_at=now,
                        )
                    )
                else:
                    connection.execute(
                        update(communication_state_table)
                        .where(self._predicate(key))
                        .values(payload=data, updated_at=now)
                    )
        except SQLAlchemyError as exc:
            raise CommunicationStorageUnavailable(
                "Durable communication storage is unavailable"
            ) from exc

    def readiness(self) -> dict[str, Any]:
        try:
            with self._engine.connect() as connection:
                connection.execute(
                    select(communication_state_table.c.state_key).limit(1)
                )
        except SQLAlchemyError as exc:
            return {
                "ready": False,
                "backend": self.backend_name,
                "durable": self.durable,
                "production_safe": True,
                "error_type": type(exc).__name__,
            }
        return {
            "ready": True,
            "backend": self.backend_name,
            "durable": self.durable,
            "production_safe": True,
        }


def build_communication_storage(
    *,
    app_env: str | None = None,
    backend: str | None = None,
    file_root: Path | str | None = None,
    engine: Engine | None = None,
) -> CommunicationStorage:
    """Build the configured adapter without connecting or writing at import time."""

    settings = get_settings()
    environment = (app_env or settings.app_env).strip().lower()
    selected = (
        backend
        or os.environ.get("DEALIX_COMMS_STORAGE_BACKEND")
        or ("postgres" if environment in {"production", "staging"} else "file")
    ).strip().lower()

    if environment in {"production", "staging"} and selected != "postgres":
        raise RuntimeError(
            "Serverless Communication OS requires durable PostgreSQL storage"
        )

    if selected == "file":
        root = (
            file_root
            or os.environ.get("DEALIX_COMMS_FILE_ROOT")
            or Path("data/comms")
        )
        return FileCommsStorage(root)

    if selected == "postgres":
        namespace = os.environ.get("DEALIX_COMMS_NAMESPACE", "dealix")
        if engine is not None:
            return PostgresCommsStorage(engine, namespace=namespace)
        return PostgresCommsStorage.from_database_url(
            settings.database_url,
            namespace=namespace,
        )

    raise ValueError(f"Unsupported communication storage backend: {selected}")


__all__ = [
    "CONTACT_LOG_KEY",
    "SEQUENCES_KEY",
    "CommunicationStorage",
    "CommunicationStorageUnavailable",
    "FileCommsStorage",
    "PostgresCommsStorage",
    "build_communication_storage",
    "communication_state_metadata",
    "communication_state_table",
]
