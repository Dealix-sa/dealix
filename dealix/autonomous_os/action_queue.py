"""
Action Queue — durable, file-backed queue of draft artifacts.

Internal, low-risk steps that clear the SafetyGate land here as *drafts*.
Nothing in this queue is external and nothing is ever auto-sent; the queue
simply records the draft work the OS prepared so a human can review it.

Storage: one JSON file per run day under <root>/actions/actions-<date>.json,
plus an append to an index. Everything is plain JSON so it is auditable and
diffable, and can live in a gitignored runtime directory.
"""

from __future__ import annotations

import datetime as dt
import json
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Action:
    id: str
    created_at: str
    strategy_id: str
    action: str
    offer: str | None
    status: str  # "draft_ready"
    summary: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ActionQueue:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root) / "actions"
        self.root.mkdir(parents=True, exist_ok=True)

    def _path_for(self, day: str) -> Path:
        return self.root / f"actions-{day}.json"

    def enqueue(
        self,
        *,
        strategy_id: str,
        action: str,
        summary: str,
        offer: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Action:
        now = dt.datetime.now(dt.timezone.utc)
        item = Action(
            id=str(uuid.uuid4()),
            created_at=now.isoformat(),
            strategy_id=strategy_id,
            action=action,
            offer=offer,
            status="draft_ready",
            summary=summary,
            payload=payload or {},
        )
        self._append(now.date().isoformat(), item)
        return item

    def _append(self, day: str, item: Action) -> None:
        path = self._path_for(day)
        existing = self._read(path)
        existing.append(item.to_dict())
        path.write_text(
            json.dumps({"day": day, "actions": existing}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _read(path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        data = json.loads(path.read_text(encoding="utf-8"))
        return list(data.get("actions", []))

    def list(self, day: str | None = None) -> list[dict[str, Any]]:
        day = day or dt.date.today().isoformat()
        return self._read(self._path_for(day))
