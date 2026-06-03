"""Shared append-only JSONL store for ``distribution_os`` entities.

Mirrors the JSONL pattern used by ``value_os.value_ledger``,
``friction_log.store`` and ``payment_ops.renewal_scheduler``: each store is
keyed by an environment variable with a ``var/<name>.jsonl`` default, and
relative paths resolve against the repository root. Live operational data is
written to ``var/`` (git-ignored); tests point the env var at a temp file.
"""

from __future__ import annotations

import json
import os
import threading
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]


def now_iso() -> str:
    """UTC timestamp in ISO-8601 — the canonical ``created_at`` format."""
    return datetime.now(UTC).isoformat()


class JsonlStore:
    """Thread-safe, append-with-last-write-wins JSONL record store."""

    def __init__(self, *, env_var: str, default_rel: str, id_field: str) -> None:
        self._env_var = env_var
        self._default_rel = default_rel
        self._id_field = id_field
        self._lock = threading.Lock()

    def path(self) -> Path:
        raw = os.environ.get(self._env_var, self._default_rel)
        p = Path(raw)
        if not p.is_absolute():
            p = _REPO_ROOT / p
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def append(self, record: dict[str, Any]) -> dict[str, Any]:
        p = self.path()
        with self._lock, p.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def list(
        self, *, predicate: Callable[[dict[str, Any]], bool] | None = None
    ) -> list[dict[str, Any]]:
        p = self.path()
        if not p.exists():
            return []
        out: list[dict[str, Any]] = []
        with self._lock, p.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                # skip a malformed JSONL line, do not crash the store
                try:
                    rec = json.loads(line)
                except Exception:  # noqa: S112
                    continue
                if predicate is None or predicate(rec):
                    out.append(rec)
        return out

    def get(self, record_id: str) -> dict[str, Any] | None:
        match: dict[str, Any] | None = None
        for rec in self.list():
            if str(rec.get(self._id_field)) == str(record_id):
                match = rec  # last write wins
        return match

    def patch(self, record_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        p = self.path()
        if not p.exists():
            return None
        with self._lock:
            lines = p.read_text(encoding="utf-8").splitlines()
            out_lines: list[str] = []
            updated: dict[str, Any] | None = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    out_lines.append(line)
                    continue
                if str(rec.get(self._id_field)) == str(record_id):
                    rec.update(patch)
                    updated = rec
                out_lines.append(json.dumps(rec, ensure_ascii=False))
            if updated is None:
                return None
            p.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        return updated

    def clear_for_test(self) -> None:
        p = self.path()
        if p.exists():
            with self._lock:
                p.write_text("", encoding="utf-8")


__all__ = ["JsonlStore", "now_iso"]
