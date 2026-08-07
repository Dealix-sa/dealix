"""Tests for the canonical Company and Contact graph contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence scoring bounds
  - Consent enforcement (opted-out contacts)
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
  - Frozen immutability
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.graph_contracts import (
    CanonicalCompany,
    CanonicalContact,
    CompanyStatus,
    ContactRole,
    ContactStatus,
    RelationshipStrength,
    build_company,
    build_contact,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _company(**overrides: object) -> CanonicalCompany:
    """Build a minimal valid company, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        deduplication_key="dedup-1",
        name="Acme Saudi",
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_company(**defaults)


def _contact(**overrides: object) -> CanonicalContact:
    """Build a minimal valid contact, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        deduplication_key="dedup-contact-1",
        company_id="company-1",
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_contact(**defaults)


# ---------------------------------------------------------------------------
# Company: Deterministic identity
# ---------------------------------------------------------------------------


class TestCompanyDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _company()
        b = _company()
        assert a.company_id == b.company_id

    def test_different_deduplication_key_produces_different_id(self) -> None:
        a = _company(deduplication_key="dedup-1")
        b = _company(deduplication_key="dedup-2")
        assert a.company_id != b.company_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _company(tenant_id="tenant-a")
        b = _company(tenant_id="tenant-b")
        assert a.company_id != b.company_id

    def test_different_source_produces_different_id(self) -> None:
        a = _company(source_id="source-1")
        b = _company(source_id="source-2")
        assert a.company_id != b.company_id

    def test_company_id_format(self) -> None:
        a = _company()
        assert a.company_id.startswith("company_")
        assert len(a.company_id) == 8 + 16  # "company_" + 16 hex chars

    def test_whitespace_in_deduplication_key_is_stripped(self) -> None:
        a = _company(deduplication_key="  dedup-1  ")
        b = _company(deduplication_key="dedup-1")
        assert a.company_id == b.company_id

    def test_name_does_not_affect_id(self) -> None:
        """Company name is mutable metadata — it must not affect the stable ID."""
        a = _company(name="Acme Saudi")
        b = _company(name="Acme Arabia")
        assert a.company_id == b.company_id


# ---------------------------------------------------------------------------
# Contact: Deterministic identity
# ---------------------------------------------------------------------------


class TestContactDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _contact()
        b = _contact()
        assert a.contact_id == b.contact_id

    def test_different_deduplication_key_produces_different_id(self) -> None:
        a = _contact(deduplication_key="dedup-contact-1")
        b = _contact(deduplication_key="dedup-contact-2")
        assert a.contact_id != b.contact_id

    def test_different_company_produces_different_id(self) -> None:
        a = _contact(company_id="company-1")
        b = _contact(company_id="company-2")
        assert a.contact_id != b.contact_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _contact(tenant_id="tenant-a")
        b = _contact(tenant_id="tenant-b")
        assert a.contact_id != b.contact_id

    def test_different_source_produces_different_id(self) -> None:
        a = _contact(source_id="source-1")
        b = _contact(source_id="source-2")
        assert a.contact_id != b.contact_id

    def test_contact_id_format(self) -> None:
        a = _contact()
        assert a.contact_id.startswith("contact_")
        assert len(a.contact_id) == 8 + 16  # "contact_" + 16 hex chars

    def test_whitespace_in_deduplication_key_is_stripped(self) -> None:
        a = _contact(deduplication_key="  dedup-contact-1  ")
        b = _contact(deduplication_key="dedup-contact-1")
        assert a.contact_id == b.contact_id


# ---------------------------------------------------------------------------
# Company: Confidence scoring
# ---------------------------------------------------------------------------


class TestCompanyConfidence:
    def test_default_confidence(self) -> None:
        a = _company()
        assert a.confidence == 0.5

    def test_custom_confidence(self) -> None:
        a = _company(confidence=0.9)
        assert a.confidence == 0.9

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _company(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _company(confidence=-0.1)


# ---------------------------------------------------------------------------
# Contact: Confidence scoring
# ---------------------------------------------------------------------------


class TestContactConfidence:
    def test_default_confidence(self) -> None:
        a = _contact()
        assert a.confidence == 0.5

    def test_custom_confidence(self) -> None:
        a = _contact(confidence=0.85)
        assert a.confidence == 0.85

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _contact(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _contact(confidence=-0.1)


# ---------------------------------------------------------------------------
# Contact: Consent enforcement
# ---------------------------------------------------------------------------


class TestContactConsentEnforcement:
    def test_default_consent_is_unknown(self) -> None:
        a = _contact()
        assert a.consent_status == "unknown"

    def test_opted_out_contact_cannot_be_engaged(self) -> None:
        a = _contact()
        data = a.model_dump()
        data["consent_status"] = "opted_out"
        data["status"] = ContactStatus.ENGAGED
        with pytest.raises(ValueError, match="opted-out"):
            CanonicalContact(**data)

    def test_opted_out_contact_can_be_identified(self) -> None:
        a = _contact(consent_status="opted_out", status=ContactStatus.IDENTIFIED)
        assert a.consent_status == "opted_out"
        assert a.status == ContactStatus.IDENTIFIED


# ---------------------------------------------------------------------------
# Company: Builder defaults
# ---------------------------------------------------------------------------


class TestCompanyBuilderDefaults:
    def test_default_status_is_discovered(self) -> None:
        a = _company()
        assert a.status == CompanyStatus.DISCOVERED

    def test_default_relationship_is_unknown(self) -> None:
        a = _company()
        assert a.relationship_strength == RelationshipStrength.UNKNOWN

    def test_default_icp_fit_score_is_zero(self) -> None:
        a = _company()
        assert a.icp_fit_score == 0.0

    def test_optional_context_links_empty(self) -> None:
        a = _company()
        assert a.signal_ids == ()
        assert a.opportunity_ids == ()
        assert a.name_ar == ""
        assert a.sector == ""
        assert a.city == ""

    def test_builder_with_full_context(self) -> None:
        a = build_company(
            tenant_id="tenant-a",
            deduplication_key="dedup-full",
            name="شركة التقنية المتقدمة",
            name_ar="شركة التقنية المتقدمة",
            source_id="source-1",
            sector="technology",
            city="riyadh",
            region="Saudi Arabia",
            website="https://example.sa",
            employee_count_estimate=50,
            source_url="https://registry.sa/company/123",
            confidence=0.8,
            status=CompanyStatus.QUALIFIED,
            relationship_strength=RelationshipStrength.WARM,
            icp_fit_score=0.75,
            signal_ids=("sig-1", "sig-2"),
            opportunity_ids=("opp-1",),
        )
        assert a.name == "شركة التقنية المتقدمة"
        assert a.sector == "technology"
        assert a.city == "riyadh"
        assert a.employee_count_estimate == 50
        assert a.icp_fit_score == 0.75
        assert len(a.signal_ids) == 2


# ---------------------------------------------------------------------------
# Contact: Builder defaults
# ---------------------------------------------------------------------------


class TestContactBuilderDefaults:
    def test_default_status_is_identified(self) -> None:
        a = _contact()
        assert a.status == ContactStatus.IDENTIFIED

    def test_default_role_is_other(self) -> None:
        a = _contact()
        assert a.role == ContactRole.OTHER

    def test_default_relationship_is_unknown(self) -> None:
        a = _contact()
        assert a.relationship_strength == RelationshipStrength.UNKNOWN

    def test_optional_fields_empty(self) -> None:
        a = _contact()
        assert a.name == ""
        assert a.email == ""
        assert a.phone == ""
        assert a.signal_ids == ()

    def test_builder_with_full_context(self) -> None:
        a = build_contact(
            tenant_id="tenant-a",
            deduplication_key="dedup-contact-full",
            company_id="company-1",
            source_id="source-1",
            name="Ahmed Mohammed",
            name_ar="أحمد محمد",
            role=ContactRole.FOUNDER,
            email="ahmed@example.sa",
            phone="+966501234567",
            confidence=0.9,
            status=ContactStatus.VERIFIED,
            relationship_strength=RelationshipStrength.WARM,
            consent_status="existing_relationship",
            consent_proof_ref="ref-consent-1",
            signal_ids=("sig-1",),
        )
        assert a.name == "Ahmed Mohammed"
        assert a.role == ContactRole.FOUNDER
        assert a.consent_status == "existing_relationship"
        assert len(a.signal_ids) == 1


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_company_extra_fields_forbidden(self) -> None:
        a = _company()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalCompany(**data)

    def test_contact_extra_fields_forbidden(self) -> None:
        a = _contact()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalContact(**data)


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_company_is_frozen(self) -> None:
        a = _company()
        with pytest.raises(Exception):
            a.status = CompanyStatus.ACTIVE  # type: ignore[misc]

    def test_contact_is_frozen(self) -> None:
        a = _contact()
        with pytest.raises(Exception):
            a.status = ContactStatus.ENGAGED  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestCompanyEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for the Company entity."""

    def test_required_fields_present(self) -> None:
        a = _company()
        # Required: tenant_id, name, source_id, confidence
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "name") and a.name
        assert hasattr(a, "source_id") and a.source_id
        assert hasattr(a, "confidence") and isinstance(a.confidence, float)

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_company(
                tenant_id="",
                deduplication_key="dedup-1",
                name="Acme",
                source_id="source-1",
            )

    def test_empty_name_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_company(
                tenant_id="tenant-a",
                deduplication_key="dedup-1",
                name="",
                source_id="source-1",
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_company(
                tenant_id="tenant-a",
                deduplication_key="dedup-1",
                name="Acme",
                source_id="",
            )


class TestContactEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for the Contact entity."""

    def test_required_fields_present(self) -> None:
        a = _contact()
        # Required: tenant_id, company_id, source_id, confidence
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "company_id") and a.company_id
        assert hasattr(a, "source_id") and a.source_id
        assert hasattr(a, "confidence") and isinstance(a.confidence, float)

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_contact(
                tenant_id="",
                deduplication_key="dedup-1",
                company_id="company-1",
                source_id="source-1",
            )

    def test_empty_company_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_contact(
                tenant_id="tenant-a",
                deduplication_key="dedup-1",
                company_id="",
                source_id="source-1",
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_contact(
                tenant_id="tenant-a",
                deduplication_key="dedup-1",
                company_id="company-1",
                source_id="",
            )
