"""Tests for the normalize_signal adapter.

Verifies that operational SignalDetection records are correctly bridged
to CanonicalSignal without escalating authority.
"""
from __future__ import annotations

from datetime import UTC, datetime, timezone
from types import SimpleNamespace

import pytest

from dealix.company_intelligence import (
    CanonicalSignal,
    ConsentStatus,
    SignalSensitivity,
    SignalType,
    normalize_signal,
)


def _signal_detection(**overrides: object) -> SimpleNamespace:
    """Build a duck-typed SignalDetection-like object."""
    values: dict[str, object] = {
        "company_id": "company-1",
        "signal_type": "hiring_sales_rep",
        "detected_at": datetime(2026, 8, 1, 12, 0, 0),  # naive
        "source": "linkedin_jobs",
        "confidence": 0.9,
        "evidence_url": "https://linkedin.com/jobs/12345",
        "payload": {"title": "Senior Sales Rep"},
    }
    values.update(overrides)
    return SimpleNamespace(**values)


class TestNormalizeSignalBasic:
    """Core normalization behavior."""

    def test_produces_canonical_signal(self) -> None:
        detection = _signal_detection()
        signal = normalize_signal(detection, tenant_id="tenant-a")

        assert isinstance(signal, CanonicalSignal)
        assert signal.tenant_id == "tenant-a"
        assert signal.company_id == "company-1"
        assert signal.signal_type == SignalType.MARKET
        assert signal.confidence == 0.9
        assert signal.evidence_ref == "https://linkedin.com/jobs/12345"
        assert signal.sensitivity == SignalSensitivity.INTERNAL
        assert signal.consent_status == ConsentStatus.UNKNOWN
        assert signal.claim == "Senior Sales Rep"

    def test_naive_datetime_promoted_to_utc(self) -> None:
        detection = _signal_detection(
            detected_at=datetime(2026, 7, 15, 10, 0, 0),  # naive
        )
        signal = normalize_signal(detection, tenant_id="t")
        assert signal.observed_at.tzinfo is not None

    def test_tz_aware_datetime_preserved(self) -> None:
        dt = datetime(2026, 7, 15, 10, 0, 0, tzinfo=UTC)
        detection = _signal_detection(detected_at=dt)
        signal = normalize_signal(detection, tenant_id="t")
        assert signal.observed_at == dt

    def test_source_id_fallback_to_detection_source(self) -> None:
        detection = _signal_detection()
        signal = normalize_signal(detection, tenant_id="t")
        assert signal.source_id == "linkedin_jobs"

    def test_explicit_source_id_overrides_detection_source(self) -> None:
        detection = _signal_detection()
        signal = normalize_signal(detection, tenant_id="t", source_id="custom-source")
        assert signal.source_id == "custom-source"


class TestNormalizeSignalTypeMapping:
    """Verify operational signal types map to correct canonical types."""

    @pytest.mark.parametrize(
        "signal_type,expected",
        [
            ("hiring_sales_rep", SignalType.MARKET),
            ("hiring_marketing", SignalType.MARKET),
            ("hiring_engineering", SignalType.MARKET),
            ("new_branch_opened", SignalType.PRODUCT),
            ("new_service_launched", SignalType.PRODUCT),
            ("booking_page_added", SignalType.PRODUCT),
            ("website_redesigned", SignalType.PRODUCT),
            ("whatsapp_business_added", SignalType.TECH_ADOPTION),
            ("whatsapp_no_followup_system", SignalType.TECH_ADOPTION),
            ("weak_website", SignalType.TECH_ADOPTION),
            ("ads_volume_increased", SignalType.MARKET),
            ("exhibition_participation", SignalType.MARKET),
            ("negative_review_spike", SignalType.CUSTOMER),
            ("review_surge", SignalType.CUSTOMER),
            ("sector_pulse_rising", SignalType.ECONOMIC),
            ("tender_published", SignalType.MONEY),
            ("leadership_change", SignalType.MARKET),
            ("funding_round", SignalType.VENTURE),
            ("vision2030_alignment", SignalType.REGULATORY),
            ("zatca_phase_2_eligible", SignalType.REGULATORY),
            ("agency_no_proof", SignalType.PARTNER),
            ("high_ticket_b2b_no_sales_process", SignalType.MONEY),
            ("unused_leads_dormant", SignalType.CUSTOMER),
        ],
    )
    def test_maps_all_known_signal_types(
        self, signal_type: str, expected: SignalType
    ) -> None:
        detection = _signal_detection(signal_type=signal_type)
        signal = normalize_signal(detection, tenant_id="t")
        assert signal.signal_type == expected

    def test_unknown_signal_type_fails_closed_to_market(self) -> None:
        detection = _signal_detection(signal_type="some_future_detector")
        signal = normalize_signal(detection, tenant_id="t")
        assert signal.signal_type == SignalType.MARKET


class TestNormalizeSignalDeterminism:
    """Deduplication and identity stability."""

    def test_same_detection_produces_same_signal_id(self) -> None:
        detection = _signal_detection()
        first = normalize_signal(detection, tenant_id="t")
        second = normalize_signal(detection, tenant_id="t")
        assert first.signal_id == second.signal_id

    def test_different_evidence_produces_different_signal_id(self) -> None:
        a = normalize_signal(
            _signal_detection(evidence_url="https://example.com/a"),
            tenant_id="t",
        )
        b = normalize_signal(
            _signal_detection(evidence_url="https://example.com/b"),
            tenant_id="t",
        )
        assert a.signal_id != b.signal_id

    def test_different_tenant_produces_different_signal_id(self) -> None:
        detection = _signal_detection()
        a = normalize_signal(detection, tenant_id="t1")
        b = normalize_signal(detection, tenant_id="t2")
        assert a.signal_id != b.signal_id


class TestNormalizeSignalSafetyInvariants:
    """Fail-closed behavior and never-escalate guarantees."""

    def test_consent_status_always_unknown(self) -> None:
        """Adapter never grants consent — requires separate ConsentBasis record."""
        detection = _signal_detection()
        signal = normalize_signal(detection, tenant_id="t")
        assert signal.consent_status == ConsentStatus.UNKNOWN

    def test_sensitivity_always_internal(self) -> None:
        detection = _signal_detection()
        signal = normalize_signal(detection, tenant_id="t")
        assert signal.sensitivity == SignalSensitivity.INTERNAL

    def test_status_always_raw(self) -> None:
        """New signals always start as RAW; validation happens downstream."""
        detection = _signal_detection()
        signal = normalize_signal(detection, tenant_id="t")
        from dealix.company_intelligence import SignalStatus

        assert signal.status == SignalStatus.RAW

    def test_confidence_clamped_to_valid_range(self) -> None:
        high = normalize_signal(
            _signal_detection(confidence=1.5), tenant_id="t"
        )
        assert high.confidence == 1.0

        low = normalize_signal(
            _signal_detection(confidence=-0.3), tenant_id="t"
        )
        assert low.confidence == 0.0


class TestNormalizeSignalValidation:
    """Input validation rejects incomplete detections."""

    def test_rejects_empty_company_id(self) -> None:
        with pytest.raises(ValueError, match="company_id"):
            normalize_signal(
                _signal_detection(company_id=""), tenant_id="t"
            )

    def test_rejects_empty_signal_type(self) -> None:
        with pytest.raises(ValueError, match="signal_type"):
            normalize_signal(
                _signal_detection(signal_type=""), tenant_id="t"
            )

    def test_rejects_missing_detected_at(self) -> None:
        with pytest.raises(ValueError, match="detected_at"):
            normalize_signal(
                _signal_detection(detected_at=None), tenant_id="t"
            )

    def test_rejects_missing_source_and_source_id(self) -> None:
        with pytest.raises(ValueError, match="source"):
            normalize_signal(
                _signal_detection(source=""), tenant_id="t"
            )


class TestNormalizeSignalEdgeCases:
    """Edge cases and payload handling."""

    def test_missing_evidence_url_produces_empty_ref(self) -> None:
        detection = _signal_detection(evidence_url=None)
        signal = normalize_signal(detection, tenant_id="t")
        assert signal.evidence_ref == ""

    def test_empty_payload_uses_signal_type_as_claim(self) -> None:
        detection = _signal_detection(payload={})
        signal = normalize_signal(detection, tenant_id="t")
        assert signal.claim == "hiring sales rep"

    def test_non_dict_payload_handled_gracefully(self) -> None:
        detection = _signal_detection(payload="not a dict")
        signal = normalize_signal(detection, tenant_id="t")
        assert signal.claim == "hiring sales rep"
