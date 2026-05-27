"""Evidence Packs.

High-risk decisions (S3+ or high-risk tool use) must attach an evidence
pack: pointers to the signal(s), score breakdown, guardrail reports, and
any external references. Evidence packs are immutable once sealed.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class EvidencePack:
    id: str
    created_at: datetime
    decision_id: str
    items: list[dict[str, Any]] = field(default_factory=list)
    sealed: bool = False
    sealed_at: datetime | None = None

    def add(self, kind: str, ref: str, detail: dict[str, Any] | None = None) -> None:
        if self.sealed:
            raise ValueError("Cannot add to a sealed evidence pack.")
        self.items.append({"kind": kind, "ref": ref, "detail": detail or {}})

    def seal(self) -> None:
        self.sealed = True
        self.sealed_at = datetime.now(timezone.utc)


@dataclass
class EvidenceStore:
    _by_id: dict[str, EvidencePack] = field(default_factory=dict)

    def open(self, decision_id: str) -> EvidencePack:
        pack = EvidencePack(
            id=f"evd_{uuid.uuid4().hex[:10]}",
            created_at=datetime.now(timezone.utc),
            decision_id=decision_id,
        )
        self._by_id[pack.id] = pack
        return pack

    def get(self, pack_id: str) -> EvidencePack:
        return self._by_id[pack_id]

    def for_decision(self, decision_id: str) -> list[EvidencePack]:
        return [p for p in self._by_id.values() if p.decision_id == decision_id]

    def all(self) -> list[EvidencePack]:
        return list(self._by_id.values())


__all__ = ["EvidencePack", "EvidenceStore"]
