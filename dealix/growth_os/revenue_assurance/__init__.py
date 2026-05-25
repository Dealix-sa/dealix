"""Revenue Assurance — verification, quality score, and operational checks."""

from __future__ import annotations

from dealix.growth_os.revenue_assurance.checks import (
    DeliveryEffortCheck,
    MarginCheck,
    RetainerPotentialCheck,
    run_all_checks,
)
from dealix.growth_os.revenue_assurance.quality_score import (
    QUALITY_WEIGHTS,
    RevenueQualityScore,
    revenue_quality_score,
)
from dealix.growth_os.revenue_assurance.verification import (
    AttributionValidation,
    DealStageValidation,
    InvoiceTracking,
    PaymentVerification,
    VerificationBundle,
    verify_record,
)

__all__ = [
    "QUALITY_WEIGHTS",
    "AttributionValidation",
    "DealStageValidation",
    "DeliveryEffortCheck",
    "InvoiceTracking",
    "MarginCheck",
    "PaymentVerification",
    "RetainerPotentialCheck",
    "RevenueQualityScore",
    "VerificationBundle",
    "revenue_quality_score",
    "run_all_checks",
    "verify_record",
]
