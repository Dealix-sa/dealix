"""Read-only runtime reader for the private ops CSV layout.

Looks up CSVs under PRIVATE_OPS_ROOT (default /opt/dealix-ops-private).
Returns empty lists / Nones when the runtime is not bootstrapped — internal
API routes treat that as a fallback condition and the founder console renders
'source=fallback' UI.
"""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

PRIVATE_OPS_ROOT_ENV = "PRIVATE_OPS_ROOT"
DEFAULT_PRIVATE_OPS_ROOT = "/opt/dealix-ops-private"


def private_ops_root() -> Path:
    return Path(os.environ.get(PRIVATE_OPS_ROOT_ENV, DEFAULT_PRIVATE_OPS_ROOT))


@dataclass(frozen=True)
class RuntimeFile:
    path: Path
    exists: bool


def runtime_path(*parts: str) -> RuntimeFile:
    path = private_ops_root().joinpath(*parts)
    return RuntimeFile(path=path, exists=path.exists())


def read_csv(*parts: str) -> list[dict[str, Any]]:
    rf = runtime_path(*parts)
    if not rf.exists:
        return []
    try:
        with rf.path.open("r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            return [dict(row) for row in reader]
    except OSError:
        return []


def iter_csv(*parts: str) -> Iterable[dict[str, Any]]:
    rf = runtime_path(*parts)
    if not rf.exists:
        return
    try:
        with rf.path.open("r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                yield dict(row)
    except OSError:
        return


def count_csv(*parts: str, where: callable | None = None) -> int:  # type: ignore[type-arg]
    n = 0
    for row in iter_csv(*parts):
        if where is None or where(row):
            n += 1
    return n


def first_csv(*parts: str) -> dict[str, Any] | None:
    for row in iter_csv(*parts):
        return row
    return None
