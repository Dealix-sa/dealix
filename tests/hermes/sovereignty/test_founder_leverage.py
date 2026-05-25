"""Founder time leverage records hours saved and computes leverage ratio."""

from __future__ import annotations

from dealix.hermes.sovereignty.founder_leverage import compute, leverage_ratio


def test_leverage_ratio_scales_with_hours_saved() -> None:
    snap = compute(
        "2026-Q1",
        tasks_delegated=12,
        proposals_drafted=6,
        decisions_summarized=20,
        follow_ups_prepared=30,
        hours_saved_estimate=80.0,
        high_value_actions_identified=5,
    )
    assert leverage_ratio(snap, hours_invested=20.0) == 4.0
    assert leverage_ratio(snap, hours_invested=0) == 0.0
