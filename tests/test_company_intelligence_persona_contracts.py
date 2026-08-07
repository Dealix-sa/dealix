"""Tests for the canonical Persona contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence scoring bounds
  - Evidence requirements
  - Targeting criteria
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
  - Frozen immutability
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.persona_contracts import (
    CanonicalPersona,
    PersonaStatus,
    build_persona,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _persona(**overrides: object) -> CanonicalPersona:
    """Build a minimal valid persona, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        name="Saudi B2B SaaS Founder",
        source_id="source-1",
        evidence_refs=("icp-analysis-1",),
    )
    defaults.update(overrides)
    return build_persona(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _persona()
        b = _persona()
        assert a.persona_id == b.persona_id

    def test_different_name_produces_different_id(self) -> None:
        a = _persona(name="Saudi B2B SaaS Founder")
        b = _persona(name="Enterprise CTO")
        assert a.persona_id != b.persona_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _persona(tenant_id="tenant-a")
        b = _persona(tenant_id="tenant-b")
        assert a.persona_id != b.persona_id

    def test_persona_id_format(self) -> None:
        a = _persona()
        assert a.persona_id.startswith("persona_")
        assert len(a.persona_id) == 8 + 16  # "persona_" + 16 hex chars

    def test_whitespace_in_name_is_stripped(self) -> None:
        a = _persona(name="  Saudi B2B SaaS Founder  ")
        b = _persona(name="Saudi B2B SaaS Founder")
        assert a.persona_id == b.persona_id

    def test_description_does_not_affect_id(self) -> None:
        """Description is mutable metadata — it must not affect the stable ID."""
        a = _persona(description="Desc A")
        b = _persona(description="Desc B")
        assert a.persona_id == b.persona_id


# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------


class TestConfidenceScoring:
    def test_default_confidence(self) -> None:
        a = _persona()
        assert a.confidence == 0.5

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _persona(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _persona(confidence=-0.1)

    def test_confidence_at_boundaries(self) -> None:
        a = _persona(confidence=0.0)
        assert a.confidence == 0.0
        b = _persona(confidence=1.0)
        assert b.confidence == 1.0


# ---------------------------------------------------------------------------
# Evidence requirements
# ---------------------------------------------------------------------------


class TestEvidenceRequirements:
    def test_empty_evidence_rejected(self) -> None:
        with pytest.raises(ValueError, match="evidence reference"):
            _persona(evidence_refs=())

    def test_single_evidence_accepted(self) -> None:
        a = _persona(evidence_refs=("ref-1",))
        assert a.evidence_refs == ("ref-1",)

    def test_multiple_evidence_accepted(self) -> None:
        a = _persona(evidence_refs=("ref-1", "ref-2", "ref-3"))
        assert len(a.evidence_refs) == 3


# ---------------------------------------------------------------------------
# Targeting criteria
# ---------------------------------------------------------------------------


class TestTargetingCriteria:
    def test_sectors_stored(self) -> None:
        a = _persona(target_sectors=("SaaS", "FinTech"))
        assert a.target_sectors == ("SaaS", "FinTech")

    def test_regions_stored(self) -> None:
        a = _persona(target_regions=("Riyadh", "Jeddah"))
        assert a.target_regions == ("Riyadh", "Jeddah")

    def test_size_bands_stored(self) -> None:
        a = _persona(target_size_bands=("20-50", "50-200"))
        assert a.target_size_bands == ("20-50", "50-200")

    def test_pain_points_stored(self) -> None:
        a = _persona(pain_points=("pipeline visibility", "lead qualification"))
        assert len(a.pain_points) == 2

    def test_preferred_channels_stored(self) -> None:
        a = _persona(preferred_channels=("email", "whatsapp"))
        assert a.preferred_channels == ("email", "whatsapp")

    def test_all_targeting_defaults_empty(self) -> None:
        a = _persona()
        assert a.target_sectors == ()
        assert a.target_regions == ()
        assert a.target_size_bands == ()
        assert a.pain_points == ()
        assert a.preferred_channels == ()


# ---------------------------------------------------------------------------
# Status lifecycle
# ---------------------------------------------------------------------------


class TestStatusLifecycle:
    def test_default_status_is_draft(self) -> None:
        a = _persona()
        assert a.status == PersonaStatus.DRAFT

    def test_active_status(self) -> None:
        a = _persona(status=PersonaStatus.ACTIVE)
        assert a.status == PersonaStatus.ACTIVE

    def test_retired_status(self) -> None:
        a = _persona(status=PersonaStatus.RETIRED)
        assert a.status == PersonaStatus.RETIRED


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _persona()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalPersona(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_status_is_draft(self) -> None:
        a = _persona()
        assert a.status == PersonaStatus.DRAFT

    def test_default_confidence(self) -> None:
        a = _persona()
        assert a.confidence == 0.5

    def test_default_evidence(self) -> None:
        a = build_persona(
            tenant_id="tenant-a",
            name="Test Persona",
            source_id="source-1",
        )
        assert a.evidence_refs == ("manual_observation",)

    def test_builder_with_full_context(self) -> None:
        a = build_persona(
            tenant_id="tenant-a",
            name="Saudi B2B SaaS Founder",
            source_id="source-1",
            description="Founders of 20-200 employee B2B SaaS companies in KSA",
            target_sectors=("SaaS", "Business Services"),
            target_regions=("Riyadh", "Jeddah", "Dammam"),
            target_size_bands=("20-50", "50-200"),
            pain_points=("pipeline visibility", "lead qualification", "manual reporting"),
            preferred_channels=("email", "whatsapp"),
            status=PersonaStatus.ACTIVE,
            confidence=0.85,
            evidence_refs=("icp-analysis", "pilot-feedback", "market-research"),
        )
        assert a.name == "Saudi B2B SaaS Founder"
        assert a.status == PersonaStatus.ACTIVE
        assert a.confidence == 0.85
        assert len(a.evidence_refs) == 3
        assert len(a.target_sectors) == 2
        assert len(a.target_regions) == 3


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_persona_is_frozen(self) -> None:
        a = _persona()
        with pytest.raises(Exception):
            a.status = PersonaStatus.ACTIVE  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for Persona."""

    def test_required_fields_present(self) -> None:
        a = _persona()
        # Required: tenant_id, name, evidence
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "name") and a.name
        assert hasattr(a, "evidence_refs") and len(a.evidence_refs) > 0

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_persona(
                tenant_id="",
                name="Test",
                source_id="source-1",
            )

    def test_empty_name_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_persona(
                tenant_id="tenant-a",
                name="",
                source_id="source-1",
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_persona(
                tenant_id="tenant-a",
                name="Test",
                source_id="",
            )
