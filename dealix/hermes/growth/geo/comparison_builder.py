"""
Comparison-table builder — emits a machine-readable comparison row set
that AI engines can quote directly.
"""

from __future__ import annotations


def build_comparison_table(
    title: str,
    columns: list[str],
    rows: list[dict[str, str]],
) -> dict[str, object]:
    if not columns:
        raise ValueError("at least one column required")
    if not rows:
        raise ValueError("at least one row required")
    for r in rows:
        for c in columns:
            if c not in r:
                raise ValueError(f"row missing column {c!r}: {r}")
    return {
        "title": title,
        "columns": list(columns),
        "rows": [{c: r[c] for c in columns} for r in rows],
    }
