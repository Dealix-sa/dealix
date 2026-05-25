"""
Multi-touch attribution: weight each touch by position. First and last
get 0.35 each; the middle touches share 0.3 evenly.
"""

from __future__ import annotations

from typing import Any


def weights(touches: list[dict[str, Any]]) -> dict[str, float]:
    if not touches:
        return {}
    ordered = sorted(touches, key=lambda t: t.get("at", ""))
    n = len(ordered)
    out: dict[str, float] = {}
    if n == 1:
        out[str(ordered[0].get("source"))] = 1.0
        return out
    out[str(ordered[0].get("source"))] = 0.35
    out[str(ordered[-1].get("source"))] = out.get(str(ordered[-1].get("source")), 0.0) + 0.35
    if n > 2:
        share = 0.3 / (n - 2)
        for t in ordered[1:-1]:
            src = str(t.get("source"))
            out[src] = out.get(src, 0.0) + share
    return out
