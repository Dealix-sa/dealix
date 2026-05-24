"""Tests for `dealix.customer.renewal.RenewalEngine`."""

from __future__ import annotations

from datetime import date, timedelta

from dealix.customer.health_score import CustomerHealth, HealthBand
from dealix.customer.renewal import RenewalEngine, RenewalRecommendation


def _health(band: HealthBand, flags: list[str] | None = None, score: float = 3.0) -> CustomerHealth:
    return CustomerHealth(
        customer_id="cust_x",
        score=score,
        band=band,
        components={"usage": score, "payment": score, "support": score, "engagement": score},
        flags=list(flags or []),
    )


def test_green_health_recommends_upsell() -> None:
    engine = RenewalEngine()
    result = engine.assess(
        _health(HealthBand.GREEN, score=4.5),
        contract_meta={"renewal_due_date": (date.today() + timedelta(days=30)).isoformat()},
    )
    assert result.recommendation == RenewalRecommendation.UPSELL
    assert result.requires_sami_review is False


def test_red_health_routes_to_at_risk_with_sami_review() -> None:
    engine = RenewalEngine()
    result = engine.assess(
        _health(HealthBand.RED, flags=["usage_decline", "payment_risk"], score=1.0),
        contract_meta={},
    )
    assert result.recommendation == RenewalRecommendation.AT_RISK
    assert result.requires_sami_review is True


def test_payment_blocked_overrides_to_do_not_renew() -> None:
    engine = RenewalEngine()
    result = engine.assess(
        _health(HealthBand.AMBER, score=3.0),
        contract_meta={"payment_blocked": True},
    )
    assert result.recommendation == RenewalRecommendation.DO_NOT_RENEW
    assert result.requires_sami_review is True
