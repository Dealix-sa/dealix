"""Fail-closed adapter from operational SignalDetection to canonical Signal truth.

Bridges ``auto_client_acquisition.market_intelligence.signal_detectors.SignalDetection``
into ``CanonicalSignal`` without escalating authority. The operational detector
provides raw observations; this adapter normalises them into the tenant-scoped,
evidence-graded, deduplicated shape the rest of the Company Intelligence spine
expects.

Key constraints:
  - A ``SignalDetection`` has fine-grained string types (e.g. ``hiring_sales_rep``);
    a ``CanonicalSignal`` uses the coarser ``SignalType`` taxonomy. An explicit
    mapping is maintained; unknown detection types fail-closed to ``MARKET``.
  - ``observed_at`` must be timezone-aware in the canonical model; naive
    datetimes from detectors are promoted to UTC.
  - ``deduplication_key`` is stable: it is derived from ``(signal_type,
    company_id, evidence_url or source)``, so repeated ingestion of the same
    detector output produces the same ``CanonicalSignal`` identity.
  - The adapter never grants consent status above ``UNKNOWN``; that requires
    a separate ``ConsentBasis`` record.
"""
from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any

from dealix.company_intelligence.signal_contracts import (
    CanonicalSignal,
    ConsentStatus,
    SignalSensitivity,
    SignalType,
    build_signal,
)

# ---------------------------------------------------------------------------
# Operational signal-type → canonical SignalType mapping
# ---------------------------------------------------------------------------

_SIGNAL_TYPE_MAP: dict[str, SignalType] = {
    # Hiring signals → MARKET (market movement indicators)
    "hiring_sales_rep": SignalType.MARKET,
    "hiring_marketing": SignalType.MARKET,
    "hiring_engineering": SignalType.MARKET,
    # Business expansion → PRODUCT
    "new_branch_opened": SignalType.PRODUCT,
    "new_service_launched": SignalType.PRODUCT,
    "booking_page_added": SignalType.PRODUCT,
    "website_redesigned": SignalType.PRODUCT,
    # Technology adoption signals
    "whatsapp_business_added": SignalType.TECH_ADOPTION,
    "whatsapp_no_followup_system": SignalType.TECH_ADOPTION,
    "weak_website": SignalType.TECH_ADOPTION,
    # Advertising → MARKET
    "ads_volume_increased": SignalType.MARKET,
    # Events → MARKET
    "exhibition_participation": SignalType.MARKET,
    # Reviews and customer signals
    "negative_review_spike": SignalType.CUSTOMER,
    "review_surge": SignalType.CUSTOMER,
    # Sector/economy
    "sector_pulse_rising": SignalType.ECONOMIC,
    # Tender → MONEY
    "tender_published": SignalType.MONEY,
    # Leadership change → MARKET
    "leadership_change": SignalType.MARKET,
    # Funding → VENTURE
    "funding_round": SignalType.VENTURE,
    # Regulatory alignment
    "vision2030_alignment": SignalType.REGULATORY,
    "zatca_phase_2_eligible": SignalType.REGULATORY,
    # Partner signals
    "agency_no_proof": SignalType.PARTNER,
    # Sales process gaps → MONEY
    "high_ticket_b2b_no_sales_process": SignalType.MONEY,
    # Dormant leads → CUSTOMER
    "unused_leads_dormant": SignalType.CUSTOMER,
}


def _ensure_tz_aware(dt: datetime) -> datetime:
    """Promote a naive datetime to UTC; leave tz-aware datetimes unchanged."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt


def normalize_signal(
    detection: Any,
    *,
    tenant_id: str,
    source_id: str | None = None,
) -> CanonicalSignal:
    """Normalize one ``SignalDetection`` into a ``CanonicalSignal``.

    Parameters
    ----------
    detection:
        A ``SignalDetection`` or any duck-typed object with ``company_id``,
        ``signal_type``, ``detected_at``, ``source``, ``confidence``, and
        optionally ``evidence_url`` and ``payload``.
    tenant_id:
        The tenant scope for the resulting canonical signal. Required because
        ``SignalDetection`` is tenant-unaware.
    source_id:
        Explicit source identity. Falls back to ``detection.source`` when not
        provided.
    """
    company_id = str(getattr(detection, "company_id", "")).strip()
    if not company_id:
        raise ValueError("detection must have a non-empty company_id")

    signal_type_str = str(getattr(detection, "signal_type", "")).strip()
    if not signal_type_str:
        raise ValueError("detection must have a non-empty signal_type")

    # Map to canonical SignalType (fail-closed to MARKET for unknown types)
    canonical_type = _SIGNAL_TYPE_MAP.get(signal_type_str, SignalType.MARKET)

    detected_at = getattr(detection, "detected_at", None)
    if detected_at is None:
        raise ValueError("detection must have a detected_at timestamp")
    observed_at = _ensure_tz_aware(detected_at)

    source_raw = str(getattr(detection, "source", "")).strip()
    resolved_source_id = source_id or source_raw
    if not resolved_source_id:
        raise ValueError("detection must have a non-empty source or source_id must be provided")

    confidence = float(getattr(detection, "confidence", 0.5))
    confidence = max(0.0, min(1.0, confidence))

    evidence_url = getattr(detection, "evidence_url", None)
    evidence_ref = str(evidence_url) if evidence_url else ""

    # Build a stable deduplication key from the detection identity
    dedup_parts = [signal_type_str, company_id]
    if evidence_ref:
        dedup_parts.append(evidence_ref)
    else:
        dedup_parts.append(source_raw)
    deduplication_key = "|".join(dedup_parts)

    # Extract claim from payload if available
    payload = getattr(detection, "payload", {})
    if not isinstance(payload, dict):
        payload = {}
    claim = payload.get("title", "") or signal_type_str.replace("_", " ")

    return build_signal(
        tenant_id=tenant_id,
        deduplication_key=deduplication_key,
        company_id=company_id,
        source_id=resolved_source_id,
        signal_type=canonical_type,
        sensitivity=SignalSensitivity.INTERNAL,
        consent_status=ConsentStatus.UNKNOWN,
        claim=claim,
        evidence_ref=evidence_ref,
        confidence=confidence,
        observed_at=observed_at,
    )
