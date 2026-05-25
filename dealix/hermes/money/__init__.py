"""
Hermes Money — Section 51.

Verified revenue conditions:
    - payment_received
    - signed_agreement
    - invoice_confirmed
    - retainer_active
    - partner_paid_customer

Never counted as revenue:
    - likes / views / meetings booked / verbal interest / unqualified pipeline
"""

from .revenue_events import RevenueEvent, RevenueEventKind, RevenueEventLog
from .revenue_verification import RevenueVerifier, VerificationResult
from .revenue_quality import RevenueQualityScorer, QualityScore

__all__ = [
    "QualityScore",
    "RevenueEvent",
    "RevenueEventKind",
    "RevenueEventLog",
    "RevenueQualityScorer",
    "RevenueVerifier",
    "VerificationResult",
]
