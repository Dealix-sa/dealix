"""V9 test: documentation governance verifier passes."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import docs_governance_verify  # noqa: E402


def test_docs_governance_passes() -> None:
    report = docs_governance_verify.verify()
    assert report["verdict"] == "PASS", report["governance_checks"]


def test_no_stale_brand_or_missing_refs() -> None:
    report = docs_governance_verify.verify()
    assert report["governance_checks"] == []
