from __future__ import annotations

"""Read raw operational state from the private ops directory.

Every reader returns an empty list when the underlying file or directory is
absent — the private ops repo is allowed to be uninitialised.
"""

import csv
from pathlib import Path
from typing import Any


def _read_csv_dicts(path: Path) -> list[dict[str, Any]]:
    path = Path(path)
    if not path.exists() or not path.is_file():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            return [dict(row) for row in reader]
    except (OSError, csv.Error):
        return []


def read_pipeline(private_ops_path: Path) -> list[dict[str, Any]]:
    """Read `pipeline/pipeline_tracker.csv`."""
    return _read_csv_dicts(Path(private_ops_path) / "pipeline" / "pipeline_tracker.csv")


def read_revenue_actions(private_ops_path: Path) -> list[dict[str, Any]]:
    """Read `revenue/revenue_action_log.csv`."""
    return _read_csv_dicts(
        Path(private_ops_path) / "revenue" / "revenue_action_log.csv"
    )


def read_mrr(private_ops_path: Path) -> list[dict[str, Any]]:
    """Read `revenue/mrr_tracker.csv`."""
    return _read_csv_dicts(Path(private_ops_path) / "revenue" / "mrr_tracker.csv")


def read_clients(private_ops_path: Path) -> list[Path]:
    """Return subdirectories of `clients/` — one per client."""
    base = Path(private_ops_path) / "clients"
    if not base.exists() or not base.is_dir():
        return []
    return sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith("."))
