"""Commercial launch readiness runs the pipeline and reaches GO with all outputs."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import commercial_launch_readiness as clr  # noqa: E402

TEST_DAY = "2099-07-01"


def test_readiness_go_after_pipeline():
    report = clr.run(TEST_DAY, regenerate=True)
    assert report["missing_outputs"] == []
    assert report["safety_passed"] is True
    assert report["decision"] == "GO"


def test_required_outputs_listed():
    assert "safety_audit.json" in clr.REQUIRED_OUTPUTS
    assert "draft_queue.jsonl" in clr.REQUIRED_OUTPUTS
