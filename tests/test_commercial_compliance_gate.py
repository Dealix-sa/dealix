"""Compliance gate flags banned claims and missing opt-out; writes rejected file."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import commercial_compliance_gate as cg  # noqa: E402
import commercial_generate_400_drafts as gen  # noqa: E402
from startup_os_common import output_day_dir, write_jsonl  # noqa: E402

TEST_DAY = "2099-05-01"


def test_clean_draft_passes_check():
    drafts = gen.generate(400, TEST_DAY)
    assert cg.check(drafts[0]) == []


def test_banned_phrase_is_caught():
    drafts = gen.generate(400, TEST_DAY)
    bad = dict(drafts[0])
    bad["body"] = "We offer guaranteed ROI and guaranteed revenue."
    reasons = cg.check(bad)
    assert any("banned_phrase" in r for r in reasons)


def test_missing_opt_out_is_caught():
    drafts = gen.generate(400, TEST_DAY)
    bad = dict(drafts[0])
    bad["opt_out"] = ""
    assert "missing_opt_out" in cg.check(bad)


def test_run_writes_report():
    write_jsonl(output_day_dir(TEST_DAY) / "draft_queue.jsonl", gen.generate(400, TEST_DAY))
    report = cg.run(TEST_DAY)
    assert report["total"] >= 400
    assert (output_day_dir(TEST_DAY) / "rejected_drafts.jsonl").exists()
    assert (output_day_dir(TEST_DAY) / "compliance_report.json").exists()
