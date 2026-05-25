"""Revenue Proof — what counts as real revenue vs vanity."""

from __future__ import annotations

from dealix.growth_os.revenue_proof.proof_rules import (
    REAL_VERIFICATION_TYPES,
    VANITY_METRICS,
    is_real_revenue,
    rejection_reasons,
)
from dealix.growth_os.revenue_proof.revenue_record import (
    RevenueRecord,
    VerificationDoc,
)
from dealix.growth_os.revenue_proof.statuses import (
    REVENUE_STATUSES,
    RevenueStatus,
)

__all__ = [
    "REAL_VERIFICATION_TYPES",
    "REVENUE_STATUSES",
    "VANITY_METRICS",
    "RevenueRecord",
    "RevenueStatus",
    "VerificationDoc",
    "is_real_revenue",
    "rejection_reasons",
]
