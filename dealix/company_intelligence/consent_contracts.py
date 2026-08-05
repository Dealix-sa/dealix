"""Canonical ConsentBasis contracts for the Company Intelligence privacy registry.

Every external action toward a Contact on a specific channel requires a
recorded ConsentBasis. This contract provides the single normalized shape
for tenant-scoped, channel-scoped consent records that feed the Draft and
Approval pipelines.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: ConsentBasis → privacy_and_governance
    (consent, lawful-basis and channel-eligibility policy).
Required fields: tenant_id, basis, channel, status, recorded_at.
Forbidden parallel names: Reachability, ContactPermission.
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


class ConsentBasisType(StrEnum):
    """Lawful bases for contacting a person on a given channel.

    Mirrors LawfulContactBasis in execution_contracts but lives in the
    privacy boundary — a ConsentBasis *record* references which basis
    was established, while a Draft *uses* that basis for its action.
    """

    EXISTING_RELATIONSHIP = "existing_relationship"
    EXPLICIT_OPT_IN = "explicit_opt_in"
    APPROVED_TEMPLATE = "approved_template"
    MANUAL_RESEARCH_ONLY = "manual_research_only"
    PUBLIC_SOURCE = "public_source"


class ConsentChannel(StrEnum):
    """Channels where consent applies."""

    EMAIL = "email"
    WHATSAPP = "whatsapp"
    LINKEDIN = "linkedin"
    SMS = "sms"
    PHONE = "phone"


class ConsentBasisStatus(StrEnum):
    """Lifecycle states for a consent basis record.

    Withdrawn consent is terminal — it cannot transition back to active.
    """

    ACTIVE = "active"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"
    SUPERSEDED = "superseded"


# Valid transitions for the consent basis state machine
_VALID_TRANSITIONS: dict[ConsentBasisStatus, frozenset[ConsentBasisStatus]] = {
    ConsentBasisStatus.ACTIVE: frozenset({
        ConsentBasisStatus.EXPIRED,
        ConsentBasisStatus.WITHDRAWN,
        ConsentBasisStatus.SUPERSEDED,
    }),
    ConsentBasisStatus.EXPIRED: frozenset({
        ConsentBasisStatus.WITHDRAWN,
    }),
    ConsentBasisStatus.WITHDRAWN: frozenset(),  # terminal
    ConsentBasisStatus.SUPERSEDED: frozenset({
        ConsentBasisStatus.WITHDRAWN,
    }),
}


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_consent_basis_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"consent_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical ConsentBasis contract
# ---------------------------------------------------------------------------


class CanonicalConsentBasis(BaseModel):
    """One tenant-scoped, channel-scoped consent basis record.

    A ConsentBasis establishes that a specific contact can be reached
    on a specific channel under a specific lawful basis. It feeds the
    Draft pipeline's lawful-contact-basis validation and the Contact's
    consent posture.

    Key invariants:
      - Withdrawn consent is terminal and blocks all action on that channel.
      - MANUAL_RESEARCH_ONLY basis cannot be active for WhatsApp or SMS.
      - Every record requires at least one evidence reference.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    consent_basis_id: NonEmptyString
    contact_id: NonEmptyString

    # Consent details
    basis: ConsentBasisType
    channel: ConsentChannel
    status: ConsentBasisStatus = ConsentBasisStatus.ACTIVE

    # Evidence
    evidence_refs: tuple[str, ...] = ()
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Provenance
    source_id: NonEmptyString

    # Expiry
    expires_at: datetime | None = None

    # Lifecycle
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    withdrawn_at: datetime | None = None
    withdrawn_reason: str = ""

    @model_validator(mode="after")
    def enforce_consent_invariants(self) -> CanonicalConsentBasis:
        # recorded_at must be timezone-aware
        if self.recorded_at.tzinfo is None:
            raise ValueError("recorded_at must be timezone-aware")

        # expires_at must be timezone-aware if set
        if self.expires_at is not None and self.expires_at.tzinfo is None:
            raise ValueError("expires_at must be timezone-aware")

        # withdrawn_at must be timezone-aware if set
        if self.withdrawn_at is not None and self.withdrawn_at.tzinfo is None:
            raise ValueError("withdrawn_at must be timezone-aware")

        # MANUAL_RESEARCH_ONLY cannot be active for WhatsApp or SMS
        if (
            self.basis == ConsentBasisType.MANUAL_RESEARCH_ONLY
            and self.channel in {ConsentChannel.WHATSAPP, ConsentChannel.SMS}
            and self.status == ConsentBasisStatus.ACTIVE
        ):
            raise ValueError(
                "manual_research_only basis cannot be active for WhatsApp or SMS channels"
            )

        # Withdrawn consent must have withdrawn_at
        if (
            self.status == ConsentBasisStatus.WITHDRAWN
            and self.withdrawn_at is None
        ):
            raise ValueError(
                "withdrawn consent must have a withdrawn_at timestamp"
            )

        # Active consent should not have withdrawn_at
        if (
            self.status == ConsentBasisStatus.ACTIVE
            and self.withdrawn_at is not None
        ):
            raise ValueError(
                "active consent must not have a withdrawn_at timestamp"
            )

        # Evidence refs must contain at least one entry
        if len(self.evidence_refs) == 0:
            raise ValueError(
                "consent basis requires at least one evidence reference"
            )

        # Verify deterministic ID
        expected_id = _stable_consent_basis_id({
            "basis": self.basis.value,
            "channel": self.channel.value,
            "contact_id": self.contact_id,
            "source_id": self.source_id,
            "tenant_id": self.tenant_id,
        })
        if self.consent_basis_id != expected_id:
            raise ValueError("consent_basis_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Transition helpers
# ---------------------------------------------------------------------------


def valid_consent_transitions_from(status: ConsentBasisStatus) -> frozenset[ConsentBasisStatus]:
    """Return the set of statuses reachable from *status*."""
    return _VALID_TRANSITIONS.get(status, frozenset())


def is_valid_consent_transition(
    from_status: ConsentBasisStatus,
    to_status: ConsentBasisStatus,
) -> bool:
    """Check whether a transition is allowed."""
    return to_status in valid_consent_transitions_from(from_status)


def transition_consent_basis(
    consent: CanonicalConsentBasis,
    *,
    to_status: ConsentBasisStatus,
    withdrawn_reason: str = "",
) -> CanonicalConsentBasis:
    """Return a new consent basis record transitioned to *to_status*.

    Raises ValueError on illegal transitions.
    """
    if not is_valid_consent_transition(consent.status, to_status):
        raise ValueError(
            f"cannot transition consent basis from {consent.status!r} to {to_status!r}"
        )

    updates: dict[str, Any] = {"status": to_status}

    if to_status == ConsentBasisStatus.WITHDRAWN:
        updates["withdrawn_at"] = datetime.now(UTC)
        updates["withdrawn_reason"] = withdrawn_reason

    return consent.model_copy(update=updates)


# ---------------------------------------------------------------------------
# Expiry detection
# ---------------------------------------------------------------------------


def is_consent_expired(
    consent: CanonicalConsentBasis,
    *,
    now: datetime | None = None,
) -> bool:
    """Check whether a consent basis has passed its expiry date."""
    if consent.expires_at is None:
        return False
    check = now or datetime.now(UTC)
    return check > consent.expires_at


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_consent_basis(
    *,
    tenant_id: str,
    contact_id: str,
    basis: ConsentBasisType,
    channel: ConsentChannel,
    source_id: str,
    evidence_refs: tuple[str, ...] = ("manual_record",),
    confidence: float = 0.5,
    status: ConsentBasisStatus = ConsentBasisStatus.ACTIVE,
    expires_at: datetime | None = None,
    recorded_at: datetime | None = None,
    withdrawn_at: datetime | None = None,
    withdrawn_reason: str = "",
) -> CanonicalConsentBasis:
    """Build a deterministic, idempotent, policy-governed consent basis."""

    consent_basis_id = _stable_consent_basis_id({
        "basis": basis.value,
        "channel": channel.value,
        "contact_id": contact_id.strip(),
        "source_id": source_id.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalConsentBasis(
        tenant_id=tenant_id,
        consent_basis_id=consent_basis_id,
        contact_id=contact_id,
        basis=basis,
        channel=channel,
        status=status,
        evidence_refs=evidence_refs,
        confidence=confidence,
        source_id=source_id,
        expires_at=expires_at,
        recorded_at=recorded_at or datetime.now(UTC),
        withdrawn_at=withdrawn_at,
        withdrawn_reason=withdrawn_reason,
    )
