"""Tests for `dealix.customer.value_report.MonthlyValueReportBuilder`."""

from __future__ import annotations

from datetime import date, timedelta

from dealix.customer.value_report import MonthlyValueReportBuilder
from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.schemas import Money


def test_build_aggregates_revenue_and_cost() -> None:
    builder = MonthlyValueReportBuilder()
    report = builder.build(
        customer_id="cust_x",
        period_outcomes=[
            Outcome(
                execution_id="plan_a",
                kind=OutcomeKind.MONEY,
                summary="pilot paid",
                value=Money.sar(8000),
            )
        ],
    )
    assert report.customer_id == "cust_x"
    assert report.revenue_delivered.amount == Money.sar(8000).amount
    # Cost-to-serve is the 25 % heuristic.
    assert report.cost_to_serve.amount == Money.sar(2000).amount
    assert report.next_quarter_plan


def test_build_collects_assets_and_learnings() -> None:
    builder = MonthlyValueReportBuilder()
    report = builder.build(
        customer_id="cust_y",
        period_outcomes=[
            Outcome(
                execution_id="plan_b",
                kind=OutcomeKind.ASSET,
                summary="reusable proposal template",
            ),
            Outcome(
                execution_id="plan_c",
                kind=OutcomeKind.LEARNING,
                summary="long sales cycle",
                learnings=["Discovery call needed before pricing"],
            ),
        ],
    )
    assert "reusable proposal template" in report.assets_built
    assert "Discovery call needed before pricing" in report.learnings


def test_build_uses_supplied_period_bounds() -> None:
    builder = MonthlyValueReportBuilder()
    start = date(2026, 5, 1)
    end = date(2026, 5, 31)
    report = builder.build(
        customer_id="cust_z",
        period_outcomes=[],
        period_start=start,
        period_end=end,
    )
    assert report.period_start == start
    assert report.period_end == end
