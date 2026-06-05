"""V9 test: cost control verifier passes and configs hold no secrets."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import cost_control_verify  # noqa: E402


def test_cost_control_passes() -> None:
    report = cost_control_verify.verify()
    assert report["verdict"] == "PASS", report["summary"]


def test_no_secrets_in_configs() -> None:
    report = cost_control_verify.verify()
    assert report["secret_scan"] == []
