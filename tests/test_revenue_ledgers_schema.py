"""Test that revenue ledger CSVs exist and match LEDGER_SCHEMAS headers.

Validates that every ledger defined in ``scripts.revenue._lib.LEDGER_SCHEMAS``
has a corresponding ``ledgers/<name>.csv`` file with the correct header row.

Usage:
    python -m pytest tests/test_revenue_ledgers_schema.py -q
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.revenue._lib import LEDGER_SCHEMAS


def _read_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or [])


def test_all_schema_ledgers_have_csv_files() -> None:
    for name in LEDGER_SCHEMAS:
        path = REPO_ROOT / "ledgers" / f"{name}.csv"
        assert path.exists(), f"Missing ledger file: {path}"


def test_ledger_csv_headers_match_schema() -> None:
    for name, expected_fields in LEDGER_SCHEMAS.items():
        path = REPO_ROOT / "ledgers" / f"{name}.csv"
        assert path.exists(), f"Missing ledger file: {path}"
        actual = _read_header(path)
        assert actual == expected_fields, (
            f"Header mismatch for {name}.csv:\n"
            f"  expected: {expected_fields}\n"
            f"  actual:   {actual}"
        )


def test_source_url_in_prospects_schema() -> None:
    assert "source_url" in LEDGER_SCHEMAS["prospects"]


def test_source_url_in_proposal_log_schema() -> None:
    assert "source_url" in LEDGER_SCHEMAS["proposal_log"]


def test_source_url_in_clients_schema() -> None:
    assert "source_url" in LEDGER_SCHEMAS["clients"]
