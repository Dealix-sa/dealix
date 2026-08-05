"""Canonical Signal contracts for the Company Intelligence graph.

Every Company Loop begins with Signals. This contract provides the single
normalized shape for tenant-scoped, evidence-graded, deduplicated signals
that feed the Opportunity Graph.

The models are persistence-neutral: no database, network, or LLM calls. They
connect Source → Signal → Opportunity and provide the input layer for the
entire execution spine.

Entity ownership: Signal → opportunity_graph (company/contact/signal graph).
Required fields: tenant_id, company_id, source_id, signal_type, confidence.
Forbidden parallel names: IntentSignal, MarketSignalRecord.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
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


class SignalType(StrEnum):
    """Categories of signals the graph can hold.

    Maps the eleven sovereign signal types from the operating manual plus
    domain-specific sub-categories used by the lead_to_cash loop.
    """

    CUSTOMER = "customer"
    PARTNER = "partner"
    PRODUCT = "product"
    MARKET = "market"
    RISK = "risk"
    MONEY = "money"
    TRAINING = "training"
    VENTURE = "venture"
    API = "api"
    TRUST = "trust"
    PERSONAL = "personal"
    REGULATORY = "regulatory"
    COMPETITIVE = "competitive"
    ECONOMIC = "economic"
    TECH_ADOPTION = "tech_adoption"


class SignalSensitivity(StrEnum):
    """Data classification for the signal payload."""

    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class SignalStatus(StrEnum):
    """Lifecycle states for a signal."""

    RAW = "raw"
    VALIDATED = "validated"
    LINKED = "linked"
    EXPIRED = "expired"
    RETRACTED = "retracted"


class ConsentStatus(StrEnum):
    """Consent posture for data linked to this signal.

    Fail-closed: unknown consent blocks external action.
    """

    UNKNOWN = "unknown"
    OPT_IN = "opt_in"
    EXISTING_RELATIONSHIP = "existing_relationship"
    PUBLIC_SOURCE = "public_source"
    WITHDRAWN = "withdrawn"


# Valid state transitions — fail-closed on anything not listed.
_VALID_TRANSITIONS: dict[SignalStatus, frozenset[SignalStatus]] = {
    SignalStatus.RAW: frozenset({
        SignalStatus.VALIDATED,
        SignalStatus.EXPIRED,
        SignalStatus.RETRACTED,
    }),
    SignalStatus.VALIDATED: frozenset({
        SignalStatus.LINKED,
        SignalStatus.EXPIRED,
        SignalStatus.RETRACTED,
    }),
    SignalStatus.LINKED: frozenset({
        SignalStatus.EXPIRED,
        SignalStatus.RETRACTED,
    }),
    SignalStatus.EXPIRED: frozenset(),
    SignalStatus.RETRACTED: frozenset(),
}


def is_valid_signal_transition(
    from_status: SignalStatus, to_status: SignalStatus,
) -> bool:
    """Check whether a signal status transition is allowed."""
    return to_status in _VALID_TRANSITIONS.get(from_status, frozenset())


def valid_signal_transitions_from(status: SignalStatus) -> frozenset[SignalStatus]:
    """Return the set of states reachable from *status*."""
    return _VALID_TRANSITIONS.get(status, frozenset())


# ---------------------------------------------------------------------------
# Stable ID generation (matches outcome_contracts / action_contracts pattern)
# ---------------------------------------------------------------------------


def _stable_signal_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"signal_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical Signal contract
# ---------------------------------------------------------------------------


class CanonicalSignal(BaseModel):
    """One tenant-scoped, evidence-graded, deduplicated signal.

    Signals are the entry point for all Company Loops. They capture
    an observed fact, claim, or indicator about a company, contact,
    market, or internal system. A signal never authorizes external
    action by itself — that requires an Opportunity → Action → Approval
    chain.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    signal_id: NonEmptyString
    deduplication_key: NonEmptyString

    # Entity links (required by entity ownership registry)
    company_id: NonEmptyString
    source_id: NonEmptyString

    # Classification
    signal_type: SignalType
    sensitivity: SignalSensitivity = SignalSensitivity.INTERNAL
    consent_status: ConsentStatus = ConsentStatus.UNKNOWN

    # Content
    claim: str = ""
    evidence_ref: str = ""

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Lifecycle
    status: SignalStatus = SignalStatus.RAW

    # Context links
    opportunity_id: str = ""
    contact_id: str = ""

    # Timestamps
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_signal_invariants(self) -> CanonicalSignal:
        # Withdrawn consent blocks linking
        if (
            self.consent_status == ConsentStatus.WITHDRAWN
            and self.status == SignalStatus.LINKED
        ):
            raise ValueError(
                "signals with withdrawn consent cannot be linked to opportunities"
            )

        # observed_at must be timezone-aware
        if self.observed_at.tzinfo is None:
            raise ValueError("observed_at must be timezone-aware")

        # expires_at must be timezone-aware if set
        if self.expires_at is not None and self.expires_at.tzinfo is None:
            raise ValueError("expires_at must be timezone-aware")

        # Verify deterministic ID
        expected_id = _stable_signal_id({
            "company_id": self.company_id,
            "deduplication_key": self.deduplication_key,
            "source_id": self.source_id,
            "tenant_id": self.tenant_id,
        })
        if self.signal_id != expected_id:
            raise ValueError("signal_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_signal(
    *,
    tenant_id: str,
    deduplication_key: str,
    company_id: str,
    source_id: str,
    signal_type: SignalType,
    sensitivity: SignalSensitivity = SignalSensitivity.INTERNAL,
    consent_status: ConsentStatus = ConsentStatus.UNKNOWN,
    claim: str = "",
    evidence_ref: str = "",
    confidence: float = 0.5,
    opportunity_id: str = "",
    contact_id: str = "",
    observed_at: datetime | None = None,
    expires_at: datetime | None = None,
) -> CanonicalSignal:
    """Build a deterministic, idempotent, evidence-graded signal."""

    signal_id = _stable_signal_id({
        "company_id": company_id.strip(),
        "deduplication_key": deduplication_key.strip(),
        "source_id": source_id.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalSignal(
        tenant_id=tenant_id,
        signal_id=signal_id,
        deduplication_key=deduplication_key,
        company_id=company_id,
        source_id=source_id,
        signal_type=signal_type,
        sensitivity=sensitivity,
        consent_status=consent_status,
        claim=claim,
        evidence_ref=evidence_ref,
        confidence=confidence,
        opportunity_id=opportunity_id,
        contact_id=contact_id,
        observed_at=observed_at or datetime.now(UTC),
        expires_at=expires_at,
    )


def transition_signal(
    signal: CanonicalSignal,
    *,
    to_status: SignalStatus,
) -> CanonicalSignal:
    """Return a new Signal with an updated status after validating the transition.

    The returned Signal is a new frozen instance — the original is unchanged.
    """
    if not is_valid_signal_transition(signal.status, to_status):
        raise ValueError(
            f"invalid transition {signal.status.value} → {to_status.value}; "
            f"allowed: {sorted(s.value for s in valid_signal_transitions_from(signal.status))}"
        )

    return signal.model_copy(update={"status": to_status})


def is_signal_stale(
    signal: CanonicalSignal,
    *,
    now: datetime | None = None,
) -> bool:
    """Check whether a signal has expired based on its expires_at timestamp."""
    if signal.expires_at is None:
        return False
    check = now or datetime.now(UTC)
    return signal.expires_at <= check
