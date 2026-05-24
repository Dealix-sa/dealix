"""
Section 70 — Scale/Kill Operating Board.

A decision surface: which offers, agents, tools, partners, verticals, and
assets to *scale*, *pause*, or *kill*. Score weights are explicit so the
doctrine is auditable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class KillReason(StrEnum):
    NO_DEMAND = "no_demand"
    LOW_MARGIN = "low_margin"
    HIGH_RISK = "high_risk"
    HIGH_DELIVERY_BURDEN = "high_delivery_burden"
    NO_DATA_MOAT = "no_data_moat"
    NO_CHANNEL = "no_channel"
    TOO_MUCH_FOUNDER_TIME = "too_much_founder_time"


@dataclass
class ScaleScore:
    revenue_score: float = 0.0
    repeatability_score: float = 0.0
    margin_score: float = 0.0
    data_moat_score: float = 0.0
    partner_score: float = 0.0
    trust_score: float = 0.0
    delivery_score: float = 0.0

    def total(self) -> float:
        return (
            self.revenue_score
            + self.repeatability_score
            + self.margin_score
            + self.data_moat_score
            + self.partner_score
            + self.trust_score
            + self.delivery_score
        ) / 7.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "revenue_score": self.revenue_score,
            "repeatability_score": self.repeatability_score,
            "margin_score": self.margin_score,
            "data_moat_score": self.data_moat_score,
            "partner_score": self.partner_score,
            "trust_score": self.trust_score,
            "delivery_score": self.delivery_score,
            "total": round(self.total(), 4),
        }


@dataclass
class _Entry:
    entity_id: str
    entity_kind: str
    label: str
    score: ScaleScore = field(default_factory=ScaleScore)
    kill_reasons: list[KillReason] = field(default_factory=list)
    notes: str = ""

    def verdict(self, *, scale_threshold: float, kill_threshold: float) -> str:
        if self.kill_reasons:
            return "kill"
        total = self.score.total()
        if total >= scale_threshold:
            return "scale"
        if total <= kill_threshold:
            return "kill"
        return "pause"

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_kind": self.entity_kind,
            "label": self.label,
            "score": self.score.to_dict(),
            "kill_reasons": [r.value for r in self.kill_reasons],
            "notes": self.notes,
        }


class ScaleKillBoard:
    def __init__(self, *, scale_threshold: float = 0.7, kill_threshold: float = 0.3) -> None:
        self._entries: dict[str, _Entry] = {}
        self._scale_threshold = scale_threshold
        self._kill_threshold = kill_threshold

    def record(
        self,
        *,
        entity_id: str,
        entity_kind: str,
        label: str,
        score: ScaleScore,
        kill_reasons: list[KillReason] | None = None,
        notes: str = "",
    ) -> _Entry:
        entry = _Entry(
            entity_id=entity_id,
            entity_kind=entity_kind,
            label=label,
            score=score,
            kill_reasons=list(kill_reasons or []),
            notes=notes,
        )
        self._entries[entity_id] = entry
        return entry

    def get(self, entity_id: str) -> _Entry:
        try:
            return self._entries[entity_id]
        except KeyError as exc:
            raise KeyError(f"unknown board entry: {entity_id}") from exc

    def verdict(self, entity_id: str) -> str:
        return self.get(entity_id).verdict(
            scale_threshold=self._scale_threshold, kill_threshold=self._kill_threshold
        )

    def to_scale(self) -> list[_Entry]:
        return [e for e in self._entries.values() if self.verdict(e.entity_id) == "scale"]

    def to_kill(self) -> list[_Entry]:
        return [e for e in self._entries.values() if self.verdict(e.entity_id) == "kill"]

    def to_pause(self) -> list[_Entry]:
        return [e for e in self._entries.values() if self.verdict(e.entity_id) == "pause"]

    def render(self) -> dict[str, Any]:
        scale = [e.to_dict() for e in self.to_scale()]
        kill = [e.to_dict() for e in self.to_kill()]
        pause = [e.to_dict() for e in self.to_pause()]
        return {
            "scale_threshold": self._scale_threshold,
            "kill_threshold": self._kill_threshold,
            "scale": scale,
            "kill": kill,
            "pause": pause,
        }
