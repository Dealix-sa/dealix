"""Commercial launch readiness reports GO when the OS is complete and safe."""

from __future__ import annotations

from scripts.commercial_launch_readiness import run_readiness


def test_readiness_is_go():
    report = run_readiness(target=400)
    assert report["pass"] is True, report["failed"]
    assert report["verdict"] == "GO"


def test_readiness_checks_present():
    report = run_readiness(target=400)
    names = {c["check"] for c in report["checks"]}
    assert "five_verticals" in names
    assert "target_met" in names
    assert "mandatory_flags" in names
    assert "safety_audit" in names
