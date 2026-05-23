"""Read CSV-shaped private ops runtime files.

The private ops runtime lives outside the repo (see
docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md). When PRIVATE_OPS or
DEALIX_PRIVATE_OPS_DIR is set, we read from there. Otherwise we return
empty structures with `source: "no-runtime"` so the UI can degrade
gracefully without crashing.
"""
from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class RuntimeRead:
    rows: list[dict[str, str]]
    source: str  # "csv" | "missing" | "no-runtime"
    path: str | None


def _runtime_dir() -> Path | None:
    raw = os.getenv("DEALIX_PRIVATE_OPS_DIR") or os.getenv("PRIVATE_OPS")
    if not raw:
        return None
    p = Path(raw).expanduser()
    return p


def read_csv(rel_path: str, limit: int | None = 200) -> RuntimeRead:
    base = _runtime_dir()
    if base is None:
        return RuntimeRead(rows=[], source="no-runtime", path=None)
    full = base / rel_path
    if not full.exists():
        return RuntimeRead(rows=[], source="missing", path=str(full))
    rows: list[dict[str, str]] = []
    with full.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader):
            if limit is not None and i >= limit:
                break
            rows.append({k: (v or "") for k, v in row.items()})
    return RuntimeRead(rows=rows, source="csv", path=str(full))


def list_csv_files(rel_dir: str) -> Iterable[str]:
    base = _runtime_dir()
    if base is None:
        return []
    full = base / rel_dir
    if not full.exists():
        return []
    return sorted(p.name for p in full.iterdir() if p.suffix.lower() == ".csv")
