"""Payment to delivery audit link for rung 0-1 customer-facing deliverables.

Every rendered deliverable (Free Diagnostic report, 7-Day Revenue Proof
Sprint Proof Pack) must be traceable to a paid or written-commitment
ledger entry. This module records that link in the EXISTING capital_os
ledger -- no new ledger infrastructure is introduced.

A rendered deliverable is a reusable capital asset, so it is appended via
``capital_os.add_asset`` with:
- ``asset_type`` = capital asset type (proof example / sector insight),
- ``asset_ref``  = the payment / written-commitment reference,
- ``notes``      = a structured, PII-free audit note.

Pure-ish: the single side effect is the JSONL append performed by
``capital_os.add_asset``. No external HTTP, no LLM, no auto-send.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.capital_os.asset_types import CapitalAssetType
from auto_client_acquisition.capital_os.capital_ledger import CapitalAsset, add_asset

# Whitelisted deliverable kinds. Rung 0-1 only -- no rung 2-5 capability.
RUNG0_DIAGNOSTIC = "rung0_free_diagnostic"
RUNG1_PROOF_PACK = "rung1_proof_pack"

_DELIVERABLE_KINDS: frozenset[str] = frozenset({RUNG0_DIAGNOSTIC, RUNG1_PROOF_PACK})

# Reference kinds that satisfy the payment->delivery audit link. The rung 0
# diagnostic is free, so a written commitment (e.g. a signed intake) is the
# valid link there; rung 1 requires a real payment reference.
PAYMENT_REF = "payment"
WRITTEN_COMMITMENT_REF = "written_commitment"

_REFERENCE_KINDS: frozenset[str] = frozenset({PAYMENT_REF, WRITTEN_COMMITMENT_REF})


class DeliveryAuditError(ValueError):
    """Raised when a deliverable cannot be linked to a payment / commitment."""


@dataclass(frozen=True, slots=True)
class DeliveryAuditLink:
    """A recorded link between a rendered deliverable and a ledger entry."""

    audit_id: str
    customer_id: str
    engagement_id: str
    deliverable_kind: str
    reference_kind: str
    reference_id: str
    created_at: str

    def to_dict(self) -> dict[str, str]:
        return {
            "audit_id": self.audit_id,
            "customer_id": self.customer_id,
            "engagement_id": self.engagement_id,
            "deliverable_kind": self.deliverable_kind,
            "reference_kind": self.reference_kind,
            "reference_id": self.reference_id,
            "created_at": self.created_at,
        }


def _asset_type_for(deliverable_kind: str) -> CapitalAssetType:
    if deliverable_kind == RUNG1_PROOF_PACK:
        return CapitalAssetType.PROOF_EXAMPLE
    return CapitalAssetType.SECTOR_INSIGHT


def record_delivery_audit_link(
    *,
    customer_id: str,
    engagement_id: str,
    deliverable_kind: str,
    reference_kind: str,
    reference_id: str,
) -> DeliveryAuditLink:
    """Record a payment/commitment to delivery audit link in the capital ledger.

    Raises ``DeliveryAuditError`` if the deliverable is not linkable: a rung 1
    Proof Pack must be backed by a real payment reference; a rung 0 diagnostic
    may be backed by a written commitment. No reference -> no recorded link.
    """
    if deliverable_kind not in _DELIVERABLE_KINDS:
        raise DeliveryAuditError(
            f"unknown deliverable_kind: {deliverable_kind!r}"
        )
    if reference_kind not in _REFERENCE_KINDS:
        raise DeliveryAuditError(
            f"unknown reference_kind: {reference_kind!r}"
        )
    if not (reference_id or "").strip():
        raise DeliveryAuditError(
            "reference_id is required -- a deliverable must trace to a "
            "payment or written-commitment ledger entry"
        )
    if deliverable_kind == RUNG1_PROOF_PACK and reference_kind != PAYMENT_REF:
        raise DeliveryAuditError(
            "rung1_proof_pack requires a payment reference (paid pilot)"
        )

    note = (
        f"delivery_audit deliverable={deliverable_kind} "
        f"ref_kind={reference_kind} ref_id={reference_id.strip()}"
    )
    asset: CapitalAsset = add_asset(
        customer_id=customer_id,
        engagement_id=engagement_id,
        asset_type=_asset_type_for(deliverable_kind),
        reusable=False,
        asset_ref=reference_id.strip(),
        notes=note,
    )
    return DeliveryAuditLink(
        audit_id=asset.asset_id,
        customer_id=asset.customer_id,
        engagement_id=asset.engagement_id,
        deliverable_kind=deliverable_kind,
        reference_kind=reference_kind,
        reference_id=reference_id.strip(),
        created_at=asset.created_at,
    )


def audit_reference_label(link: DeliveryAuditLink) -> str:
    """Short bilingual audit line embedded in the rendered deliverable footer."""
    return (
        f"Audit / مرجع التدقيق: {link.audit_id} "
        f"({link.reference_kind}:{link.reference_id})"
    )


__all__ = [
    "PAYMENT_REF",
    "RUNG0_DIAGNOSTIC",
    "RUNG1_PROOF_PACK",
    "WRITTEN_COMMITMENT_REF",
    "DeliveryAuditError",
    "DeliveryAuditLink",
    "audit_reference_label",
    "record_delivery_audit_link",
]
