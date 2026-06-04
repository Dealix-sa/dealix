"""The safety audit proves no external-send capability and catches violations."""

from __future__ import annotations

import commercial_safety_audit as audit
from _commercial_common import COMMERCIAL_OUTPUTS, write_jsonl


def test_code_surface_has_no_send_constructs():
    assert audit.scan_code_surface() == []


def test_clean_drafts_pass_flag_scan(tmp_path):
    day = "_pytest_safe"
    out = COMMERCIAL_OUTPUTS / day
    write_jsonl(
        out / "draft_queue.jsonl",
        [
            {
                "draft_id": "d1",
                "send_allowed": False,
                "external_send_blocked": True,
                "requires_founder_approval": True,
                "no_auto_send": True,
            }
        ],
    )
    try:
        count, violations = audit.scan_draft_flags(day)
        assert count == 1
        assert violations == []
    finally:
        import shutil

        shutil.rmtree(out, ignore_errors=True)


def test_tampered_flag_is_caught():
    day = "_pytest_bad"
    out = COMMERCIAL_OUTPUTS / day
    write_jsonl(
        out / "draft_queue.jsonl",
        [
            {
                "draft_id": "bad",
                "send_allowed": True,
                "external_send_blocked": False,
                "requires_founder_approval": True,
                "no_auto_send": False,
            }
        ],
    )
    try:
        _, violations = audit.scan_draft_flags(day)
        flags = {v["flag"] for v in violations}
        assert "send_allowed" in flags
        assert "external_send_blocked" in flags
        assert "no_auto_send" in flags
    finally:
        import shutil

        shutil.rmtree(out, ignore_errors=True)
