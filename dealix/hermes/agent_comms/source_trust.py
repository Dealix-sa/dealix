"""Trust score per source: system | approved_agent | external | unknown."""

from __future__ import annotations

from dataclasses import dataclass

_TRUST_LEVELS: dict[str, int] = {
    "system": 100,
    "approved_agent": 75,
    "external": 30,
    "unknown": 0,
}


@dataclass(frozen=True)
class TrustScore:
    source: str
    level: str
    score: int


def trust_of(source: str) -> TrustScore:
    """Return TrustScore mapping a source label to a numeric trust level."""
    level = source if source in _TRUST_LEVELS else "unknown"
    return TrustScore(source=source, level=level, score=_TRUST_LEVELS[level])


def meets_threshold(source: str, minimum: int) -> bool:
    """Return True when trust(source) >= minimum."""
    return trust_of(source).score >= minimum
