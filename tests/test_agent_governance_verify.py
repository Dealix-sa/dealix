"""V9 test: agent_governance_verify returns PASS and carries no forbidden-claim violations."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import agent_governance_verify  # noqa: E402


def test_agent_governance_verify_passes() -> None:
    report = agent_governance_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_agent_governance_verify_no_violations() -> None:
    report = agent_governance_verify.verify()
    assert report["summary"]["violations"] == []
