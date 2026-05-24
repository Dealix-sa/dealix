"""Partner Scout — keeps the partner pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from dealix.hermes.partners.fit_score import PartnerSignals, score


class PartnerKind(StrEnum):
    REFERRAL = "referral"
    WHITE_LABEL = "white_label"
    IMPLEMENTATION = "implementation"
    TRAINING = "training"
    STRATEGIC = "strategic"
    DATA = "data"
    CHANNEL = "channel"


class PartnerStage(StrEnum):
    SIGNAL = "signal"
    FIT_SCORED = "fit_scored"
    PITCHED = "pitched"
    AGREEMENT_DRAFT = "agreement_draft"
    APPROVED = "approved"
    ONBOARDED = "onboarded"
    ACTIVE = "active"
    DORMANT = "dormant"
    DECLINED = "declined"


@dataclass(slots=True)
class Partner:
    partner_id: str
    name: str
    kind: PartnerKind
    signals: PartnerSignals
    fit_score: float
    stage: PartnerStage
    notes: str = ""
    added_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class PartnerScout:
    def __init__(self) -> None:
        self._partners: dict[str, Partner] = {}

    def register(
        self,
        *,
        name: str,
        kind: PartnerKind,
        signals: PartnerSignals,
        notes: str = "",
    ) -> Partner:
        fit = score(signals)
        partner = Partner(
            partner_id=str(uuid4()),
            name=name,
            kind=kind,
            signals=signals,
            fit_score=fit,
            stage=PartnerStage.FIT_SCORED,
            notes=notes,
        )
        self._partners[partner.partner_id] = partner
        return partner

    def advance(self, partner_id: str, stage: PartnerStage) -> Partner:
        p = self._partners[partner_id]
        p.stage = stage
        return p

    def get(self, partner_id: str) -> Partner | None:
        return self._partners.get(partner_id)

    def all(self) -> list[Partner]:
        return list(self._partners.values())

    def top(self, n: int = 10) -> list[Partner]:
        return sorted(self._partners.values(), key=lambda p: p.fit_score, reverse=True)[:n]


__all__ = ["Partner", "PartnerKind", "PartnerStage", "PartnerScout"]
