"""Sprint store — durable JSON-Lines snapshots of 7-day sprint runs.

The orchestrator (`dealix.commercial.sprint_orchestrator`) is stateless: it runs
one day at a time as a pure function. The executor needs to remember state
*between* days (and across processes / restarts). This store provides that with
the same file-store pattern as `lead_inbox` / `draft_queue`:

- File: $DEALIX_SPRINT_STORE_PATH (default: var/sprint-runs.jsonl), append-only.
- Each change appends a full state snapshot; `get` returns the latest snapshot
  for an engagement, so the log doubles as an audit trail.
- `var/` is gitignored — no engagement state leaks into the repo.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_DEFAULT_PATH = "var/sprint-runs.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_SPRINT_STORE_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def save(state: dict[str, Any]) -> dict[str, Any]:
    """Append a full state snapshot. `state` must carry `engagement_id`."""
    if not state.get("engagement_id"):
        raise ValueError("state requires engagement_id")
    snap = {**state, "_saved_at": datetime.now(UTC).isoformat()}
    try:
        path = _path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with _lock, path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(snap, ensure_ascii=False) + "\n")
        snap["persisted"] = True
    except Exception:
        snap["persisted"] = False
    return snap


def _latest() -> dict[str, dict[str, Any]]:
    path = _path()
    if not path.exists():
        return {}
    out: dict[str, dict[str, Any]] = {}
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                eid = rec.get("engagement_id")
                if eid:
                    out[eid] = rec  # last write wins
    except Exception:
        return {}
    return out


def get(engagement_id: str) -> dict[str, Any] | None:
    return _latest().get(engagement_id)


def list_runs(limit: int = 100, status: str | None = None) -> list[dict[str, Any]]:
    runs = list(_latest().values())
    if status:
        runs = [r for r in runs if r.get("status") == status]
    runs.sort(key=lambda r: r.get("_saved_at", ""), reverse=True)
    return runs[:limit]


__all__ = ["save", "get", "list_runs"]
