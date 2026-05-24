"""خادم الثقة — EvidencePack (spec §40).

An EvidencePack is the structured story that accompanies every
sovereign-grade decision. It records decision text, context, signals,
score, risks, alternatives, recommendation, approvals, next steps.

The store is in-memory for Phase 0–1; the durable Postgres-backed store
arrives in Phase 2.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dealix.hermes.core.decisions import Decision
from dealix.hermes.core.opportunities import ScoredOpportunity
from dealix.hermes.core.schemas import utcnow


def _new_pack_id() -> str:
    return f"epk_{uuid4().hex}"


class EvidencePack(BaseModel):
    """Spec §40 shape — exactly the fields the trust plane requires."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str = Field(default_factory=_new_pack_id)
    decision: str = Field(..., min_length=1, max_length=2000)
    context: str = Field(..., min_length=1, max_length=4000)
    signals: list[str] = Field(default_factory=list, max_length=50)
    opportunity_score: float = Field(..., ge=0.0, le=5.0)
    risks: list[str] = Field(default_factory=list, max_length=50)
    alternatives: list[str] = Field(default_factory=list, max_length=20)
    recommendation: str = Field(..., min_length=1, max_length=2000)
    approvals: list[dict[str, Any]] = Field(default_factory=list, max_length=20)
    next_steps: list[str] = Field(default_factory=list, max_length=20)
    created_at: datetime = Field(default_factory=utcnow)

    @field_validator("alternatives")
    @classmethod
    def _at_least_one_alternative(cls, value: list[str]) -> list[str]:
        cleaned = [v.strip() for v in value if v and v.strip()]
        if not cleaned:
            raise ValueError("EvidencePack.alternatives must contain at least one entry")
        return cleaned


# ─────────────────────────────────────────────────────────────
# Builder
# ─────────────────────────────────────────────────────────────


class EvidenceBuilder:
    """Builds EvidencePacks from kernel artifacts."""

    def build_from_decision(
        self,
        decision: Decision,
        scored_opportunity: ScoredOpportunity,
        risk_register: list[str] | None = None,
        approvals: list[dict[str, Any]] | None = None,
        next_steps: list[str] | None = None,
        signals: list[str] | None = None,
    ) -> EvidencePack:
        opp = scored_opportunity.opportunity
        return EvidencePack(
            decision=decision.summary,
            context=f"{opp.opp_type.value} opportunity: {opp.title}\n\n{opp.narrative}",
            signals=list(signals or [opp.signal_id]),
            opportunity_score=scored_opportunity.score,
            risks=list(risk_register or []),
            alternatives=[o for o in decision.options if o != decision.chosen_option] or list(decision.options),
            recommendation=decision.chosen_option,
            approvals=list(approvals or []),
            next_steps=list(next_steps or [decision.rationale]),
        )


# ─────────────────────────────────────────────────────────────
# Store
# ─────────────────────────────────────────────────────────────


class EvidenceStore:
    """In-memory EvidencePack store."""

    def __init__(self) -> None:
        self._packs: dict[str, EvidencePack] = {}
        self._by_entity: dict[str, list[str]] = {}

    def save(self, pack: EvidencePack, entity_ref: str | None = None) -> str:
        if pack.pack_id in self._packs:
            raise ValueError(f"duplicate pack_id: {pack.pack_id}")
        self._packs[pack.pack_id] = pack
        if entity_ref:
            self._by_entity.setdefault(entity_ref, []).append(pack.pack_id)
        return pack.pack_id

    def get(self, pack_id: str) -> EvidencePack:
        try:
            return self._packs[pack_id]
        except KeyError as exc:
            raise KeyError(f"unknown evidence pack: {pack_id}") from exc

    def list_for_entity(self, entity_ref: str) -> list[EvidencePack]:
        ids = self._by_entity.get(entity_ref, [])
        return [self._packs[i] for i in ids if i in self._packs]

    def all(self) -> list[EvidencePack]:
        return list(self._packs.values())


__all__ = [
    "EvidenceBuilder",
    "EvidencePack",
    "EvidenceStore",
]
