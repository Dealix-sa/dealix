"""Tests for `dealix.customer.health_score.CustomerHealthScorer`."""

from __future__ import annotations

from datetime import timedelta

from dealix.customer.health_score import CustomerHealthScorer, HealthBand
from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.schemas import Money, utcnow


def test_healthy_customer_lands_in_green_band() -> None:
    scorer = CustomerHealthScorer()
    health = scorer.score(
        customer_meta={
            "customer_id": "cust_a",
            "usage_ratio": 0.9,
            "days_past_due": 0,
            "support_tickets_week": 0,
            "last_engagement_at": utcnow().isoformat(),
        },
        outcomes=[
            Outcome(
                execution_id="plan_a",
                kind=OutcomeKind.MONEY,
                summary="paid",
                value=Money.sar(5000),
            )
        ],
    )
    assert health.band == HealthBand.GREEN
    assert health.score >= 4.0
    assert health.flags == []


def test_blocked_payment_pushes_score_into_red() -> None:
    scorer = CustomerHealthScorer()
    health = scorer.score(
        customer_meta={
            "customer_id": "cust_b",
            "usage_ratio": 0.2,
            "days_past_due": 45,
            "support_tickets_week": 8,
            "payment_blocked": True,
        },
        outcomes=[],
    )
    assert health.band == HealthBand.RED
    assert "payment_risk" in health.flags
    assert "support_volume_high" in health.flags


def test_engagement_decay_over_time() -> None:
    scorer = CustomerHealthScorer()
    now = utcnow()
    old = (now - timedelta(days=120)).isoformat()
    health = scorer.score(
        customer_meta={
            "customer_id": "cust_c",
            "usage_ratio": 0.5,
            "days_past_due": 5,
            "support_tickets_week": 1,
            "last_engagement_at": old,
        },
        outcomes=[],
        now=now,
    )
    assert health.components["engagement"] < 2.5
