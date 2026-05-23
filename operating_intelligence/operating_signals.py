"""
Operating signals.

A signal is a single observed reading the rest of operating_intelligence
consumes. The collector exists so callers don't construct dataclasses by
hand and so we can change the underlying representation later.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class OperatingSignal:
    name: str
    value: float
    unit: str
    observed_at: datetime


def collect_signals(readings: dict[str, tuple[float, str]]) -> list[OperatingSignal]:
    """Turn a dict of name -> (value, unit) into typed signals."""
    now = datetime.now(timezone.utc)
    return [
        OperatingSignal(name=k, value=float(v), unit=u, observed_at=now)
        for k, (v, u) in readings.items()
    ]
