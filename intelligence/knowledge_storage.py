"""Durable, serverless-safe storage for Knowledge and Research OS.

Routers import this module during application startup, so constructors must not
touch the filesystem or connect to the database. Reads and mutations are lazy.
Production and staging default to PostgreSQL; local and test environments use
the explicit file adapter.
"""

from __future__ import annotations

import copy
import json
import os
import threading
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol, TypeVar

from sqlalchemy import JSON, DateTime, String, create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url
from core.config.settings import get_settings

MutationResult = TypeVar("MutationResult")


class KnowledgeStorageUnavailable(RuntimeError):
    """Raised when Knowledge OS cannot safely access durable storage."""


class KnowledgeStorage(Protocol):
    """Storage contract used by :class:`KnowledgeAccumulator`."""

    backend_name: str
    durable: bool

    def read(self) -> list[dict[str, Any]]:
        """Return a detached snapshot of accumulated knowledge."""

    def mutate(
        self,
        mutation: Callable[[list[dict[str, Any]]], MutationResult],
    ) -> MutationResult:
        """Atomically mutate accumulated knowledge."""

    def readiness(self) -> dict[str, Any]:
        """Return a non-secret backend readiness signal."""


def _validate_snapshot(data: object) -> list[dict[str, Any]]:
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise KnowledgeStorageUnavailable("Knowledge storage contains an invalid snapshot")
    return data


class FileKnowledgeStorage:
    """Lazy JSON-file adapter for local development and tests only."""

    backend_name = "file"
    durable = False

    def __init__(
        self,
        store_path: Path | str = Path("data/knowledge/accumulated_intel.json"),
    ) -> None:
        self._store_path = Path(store_path)
        self._lock = threading.RLock()

    def _read_unlocked(self) -> list[dict[str, Any]]:
        if not self._store_path.exists():
            return []
        try:
            data = json.loads(self._store_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise KnowledgeStorageUnavailable(
                "Knowledge file storage could not be read safely"
            ) from exc
        return _validate_snapshot(data)

    def read(self) -> list[dict[str, Any]]:
        with self._lock:
            return copy.deepcopy(self._read_unlocked())

    def mutate(
        self,
        mutation: Callable[[list[dict[str, Any]]], MutationResult],
    ) -> MutationResult:
        with self._lock:
            data = self._read_unlocked()
            result = mutation(data)
            try:
                self._store_path.parent.mkdir(parents=True, exist_ok=True)
                temp_path = self._store_path.with_suffix(f"{self._store_path.suffix}.tmp")
                temp_path.write_text(
                    json.dumps(data, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                temp_path.replace(self._store_path)
            except Exception as exc:
                raise KnowledgeStorageUnavailable("Knowledge file storage is not writable") from exc
            return result

    def readiness(self) -> dict[str, Any]:
        try:
            self.read()
        except KnowledgeStorageUnavailable:
            return {
                "status": "degraded",
                "backend": self.backend_name,
                "durable": self.durable,
                "write_ready": False,
                "reason": "file_storage_unavailable",
            }
        return {
            "status": "ready",
            "backend": self.backend_name,
            "durable": self.durable,
            "write_ready": True,
            "reason": "local_or_test_file_backend",
        }


class _KnowledgeStorageBase(DeclarativeBase):
    pass


class KnowledgeSnapshotORM(_KnowledgeStorageBase):
    """Single transactional snapshot for accumulated knowledge."""

    __tablename__ = "knowledge_accumulator_snapshots"

    collection: Mapped[str] = mapped_column(String(32), primary_key=True)
    data: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PostgresKnowledgeStorage:
    """Transactional JSON snapshot storage backed by PostgreSQL."""

    backend_name = "postgres"
    durable = True
    _COLLECTION = "entries"

    def __init__(
        self,
        *,
        engine: Engine | None = None,
        database_url: str | None = None,
        create_tables: bool = False,
    ) -> None:
        if engine is None:
            if not database_url:
                raise ValueError("database_url is required for PostgreSQL knowledge storage")
            engine = create_engine(
                database_url,
                future=True,
                pool_pre_ping=True,
                pool_size=2,
                max_overflow=2,
                pool_timeout=10,
                pool_recycle=1800,
            )
        self._engine = engine
        self._sessionmaker = sessionmaker(
            self._engine,
            expire_on_commit=False,
            future=True,
        )
        if create_tables:
            _KnowledgeStorageBase.metadata.create_all(self._engine)

    def read(self) -> list[dict[str, Any]]:
        try:
            with self._sessionmaker() as session:
                row = session.get(KnowledgeSnapshotORM, self._COLLECTION)
                data = row.data if row is not None else []
                return copy.deepcopy(_validate_snapshot(data))
        except KnowledgeStorageUnavailable:
            raise
        except Exception as exc:
            raise KnowledgeStorageUnavailable("Durable knowledge storage is unavailable") from exc

    def mutate(
        self,
        mutation: Callable[[list[dict[str, Any]]], MutationResult],
    ) -> MutationResult:
        try:
            with self._sessionmaker() as session:
                row = session.execute(
                    select(KnowledgeSnapshotORM)
                    .where(KnowledgeSnapshotORM.collection == self._COLLECTION)
                    .with_for_update()
                ).scalar_one_or_none()
                if row is None:
                    row = KnowledgeSnapshotORM(
                        collection=self._COLLECTION,
                        data=[],
                        updated_at=datetime.now(UTC),
                    )
                    session.add(row)
                data = copy.deepcopy(_validate_snapshot(row.data or []))
                result = mutation(data)
                row.data = data
                row.updated_at = datetime.now(UTC)
                session.commit()
                return result
        except KnowledgeStorageUnavailable:
            raise
        except Exception as exc:
            raise KnowledgeStorageUnavailable(
                "Durable knowledge storage mutation failed closed"
            ) from exc

    def readiness(self) -> dict[str, Any]:
        try:
            with self._sessionmaker() as session:
                session.execute(select(KnowledgeSnapshotORM.collection).limit(1)).all()
        except Exception:
            return {
                "status": "degraded",
                "backend": self.backend_name,
                "durable": self.durable,
                "write_ready": False,
                "reason": "postgres_unavailable_or_migration_missing",
            }
        return {
            "status": "ready",
            "backend": self.backend_name,
            "durable": self.durable,
            "write_ready": True,
            "reason": "postgres_available",
        }


class UnavailableKnowledgeStorage:
    """Fail-closed backend that keeps Knowledge and Research routers importable."""

    backend_name = "unavailable"
    durable = False

    def __init__(self, reason: str) -> None:
        self._reason = reason

    def read(self) -> list[dict[str, Any]]:
        raise KnowledgeStorageUnavailable("Knowledge storage is not configured safely")

    def mutate(
        self,
        mutation: Callable[[list[dict[str, Any]]], MutationResult],
    ) -> MutationResult:
        raise KnowledgeStorageUnavailable(
            "Knowledge storage mutation blocked because durable storage is unavailable"
        )

    def readiness(self) -> dict[str, Any]:
        return {
            "status": "degraded",
            "backend": self.backend_name,
            "durable": self.durable,
            "write_ready": False,
            "reason": self._reason,
        }


def get_knowledge_storage(
    *,
    environment: str | None = None,
    backend: str | None = None,
    database_url: str | None = None,
    file_store_path: Path | str = Path("data/knowledge/accumulated_intel.json"),
) -> KnowledgeStorage:
    """Select storage without performing filesystem or network I/O."""

    settings = get_settings()
    environment = (environment or settings.app_env).strip().lower()
    selected_backend = (
        backend
        or os.getenv("DEALIX_KNOWLEDGE_STORAGE_BACKEND", "").strip().lower()
        or ("postgres" if environment in {"staging", "production"} else "file")
    )

    if environment == "production" and selected_backend != "postgres":
        return UnavailableKnowledgeStorage("production_requires_postgres")
    if selected_backend == "file":
        return FileKnowledgeStorage(file_store_path)
    if selected_backend != "postgres":
        return UnavailableKnowledgeStorage("unsupported_storage_backend")

    raw_url = (database_url or settings.database_url or "").strip()
    if not raw_url:
        return UnavailableKnowledgeStorage("database_url_missing")
    try:
        return PostgresKnowledgeStorage(
            database_url=sync_sqlalchemy_url(raw_url),
            create_tables=False,
        )
    except Exception:
        return UnavailableKnowledgeStorage("postgres_configuration_invalid")


__all__ = [
    "FileKnowledgeStorage",
    "KnowledgeSnapshotORM",
    "KnowledgeStorage",
    "KnowledgeStorageUnavailable",
    "PostgresKnowledgeStorage",
    "UnavailableKnowledgeStorage",
    "get_knowledge_storage",
]
