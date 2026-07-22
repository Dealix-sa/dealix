"""Serverless-safe CommunicationHub backed by an explicit storage adapter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from intelligence.comms_storage import (
    CONTACT_LOG_KEY,
    SEQUENCES_KEY,
    CommunicationStorage,
    build_communication_storage,
)
from intelligence.communication_hub import CommunicationHub


class ServerlessCommunicationHub(CommunicationHub):
    """Communication hub with no filesystem side effects at import or init time.

    The inherited business rules remain unchanged. Only persistence is replaced
    by the configured storage adapter. Production and staging are forced to use
    durable PostgreSQL storage by ``build_communication_storage``.
    """

    def __init__(self, storage: CommunicationStorage | None = None) -> None:
        self.storage = storage or build_communication_storage()

    def _storage_key(self, path: Path) -> str:
        if path == self.LOG_PATH:
            return CONTACT_LOG_KEY
        if path == self.SEQUENCE_PATH:
            return SEQUENCES_KEY
        raise ValueError(f"Unsupported communication path: {path}")

    def _ensure_files(self) -> None:
        """Compatibility no-op; storage initialization is adapter-owned."""

    def _read_json(self, path: Path) -> list[dict[str, Any]]:
        return self.storage.read_list(self._storage_key(path))

    def _write_json(self, path: Path, data: list[dict[str, Any]]) -> None:
        self.storage.write_list(self._storage_key(path), data)

    def readiness(self) -> dict[str, Any]:
        """Return a secret-free storage readiness result."""

        return self.storage.readiness()


__all__ = ["ServerlessCommunicationHub"]
