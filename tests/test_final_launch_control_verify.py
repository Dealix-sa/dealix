"""Final launch control orchestrator reaches PASS with all critical steps green."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import final_launch_control_verify as flc  # noqa: E402


def test_final_launch_control_passes():
    report = flc.run()
    assert report["decision"] == "PASS", report["critical_failures"]
    # Every critical step must be OK.
    for r in report["results"]:
        if r["critical"]:
            assert r["ok"], f"critical step failed: {r['step']}"
