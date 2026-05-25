"""First-touch attribution: the first known channel gets full credit."""

from __future__ import annotations

from typing import Any


def attribute(touches: list[dict[str, Any]]) -> str | None:
    if not touches:
        return None
    ordered = sorted(touches, key=lambda t: t.get("at", ""))
    return str(ordered[0].get("source"))
