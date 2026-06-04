"""Seed-lead validator accepts the example file and rejects malformed rows."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import commercial_seed_leads_validate as seed  # noqa: E402


def test_example_file_is_valid():
    result = seed.validate()
    assert result["verdict"] == "PASS", result["errors"]
    assert result["rows"] >= 1


def test_example_file_has_no_personal_contact_fields():
    text = seed.SEED_FILE.read_text(encoding="utf-8").lower()
    for forbidden in ('"email"', '"phone"', '"mobile"', '"personal_email"'):
        assert forbidden not in text
