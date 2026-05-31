"""Agent-influenced attribution: every agent that touched the deal gets a small share."""

from __future__ import annotations


def apply(weights: dict[str, float], agents: tuple[str, ...]) -> dict[str, float]:
    if not agents:
        return weights
    out = dict(weights)
    bump = 0.05
    for a in agents:
        out[f"agent:{a}"] = out.get(f"agent:{a}", 0.0) + bump
    return out
