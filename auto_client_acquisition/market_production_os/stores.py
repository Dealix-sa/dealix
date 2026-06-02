"""JSONL stores for the Market Production OS.

Mirrors the repo store convention (see ``value_os/value_ledger.py``):
append-only JSONL, path overridable via a ``DEALIX_*_PATH`` env var,
default under ``data/market_production_os/`` (gitignored runtime data).

These stores hold operational records only. No PII belongs in logs; the
reply store keeps classification + routing, not raw correspondence beyond
what the founder explicitly records.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

_DEFAULT_DIR = "data/market_production_os"

_ENV_BY_NAME: dict[str, str] = {
    "prospects": "DEALIX_PROSPECTS_PATH",
    "drafts": "DEALIX_OUTREACH_DRAFTS_PATH",
    "signals": "DEALIX_SIGNALS_PATH",
    "replies": "DEALIX_REPLIES_PATH",
    "suppression": "DEALIX_SUPPRESSION_PATH",
    "sending_batches": "DEALIX_SENDING_BATCHES_PATH",
    "approval_actions": "DEALIX_APPROVAL_ACTIONS_PATH",
}


def store_path(name: str) -> Path:
    if name not in _ENV_BY_NAME:
        raise KeyError(f"unknown store: {name}")
    raw = os.getenv(_ENV_BY_NAME[name], f"{_DEFAULT_DIR}/{name}.jsonl")
    path = Path(raw)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _to_dict(record: Any) -> dict[str, Any]:
    if hasattr(record, "to_dict"):
        return record.to_dict()  # type: ignore[no-any-return]
    if is_dataclass(record) and not isinstance(record, type):
        return asdict(record)
    if isinstance(record, dict):
        return record
    raise TypeError(f"cannot serialize record of type {type(record)!r}")


def append(name: str, record: Any) -> None:
    path = store_path(name)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(_to_dict(record), ensure_ascii=False))
        handle.write("\n")


def append_many(name: str, records: list[Any]) -> int:
    path = store_path(name)
    count = 0
    with path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(_to_dict(record), ensure_ascii=False))
            handle.write("\n")
            count += 1
    return count


def read_all(name: str) -> list[dict[str, Any]]:
    path = store_path(name)
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def load_suppression() -> set[str]:
    """Return the set of suppressed emails (lowercased)."""
    return {
        str(row.get("email", "")).strip().lower()
        for row in read_all("suppression")
        if row.get("email")
    }


def clear_for_test(name: str) -> None:
    path = store_path(name)
    if path.exists():
        path.unlink()


__all__ = [
    "append",
    "append_many",
    "clear_for_test",
    "load_suppression",
    "read_all",
    "store_path",
]
