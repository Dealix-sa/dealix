"""CSV → accounts adapter for the Sprint Day-2 DQ baseline.

Loads a customer-supplied CSV into the row-shape expected by ``compute_dq`` and
returns both the deterministic 0-100 Data Quality Score and a small per-row
diagnostic summary (issues per row). No LLM calls. No network. Synthetic-data
safe — never logs row contents.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from auto_client_acquisition.data_os.data_quality_score import (
    DataQualityScore,
    compute_dq,
)

DEFAULT_REQUIRED_KEYS: tuple[str, ...] = ("company_name", "sector", "city")
MAX_ROWS = 10_000


@dataclass(frozen=True, slots=True)
class CsvIntakeReport:
    """Result of loading + scoring a customer CSV for the Sprint Day-2 deliverable."""

    row_count: int
    columns: tuple[str, ...]
    score: DataQualityScore
    issues_per_row: tuple[tuple[int, tuple[str, ...]], ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_count": self.row_count,
            "columns": list(self.columns),
            "score": {
                "overall": self.score.overall,
                "completeness": self.score.completeness,
                "duplicate_inverse": self.score.duplicate_inverse,
                "format_consistency": self.score.format_consistency,
                "source_clarity": self.score.source_clarity,
            },
            "issues_per_row": [
                {"row": idx, "missing": list(missing)} for idx, missing in self.issues_per_row
            ],
        }


def load_accounts_csv(path: str | Path) -> tuple[list[dict[str, Any]], tuple[str, ...]]:
    """Load a CSV into a list of dict rows with normalized string fields.

    Raises FileNotFoundError if the file does not exist and ValueError if the
    file is empty or exceeds MAX_ROWS (synthetic-data-only safety rail).
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))
    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")
        columns = tuple(c.strip() for c in reader.fieldnames if c and c.strip())
        rows: list[dict[str, Any]] = []
        for raw in reader:
            row = {(k or "").strip(): (v.strip() if isinstance(v, str) else v) for k, v in raw.items()}
            rows.append(row)
            if len(rows) > MAX_ROWS:
                raise ValueError(f"CSV exceeds MAX_ROWS={MAX_ROWS}")
    if not rows:
        raise ValueError("CSV has a header but no data rows")
    return rows, columns


def _issues_per_row(
    rows: list[dict[str, Any]],
    required_keys: tuple[str, ...],
) -> tuple[tuple[int, tuple[str, ...]], ...]:
    """Per-row list of missing required keys (1-indexed for human reading)."""
    out: list[tuple[int, tuple[str, ...]]] = []
    for i, row in enumerate(rows, start=1):
        missing: list[str] = []
        for k in required_keys:
            v = row.get(k)
            if v is None:
                missing.append(k)
                continue
            if isinstance(v, str) and not v.strip():
                missing.append(k)
        if missing:
            out.append((i, tuple(missing)))
    return tuple(out)


def score_csv(
    path: str | Path,
    *,
    has_valid_passport: bool = False,
    required_keys: tuple[str, ...] = DEFAULT_REQUIRED_KEYS,
) -> CsvIntakeReport:
    """Sprint Day-2 deliverable: CSV in → ``CsvIntakeReport`` out.

    ``has_valid_passport`` should mirror whether a signed Source Passport exists
    on file (see ``data_os/source_passport.py``); when False, source clarity is
    derived from per-row ``source`` field coverage.
    """
    rows, columns = load_accounts_csv(path)
    score = compute_dq(
        rows,
        columns=list(columns),
        has_valid_passport=has_valid_passport,
        required_keys=required_keys,
    )
    return CsvIntakeReport(
        row_count=len(rows),
        columns=columns,
        score=score,
        issues_per_row=_issues_per_row(rows, required_keys),
    )


__all__ = [
    "CsvIntakeReport",
    "DEFAULT_REQUIRED_KEYS",
    "MAX_ROWS",
    "load_accounts_csv",
    "score_csv",
]
