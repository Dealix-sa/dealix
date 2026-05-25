from __future__ import annotations

"""Smoke tests for ops_runtime."""

import csv
from pathlib import Path

import pytest

from ops_runtime.alerts_generator import generate_alerts
from ops_runtime.bottleneck_analyzer import find_bottleneck
from ops_runtime.ceo_brief_generator import generate_daily_brief
from ops_runtime.decision_queue_builder import build_decision_queue
from ops_runtime.founder_focus import compute_founder_focus
from ops_runtime.learning_decision_engine import decide_learning_actions
from ops_runtime.markdown_writer import read_markdown_frontmatter, write_markdown
from ops_runtime.metrics_calculator import (
    compute_delivery_metrics,
    compute_pipeline_metrics,
    compute_revenue_metrics,
)
from ops_runtime.private_ops_reader import (
    read_clients,
    read_mrr,
    read_pipeline,
    read_revenue_actions,
)
from ops_runtime.scorecard_updater import update_scorecard
from ops_runtime.target_scoring import score_against_targets
from ops_runtime.weekly_comparison import compare_to_prior_week
from ops_runtime.weekly_metrics_writer import write_weekly_metrics
from ops_runtime.weekly_review_generator import generate_weekly_review
from ops_runtime.weekly_review_v2_generator import generate_weekly_review_v2


def _all_metrics_sample() -> dict:
    return {
        "pipeline": {
            "total_leads": 30,
            "by_stage": {"lead": 20, "contacted": 5, "qualified": 3, "proposal": 2},
            "by_sector": {"fintech": 18, "logistics": 8, "edtech": 4},
            "pipeline_value_sar": 250000.0,
            "priority_high": 4,
        },
        "revenue": {
            "dms_sent": 30,
            "samples_sent": 3,
            "proposals_sent": 4,
            "payments_pursued": 1,
            "cash_collected_sar": 12000.0,
        },
        "delivery": {
            "active_clients": 2,
            "in_delivery": 1,
            "completed": 0,
            "at_risk": 0,
        },
    }


def test_pipeline_metrics_aggregates_counts() -> None:
    rows = [
        {"stage": "lead", "sector": "fintech", "deal_value_sar": "1000", "priority": "high"},
        {"stage": "lead", "sector": "fintech", "deal_value_sar": "2000", "priority": "low"},
        {"stage": "proposal", "sector": "logistics", "deal_value_sar": "5000", "priority": "P1"},
    ]
    m = compute_pipeline_metrics(rows)
    assert m["total_leads"] == 3
    assert m["by_stage"]["lead"] == 2
    assert m["by_sector"]["fintech"] == 2
    assert m["pipeline_value_sar"] == 8000.0
    assert m["priority_high"] == 2


def test_revenue_metrics_buckets_actions() -> None:
    rows = [
        {"action_type": "dm_sent"},
        {"action_type": "DM_SENT"},
        {"action_type": "sample_sent"},
        {"action_type": "proposal_sent"},
        {"action_type": "payment_pursued"},
        {"action_type": "payment_received", "amount_sar": "5000"},
    ]
    m = compute_revenue_metrics(rows)
    assert m["dms_sent"] == 2
    assert m["samples_sent"] == 1
    assert m["proposals_sent"] == 1
    assert m["payments_pursued"] == 1
    assert m["cash_collected_sar"] == 5000.0


def test_delivery_metrics_classifies_clients(tmp_path: Path) -> None:
    c1 = tmp_path / "alpha"
    c1.mkdir()
    (c1 / "status.md").write_text(
        "---\nstatus: in_delivery\n---\nactive\n", encoding="utf-8"
    )
    c2 = tmp_path / "beta"
    c2.mkdir()
    (c2 / "status.md").write_text(
        "---\nstatus: at_risk\n---\nblocked\n", encoding="utf-8"
    )
    c3 = tmp_path / "gamma"
    c3.mkdir()
    (c3 / "status.md").write_text(
        "---\nstatus: completed\n---\ndone\n", encoding="utf-8"
    )
    m = compute_delivery_metrics([c1, c2, c3])
    assert m["active_clients"] == 2
    assert m["in_delivery"] == 1
    assert m["at_risk"] == 1
    assert m["completed"] == 1


def test_private_ops_reader_empty_when_missing(tmp_path: Path) -> None:
    assert read_pipeline(tmp_path) == []
    assert read_revenue_actions(tmp_path) == []
    assert read_mrr(tmp_path) == []
    assert read_clients(tmp_path) == []


def test_private_ops_reader_parses_csv(tmp_path: Path) -> None:
    p = tmp_path / "pipeline" / "pipeline_tracker.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "stage", "sector"])
        w.writerow(["lead-1", "lead", "fintech"])
    rows = read_pipeline(tmp_path)
    assert len(rows) == 1
    assert rows[0]["stage"] == "lead"


def test_markdown_writer_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "x.md"
    write_markdown(path, {"type": "test", "n": 3}, "# Hello\n\nbody\n")
    fm = read_markdown_frontmatter(path)
    assert fm is not None
    assert fm["type"] == "test"
    assert fm["n"] == "3"


def test_daily_brief_writes_file(tmp_path: Path) -> None:
    out = generate_daily_brief(_all_metrics_sample(), tmp_path)
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "# Daily Brief" in text


def test_weekly_review_writes_file(tmp_path: Path) -> None:
    out = generate_weekly_review(_all_metrics_sample(), tmp_path)
    assert out.exists()
    assert "Weekly Review" in out.read_text(encoding="utf-8")


def test_weekly_metrics_appends(tmp_path: Path) -> None:
    write_weekly_metrics(_all_metrics_sample(), tmp_path)
    write_weekly_metrics(_all_metrics_sample(), tmp_path)
    csv_path = tmp_path / "metrics_history" / "weekly_metrics.csv"
    with csv_path.open("r", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 2


def test_weekly_comparison_handles_thin_history(tmp_path: Path) -> None:
    result = compare_to_prior_week(tmp_path)
    assert result["available"] is False
    write_weekly_metrics(_all_metrics_sample(), tmp_path)
    assert compare_to_prior_week(tmp_path)["available"] is False
    write_weekly_metrics(_all_metrics_sample(), tmp_path)
    assert compare_to_prior_week(tmp_path)["available"] is True


def test_learning_decisions_emit_signals() -> None:
    items = decide_learning_actions(_all_metrics_sample(), {"available": False})
    assert isinstance(items, list)
    # Should suggest doubling on top sector.
    assert any(i["type"] == "double" for i in items)


def test_bottleneck_analyzer_picks_stage() -> None:
    out = find_bottleneck(_all_metrics_sample())
    assert "stage" in out
    assert "recommendation" in out


def test_alerts_generator_returns_warnings() -> None:
    thin_metrics = {
        "pipeline": {"total_leads": 0},
        "revenue": {"dms_sent": 0, "proposals_sent": 0},
        "delivery": {"at_risk": 0},
    }
    alerts = generate_alerts(thin_metrics, {"available": False})
    assert any(a["severity"] in {"warn", "info"} for a in alerts)


def test_target_scoring_overall_percent() -> None:
    scores = score_against_targets(_all_metrics_sample())
    assert "_overall_percent" in scores
    assert 0.0 <= scores["_overall_percent"] <= 100.0


def test_founder_focus_returns_at_most_3() -> None:
    metrics = _all_metrics_sample()
    alerts = generate_alerts(metrics, {"available": False})
    focus = compute_founder_focus(metrics, alerts)
    assert 1 <= len(focus) <= 3


def test_decision_queue_writes_file(tmp_path: Path) -> None:
    out = build_decision_queue(tmp_path, [])
    assert out.exists()
    assert "Decision Queue" in out.read_text(encoding="utf-8")


def test_scorecard_writes_file(tmp_path: Path) -> None:
    out = update_scorecard(_all_metrics_sample(), tmp_path)
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "CEO Dashboard" in text
    assert "KPI scorecard" in text


def test_weekly_review_v2_writes_file(tmp_path: Path) -> None:
    metrics = _all_metrics_sample()
    out = generate_weekly_review_v2(metrics, {"available": False}, [], tmp_path)
    assert out.exists()
    assert "Weekly Review v2" in out.read_text(encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
