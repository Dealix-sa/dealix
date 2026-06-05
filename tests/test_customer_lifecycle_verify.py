"""V9 test: customer lifecycle verifier and stage integrity."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import customer_lifecycle_verify  # noqa: E402


def test_customer_lifecycle_passes() -> None:
    report = customer_lifecycle_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_stage_integrity_clean() -> None:
    report = customer_lifecycle_verify.verify()
    assert report["stage_integrity"] == []


def test_no_violations() -> None:
    report = customer_lifecycle_verify.verify()
    assert report["summary"]["violations"] == []
