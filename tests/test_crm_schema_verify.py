"""CRM pipeline schema verifies as send-free with all required stages."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import commercial_crm_schema_verify as csv_  # noqa: E402


def test_schema_verifies():
    assert csv_.verify() == []


def test_required_stages_complete():
    assert "suppressed" in csv_.REQUIRED_STAGES
    assert "founder_review" in csv_.REQUIRED_STAGES
