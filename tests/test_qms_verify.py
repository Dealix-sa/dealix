"""V9 test: QMS verifier passes and required checklists are present."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import qms_verify  # noqa: E402


def test_qms_passes() -> None:
    report = qms_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_checklist_integrity_clean() -> None:
    report = qms_verify.verify()
    assert report["checklist_integrity"] == []
