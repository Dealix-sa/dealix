"""Strict, caller-supplied JSON storage for private deal memory.

Malformed state raises an error instead of silently replacing the CRM with an
empty book. No default customer-data path is committed by this package.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .models import DealRecord

SCHEMA = "dealix.deal_intelligence.book.v1"


class DealBookError(RuntimeError):
    pass


@dataclass(frozen=True)
class DealBook:
    deals: tuple[DealRecord, ...] = field(default_factory=tuple)
    history: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "deals": [deal.to_dict() for deal in self.deals],
            "history": list(self.history[-365:]),
        }


def load_book(path: Path) -> DealBook:
    if not path.exists():
        return DealBook()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DealBookError(f"cannot read valid deal book: {path}") from exc
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise DealBookError("unsupported or missing deal-book schema")
    raw_deals = payload.get("deals")
    raw_history = payload.get("history", [])
    if not isinstance(raw_deals, list) or not isinstance(raw_history, list):
        raise DealBookError("deal book must contain deals and history lists")
    try:
        deals = tuple(DealRecord.from_dict(item) for item in raw_deals if isinstance(item, dict))
    except (TypeError, ValueError) as exc:
        raise DealBookError("deal book contains an invalid deal record") from exc
    if len(deals) != len(raw_deals):
        raise DealBookError("deal book contains a non-object deal entry")
    history = tuple(item for item in raw_history if isinstance(item, dict))
    if len(history) != len(raw_history):
        raise DealBookError("deal book contains a non-object history entry")
    return DealBook(deals=deals, history=history)


def save_book_atomic(book: DealBook, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(book.to_dict(), ensure_ascii=False, indent=2) + "\n"
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return path
