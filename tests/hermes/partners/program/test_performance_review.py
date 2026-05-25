"""Partner performance review demotes partners with compliance violations."""

from __future__ import annotations

from dealix.hermes.partners.program.performance_review import evaluate


def test_violation_drops_to_rating_c_and_loses_tier() -> None:
    rep = evaluate("p_alpha", "2026-Q1", verified_revenue_sar=100_000, deals_closed=3, compliance_violations=1)
    assert rep.rating == "C"
    assert rep.keep_tier is False


def test_strong_perf_keeps_tier() -> None:
    rep = evaluate("p_beta", "2026-Q1", verified_revenue_sar=200_000, deals_closed=5, compliance_violations=0)
    assert rep.rating == "A"
    assert rep.keep_tier is True
