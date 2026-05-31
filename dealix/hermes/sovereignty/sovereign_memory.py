"""Sovereign memory — Sami's permanent context that no agent can mutate."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class SovereignFact:
    key: str
    value: str
    set_by: str = "Sami"
    set_at: str = ""


@dataclass
class SovereignMemory:
    _facts: dict[str, SovereignFact] = field(default_factory=dict)
    _readonly: bool = False

    def set(self, key: str, value: str, set_by: str = "Sami") -> SovereignFact:
        if self._readonly:
            raise PermissionError("sovereign memory is sealed; reopen explicitly to mutate")
        fact = SovereignFact(
            key=key, value=value, set_by=set_by,
            set_at=datetime.now(UTC).isoformat(),
        )
        self._facts[key] = fact
        return fact

    def get(self, key: str) -> SovereignFact | None:
        return self._facts.get(key)

    def all(self) -> list[SovereignFact]:
        return list(self._facts.values())

    def seal(self) -> None:
        self._readonly = True

    def reopen(self) -> None:
        self._readonly = False
