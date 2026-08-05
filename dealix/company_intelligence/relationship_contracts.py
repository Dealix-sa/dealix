"""Canonical Relationship contracts for the Company Intelligence graph.

Relationships are directed edges in the opportunity graph connecting
companies, contacts, and partners. They carry provenance, strength,
and confidence — enabling the Company Loops to navigate the graph
of commercial relationships.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: Relationship → opportunity_graph
    (relationship edges between companies, contacts and partners).
Required fields: tenant_id, from_id, to_id, relationship_type, source_id.
Forbidden parallel names: Connection, NetworkEdge.
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


class RelationshipType(StrEnum):
    """Categories of relationships in the opportunity graph."""

    CUSTOMER = "customer"
    PARTNER = "partner"
    COMPETITOR = "competitor"
    REFERRAL = "referral"
    SUBSIDIARY = "subsidiary"
    PARENT_COMPANY = "parent_company"
    INVESTOR = "investor"
    VENDOR = "vendor"
    ADVISOR = "advisor"
    CHANNEL_PARTNER = "channel_partner"
    INTEGRATOR = "integrator"
    RESELLER = "reseller"
    OTHER = "other"


class RelationshipStatus(StrEnum):
    """Lifecycle states for a relationship edge."""

    DISCOVERED = "discovered"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISSOLVED = "dissolved"


class EntityType(StrEnum):
    """Types of entities that can participate in a relationship."""

    COMPANY = "company"
    CONTACT = "contact"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_relationship_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"rel_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical Relationship contract
# ---------------------------------------------------------------------------


class CanonicalRelationship(BaseModel):
    """One tenant-scoped, evidence-graded relationship edge in the graph.

    Relationships are directed: from_id → to_id with a type. For example,
    Company A is a CUSTOMER of Company B. They carry provenance and
    confidence scoring but never authorize external action by themselves.

    Key invariants:
      - from_id and to_id must be different entities.
      - Dissolved relationships are terminal.
      - Relationship ID is deterministic from the edge key.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    relationship_id: NonEmptyString

    # Edge definition
    from_id: NonEmptyString
    from_type: EntityType
    to_id: NonEmptyString
    to_type: EntityType
    relationship_type: RelationshipType

    # Classification
    status: RelationshipStatus = RelationshipStatus.DISCOVERED
    strength: str = "unknown"
    description: str = ""

    # Provenance
    source_id: NonEmptyString

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Context links
    signal_ids: tuple[str, ...] = ()

    # Timestamps
    discovered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    confirmed_at: datetime | None = None

    @model_validator(mode="after")
    def enforce_relationship_invariants(self) -> CanonicalRelationship:
        # from_id and to_id must differ
        if self.from_id == self.to_id:
            raise ValueError(
                "from_id and to_id must be different entities"
            )

        # confirmed_at must be timezone-aware if set
        if self.confirmed_at is not None and self.confirmed_at.tzinfo is None:
            raise ValueError("confirmed_at must be timezone-aware")

        # Verify deterministic ID
        expected_id = _stable_relationship_id({
            "from_id": self.from_id,
            "relationship_type": self.relationship_type.value,
            "source_id": self.source_id,
            "tenant_id": self.tenant_id,
            "to_id": self.to_id,
        })
        if self.relationship_id != expected_id:
            raise ValueError("relationship_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------

_RELATIONSHIP_TRANSITIONS: dict[RelationshipStatus, frozenset[RelationshipStatus]] = {
    RelationshipStatus.DISCOVERED: frozenset(
        {RelationshipStatus.CONFIRMED, RelationshipStatus.DISSOLVED}
    ),
    RelationshipStatus.CONFIRMED: frozenset(
        {RelationshipStatus.ACTIVE, RelationshipStatus.DISSOLVED}
    ),
    RelationshipStatus.ACTIVE: frozenset(
        {RelationshipStatus.INACTIVE, RelationshipStatus.DISSOLVED}
    ),
    RelationshipStatus.INACTIVE: frozenset(
        {RelationshipStatus.ACTIVE, RelationshipStatus.DISSOLVED}
    ),
    RelationshipStatus.DISSOLVED: frozenset(),  # terminal
}


def valid_relationship_transitions_from(
    status: RelationshipStatus,
) -> frozenset[RelationshipStatus]:
    """Return the set of valid target states from *status*."""
    return _RELATIONSHIP_TRANSITIONS.get(status, frozenset())


def is_valid_relationship_transition(
    from_status: RelationshipStatus,
    to_status: RelationshipStatus,
) -> bool:
    """Check whether *from_status* → *to_status* is a valid transition."""
    return to_status in valid_relationship_transitions_from(from_status)


def transition_relationship(
    relationship: CanonicalRelationship,
    *,
    to_status: RelationshipStatus,
) -> CanonicalRelationship:
    """Return a new CanonicalRelationship with *to_status* applied.

    Raises ValueError on invalid transitions. The original is never mutated.
    """
    if not is_valid_relationship_transition(relationship.status, to_status):
        raise ValueError(
            f"invalid relationship transition: "
            f"{relationship.status.value} → {to_status.value}"
        )
    return relationship.model_copy(update={"status": to_status})


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_relationship(
    *,
    tenant_id: str,
    from_id: str,
    from_type: EntityType,
    to_id: str,
    to_type: EntityType,
    relationship_type: RelationshipType,
    source_id: str,
    status: RelationshipStatus = RelationshipStatus.DISCOVERED,
    strength: str = "unknown",
    description: str = "",
    confidence: float = 0.5,
    signal_ids: tuple[str, ...] = (),
    confirmed_at: datetime | None = None,
) -> CanonicalRelationship:
    """Build a deterministic, idempotent, evidence-graded relationship edge."""

    relationship_id = _stable_relationship_id({
        "from_id": from_id.strip(),
        "relationship_type": relationship_type.value,
        "source_id": source_id.strip(),
        "tenant_id": tenant_id.strip(),
        "to_id": to_id.strip(),
    })

    return CanonicalRelationship(
        tenant_id=tenant_id,
        relationship_id=relationship_id,
        from_id=from_id,
        from_type=from_type,
        to_id=to_id,
        to_type=to_type,
        relationship_type=relationship_type,
        status=status,
        strength=strength,
        description=description,
        source_id=source_id,
        confidence=confidence,
        signal_ids=signal_ids,
        confirmed_at=confirmed_at,
    )
