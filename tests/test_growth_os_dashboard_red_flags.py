"""Dashboard red-flag detection tests — each of the 7 patterns."""

from __future__ import annotations

from datetime import UTC, datetime

from dealix.growth_os.dashboard.metrics import GrowthDashboardSnapshot
from dealix.growth_os.dashboard.red_flags import RED_FLAG_CATALOG, detect_red_flags


def _snap(**overrides: object) -> GrowthDashboardSnapshot:
    base: dict[str, object] = {
        "period_start": datetime(2026, 5, 1, tzinfo=UTC),
        "period_end": datetime(2026, 5, 31, tzinfo=UTC),
    }
    base.update(overrides)
    return GrowthDashboardSnapshot.model_validate(base)


def test_catalog_has_seven_red_flags() -> None:
    keys = {f.key for f in RED_FLAG_CATALOG}
    expected = {
        "no_real_revenue",
        "pipeline_without_proposals",
        "low_win_rate",
        "margin_collapse",
        "no_retainer_revenue",
        "vanity_metric_drift",
        "operating_rules_breached",
    }
    assert keys == expected


def test_no_real_revenue_triggers() -> None:
    flags = detect_red_flags(_snap(real_revenue_usd=0.0))
    assert any(f.key == "no_real_revenue" for f in flags)


def test_pipeline_without_proposals_triggers() -> None:
    flags = detect_red_flags(_snap(pipeline_value_usd=50_000.0, proposals_sent=0))
    assert any(f.key == "pipeline_without_proposals" for f in flags)


def test_low_win_rate_triggers() -> None:
    flags = detect_red_flags(
        _snap(proposals_won=1, proposals_lost=10, real_revenue_usd=500.0)
    )
    assert any(f.key == "low_win_rate" for f in flags)


def test_margin_collapse_triggers() -> None:
    flags = detect_red_flags(_snap(avg_margin_pct=0.10, real_revenue_usd=500.0))
    assert any(f.key == "margin_collapse" for f in flags)


def test_no_retainer_revenue_triggers() -> None:
    flags = detect_red_flags(
        _snap(real_revenue_usd=1000.0, retainer_revenue_usd=0.0)
    )
    assert any(f.key == "no_retainer_revenue" for f in flags)


def test_vanity_metric_drift_triggers() -> None:
    flags = detect_red_flags(_snap(vanity_metric_attempts_blocked=1))
    assert any(f.key == "vanity_metric_drift" for f in flags)


def test_operating_rules_breached_triggers() -> None:
    flags = detect_red_flags(_snap(operating_rule_violations=5))
    assert any(f.key == "operating_rules_breached" for f in flags)
