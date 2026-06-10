"""Shared safe IO helpers for ops_runtime readers."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


def read_csv_rows(path: Path) -> list[dict]:
    """Return rows from a CSV file, or [] if missing/empty."""
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return [row for row in reader if any((row.get(k) or "").strip() for k in row)]


def sum_int(rows: Iterable[dict], field: str) -> int:
    total = 0
    for row in rows:
        value = (row.get(field) or "").strip()
        if not value:
            continue
        try:
            total += int(float(value))
        except ValueError:
            continue
    return total


def sum_float(rows: Iterable[dict], field: str) -> float:
    total = 0.0
    for row in rows:
        value = (row.get(field) or "").strip()
        if not value:
            continue
        try:
            total += float(value)
        except ValueError:
            continue
    return total


def count_with_value(rows: Iterable[dict], field: str) -> int:
    return sum(1 for row in rows if (row.get(field) or "").strip())


def first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None
