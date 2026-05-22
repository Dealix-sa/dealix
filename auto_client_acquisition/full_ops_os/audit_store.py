"""Append-only JSONL audit store for the Full Ops Sales System.

Every stage transition writes an ``AuditEntry``. The store mirrors the
``value_os/value_ledger.py`` pattern: JSONL file, ``DEALIX_*_PATH`` env
override, ``clear_for_test`` helper.
"""

from __future__ import annotations

import os
from pathlib import Path

from dealix.contracts.audit_log import AuditEntry


def _audit_path() -> Path:
    raw = os.getenv("DEALIX_FULL_OPS_AUDIT_PATH", "data/full_ops_audit.jsonl")
    path = Path(raw)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def record(entry: AuditEntry) -> AuditEntry:
    """Append an audit entry to the log."""
    path = _audit_path()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(entry.model_dump_json())
        handle.write("\n")
    return entry


def list_entries(*, workflow_id: str | None = None, limit: int = 200) -> list[AuditEntry]:
    """Return audit entries, newest first, optionally scoped to a workflow run."""
    path = _audit_path()
    if not path.exists():
        return []
    rows: list[AuditEntry] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                entry = AuditEntry.model_validate_json(line)
            except Exception:  # noqa: BLE001 — skip corrupt lines
                continue
            if workflow_id and entry.workflow_id != workflow_id:
                continue
            rows.append(entry)
    rows.reverse()
    return rows[: max(0, limit)]


def clear_for_test() -> None:
    """Delete the audit log. Test-only."""
    path = _audit_path()
    if path.exists():
        path.unlink()


__all__ = ["record", "list_entries", "clear_for_test"]
