"""Revenue quality grade reflects margin, churn risk and repeatability."""

from __future__ import annotations

from dealix.hermes.growth.revenue.revenue_quality import assess


def test_high_margin_low_churn_yields_grade_a() -> None:
    q = assess(gross_margin=0.85, churn_risk=0.05, repeatability=0.9)
    assert q.grade == "A"
    assert q.quality_score >= 0.85


def test_low_quality_yields_grade_d() -> None:
    q = assess(gross_margin=0.1, churn_risk=0.7, repeatability=0.2)
    assert q.grade == "D"
