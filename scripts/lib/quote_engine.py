"""Quote ledger helpers (V12 quote-to-cash).

Thin, deterministic JSON store wrapping
``business/_data/quotes.index.json``. Demo-safe: quotes are drafts only —
nothing is ever sent or charged from here. The deal desk and the website's
``/quotes`` route read the same index.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
QUOTES_PATH = REPO_ROOT / "business" / "_data" / "quotes.index.json"

_ID_RE = re.compile(r"(\d+)\s*$")


def now() -> str:
    """UTC ISO-8601 timestamp (seconds precision)."""
    return _dt.datetime.now(tz=_dt.UTC).isoformat(timespec="seconds")


def load_quotes() -> dict[str, Any]:
    """Load the quote index, tolerating a missing/empty file."""
    if not QUOTES_PATH.exists():
        return {"version": 1, "demo": True, "quotes": []}
    data = json.loads(QUOTES_PATH.read_text(encoding="utf-8"))
    data.setdefault("quotes", [])
    return data


def save_quotes(index: dict[str, Any]) -> None:
    """Persist the quote index (pretty-printed, UTF-8, Arabic-safe)."""
    QUOTES_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUOTES_PATH.write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def next_id(prefix: str, items: list[dict[str, Any]]) -> str:
    """Return the next ``PREFIX-NNN`` id given existing items.

    Reads the numeric suffix of each existing ``id`` and increments the max,
    so ids stay unique and monotonic even if the list is sparse.
    """
    highest = 0
    for it in items:
        raw = str(it.get("id", ""))
        m = _ID_RE.search(raw)
        if m:
            highest = max(highest, int(m.group(1)))
    return f"{prefix}-{highest + 1:03d}"
