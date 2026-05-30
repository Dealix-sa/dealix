"""Custom Systems OS — JSONL engagement ledger. Tenant-scoped via customer_id.

Mirrors the ``friction_log``/``capital_ledger`` pattern: append-only JSONL with
a ``DEALIX_CUSTOM_SYSTEMS_PATH`` override and a threading lock. No DB, no
Alembic migration.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import UTC, datetime
from pathlib import Path

from auto_client_acquisition.custom_systems_os.schemas import CustomSystemRecord

_DEFAULT_PATH = "var/custom-systems-os.jsonl"
_lock = threading.Lock()

_TUPLE_FIELDS = ("capital_asset_ids", "spec_written_files")


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_CUSTOM_SYSTEMS_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def record_engagement(*, record: CustomSystemRecord) -> CustomSystemRecord:
    if not record.customer_id:
        raise ValueError("customer_id is required")
    if not record.engagement_id:
        raise ValueError("engagement_id is required")
    stored = record
    if not record.created_at:
        stored = CustomSystemRecord(
            **{**record.to_dict(), "created_at": datetime.now(UTC).isoformat()}
        )
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(stored.to_dict(), ensure_ascii=False) + "\n")
    return stored


def list_engagements(
    *,
    customer_id: str | None = None,
    limit: int = 200,
) -> list[CustomSystemRecord]:
    path = _path()
    if not path.exists():
        return []
    out: list[CustomSystemRecord] = []
    with _lock, path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                for key in _TUPLE_FIELDS:
                    if key in data and isinstance(data[key], list):
                        data[key] = tuple(data[key])
                record = CustomSystemRecord(**data)
            except Exception:  # noqa: S112 — skip a malformed JSONL line, keep reading
                continue
            if customer_id is not None and record.customer_id != customer_id:
                continue
            out.append(record)
    return out[-limit:] if limit else out


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = ["clear_for_test", "list_engagements", "record_engagement"]
