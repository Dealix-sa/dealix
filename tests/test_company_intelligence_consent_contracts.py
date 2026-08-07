"""Tests for the canonical ConsentBasis privacy contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence scoring bounds
  - Channel safety invariants
  - Consent withdrawal enforcement
  - State machine transitions
  - Expiry detection
  - Evidence requirements
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from dealix.company_intelligence.consent_contracts import (
    CanonicalConsentBasis,
    ConsentBasisStatus,
    ConsentBasisType,
    ConsentChannel,
    build_consent_basis,
    is_consent_expired,
    is_valid_consent_transition,
    transition_consent_basis,
    valid_consent_transitions_from,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _consent(**overrides: object) -> CanonicalConsentBasis:
    """Build a minimal valid consent basis, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        contact_id="contact-1",
        basis=ConsentBasisType.EXISTING_RELATIONSHIP,
        channel=ConsentChannel.EMAIL,
        source_id="source-1",
        evidence_refs=("ref-manual-1",),
    )
    defaults.update(overrides)
    return build_consent_basis(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _consent()
        b = _consent()
        assert a.consent_basis_id == b.consent_basis_id

    def test_different_contact_produces_different_id(self) -> None:
        a = _consent(contact_id="contact-1")
        b = _consent(contact_id="contact-2")
        assert a.consent_basis_id != b.consent_basis_id

    def test_different_channel_produces_different_id(self) -> None:
        a = _consent(channel=ConsentChannel.EMAIL)
        b = _consent(channel=ConsentChannel.WHATSAPP)
        assert a.consent_basis_id != b.consent_basis_id

    def test_different_basis_produces_different_id(self) -> None:
        a = _consent(basis=ConsentBasisType.EXISTING_RELATIONSHIP)
        b = _consent(basis=ConsentBasisType.EXPLICIT_OPT_IN)
        assert a.consent_basis_id != b.consent_basis_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _consent(tenant_id="tenant-a")
        b = _consent(tenant_id="tenant-b")
        assert a.consent_basis_id != b.consent_basis_id

    def test_different_source_produces_different_id(self) -> None:
        a = _consent(source_id="source-1")
        b = _consent(source_id="source-2")
        assert a.consent_basis_id != b.consent_basis_id

    def test_consent_basis_id_format(self) -> None:
        a = _consent()
        assert a.consent_basis_id.startswith("consent_")
        assert len(a.consent_basis_id) == 8 + 16  # "consent_" + 16 hex chars

    def test_whitespace_in_contact_id_is_stripped(self) -> None:
        a = _consent(contact_id="  contact-1  ")
        b = _consent(contact_id="contact-1")
        assert a.consent_basis_id == b.consent_basis_id


# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------


class TestConfidenceScoring:
    def test_default_confidence(self) -> None:
        a = _consent()
        assert a.confidence == 0.5

    def test_custom_confidence(self) -> None:
        a = _consent(confidence=0.9)
        assert a.confidence == 0.9

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _consent(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _consent(confidence=-0.1)


# ---------------------------------------------------------------------------
# Channel safety invariants
# ---------------------------------------------------------------------------


class TestChannelSafety:
    def test_manual_research_cannot_be_active_for_whatsapp(self) -> None:
        with pytest.raises(ValueError, match="manual_research_only"):
            _consent(
                basis=ConsentBasisType.MANUAL_RESEARCH_ONLY,
                channel=ConsentChannel.WHATSAPP,
                status=ConsentBasisStatus.ACTIVE,
            )

    def test_manual_research_cannot_be_active_for_sms(self) -> None:
        with pytest.raises(ValueError, match="manual_research_only"):
            _consent(
                basis=ConsentBasisType.MANUAL_RESEARCH_ONLY,
                channel=ConsentChannel.SMS,
                status=ConsentBasisStatus.ACTIVE,
            )

    def test_manual_research_can_be_active_for_email(self) -> None:
        a = _consent(
            basis=ConsentBasisType.MANUAL_RESEARCH_ONLY,
            channel=ConsentChannel.EMAIL,
        )
        assert a.status == ConsentBasisStatus.ACTIVE

    def test_explicit_opt_in_can_be_active_for_whatsapp(self) -> None:
        a = _consent(
            basis=ConsentBasisType.EXPLICIT_OPT_IN,
            channel=ConsentChannel.WHATSAPP,
        )
        assert a.status == ConsentBasisStatus.ACTIVE


# ---------------------------------------------------------------------------
# Consent withdrawal enforcement
# ---------------------------------------------------------------------------


class TestWithdrawalEnforcement:
    def test_withdrawn_requires_withdrawn_at(self) -> None:
        with pytest.raises(ValueError, match="withdrawn_at"):
            _consent(
                status=ConsentBasisStatus.WITHDRAWN,
                withdrawn_at=None,
            )

    def test_active_must_not_have_withdrawn_at(self) -> None:
        with pytest.raises(ValueError, match="withdrawn_at"):
            _consent(
                status=ConsentBasisStatus.ACTIVE,
                withdrawn_at=datetime.now(UTC),
            )

    def test_withdrawn_with_timestamp_and_reason(self) -> None:
        now = datetime.now(UTC)
        a = _consent(
            status=ConsentBasisStatus.WITHDRAWN,
            withdrawn_at=now,
            withdrawn_reason="Contact requested removal",
        )
        assert a.status == ConsentBasisStatus.WITHDRAWN
        assert a.withdrawn_at == now
        assert a.withdrawn_reason == "Contact requested removal"


# ---------------------------------------------------------------------------
# Evidence requirements
# ---------------------------------------------------------------------------


class TestEvidenceRequirements:
    def test_empty_evidence_rejected(self) -> None:
        with pytest.raises(ValueError, match="evidence reference"):
            _consent(evidence_refs=())

    def test_single_evidence_accepted(self) -> None:
        a = _consent(evidence_refs=("ref-1",))
        assert a.evidence_refs == ("ref-1",)

    def test_multiple_evidence_accepted(self) -> None:
        a = _consent(evidence_refs=("ref-1", "ref-2", "ref-3"))
        assert len(a.evidence_refs) == 3


# ---------------------------------------------------------------------------
# State machine transitions
# ---------------------------------------------------------------------------


class TestStateTransitions:
    def test_active_to_expired(self) -> None:
        a = _consent()
        b = transition_consent_basis(a, to_status=ConsentBasisStatus.EXPIRED)
        assert b.status == ConsentBasisStatus.EXPIRED

    def test_active_to_withdrawn(self) -> None:
        a = _consent()
        b = transition_consent_basis(
            a,
            to_status=ConsentBasisStatus.WITHDRAWN,
            withdrawn_reason="Contact opted out",
        )
        assert b.status == ConsentBasisStatus.WITHDRAWN
        assert b.withdrawn_at is not None
        assert b.withdrawn_reason == "Contact opted out"

    def test_active_to_superseded(self) -> None:
        a = _consent()
        b = transition_consent_basis(a, to_status=ConsentBasisStatus.SUPERSEDED)
        assert b.status == ConsentBasisStatus.SUPERSEDED

    def test_withdrawn_is_terminal(self) -> None:
        a = _consent(
            status=ConsentBasisStatus.WITHDRAWN,
            withdrawn_at=datetime.now(UTC),
            withdrawn_reason="test",
        )
        with pytest.raises(ValueError, match="cannot transition"):
            transition_consent_basis(a, to_status=ConsentBasisStatus.ACTIVE)

    def test_expired_to_withdrawn(self) -> None:
        a = _consent()
        b = transition_consent_basis(a, to_status=ConsentBasisStatus.EXPIRED)
        c = transition_consent_basis(b, to_status=ConsentBasisStatus.WITHDRAWN)
        assert c.status == ConsentBasisStatus.WITHDRAWN

    def test_expired_to_active_rejected(self) -> None:
        a = _consent()
        b = transition_consent_basis(a, to_status=ConsentBasisStatus.EXPIRED)
        with pytest.raises(ValueError, match="cannot transition"):
            transition_consent_basis(b, to_status=ConsentBasisStatus.ACTIVE)

    def test_valid_transitions_from_active(self) -> None:
        targets = valid_consent_transitions_from(ConsentBasisStatus.ACTIVE)
        assert ConsentBasisStatus.EXPIRED in targets
        assert ConsentBasisStatus.WITHDRAWN in targets
        assert ConsentBasisStatus.SUPERSEDED in targets

    def test_valid_transitions_from_withdrawn_is_empty(self) -> None:
        targets = valid_consent_transitions_from(ConsentBasisStatus.WITHDRAWN)
        assert len(targets) == 0

    def test_is_valid_consent_transition(self) -> None:
        assert is_valid_consent_transition(
            ConsentBasisStatus.ACTIVE, ConsentBasisStatus.EXPIRED
        )
        assert not is_valid_consent_transition(
            ConsentBasisStatus.WITHDRAWN, ConsentBasisStatus.ACTIVE
        )


# ---------------------------------------------------------------------------
# Expiry detection
# ---------------------------------------------------------------------------


class TestExpiryDetection:
    def test_no_expiry_is_not_expired(self) -> None:
        a = _consent(expires_at=None)
        assert is_consent_expired(a) is False

    def test_future_expiry_is_not_expired(self) -> None:
        now = datetime.now(UTC)
        a = _consent(expires_at=now + timedelta(days=90))
        assert is_consent_expired(a, now=now) is False

    def test_past_expiry_is_expired(self) -> None:
        now = datetime.now(UTC)
        a = _consent(expires_at=now - timedelta(days=1))
        assert is_consent_expired(a, now=now) is True

    def test_exact_boundary_is_not_expired(self) -> None:
        now = datetime.now(UTC)
        a = _consent(expires_at=now)
        # Exactly at boundary — not expired (> not >=)
        assert is_consent_expired(a, now=now) is False


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _consent()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalConsentBasis(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_status_is_active(self) -> None:
        a = _consent()
        assert a.status == ConsentBasisStatus.ACTIVE

    def test_default_confidence(self) -> None:
        a = _consent()
        assert a.confidence == 0.5

    def test_default_evidence(self) -> None:
        a = build_consent_basis(
            tenant_id="tenant-a",
            contact_id="contact-1",
            basis=ConsentBasisType.EXISTING_RELATIONSHIP,
            channel=ConsentChannel.EMAIL,
            source_id="source-1",
        )
        assert a.evidence_refs == ("manual_record",)

    def test_builder_with_full_context(self) -> None:
        now = datetime.now(UTC)
        a = build_consent_basis(
            tenant_id="tenant-a",
            contact_id="contact-1",
            basis=ConsentBasisType.EXPLICIT_OPT_IN,
            channel=ConsentChannel.WHATSAPP,
            source_id="source-1",
            evidence_refs=("consent-form-123", "email-confirmation-456"),
            confidence=0.95,
            expires_at=now + timedelta(days=365),
            recorded_at=now,
        )
        assert a.basis == ConsentBasisType.EXPLICIT_OPT_IN
        assert a.channel == ConsentChannel.WHATSAPP
        assert a.confidence == 0.95
        assert len(a.evidence_refs) == 2
        assert a.expires_at is not None


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_consent_basis_is_frozen(self) -> None:
        a = _consent()
        with pytest.raises(Exception):
            a.status = ConsentBasisStatus.EXPIRED  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for the ConsentBasis entity."""

    def test_required_fields_present(self) -> None:
        a = _consent()
        # Required: tenant_id, basis, channel, status, recorded_at
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "basis") and a.basis
        assert hasattr(a, "channel") and a.channel
        assert hasattr(a, "status") and a.status
        assert hasattr(a, "recorded_at") and a.recorded_at

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_consent_basis(
                tenant_id="",
                contact_id="contact-1",
                basis=ConsentBasisType.EXISTING_RELATIONSHIP,
                channel=ConsentChannel.EMAIL,
                source_id="source-1",
            )

    def test_empty_contact_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_consent_basis(
                tenant_id="tenant-a",
                contact_id="",
                basis=ConsentBasisType.EXISTING_RELATIONSHIP,
                channel=ConsentChannel.EMAIL,
                source_id="source-1",
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_consent_basis(
                tenant_id="tenant-a",
                contact_id="contact-1",
                basis=ConsentBasisType.EXISTING_RELATIONSHIP,
                channel=ConsentChannel.EMAIL,
                source_id="",
            )
