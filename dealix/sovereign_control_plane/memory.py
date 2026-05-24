"""
Typed memory stores — §86.

Eight memory kinds (personal, sovereign, company, customer, partner,
outcome, market, trust) each backed by the same ``TypedMemoryStore``.
SOVEREIGN memory must never appear in external output — the
``MemoryManager.redact_for_external`` helper enforces that rule when
called on outbound payloads.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from dealix.sovereign_control_plane.types import DataSensitivity


class MemoryKind(StrEnum):
    PERSONAL = "personal"
    SOVEREIGN = "sovereign"
    COMPANY = "company"
    CUSTOMER = "customer"
    PARTNER = "partner"
    OUTCOME = "outcome"
    MARKET = "market"
    TRUST = "trust"


@dataclass
class MemoryEntry:
    scope_id: str
    key: str
    value: Any
    sensitivity: DataSensitivity
    updated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "scope_id": self.scope_id,
            "key": self.key,
            "value": self.value,
            "sensitivity": self.sensitivity.value,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }


class TypedMemoryStore:
    def __init__(self, kind: MemoryKind) -> None:
        self.kind = kind
        self._data: dict[str, dict[str, MemoryEntry]] = {}
        self._lock = threading.Lock()

    def write(
        self,
        scope_id: str,
        key: str,
        value: Any,
        sensitivity: DataSensitivity,
    ) -> MemoryEntry:
        entry = MemoryEntry(
            scope_id=scope_id,
            key=key,
            value=value,
            sensitivity=sensitivity,
            updated_at=datetime.now(UTC).isoformat(),
        )
        with self._lock:
            self._data.setdefault(scope_id, {})[key] = entry
        return entry

    def read(self, scope_id: str, key: str) -> MemoryEntry | None:
        return self._data.get(scope_id, {}).get(key)

    def query(
        self,
        scope_id: str,
        predicate: Callable[[MemoryEntry], bool] | None = None,
    ) -> list[MemoryEntry]:
        items = list(self._data.get(scope_id, {}).values())
        if predicate is None:
            return items
        return [e for e in items if predicate(e)]

    def forget(self, scope_id: str, key: str) -> bool:
        with self._lock:
            bucket = self._data.get(scope_id, {})
            if key in bucket:
                bucket.pop(key)
                return True
            return False


class MemoryManager:
    def __init__(self) -> None:
        self._stores: dict[MemoryKind, TypedMemoryStore] = {
            kind: TypedMemoryStore(kind) for kind in MemoryKind
        }

    def store(self, kind: MemoryKind) -> TypedMemoryStore:
        return self._stores[kind]

    def redact_for_external(self, payload: Any) -> Any:
        """Return a copy of ``payload`` with SOVEREIGN keys/values removed."""
        if isinstance(payload, dict):
            return {
                k: self.redact_for_external(v)
                for k, v in payload.items()
                if not self._is_sovereign_marker(k, v)
            }
        if isinstance(payload, list):
            return [self.redact_for_external(v) for v in payload]
        return payload

    @staticmethod
    def _is_sovereign_marker(key: Any, value: Any) -> bool:
        if isinstance(key, str) and key.startswith("sovereign_"):
            return True
        if isinstance(value, dict) and value.get("sensitivity") == DataSensitivity.SOVEREIGN.value:
            return True
        if isinstance(value, str) and value.upper() == "SOVEREIGN":
            return True
        return False
