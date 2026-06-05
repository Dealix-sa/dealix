"""V9 test: data_room_verify returns PASS and carries no forbidden-claim violations."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import data_room_verify  # noqa: E402


def test_data_room_verify_passes() -> None:
    report = data_room_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_data_room_verify_no_violations() -> None:
    report = data_room_verify.verify()
    assert report["summary"]["violations"] == []
