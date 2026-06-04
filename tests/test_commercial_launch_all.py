"""The launch-everything orchestrator runs the full pipeline without sending."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import commercial_launch_all as launch  # noqa: E402
import commercial_launch_lib as lib  # noqa: E402


def test_run_all_pipeline(tmp_path, monkeypatch):
    monkeypatch.setattr(lib, "OUTPUT_ROOT", tmp_path)
    snap = launch.run_all(target=400, date="2026-06-04")

    assert snap["drafts"]["drafts_generated"] >= 400
    assert snap["safety_audit"]["verdict"] == "PASS"
    assert snap["readiness"]["verdict"] == "READY"
    assert snap["seed_validation"]["verdict"] == "PASS"
    assert snap["media_calendar_days"] == 30
    assert snap["external_sends_performed"] == 0
    assert snap["safety_flags"]["send_allowed"] is False

    out = tmp_path / "2026-06-04"
    assert (out / "LAUNCH_SNAPSHOT.md").exists()
    assert (out / "LAUNCH_SNAPSHOT.json").exists()
    assert (out / "media_social" / "content_calendar.json").exists()


def test_master_plan_doc_exists():
    assert (ROOT / "docs/commercial-launch/01_MASTER_LAUNCH_PLAN_A_TO_Z.md").exists()
