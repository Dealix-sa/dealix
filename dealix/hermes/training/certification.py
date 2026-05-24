"""Certification ledger — who passed which workshop."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class Certification:
    id: str
    person: str
    workshop_id: str
    issued_at: datetime


@dataclass
class CertificationLedger:
    _entries: list[Certification] = field(default_factory=list)

    def issue(self, *, person: str, workshop_id: str) -> Certification:
        c = Certification(
            id=f"crt_{uuid.uuid4().hex[:10]}",
            person=person,
            workshop_id=workshop_id,
            issued_at=datetime.now(timezone.utc),
        )
        self._entries.append(c)
        return c

    def all(self) -> list[Certification]:
        return list(self._entries)


__all__ = ["Certification", "CertificationLedger"]
