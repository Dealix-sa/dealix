"""Safety audit passes for a freshly generated queue and proves no external send."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import commercial_generate_400_drafts as gen  # noqa: E402
import commercial_safety_audit as audit  # noqa: E402
from startup_os_common import output_day_dir, write_jsonl  # noqa: E402

TEST_DAY = "2099-02-01"


def _seed_queue(day: str) -> None:
    drafts = gen.generate(400, day)
    write_jsonl(output_day_dir(day) / "draft_queue.jsonl", drafts)


def test_safety_audit_passes():
    _seed_queue(TEST_DAY)
    report = audit.audit(TEST_DAY)
    assert report["passed"] is True
    assert report["draft_count"] >= 400
    assert report["external_send"] == "blocked"


def test_safety_audit_detects_tampered_flag():
    day = "2099-02-02"
    drafts = gen.generate(400, day)
    drafts[0]["send_allowed"] = True  # tamper
    write_jsonl(output_day_dir(day) / "draft_queue.jsonl", drafts)
    report = audit.audit(day)
    assert report["passed"] is False
    assert any("send_allowed" in v for v in report["violations"])
