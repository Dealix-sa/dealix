"""Shared helpers for internal launch/risk/finance/learning endpoints.

All readers operate on <private_ops>/ when configured, otherwise return
a fallback envelope so the UI can still render with `source: "fallback"`.

No external calls. No mutations. No secrets surfaced.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from typing import Any


def private_ops_dir() -> Path | None:
    """Return Path to private ops tree if configured + present, else None."""
    raw = os.environ.get("DEALIX_PRIVATE_OPS") or os.environ.get("PRIVATE_OPS")
    if not raw:
        return None
    p = Path(raw).expanduser()
    try:
        return p.resolve() if p.exists() else None
    except OSError:  # pragma: no cover
        return None


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    except (OSError, csv.Error):  # pragma: no cover
        return []


def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):  # pragma: no cover
        return None


def read_text(path: Path, limit_kb: int = 64) -> str | None:
    if not path.exists():
        return None
    try:
        data = path.read_text(encoding="utf-8")
        if len(data) > limit_kb * 1024:
            return data[: limit_kb * 1024] + "\n…[truncated]"
        return data
    except OSError:  # pragma: no cover
        return None


def fallback_envelope(reason: str) -> dict[str, Any]:
    return {
        "source": "fallback",
        "reason": reason,
        "note": "Configure DEALIX_PRIVATE_OPS to enable live data.",
    }
