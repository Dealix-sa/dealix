"""V9 test: deployment_static_verify returns PASS and carries no forbidden-claim violations."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import deployment_static_verify  # noqa: E402


def test_deployment_static_verify_passes() -> None:
    report = deployment_static_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_deployment_static_verify_no_violations() -> None:
    report = deployment_static_verify.verify()
    assert report["summary"]["violations"] == []
