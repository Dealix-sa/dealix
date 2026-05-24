"""Read snapshots from the private ops workspace.

The workspace path is configured via DEALIX_PRIVATE_OPS (defaults to
/opt/dealix-ops-private). We read CSVs and MD files only — never write
without going through the policy adapter.
"""
from __future__ import annotations

import csv
import datetime
import os
from pathlib import Path

PRIVATE_OPS_ENV = "DEALIX_PRIVATE_OPS"
DEFAULT_PRIVATE_OPS = "/opt/dealix-ops-private"


def workspace_root() -> Path:
    return Path(os.environ.get(PRIVATE_OPS_ENV, DEFAULT_PRIVATE_OPS))


def read_csv(rel_path: str, limit: int | None = 50) -> dict:
    root = workspace_root()
    path = root / rel_path
    if not path.exists():
        return {
            "source": "missing_workspace_file",
            "freshness_iso": datetime.datetime.utcnow().isoformat(timespec="seconds"),
            "data": {"rel_path": rel_path, "rows": []},
        }
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader):
            if limit is not None and i >= limit:
                break
            rows.append(row)
    stat = path.stat()
    return {
        "source": str(path),
        "freshness_iso": datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
        "data": {"rel_path": rel_path, "rows": rows},
    }


def read_markdown(rel_path: str) -> dict:
    root = workspace_root()
    path = root / rel_path
    if not path.exists():
        return {
            "source": "missing_workspace_file",
            "freshness_iso": datetime.datetime.utcnow().isoformat(timespec="seconds"),
            "data": {"rel_path": rel_path, "markdown": ""},
        }
    text = path.read_text(encoding="utf-8")
    stat = path.stat()
    return {
        "source": str(path),
        "freshness_iso": datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
        "data": {"rel_path": rel_path, "markdown": text},
    }
