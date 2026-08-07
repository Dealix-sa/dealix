"""Tests for the canonical Relationship graph contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence scoring bounds
  - Self-referencing prevention
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
  - Frozen immutability
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.relationship_contracts import (
    CanonicalRelationship,
    EntityType,
    RelationshipStatus,
    RelationshipType,
    build_relationship,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _relationship(**overrides: object) -> CanonicalRelationship:
    """Build a minimal valid relationship, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        from_id="company-1",
        from_type=EntityType.COMPANY,
        to_id="company-2",
        to_type=EntityType.COMPANY,
        relationship_type=RelationshipType.CUSTOMER,
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_relationship(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _relationship()
        b = _relationship()
        assert a.relationship_id == b.relationship_id

    def test_different_from_id_produces_different_id(self) -> None:
        a = _relationship(from_id="company-1")
        b = _relationship(from_id="company-3")
        assert a.relationship_id != b.relationship_id

    def test_different_to_id_produces_different_id(self) -> None:
        a = _relationship(to_id="company-2")
        b = _relationship(to_id="company-4")
        assert a.relationship_id != b.relationship_id

    def test_different_type_produces_different_id(self) -> None:
        a = _relationship(relationship_type=RelationshipType.CUSTOMER)
        b = _relationship(relationship_type=RelationshipType.PARTNER)
        assert a.relationship_id != b.relationship_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _relationship(tenant_id="tenant-a")
        b = _relationship(tenant_id="tenant-b")
        assert a.relationship_id != b.relationship_id

    def test_different_source_produces_different_id(self) -> None:
        a = _relationship(source_id="source-1")
        b = _relationship(source_id="source-2")
        assert a.relationship_id != b.relationship_id

    def test_relationship_id_format(self) -> None:
        a = _relationship()
        assert a.relationship_id.startswith("rel_")
        assert len(a.relationship_id) == 4 + 16  # "rel_" + 16 hex chars

    def test_whitespace_in_from_id_is_stripped(self) -> None:
        a = _relationship(from_id="  company-1  ")
        b = _relationship(from_id="company-1")
        assert a.relationship_id == b.relationship_id

    def test_directionality_matters(self) -> None:
        """A→B and B→A are different relationships."""
        a = _relationship(from_id="company-1", to_id="company-2")
        b = _relationship(from_id="company-2", to_id="company-1")
        assert a.relationship_id != b.relationship_id


# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------


class TestConfidenceScoring:
    def test_default_confidence(self) -> None:
        a = _relationship()
        assert a.confidence == 0.5

    def test_custom_confidence(self) -> None:
        a = _relationship(confidence=0.9)
        assert a.confidence == 0.9

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _relationship(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _relationship(confidence=-0.1)


# ---------------------------------------------------------------------------
# Self-referencing prevention
# ---------------------------------------------------------------------------


class TestSelfReferencing:
    def test_same_from_and_to_rejected(self) -> None:
        with pytest.raises(ValueError, match="different entities"):
            _relationship(from_id="company-1", to_id="company-1")

    def test_different_from_and_to_accepted(self) -> None:
        a = _relationship(from_id="company-1", to_id="company-2")
        assert a.from_id != a.to_id


# ---------------------------------------------------------------------------
# Entity types
# ---------------------------------------------------------------------------


class TestEntityTypes:
    def test_company_to_company(self) -> None:
        a = _relationship(
            from_type=EntityType.COMPANY,
            to_type=EntityType.COMPANY,
        )
        assert a.from_type == EntityType.COMPANY
        assert a.to_type == EntityType.COMPANY

    def test_company_to_contact(self) -> None:
        a = _relationship(
            from_id="company-1",
            from_type=EntityType.COMPANY,
            to_id="contact-1",
            to_type=EntityType.CONTACT,
        )
        assert a.from_type == EntityType.COMPANY
        assert a.to_type == EntityType.CONTACT

    def test_contact_to_contact(self) -> None:
        a = _relationship(
            from_id="contact-1",
            from_type=EntityType.CONTACT,
            to_id="contact-2",
            to_type=EntityType.CONTACT,
        )
        assert a.from_type == EntityType.CONTACT
        assert a.to_type == EntityType.CONTACT


# ---------------------------------------------------------------------------
# Relationship types coverage
# ---------------------------------------------------------------------------


class TestRelationshipTypes:
    def test_all_types_are_valid(self) -> None:
        for rtype in RelationshipType:
            a = _relationship(relationship_type=rtype)
            assert a.relationship_type == rtype

    def test_customer_type(self) -> None:
        a = _relationship(relationship_type=RelationshipType.CUSTOMER)
        assert a.relationship_type == RelationshipType.CUSTOMER

    def test_partner_type(self) -> None:
        a = _relationship(relationship_type=RelationshipType.PARTNER)
        assert a.relationship_type == RelationshipType.PARTNER


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _relationship()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalRelationship(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_status_is_discovered(self) -> None:
        a = _relationship()
        assert a.status == RelationshipStatus.DISCOVERED

    def test_default_strength_is_unknown(self) -> None:
        a = _relationship()
        assert a.strength == "unknown"

    def test_default_signal_ids_empty(self) -> None:
        a = _relationship()
        assert a.signal_ids == ()

    def test_builder_with_full_context(self) -> None:
        a = build_relationship(
            tenant_id="tenant-a",
            from_id="company-1",
            from_type=EntityType.COMPANY,
            to_id="company-2",
            to_type=EntityType.COMPANY,
            relationship_type=RelationshipType.PARTNER,
            source_id="source-1",
            status=RelationshipStatus.CONFIRMED,
            strength="strong",
            description="Strategic technology partner",
            confidence=0.85,
            signal_ids=("sig-1", "sig-2"),
        )
        assert a.relationship_type == RelationshipType.PARTNER
        assert a.status == RelationshipStatus.CONFIRMED
        assert a.strength == "strong"
        assert a.confidence == 0.85
        assert len(a.signal_ids) == 2


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_relationship_is_frozen(self) -> None:
        a = _relationship()
        with pytest.raises(Exception):
            a.status = RelationshipStatus.ACTIVE  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for the Relationship entity."""

    def test_required_fields_present(self) -> None:
        a = _relationship()
        # Required: tenant_id, from_id, to_id, relationship_type, source_id
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "from_id") and a.from_id
        assert hasattr(a, "to_id") and a.to_id
        assert hasattr(a, "relationship_type") and a.relationship_type
        assert hasattr(a, "source_id") and a.source_id

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_relationship(
                tenant_id="",
                from_id="company-1",
                from_type=EntityType.COMPANY,
                to_id="company-2",
                to_type=EntityType.COMPANY,
                relationship_type=RelationshipType.CUSTOMER,
                source_id="source-1",
            )

    def test_empty_from_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_relationship(
                tenant_id="tenant-a",
                from_id="",
                from_type=EntityType.COMPANY,
                to_id="company-2",
                to_type=EntityType.COMPANY,
                relationship_type=RelationshipType.CUSTOMER,
                source_id="source-1",
            )

    def test_empty_to_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_relationship(
                tenant_id="tenant-a",
                from_id="company-1",
                from_type=EntityType.COMPANY,
                to_id="",
                to_type=EntityType.COMPANY,
                relationship_type=RelationshipType.CUSTOMER,
                source_id="source-1",
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_relationship(
                tenant_id="tenant-a",
                from_id="company-1",
                from_type=EntityType.COMPANY,
                to_id="company-2",
                to_type=EntityType.COMPANY,
                relationship_type=RelationshipType.CUSTOMER,
                source_id="",
            )
