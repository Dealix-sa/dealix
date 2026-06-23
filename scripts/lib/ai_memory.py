"""Lightweight audit memory for AI routing decisions (V14).

Append-only JSONL log of every routing decision so a human can review what
was drafted and why. The default log path lives under ``reports/ai/`` (a
gitignored runtime directory). Persistence is opt-in: the router records
only when a sink is provided, keeping ``route()`` pure by default.
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG = REPO_ROOT / "reports" / "ai" / "router_audit.jsonl"


class RouterMemory:
    """Append-only audit log of routing decisions."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path else DEFAULT_LOG

    def record(self, entry: dict[str, Any]) -> None:
        payload = {"at": _dt.datetime.now(tz=_dt.UTC).isoformat(timespec="seconds"), **entry}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def recent(self, limit: int = 20) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").splitlines()
        out: list[dict[str, Any]] = []
        for line in lines[-limit:]:
            line = line.strip()
            if line:
                out.append(json.loads(line))
        return out
