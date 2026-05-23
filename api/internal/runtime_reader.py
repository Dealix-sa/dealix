"""
Read-only CSV reader for the private Dealix ops root.

The private ops root path is taken from DEALIX_PRIVATE_OPS_ROOT
(default /opt/dealix-ops-private). Every helper returns
{"rows": [...], "source": "csv"|"fallback"} and never raises on missing
files — it falls back to an empty list so the dashboard stays useful.
"""

from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Any


def private_ops_root() -> Path:
    return Path(os.getenv("DEALIX_PRIVATE_OPS_ROOT", "/opt/dealix-ops-private"))


def read_csv_rows(relative_path: str) -> dict[str, Any]:
    """Read all rows from a CSV file inside the private ops root.

    Returns {"rows": [...], "source": "csv"|"fallback", "path": <str>}.
    Returns an empty list and source='fallback' when the file is missing.
    """
    full = private_ops_root() / relative_path
    if not full.exists() or not full.is_file():
        return {"rows": [], "source": "fallback", "path": str(full)}
    rows: list[dict[str, str]] = []
    try:
        with full.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rows.append({k: (v or "") for k, v in row.items()})
    except Exception as exc:  # noqa: BLE001 — return safely
        return {"rows": [], "source": "fallback", "path": str(full), "error": str(exc)}
    return {"rows": rows, "source": "csv", "path": str(full)}


def append_csv_row(relative_path: str, row: dict[str, str]) -> dict[str, Any]:
    """Append a single row to a CSV file inside the private ops root.

    Creates the file (with header) if it does not exist. Returns
    {"ok": bool, "path": <str>, "error"?: str}.
    The private ops root is created on demand.
    """
    full = private_ops_root() / relative_path
    try:
        full.parent.mkdir(parents=True, exist_ok=True)
        file_exists = full.exists()
        with full.open("a", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(row.keys()))
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "path": str(full), "error": str(exc)}
    return {"ok": True, "path": str(full)}
