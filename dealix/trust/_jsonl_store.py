"""خادم الثقة — JSONL persistence helper.

A small, generic, atomic JSON-lines store used by the Trust plane (e.g.
ApprovalQueue, EvidenceStore) when callers want disk-backed durability
instead of pure in-memory state.

Design notes:
  * append-only on the hot path (append a single dict line, fsync the
    parent dir lazily via the OS — we don't fsync per write).
  * `replace_all` is atomic via temp-file + os.replace.
  * `load_all` skips malformed lines silently so a partial line cannot
    bring down boot; the caller is expected to be defensive too.
  * `safe_open(path)` returns None if the parent directory cannot be
    written (read-only FS, sandboxed CI, ...). Callers fall back to
    in-memory state in that case.
"""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any


class JsonlStore:
    """Append-only JSON-lines store with atomic full-rewrite support."""

    def __init__(self, path: Path | str) -> None:
        self._path = Path(path)

    @property
    def path(self) -> Path:
        return self._path

    def exists(self) -> bool:
        return self._path.exists()

    def ensure_parent(self) -> bool:
        """Create the parent directory; return False on failure (e.g. RO FS)."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            return True
        except OSError:
            return False

    # ── writes ────────────────────────────────────────────────────
    def append(self, obj: dict[str, Any]) -> None:
        if not self.ensure_parent():
            raise OSError(f"cannot create parent for {self._path}")
        line = json.dumps(obj, ensure_ascii=False, default=str)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(line)
            handle.write("\n")

    def replace_all(self, records: list[dict[str, Any]]) -> None:
        """Atomically rewrite the whole file with the supplied records."""
        if not self.ensure_parent():
            raise OSError(f"cannot create parent for {self._path}")
        # Temp file in the same directory ensures os.replace is atomic
        # (cross-device renames raise EXDEV otherwise).
        fd, tmp_name = tempfile.mkstemp(
            prefix=self._path.name + ".",
            suffix=".tmp",
            dir=str(self._path.parent),
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                for record in records:
                    handle.write(json.dumps(record, ensure_ascii=False, default=str))
                    handle.write("\n")
            os.replace(tmp_name, self._path)
        except Exception:
            # Best effort cleanup of the temp file.
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise

    # ── reads ─────────────────────────────────────────────────────
    def load_all(self) -> Iterator[dict[str, Any]]:
        """Yield each parseable record. Malformed lines are skipped."""
        if not self._path.exists():
            return
        with self._path.open("r", encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    # Partial / corrupt line — skip rather than abort load.
                    continue
                if isinstance(record, dict):
                    yield record

    def load_list(self) -> list[dict[str, Any]]:
        return list(self.load_all())


__all__ = ["JsonlStore"]
