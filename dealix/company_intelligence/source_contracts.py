"""Canonical Source contracts for the Company Intelligence provenance registry.

Every entity in the graph traces its provenance to a Source. This contract
provides the single normalized shape for tenant-scoped, policy-governed data
sources that feed the Company Brain, Signal graph, and Opportunity pipeline.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: Source → data_provenance (source and provenance registry).
Required fields: tenant_id, source_type, source_url, retrieved_at, confidence.
Forbidden parallel names: EvidenceSource, ResearchSource.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class SourceType(StrEnum):
    """Categories of data sources the provenance registry can hold."""

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
    INTERNAL_SYSTEM = "internal_system"


class SourcePolicyStatus(StrEnum):
    """Policy gate for source usage. Blocked sources score zero."""

    APPROVED = "approved"
    RESEARCH_ONLY = "research_only"
    REVIEW_REQUIRED = "review_required"
    BLOCKED = "blocked"


class SourceStatus(StrEnum):
    """Lifecycle states for a source in the provenance registry."""

    ACTIVE = "active"
    STALE = "stale"
    RETIRED = "retired"
    BLOCKED = "blocked"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_source_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"source_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical Source contract
# ---------------------------------------------------------------------------


class CanonicalSource(BaseModel):
    """One tenant-scoped, policy-governed data source in the provenance registry.

    Sources are the provenance foundation — every Signal, Company, Contact,
    and CompanyBrain traces back to one or more Sources. A Source never
    authorizes external action by itself.

    Blocked sources always produce a zero confidence floor regardless of
    their raw scores.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    source_id: NonEmptyString
    deduplication_key: NonEmptyString

    # Profile
    name: NonEmptyString
    source_type: SourceType
    source_url: str = ""
    description: str = ""

    # Policy
    policy_status: SourcePolicyStatus = SourcePolicyStatus.REVIEW_REQUIRED
    allowed_use: str = "research_only"

    # Quality scores (0–100)
    authority_score: int = Field(default=50, ge=0, le=100)
    verifiability_score: int = Field(default=50, ge=0, le=100)

    # Freshness
    freshness_days: int = Field(default=90, ge=1)
    retention_days: int = Field(default=365, ge=1)

    # Evidence
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    terms_reviewed_at: datetime | None = None

    # Lifecycle
    status: SourceStatus = SourceStatus.ACTIVE

    # Timestamps
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_source_invariants(self) -> CanonicalSource:
        # retrieved_at must be timezone-aware
        if self.retrieved_at.tzinfo is None:
            raise ValueError("retrieved_at must be timezone-aware")

        # terms_reviewed_at must be timezone-aware if set
        if self.terms_reviewed_at is not None and self.terms_reviewed_at.tzinfo is None:
            raise ValueError("terms_reviewed_at must be timezone-aware")

        # Blocked sources cannot be active
        if (
            self.policy_status == SourcePolicyStatus.BLOCKED
            and self.status == SourceStatus.ACTIVE
        ):
            raise ValueError(
                "blocked sources cannot be in active status"
            )

        # Verify deterministic ID
        expected_id = _stable_source_id({
            "deduplication_key": self.deduplication_key,
            "source_type": self.source_type.value,
            "tenant_id": self.tenant_id,
        })
        if self.source_id != expected_id:
            raise ValueError("source_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def compute_source_score(source: CanonicalSource, *, now: datetime | None = None) -> int:
    """Return a policy-aware composite source score (0–100).

    Blocked sources always return zero. The score weighs authority,
    verifiability, policy, and terms freshness.
    """
    if source.policy_status == SourcePolicyStatus.BLOCKED:
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


# ---------------------------------------------------------------------------
# Staleness
# ---------------------------------------------------------------------------


def is_source_stale(source: CanonicalSource, *, now: datetime | None = None) -> bool:
    """Check whether a source has exceeded its freshness window."""
    check = now or datetime.now(UTC)
    age = check - source.retrieved_at
    return age > timedelta(days=source.freshness_days)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Source state machine
# ---------------------------------------------------------------------------


_SOURCE_TRANSITIONS: dict[SourceStatus, frozenset[SourceStatus]] = {
    SourceStatus.ACTIVE: frozenset({
        SourceStatus.STALE,
        SourceStatus.BLOCKED,
        SourceStatus.RETIRED,
    }),
    SourceStatus.STALE: frozenset({
        SourceStatus.ACTIVE,
        SourceStatus.BLOCKED,
        SourceStatus.RETIRED,
    }),
    # Terminal states
    SourceStatus.RETIRED: frozenset(),
    SourceStatus.BLOCKED: frozenset(),
}


def valid_source_transitions_from(
    status: SourceStatus,
) -> frozenset[SourceStatus]:
    """Return the set of valid next statuses from the given source status."""
    return _SOURCE_TRANSITIONS.get(status, frozenset())


def is_valid_source_transition(
    from_status: SourceStatus,
    to_status: SourceStatus,
) -> bool:
    """Check whether a source status transition is valid."""
    return to_status in valid_source_transitions_from(from_status)


def transition_source(
    source: CanonicalSource,
    *,
    to_status: SourceStatus,
) -> CanonicalSource:
    """Return a new Source with an updated status after validating the transition.

    The returned Source is a new frozen instance — the original is unchanged.
    """
    if not is_valid_source_transition(source.status, to_status):
        raise ValueError(
            f"invalid source transition: "
            f"{source.status.value} → {to_status.value}"
        )
    return source.model_copy(update={"status": to_status})


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_source(
    *,
    tenant_id: str,
    deduplication_key: str,
    name: str,
    source_type: SourceType,
    source_url: str = "",
    description: str = "",
    policy_status: SourcePolicyStatus = SourcePolicyStatus.REVIEW_REQUIRED,
    allowed_use: str = "research_only",
    authority_score: int = 50,
    verifiability_score: int = 50,
    freshness_days: int = 90,
    retention_days: int = 365,
    confidence: float = 0.5,
    terms_reviewed_at: datetime | None = None,
    status: SourceStatus = SourceStatus.ACTIVE,
    retrieved_at: datetime | None = None,
) -> CanonicalSource:
    """Build a deterministic, idempotent, policy-governed source."""

    source_id = _stable_source_id({
        "deduplication_key": deduplication_key.strip(),
        "source_type": source_type.value,
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalSource(
        tenant_id=tenant_id,
        source_id=source_id,
        deduplication_key=deduplication_key,
        name=name,
        source_type=source_type,
        source_url=source_url,
        description=description,
        policy_status=policy_status,
        allowed_use=allowed_use,
        authority_score=authority_score,
        verifiability_score=verifiability_score,
        freshness_days=freshness_days,
        retention_days=retention_days,
        confidence=confidence,
        terms_reviewed_at=terms_reviewed_at,
        status=status,
        retrieved_at=retrieved_at or datetime.now(UTC),
    )
