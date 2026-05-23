"""
Evidence pack.

Bundles the proofs (PDFs, screenshots, links, audit-trail excerpts) that
back a claim or a delivered outcome. Used by case-study capture and the
investor data room.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class EvidencePack:
    claim: str
    created_at: datetime
    items: list[str] = field(default_factory=list)
    approved_by: str | None = None

    def add(self, item: str) -> None:
        if item and item not in self.items:
            self.items.append(item)

    @property
    def is_complete(self) -> bool:
        return bool(self.items) and self.approved_by is not None


def new_pack(claim: str) -> EvidencePack:
    return EvidencePack(claim=claim, created_at=datetime.now(timezone.utc))
