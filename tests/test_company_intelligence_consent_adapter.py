"""Tests for the normalize_consent adapter.

Verifies that operational ConsentRecord instances are correctly bridged
to CanonicalConsentBasis without escalating authority.
"""
from __future__ import annotations

from datetime import UTC, datetime, timezone
from types import SimpleNamespace

import pytest

from dealix.company_intelligence import (
    CanonicalConsentBasis,
    ConsentBasisStatus,
    ConsentBasisType,
    ConsentChannel,
)
from dealix.company_intelligence.consent_adapter import normalize_consent


def _consent_record(**overrides: object) -> SimpleNamespace:
    """Build a duck-typed ConsentRecord-like object."""
    values: dict[str, object] = {
        "record_id": "cons_abc123",
        "customer_id": "tenant-a",
        "contact_id": "contact-1",
        "record_type": "consent_granted",
        "lawful_basis": "consent",
        "purpose": "outreach",
        "channel": "email",
        "source": "explicit_email",
        "occurred_at": datetime(2026, 7, 1, 10, 0, 0),  # naive
        "expires_at": None,
        "proof_url": "https://example.com/consent-proof",
        "metadata": {},
    }
    values.update(overrides)
    return SimpleNamespace(**values)


class TestNormalizeConsentBasic:
    """Core normalization behavior."""

    def test_produces_canonical_consent_basis(self) -> None:
        record = _consent_record()
        consent = normalize_consent(record, tenant_id="tenant-a")

        assert isinstance(consent, CanonicalConsentBasis)
        assert consent.tenant_id == "tenant-a"
        assert consent.contact_id == "contact-1"
        assert consent.basis == ConsentBasisType.EXPLICIT_OPT_IN
        assert consent.channel == ConsentChannel.EMAIL
        assert consent.status == ConsentBasisStatus.ACTIVE
        assert consent.withdrawn_at is None
        assert consent.withdrawn_reason == ""

    def test_naive_datetime_promoted_to_utc(self) -> None:
        record = _consent_record(
            occurred_at=datetime(2026, 6, 15, 8, 0, 0),
        )
        consent = normalize_consent(record, tenant_id="t")
        assert consent.recorded_at.tzinfo is not None

    def test_tz_aware_datetime_preserved(self) -> None:
        dt = datetime(2026, 6, 15, 8, 0, 0, tzinfo=UTC)
        record = _consent_record(occurred_at=dt)
        consent = normalize_consent(record, tenant_id="t")
        assert consent.recorded_at == dt

    def test_source_id_fallback(self) -> None:
        record = _consent_record()
        consent = normalize_consent(record, tenant_id="t")
        assert consent.source_id == "explicit_email"

    def test_explicit_source_id_overrides(self) -> None:
        record = _consent_record()
        consent = normalize_consent(
            record, tenant_id="t", source_id="custom-source"
        )
        assert consent.source_id == "custom-source"


class TestNormalizeConsentBasisMapping:
    """Verify lawful basis mapping from operational to canonical."""

    @pytest.mark.parametrize(
        "lawful_basis,expected",
        [
            ("consent", ConsentBasisType.EXPLICIT_OPT_IN),
            ("legitimate_interest", ConsentBasisType.MANUAL_RESEARCH_ONLY),
            ("contract", ConsentBasisType.EXISTING_RELATIONSHIP),
            ("legal_obligation", ConsentBasisType.EXISTING_RELATIONSHIP),
            ("public_interest", ConsentBasisType.PUBLIC_SOURCE),
            ("vital_interest", ConsentBasisType.EXISTING_RELATIONSHIP),
        ],
    )
    def test_maps_all_known_bases(
        self, lawful_basis: str, expected: ConsentBasisType
    ) -> None:
        record = _consent_record(lawful_basis=lawful_basis)
        consent = normalize_consent(record, tenant_id="t")
        assert consent.basis == expected


class TestNormalizeConsentChannelMapping:
    """Verify channel string → ConsentChannel mapping."""

    @pytest.mark.parametrize(
        "channel_str,expected",
        [
            ("email", ConsentChannel.EMAIL),
            ("whatsapp", ConsentChannel.WHATSAPP),
            ("linkedin", ConsentChannel.LINKEDIN),
            ("sms", ConsentChannel.SMS),
            ("phone", ConsentChannel.PHONE),
        ],
    )
    def test_maps_known_channels(
        self, channel_str: str, expected: ConsentChannel
    ) -> None:
        record = _consent_record(channel=channel_str)
        # For whatsapp/sms with MANUAL_RESEARCH_ONLY → would violate invariant.
        # Use EXPLICIT_OPT_IN which is safe for all channels.
        consent = normalize_consent(record, tenant_id="t")
        assert consent.channel == expected

    def test_unknown_channel_defaults_to_email(self) -> None:
        record = _consent_record(channel="carrier_pigeon")
        consent = normalize_consent(record, tenant_id="t")
        assert consent.channel == ConsentChannel.EMAIL

    def test_all_channel_scoped_to_email(self) -> None:
        """'all' is ambiguous — fail-closed to email."""
        record = _consent_record(channel="all")
        consent = normalize_consent(record, tenant_id="t")
        assert consent.channel == ConsentChannel.EMAIL


class TestNormalizeConsentOptOut:
    """Opt-out records produce WITHDRAWN status."""

    def test_opt_out_produces_withdrawn_status(self) -> None:
        record = _consent_record(
            record_type="opt_out",
            lawful_basis=None,
        )
        consent = normalize_consent(record, tenant_id="t")
        assert consent.status == ConsentBasisStatus.WITHDRAWN
        assert consent.withdrawn_at is not None
        assert consent.withdrawn_reason == "opt_out_request"

    def test_opt_out_defaults_basis_to_explicit_opt_in(self) -> None:
        """Even opt-out records need a basis type for the canonical model."""
        record = _consent_record(
            record_type="opt_out",
            lawful_basis=None,
        )
        consent = normalize_consent(record, tenant_id="t")
        assert consent.basis == ConsentBasisType.EXPLICIT_OPT_IN


class TestNormalizeConsentEvidence:
    """Evidence reference handling."""

    def test_proof_url_included_in_evidence(self) -> None:
        record = _consent_record(
            proof_url="https://example.com/proof",
            source="form_submission",
        )
        consent = normalize_consent(record, tenant_id="t")
        assert "https://example.com/proof" in consent.evidence_refs
        assert "form_submission" in consent.evidence_refs

    def test_no_proof_url_uses_source(self) -> None:
        record = _consent_record(proof_url=None, source="api")
        consent = normalize_consent(record, tenant_id="t")
        assert "api" in consent.evidence_refs

    def test_higher_confidence_with_proof_url(self) -> None:
        with_proof = normalize_consent(
            _consent_record(proof_url="https://example.com/proof"),
            tenant_id="t",
        )
        without_proof = normalize_consent(
            _consent_record(proof_url=None),
            tenant_id="t",
        )
        assert with_proof.confidence > without_proof.confidence

    def test_fallback_manual_record_when_no_evidence(self) -> None:
        record = _consent_record(proof_url=None, source="")
        consent = normalize_consent(
            record, tenant_id="t", source_id="external"
        )
        assert "manual_record" in consent.evidence_refs


class TestNormalizeConsentDeterminism:
    """Identity stability across repeated normalisation."""

    def test_same_record_produces_same_id(self) -> None:
        record = _consent_record()
        first = normalize_consent(record, tenant_id="t")
        second = normalize_consent(record, tenant_id="t")
        assert first.consent_basis_id == second.consent_basis_id

    def test_different_tenant_produces_different_id(self) -> None:
        record = _consent_record()
        a = normalize_consent(record, tenant_id="t1")
        b = normalize_consent(record, tenant_id="t2")
        assert a.consent_basis_id != b.consent_basis_id

    def test_different_channel_produces_different_id(self) -> None:
        a = normalize_consent(
            _consent_record(channel="email"), tenant_id="t"
        )
        b = normalize_consent(
            _consent_record(channel="whatsapp"), tenant_id="t"
        )
        assert a.consent_basis_id != b.consent_basis_id


class TestNormalizeConsentValidation:
    """Input validation rejects incomplete records."""

    def test_rejects_empty_contact_id(self) -> None:
        with pytest.raises(ValueError, match="contact_id"):
            normalize_consent(
                _consent_record(contact_id=""), tenant_id="t"
            )

    def test_rejects_empty_record_type(self) -> None:
        with pytest.raises(ValueError, match="record_type"):
            normalize_consent(
                _consent_record(record_type=""), tenant_id="t"
            )

    def test_rejects_unknown_lawful_basis(self) -> None:
        with pytest.raises(ValueError, match="unknown lawful_basis"):
            normalize_consent(
                _consent_record(lawful_basis="alien_treaty"), tenant_id="t"
            )

    def test_rejects_missing_lawful_basis_on_non_opt_out(self) -> None:
        with pytest.raises(ValueError, match="lawful_basis"):
            normalize_consent(
                _consent_record(lawful_basis=None), tenant_id="t"
            )

    def test_rejects_missing_occurred_at(self) -> None:
        with pytest.raises(ValueError, match="occurred_at"):
            normalize_consent(
                _consent_record(occurred_at=None), tenant_id="t"
            )

    def test_rejects_missing_source_and_source_id(self) -> None:
        with pytest.raises(ValueError, match="source"):
            normalize_consent(
                _consent_record(source="", proof_url=None), tenant_id="t"
            )


class TestNormalizeConsentExpiry:
    """Expiry timestamp handling."""

    def test_expires_at_promoted_to_utc(self) -> None:
        record = _consent_record(
            expires_at=datetime(2027, 1, 1, 0, 0, 0),  # naive
        )
        consent = normalize_consent(record, tenant_id="t")
        assert consent.expires_at is not None
        assert consent.expires_at.tzinfo is not None

    def test_none_expires_at_preserved(self) -> None:
        record = _consent_record(expires_at=None)
        consent = normalize_consent(record, tenant_id="t")
        assert consent.expires_at is None
