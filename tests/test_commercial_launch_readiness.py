"""Launch readiness scoring + daily metrics."""

from __future__ import annotations

import json

from tests._lc_util import REPO_ROOT  # noqa: F401

from launch_os.drafts import generate_drafts, write_run
from launch_os.readiness import readiness_report, daily_metrics


def _queue(tmp_path):
    drafts = generate_drafts(target=400)
    out = tmp_path / "c"
    summary = write_run(drafts, out, out / "latest")
    return summary["run_dir"] / "draft_queue.jsonl"


def test_readiness_full_score(tmp_path):
    report = readiness_report(_queue(tmp_path), target=400)
    assert report["ready"] is True
    assert report["score"] == 100
    assert report["safety_pass"] is True


def test_daily_metrics_zero_sent():
    drafts = generate_drafts(target=400)
    m = daily_metrics(drafts)
    assert m["drafts_sent"] == 0
    assert m["total_drafts"] >= 400
    assert len(m["by_vertical"]) >= 5


def test_readiness_below_target_not_ready(tmp_path):
    drafts = generate_drafts(target=400)[:100]
    out = tmp_path / "c"
    summary = write_run(drafts, out, out / "latest")
    report = readiness_report(summary["run_dir"] / "draft_queue.jsonl", target=400)
    assert report["ready"] is False
