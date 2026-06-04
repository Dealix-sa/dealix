"""V9 test: trust_center_verify returns PASS and carries no forbidden-claim violations."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import trust_center_verify  # noqa: E402


def test_trust_center_verify_passes() -> None:
    report = trust_center_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_trust_center_verify_no_violations() -> None:
    report = trust_center_verify.verify()
    assert report["summary"]["violations"] == []
