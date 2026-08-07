"""Tests for the canonical Signal contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence scoring bounds
  - Consent enforcement
  - Status transition state machine
  - Staleness detection
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from dealix.company_intelligence.signal_contracts import (
    CanonicalSignal,
    ConsentStatus,
    SignalSensitivity,
    SignalStatus,
    SignalType,
    build_signal,
    is_signal_stale,
    is_valid_signal_transition,
    transition_signal,
    valid_signal_transitions_from,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _signal(**overrides: object) -> CanonicalSignal:
    """Build a minimal valid signal, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        deduplication_key="dedup-1",
        company_id="company-1",
        source_id="source-1",
        signal_type=SignalType.CUSTOMER,
    )
    defaults.update(overrides)
    return build_signal(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _signal()
        b = _signal()
        assert a.signal_id == b.signal_id

    def test_different_deduplication_key_produces_different_id(self) -> None:
        a = _signal(deduplication_key="dedup-1")
        b = _signal(deduplication_key="dedup-2")
        assert a.signal_id != b.signal_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _signal(tenant_id="tenant-a")
        b = _signal(tenant_id="tenant-b")
        assert a.signal_id != b.signal_id

    def test_different_company_produces_different_id(self) -> None:
        a = _signal(company_id="company-1")
        b = _signal(company_id="company-2")
        assert a.signal_id != b.signal_id

    def test_different_source_produces_different_id(self) -> None:
        a = _signal(source_id="source-1")
        b = _signal(source_id="source-2")
        assert a.signal_id != b.signal_id

    def test_signal_id_format(self) -> None:
        a = _signal()
        assert a.signal_id.startswith("signal_")
        assert len(a.signal_id) == 7 + 16  # "signal_" + 16 hex chars

    def test_whitespace_in_deduplication_key_is_stripped(self) -> None:
        a = _signal(deduplication_key="  dedup-1  ")
        b = _signal(deduplication_key="dedup-1")
        assert a.signal_id == b.signal_id


# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------


class TestConfidenceScoring:
    def test_default_confidence(self) -> None:
        a = _signal()
        assert a.confidence == 0.5

    def test_custom_confidence(self) -> None:
        a = _signal(confidence=0.9)
        assert a.confidence == 0.9

    def test_confidence_floor_zero(self) -> None:
        a = _signal(confidence=0.0)
        assert a.confidence == 0.0

    def test_confidence_ceiling_one(self) -> None:
        a = _signal(confidence=1.0)
        assert a.confidence == 1.0

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _signal(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _signal(confidence=-0.1)


# ---------------------------------------------------------------------------
# Consent enforcement
# ---------------------------------------------------------------------------


class TestConsentEnforcement:
    def test_default_consent_is_unknown(self) -> None:
        a = _signal()
        assert a.consent_status == ConsentStatus.UNKNOWN

    def test_withdrawn_consent_blocks_linking(self) -> None:
        a = _signal(consent_status=ConsentStatus.WITHDRAWN)
        with pytest.raises(ValueError, match="withdrawn consent"):
            transition_signal(a, to_status=SignalStatus.VALIDATED)
            b = a.model_copy(update={
                "status": SignalStatus.LINKED,
                "consent_status": ConsentStatus.WITHDRAWN,
            })
            # Force construction to trigger validator
            CanonicalSignal(**b.model_dump())

    def test_withdrawn_consent_direct_construction_rejected(self) -> None:
        a = _signal()
        data = a.model_dump()
        data["status"] = SignalStatus.LINKED
        data["consent_status"] = ConsentStatus.WITHDRAWN
        with pytest.raises(ValueError, match="withdrawn consent"):
            CanonicalSignal(**data)

    def test_opt_in_consent_allows_linking(self) -> None:
        a = _signal(consent_status=ConsentStatus.OPT_IN)
        b = transition_signal(a, to_status=SignalStatus.VALIDATED)
        c = transition_signal(b, to_status=SignalStatus.LINKED)
        assert c.status == SignalStatus.LINKED
        assert c.consent_status == ConsentStatus.OPT_IN


# ---------------------------------------------------------------------------
# Status transitions
# ---------------------------------------------------------------------------


class TestStatusTransitions:
    def test_raw_to_validated(self) -> None:
        a = _signal()
        assert a.status == SignalStatus.RAW
        b = transition_signal(a, to_status=SignalStatus.VALIDATED)
        assert b.status == SignalStatus.VALIDATED
        assert a.status == SignalStatus.RAW  # original unchanged

    def test_validated_to_linked(self) -> None:
        a = _signal()
        b = transition_signal(a, to_status=SignalStatus.VALIDATED)
        c = transition_signal(b, to_status=SignalStatus.LINKED)
        assert c.status == SignalStatus.LINKED

    def test_expired_is_terminal(self) -> None:
        a = _signal()
        b = transition_signal(a, to_status=SignalStatus.EXPIRED)
        with pytest.raises(ValueError, match="invalid transition"):
            transition_signal(b, to_status=SignalStatus.RAW)

    def test_retracted_is_terminal(self) -> None:
        a = _signal()
        b = transition_signal(a, to_status=SignalStatus.RETRACTED)
        with pytest.raises(ValueError, match="invalid transition"):
            transition_signal(b, to_status=SignalStatus.RAW)

    def test_raw_cannot_skip_to_linked(self) -> None:
        a = _signal()
        with pytest.raises(ValueError, match="invalid transition"):
            transition_signal(a, to_status=SignalStatus.LINKED)

    def test_any_state_can_expire(self) -> None:
        for status in (SignalStatus.RAW, SignalStatus.VALIDATED, SignalStatus.LINKED):
            a = _signal()
            current = a
            # Walk to the target status
            if status == SignalStatus.VALIDATED:
                current = transition_signal(current, to_status=SignalStatus.VALIDATED)
            elif status == SignalStatus.LINKED:
                current = transition_signal(current, to_status=SignalStatus.VALIDATED)
                current = transition_signal(current, to_status=SignalStatus.LINKED)
            result = transition_signal(current, to_status=SignalStatus.EXPIRED)
            assert result.status == SignalStatus.EXPIRED

    def test_any_state_can_retract(self) -> None:
        for status in (SignalStatus.RAW, SignalStatus.VALIDATED, SignalStatus.LINKED):
            a = _signal()
            current = a
            if status == SignalStatus.VALIDATED:
                current = transition_signal(current, to_status=SignalStatus.VALIDATED)
            elif status == SignalStatus.LINKED:
                current = transition_signal(current, to_status=SignalStatus.VALIDATED)
                current = transition_signal(current, to_status=SignalStatus.LINKED)
            result = transition_signal(current, to_status=SignalStatus.RETRACTED)
            assert result.status == SignalStatus.RETRACTED

    def test_valid_transitions_from_raw(self) -> None:
        allowed = valid_signal_transitions_from(SignalStatus.RAW)
        assert SignalStatus.VALIDATED in allowed
        assert SignalStatus.EXPIRED in allowed
        assert SignalStatus.RETRACTED in allowed
        assert SignalStatus.LINKED not in allowed

    def test_is_valid_transition_helper(self) -> None:
        assert is_valid_signal_transition(SignalStatus.RAW, SignalStatus.VALIDATED) is True
        assert is_valid_signal_transition(SignalStatus.RAW, SignalStatus.LINKED) is False


# ---------------------------------------------------------------------------
# Staleness detection
# ---------------------------------------------------------------------------


class TestStalenessDetection:
    def test_no_expiry_is_not_stale(self) -> None:
        a = _signal()
        assert is_signal_stale(a) is False

    def test_future_expiry_is_not_stale(self) -> None:
        future = datetime.now(UTC) + timedelta(days=30)
        a = _signal(expires_at=future)
        assert is_signal_stale(a) is False

    def test_past_expiry_is_stale(self) -> None:
        past = datetime.now(UTC) - timedelta(days=1)
        a = _signal(expires_at=past)
        assert is_signal_stale(a) is True

    def test_stale_at_exact_boundary(self) -> None:
        now = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
        a = _signal(expires_at=now)
        assert is_signal_stale(a, now=now) is True


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _signal()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalSignal(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_status_is_raw(self) -> None:
        a = _signal()
        assert a.status == SignalStatus.RAW

    def test_default_sensitivity_is_internal(self) -> None:
        a = _signal()
        assert a.sensitivity == SignalSensitivity.INTERNAL

    def test_default_consent_is_unknown(self) -> None:
        a = _signal()
        assert a.consent_status == ConsentStatus.UNKNOWN

    def test_optional_context_links_empty(self) -> None:
        a = _signal()
        assert a.opportunity_id == ""
        assert a.contact_id == ""
        assert a.claim == ""
        assert a.evidence_ref == ""

    def test_builder_with_full_context(self) -> None:
        now = datetime.now(UTC)
        a = build_signal(
            tenant_id="tenant-a",
            deduplication_key="dedup-full",
            company_id="company-1",
            source_id="source-1",
            signal_type=SignalType.MARKET,
            sensitivity=SignalSensitivity.CONFIDENTIAL,
            consent_status=ConsentStatus.EXISTING_RELATIONSHIP,
            claim="Expanding into AI operations",
            evidence_ref="https://example.com/article",
            confidence=0.85,
            opportunity_id="opp-1",
            contact_id="contact-1",
            observed_at=now,
            expires_at=now + timedelta(days=90),
        )
        assert a.signal_type == SignalType.MARKET
        assert a.sensitivity == SignalSensitivity.CONFIDENTIAL
        assert a.consent_status == ConsentStatus.EXISTING_RELATIONSHIP
        assert a.confidence == 0.85
        assert a.opportunity_id == "opp-1"
        assert a.contact_id == "contact-1"


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_signal_is_frozen(self) -> None:
        a = _signal()
        with pytest.raises(Exception):
            a.status = SignalStatus.VALIDATED  # type: ignore[misc]

    def test_transition_returns_new_instance(self) -> None:
        a = _signal()
        b = transition_signal(a, to_status=SignalStatus.VALIDATED)
        assert a is not b
        assert a.status == SignalStatus.RAW
        assert b.status == SignalStatus.VALIDATED


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for the Signal entity."""

    def test_required_fields_present(self) -> None:
        a = _signal()
        # Required: tenant_id, company_id, source_id, signal_type, confidence
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "company_id") and a.company_id
        assert hasattr(a, "source_id") and a.source_id
        assert hasattr(a, "signal_type") and a.signal_type
        assert hasattr(a, "confidence") and isinstance(a.confidence, float)

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_signal(
                tenant_id="",
                deduplication_key="dedup-1",
                company_id="company-1",
                source_id="source-1",
                signal_type=SignalType.CUSTOMER,
            )

    def test_empty_company_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_signal(
                tenant_id="tenant-a",
                deduplication_key="dedup-1",
                company_id="",
                source_id="source-1",
                signal_type=SignalType.CUSTOMER,
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_signal(
                tenant_id="tenant-a",
                deduplication_key="dedup-1",
                company_id="company-1",
                source_id="",
                signal_type=SignalType.CUSTOMER,
            )

    def test_empty_deduplication_key_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_signal(
                tenant_id="tenant-a",
                deduplication_key="",
                company_id="company-1",
                source_id="source-1",
                signal_type=SignalType.CUSTOMER,
            )
