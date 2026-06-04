"""V9 test: demo OS verifier passes."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import demo_os_verify  # noqa: E402


def test_demo_os_passes() -> None:
    report = demo_os_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_demo_scenarios_sandbox_only() -> None:
    report = demo_os_verify.verify()
    # the demo_scenarios config must declare sandbox/sample-only safety
    cfg = next(c for c in report["configs"] if c["path"].endswith("demo_scenarios.json"))
    assert cfg["valid_json"]
    assert cfg["missing_keys"] == []
