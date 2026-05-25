"""Track brand mentions and citations across AI answer engines (offline stub)."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

_MENTIONS: list["AIVisibilityRecord"] = []


@dataclass(frozen=True)
class AIVisibilityRecord:
    record_id: str
    brand: str
    engine: str
    query: str
    mention_position: int
    cited: bool
    captured_at: float


def record_mention(brand: str, engine: str, query: str, mention_position: int, cited: bool) -> AIVisibilityRecord:
    """Record an AI engine mention/citation observation."""
    r = AIVisibilityRecord(
        record_id=f"vis_{uuid.uuid4().hex[:8]}",
        brand=brand,
        engine=engine,
        query=query,
        mention_position=int(mention_position),
        cited=bool(cited),
        captured_at=time.time(),
    )
    _MENTIONS.append(r)
    return r


def visibility_rate(brand: str, engine: str | None = None) -> float:
    """Return the fraction of records (filtered to brand/engine) that included a citation."""
    pool = [m for m in _MENTIONS if m.brand == brand and (engine is None or m.engine == engine)]
    if not pool:
        return 0.0
    cited = sum(1 for m in pool if m.cited)
    return round(cited / len(pool), 4)


def reset() -> None:
    """Clear visibility records (test helper)."""
    _MENTIONS.clear()
