"""Test that prospects require a source_url — no source, no entry.

Validates that validate_targets.py rejects prospects without source_url
and that the prospects CSV schema includes source_url as a required column.

Usage:
    python -m pytest tests/test_prospects_require_source_url.py -q
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.revenue._lib import LEDGER_SCHEMAS
from scripts.revenue.validate_targets import validate_rows


def test_prospects_schema_includes_source_url() -> None:
    fields = LEDGER_SCHEMAS["prospects"]
    assert "source_url" in fields, "prospects schema must include source_url"


def test_validate_rejects_missing_source_url() -> None:
    rows = [
        {"company_name": "Test Co", "sector": "logistics", "city": "Riyadh",
         "source_url": "", "verification_status": "placeholder", "confidence": "0.5"},
    ]
    issues, valid = validate_rows(rows)
    assert len(issues) > 0, "Should reject row with empty source_url"
    assert any("source_url" in i for i in issues), f"Should mention source_url in issues: {issues}"
    assert len(valid) == 0, "No valid rows should be returned"


def test_validate_rejects_non_http_source_url() -> None:
    rows = [
        {"company_name": "Test Co", "sector": "logistics", "city": "Riyadh",
         "source_url": "not-a-url", "verification_status": "placeholder", "confidence": "0.5"},
    ]
    issues, valid = validate_rows(rows)
    assert len(issues) > 0, "Should reject non-http source_url"
    assert any("http" in i for i in issues), f"Should mention http requirement: {issues}"
    assert len(valid) == 0


def test_validate_accepts_valid_source_url() -> None:
    rows = [
        {"company_name": "Test Co", "sector": "logistics", "city": "Riyadh",
         "source_url": "https://example.com/about", "verification_status": "placeholder",
         "confidence": "0.5"},
    ]
    issues, valid = validate_rows(rows)
    assert len(issues) == 0, f"Should accept valid row, got issues: {issues}"
    assert len(valid) == 1


def test_validate_rejects_empty_prospects() -> None:
    issues, valid = validate_rows([])
    assert len(issues) > 0, "Should reject empty prospects list"
    assert len(valid) == 0


def test_seed_demo_data_has_source_urls() -> None:
    """Verify all demo prospects include a valid source_url."""
    from scripts.revenue.seed_demo_revenue_data import DEMO_PROSPECTS
    for prospect in DEMO_PROSPECTS:
        source = prospect.get("source_url", "")
        assert source.startswith("http"), (
            f"Demo prospect {prospect.get('company_name')} missing valid source_url: {source}"
        )


def test_prospects_csv_header_has_source_url() -> None:
    prospects_path = REPO_ROOT / "ledgers" / "prospects.csv"
    with prospects_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames is not None
        assert "source_url" in reader.fieldnames, "prospects.csv header must have source_url"