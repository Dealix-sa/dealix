"""Client-workspace ledger helpers (V13 client portal).

Deterministic JSON store wrapping ``business/_data/client_workspaces.json``.
A workspace is created from a won deal and tracks deliverables, approvals,
risks and proof items. Demo-safe — no external calls, no auto-send.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
STORE_PATH = REPO_ROOT / "business" / "_data" / "client_workspaces.json"

_ID_RE = re.compile(r"(\d+)\s*$")


def now_iso() -> str:
    """UTC ISO-8601 timestamp (seconds precision)."""
    return _dt.datetime.now(tz=_dt.timezone.utc).isoformat(timespec="seconds")


def load() -> dict[str, Any]:
    """Load the workspace store, tolerating a missing/empty file."""
    if not STORE_PATH.exists():
        return {"version": 1, "demo": True, "workspaces": []}
    data = json.loads(STORE_PATH.read_text(encoding="utf-8"))
    data.setdefault("workspaces", [])
    return data


def save(data: dict[str, Any]) -> None:
    """Persist the workspace store (pretty-printed, UTF-8, Arabic-safe)."""
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def find(workspaces: list[dict[str, Any]], client_id: str) -> dict[str, Any] | None:
    """Return the workspace whose ``clientId`` matches, else ``None``."""
    for ws in workspaces:
        if str(ws.get("clientId")) == str(client_id):
            return ws
    return None


def next_id(prefix: str, items: list[dict[str, Any]]) -> str:
    """Return the next ``PREFIX-NNN`` id given existing items."""
    highest = 0
    for it in items:
        raw = str(it.get("id", ""))
        m = _ID_RE.search(raw)
        if m:
            highest = max(highest, int(m.group(1)))
    return f"{prefix}-{highest + 1:03d}"
