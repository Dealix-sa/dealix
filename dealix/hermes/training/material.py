"""Library of training materials (decks, exercises, runbooks)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class TrainingMaterial:
    id: str
    title: str
    kind: str       # "deck" | "exercise" | "runbook"
    body: str
    language: str   # "ar" | "en" | "ar+en"


@dataclass
class MaterialLibrary:
    _by_id: dict[str, TrainingMaterial] = field(default_factory=dict)

    def add(self, *, title: str, kind: str, body: str, language: str = "ar+en") -> TrainingMaterial:
        m = TrainingMaterial(
            id=f"mtl_{uuid.uuid4().hex[:10]}",
            title=title,
            kind=kind,
            body=body,
            language=language,
        )
        self._by_id[m.id] = m
        return m

    def all(self) -> list[TrainingMaterial]:
        return list(self._by_id.values())


__all__ = ["MaterialLibrary", "TrainingMaterial"]
