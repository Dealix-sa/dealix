"""Contract: the readiness check verifies the OS is internally consistent and
safe to run as a review-only draft factory."""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "scripts"))

import commercial_launch_core as core
import commercial_launch_readiness as readiness

# Isolate all runtime writes to a unique temp dir so parallel (-n auto) test
# workers never race on or pollute the repo's outputs/ tree.
import tempfile as _tempfile
import commercial_launch_core as _clc_isolate
_clc_isolate.OUTPUT_ROOT = _Path(_tempfile.mkdtemp(prefix='cl_test_out_'))


def test_readiness_passes_draft_only():
    report = readiness.run_readiness(date_str="2026-01-06")
    failed = [c for c in report["checks"] if not c["ok"]]
    assert report["ready_draft_only"] is True, failed


def test_offer_ladder_complete():
    cfg = core.load_all_configs()
    stages = {o["stage"] for o in cfg["offers"]["ladder"]}
    assert {"entry_diagnostic", "paid_pilot", "department_os",
            "monthly_retainer", "enterprise_custom_os"}.issubset(stages)


def test_five_verticals_configured():
    cfg = core.load_all_configs()
    assert len(cfg["verticals"]["verticals"]) >= 5


def test_global_safety_flags_locked():
    cfg = core.load_all_configs()
    flags = cfg["launch"]["global_safety_flags"]
    assert flags["send_allowed"] is False
    assert flags["external_send_blocked"] is True
    assert flags["requires_founder_approval"] is True
    assert flags["no_auto_send"] is True


def test_allowed_statuses_have_no_send_states():
    cfg = core.load_all_configs()
    allowed = set(cfg["launch"]["allowed_statuses"])
    assert not (allowed & core.FORBIDDEN_STATUSES)
