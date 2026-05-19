"""Append-only JSONL store for executive briefs.

Path resolves from ``DEALIX_EXECUTIVE_BRIEF_PATH`` (default
``var/executive-brief.jsonl``). Mirrors the audit-log convention so the
scheduled workflow can ship the file as an artifact.
"""

from __future__ import annotations

import contextlib
import json
import os
import threading
from pathlib import Path
from typing import Any

from auto_client_acquisition.executive_os.schemas import ExecutiveBrief

_DEFAULT_PATH = "var/executive-brief.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_EXECUTIVE_BRIEF_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def save_brief(brief: ExecutiveBrief) -> None:
    """Append one brief as a JSON line."""
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(brief.to_dict(), ensure_ascii=False) + "\n")


def load_latest_brief() -> dict[str, Any] | None:
    """Return the most recent brief as a dict, or ``None`` if none stored."""
    path = _path()
    if not path.exists():
        return None
    latest: dict[str, Any] | None = None
    with _lock, path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            with contextlib.suppress(Exception):
                latest = json.loads(line)
    return latest


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = ["clear_for_test", "load_latest_brief", "save_brief"]
