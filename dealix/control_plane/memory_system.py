"""
Section 57 — Memory System.

Seven memory kinds, sharply separated. Outcome Memory is the most
commercially important; Personal/Sovereign Memory is the most sensitive.
The Memory System never blends kinds — every entry carries the kind on
its face so policy and audit can key off it.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from dealix.control_plane.data_classification import DataClass


class MemoryKind(StrEnum):
    PERSONAL = "personal"
    COMPANY = "company"
    CUSTOMER = "customer"
    PARTNER = "partner"
    OUTCOME = "outcome"
    MARKET = "market"
    TRUST = "trust"

    @property
    def default_sensitivity(self) -> DataClass:
        return {
            MemoryKind.PERSONAL: DataClass.SOVEREIGN,
            MemoryKind.COMPANY: DataClass.INTERNAL,
            MemoryKind.CUSTOMER: DataClass.CONFIDENTIAL,
            MemoryKind.PARTNER: DataClass.CONFIDENTIAL,
            MemoryKind.OUTCOME: DataClass.INTERNAL,
            MemoryKind.MARKET: DataClass.INTERNAL,
            MemoryKind.TRUST: DataClass.RESTRICTED,
        }[self]


@dataclass(frozen=True)
class MemoryEntry:
    entry_id: str
    kind: MemoryKind
    workspace_id: str
    title: str
    body: str
    sensitivity: DataClass
    tags: tuple[str, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class MemorySystem:
    def __init__(self) -> None:
        self._entries: dict[str, MemoryEntry] = {}

    def remember(
        self,
        *,
        kind: MemoryKind,
        workspace_id: str,
        title: str,
        body: str,
        sensitivity: DataClass | None = None,
        tags: Iterable[str] = (),
    ) -> MemoryEntry:
        entry = MemoryEntry(
            entry_id=f"mem_{uuid.uuid4().hex[:12]}",
            kind=kind,
            workspace_id=workspace_id,
            title=title,
            body=body,
            sensitivity=sensitivity or kind.default_sensitivity,
            tags=tuple(tags),
        )
        self._entries[entry.entry_id] = entry
        return entry

    def recall(
        self,
        *,
        kind: MemoryKind | None = None,
        workspace_id: str | None = None,
        tag: str | None = None,
    ) -> list[MemoryEntry]:
        entries = list(self._entries.values())
        if kind is not None:
            entries = [e for e in entries if e.kind == kind]
        if workspace_id is not None:
            entries = [e for e in entries if e.workspace_id == workspace_id]
        if tag is not None:
            entries = [e for e in entries if tag in e.tags]
        return entries

    def forget(self, entry_id: str) -> None:
        self._entries.pop(entry_id, None)

    def stats(self) -> dict[str, int]:
        counts: dict[str, int] = {k.value: 0 for k in MemoryKind}
        for entry in self._entries.values():
            counts[entry.kind.value] += 1
        counts["total"] = len(self._entries)
        return counts

    def to_dicts(self) -> list[dict[str, Any]]:
        return [
            {
                "entry_id": e.entry_id,
                "kind": e.kind.value,
                "workspace_id": e.workspace_id,
                "title": e.title,
                "sensitivity": e.sensitivity.label,
                "tags": list(e.tags),
                "created_at": e.created_at.isoformat(),
            }
            for e in self._entries.values()
        ]
