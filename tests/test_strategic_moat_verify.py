"""V9 test: strategic_moat_verify returns PASS and carries no forbidden-claim violations."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import strategic_moat_verify  # noqa: E402


def test_strategic_moat_verify_passes() -> None:
    report = strategic_moat_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_strategic_moat_verify_no_violations() -> None:
    report = strategic_moat_verify.verify()
    assert report["summary"]["violations"] == []
