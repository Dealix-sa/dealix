"""Quality gate runs and reports a pass rate over the generated queue."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import commercial_generate_400_drafts as gen  # noqa: E402
import commercial_quality_gate as qg  # noqa: E402
from startup_os_common import output_day_dir, write_jsonl  # noqa: E402

TEST_DAY = "2099-04-01"


def test_quality_gate_runs():
    write_jsonl(output_day_dir(TEST_DAY) / "draft_queue.jsonl", gen.generate(400, TEST_DAY))
    report = qg.run(TEST_DAY)
    assert report["total"] >= 400
    assert 0.0 <= report["pass_rate"] <= 1.0
    assert report["passed"] + report["failed"] == report["total"]
    assert (output_day_dir(TEST_DAY) / "quality_report.json").exists()
