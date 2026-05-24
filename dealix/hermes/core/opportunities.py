"""خادم Hermes — opportunity mapping.

A Signal that survives classification is mapped to an Opportunity. The
opportunity carries the business framing (type, expected value, effort,
urgency, fit) the rest of the kernel needs to score and decide.

Mapping is heuristic and deterministic so the kernel stays offline-safe;
LLM-backed enrichment is a strictly downstream concern.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from dealix.hermes.core.schemas import (
    Money,
    Score1to5,
    WorkspaceScope,
    utcnow,
)
from dealix.hermes.core.signals import (
    Signal,
    SignalCategory,
    SignalClassification,
)


class OpportunityType(StrEnum):
    """Spec §26 — the five classes of opportunity the kernel reasons about."""

    REVENUE = "revenue"
    PARTNER = "partner"
    PRODUCT = "product"
    KNOWLEDGE = "knowledge"
    RISK_AVOIDANCE = "risk_avoidance"


def _new_opp_id() -> str:
    return f"opp_{uuid4().hex}"


# Heuristic defaults for expected_value when only the type is known.
_DEFAULT_VALUES_SAR: dict[OpportunityType, Decimal | None] = {
    OpportunityType.REVENUE: Decimal("2500"),
    OpportunityType.PARTNER: None,  # partner deals priced case-by-case
    OpportunityType.PRODUCT: Decimal("5000"),
    OpportunityType.KNOWLEDGE: Decimal("500"),
    OpportunityType.RISK_AVOIDANCE: Decimal("0"),
}


class Opportunity(BaseModel):
    """An actionable business opportunity derived from a Signal."""

    model_config = ConfigDict(extra="forbid")

    opp_id: str = Field(default_factory=_new_opp_id)
    signal_id: str = Field(..., min_length=1)
    opp_type: OpportunityType
    title: str = Field(..., min_length=1, max_length=200)
    narrative: str = Field(..., min_length=1, max_length=4000)

    expected_value: Money | None = None
    effort_score: Score1to5 = Field(default=3)
    urgency: Score1to5 = Field(default=3)
    fit_score: Score1to5 = Field(default=3)

    # Classification echoes for fast filtering downstream
    monetizable: bool = False
    sensitive: bool = False
    repeatable: bool = False
    needs_sami: bool = False

    workspace: WorkspaceScope = WorkspaceScope.INTERNAL
    created_at: datetime = Field(default_factory=utcnow)

    @model_validator(mode="after")
    def _coerce_revenue_value(self) -> Opportunity:
        """REVENUE opportunities must carry a Money value (default if missing)."""
        if self.opp_type == OpportunityType.REVENUE and self.expected_value is None:
            self.expected_value = Money.sar(_DEFAULT_VALUES_SAR[OpportunityType.REVENUE])
        return self


class ScoredOpportunity(BaseModel):
    """An Opportunity decorated with its aggregate weighted score."""

    model_config = ConfigDict(extra="forbid")

    opportunity: Opportunity
    score: Annotated[float, Field(ge=0.0, le=5.0)]
    rationale: str = Field(..., min_length=1, max_length=2000)
    components: dict[str, float] = Field(default_factory=dict)


# ─────────────────────────────────────────────────────────────
# Mapper — Signal + Classification → Opportunity
# ─────────────────────────────────────────────────────────────

_CATEGORY_TO_TYPE: dict[SignalCategory, OpportunityType] = {
    SignalCategory.MONEY: OpportunityType.REVENUE,
    SignalCategory.PARTNER: OpportunityType.PARTNER,
    SignalCategory.PRODUCT: OpportunityType.PRODUCT,
    SignalCategory.KNOWLEDGE: OpportunityType.KNOWLEDGE,
    SignalCategory.RISK: OpportunityType.RISK_AVOIDANCE,
    SignalCategory.NOISE: OpportunityType.KNOWLEDGE,
}


def _summarise(text: str, limit: int = 160) -> str:
    snippet = " ".join(text.split())
    if len(snippet) <= limit:
        return snippet
    return snippet[: limit - 1].rstrip() + "…"


class OpportunityMapper:
    """Map a (Signal, Classification) pair to an Opportunity."""

    def map(
        self,
        signal: Signal,
        classification: SignalClassification,
    ) -> Opportunity:
        opp_type = _CATEGORY_TO_TYPE[classification.category]
        default_amount = _DEFAULT_VALUES_SAR[opp_type]
        expected_value: Money | None
        if default_amount is None or default_amount == Decimal("0"):
            expected_value = None
        else:
            expected_value = Money.sar(default_amount)

        # Effort heuristic — partner/product cost more energy than knowledge.
        effort_score = {
            OpportunityType.REVENUE: 3,
            OpportunityType.PARTNER: 4,
            OpportunityType.PRODUCT: 4,
            OpportunityType.KNOWLEDGE: 2,
            OpportunityType.RISK_AVOIDANCE: 3,
        }[opp_type]

        # Urgency heuristic — risk/SAMI-routed signals are higher urgency.
        urgency = 5 if classification.needs_sami or opp_type == OpportunityType.RISK_AVOIDANCE else 3
        if classification.repeatable:
            urgency = min(5, urgency + 1)

        # Fit heuristic — monetizable + repeatable is the sweet spot.
        fit_score = 3
        if classification.monetizable:
            fit_score += 1
        if classification.repeatable:
            fit_score += 1
        fit_score = max(1, min(5, fit_score))

        title = self._title_for(opp_type, signal)
        narrative = _summarise(signal.raw_text, limit=400)

        return Opportunity(
            signal_id=signal.signal_id,
            opp_type=opp_type,
            title=title,
            narrative=narrative,
            expected_value=expected_value,
            effort_score=effort_score,
            urgency=urgency,
            fit_score=fit_score,
            monetizable=classification.monetizable,
            sensitive=classification.sensitive,
            repeatable=classification.repeatable,
            needs_sami=classification.needs_sami,
            workspace=signal.workspace,
        )

    @staticmethod
    def _title_for(opp_type: OpportunityType, signal: Signal) -> str:
        prefix = {
            OpportunityType.REVENUE: "Revenue lead",
            OpportunityType.PARTNER: "Partner overture",
            OpportunityType.PRODUCT: "Product signal",
            OpportunityType.KNOWLEDGE: "Knowledge ask",
            OpportunityType.RISK_AVOIDANCE: "Risk signal",
        }[opp_type]
        return f"{prefix} via {signal.source.value}"

    def map_many(
        self,
        signal: Signal,
        classification: SignalClassification,
        extra: dict[str, Any] | None = None,
    ) -> Opportunity:
        opp = self.map(signal, classification)
        if extra:
            # Re-validate by round-tripping through pydantic so extras are checked.
            data = opp.model_dump() | extra
            opp = Opportunity.model_validate(data)
        return opp


__all__ = [
    "Opportunity",
    "OpportunityMapper",
    "OpportunityType",
    "ScoredOpportunity",
]
