"""Evidence-governed commercial intelligence domain for Dealix.

This module is deliberately pure.  It scores sources, signals, and commercial
opportunities, but it never scrapes, sends, charges, changes production, or
infers contact consent from public data.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any


class SourceKind(StrEnum):
    OWNED = "owned"
    CRM = "crm"
    EMAIL = "email"
    CLIENT_PROVIDED = "client_provided"
    PARTNER = "partner"
    COMPANY_WEBSITE = "company_website"
    PUBLIC_REGISTRY = "public_registry"
    OPEN_DATA = "open_data"
    NEWS = "news"
    JOBS = "jobs"
    EVENT = "event"
    MANUAL = "manual"


class SourcePolicyStatus(StrEnum):
    APPROVED = "approved"
    RESEARCH_ONLY = "research_only"
    REVIEW_REQUIRED = "review_required"
    BLOCKED = "blocked"


class EvidenceLevel(StrEnum):
    L0_UNKNOWN = "l0_unknown"
    L1_HYPOTHESIS = "l1_hypothesis"
    L2_PUBLIC_SIGNAL = "l2_public_signal"
    L3_FIRST_PARTY = "l3_first_party"
    L4_VERIFIED = "l4_verified"
    L5_MEASURED_OUTCOME = "l5_measured_outcome"


class OpportunityStage(StrEnum):
    RESEARCH = "research"
    QUALIFY = "qualify"
    APPROVAL = "approval"
    CONVERSATION = "conversation"
    PILOT = "pilot"
    PROOF = "proof"
    COMMERCIAL = "commercial"
    WON = "won"
    LOST = "lost"
    PARKED = "parked"


_EVIDENCE_RANK = {
    EvidenceLevel.L0_UNKNOWN: 0,
    EvidenceLevel.L1_HYPOTHESIS: 1,
    EvidenceLevel.L2_PUBLIC_SIGNAL: 2,
    EvidenceLevel.L3_FIRST_PARTY: 3,
    EvidenceLevel.L4_VERIFIED: 4,
    EvidenceLevel.L5_MEASURED_OUTCOME: 5,
}


@dataclass(frozen=True)
class GovernedSource:
    tenant_id: str
    source_id: str
    name: str
    kind: SourceKind
    policy_status: SourcePolicyStatus
    allowed_use: str
    authority_score: int
    verifiability_score: int
    freshness_days: int
    retention_days: int
    terms_reviewed_at: datetime | None = None
    source_url: str | None = None

    def __post_init__(self) -> None:
        for field in ("tenant_id", "source_id", "name", "allowed_use"):
            if not getattr(self, field).strip():
                raise ValueError(f"{field} must not be empty")
        for field in ("authority_score", "verifiability_score"):
            if not 0 <= getattr(self, field) <= 100:
                raise ValueError(f"{field} must be between 0 and 100")
        if self.freshness_days < 1 or self.retention_days < 1:
            raise ValueError("freshness_days and retention_days must be positive")


@dataclass(frozen=True)
class CommercialSignal:
    tenant_id: str
    signal_id: str
    account_id: str
    source_id: str
    signal_type: str
    claim: str
    evidence_ref: str
    observed_at: datetime
    confidence: int
    evidence_level: EvidenceLevel
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        for field in (
            "tenant_id",
            "signal_id",
            "account_id",
            "source_id",
            "signal_type",
            "claim",
            "evidence_ref",
        ):
            if not getattr(self, field).strip():
                raise ValueError(f"{field} must not be empty")
        if not 0 <= self.confidence <= 100:
            raise ValueError("confidence must be between 0 and 100")
        if self.observed_at.tzinfo is None:
            raise ValueError("observed_at must be timezone-aware")

    def is_stale(self, *, now: datetime | None = None) -> bool:
        check = now or datetime.now(UTC)
        return bool(self.expires_at and self.expires_at <= check)


@dataclass(frozen=True)
class OpportunityInputs:
    strategic_fit: int
    problem_evidence: int
    urgency: int
    relationship_strength: int
    commercial_value: int
    evidence_level: EvidenceLevel
    source_score: int
    signal_count: int

    def __post_init__(self) -> None:
        for field in (
            "strategic_fit",
            "problem_evidence",
            "urgency",
            "relationship_strength",
            "commercial_value",
            "source_score",
        ):
            if not 0 <= getattr(self, field) <= 100:
                raise ValueError(f"{field} must be between 0 and 100")
        if self.signal_count < 0:
            raise ValueError("signal_count must not be negative")


@dataclass(frozen=True)
class OpportunityScore:
    score: int
    uncapped_score: int
    evidence_cap: int
    confidence_band: str
    blockers: tuple[str, ...]
    score_components: dict[str, int]
    external_action_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def score_source(source: GovernedSource, *, now: datetime | None = None) -> int:
    """Return a policy-aware source score; blocked sources always score zero."""
    if source.policy_status is SourcePolicyStatus.BLOCKED:
        return 0
    policy_factor = {
        SourcePolicyStatus.APPROVED: 100,
        SourcePolicyStatus.RESEARCH_ONLY: 70,
        SourcePolicyStatus.REVIEW_REQUIRED: 45,
        SourcePolicyStatus.BLOCKED: 0,
    }[source.policy_status]
    terms_freshness = 100
    if source.terms_reviewed_at is None:
        terms_freshness = 40
    else:
        check = now or datetime.now(UTC)
        if source.terms_reviewed_at.tzinfo is None:
            raise ValueError("terms_reviewed_at must be timezone-aware")
        age = check - source.terms_reviewed_at
        if age > timedelta(days=365):
            terms_freshness = 60
    weighted = (
        source.authority_score * 0.35
        + source.verifiability_score * 0.30
        + policy_factor * 0.25
        + terms_freshness * 0.10
    )
    return round(weighted)


def score_opportunity(inputs: OpportunityInputs) -> OpportunityScore:
    """Score an opportunity while capping confidence to the available evidence."""
    components = {
        "strategic_fit": round(inputs.strategic_fit * 0.25),
        "problem_evidence": round(inputs.problem_evidence * 0.25),
        "urgency": round(inputs.urgency * 0.15),
        "relationship_strength": round(inputs.relationship_strength * 0.15),
        "commercial_value": round(inputs.commercial_value * 0.10),
        "source_quality": round(inputs.source_score * 0.10),
    }
    uncapped = min(sum(components.values()), 100)
    caps = {
        EvidenceLevel.L0_UNKNOWN: 20,
        EvidenceLevel.L1_HYPOTHESIS: 40,
        EvidenceLevel.L2_PUBLIC_SIGNAL: 60,
        EvidenceLevel.L3_FIRST_PARTY: 75,
        EvidenceLevel.L4_VERIFIED: 90,
        EvidenceLevel.L5_MEASURED_OUTCOME: 100,
    }
    cap = caps[inputs.evidence_level]
    blockers: list[str] = []
    if inputs.signal_count == 0:
        blockers.append("no_evidence_signal")
        cap = min(cap, 20)
    if inputs.source_score < 50:
        blockers.append("source_quality_below_50")
        cap = min(cap, 45)
    if _EVIDENCE_RANK[inputs.evidence_level] < _EVIDENCE_RANK[EvidenceLevel.L3_FIRST_PARTY]:
        blockers.append("client_validation_required")
    score = min(uncapped, cap)
    confidence_band = "high" if score >= 75 else "medium" if score >= 50 else "low"
    return OpportunityScore(
        score=score,
        uncapped_score=uncapped,
        evidence_cap=cap,
        confidence_band=confidence_band,
        blockers=tuple(blockers),
        score_components=components,
    )


def highest_evidence_level(signals: list[CommercialSignal]) -> EvidenceLevel:
    if not signals:
        return EvidenceLevel.L0_UNKNOWN
    return max(signals, key=lambda signal: _EVIDENCE_RANK[signal.evidence_level]).evidence_level


def source_scorecard(
    source: GovernedSource,
    signals: list[CommercialSignal],
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    scoped = [
        signal
        for signal in signals
        if signal.tenant_id == source.tenant_id and signal.source_id == source.source_id
    ]
    stale = sum(signal.is_stale(now=now) for signal in scoped)
    avg_confidence = round(sum(signal.confidence for signal in scoped) / len(scoped)) if scoped else 0
    return {
        "source_id": source.source_id,
        "name": source.name,
        "policy_status": source.policy_status.value,
        "source_score": score_source(source, now=now),
        "signals": len(scoped),
        "stale_signals": stale,
        "average_signal_confidence": avg_confidence,
        "external_action_allowed": False,
    }


__all__ = [
    "CommercialSignal",
    "EvidenceLevel",
    "GovernedSource",
    "OpportunityInputs",
    "OpportunityScore",
    "OpportunityStage",
    "SourceKind",
    "SourcePolicyStatus",
    "highest_evidence_level",
    "score_opportunity",
    "score_source",
    "source_scorecard",
]
