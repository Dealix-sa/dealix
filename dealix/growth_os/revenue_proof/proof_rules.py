"""Proof rules — revenue is real only if backed by hard verification.

These are doctrine guards: vanity metrics never count as revenue.
"""

from __future__ import annotations

from typing import Final

from dealix.growth_os.revenue_proof.revenue_record import (
    RevenueRecord,
    VerificationType,
)

REAL_VERIFICATION_TYPES: Final[frozenset[VerificationType]] = frozenset(
    {
        "payment",
        "signed_agreement",
        "invoice",
        "retainer_active",
        "partner_paid",
    }
)

# Things callers sometimes try to count as revenue — they never do.
VANITY_METRICS: Final[frozenset[str]] = frozenset(
    {
        "likes",
        "views",
        "replies",
        "meetings_booked",
        "demo_requested",
        "downloads",
        "impressions",
        "followers",
    }
)


def is_real_revenue(record: RevenueRecord) -> bool:
    """Return True only if the record has a real verification doc.

    A status of ``paid`` or ``retainer_active`` is still rejected if there
    is no verification doc attached.
    """
    if record.amount_usd <= 0:
        return False
    if record.verification is None:
        return False
    return record.verification.kind in REAL_VERIFICATION_TYPES


def rejection_reasons(record: RevenueRecord) -> list[str]:
    """Enumerate why a record fails ``is_real_revenue``. Empty if it passes."""
    reasons: list[str] = []
    if record.amount_usd <= 0:
        reasons.append("amount_must_be_positive")
    if record.verification is None:
        reasons.append("missing_verification_doc")
    elif record.verification.kind not in REAL_VERIFICATION_TYPES:
        reasons.append(f"verification_kind_not_real:{record.verification.kind}")
    return reasons


def reject_vanity_metric(metric_name: str) -> bool:
    """Return True if the named metric is a vanity metric.

    Public helper used by the operating rules and dashboards.
    """
    return metric_name.strip().lower() in VANITY_METRICS


__all__ = [
    "REAL_VERIFICATION_TYPES",
    "VANITY_METRICS",
    "is_real_revenue",
    "reject_vanity_metric",
    "rejection_reasons",
]
