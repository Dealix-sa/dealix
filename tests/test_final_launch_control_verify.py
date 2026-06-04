"""Tests for the Final Launch Control verifier (V7)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_final_launch_control_passes() -> None:
    mod = _load("final_launch_control_verify")
    result = mod.verify()
    assert result["status"] == "PASS", result
    assert all(result["checks"].values())


def test_no_go_items_enforced() -> None:
    mod = _load("final_launch_control_verify")
    result = mod.verify()
    for forbidden in ("LinkedIn automation", "bulk email", "fake traction"):
        assert forbidden in result["no_go_items"]
