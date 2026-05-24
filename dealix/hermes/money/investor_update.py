"""Investor Update Builder — assembles a draft, never sends."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class InvestorUpdate:
    id: str
    title: str
    summary: str
    wins: list[str]
    risks: list[str]
    asks: list[str]
    metrics: dict[str, float]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    approved_to_send: bool = False


@dataclass
class InvestorUpdateBuilder:
    _by_id: dict[str, InvestorUpdate] = field(default_factory=dict)

    def draft(
        self,
        *,
        title: str,
        summary: str,
        wins: list[str],
        risks: list[str],
        asks: list[str],
        metrics: dict[str, float],
    ) -> InvestorUpdate:
        u = InvestorUpdate(
            id=f"inv_upd_{uuid.uuid4().hex[:10]}",
            title=title,
            summary=summary,
            wins=list(wins),
            risks=list(risks),
            asks=list(asks),
            metrics=dict(metrics),
        )
        self._by_id[u.id] = u
        return u

    def approve(self, update_id: str, *, by: str = "sami") -> InvestorUpdate:
        if by != "sami":
            raise PermissionError("Only Sami may approve investor updates.")
        u = self._by_id[update_id]
        u.approved_to_send = True
        return u

    def all(self) -> list[InvestorUpdate]:
        return list(self._by_id.values())


__all__ = ["InvestorUpdate", "InvestorUpdateBuilder"]
