"""
Proof Logger — append-only audit trail for the Autonomous OS.

Every meaningful event (plan produced, action drafted, approval requested,
step blocked, learning summary) is appended as one JSON line. The log is the
evidence base for the learning loop and for founder/compliance review, in the
spirit of the Dealix proof-pack doctrine.

Append-only JSONL keeps the trail tamper-evident-by-convention and easy to
tail, diff, and ship as an artifact.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


class ProofLogger:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root) / "proofs"
        self.root.mkdir(parents=True, exist_ok=True)

    def _path_for(self, day: str) -> Path:
        return self.root / f"proof-{day}.jsonl"

    def log(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        now = dt.datetime.now(dt.UTC)
        record = {
            "ts": now.isoformat(),
            "event_type": event_type,
            "payload": payload,
        }
        path = self._path_for(now.date().isoformat())
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def read(self, day: str | None = None) -> list[dict[str, Any]]:
        day = day or dt.date.today().isoformat()
        path = self._path_for(day)
        if not path.exists():
            return []
        out: list[dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                out.append(json.loads(line))
        return out

    def read_all(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for path in sorted(self.root.glob("proof-*.jsonl")):
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out
