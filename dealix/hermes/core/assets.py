"""خادم Hermes — asset capture.

When an outcome shows reusable value the AssetBuilder turns it into an
Asset record (template, playbook, offer, etc.). Assets are the
compounding layer of the kernel — every reusable artifact lives here.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.schemas import Score1to5, utcnow


class AssetType(StrEnum):
    TEMPLATE = "template"
    PLAYBOOK = "playbook"
    DATA_PACK = "data_pack"
    OFFER = "offer"
    PROCESS = "process"
    MODEL = "model"
    REPORT = "report"
    RELATIONSHIP = "relationship"


def _new_asset_id() -> str:
    return f"ast_{uuid4().hex}"


class Asset(BaseModel):
    """A reusable artifact promoted from an outcome."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(default_factory=_new_asset_id)
    asset_type: AssetType
    name: str = Field(..., min_length=1, max_length=160)
    description: str = Field(..., min_length=1, max_length=2000)
    source_outcome_id: str = Field(..., min_length=1)
    reusability_score: Score1to5 = Field(default=3)
    monetization_potential: Score1to5 = Field(default=3)
    tags: list[str] = Field(default_factory=list, max_length=24)
    created_at: datetime = Field(default_factory=utcnow)


# ─────────────────────────────────────────────────────────────
# AssetBuilder
# ─────────────────────────────────────────────────────────────


_KIND_TO_TYPE: dict[OutcomeKind, AssetType] = {
    OutcomeKind.MONEY: AssetType.OFFER,
    OutcomeKind.DATA: AssetType.DATA_PACK,
    OutcomeKind.ASSET: AssetType.TEMPLATE,
    OutcomeKind.PARTNER: AssetType.RELATIONSHIP,
    OutcomeKind.ACCESS: AssetType.PROCESS,
    OutcomeKind.TRUST: AssetType.REPORT,
    OutcomeKind.LEARNING: AssetType.PLAYBOOK,
}


class AssetBuilder:
    """Promote eligible outcomes into Asset records."""

    @staticmethod
    def _is_eligible(outcome: Outcome, reusability_score: int) -> bool:
        if outcome.kind in {OutcomeKind.LEARNING, OutcomeKind.DATA, OutcomeKind.ASSET}:
            return True
        return reusability_score >= 3

    def consider(
        self,
        outcome: Outcome,
        *,
        reusability_score: int = 3,
        monetization_potential: int = 3,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
    ) -> Asset | None:
        if not self._is_eligible(outcome, reusability_score):
            return None
        asset_type = _KIND_TO_TYPE.get(outcome.kind, AssetType.PLAYBOOK)
        return Asset(
            asset_type=asset_type,
            name=name or f"{asset_type.value.title()} from {outcome.outcome_id}",
            description=description or outcome.summary,
            source_outcome_id=outcome.outcome_id,
            reusability_score=reusability_score,
            monetization_potential=monetization_potential,
            tags=list(tags or []),
        )

    def consider_many(self, outcomes: list[Outcome], **defaults: Any) -> list[Asset]:
        assets: list[Asset] = []
        for o in outcomes:
            asset = self.consider(o, **defaults)
            if asset is not None:
                assets.append(asset)
        return assets


__all__ = [
    "Asset",
    "AssetBuilder",
    "AssetType",
]
