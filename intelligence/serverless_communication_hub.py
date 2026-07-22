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
        super().__init__(skip_fs_init=True)
        self._storage = storage

    @classmethod
    def from_environment(
        cls,
        *,
        app_env: str | None = None,
        backend: str | None = None,
        file_root: Path | str | None = None,
    ) -> "ServerlessCommunicationHub":
        """Create a hub backed by storage derived from environment variables."""
        storage = build_communication_storage(
            app_env=app_env,
            backend=backend,
            file_root=file_root,
        )
        return cls(storage=storage)

    def readiness(self) -> dict[str, Any]:
        """Return readiness state from the injected storage adapter."""
        if self._storage is None:
            return {"backend": "none", "production_safe": False}
        return self._storage.readiness()

    # --- persistence adapter ---

    async def _get_state(self, key: str) -> list[dict[str, Any]]:
        if self._storage is None:
            return []
        return await self._storage.read_list(key)

    async def _set_state(self, key: str, value: list[dict[str, Any]]) -> None:
        if self._storage is None:
            return
        await self._storage.write_list(key, value)

    async def _delete_state(self, key: str) -> None:
        if self._storage is None:
            return
        await self._storage.delete(key)

    # --- aliases used by communication_hub.py ---

    async def get_contact_log(self) -> list[dict[str, Any]]:
        return await self._get_state(CONTACT_LOG_KEY)

    async def set_contact_log(self, value: list[dict[str, Any]]) -> None:
        await self._set_state(CONTACT_LOG_KEY, value)

    async def get_sequences(self) -> list[dict[str, Any]]:
        return await self._get_state(SEQUENCES_KEY)

    async def set_sequences(self, value: list[dict[str, Any]]) -> None:
        await self._set_state(SEQUENCES_KEY, value)
