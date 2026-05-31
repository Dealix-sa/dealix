"""Revenue quality summary surfaces grade and headline."""

from __future__ import annotations

from dealix.hermes.board.revenue_quality_summary import summarize
from dealix.hermes.growth.revenue.revenue_quality import assess


def test_summary_includes_grade() -> None:
    q = assess(gross_margin=0.8, churn_risk=0.1, repeatability=0.85)
    s = summarize("2026-Q1", q)
    assert s.grade == q.grade
    assert "Revenue quality grade" in s.headline
