"""
Section 73 — Venture Value Loop.

For each vertical:
    Sector signal → Pain map → Offer → First 50 targets → Pilot →
    Outcomes → Assets → Scale/Kill.

Venture Rule: no vertical product is built before *real replies*, a clear
pain, a defined offer, a target list, and outcomes — in that order.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class VentureStage(StrEnum):
    SECTOR_SIGNAL = "sector_signal"
    PAIN_MAP = "pain_map"
    OFFER = "offer"
    FIRST_50_TARGETS = "first_50_targets"
    PILOT = "pilot"
    OUTCOMES = "outcomes"
    ASSETS = "assets"
    SCALE = "scale"
    KILL = "kill"


@dataclass
class Venture:
    venture_id: str
    sector: str
    workspace_id: str
    stage: VentureStage = VentureStage.SECTOR_SIGNAL
    pain_map: list[str] = field(default_factory=list)
    offer_id: str | None = None
    targets: list[str] = field(default_factory=list)
    replies: list[str] = field(default_factory=list)
    outcomes: list[str] = field(default_factory=list)
    assets: list[str] = field(default_factory=list)
    notes: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "venture_id": self.venture_id,
            "sector": self.sector,
            "workspace_id": self.workspace_id,
            "stage": self.stage.value,
            "pain_map": list(self.pain_map),
            "offer_id": self.offer_id,
            "targets": list(self.targets),
            "replies": list(self.replies),
            "outcomes": list(self.outcomes),
            "assets": list(self.assets),
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
        }


_STAGE_ORDER: tuple[VentureStage, ...] = (
    VentureStage.SECTOR_SIGNAL,
    VentureStage.PAIN_MAP,
    VentureStage.OFFER,
    VentureStage.FIRST_50_TARGETS,
    VentureStage.PILOT,
    VentureStage.OUTCOMES,
    VentureStage.ASSETS,
    VentureStage.SCALE,
)


class VentureValueLoop:
    def __init__(self) -> None:
        self._ventures: dict[str, Venture] = {}

    def signal(self, *, sector: str, workspace_id: str) -> Venture:
        venture = Venture(
            venture_id=f"vtr_{uuid.uuid4().hex[:12]}",
            sector=sector,
            workspace_id=workspace_id,
        )
        self._ventures[venture.venture_id] = venture
        return venture

    def set_pain_map(self, venture_id: str, *, pains: Iterable[str]) -> Venture:
        venture = self.get(venture_id)
        venture.pain_map = list(pains)
        venture.stage = VentureStage.PAIN_MAP
        return venture

    def attach_offer(self, venture_id: str, *, offer_id: str) -> Venture:
        venture = self.get(venture_id)
        venture.offer_id = offer_id
        venture.stage = VentureStage.OFFER
        return venture

    def add_targets(self, venture_id: str, *, targets: Iterable[str]) -> Venture:
        venture = self.get(venture_id)
        venture.targets.extend(targets)
        if len(venture.targets) >= 50:
            venture.stage = VentureStage.FIRST_50_TARGETS
        return venture

    def record_reply(self, venture_id: str, *, reply: str) -> Venture:
        venture = self.get(venture_id)
        venture.replies.append(reply)
        return venture

    def record_outcome(self, venture_id: str, *, outcome: str) -> Venture:
        venture = self.get(venture_id)
        venture.outcomes.append(outcome)
        venture.stage = VentureStage.OUTCOMES
        return venture

    def record_asset(self, venture_id: str, *, asset_id: str) -> Venture:
        venture = self.get(venture_id)
        venture.assets.append(asset_id)
        venture.stage = VentureStage.ASSETS
        return venture

    def can_productise(self, venture_id: str) -> tuple[bool, list[str]]:
        venture = self.get(venture_id)
        missing: list[str] = []
        if not venture.replies:
            missing.append("real replies")
        if not venture.pain_map:
            missing.append("pain map")
        if not venture.offer_id:
            missing.append("offer")
        if len(venture.targets) < 50:
            missing.append("first 50 targets")
        if not venture.outcomes:
            missing.append("outcomes")
        return (not missing, missing)

    def scale(self, venture_id: str) -> Venture:
        ready, missing = self.can_productise(venture_id)
        if not ready:
            raise ValueError(
                f"venture {venture_id} cannot scale — missing: {', '.join(missing)}"
            )
        venture = self.get(venture_id)
        venture.stage = VentureStage.SCALE
        return venture

    def kill(self, venture_id: str, *, reason: str) -> Venture:
        venture = self.get(venture_id)
        venture.stage = VentureStage.KILL
        venture.notes = (venture.notes + f" | killed: {reason}").strip(" |")
        return venture

    def get(self, venture_id: str) -> Venture:
        try:
            return self._ventures[venture_id]
        except KeyError as exc:
            raise KeyError(f"unknown venture: {venture_id}") from exc

    def all(self) -> list[Venture]:
        return list(self._ventures.values())
