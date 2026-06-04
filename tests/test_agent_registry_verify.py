"""V9 test: agent registry structure and boundaries."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import agent_registry_verify  # noqa: E402


def test_agent_registry_passes() -> None:
    report = agent_registry_verify.verify()
    assert report["verdict"] == "PASS", report["problems"]


def test_all_expected_agents_present() -> None:
    report = agent_registry_verify.verify()
    assert report["agent_count"] >= len(agent_registry_verify.EXPECTED_AGENTS)
    assert report["problems"] == []
