"""Append-only audit writer.

Writes JSON lines to $DEALIX_PRIVATE_OPS/trust/audit_log.jsonl. Never
overwrites, never edits prior lines. Refuses to write secret values
even if accidentally placed into the payload (best-effort scrub).
"""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Iterable

SECRET_NAME_HINTS: tuple[str, ...] = (
    "TOKEN", "SECRET", "API_KEY", "ACCESS_KEY", "PASSWORD",
    "PRIVATE_KEY", "CLIENT_SECRET",
)


def _root() -> Path:
    root = os.environ.get("DEALIX_PRIVATE_OPS")
    if not root:
        raise RuntimeError("DEALIX_PRIVATE_OPS is not set")
    return Path(root)


def _scrub(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: ("***" if _looks_secret(k) else _scrub(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [_scrub(x) for x in value]
    return value


def _looks_secret(key: str) -> bool:
    up = key.upper()
    return any(h in up for h in SECRET_NAME_HINTS)


def write(event_type: str, payload: dict[str, Any], *, actor: str = "system",
          tags: Iterable[str] = ()) -> str:
    """Append one event and return its event_id."""
    log_dir = _root() / "trust"
    log_dir.mkdir(parents=True, exist_ok=True)
    log = log_dir / "audit_log.jsonl"
    event_id = str(uuid.uuid4())
    line = {
        "id": event_id,
        "ts": int(time.time()),
        "event_type": event_type,
        "actor": actor,
        "tags": list(tags),
        "payload": _scrub(payload),
    }
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    return event_id
