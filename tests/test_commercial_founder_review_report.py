"""The founder review report is built and ranked by priority."""

from __future__ import annotations

import commercial_generate_400_drafts as gen
from _launch_util import SEED, TEST_DAY
from commercial_founder_review_report import build_report


def test_review_report_is_ranked():
    drafts = gen.generate(target=400, day=TEST_DAY, seed_path=SEED)["drafts"]
    rep = build_report(drafts, TEST_DAY)
    ranked = rep["ranked"]
    assert len(ranked) >= 1
    scores = [d["priority_score"] for d in ranked]
    assert scores == sorted(scores, reverse=True)


def test_review_columns_present():
    drafts = gen.generate(target=400, day=TEST_DAY, seed_path=SEED)["drafts"]
    rep = build_report(drafts, TEST_DAY)
    assert "draft_id" in rep["cols"]
    assert "priority_score" in rep["cols"]
    assert len(rep["rows"]) == len(rep["approved"])
