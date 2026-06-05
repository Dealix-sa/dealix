"""V9 test: enterprise_readiness_verify returns PASS and carries no forbidden-claim violations."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import enterprise_readiness_verify  # noqa: E402


def test_enterprise_readiness_verify_passes() -> None:
    report = enterprise_readiness_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_enterprise_readiness_verify_no_violations() -> None:
    report = enterprise_readiness_verify.verify()
    assert report["summary"]["violations"] == []
