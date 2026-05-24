"""خادم الشركاء — PartnerOnboarding state machine.

Stages:

    PROSPECT → QUALIFIED → MOU_DRAFTED → PILOT → LIVE → PAUSED

`advance(...)` enforces valid transitions and demands a `evidence_ref`
for any move into MOU_DRAFTED / LIVE / PAUSED — these stages have
sovereignty implications (Sami sign-off needed downstream).
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import utcnow


class PartnerStage(StrEnum):
    PROSPECT = "prospect"
    QUALIFIED = "qualified"
    MOU_DRAFTED = "mou_drafted"
    PILOT = "pilot"
    LIVE = "live"
    PAUSED = "paused"


_VALID_TRANSITIONS: dict[PartnerStage, set[PartnerStage]] = {
    PartnerStage.PROSPECT: {PartnerStage.QUALIFIED, PartnerStage.PAUSED},
    PartnerStage.QUALIFIED: {PartnerStage.MOU_DRAFTED, PartnerStage.PAUSED},
    PartnerStage.MOU_DRAFTED: {PartnerStage.PILOT, PartnerStage.PAUSED},
    PartnerStage.PILOT: {PartnerStage.LIVE, PartnerStage.PAUSED},
    PartnerStage.LIVE: {PartnerStage.PAUSED},
    PartnerStage.PAUSED: {PartnerStage.QUALIFIED, PartnerStage.PILOT, PartnerStage.LIVE},
}

# Stages that demand an evidence reference before we accept the transition.
_REQUIRES_EVIDENCE: frozenset[PartnerStage] = frozenset(
    {PartnerStage.MOU_DRAFTED, PartnerStage.LIVE, PartnerStage.PAUSED}
)


def _new_partner_id() -> str:
    return f"prt_{uuid4().hex[:16]}"


class PartnerRecord(BaseModel):
    """A partner's tracked lifecycle record."""

    model_config = ConfigDict(extra="forbid")

    partner_id: str = Field(default_factory=_new_partner_id)
    name: str = Field(..., min_length=1, max_length=200)
    stage: PartnerStage = PartnerStage.PROSPECT
    history: list[dict[str, str]] = Field(default_factory=list, max_length=50)
    evidence_refs: list[str] = Field(default_factory=list, max_length=50)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


# ─────────────────────────────────────────────────────────────
# State machine
# ─────────────────────────────────────────────────────────────


class PartnerOnboardingError(ValueError):
    """Raised on invalid transitions or missing evidence."""


class PartnerOnboarding:
    """Track partner lifecycle + enforce valid transitions."""

    def __init__(self) -> None:
        self._partners: dict[str, PartnerRecord] = {}

    def register(self, name: str) -> PartnerRecord:
        record = PartnerRecord(name=name)
        self._partners[record.partner_id] = record
        return record

    def get(self, partner_id: str) -> PartnerRecord:
        try:
            return self._partners[partner_id]
        except KeyError as exc:
            raise KeyError(f"unknown partner: {partner_id}") from exc

    def all(self) -> list[PartnerRecord]:
        return list(self._partners.values())

    def advance(
        self,
        partner_id: str,
        to_state: PartnerStage,
        evidence_ref: str | None = None,
    ) -> PartnerRecord:
        record = self.get(partner_id)
        if to_state not in _VALID_TRANSITIONS[record.stage]:
            raise PartnerOnboardingError(
                f"illegal transition {record.stage.value} → {to_state.value}"
            )
        if to_state in _REQUIRES_EVIDENCE and not evidence_ref:
            raise PartnerOnboardingError(
                f"transition to {to_state.value} requires evidence_ref"
            )
        from_state = record.stage
        record.stage = to_state
        record.updated_at = utcnow()
        if evidence_ref:
            record.evidence_refs.append(evidence_ref)
        record.history.append(
            {
                "from": from_state.value,
                "to": to_state.value,
                "at": record.updated_at.isoformat(),
                "evidence_ref": evidence_ref or "",
            }
        )
        self._partners[partner_id] = record
        return record


__all__ = [
    "PartnerOnboarding",
    "PartnerOnboardingError",
    "PartnerRecord",
    "PartnerStage",
]
