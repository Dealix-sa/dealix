"""خادم Hermes — decision memos.

A Decision is the human-readable artifact that bridges a scored
opportunity and a planned execution. It enumerates options, picks one,
records the rationale, and stores evidence references.

State machine:
    DRAFT → PENDING_APPROVAL → APPROVED|REJECTED → EXECUTED|ABANDONED
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from dealix.hermes.core.opportunities import (
    Opportunity,
    OpportunityType,
    ScoredOpportunity,
)
from dealix.hermes.core.schemas import utcnow


class DecisionStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    ABANDONED = "abandoned"


_VALID_TRANSITIONS: dict[DecisionStatus, set[DecisionStatus]] = {
    DecisionStatus.DRAFT: {
        DecisionStatus.PENDING_APPROVAL,
        DecisionStatus.APPROVED,
        DecisionStatus.ABANDONED,
    },
    DecisionStatus.PENDING_APPROVAL: {
        DecisionStatus.APPROVED,
        DecisionStatus.REJECTED,
        DecisionStatus.ABANDONED,
    },
    DecisionStatus.APPROVED: {DecisionStatus.EXECUTED, DecisionStatus.ABANDONED},
    DecisionStatus.REJECTED: set(),
    DecisionStatus.EXECUTED: set(),
    DecisionStatus.ABANDONED: set(),
}


def _new_decision_id() -> str:
    return f"hdec_{uuid4().hex}"


class Decision(BaseModel):
    """A drafted decision memo ready for the trust + execution lanes."""

    model_config = ConfigDict(extra="forbid")

    decision_id: str = Field(default_factory=_new_decision_id)
    opportunity_id: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1, max_length=600)
    options: list[str] = Field(..., min_length=2, max_length=10)
    chosen_option: str = Field(..., min_length=1, max_length=300)
    rationale: str = Field(..., min_length=1, max_length=4000)
    evidence_refs: list[str] = Field(default_factory=list)

    sovereignty_level: str = Field(default="s0_autonomous", min_length=1, max_length=64)
    status: DecisionStatus = DecisionStatus.DRAFT
    decided_by: str | None = None
    decided_at: datetime | None = None

    created_at: datetime = Field(default_factory=utcnow)

    @field_validator("options")
    @classmethod
    def _options_non_empty(cls, value: list[str]) -> list[str]:
        cleaned = [o.strip() for o in value if o and o.strip()]
        if len(cleaned) < 2:
            raise ValueError("Decision.options must contain at least two distinct options")
        if len(set(cleaned)) != len(cleaned):
            raise ValueError("Decision.options must be unique")
        return cleaned

    @model_validator(mode="after")
    def _chosen_in_options(self) -> Decision:
        if self.chosen_option not in self.options:
            raise ValueError("chosen_option must appear in options[]")
        return self

    def can_transition_to(self, target: DecisionStatus) -> bool:
        return target in _VALID_TRANSITIONS[self.status]

    def transition(self, target: DecisionStatus, by: str | None = None) -> Decision:
        if not self.can_transition_to(target):
            raise ValueError(
                f"illegal decision transition {self.status.value} → {target.value}"
            )
        update: dict[str, Any] = {"status": target}
        if target in (
            DecisionStatus.APPROVED,
            DecisionStatus.REJECTED,
            DecisionStatus.EXECUTED,
            DecisionStatus.ABANDONED,
        ):
            update["decided_at"] = utcnow()
            if by is not None:
                update["decided_by"] = by
        return self.model_copy(update=update)


# ─────────────────────────────────────────────────────────────
# Memo builder
# ─────────────────────────────────────────────────────────────


_DEFAULT_OPTIONS: dict[OpportunityType, list[str]] = {
    OpportunityType.REVENUE: [
        "Send a tailored proposal within 24h",
        "Schedule a discovery call this week",
        "Park lead for monthly nurture",
    ],
    OpportunityType.PARTNER: [
        "Draft a partner pitch deck and reply",
        "Request a vetting call before responding",
        "Decline politely and log rationale",
    ],
    OpportunityType.PRODUCT: [
        "Open product backlog item with evidence",
        "Build a thin landing-page test",
        "Defer to next quarterly planning",
    ],
    OpportunityType.KNOWLEDGE: [
        "Capture answer in playbook + reply",
        "Share existing doc + close",
        "Ignore — out of scope",
    ],
    OpportunityType.RISK_AVOIDANCE: [
        "Open incident & inform owner",
        "Add to risk register and monitor",
        "Mitigate immediately with rollback",
    ],
}


class DecisionMemoBuilder:
    """Produce a draft `Decision` from a `ScoredOpportunity`.

    Always produces at least two options and a chosen recommendation
    based on the score band and opportunity type.
    """

    def build(
        self,
        scored: ScoredOpportunity,
        evidence_refs: list[str] | None = None,
        sovereignty_level: str = "s0_autonomous",
    ) -> Decision:
        opp = scored.opportunity
        options = list(_DEFAULT_OPTIONS[opp.opp_type])
        chosen = self._pick(scored, options)
        summary = self._summary(opp, scored)
        rationale = self._rationale(scored, chosen)
        return Decision(
            opportunity_id=opp.opp_id,
            summary=summary,
            options=options,
            chosen_option=chosen,
            rationale=rationale,
            evidence_refs=list(evidence_refs or []),
            sovereignty_level=sovereignty_level,
        )

    @staticmethod
    def _pick(scored: ScoredOpportunity, options: list[str]) -> str:
        # High score → first/most-active option; low score → defer.
        if scored.score >= 3.5:
            return options[0]
        if scored.score >= 2.0:
            return options[1]
        return options[-1]

    @staticmethod
    def _summary(opp: Opportunity, scored: ScoredOpportunity) -> str:
        value = f" ({opp.expected_value})" if opp.expected_value else ""
        return (
            f"{opp.opp_type.value.title()} opportunity{value} "
            f"— score {scored.score:.2f}: {opp.title}"
        )

    @staticmethod
    def _rationale(scored: ScoredOpportunity, chosen: str) -> str:
        comps = scored.components or {}
        parts = [
            f"score={scored.score:.2f}",
            *(f"{k}={v:.2f}" for k, v in comps.items()),
        ]
        return f"Chose '{chosen}' because {', '.join(parts)}."


__all__ = [
    "Decision",
    "DecisionMemoBuilder",
    "DecisionStatus",
]
