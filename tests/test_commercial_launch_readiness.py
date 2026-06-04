"""Launch readiness verifier returns READY once artifacts exist."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import commercial_launch_readiness as readiness  # noqa: E402


def test_readiness_ready():
    result = readiness.check()
    failing = [c for c in result["checks"] if not c["ok"]]
    assert result["verdict"] == "READY", failing


def test_readiness_includes_core_checks():
    result = readiness.check()
    names = {c["check"] for c in result["checks"]}
    assert "verticals_count==5" in names
    assert "distribution>=400" in names
    assert "safety_contract" in names
    assert "generates>=400" in names
    assert "all_drafts_safe" in names
