"""Scoring tests — weights, clamping, vanity classification."""

from __future__ import annotations

import math

import pytest

from dealix.revenue_marketing.schemas import LEAD_SCORE_WEIGHTS, compute_lead_score
from dealix.revenue_marketing.scoring import (
    classify_outcome,
    compute_money_quality_score,
)


def test_lead_score_weights_sum_to_one() -> None:
    total = sum(LEAD_SCORE_WEIGHTS.values())
    assert math.isclose(total, 1.0, abs_tol=1e-9)


def test_lead_score_all_one_returns_one() -> None:
    assert compute_lead_score(1, 1, 1, 1, 1, 1) == pytest.approx(1.0)


def test_lead_score_all_zero_returns_zero() -> None:
    assert compute_lead_score(0, 0, 0, 0, 0, 0) == pytest.approx(0.0)


def test_lead_score_clamps_above_one() -> None:
    assert compute_lead_score(5.0, 5.0, 5.0, 5.0, 5.0, 5.0) == pytest.approx(1.0)


def test_lead_score_clamps_below_zero() -> None:
    assert compute_lead_score(-5.0, -5.0, -5.0, -5.0, -5.0, -5.0) == pytest.approx(0.0)


def test_lead_score_weighted_sum_sanity() -> None:
    # Only ICP fit and ability_to_pay; weights are 0.25 + 0.20 = 0.45.
    score = compute_lead_score(1.0, 0.0, 1.0, 0.0, 0.0, 0.0)
    assert score == pytest.approx(0.45)


def test_money_quality_score_perfect_positives_no_risk() -> None:
    score = compute_money_quality_score(1, 1, 1, 1, 1, 1, 0)
    assert score == pytest.approx(1.0)


def test_money_quality_score_high_risk_subtracts() -> None:
    no_risk = compute_money_quality_score(1, 1, 1, 1, 1, 1, 0)
    high_risk = compute_money_quality_score(1, 1, 1, 1, 1, 1, 1)
    assert high_risk < no_risk
    assert high_risk == pytest.approx(0.5)


def test_money_quality_score_clamped_zero() -> None:
    assert compute_money_quality_score(0, 0, 0, 0, 0, 0, 1) == pytest.approx(0.0)


def test_classify_outcome_noise() -> None:
    assert classify_outcome(0, 0, 0, 0, 0) == "noise"


def test_classify_outcome_engagement_only() -> None:
    assert classify_outcome(100, 0, 0, 0, 0) == "engagement_only"


def test_classify_outcome_leads_only() -> None:
    assert classify_outcome(100, 5, 0, 0, 0) == "leads_only"


def test_classify_outcome_sales_motion() -> None:
    assert classify_outcome(100, 5, 3, 0, 0) == "sales_motion"
    assert classify_outcome(100, 5, 3, 2, 0) == "sales_motion"


def test_classify_outcome_revenue_validated() -> None:
    assert classify_outcome(100, 5, 3, 2, 1) == "revenue_validated"
