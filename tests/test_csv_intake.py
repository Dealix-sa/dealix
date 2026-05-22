"""Tests for Sprint Day-2 CSV intake (data_os.csv_intake)."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_client_acquisition.data_os.csv_intake import (
    CsvIntakeReport,
    MAX_ROWS,
    load_accounts_csv,
    score_csv,
)

HEADER = "company_name,sector,city,source\n"


def _write(tmp_path: Path, body: str, name: str = "accounts.csv") -> Path:
    p = tmp_path / name
    p.write_text(HEADER + body, encoding="utf-8")
    return p


def test_load_accounts_csv_parses_rows_and_columns(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "Acme,fintech,Riyadh,crm_export\n"
        "Beta,health,Jeddah,crm_export\n",
    )
    rows, columns = load_accounts_csv(p)
    assert columns == ("company_name", "sector", "city", "source")
    assert len(rows) == 2
    assert rows[0]["company_name"] == "Acme"
    assert rows[1]["sector"] == "health"


def test_load_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_accounts_csv(tmp_path / "nope.csv")


def test_load_header_only_rejected(tmp_path: Path) -> None:
    p = tmp_path / "empty.csv"
    p.write_text(HEADER, encoding="utf-8")
    with pytest.raises(ValueError):
        load_accounts_csv(p)


def test_score_clean_csv_is_high(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "Acme,fintech,Riyadh,crm_export\n"
        "Beta,health,Jeddah,crm_export\n"
        "Gamma,logistics,Dammam,crm_export\n",
    )
    report = score_csv(p, has_valid_passport=True)
    assert isinstance(report, CsvIntakeReport)
    assert report.row_count == 3
    assert report.score.overall >= 95.0  # clean, unique, complete, source via passport
    assert report.score.completeness == 100.0
    assert report.score.duplicate_inverse == 100.0
    assert report.score.source_clarity == 100.0
    assert report.issues_per_row == ()


def test_score_csv_with_missing_fields_records_issues(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "Acme,fintech,Riyadh,crm_export\n"
        "Beta,,Jeddah,crm_export\n"  # missing sector
        ",health,Dammam,crm_export\n",  # missing company_name
    )
    report = score_csv(p, has_valid_passport=True)
    assert report.row_count == 3
    assert report.score.completeness < 100.0
    issue_rows = {idx: missing for idx, missing in report.issues_per_row}
    assert issue_rows[2] == ("sector",)
    assert issue_rows[3] == ("company_name",)


def test_score_csv_detects_duplicates(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "Acme,fintech,Riyadh,crm_export\n"
        "acme ,fintech,Riyadh,crm_export\n"  # case + whitespace dup
        "Beta,health,Jeddah,crm_export\n",
    )
    report = score_csv(p, has_valid_passport=True)
    assert report.score.duplicate_inverse < 100.0


def test_score_csv_to_dict_is_serializable(tmp_path: Path) -> None:
    p = _write(tmp_path, "Acme,fintech,Riyadh,crm_export\n")
    payload = score_csv(p, has_valid_passport=True).to_dict()
    assert payload["row_count"] == 1
    assert payload["columns"] == ["company_name", "sector", "city", "source"]
    assert payload["score"]["overall"] > 0.0


def test_load_rejects_csv_above_max_rows(tmp_path: Path) -> None:
    body = "Acme,fintech,Riyadh,crm_export\n" * (MAX_ROWS + 1)
    p = _write(tmp_path, body)
    with pytest.raises(ValueError, match="MAX_ROWS"):
        load_accounts_csv(p)
