"""
ComparisonBuilder — emit a structured comparison table that answer engines
can parse and re-cite.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComparisonTable:
    topic: str
    columns: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "topic": self.topic,
            "columns": list(self.columns),
            "rows": [list(r) for r in self.rows],
        }


def build_comparison(
    topic: str,
    *,
    columns: tuple[str, ...],
    rows: tuple[tuple[str, ...], ...],
) -> ComparisonTable:
    width = len(columns)
    for r in rows:
        if len(r) != width:
            raise ValueError(f"row width mismatch: expected {width}, got {len(r)}")
    return ComparisonTable(topic=topic, columns=columns, rows=rows)
