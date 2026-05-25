"""Verification primitives for revenue records.

Each check returns a small pydantic record that the quality score consumes.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.revenue_proof.revenue_record import RevenueRecord


class PaymentVerification(BaseModel):
    model_config = ConfigDict(extra="forbid")

    has_payment: bool
    reference: str = ""
    notes_en: str = ""


class InvoiceTracking(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invoice_present: bool
    invoice_id: str = ""
    notes_en: str = ""


class DealStageValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stage_consistent: bool
    expected_stage: str
    observed_stage: str
    notes_en: str = ""


class AttributionValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    has_any_attribution: bool
    sources_count: int = Field(ge=0)
    notes_en: str = ""


class VerificationBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payment: PaymentVerification
    invoice: InvoiceTracking
    deal_stage: DealStageValidation
    attribution: AttributionValidation


def _expected_stage_for(record: RevenueRecord) -> str:
    if record.verification and record.verification.kind == "payment":
        return "paid"
    if record.verification and record.verification.kind == "invoice":
        return "invoiced"
    if record.verification and record.verification.kind == "signed_agreement":
        return "committed"
    if record.verification and record.verification.kind == "retainer_active":
        return "retainer_active"
    if record.verification and record.verification.kind == "partner_paid":
        return "paid"
    return record.status


def verify_record(record: RevenueRecord) -> VerificationBundle:
    """Produce a VerificationBundle from a RevenueRecord. Pure function."""
    v = record.verification
    has_payment = v is not None and v.kind in {"payment", "partner_paid"}
    payment = PaymentVerification(
        has_payment=has_payment,
        reference=(v.reference if v and has_payment else ""),
        notes_en=("payment_verified" if has_payment else "no_payment"),
    )

    has_invoice = v is not None and v.kind == "invoice"
    invoice = InvoiceTracking(
        invoice_present=has_invoice,
        invoice_id=(v.reference if v and has_invoice else ""),
        notes_en=("invoice_tracked" if has_invoice else "no_invoice"),
    )

    expected = _expected_stage_for(record)
    deal_stage = DealStageValidation(
        stage_consistent=(expected == record.status),
        expected_stage=expected,
        observed_stage=record.status,
        notes_en=(
            "stage_matches_verification"
            if expected == record.status
            else "stage_mismatch"
        ),
    )

    src_count = sum(
        [
            len(record.attributed_channels),
            len(record.attributed_assets),
            len(record.attributed_agents),
            len(record.attributed_partners),
            len(record.attributed_campaigns),
        ]
    )
    attribution = AttributionValidation(
        has_any_attribution=src_count > 0,
        sources_count=src_count,
        notes_en=(
            "attribution_present" if src_count > 0 else "attribution_missing"
        ),
    )

    return VerificationBundle(
        payment=payment,
        invoice=invoice,
        deal_stage=deal_stage,
        attribution=attribution,
    )


__all__ = [
    "AttributionValidation",
    "DealStageValidation",
    "InvoiceTracking",
    "PaymentVerification",
    "VerificationBundle",
    "verify_record",
]
