"""V9 test: procurement_verify returns PASS and carries no forbidden-claim violations."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import procurement_verify  # noqa: E402


def test_procurement_verify_passes() -> None:
    report = procurement_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_procurement_verify_no_violations() -> None:
    report = procurement_verify.verify()
    assert report["summary"]["violations"] == []
