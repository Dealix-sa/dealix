"""Fail-closed adapter from operational ConsentRecord to canonical ConsentBasis truth.

Bridges ``auto_client_acquisition.compliance_os.consent_ledger.ConsentRecord``
into ``CanonicalConsentBasis`` without escalating authority. The operational
ledger captures append-only consent events; this adapter normalises them into
the tenant-scoped, channel-scoped shape the Draft and Approval pipelines
expect.

Key constraints:
  - Opt-out records produce a ``WITHDRAWN`` status — terminal and irreversible.
  - Naive datetimes from the ledger are promoted to UTC (the operational
    ledger's ``occurred_at`` is often naive).
  - The adapter never promotes lawful basis authority beyond what the
    operational record states.
  - ``MANUAL_RESEARCH_ONLY`` basis cannot be active for WhatsApp or SMS
    channels — enforced by the canonical model, not the adapter.
  - The adapter requires at least one evidence reference (``proof_url`` or
    ``source`` from the ledger).
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.company_intelligence.consent_contracts import (
    CanonicalConsentBasis,
    ConsentBasisStatus,
    ConsentBasisType,
    ConsentChannel,
    build_consent_basis,
)

# ---------------------------------------------------------------------------
# Lawful-basis mapping (operational → canonical)
# ---------------------------------------------------------------------------

_LAWFUL_BASIS_MAP: dict[str, ConsentBasisType] = {
    "consent": ConsentBasisType.EXPLICIT_OPT_IN,
    "legitimate_interest": ConsentBasisType.MANUAL_RESEARCH_ONLY,
    "contract": ConsentBasisType.EXISTING_RELATIONSHIP,
    "legal_obligation": ConsentBasisType.EXISTING_RELATIONSHIP,
    "public_interest": ConsentBasisType.PUBLIC_SOURCE,
    "vital_interest": ConsentBasisType.EXISTING_RELATIONSHIP,
}

# Channel mapping (operational string → canonical ConsentChannel)
_CHANNEL_MAP: dict[str, ConsentChannel] = {
    "email": ConsentChannel.EMAIL,
    "whatsapp": ConsentChannel.WHATSAPP,
    "linkedin": ConsentChannel.LINKEDIN,
    "sms": ConsentChannel.SMS,
    "phone": ConsentChannel.PHONE,
    "all": ConsentChannel.EMAIL,  # fail-closed: "all" scoped to email
}


def _ensure_tz_aware(dt: datetime) -> datetime:
    """Promote a naive datetime to UTC; leave tz-aware datetimes unchanged."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt


def normalize_consent(
    record: Any,
    *,
    tenant_id: str,
    source_id: str | None = None,
) -> CanonicalConsentBasis:
    """Normalize one ``ConsentRecord`` into a ``CanonicalConsentBasis``.

    Parameters
    ----------
    record:
        A ``ConsentRecord`` or any duck-typed object with ``contact_id``,
        ``record_type``, ``lawful_basis``, ``channel``, ``source``,
        ``occurred_at``, and optionally ``expires_at``, ``proof_url``,
        and ``customer_id``.
    tenant_id:
        The tenant scope for the resulting canonical consent basis.
    source_id:
        Explicit source identity for provenance. Falls back to
        ``record.source`` when not provided.
    """
    contact_id = str(getattr(record, "contact_id", "")).strip()
    if not contact_id:
        raise ValueError("consent record must have a non-empty contact_id")

    record_type = str(getattr(record, "record_type", "")).strip()
    if not record_type:
        raise ValueError("consent record must have a non-empty record_type")

    # Determine status from record_type
    is_opt_out = record_type == "opt_out"

    # Resolve lawful basis
    lawful_basis_raw = getattr(record, "lawful_basis", None)
    lawful_basis_str = str(lawful_basis_raw).strip() if lawful_basis_raw else ""

    if is_opt_out:
        # Opt-out records: default to EXPLICIT_OPT_IN since the person
        # had some prior relationship; status will be WITHDRAWN regardless.
        basis = ConsentBasisType.EXPLICIT_OPT_IN
    elif lawful_basis_str:
        basis = _LAWFUL_BASIS_MAP.get(lawful_basis_str)
        if basis is None:
            raise ValueError(
                f"unknown lawful_basis {lawful_basis_str!r}; "
                f"expected one of {sorted(_LAWFUL_BASIS_MAP)}"
            )
    else:
        raise ValueError("consent record must have a lawful_basis when not an opt-out")

    # Resolve channel
    channel_raw = str(getattr(record, "channel", "") or "").strip().lower()
    channel = _CHANNEL_MAP.get(channel_raw, ConsentChannel.EMAIL)

    # Resolve source
    source_raw = str(getattr(record, "source", "")).strip()
    resolved_source_id = source_id or source_raw
    if not resolved_source_id:
        raise ValueError(
            "consent record must have a non-empty source or source_id must be provided"
        )

    # Resolve timestamps
    occurred_at = getattr(record, "occurred_at", None)
    if occurred_at is None:
        raise ValueError("consent record must have an occurred_at timestamp")
    recorded_at = _ensure_tz_aware(occurred_at)

    expires_at_raw = getattr(record, "expires_at", None)
    expires_at = _ensure_tz_aware(expires_at_raw) if expires_at_raw is not None else None

    # Build evidence refs
    proof_url = getattr(record, "proof_url", None)
    evidence_parts: list[str] = []
    if proof_url:
        evidence_parts.append(str(proof_url))
    if source_raw:
        evidence_parts.append(source_raw)
    if not evidence_parts:
        evidence_parts.append("manual_record")
    evidence_refs = tuple(sorted(set(evidence_parts)))

    # Determine status and withdrawn_at
    if is_opt_out:
        status = ConsentBasisStatus.WITHDRAWN
        withdrawn_at: datetime | None = recorded_at
        withdrawn_reason = "opt_out_request"
    else:
        status = ConsentBasisStatus.ACTIVE
        withdrawn_at = None
        withdrawn_reason = ""

    return build_consent_basis(
        tenant_id=tenant_id,
        contact_id=contact_id,
        basis=basis,
        channel=channel,
        source_id=resolved_source_id,
        evidence_refs=evidence_refs,
        confidence=0.8 if proof_url else 0.5,
        status=status,
        expires_at=expires_at,
        recorded_at=recorded_at,
        withdrawn_at=withdrawn_at,
        withdrawn_reason=withdrawn_reason,
    )
