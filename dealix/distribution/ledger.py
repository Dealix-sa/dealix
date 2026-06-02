"""Append-only JSONL ledgers for distribution records (drafts, proposals, ...).

Each record type lives in its own ``.jsonl`` file under ``data/`` (gitignored
runtime state). Helpers here keep the ledgers consistent: stable ``id``,
``created_at`` / ``updated_at`` stamps, id-based upsert for status transitions,
and PII-safe display (reusing the repo's canonical log redaction).
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:  # canonical PII/secret redaction (best-effort — never hard-fail on import)
    from auto_client_acquisition.security_privacy.log_redaction import (
        redact_log_entry as _redact_log_entry,
    )
except Exception:  # pragma: no cover - redaction is defense in depth

    def _redact_log_entry(entry: Any) -> Any:  # type: ignore[misc]
        return entry


def now_iso() -> str:
    """UTC ISO-8601 timestamp."""
    return datetime.now(UTC).isoformat()


def new_id(prefix: str) -> str:
    """Short, unique, human-scannable id, e.g. ``draft_a1b2c3d4``."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def read_records(path: Path) -> list[dict[str, Any]]:
    """Read all JSON objects from a ``.jsonl`` ledger (missing file → [])."""
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out


def append_record(path: Path, record: dict[str, Any]) -> dict[str, Any]:
    """Append one record (filling ``id`` / ``created_at`` if absent)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    record.setdefault("id", new_id("rec"))
    record.setdefault("created_at", now_iso())
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def write_all(path: Path, records: list[dict[str, Any]]) -> None:
    """Rewrite the whole ledger (used by upsert / status transitions)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(r, ensure_ascii=False) for r in records]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def upsert_record(path: Path, record: dict[str, Any], *, key: str = "id") -> dict[str, Any]:
    """Insert or replace by ``key`` (sets ``updated_at`` on replace)."""
    records = read_records(path)
    rid = record.get(key)
    record.setdefault("created_at", now_iso())
    for i, existing in enumerate(records):
        if existing.get(key) == rid and rid is not None:
            record["updated_at"] = now_iso()
            records[i] = {**existing, **record}
            write_all(path, records)
            return records[i]
    record.setdefault("id", new_id("rec"))
    records.append(record)
    write_all(path, records)
    return record


def update_status(
    path: Path, record_id: str, status: str, *, key: str = "id", **extra: Any
) -> dict[str, Any] | None:
    """Transition a record's ``status`` (and optional extra fields) by id."""
    records = read_records(path)
    hit: dict[str, Any] | None = None
    for rec in records:
        if rec.get(key) == record_id:
            rec["status"] = status
            rec["updated_at"] = now_iso()
            for k, v in extra.items():
                rec[k] = v
            hit = rec
            break
    if hit is not None:
        write_all(path, records)
    return hit


def latest_by_key(records: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    """Keep only the most recent record per ``key`` (last write wins)."""
    seen: dict[Any, dict[str, Any]] = {}
    for rec in records:
        seen[rec.get(key)] = rec
    return list(seen.values())


def redact_for_display(value: Any) -> Any:
    """PII/secret-safe view of a record for reports / stdout / API."""
    return _redact_log_entry(value)


__all__ = [
    "append_record",
    "latest_by_key",
    "new_id",
    "now_iso",
    "read_records",
    "redact_for_display",
    "update_status",
    "upsert_record",
    "write_all",
]
