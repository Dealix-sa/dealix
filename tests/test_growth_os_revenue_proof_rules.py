"""DOCTRINE GUARD — vanity metrics never count as revenue."""

from __future__ import annotations

from dealix.growth_os.revenue_proof.proof_rules import (
    REAL_VERIFICATION_TYPES,
    VANITY_METRICS,
    is_real_revenue,
    reject_vanity_metric,
    rejection_reasons,
)
from dealix.growth_os.revenue_proof.revenue_record import (
    RevenueRecord,
    VerificationDoc,
)


def _record_with(verification: VerificationDoc | None, amount: float = 1000.0) -> RevenueRecord:
    return RevenueRecord(
        record_id="rev_001",
        customer_id="cust_001",
        offer_key="revenue_hunter",
        amount_usd=amount,
        status="paid",
        verification=verification,
    )


def test_vanity_metric_names_are_blocked() -> None:
    for name in ["likes", "views", "replies", "meetings_booked", "downloads"]:
        assert name in VANITY_METRICS
        assert reject_vanity_metric(name) is True


def test_record_without_verification_is_not_real() -> None:
    rec = _record_with(verification=None)
    assert is_real_revenue(rec) is False
    reasons = rejection_reasons(rec)
    assert "missing_verification_doc" in reasons


def test_record_with_zero_amount_is_not_real() -> None:
    rec = _record_with(
        verification=VerificationDoc(kind="payment", reference="pay_001"),
        amount=0.0,
    )
    assert is_real_revenue(rec) is False


def test_each_real_verification_type_passes() -> None:
    for kind in REAL_VERIFICATION_TYPES:
        rec = _record_with(verification=VerificationDoc(kind=kind, reference="ref"))
        assert is_real_revenue(rec) is True, f"failed kind: {kind}"


def test_status_paid_without_verification_is_still_rejected() -> None:
    # The status alone never counts. Doctrine guard.
    rec = RevenueRecord(
        record_id="rev_002",
        customer_id="cust_001",
        offer_key="ai_trust_kit",
        amount_usd=500.0,
        status="paid",
        verification=None,
    )
    assert is_real_revenue(rec) is False


def test_retainer_active_status_without_verification_is_rejected() -> None:
    rec = RevenueRecord(
        record_id="rev_003",
        customer_id="cust_001",
        offer_key="revenue_hunter_retainer",
        amount_usd=2000.0,
        status="retainer_active",
        verification=None,
    )
    assert is_real_revenue(rec) is False
