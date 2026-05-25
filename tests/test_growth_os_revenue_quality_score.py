"""Revenue quality score weights + ordering tests."""

from __future__ import annotations

import math

from dealix.growth_os.revenue_assurance.quality_score import (
    QUALITY_WEIGHTS,
    revenue_quality_score,
)
from dealix.growth_os.revenue_proof.revenue_record import (
    RevenueRecord,
    VerificationDoc,
)


def test_weights_sum_to_one() -> None:
    assert math.isclose(sum(QUALITY_WEIGHTS.values()), 1.0, abs_tol=1e-9)


def test_unverified_record_scores_zero() -> None:
    rec = RevenueRecord(
        record_id="rev_a",
        customer_id="cust_001",
        offer_key="x",
        amount_usd=100.0,
        status="paid",
        verification=None,
    )
    qs = revenue_quality_score(rec)
    assert qs.score == 0.0
    assert qs.band == "reject"
    assert qs.is_real_revenue is False


def test_high_margin_retainer_outscores_one_off_low_margin() -> None:
    retainer = RevenueRecord(
        record_id="rev_retainer",
        customer_id="cust_001",
        offer_key="revenue_hunter_retainer",
        amount_usd=5_000.0,
        status="retainer_active",
        verification=VerificationDoc(kind="retainer_active", reference="ret_001"),
        attributed_channels=["referral"],
        delivery_effort_hours=10.0,
        margin_pct=0.70,
        retainer_signal=True,
    )
    one_off = RevenueRecord(
        record_id="rev_oneoff",
        customer_id="cust_002",
        offer_key="diag",
        amount_usd=500.0,
        status="paid",
        verification=VerificationDoc(kind="payment", reference="pay_002"),
        attributed_channels=["referral"],
        delivery_effort_hours=30.0,
        margin_pct=0.10,
        retainer_signal=False,
    )

    qs_retainer = revenue_quality_score(retainer)
    qs_oneoff = revenue_quality_score(one_off)
    assert qs_retainer.score > qs_oneoff.score
    assert qs_retainer.band in {"gold", "silver"}


def test_delivery_burden_subtracts() -> None:
    base_kwargs: dict[str, object] = {
        "record_id": "rev_b",
        "customer_id": "cust_001",
        "offer_key": "x",
        "amount_usd": 1000.0,
        "status": "paid",
        "verification": VerificationDoc(kind="payment", reference="pay_b"),
        "attributed_channels": ["referral"],
        "margin_pct": 0.5,
        "retainer_signal": True,
    }
    light = RevenueRecord(**base_kwargs, delivery_effort_hours=2.0)  # type: ignore[arg-type]
    heavy = RevenueRecord(**base_kwargs, delivery_effort_hours=200.0)  # type: ignore[arg-type]
    assert revenue_quality_score(light).score >= revenue_quality_score(heavy).score
