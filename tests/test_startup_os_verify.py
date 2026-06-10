"""Master Startup OS verifier passes once docs/scripts/tests/workflows exist."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import startup_os_verify as sov  # noqa: E402


def test_startup_os_verifies():
    report = sov.verify()
    assert report["decision"] == "PASS", report["critical_failures"]


def test_expected_doc_count_reasonable():
    report = sov.verify()
    assert report["total_docs_expected"] >= 200
    assert report["os_areas"] >= 20
