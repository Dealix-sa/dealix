"""Lightweight developer-docs index for capabilities."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DeveloperDoc:
    capability_id: str
    title: str
    body: str


@dataclass
class DeveloperDocs:
    _by_capability: dict[str, DeveloperDoc] = field(default_factory=dict)

    def upsert(self, doc: DeveloperDoc) -> None:
        self._by_capability[doc.capability_id] = doc

    def get(self, capability_id: str) -> DeveloperDoc:
        return self._by_capability[capability_id]


__all__ = ["DeveloperDoc", "DeveloperDocs"]
